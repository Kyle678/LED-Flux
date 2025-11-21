import urls, { getResponse } from './urls';

const svrOp = {

    playConfig: async (config_id) => {
        const url = urls.playConfig
        const data = { 'cid': config_id };
        return await getResponse(url, 'POST', data);
    }

}

export default svrOp;