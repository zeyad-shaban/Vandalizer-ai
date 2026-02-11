import { useEffect, useRef, useState } from "react";
import { checkJobStatus, fetchBBoxes } from "../services/api";
import {sleep} from "../utils"

export const useGetBBoxes = (jobID) => {
    const [data, setData] = useState({ boxes: [], scores: [], textLabels: [] })
    const isComponentAlive = useRef(true);

    useEffect(() => {
        () => {
            isComponentAlive.current = false;
        }
    })

    const getBBoxes = async () => {
        try {
            while (isComponentAlive.current) {
                const status = (await checkJobStatus(jobID)).data.status; // PENDING, RUNNING, SUCCESS, ERROR
                if (status == "SUCCESS" && isComponentAlive.current) {
                    const res = await fetchBBoxes(jobID);
                    setData(res.data);
                    return true;
                }
                else if (status == "FAILURE")
                    throw new Error("Server error, job failed to execute detections");
                
                await sleep(1000);
            }
        } catch (err) {
            console.error("Polling error: ", err)
            throw err;
        }
    }

    return { data, getBBoxes };
}