from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "database.db"

districts = [
    "Yunusabad",
    "Mirzo Ulugbek",
    "Chilanzar",
    "Shaykhantakhur",
    "Yakkasaray",
    "Almazar",
    "Uchtepa",
    "Sergeli",
    "Bektemir",
    "Yashnabad",
]

def create_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS apartments(
        id INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        price INTEGER,
        area INTEGER,
        rooms INTEGER,
        district TEXT,
        price_per_m2 INTEGER,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


def generate_apartments():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    for i in range(120):

        lat = 41.29 + random.uniform(-0.08,0.08)
        lon = 69.24 + random.uniform(-0.08,0.08)

        area = random.randint(30,120)
        rooms = random.randint(1,4)

        price_per_m2 = random.randint(600,1500)

        price = area * price_per_m2

        district = random.choice(districts)

        type_ = random.choice(["sale","rent"])

        if type_ == "rent":
            price = random.randint(300,1500)

        c.execute("""
        INSERT INTO apartments
        (latitude,longitude,price,area,rooms,district,price_per_m2,type)
        VALUES(?,?,?,?,?,?,?,?)
        """,(lat,lon,price,area,rooms,district,price_per_m2,type_))

    conn.commit()
    conn.close()


@app.get("/apartments")
def get_apartments():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM apartments")

    rows = c.fetchall()

    conn.close()

    result = []

    for r in rows:
        result.append({
            "id": r[0],
            "lat": r[1],
            "lon": r[2],
            "price": r[3],
            "area": r[4],
            "rooms": r[5],
            "district": r[6],
            "price_per_m2": r[7],
            "type": r[8]
        })

    return result


create_db()
generate_apartments()
