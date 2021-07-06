import axios from 'axios';

import CONFIG from '@/config';

export function call(method, params = {}) {
    return axios.get(
        (CONFIG.PRODUCTION ? CONFIG.PRODUCTION_SERVER : CONFIG.DEVELOPMENT_SERVER) + '/' + method,
        {
            params: params
        }
    );
}