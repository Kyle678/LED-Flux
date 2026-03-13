import React, { useState, useEffect, useRef } from 'react';

const API_BASE = 'http://192.168.1.101:5000/api';

const ANIMATION_PRESETS = {
  rainbow: { name: "rainbow", num_pixels: 1500, loop_duration: 10, target_fps: 30 },
  white: { name: "white", num_pixels: 1500, start_index: 0}
};

export default function App() {
  const [brightness, setBrightness] = useState(100);
  const [isOn, setIsOn] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // --- New State for Config Builder ---
  const [configList, setConfigList] = useState([]);
  const [builderType, setBuilderType] = useState('static');
  const [builderPixels, setBuilderPixels] = useState(100);
  const [builderStart, setBuilderStart] = useState(0);
  const [builderColor, setBuilderColor] = useState('#0000ff'); // Default blue
  
  const debounceTimer = useRef(null);

  // Fetch initial status on load
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();

        if (data.status === 'success') {
          setBrightness(data.data.brightness * 100 || 100);
          setIsOn(data.data.power || false);
          setIsPlaying(data.data.current_animation !== 'none'); 
        }
      } catch (error) {
        console.error("Could not reach LED API:", error);
      }
    };

    fetchStatus();
  }, []);

  // Handle Real-Time Brightness
  const handleBrightnessChange = (e) => {
    const newLevel = parseInt(e.target.value, 10);
    setBrightness(newLevel); 

    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    debounceTimer.current = setTimeout(async () => {
      try {
        await fetch(`${API_BASE}/brightness`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: "brightness", data: { value: newLevel / 100 } })
        });
      } catch (error) {
        console.error("Error setting brightness:", error);
      }
    }, 50); 
  };

  const togglePlayPause = async () => {
    const newState = !isPlaying;
    setIsPlaying(newState);
    const payload = { action: "pause", data: { "value": newState ? "on" : "off" } };

    await fetch(`${API_BASE}/pause`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  };

  const togglePower = async () => {
    const newState = !isOn;
    setIsOn(newState);
    await fetch(`${API_BASE}/power`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: "power", data: { value: newState ? "on" : "off" } })
    });
  };

  const triggerPreset = async (presetKey) => {
    const presetData = ANIMATION_PRESETS[presetKey];
    if (!presetData) return;

    try {
      await fetch(`${API_BASE}/animation`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: "animation", data: presetData })
      });
      setIsOn(true);
      setIsPlaying(true);
    } catch (error) {
      console.error(`Error setting preset:`, error);
    }
  };

  // --- New Config Builder Functions ---
  
  // Helper to convert hex color (#ff0000) to RGB array ([255, 0, 0])
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
      parseInt(result[1], 16),
      parseInt(result[2], 16),
      parseInt(result[3], 16)
    ] : [255, 255, 255];
  };

  const addAnimationToConfig = () => {
    const newAnim = {
      name: builderType,
      num_pixels: parseInt(builderPixels, 10),
      start_index: parseInt(builderStart, 10)
    };

    // Only add the color array if it's a static animation
    if (builderType === 'static') {
      newAnim.color = hexToRgb(builderColor);
    }

    setConfigList([...configList, newAnim]);
  };

  const removeFromConfig = (indexToRemove) => {
    setConfigList(configList.filter((_, index) => index !== indexToRemove));
  };

  const playConfig = async () => {
    if (configList.length === 0) return;

    const payload = {
      action: "config",
      data: {
        name: "custom-web-config",
        animations: configList
      }
    };

    try {
      await fetch(`${API_BASE}/config`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      setIsOn(true);
      setIsPlaying(true);
    } catch (error) {
      console.error(`Error sending config:`, error);
    }
  };

  // Styles
  const styles = {
    container: { maxWidth: '500px', margin: '40px auto', fontFamily: 'sans-serif', textAlign: 'center', padding: '20px', border: '1px solid #ddd', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
    button: { padding: '10px 20px', margin: '5px', fontSize: '14px', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#007BFF', color: 'white' },
    presetButton: { padding: '8px 16px', margin: '5px', fontSize: '14px', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#28a745', color: 'white' },
    actionButton: { padding: '10px 20px', margin: '15px 0', width: '100%', fontSize: '16px', fontWeight: 'bold', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#6f42c1', color: 'white' },
    slider: { width: '100%', cursor: 'pointer', marginTop: '10px' },
    section: { marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '8px', textAlign: 'left' },
    inputGroup: { display: 'flex', flexDirection: 'column', marginBottom: '10px', fontSize: '14px' },
    input: { padding: '8px', marginTop: '4px', borderRadius: '4px', border: '1px solid #ccc' },
    listItem: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px', borderBottom: '1px solid #ddd', fontSize: '13px' }
  };

  return (
    <div style={styles.container}>
      <h2>LED Flux Control</h2>
      
      <div>
        <button style={styles.button} onClick={togglePower}>
          {isOn ? '🔌 Turn Off' : '🔌 Turn On'}
        </button>
        <button style={styles.button} onClick={togglePlayPause}>
          {isPlaying ? '⏸ Pause' : '▶️ Play'}
        </button>
      </div>

      {/* Brightness Control */}
      <div style={styles.section}>
        <label><strong>Brightness:</strong> {brightness}</label>
        <input 
          type="range" min="0" max="100" step="1"
          value={brightness} onChange={handleBrightnessChange} 
          style={styles.slider}
        />
      </div>

      {/* Single Animation Presets */}
      <div style={styles.section}>
        <h3 style={{ marginTop: '0', fontSize: '16px' }}>Quick Presets</h3>
        {Object.keys(ANIMATION_PRESETS).map((key) => (
          <button key={key} style={styles.presetButton} onClick={() => triggerPreset(key)}>
            {key.charAt(0).toUpperCase() + key.slice(1)}
          </button>
        ))}
      </div>

      {/* 4. Multi-Animation Config Builder */}
      <div style={{...styles.section, backgroundColor: '#e9ecef'}}>
        <h3 style={{ marginTop: '0', fontSize: '16px' }}>Config Builder</h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          <div style={styles.inputGroup}>
            <label>Type</label>
            <select style={styles.input} value={builderType} onChange={(e) => setBuilderType(e.target.value)}>
              <option value="static">Static</option>
              <option value="rainbow">Rainbow</option>
              <option value="white">White</option>
            </select>
          </div>

          <div style={styles.inputGroup}>
            <label>Pixels</label>
            <input type="number" style={styles.input} value={builderPixels} onChange={(e) => setBuilderPixels(e.target.value)} />
          </div>

          <div style={styles.inputGroup}>
            <label>Start Index</label>
            <input type="number" style={styles.input} value={builderStart} onChange={(e) => setBuilderStart(e.target.value)} />
          </div>

          {builderType === 'static' && (
            <div style={styles.inputGroup}>
              <label>Color</label>
              <input type="color" style={{...styles.input, height: '34px', padding: '2px'}} value={builderColor} onChange={(e) => setBuilderColor(e.target.value)} />
            </div>
          )}
        </div>

        <button style={{...styles.button, width: '100%', marginTop: '10px', backgroundColor: '#17a2b8'}} onClick={addAnimationToConfig}>
          + Add to Config
        </button>

        {/* Staged Animations List */}
        {configList.length > 0 && (
          <div style={{ marginTop: '15px', backgroundColor: 'white', padding: '10px', borderRadius: '4px' }}>
            <h4 style={{ margin: '0 0 10px 0', fontSize: '14px' }}>Staged Animations:</h4>
            {configList.map((anim, index) => (
              <div key={index} style={styles.listItem}>
                <span>
                  <strong>{anim.name}</strong> ({anim.num_pixels}px @ idx {anim.start_index}) 
                  {anim.color && ` rgb(${anim.color.join(',')})`}
                </span>
                <button 
                  onClick={() => removeFromConfig(index)} 
                  style={{...styles.button, backgroundColor: '#dc3545', padding: '4px 8px', margin: '0'}}
                >
                  X
                </button>
              </div>
            ))}
            
            <button style={styles.actionButton} onClick={playConfig}>
              🚀 Play Config
            </button>
          </div>
        )}
      </div>

    </div>
  );
}