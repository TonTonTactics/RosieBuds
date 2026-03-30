/* Receives sensor data


Antony Wiegand, Mcmaster, 2026*/

import { useEffect, useState } from "react";

export function GetSensors({ sensor_id, plant_type }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!plant_type) return;

    const today = new Date().toISOString().split("T")[0];

    fetch(`http://192.168.4.1:8000/sensors/?date=${today}&sensor_id=${sensor_id}&plant_type=${plant_type}`)
      .then(response => response.json())
      .then(data => setData(data))
      .catch(() => setData([]));
  }, [sensor_id, plant_type]);

  if (!plant_type) return <div>Select a plant first</div>;
  if (data === null) return <div>Loading...</div>;
  if (data.length === 0) return <div>No Data</div>;

  return (
    <div>
      {data.map(sensor => (
        <div key={sensor?.sensor_id ?? "none"}>
          <div key={sensor?.plant_name ?? "none"}>
            <div>Plant: {sensor?.plant_name}</div>
          </div>
          <div>ID: {sensor?.sensor_id}</div>
          <div>Moisture: {sensor?.moisture}</div>
          <div>Temperature: {sensor?.temperature}</div>
          <div>Humidity: {sensor?.humidity}</div>
        </div>
      ))}
    </div>
  );
}

export function GetGuidebook({ id }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`http://192.168.4.1:8000/guidebook/${id}`)
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

export function GetPlants( {id } ) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch(`http://192.168.4.1:8000/guidebook/${id}`)
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

