const baseUrl = 'http://192.168.1.101:5000';

const partial_urls = {
    connectionTest: 'connectionTest',
    powerStatus: 'getPowerStatus',
    getAnimationTypes: 'getAnimationTypes',
    getAnimations: 'getAnimations',
    getDisplayTypes: 'getDisplayTypes',
    setConfig: 'setConfig',
    turnOff: 'turnOff',
    setColor: 'setColor',
    setBrightness: 'setBrightness',
    setPlay: 'setPlay',
    getPlayStatus: 'getPlayStatus',

    createConfig: 'createConfig',
    deleteConfig: 'deleteConfig',
    editConfig: 'editConfig',
    getConfigs: 'getConfigs',
    getConfig: 'getConfig',

    createSection: 'createSection',
    deleteSection: 'deleteSection',
    editSection: 'editSection',
    getSections: 'getSections',
    getSection: 'getSection',

    createLink: 'createLink',
    deleteLink: 'deleteLink',
    editLink: 'editLink',
    getLinks: 'getLinks',
    getLink: 'getLink'
};

const urls = {}

for(const key in partial_urls) {
    urls[key] = `${baseUrl}/${partial_urls[key]}`
}

export const getResponse = async (url, method, data) => {
    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: data ? JSON.stringify(data) : null,
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error at', url, ':', error);
        return;
    }
}

export default urls;