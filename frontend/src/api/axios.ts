import axios from 'axios'

export const isDev = import.meta.env.DEV

const axiosInstance = axios.create({
    baseURL: isDev ? import.meta.env.VITE_API_URL : '',
    headers: {
        'Content-Type': 'application/json',
        Authorization: import.meta.env.VITE_API_KEY,
    },
})

export default axiosInstance
