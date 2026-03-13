import React from 'react';
import { styles } from '../styles';
import { ANIMATION_PRESETS } from '../constants';

export default function QuickPresets({ triggerPreset }) {
  return (
    <div style={styles.section}>
      <h3 style={{ marginTop: '0', fontSize: '16px', color: '#fff' }}>Single Presets</h3>
      {Object.keys(ANIMATION_PRESETS).map((key) => (
        <button key={key} style={styles.presetButton} onClick={() => triggerPreset(key)}>
          {key.charAt(0).toUpperCase() + key.slice(1)}
        </button>
      ))}
    </div>
  );
}