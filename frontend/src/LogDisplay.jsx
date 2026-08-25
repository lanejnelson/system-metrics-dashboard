import React from "react"

function formatTimestamp(id) {
    return new Date(id * 1000).toLocaleString();
}

const LogDisplay = ({logs}) => {
    return <div>
        <h2>System Logs</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Hostname</th>
                    <th>Operating System</th>
                    <th>CPU Usage</th>
                    <th>Memory Usage</th>
                    <th>Storage Used Percentage</th>
                </tr>
            </thead>
            <tbody>
                {logs.map((log) => (
                    <tr key={log.id}>
                        <td>{formatTimestamp(log.timestamp)}</td>
                        <td>{log.hostname}</td>
                        <td>{log.operatingSys}</td>
                        <td>{log.cpuUsage}%</td>
                        <td>{log.memoryUsage}%</td>
                        <td>{log.diskUsage}%</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default LogDisplay;