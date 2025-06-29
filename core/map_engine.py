import sqlite3
from flask import Blueprint, Response, abort
import os

mbtiles = Blueprint('mbtiles', __name__)

MBTILES_PATH = r"C:\mbtiles_test\india.mbtiles"

from werkzeug.exceptions import HTTPException

@mbtiles.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def serve_tile(z, x, y):
    try:
        flipped_y = (1 << z) - 1 - y  # TMS flip
        with sqlite3.connect(MBTILES_PATH) as conn:
            cursor = conn.cursor()
            # 1. Look up tile_id in map table
            cursor.execute(
                "SELECT tile_id FROM map WHERE zoom_level=? AND tile_column=? AND tile_row=?;",
                (z, x, flipped_y)
            )
            row = cursor.fetchone()
            if not row:
                abort(404)
            tile_id = row[0]
            # 2. Look up tile_data in images table
            cursor.execute("SELECT tile_data FROM images WHERE tile_id=?;", (tile_id,))
            img_row = cursor.fetchone()
            if img_row:
                return Response(img_row[0], mimetype='image/png')
            else:
                abort(404)
    except HTTPException:
        raise  # Let Flask handle abort(404) properly
    except Exception as e:
        print(f"❌ Tile error: {e}")
        abort(500)

