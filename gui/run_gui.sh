#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ -x "$script_dir/.venv/bin/python3" ]]; then
	exec "$script_dir/.venv/bin/python3" "$script_dir/pdu_gui.py"
fi

if python3 -c 'import can, canopen, tkinter' >/dev/null 2>&1; then
	exec python3 "$script_dir/pdu_gui.py"
fi

echo "GUI dependencies are not installed." >&2
echo "Follow docs/GUI_MANUAL.md, then run this launcher again." >&2
exit 1

