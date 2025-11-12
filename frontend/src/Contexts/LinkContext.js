import React, { createContext, useState, useEffect, useContext } from 'react';

import db from 'Helper/db';

import ConfigContext from './ConfigContext';

const LinkContext = createContext();

export const LinkProvider = ({ children }) => {

    const { selectedConfig } = useContext(ConfigContext);

    const [links, setLinks] = useState([]);
    const [selectedLink, setSelectedLink] = useState(null);
    const [updateLinks, setUpdateLinks] = useState(false);

    const toggleUpdateLinks = () => {
        setUpdateLinks(!updateLinks);
    }

    const createLink = async (cid, sid) => {
        const default_settings = {
            "pattern": "flat",
            "colors": ["#100000"]
        }
        await db.createLink(cid, sid, "static", default_settings);
        toggleUpdateLinks();
    }

    const editLink = async (cid, sid, settings) => {
        await db.editLink(cid, sid, settings);
        toggleUpdateLinks();
    }

    const deleteLink = async (cid, sid) => {
        await db.deleteLink(cid, sid);
        toggleUpdateLinks();
    }

    useEffect(() => {
        if(!selectedConfig) { return; }
        const fetchLinks = async () => {
            const links = await db.getLinks(selectedConfig.cid);
            setLinks(links);
        };
        fetchLinks();
    }, [updateLinks, selectedConfig]);

    return (
        <LinkContext.Provider value={{ links,
                                        setLinks,
                                        selectedLink,
                                        setSelectedLink,
                                        updateLinks,
                                        setUpdateLinks,
                                        toggleUpdateLinks,
                                        createLink,
                                        editLink,
                                        deleteLink
                                    }}>
            { children }
        </LinkContext.Provider>
    );
};

export default LinkContext;