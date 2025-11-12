import urls, { getResponse } from './urls';

const svrOp = {

    setPlay: async(config_id, value) => {
        const url = urls.setPlay + '/' + config_id;
        const data = {'value' : value}
        return await getResponse(url, 'POST', data);
    },

    getPlayStatus: async() => {
        const url = urls.getPlayStatus;
        const response = await getResponse(url);
        return response
    },

    setConfig: async (config_id) => {
        const url = urls.setConfig + '/' + config_id;
        return await getResponse(url, 'POST');
    },

    turnOff: async () => {
        const url = urls.turnOff;
        return await getResponse(url, 'POST');
    },

    setColor: async (color) => {
        const url = urls.setColor;
        const color_data = { 'hex': color };
        return await getResponse(url, 'POST', color_data);
    },

    setBrightness: async (brightness) => {
        const url = urls.setBrightness;
        const brightness_data = { 'brightness': brightness };
        return await getResponse(url, 'POST', brightness_data);
    },

    connectionTest: async () => {
        const url = urls.connectionTest;
        return await getResponse(url, 'GET');
    },

    getAnimations: async () => {
        const url = urls.getAnimations;
        return await getResponse(url, 'GET');
    },

    getDisplayTypes: async () => {
        const url = urls.getDisplayTypes;
        return await getResponse(url, 'GET');
    }

}

export default svrOp;