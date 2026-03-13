import React, { useState, useEffect, useRef } from 'react';
import { API_BASE, ANIMATION_PRESETS } from './constants';
import { styles } from './styles';

import MainControls from './components/MainControls';
import BrightnessSlider from './components/BrightnessSlider';
import QuickPresets from './components/QuickPresets';
import SavedScenes from './components/SavedScenes';
import ConfigBuilder from './components/ConfigBuilder';

export default function App() {
  const [brightness, setBrightness] = useState(100);
  const [isOn, setIsOn] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const [configList, setConfigList] = useState([]);
  const [configName, setConfigName] = useState('');
  const [savedConfigs, setSavedConfigs] = useState([]);
  
  const debounceTimer = useRef(null);

  const fetchSavedConfigs = async () => {
    try {
      const response = await fetch(`${API_BASE}/configs`);
      const data = await response.json();
      if (data.status === 'success') setSavedConfigs(data.data); 
    } catch (error) { console.error("Could not fetch saved configs:", error); }
  };

  useEffect(() => {
    document.body.style.backgroundColor = '#000000';
    document.body.style.color = '#e0e0e0';

    const fetchStatus = async () => {
      try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        if (data.status === 'success') {
          setBrightness(data.data.brightness * 100 || 100);
          setIsOn(data.data.power || false);
          setIsPlaying(data.data.current_animation !== 'none'); 
        }
      } catch (error) { console.error("Could not reach LED API:", error); }
    };

    fetchStatus();
    fetchSavedConfigs();
  }, []);

  const handleBrightnessChange = (e) => {
    const newLevel = parseInt(e.target.value, 10);
    setBrightness(newLevel); 
    if (debounceTimer.current) clearTimeout(debounceTimer.current);

    debounceTimer.current = setTimeout(async () => {
      try {
        await fetch(`${API_BASE}/brightness`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: "brightness", data: { value: newLevel / 100 } })
        });
      } catch (error) { console.error("Error setting brightness:", error); }
    }, 50); 
  };

  const togglePlayPause = async () => {
    const newState = !isPlaying;
    setIsPlaying(newState);
    await fetch(`${API_BASE}/pause`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: "pause", data: { "value": newState ? "on" : "off" } })
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
      setIsOn(true); setIsPlaying(true);
    } catch (error) { console.error(`Error setting preset:`, error); }
  };

  const playConfig = async (configData) => {
    try {
      await fetch(`${API_BASE}/config`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: "config", data: configData })
      });
      setIsOn(true); setIsPlaying(true);
    } catch (error) { console.error(`Error sending config:`, error); }
  };

  const loadConfigForEditing = (config) => {
    setConfigName(config.name);
    setConfigList([...config.animations]); 
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  const deleteSavedConfig = async (name) => {
    if (!window.confirm(`Are you sure you want to delete '${name}'?`)) return;
    try {
      const response = await fetch(`${API_BASE}/configs/${encodeURIComponent(name)}`, { method: 'DELETE' });
      if ((await response.json()).status === 'success') fetchSavedConfigs(); 
    } catch (error) { console.error("Error deleting config:", error); }
  };

  const saveCurrentConfig = async () => {
    if (!configName || configList.length === 0) {
      alert("Please provide a name and add at least one animation.");
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/configs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: configName, animations: configList })
      });
      
      if ((await response.json()).status === 'success') {
        fetchSavedConfigs();
        setConfigList([]);
        setConfigName('');
      }
    } catch (error) { console.error("Error saving config:", error); }
  };

  return (
    <div style={styles.container}>
      <h2 style={{ color: '#fff' }}>LED Flux Control</h2>
      
      <MainControls 
        isOn={isOn} isPlaying={isPlaying} 
        togglePower={togglePower} togglePlayPause={togglePlayPause} 
      />
      
      <BrightnessSlider 
        brightness={brightness} handleBrightnessChange={handleBrightnessChange} 
      />
      
      <QuickPresets triggerPreset={triggerPreset} />
      
      <SavedScenes 
        savedConfigs={savedConfigs} 
        playConfig={playConfig} 
        loadConfigForEditing={loadConfigForEditing} 
        deleteSavedConfig={deleteSavedConfig} 
      />
      
      <ConfigBuilder 
        configList={configList} setConfigList={setConfigList}
        configName={configName} setConfigName={setConfigName}
        playConfig={playConfig} saveCurrentConfig={saveCurrentConfig}
      />
    </div>
  );
}