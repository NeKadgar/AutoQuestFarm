import sqlite3
from Path.WoWPoint import WoWPoint

conn = sqlite3.connect('points.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS point(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    x REAL,
    y REAL
);
""")
conn.commit()


def add_point(location, x, y):
    cur.execute("INSERT OR IGNORE INTO point (location, x, y) VALUES (?, ?, ?);", (location, x, y))
    conn.commit()


def get_all_points():
    cur.execute("SELECT * FROM point;")
    result = cur.fetchall()
    return result


def get_point_by_id(id):
    cur.execute("SELECT * FROM point WHERE id  = ?;", (id,))
    result = cur.fetchone()
    return WoWPoint(result[0], result[2], result[3])


def delete_point(id):
    cur.execute("DELETE FROM point WHERE id  = ?;", (id,))
    conn.commit()


def get_location_points(location):
    cur.execute("SELECT * from point WHERE location = ?", [location])
    result = []
    for p in cur.fetchall():
        result.append(WoWPoint(p[0], p[2], p[3]))
    return result


def get_near_points(location, x, y, dist=40):
    dist = dist * dist
    cur.execute("SELECT * from point WHERE location = ? AND (((x-?)*100*(x-?)*100)+((y-?)*100*(y-?)*100))<?",
                [location, x, x, y, y, dist])
    result = []
    for p in cur.fetchall():
        result.append(WoWPoint(p[0], p[2], p[3]))
    return result
