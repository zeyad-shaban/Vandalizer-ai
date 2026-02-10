// todo annoying how to debug this i have to go through my entire application layer first.. annoying

import { useState } from "react";
import { sendDetectorPrompt } from "../services/api";
import { Loading } from "../components/Loading"

export const ImageDisplay = ({ jobID, setErr }) => {
    const [loading, setLoading] = useState(false);
    const [prompt, setPrompt] = useState("");

    const handleSubmit = async e => {
        e.preventDefault();

        setLoading(true);

        try {
            // todo this makes the app frz till we get results, perhaps use our check_job_status thing for this job?
            const res = await sendDetectorPrompt(jobID, prompt);
            console.log(res.data);
        } catch (err) {
            console.log(err);
            setErr("Failed to detect objects, check developer console for more details")
        } finally {
            setLoading(false);
        }

    }

    const handlePromptChange = e => {
        setPrompt(e.target.value);
    }
    // Todo handle errors, loading for image itself
    // todo  don't hard the url like that
    if (loading)
        return <Loading />
    return (
        <>
            <img src={`${import.meta.env.VITE_API_BASE_URL}/uploads/${jobID}/${import.meta.env.VITE_INPUT_IMG_PATH}`} />
            <form onSubmit={handleSubmit}>
                <label htmlFor="prompt">Prompt</label>
                <input type="text" name="prompt" value={prompt} onChange={handlePromptChange} />
                <button type="submit">Submit</button>
            </form>
        </>
    )
}