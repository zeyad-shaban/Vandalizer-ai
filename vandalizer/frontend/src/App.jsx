import axios from "axios";
import { useEffect, useState } from "react"

function App() {
  const [file, setFile] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <>
      {/* Header */}
      <div>
        <h1>VANDALIZER!</h1>
      </div>

      {/* Upload Image */}
      <div>
          <input type='file' accept="image/*" onChange={e => setFile(e.target.files[0])} />
      </div>
    </>
  )
}

export default App