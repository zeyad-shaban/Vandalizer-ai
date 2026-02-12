import { useState } from "react";
import { Loading } from "../components/Loading"
import ImageWithBoxes from "../components/ImageWithBoxes"
import { useDetector } from "../hooks/useDetector"
import { ErrorMessage } from "./ErrorMessage";
import { useParams } from "react-router-dom";
import { useSegmentor } from "../hooks/useSegmentor";

// todo add threshold slider
export const ImageDisplay = () => {
    const { jobID } = useParams();
    const { boxes, scores, text_labels: textLabels, detect, loading: detectorLoading, err: detectorErr } = useDetector(jobID);
    const { mask, segment, loading: segmentorLoading, err: segmentorErr } = useSegmentor(jobID, boxes);

    const [prompt, setPrompt] = useState("");
    const [thresh, setThresh] = useState(0.1);

    const handleSubmit = async e => {
        e.preventDefault();
        detect(prompt);
    }

    const handlePromptChange = e => {
        setPrompt(e.target.value);
    }

    const handleStartSegmenting = async () => {
        segment();
    }

    if (detectorLoading || segmentorLoading)
        return <Loading />
    if (detectorErr || segmentorErr)
        return <ErrorMessage err={detectorErr || segmentorErr} />

    return (
        <>
            <ImageWithBoxes {...{ jobID, boxes, scores, textLabels }} />

            <form onSubmit={handleSubmit}>
                <label htmlFor="prompt">Prompt  </label>
                <input type="text" name="prompt" value={prompt} onChange={handlePromptChange} />
                <button type="submit">Submit</button>
            </form>
            
            <button onClick={handleStartSegmenting}>Start Segmenting</button>
        </>
    )
}