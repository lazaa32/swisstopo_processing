import sqlite3
import sys
from PIL import Image
import io


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4,))


if len(sys.argv) < 4:
    print("Usage: {} <input> <zoom:alpha> ...".format(
        sys.argv[0]))
    print("  Blend input * alpha (0-1)")
    sys.exit(1)

input_mbtiles = sys.argv[1]

alpha_arg = 2

in_con = sqlite3.connect(input_mbtiles)
read_cur = in_con.cursor()
write_cur = in_con.cursor()

debug = False

background_color = (255, 255, 255, 0)

total_tiles = 0
total_processed = 0
for arg in range(alpha_arg, len(sys.argv)):
    zoom_processed = 0
    zoom, zoom_alpha = sys.argv[arg].split(':')
    alpha = float(zoom_alpha)

    # Get number of tiles on given zoom
    read_cur.execute("""
            SELECT count(1)
            FROM images i
            JOIN map m ON m.tile_id = i.tile_id
            WHERE i.tile_id IS NOT 'background' AND 
            m.zoom_level = ?
        """, (zoom,))
    zoom_tiles = int(read_cur.fetchone()[0])

    # Get tiles
    read_cur.execute("""
        SELECT i.tile_id, i.tile_data,
            m.zoom_level, m.tile_row, m.tile_column
        FROM images i
        JOIN map m ON m.tile_id = i.tile_id
        WHERE i.tile_id IS NOT 'background' AND
        m.zoom_level = ?
    """, (zoom,))

    print('Updating Zoom {} with alpha value: {}'.format(
        zoom, zoom_alpha))
    sys.stdout.flush()

    for in_row in read_cur:
        ti = in_row[0]
        tz = in_row[2]
        tr = in_row[3]
        tc = in_row[4]
        zoom_processed += 1

        in_im = Image.open(io.BytesIO(in_row[1]))

        bands = list(in_im.split())
        bands[3] = bands[3].point(lambda x: x * alpha)
        blended_im = Image.merge(in_im.mode, bands)
        stream = io.BytesIO()
        blended_im.save(stream, format="PNG")

        write_cur.execute("""
            UPDATE images
            SET tile_data = ?
            WHERE tile_id = ?
            """, (stream.getvalue(), ti,))
        total_processed += zoom_processed
        total_tiles += zoom_tiles
        print("Stats zoom {}: [{}/{}]".format(zoom, zoom_processed, zoom_tiles), end='\r')
        sys.stdout.flush()
    print()
    in_con.commit()

# Save background tile as png
read_cur.execute("""
    SELECT i.tile_id, i.tile_data
    FROM images i
    WHERE i.tile_id='background'
""")

for bg_row in read_cur:
    bg_id = bg_row[0]
    bg_im = Image.open(io.BytesIO(bg_row[1]))
    stream = io.BytesIO()
    bg_im.save(stream, format="PNG")

write_cur.execute("""
    UPDATE images
    SET tile_data = ?
    WHERE tile_id = ?
    """, (stream.getvalue(), bg_id,))


# Update metadata table
write_cur.execute("""
    UPDATE metadata
    SET value = 'png'
    WHERE name = 'format'
    """)
in_con.commit()
in_con.close()
