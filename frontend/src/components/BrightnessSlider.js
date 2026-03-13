import React from 'react';
import { styles } from '../styles';

export default function BrightnessSlider({ brightness, handleBrightnessChange }) {
  return (
    <div style={styles.section}>
      <label style={{ color: '#fff' }}><strong>Brightness:</strong> {brightness}</label>
      <input 
        type="range" min="0" max="100" step="1" 
        value={brightness} onChange={handleBrightnessChange} 
        style={styles.slider} 
      />
    </div>
  );
}