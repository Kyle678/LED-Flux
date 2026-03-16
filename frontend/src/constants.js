export const API_BASE = 'http://192.168.1.101:5000/api';

export const ANIMATION_PRESETS = {

  White: {
    animation_type: "white",
    name: "White",
    animations: 
    [{
      animation_type: "static",
      name: "White",
      num_pixels: 1500,
      colors: [[255, 255, 255]]
    }]
  }
}

export const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? [ parseInt(result[1], 16), parseInt(result[2], 16), parseInt(result[3], 16) ] : [255, 255, 255];
};

export const rgbToHex = (r, g, b) => {
  return "#" + ((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1);
};