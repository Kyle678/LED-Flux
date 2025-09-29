import React, { useState } from "react";

export default function SectionProfile({ sections }) {
  const animations = ["Fade", "Chase", "Rainbow", "Static"];

  const [selectedProfile, setSelectedProfile] = useState("");
  const [selectedAnimation, setSelectedAnimation] = useState("");
  const [applied, setApplied] = useState([]);

  const applyAnimation = () => {
    if (!selectedProfile || !selectedAnimation) return;
    const profile = sections.find((p) => p.name === selectedProfile);
    if (!profile) return;

    setApplied((prev) => [...prev, { ...profile, animation: selectedAnimation }]);
    setSelectedProfile("");
    setSelectedAnimation("");
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Section Profile</h1>

      {sections.length === 0 ? (
        <p className="text-gray-500">No sections created yet.</p>
      ) : (
        <div className="space-y-3">
          <div>
            <label className="block font-medium">Select Profile</label>
            <select
              value={selectedProfile}
              onChange={(e) => setSelectedProfile(e.target.value)}
              className="w-full border rounded p-2"
            >
              <option value="">-- Choose a Section --</option>
              {sections.map((p, i) => (
                <option key={i} value={p.name}>
                  {p.name} (Start: {p.startIndex}, Len: {p.length})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block font-medium">Select Animation</label>
            <select
              value={selectedAnimation}
              onChange={(e) => setSelectedAnimation(e.target.value)}
              className="w-full border rounded p-2"
            >
              <option value="">-- Choose an Animation --</option>
              {animations.map((a, i) => (
                <option key={i} value={a}>
                  {a}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={applyAnimation}
            className="w-full bg-blue-500 text-white rounded p-2 hover:bg-blue-600"
          >
            Apply
          </button>
        </div>
      )}

      <div className="mt-6 space-y-2">
        <h2 className="font-semibold">Applied Profiles</h2>
        {applied.length === 0 && (
          <p className="text-sm text-gray-500">No profiles set yet.</p>
        )}
        {applied.map((a, i) => (
          <div key={i} className="border rounded p-3 bg-gray-50 shadow-sm">
            <p className="font-medium">{a.name}</p>
            <p className="text-sm text-gray-600">
              Start: {a.startIndex}, Length: {a.length}
            </p>
            <p className="text-sm">Animation: {a.animation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
