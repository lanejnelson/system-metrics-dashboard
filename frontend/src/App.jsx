import { useState, useEffect } from 'react'
import LogDisplay from './LogDisplay'
import EventDisplay from './EventDisplay'
import './App.css'

function App() {
  const [logs, setLogs] = useState([])
  const [events, setEvents] = useState([])

  useEffect(() => {
        fetchLog();
        fetchEvents();
    }, []);

  const fetchLog = async () => {
    const response = await fetch("http://127.0.0.1:5000/metrics")
    const data = await response.json()
    setLogs(data.logs)
    console.log(data.logs)
  }

  const fetchEvents = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/events")
    const data = await response.json()
    setEvents(data.events)
    console.log(data.events)
  }


  return (
    <>
      <EventDisplay events={events} />
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <LogDisplay logs={logs} />
    </>
  )
}

export default App
