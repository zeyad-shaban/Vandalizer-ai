import { useEffect, useState } from "react"

import { Header } from "./components/Header"
import { ImageForm } from "./components/ImageForm"
import { ErrorMessage } from "./components/ErrorMessage"


const AppStates = Object.freeze({
  IDLE: "IDLE",
  WAITING_DETECT_PROMPT: "WAITING_DETECT_PROMPT",
});

function App() {
  const [appState, setAppState] = useState(AppStates.IDLE);

  let [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  const [jobID, setJobID] = useState(null);

  useEffect(() => {
    console.log(jobID)
  }, [jobID]);

  if (loading)
    return <h1>Loading... we need to turn this into a component?</h1>


  const renderContent = () => {
    if (appState == AppStates.IDLE) {
      return <ImageForm {...{ loading, setLoading, setErr, setJobID }}
        onSuccess={res => { setJobID(res.data); setAppState(AppStates.WAITING_DETECT_PROMPT); }
        }
      />
    }
  }

  return (
    <>
      {/* Header */}
      <Header />
      <ErrorMessage err={err} />
      {renderContent()}
    </>
  )
}

export default App