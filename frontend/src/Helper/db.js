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
// Links

    createLink: async (cid, sid, type, settings) => {
        const url = urls.createLink;
        const link_data = { cid, sid, type, settings };
        return await getResponse(url, 'POST', link_data);
    },

    deleteLink: async (cid, sid) => {
        const url = urls.deleteLink + '/' + cid + '/' + sid;
        return await getResponse(url, 'DELETE');
    },

    editLink: async (cid, sid, form_data) => {
        const url = urls.editLink + '/' + cid + '/' + sid;
        return await getResponse(url, 'PUT', form_data);
    },

    getLinks: async (cid) => {
        const url = urls.getLinks + '/' + cid;
        return await getResponse(url, 'GET');
    },

    getLink: async (cid, sid) => {
        const url = urls.getLink + '/' + cid + '/' + sid;
        return await getResponse(url, 'GET');
    }
};

export default dbOp;
