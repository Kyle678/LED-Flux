import React, { useState, useEffect, useRef } from 'react';

const API_BASE = 'http://192.168.1.101:5000/api';

// 1. Preset Dictionary - Just add new entries here to expand your UI!
const ANIMATION_PRESETS = {
  rainbow: { name: "rainbow", num_pixels: 1500, loop_duration: 10, target_fps: 30 },
  white: { name: "white", num_pixels: 1500, start_index: 0}
};

export default function App() {
  const [brightness, setBrightness] = useState(100);
  const [isOn, setIsOn] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // We use a ref to keep track of our debounce timer
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
          // Guessing play state based on whether an animation is active
          setIsPlaying(data.data.current_animation !== 'none'); 
        }
      } catch (error) {
        console.error("Could not reach LED API:", error);
      }
    };

    fetchStatus();
  }, []);

  // Handle Real-Time Brightness with Debouncing
  const handleBrightnessChange = (e) => {
    const newLevel = parseInt(e.target.value, 10);
    setBrightness(newLevel); // Instantly update UI

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

  // Play/Pause Toggle
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

  // Power Toggle
  const togglePower = async () => {
    const newState = !isOn;
    setIsOn(newState);
    await fetch(`${API_BASE}/power`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: "power", data: { value: newState ? "on" : "off" } })
    });
  };

  // 2. Preset Handler
  const triggerPreset = async (presetKey) => {
    const presetData = ANIMATION_PRESETS[presetKey];
    if (!presetData) return;

    try {
      // Assuming your endpoint matches the action name like your other routes
      await fetch(`${API_BASE}/animation`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: "animation",
          data: presetData
        })
      });
      
      // Update UI state to reflect the new animation
      setIsOn(true);
      setIsPlaying(true);
    } catch (error) {
      console.error(`Error setting ${presetKey} preset:`, error);
    }
  };

  // Basic inline styles for a clean layout
  const styles = {
    container: { maxWidth: '400px', margin: '50px auto', fontFamily: 'sans-serif', textAlign: 'center', padding: '20px', border: '1px solid #ddd', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
    button: { padding: '10px 20px', margin: '10px', fontSize: '16px', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#007BFF', color: 'white' },
    presetButton: { padding: '8px 16px', margin: '5px', fontSize: '14px', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#28a745', color: 'white' },
    slider: { width: '100%', cursor: 'pointer', marginTop: '10px' }
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

      {/* 3. Dynamic Presets UI */}
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
        <h3 style={{ marginTop: '0', fontSize: '16px', color: '#333' }}>Presets</h3>
        {Object.keys(ANIMATION_PRESETS).map((key) => (
          <button 
            key={key} 
            style={styles.presetButton} 
            onClick={() => triggerPreset(key)}
          >
            {/* Capitalize the first letter for the button label */}
            {key.charAt(0).toUpperCase() + key.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ marginTop: '30px', textAlign: 'left' }}>
        <label>
          <strong>Brightness:</strong> {brightness}
        </label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          step="1"
          value={brightness} 
          onChange={handleBrightnessChange} 
          style={styles.slider}
        />
      </div>
    </div>
  );
}