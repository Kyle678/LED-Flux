import React, { createContext, useState, useEffect } from 'react';

import db from '../Helper/db';

const ConfigContext = createContext();

export const ConfigProvider = ({ children }) => {
    const [configs, setConfigs] = useState([]);
    const [selectedConfig, setSelectedConfig] = useState(null);
    const [updateConfigs, setUpdateConfigs] = useState(false);
    const [addConfigIsOpen, setAddConfigIsOpen] = useState(false);

    const toggleUpdateConfigs = () => {
        setUpdateConfigs(!updateConfigs);
    }

    const openEditConfigMenu = (cid) => {
        setAddConfigIsOpen(cid);
    }

    const openAddConfigMenu = () => {
        setAddConfigIsOpen(true);
    }

    const createConfig = async (name, description) => {
        await db.createConfig(name, description);
        toggleUpdateConfigs();
    }

    const editConfig = async (cid, name, description) => {
        await db.editConfig(cid, name, description);
        toggleUpdateConfigs();
    }

    const deleteConfig = async (cid) => {
        await db.deleteConfig(cid);
        if(selectedConfig && selectedConfig.cid===cid){
            setSelectedConfig(null);
        }
        toggleUpdateConfigs();
    }

    useEffect(() => {
        const fetchConfigs = async () => {
            const configs = await db.getConfigs();
            setConfigs(configs);
        };
        fetchConfigs();
    }, [updateConfigs]);

    return (
        <ConfigContext.Provider value={{ configs,
                                        setConfigs,
                                        selectedConfig,
                                        setSelectedConfig,
                                        updateConfigs,
                                        setUpdateConfigs,
                                        addConfigIsOpen,
                                        setAddConfigIsOpen,
                                        openAddConfigMenu,
                                        openEditConfigMenu,
                                        createConfig,
                                        editConfig,
                                        deleteConfig,
                                        toggleUpdateConfigs
                                    }}>
            { children }
        </ConfigContext.Provider>
    );
};

export default ConfigContext;