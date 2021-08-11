const axios = require('axios');
export function authenticate(userData) {
    return axios.post(`${'http://localhost:5000'}/login/`, userData)
}

export function register(userData) {
    return axios.post(`${'http://localhost:5000'}/register/`, userData)
}