#!/bin/bash
set -e
set -x

DATA_DIR=/mnt/lssd/data
WORK_DIR=/mnt/lssd/data_opacity

FELS_MBTILES_FILE=SMV10_Fels.mbtiles
GEROELL_MBTILES_FILE=SMV10_Geroell.mbtiles
GLETSCHERFORM_MBTILES_FILE=SMV10_Gletscherform.mbtiles

# Fels
cp ${DATA_DIR}/${FELS_MBTILES_FILE} ${WORK_DIR}/${FELS_MBTILES_FILE}
python3 add_opacity_by_zoom.py ${WORK_DIR}/${FELS_MBTILES_FILE} \
1:0.1 \
2:0.1 \
3:0.1 \
4:0.1 \
5:0.1 \
6:0.1 \
7:0.1 \
8:0.1 \
9:0.2 \
10:0.3 \
11:0.39 \
12:0.45 \
13:0.45 \
14:0.45 \
15:0.45 \
16:0.45 \
17:0.45

# Geroell
cp ${DATA_DIR}/${GEROELL_MBTILES_FILE} ${WORK_DIR}/${GEROELL_MBTILES_FILE}
python3 add_opacity_by_zoom.py ${WORK_DIR}/${GEROELL_MBTILES_FILE} \
1:0.1 \
2:0.1 \
3:0.1 \
4:0.1 \
5:0.1 \
6:0.1 \
7:0.1 \
8:0.1 \
9:0.2 \
10:0.3 \
11:0.39 \
12:0.45 \
13:0.45 \
14:0.45 \
15:0.45 \
16:0.45 \
17:0.45

# Gletscherform
cp ${DATA_DIR}/${GLETSCHERFORM_MBTILES_FILE} ${WORK_DIR}/${GLETSCHERFORM_MBTILES_FILE}
python3 add_opacity_by_zoom.py ${WORK_DIR}/${GLETSCHERFORM_MBTILES_FILE} \
1:0.1 \
2:0.1 \
3:0.1 \
4:0.1 \
5:0.1 \
6:0.1 \
7:0.1 \
8:0.1 \
9:0.3 \
10:0.5 \
11:0.59 \
12:0.65 \
13:0.65 \
14:0.65 \
15:0.65 \
16:0.65 \
17:0.65