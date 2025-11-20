import React from "react";

export default function Animation({ animation, setAnimation }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setAnimation((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  return (
    <div className="animation-entry-box">
      <h1> Animation {animation.aid} </h1>
      <div className="animation-data-box">
        <h2> Name: {animation.name} </h2>
        <h3> Description: {animation.description} </h3>
        <div>
            {Object.entries(animation).map(([key, value], index) => (
            <div key={key}>
                <p>
                <span style={{ fontWeight: 'bold' }}>{key}:</span>{" "}
                {typeof value === 'object' && value !== null
                    ? JSON.stringify(value)
                    : String(value)}
                </p>
            </div>
            ))}
        </div>
      </div>
    </div>
  );
}