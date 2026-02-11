import { useState } from 'react'
import { checkJobStatus, getBBoxes, sendDetectorPrompt } from '../services/api';
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

            // wait till we are done...
            while (true) {
                const status = (await checkJobStatus(jobID)).data.status; // PENDING, RUNNING, SUCCESS, ERROR
                if (status == "SUCCESS") {
                    const res = await getBBoxes(jobID);
                    setData(res.data);
                    break;
                }
                else if (status == "FAILURE")
                    throw new Error("Server error, job failed to execute detections");
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