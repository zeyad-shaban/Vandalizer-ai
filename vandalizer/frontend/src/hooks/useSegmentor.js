import { useGetServerResult } from "./useGetServerResult";
import { fetchSegmentMasks, startSegmenting } from "../services/api";
import { useState } from "react";

export const useSegmentor = (jobID, boxes) => {
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(null);

    const { data, getResult } = useGetServerResult(jobID, fetchSegmentMasks, null)

    const segment = async () => {
        try {
            setLoading(true);
            await startSegmenting(jobID, boxes);
            await getResult();
            console.log(data);
        } catch (e) {
            console.error("Error Starting Segmentation", e)
            setErr(e);
        } finally {
            setLoading(false);
        }
    }

    return { mask: data, segment, loading, err };
}