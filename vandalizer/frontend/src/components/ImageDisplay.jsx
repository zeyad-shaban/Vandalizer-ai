// todo annoying how to debug this i have to go through my entire application layer first.. annoying didnt' we intend intially to make it that we can refresh it without losing progress? this "stateless" concept?

import { useState, useRef } from "react";
import { fetchBBoxes, sendDetectorPrompt } from "../services/api";
import { Loading } from "../components/Loading"
import ImageWithBoxes from "../components/ImageWithBoxes"
import { useDetector } from "../hooks/useDetector"
import { ErrorMessage } from "./ErrorMessage";
import { useParams } from "react-router-dom";

// todo as of now if i put another prompt and put submit the server just returns the old thing back as it can already find a reference fiel for that there... we need a way to check status of teh thing and such...
export const ImageDisplay = () => {
    const { jobID } = useParams();
    const { boxes, scores, text_labels: textLabels, loading, err, detect } = useDetector(jobID);


    const [prompt, setPrompt] = useState("");
    const [thresh, setThresh] = useState(0.1);

    const handleSubmit = async e => {
        e.preventDefault();
        detect(prompt);
    }

    const handlePromptChange = e => {
        setPrompt(e.target.value);
    }

    if (loading)
        return <Loading />
    if (err)
        return <ErrorMessage err={err} />

    return (
        <>
            <ImageWithBoxes {...{ jobID, boxes, scores, textLabels }} />

            <form onSubmit={handleSubmit}>
                <label htmlFor="prompt">Prompt  </label>
                <input type="text" name="prompt" value={prompt} onChange={handlePromptChange} />
                <button type="submit">Submit</button>
            </form>
        </>
    )
}