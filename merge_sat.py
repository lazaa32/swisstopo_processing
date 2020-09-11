import sqlite3
import os
import sys
from PIL import Image
import io


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4,))


if len(sys.argv) < 4:
    print("Usage: {} <output> <lowres> [<mediumres>] [<zoom:alpha> ...]".format(
        sys.argv[0]))
    print("  Blend lowres * alpha into output/mediumres (using mediumres if defined)")
    sys.exit(1)

output = mediumres = sys.argv[1]
lowres = sys.argv[2]

alpha_arg = 3
if ':' not in sys.argv[3] and os.path.isfile(sys.argv[3]):
    mediumres = sys.argv[3]
    alpha_arg = 4

out_con = sqlite3.connect(output)
out_cur = out_con.cursor()
med_con = sqlite3.connect(mediumres)
med_cur = med_con.cursor()
low_con = sqlite3.connect(lowres)
low_cur = low_con.cursor()

# test = True
test = False
debug = False

# Default white color
background_color = hex_to_rgb('#FFFFFF')

row = med_cur.execute(
    "SELECT value FROM metadata WHERE name = 'color'").fetchone()
if row:
    background_color = hex_to_rgb(row[0])


total_tiles = 0
total_merged = 0
for arg in range(alpha_arg, len(sys.argv)):
    zoom, salpha = sys.argv[arg].split(':')
    alpha = float(int(salpha) / 100)
    low_cur.execute("""
        SELECT i.tile_id, i.tile_data,
            m.zoom_level, m.tile_row, m.tile_column
        FROM images i
        JOIN map m ON m.tile_id = i.tile_id
        WHERE m.zoom_level = ?
    """, (zoom,))
    tiles = 0
    merged = 0
    background = False
    print('Merging Zoom {} with {} alpha'.format(
        zoom, alpha))
    sys.stdout.flush()

    for low_row in low_cur:
        ti = low_row[0]
        tz = low_row[2]
        tr = low_row[3]
        tc = low_row[4]
        med_cur.execute("""
            SELECT i.tile_id, i.tile_data
            FROM images i
            JOIN map m ON m.tile_id = i.tile_id
            WHERE m.zoom_level = ? AND m.tile_row = ? AND m.tile_column = ?
            """, (tz, tr, tc,))
        med_row = med_cur.fetchone()
        tiles += 1
        total_tiles += 1
        if debug:
            print('Process {}/{}/{} as Tid {}'.format(tz, tr, tc, ti))
            sys.stdout.flush()

        low_im = Image.open(io.BytesIO(low_row[1]))
        low_im.putalpha(255)
        stream = io.BytesIO()
        bg = Image.new("RGB", low_im.size, background_color)

        # Missing tile, append new tile with low_row only and background color
        if not med_row:
            med_im = Image.new("RGB", low_im.size, background_color)
            med_im.putalpha(255)
            merged_im = Image.blend(med_im, low_im, alpha)

            bg.paste(merged_im, mask=merged_im.split()[3])
            bg.save(stream, format="JPEG", quality=85)
            lnn = len(stream.getvalue())

            if not test:
                out_cur.execute("""
                    INSERT INTO map (zoom_level, tile_row, tile_column, tile_id)
                    VALUES (?, ?, ?, ?);
                    """, (tz, tr, tc, ti,))
                out_cur.execute("""
                    INSERT INTO images (tile_id, tile_data)
                    VALUES (?, ?);
                    """, (ti, stream.getvalue(),))

        else:     # and (med_row[0] != 'background' or not background):
            # background = ( med_row[0] == 'background' )
            if med_row[0] == 'background' and ti == 'background':
                if background:
                    continue
                background = True

            merged += 1
            total_merged += 1

            med_im = Image.open(io.BytesIO(med_row[1]))
            med_im.putalpha(255)
            merged_im = Image.blend(med_im, low_im, alpha)

            bg.paste(merged_im, mask=merged_im.split()[3])
            bg.save(stream, format="JPEG", quality=85)
            lnn = len(stream.getvalue())
            if not test:
                if med_row[0] == 'background' and ti != 'background':
                    out_cur.execute("""
                        INSERT INTO images (tile_id, tile_data)
                        VALUES (?, ?)
                        """, (ti, stream.getvalue(),))
                    out_cur.execute("""
                        UPDATE map
                        SET tile_id = ?
                        WHERE zoom_level = ? AND tile_row = ?
                            AND tile_column = ?""", (ti, tz, tr, tc,))
                else:
                    out_cur.execute("""
                        UPDATE images
                        SET tile_data = ?
                        WHERE tile_id = ?
                        """, (stream.getvalue(), med_row[0],))
            if test:
                fn = "{}_{}_{}_{}".format(
                    tz, tr, tc,
                    ti.replace('/', '-'))
                low_im.save("out/low/{}.png".format(fn), format="PNG")
                med_im.save("out/med/{}.png".format(fn), format="PNG")
                merged_im.save("out/merged/{}.png".format(fn), format="PNG")
                bg.save("out/bg/{}.jpg".format(fn), format="JPEG", quality=85)
            if debug:
                print({
                    "medium": {
                        "size": med_im.size,
                        "mode": med_im.mode,
                        "id": med_row[0],
                        "tile id": "/".join(map(str, [tz, tr, tc])),
                        "len": len(med_row[1])
                    },
                    "low": {
                        "size": low_im.size,
                        "mode": low_im.mode,
                        "id": ti,
                        "tile id": "/".join(map(str, [tz, tr, tc])),
                        "len": len(low_row[1])
                    },
                    "merged": {
                        "size": merged_im.size,
                        "mode": merged_im.mode,
                        "id": med_row[0],
                        "tile id": "/".join(map(str, [tz, tr, tc])),
                        "len": lnn
                    }
                })
                sys.stdout.flush()
            # if merged > 10:
            #    break
    print("Stats: [{}/{}]".format(merged, tiles))
    sys.stdout.flush()
    if not test:
        out_con.commit()

if not test:
    out_con.commit()
med_con.close()
low_con.close()
out_con.close()