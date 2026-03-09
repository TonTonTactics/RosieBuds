/* Receives sensor data


Antony Wiegand, Mcmaster, 2026*/

import { useEffect, useState } from "react";

export function GetSensors({ sensor_id }) {
  const [data, setData] = useState([]);
  useEffect(() => {
    const today = new Date().toISOString().split("T")[0];
    fetch(`/sensors/?date=${today}&sensor_id=${sensor_id}`)
      .then(response => response.json())
      .then(data => setData(data));
  }, [sensor_id]);
  
  if (data.length === 0) {
    return <div>Error</div>;
  }

  return (
    <div>
      {data.map(sensor => (
        <div key={sensor.id}>
          TS: {sensor.timestamp} | 
          ID: {sensor.sensor_id} |
          M: {sensor.moisture} |
          H: {sensor.humidity} |
          T: {sensor.temperature}
        </div>
      ))}
    </div>
  );
}