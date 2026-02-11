import { useState } from 'react'
import { sendDetectorPrompt } from '../services/api';
import { useGetBBoxes } from './useGetBBoxes';

/**
 * @typedef {Object} DetectorData
 * @property {number[][]} boxes
 * @property {number[]} scores
 * @property {string[]} textLabels
 */

export const useDetector = (jobID) => {
    /** @type {[DetectorData, Function]} */
    const { data, getBBoxes } = useGetBBoxes(jobID);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState();

    const detect = async (prompt) => {
        try {
            setLoading(true);
            await sendDetectorPrompt(jobID, prompt);
            await getBBoxes();
        } catch (err) {
            console.log(err);
            setErr("Failed to detect objects, check developer console for more details")
        } finally {
            setLoading(false);
        }
    }

    return { ...data, loading, err, detect }
}