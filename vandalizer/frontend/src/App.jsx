import axios from "axios";
import { useEffect, useState } from "react"

function App() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);

    try {
      console.log("about to send")
      const res = await axios.get("https://jsonplaceholder.typicode.com/users")
      setUsers(res.data)
    } catch (err) {
      console.error(err)
      setError("Faild to load users")
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchUsers();
  }, [])

  if (loading)
    return <h1>wait bruh</h1>
  if (error)
    return <h1>Error bruh {error}</h1>
  return (
    <>
      <div>
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.username} - {user.name} - {user.email}</li>
          ))}
        </ul>
      </div>
    </>
  )
}

export default App