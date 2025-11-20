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
    <div className="config-entry-box">
      <h1> Config {config.cid} </h1>
      <div className="config-data-box">
        <h2> Name: {config.name} </h2>
        <h3> Description: {config.description} </h3>
        <div>{JSON.stringify(config)}</div>
      </div>
    </div>
  );
}
