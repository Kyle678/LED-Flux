import React, { createContext, useState, useEffect } from 'react';

import db from '../Helper/db';

const SectionContext = createContext();

export const SectionProvider = ({ children }) => {
    const [sections, setSections] = useState([]);
    const [selectedSection, setSelectedSection] = useState(null);
    const [updateSections, setUpdateSections] = useState(false);
    const [addSectionIsOpen, setAddSectionIsOpen] = useState(false);

    const toggleUpdateSections = () => {
        setUpdateSections(!updateSections);
    }

    const openEditSectionMenu = (sid) => {
        setAddSectionIsOpen(sid);
    }

    const openAddSectionMenu = () => {
        setAddSectionIsOpen(true);
    }

    const createSection = async (name, start, length) => {
        await db.createSection(name, start, length);
        toggleUpdateSections();
    }

    const editSection = async (sid, name, start, length) => {
        await db.editSection(sid, name, start, length);
        toggleUpdateSections();
    }

    const deleteSection = async (sid) => {
        await db.deleteSection(sid);
        toggleUpdateSections();
    }

    useEffect(() => {
        const fetchSections = async () => {
            const sections = await db.getSections();
            setSections(sections);
        };
        fetchSections();
    }, [updateSections]);

    return (
        <SectionContext.Provider value={{ sections,
                                        setSections,
                                        selectedSection,
                                        setSelectedSection,
                                        updateSections,
                                        setUpdateSections,
                                        addSectionIsOpen,
                                        setAddSectionIsOpen,
                                        toggleUpdateSections,
                                        openEditSectionMenu,
                                        openAddSectionMenu,
                                        createSection,
                                        editSection,
                                        deleteSection
                                    }}>
            { children }
        </SectionContext.Provider>
    );
};

export default SectionContext;