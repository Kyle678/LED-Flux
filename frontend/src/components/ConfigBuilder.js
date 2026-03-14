import React, { useState } from 'react';
import { styles } from '../styles';
import { hexToRgb, rgbToHex } from '../constants';

export default function ConfigBuilder({ configList, setConfigList, configName, setConfigName, playConfig, saveCurrentConfig }) {
  const [builderType, setBuilderType] = useState('static');
  const [builderPixels, setBuilderPixels] = useState(100);
  const [builderStart, setBuilderStart] = useState(0);
  const [builderColor, setBuilderColor] = useState('#0000ff'); 
  // New state for the rotating color list
  const [builderColorList, setBuilderColorList] = useState(['#ff0000', '#00ff00', '#0000ff']);
  const [editingAnimIndex, setEditingAnimIndex] = useState(null);

  // Helpers for managing the dynamic color list
  const handleColorListChange = (index, newColor) => {
    const newList = [...builderColorList];
    newList[index] = newColor;
    setBuilderColorList(newList);
  };
  
  const addColorToList = () => {
    setBuilderColorList([...builderColorList, '#ffffff']);
  };

  const removeColorFromList = (indexToRemove) => {
    setBuilderColorList(builderColorList.filter((_, index) => index !== indexToRemove));
  };

  const addOrUpdateAnimation = () => {
    const newAnim = {
      name: builderType,
      num_pixels: parseInt(builderPixels, 10),
      start_index: parseInt(builderStart, 10)
    };
    
    // Attach the appropriate color data based on type
    if (builderType === 'static') {
      newAnim.color = hexToRgb(builderColor);
    } else if (builderType === 'rotating') {
      newAnim.colors = builderColorList.map(hex => hexToRgb(hex));
    }

    if (editingAnimIndex !== null) {
      const updatedList = [...configList];
      updatedList[editingAnimIndex] = newAnim;
      setConfigList(updatedList);
      setEditingAnimIndex(null); 
    } else {
      setConfigList([...configList, newAnim]);
    }
  };

  const loadAnimForEditing = (index) => {
    const anim = configList[index];
    setBuilderType(anim.name);
    setBuilderPixels(anim.num_pixels);
    setBuilderStart(anim.start_index);
    
    // Load existing color(s) into the builder
    if (anim.name === 'static' && anim.color) {
      setBuilderColor(rgbToHex(anim.color[0], anim.color[1], anim.color[2]));
    } else if (anim.name === 'rotating' && anim.colors) {
      setBuilderColorList(anim.colors.map(c => rgbToHex(c[0], c[1], c[2])));
    }
    
    setEditingAnimIndex(index);
  };

  const cancelEdit = () => setEditingAnimIndex(null);

  const removeFromConfig = (indexToRemove) => {
    setConfigList(configList.filter((_, index) => index !== indexToRemove));
    if (editingAnimIndex === indexToRemove) setEditingAnimIndex(null);
  };

  return (
    <div style={{...styles.section, backgroundColor: '#222'}}>
      <h3 style={{ marginTop: '0', fontSize: '16px', color: '#fff' }}>Build Custom Scene</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        <div style={styles.inputGroup}>
          <label>Type</label>
          <select style={styles.input} value={builderType} onChange={(e) => setBuilderType(e.target.value)}>
            <option value="static">Static</option>
            <option value="rotating">Rotating</option>
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
        
        {/* Single Color Input for Static */}
        {builderType === 'static' && (
          <div style={styles.inputGroup}>
            <label>Color</label>
            <input type="color" style={{...styles.input, height: '34px', padding: '2px', cursor: 'pointer'}} value={builderColor} onChange={(e) => setBuilderColor(e.target.value)} />
          </div>
        )}
      </div>

      {/* Multiple Color Inputs for Rotating (Spans full width) */}
      {builderType === 'rotating' && (
        <div style={{...styles.inputGroup, marginTop: '10px'}}>
          <label>Colors</label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '4px' }}>
            {builderColorList.map((color, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', backgroundColor: '#333', padding: '2px', borderRadius: '4px' }}>
                <input 
                  type="color" 
                  style={{ width: '30px', height: '30px', padding: '0', border: 'none', cursor: 'pointer', background: 'none' }} 
                  value={color} 
                  onChange={(e) => handleColorListChange(index, e.target.value)} 
                />
                {builderColorList.length > 1 && (
                  <button 
                    style={{ background: 'none', border: 'none', color: '#dc3545', cursor: 'pointer', padding: '0 4px', fontWeight: 'bold' }} 
                    onClick={() => removeColorFromList(index)}
                    title="Remove Color"
                  >
                    X
                  </button>
                )}
              </div>
            ))}
            <button 
              style={{...styles.button, backgroundColor: '#444', color: '#fff', margin: '0', padding: '4px 10px', fontSize: '12px'}} 
              onClick={addColorToList}
            >
              + Add Color
            </button>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
        <button 
          style={{...styles.button, flex: 1, backgroundColor: editingAnimIndex !== null ? '#ffc107' : '#0dcaf0', color: '#000', fontWeight: 'bold', margin: 0}} 
          onClick={addOrUpdateAnimation}
        >
          {editingAnimIndex !== null ? '✓ Update Animation' : '+ Add to Scene'}
        </button>
        {editingAnimIndex !== null && (
          <button style={{...styles.button, backgroundColor: '#6c757d', margin: 0}} onClick={cancelEdit}>Cancel</button>
        )}
      </div>

      {configList.length > 0 && (
        <div style={{ marginTop: '15px', backgroundColor: '#1a1a1a', padding: '10px', borderRadius: '6px', border: '1px solid #333' }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#fff' }}>
            {configName ? `Editing: ${configName}` : 'Staged Animations:'}
          </h4>
          {configList.map((anim, index) => (
            <div key={index} style={{...styles.listItem, backgroundColor: editingAnimIndex === index ? '#333' : 'transparent'}}>
              <span style={{ color: '#ddd' }}>
                <strong style={{ color: '#fff' }}>{anim.name}</strong> ({anim.num_pixels}px @ idx {anim.start_index})
                {/* Optional: Show a tiny preview indicator of the colors */}
                {anim.name === 'rotating' && anim.colors && ` [${anim.colors.length} colors]`}
              </span>
              <div style={{ display: 'flex' }}>
                <button onClick={() => loadAnimForEditing(index)} style={{...styles.button, backgroundColor: '#0d6efd', padding: '4px 8px', margin: '0 5px 0 0'}}>✏️</button>
                <button onClick={() => removeFromConfig(index)} style={{...styles.button, backgroundColor: '#dc3545', padding: '4px 8px', margin: '0'}}>X</button>
              </div>
            </div>
          ))}
          
          <button style={{...styles.actionButton, backgroundColor: '#198754', marginTop: '15px'}} onClick={() => playConfig({ name: "unsaved-test", animations: configList })}>
            ▶️ Test Current Scene
          </button>

          <div style={{...styles.inputGroup, marginTop: '15px', borderTop: '1px solid #444', paddingTop: '15px'}}>
            <label><strong style={{ color: '#fff' }}>Save to Database</strong></label>
            <div style={{ display: 'flex', gap: '10px' }}>
              <input type="text" placeholder="e.g., 'Party Mode'" style={{...styles.input, flex: 1}} value={configName} onChange={(e) => setConfigName(e.target.value)} />
              <button style={{...styles.button, backgroundColor: '#6f42c1', margin: 0, marginTop: '4px'}} onClick={saveCurrentConfig}>
                💾 Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}