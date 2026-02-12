import { useState } from "react";
import { getInputImgUrl } from "../services/api"
import { BoxesOverlay } from "./BoxesOverlay"
import { MaskOverlay } from "./MaskOverlay"


// todo dispaly score and textlabels
// todo make it render basd on the threshold
// hmm something i don't like i'm doing is how i hve to pass the boxes, scores, textLabels into this workspace, and to pass it later into BoxesOverlay, but i think pasing dims is fine? but idk...
// i think having a neted component pasing indicates there i something i can do better overall?

export default function Workspace({ jobID, boxes = [], scores = [], textLabels = [], normalized = false }) {
  const [dims, setDims] = useState({ dw: 1, dh: 1, nw: 1, nh: 1 });

  const onLoad = (e) => {
    const img = e.currentTarget;
    setDims({ dw: img.clientWidth, dh: img.clientHeight, nw: img.naturalWidth, nh: img.naturalHeight });
  };

  return (
    <div className="relative inline-block">
      <img src={getInputImgUrl(jobID)} onLoad={onLoad} className="block max-w-full h-auto" alt="" />
      <MaskOverlay jobID={jobID} />
      <BoxesOverlay jobID={jobID} {...{ boxes, scores, textLabels, normalized, dims }} />
    </div>
  );
}
