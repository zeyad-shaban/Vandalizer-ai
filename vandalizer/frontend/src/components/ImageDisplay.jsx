// todo annoying how to debug this i have to go through my entire application layer first.. annoying didnt' we intend intially to make it that we can refresh it without losing progress? this "stateless" concept?

import { useState, useRef } from "react";
import { getBBoxes, sendDetectorPrompt } from "../services/api";
import { Loading } from "../components/Loading"
import ImageWithBoxes from "../components/ImageWithBoxes"
import { sleep } from "../utils"

// todo as of now if i put another prompt and put submit the server just returns the old thing back as it can already find a reference fiel for that there... we need a way to check status of teh thing and such...
export const ImageDisplay = ({ jobID, setErr }) => {
    const maxServerAttempts = 40;

    const [loading, setLoading] = useState(false);
    // contains scores, labels, boxes, text_label, there must be a better way to get intellisense on what it have
    const [boxes, setBoxes] = useState([]); // todo i dont' think having the bboxes here is a good idea, this imagedisplay shoudl be made only to display image not the bboxes nor retreiving them, i think or is this a good practice?
    const [scores, setScores] = useState([]);
    const [textLabels, setTextLabels] = useState([]);

    const [prompt, setPrompt] = useState("");
    const [thresh, setThresh] = useState(0.1);

    const handleSubmit = async e => {
        e.preventDefault();
        setLoading(true);

        try {
            // todo this makes the app frz till we get results, perhaps use our check_job_status thing for this job?
            await sendDetectorPrompt(jobID, prompt); // todo backend side handle possible errors with a proper returned status code

            // retreive boundary boxes
            for (let i = 0; i <= maxServerAttempts; ++i) {
                try {
                    const res = await (getBBoxes(jobID));
                    setBoxes(res.data['boxes']);
                    setScores(res.data['scores']);
                    setTextLabels(res.data['text_labels']);
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

    const handlePromptChange = e => {
        setPrompt(e.target.value);
    }

    // Todo handle errors, loading for image itself
    if (loading)
        return <Loading />

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