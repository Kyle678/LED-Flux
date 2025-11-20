import urls, { getResponse } from './urls';

const dbOp = {

//------------------------------------------------------------
// Configs

    createConfig: async (name, description) => {
        const url = urls.createConfig;
        const config_data = { name, description };
        return await getResponse(url, 'POST', config_data);
    },

    deleteConfig: async (cid) => {
        const url = urls.deleteConfig + '/' + cid;
        return await getResponse(url, 'DELETE');
    },

    editConfig: async (cid, name, description) => {
        const url = urls.editConfig + '/' + cid;
        const config_data = { name, description };
        return await getResponse(url, 'PUT', config_data);
    },

    getConfigs: async () => {
        const url = urls.getConfigs;
        return await getResponse(url, 'GET');
    },

    getConfig: async (cid) => {
        const url = urls.getConfig + '/' + cid;
        return await getResponse(url, 'GET');
    },

//------------------------------------------------------------
// Animations

    createAnimation: async (name, type, settings) => {
        const url = urls.createAnimation;
        const animation_data = { name, type, settings };
        return await getResponse(url, 'POST', animation_data);
    },

    deleteAnimation: async (aid) => {
        const url = urls.deleteAnimation + '/' + aid;
        return await getResponse(url, 'DELETE');
    },

    editAnimation: async (aid, name, type, settings) => {
        const url = urls.editAnimation + '/' + aid;
        const animation_data = { name, type, settings };
        return await getResponse(url, 'PUT', animation_data);
    },

    getAnimations: async () => {
        const url = urls.getAnimations;
        return await getResponse(url, 'GET');
    },

    getAnimation: async (aid) => {
        const url = urls.getAnimation + '/' + aid;
        return await getResponse(url, 'GET');
    },

//----------------------------------------------------------
// Sections

    createSection: async (name, start, length) => {
        const url = urls.createSection;
        const section_data = { name, start, length };
        return await getResponse(url, 'POST', section_data);
    },

    deleteSection: async (sid) => {
        const url = urls.deleteSection + '/' + sid;
        return await getResponse(url, 'DELETE');
    },

    editSection: async (sid, name, start, length) => {
        const url = urls.editSection + '/' + sid;
        const section_data = { name, start, length };
        return await getResponse(url, 'PUT', section_data);
    },

    getSections: async () => {
        const url = urls.getSections;
        return await getResponse(url, 'GET');
    },

    getSection: async (sid) => {
        const url = urls.getSection + '/' + sid;
        return await getResponse(url, 'GET');
    },

//------------------------------------------------------------
// Relations

    createRelation: async (cid, sid, type, settings) => {
        const url = urls.createRelation;
        const Relation_data = { cid, sid, type, settings };
        return await getResponse(url, 'POST', Relation_data);
    },

    deleteRelation: async (cid, sid) => {
        const url = urls.deleteRelation + '/' + cid + '/' + sid;
        return await getResponse(url, 'DELETE');
    },

    editRelation: async (cid, sid, form_data) => {
        const url = urls.editRelation + '/' + cid + '/' + sid;
        return await getResponse(url, 'PUT', form_data);
    },

    getRelations: async (cid) => {
        const url = urls.getRelations + '/' + cid;
        return await getResponse(url, 'GET');
    },

    getRelation: async (cid, sid) => {
        const url = urls.getRelation + '/' + cid + '/' + sid;
        return await getResponse(url, 'GET');
    }
};

export default dbOp;
