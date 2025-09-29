import React, { useState } from "react";

function Sections({ sections, setSections }) {
  const [form, setForm] = useState({
    name: "",
    description: "",
    startIndex: "",
    length: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const addSection = (e) => {
    e.preventDefault();
    if (!form.name || !form.startIndex || !form.length) return;

    setSections((prev) => [
      ...prev,
      {
        ...form,
        startIndex: parseInt(form.startIndex, 10),
        length: parseInt(form.length, 10),
      },
    ]);

    setForm({ name: "", description: "", startIndex: "", length: "" });
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Sections</h1>

      <form onSubmit={addSection} className="space-y-3">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          className="w-full border rounded p-2"
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          className="w-full border rounded p-2"
        />
        <input
          type="number"
          name="startIndex"
          placeholder="Start Index"
          value={form.startIndex}
          onChange={handleChange}
          className="w-full border rounded p-2"
        />
        <input
          type="number"
          name="length"
          placeholder="Length"
          value={form.length}
          onChange={handleChange}
          className="w-full border rounded p-2"
        />

        <button
          type="submit"
          className="w-full bg-blue-500 text-white rounded p-2 hover:bg-blue-600"
        >
          Add Section
        </button>
      </form>

      <ul className="mt-6 space-y-2">
        {sections.map((sec, i) => (
          <li key={i} className="border rounded p-3 shadow-sm">
            <h2 className="font-semibold">{sec.name}</h2>
            <p className="text-sm text-gray-600">{sec.description}</p>
            <p className="text-sm">
              Start: {sec.startIndex}, Length: {sec.length}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sections;
