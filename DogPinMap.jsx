import DogPinMap from './DogPinMap';
// 📍 INTERACTIVE MAP WITH COLORED PINS USING LEAFLET import React, { useState } from "react"; import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet"; import L from "leaflet"; import "leaflet/dist/leaflet.css";

// Custom icons for different pin types const redIcon = new L.Icon({ iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png", iconSize: [32, 32], iconAnchor: [16, 32] });

const blueIcon = new L.Icon({ iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png", iconSize: [32, 32], iconAnchor: [16, 32] });

const yellowIcon = new L.Icon({ iconUrl: "https://maps.google.com/mapfiles/ms/icons/yellow-dot.png", iconSize: [32, 32], iconAnchor: [16, 32] });

function MapEventHandler({ onAddPin }) { useMapEvents({ click(e) { const type = prompt("Enter pin type: lost, sighting, flyer").toLowerCase(); if (["lost", "sighting", "flyer"].includes(type)) { onAddPin({ type, position: e.latlng, }); } else { alert("Invalid type. Use: lost, sighting, flyer"); } } }); return null; }

export default function DogPinMap() { const [pins, setPins] = useState([]);

const addPin = (pin) => { setPins((prev) => [...prev, pin]); };

const getIcon = (type) => { switch (type) { case "lost": return redIcon; case "sighting": return blueIcon; case "flyer": return yellowIcon; default: return redIcon; } };

return ( <div className="w-full h-[500px] rounded-xl overflow-hidden border-2 border-gray-300"> <MapContainer center={[33.5, -86.8]} zoom={7} scrollWheelZoom={true} className="w-full h-full"> <TileLayer
attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
/> <MapEventHandler onAddPin={addPin} /> {pins.map((pin, idx) => ( <Marker
key={idx}
position={pin.position}
icon={getIcon(pin.type)}
> <Popup> {pin.type.charAt(0).toUpperCase() + pin.type.slice(1)} location<br /> Lat: {pin.position.lat.toFixed(4)}, Lng: {pin.position.lng.toFixed(4)} </Popup> </Marker> ))} </MapContainer> </div> ); }
<DogPinMap />
