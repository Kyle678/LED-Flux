import React from "react";
import svrOp from "./Helper/svr";

export default function Config({ config, setConfig, isSelected }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  return (
    <div className={`config-entry-box ${isSelected ? 'selected' : ''}`} onClick={() => setConfig(config)}>
      <h1> Config {config.cid} </h1>
      <div className="config-data-box">
        <h2> Name: {config.name} </h2>
        <h3> Description: {config.description} </h3>
        <div>{JSON.stringify(config)}</div>
        <button onClick={async () => {
          const response = await svrOp.playConfig(config.cid);
        }}>Play Config</button>
      </div>
    </div>
  );
}
