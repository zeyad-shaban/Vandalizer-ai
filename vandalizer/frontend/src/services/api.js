import axios from 'axios';

const apiClient = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

export const uploadImage = (file) => {
    const data = new FormData()
    data.append('img', file)
    return apiClient.post('/upload', data)
}

export const sendDetectorPrompt = (jobID, prompt) => {
    const endpoint = `/process/detect_objects/${jobID}`;
    const data = new FormData();
    data.append('prompt', prompt);

    return apiClient.post(endpoint, data);
}

export const getBBoxes = (jobID) => {
    const endpoint = `/uploads/${jobID}/detector_boxes.json`;
    return apiClient.get(endpoint);
}

export const getInputImgUrl = (jobID) => `${import.meta.env.VITE_API_BASE_URL}/uploads/${jobID}/${import.meta.env.VITE_INPUT_IMG_PATH}`
