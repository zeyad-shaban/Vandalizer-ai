import { getSegmentImgUrl } from "../services/api"

export const MaskOverlay = ({ jobID }) => {
    return (
        <img src={getSegmentImgUrl(jobID)} className="block max-w-full h-auto" />
    )
}