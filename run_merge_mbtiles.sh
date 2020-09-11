#!/bin/bash
set -e
set -x

DATA_DIR=/mnt/lssd/data
alias merge_mbtiles="docker run -ti --rm -v $(pwd):/data -e MAPTILER_LICENSE=AAAA-BBBB-CCCC-DDDD-EEEE-FFFF maptiler/engine merge_mbtiles"

cd DATA_DIR
merge_mbtiles -f png32 Hintergrund.mbtiles SMV10_Gletscherform.mbtiles SMV10_Fels.mbtiles SMV10_Geroell.mbtiles -reencode