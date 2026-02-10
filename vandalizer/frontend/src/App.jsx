import { useState } from "react"

import { Loading } from "./components/Loading"
import { Header } from "./components/Header"
import { ImageForm } from "./components/ImageForm"
import { ErrorMessage } from "./components/ErrorMessage"
import { ImageDisplay } from "./components/ImageDisplay";


const AppStates = Object.freeze({
  IDLE: "IDLE",
  WAITING_DETECT_PROMPT: "WAITING_DETECT_PROMPT",
});

function App() {
  const [appState, setAppState] = useState(AppStates.IDLE);

  let [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  const [jobID, setJobID] = useState(null);

  if (loading)
    return <Loading />


  const renderContent = () => {
    if (appState == AppStates.IDLE) {
      return <ImageForm {...{ loading, setLoading, setErr, setJobID }}
        onSuccess={res => { setJobID(res.data); setAppState(AppStates.WAITING_DETECT_PROMPT); }
        } />
    } else if (appState == AppStates.WAITING_DETECT_PROMPT) {
      return <ImageDisplay {...{ jobID, setErr }} />
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