import axios from 'axios';

import CONFIG from '@/config';

export function call(method, params = {}) {
    return axios.get(
        (CONFIG.SERVER_URI) + '/' + method,
        {
            params: params
        }
    );
}