import React, { useState } from 'react';
import { styles } from '../styles';
import { hexToRgb, rgbToHex } from '../constants';

export default function ConfigBuilder({ configList, setConfigList, configName, setConfigName, playConfig, saveCurrentConfig }) {
  const [builderType, setBuilderType] = useState('static');
  const [builderPixels, setBuilderPixels] = useState(100);
  const [builderStart, setBuilderStart] = useState(0);
  const [builderColor, setBuilderColor] = useState('#0000ff'); 
  const [editingAnimIndex, setEditingAnimIndex] = useState(null);

  const addOrUpdateAnimation = () => {
    const newAnim = {
      name: builderType,
      num_pixels: parseInt(builderPixels, 10),
      start_index: parseInt(builderStart, 10)
    };
    if (builderType === 'static') newAnim.color = hexToRgb(builderColor);

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
    if (anim.color) setBuilderColor(rgbToHex(anim.color[0], anim.color[1], anim.color[2]));
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
            <input type="color" style={{...styles.input, height: '34px', padding: '2px', cursor: 'pointer'}} value={builderColor} onChange={(e) => setBuilderColor(e.target.value)} />
          </div>
        )}
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
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