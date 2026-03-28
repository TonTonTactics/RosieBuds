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
        <div key={sensor.sensor_id}>
          <div>ID: {sensor.sensor_id} </div>
          <div>Water Next: {sensor.water_next} </div>
          <div>Temperature: {sensor.temperature_rating} </div>
          <div>Humidity: {sensor.humidity_rating} </div>
        </div>
      ))}
    </div>
  );
}

export function GetGuidebook({ id }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`/sensors/${id}`)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(() => setError(true));
  }, [id]);

  if (error) return <div>Error loading data</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <div>
        name: {data.name}
      </div>
      <div>
        tips: <pre>{data.tips}</pre>
      </div>
      <img className="GuideImage" src={data.image_url}/>
    </div>
  );
}

