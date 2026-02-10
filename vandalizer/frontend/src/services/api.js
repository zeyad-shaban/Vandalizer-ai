import axios from 'axios';

const apiClient = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

export const uploadImage = (file) => {
    const data = new FormData()
    data.append('img', file)
    return apiClient.post('/upload', data)
}

export const sendDetectorPrompt = (jobID, prompt) => {
    const endpoint = `/process/detect_objects/${jobID}`
    const data = new FormData()
    data.append('prompt', prompt);

    return apiClient.post(endpoint, data);
}