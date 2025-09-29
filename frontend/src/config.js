import React from "react";

export default function Config({ config, setConfig }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">LED Config</h1>

      <div className="space-y-3">
        <div>
          <label className="block font-medium">LED Count</label>
          <input
            type="number"
            name="ledCount"
            value={config.ledCount}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block font-medium">Update Speed (ms)</label>
          <input
            type="number"
            name="updateSpeed"
            value={config.updateSpeed}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block font-medium">Brightness (%)</label>
          <input
            type="number"
            name="brightness"
            value={config.brightness}
            onChange={handleChange}
            className="w-full border rounded p-2"
            min="0"
            max="100"
          />
        </div>
      </div>

      <div className="mt-6 p-4 border rounded bg-gray-50">
        <h2 className="font-semibold">Current Config</h2>
        <pre className="text-sm mt-2">{JSON.stringify(config, null, 2)}</pre>
      </div>
    </div>
  );
}
