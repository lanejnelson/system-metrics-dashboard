import React from "react"

function formatTimestamp(id) {
    const milliseconds = Number(id.split("-")[0]);
    return new Date(milliseconds).toLocaleString();
}

const EventDisplay = ({events}) => {
    return <div>
        <h2>System Events</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Level</th>
                    <th>Host ID</th>
                    <th>Event Type</th>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {events.map((event) => (
                    <tr key={event.id}>
                        <td>{formatTimestamp(event.id)}</td>
                        <td>{event.level}</td>
                        <td>{event.host_id}</td>
                        <td>{event.event_type}</td>
                        <td>{event.metric}</td>
                        <td>{event.value}</td>
                        <td>{event.message}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default EventDisplay;