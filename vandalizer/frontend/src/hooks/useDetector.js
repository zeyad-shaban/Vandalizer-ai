import { useState } from 'react'
import { getBBoxes, sendDetectorPrompt } from '../services/api';
import { sleep } from '../utils'

/**
 * @typedef {Object} DetectorData
 * @property {number[][]} boxes
 * @property {number[]} scores
 * @property {string[]} textLabels
 */

export const useDetector = () => {
    const maxServerAttempts = 50;

    /** @type {[DetectorData, Function]} */
    const [data, setData] = useState({ boxes: [], scores: [], textLabels: [] });
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState();

    const detect = async (jobID, prompt) => {
        try {
            setLoading(true);
            await sendDetectorPrompt(jobID, prompt);

            // retreive boundary boxes
            for (let i = 0; i <= maxServerAttempts; ++i) {
                try {
                    const res = await (getBBoxes(jobID));
                    setData(res.data);
                    break;
                } catch (e) {
                    if (e.response?.status === 404 && i != maxServerAttempts) await sleep(500);
                    else throw e;
                }
            }
        } catch (err) {
            console.log(err);
            setErr("Failed to detect objects, check developer console for more details")
        } finally {
            setLoading(false);
        }
    }

    return { ...data, loading, err, detect }
}