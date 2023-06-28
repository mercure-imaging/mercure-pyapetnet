#!/usr/bin/env bash
set -Eeo pipefail
echo "-- Starting pyapetnet..."
conda run -n mercure-pyapetnet  python pyapetnet_process.py $MERCURE_IN_DIR $MERCURE_OUT_DIR  
echo "-- Done."