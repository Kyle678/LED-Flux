const baseUrl = 'http://192.168.1.101:5000';

const partial_urls = {

    createConfig: 'configs',
    deleteConfig: 'configs',
    editConfig: 'configs',
    getConfigs: 'configs',
    getConfig: 'configs',

    createAnimation: 'animations',
    deleteAnimation: 'animations',
    editAnimation: 'animations',
    getAnimations: 'animations',
    getAnimation: 'animations',

    createSection: 'sections',
    deleteSection: 'sections',
    editSection: 'sections',
    getSections: 'sections',
    getSection: 'sections',

    createRelation: 'relations',
    deleteRelation: 'relations',
    editRelation: 'relations',
    getRelations: 'relations',
    getRelation: 'relations'
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