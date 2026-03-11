const API = "http://127.0.0.1:8000"

let map = L.map('map').setView([41.2995,69.2401],12)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
}).addTo(map)

async function loadApartments(){

let res = await fetch(API + "/apartments")

let data = await res.json()

data.forEach(a=>{

let marker = L.marker([a.lat,a.lon]).addTo(map)

marker.bindPopup(`
<b>${a.price}$</b><br>
Area ${a.area} m²<br>
Rooms ${a.rooms}<br>
District ${a.district}
`)
})
}

loadApartments()
