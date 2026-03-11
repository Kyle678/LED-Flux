import React, { useState, useEffect, useRef } from 'react';

const API_BASE = 'http://192.168.1.101:5000/api';

export default function App() {
  const [brightness, setBrightness] = useState(128);
  const [isOn, setIsOn] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // We use a ref to keep track of our debounce timer
  const debounceTimer = useRef(null);

  // 1. Fetch initial status on load
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.status === 'success' && data.state) {
          setBrightness(data.state.brightness || 128);
          setIsOn(data.state.is_on || false);
          // Guessing play state based on whether an animation is active
          setIsPlaying(data.state.current_animation !== 'none'); 
        }
      } catch (error) {
        console.error("Could not reach LED API:", error);
      }
    };

    fetchStatus();
  }, []);

  // 2. Handle Real-Time Brightness with Debouncing
  const handleBrightnessChange = (e) => {
    const newLevel = parseInt(e.target.value, 10);
    setBrightness(newLevel); // Instantly update UI

    // Clear the old timer if the user is still dragging
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Wait 50ms before sending. If they stop dragging, send the payload!
    debounceTimer.current = setTimeout(async () => {
      try {
        await fetch(`${API_BASE}/brightness`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // Sending the nested dictionary structure your engine expects
          body: JSON.stringify({ action: "brightness", data: { value: newLevel } })
        });
      } catch (error) {
        console.error("Error setting brightness:", error);
      }
    }, 50); 
  };

  // 3. Play/Pause Toggle
  const togglePlayPause = async () => {
    const newState = !isPlaying;
    setIsPlaying(newState);
    
    // Depending on your API, you might send an animation name or a pause command
    const payload = newState 
      ? { action: "animation", data: { name: "rainbow" } } 
      : { action: "clear", data: {} };

    await fetch(`${API_BASE}/${newState ? 'animation' : 'clear'}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  };

  // 4. Power Toggle
  const togglePower = async () => {
    const newState = !isOn;
    setIsOn(newState);
    // You'll need a route/handler for general power if you want it distinct from clear!
    console.log(`Power toggled: ${newState}`);
  };

  // Basic inline styles for a clean layout
  const styles = {
    container: { maxWidth: '400px', margin: '50px auto', fontFamily: 'sans-serif', textAlign: 'center', padding: '20px', border: '1px solid #ddd', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
    button: { padding: '10px 20px', margin: '10px', fontSize: '16px', cursor: 'pointer', borderRadius: '8px', border: 'none', backgroundColor: '#007BFF', color: 'white' },
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

      <div style={{ marginTop: '30px', textAlign: 'left' }}>
        <label>
          <strong>Brightness:</strong> {brightness}
        </label>
        <input 
          type="range" 
          min="0" 
          max="255" 
          value={brightness} 
          onChange={handleBrightnessChange} 
          style={styles.slider}
        />
      </div>
    </div>
  );
}