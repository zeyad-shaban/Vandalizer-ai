// todo annoying how to debug this i have to go through my entire application layer first.. annoying didnt' we intend intially to make it that we can refresh it without losing progress? this "stateless" concept?

import { useState } from "react";
import { getBBoxes, sendDetectorPrompt } from "../services/api";
import { Loading } from "../components/Loading"
import { sleep } from "../utils"

export const ImageDisplay = ({ jobID, setErr }) => {
    const [loading, setLoading] = useState(false);
    // scores, labels, boxes, text_label
    const [bboxes, setBboxes] = useState(null); // todo i dont' think having the bboxes here is a good idea, this imagedisplay shoudl be made only to display image not the bboxes nor retreiving them, i think or is this a good practice?
    const [prompt, setPrompt] = useState("");

    const handleSubmit = async e => {
        e.preventDefault();

        setLoading(true);

        try {
            // todo this makes the app frz till we get results, perhaps use our check_job_status thing for this job?
            await sendDetectorPrompt(jobID, prompt); // todo backend side handle possible errors with a proper returned status code

            // retreive boundary boxes
            // todo handle it not working even after 20 attempts
            for (let i = 0; i < 20; ++i) {
                try {
                    const res = await (getBBoxes(jobID));
                    setBboxes(res.data);
                } catch (e) {
                    if (e.response?.status === 404) await sleep(500)
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

    const handlePromptChange = e => {
        setPrompt(e.target.value);
    }

    const renderBboxes = () => {
        if (bboxes === null) return null;
        console.log(bboxes);

        return (
            // todo draw them
            <h1>ok boys we got some bboxes to display</h1>
        )
    }

    // Todo handle errors, loading for image itself
    // todo  don't hardcode the url like that
    if (loading)
        return <Loading />

    return (
        <>
            {renderBboxes()}
            <img src={`${import.meta.env.VITE_API_BASE_URL}/uploads/${jobID}/${import.meta.env.VITE_INPUT_IMG_PATH}`} />
            <form onSubmit={handleSubmit}>
                <label htmlFor="prompt">Prompt  </label>
                <input type="text" name="prompt" value={prompt} onChange={handlePromptChange} />
                <button type="submit">Submit</button>
            </form>
        </>
    )
}