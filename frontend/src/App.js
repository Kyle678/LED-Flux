import React, { useEffect, useState } from "react";
import Config from "./config";
import Animation from "./animation";
import dbOp from "./Helper/db";
import urls from "./Helper/urls";
import "./leds.css";

function App() {

  const [configs, setConfigs] = useState([]);
  const [animations, setAnimations] = useState([]);
  const [relations, setRelations] = useState([]);

  const [configName, setConfigName] = useState("");
  const [configDescription, setConfigDescription] = useState("");

  useEffect(() => {
    const fetchConfigs = async () => {
      const configs = await dbOp.getConfigs();
      console.log("configs:", configs);
      setConfigs(configs);
    }
    fetchConfigs();
  }, [])

  useEffect(() => {
    const fetchAnimations = async () => {
      const animations = await dbOp.getAnimations();
      console.log("animations:", animations);
      setAnimations(animations);
    }
    fetchAnimations();
  }, [])

  useEffect(() => {
    const fetchRelations = async () => {
      const relations = await dbOp.getRelations(1);
      console.log(relations);
      setRelations(relations);
    }
    fetchRelations();
  }, [])

  return (
    <div className="boxes">
      <div className="config-box">
        {configs.map((config, index) => (
          <Config key={index} config={config} />
        ))}
        <input type="text" placeholder="Config Name" value={configName} onChange={(e) => setConfigName(e.target.value)}/>
        <input type="text" placeholder="Description" value={configDescription} onChange={(e) => setConfigDescription(e.target.value)}/>
        <input type="button" value="Add Config" onClick={async () => {
          const new_config = await dbOp.createConfig("New Config", "Description");
          setConfigs((prev) => [...prev, new_config]);
        }} />
      </div>
      <div className="animations-box">
        {animations.map((animation, index) => (
          <Animation key={index} animation={animation} />
        ))}
      </div>
    </div>
  );
}

export default App;
