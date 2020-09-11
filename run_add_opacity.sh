#!/bin/bash
set -e
set -x

DATA_DIR=/mnt/lssd/data
BACKUP_DIR=/mnt/lssd/data_backup
SERVER_DIR=/mnt/lssd/data_opacity

#python3 add_opacity_by_zoom.py ${DATA_DIR}/SMV10_Fels.mbtiles \
#1:0.1 \
#2:0.1 \
#3:0.1 \
#4:0.1 \
#5:0.1 \
#6:0.1 \
#7:0.1 \
#8:0.1 \
#9:0.2 \
#10:0.3 \
#11:0.39 \
#12:0.45 \
#13:0.45 \
#14:0.45 \
#15:0.45 \
#16:0.45 \
#17:0.45

#python3 add_opacity_by_zoom.py ${DATA_DIR}/SMV10_Geroell.mbtiles \
#1:0.1 \
#2:0.1 \
#3:0.1 \
#4:0.1 \
#5:0.1 \
#6:0.1 \
#7:0.1 \
#8:0.1 \
#9:0.2 \
#10:0.3 \
#11:0.39 \
#12:0.45 \
#13:0.45 \
#14:0.45 \
#15:0.45 \
#16:0.45 \
#17:0.45

cp ${BACKUP_DIR}/SMV10_Geroell ${DATA_DIR}/SMV10_Geroell
python3 add_opacity_by_zoom.py ${DATA_DIR}/SMV10_Gletscherform.mbtiles \
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

cp ${DATA_DIR}/SMV10_Geroell ${SERVER_DIR}/SMV10_Geroell