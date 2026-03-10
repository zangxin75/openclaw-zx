#!/bin/bash
# Gateway 守护脚本包装器

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -eq 0 ]; then
    echo "用法: $(basename $0) [start|stop|status]"
    exit 1
fi

python3 "$SCRIPT_DIR/guardian.py" "$@"
