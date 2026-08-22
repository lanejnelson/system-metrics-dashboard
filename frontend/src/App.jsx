import { useState, useEffect } from 'react'
import LogDisplay from './LogDisplay'
import './App.css'

function App() {
  const [logs, setLogs] = useState([])
  useEffect(() => {
    fetchLog()
  }, [])
  const fetchLog = async () => {
    const response = await fetch("http://127.0.0.1:5000/metrics")
    const data = await response.json()
    setLogs(data.logs)
    console.log(data.logs)
  }



  return (
    <>
      <LogDisplay logs={logs}/>
    </>
  )
}

export default App
