#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
can_interface="${PDU_CAN_IFACE:-can0}"
can_bitrate="${PDU_CAN_BITRATE:-500000}"

set +e
"$script_dir/setup_can.sh" "$can_interface" "$can_bitrate"
can_status=$?
set -e
if (( can_status == 77 )); then
	if ! sudo -n "$script_dir/setup_can.sh" "$can_interface" "$can_bitrate" 2>/dev/null; then
		if command -v pkexec >/dev/null 2>&1; then
			pkexec "$script_dir/setup_can.sh" "$can_interface" "$can_bitrate"
		else
			echo "Administrator permission is required to start $can_interface." >&2
			exit 1
		fi
	fi
elif (( can_status != 0 )); then
	echo "Unable to prepare $can_interface for the PDU workbench." >&2
	exit "$can_status"
fi

if [[ -x "$script_dir/.venv/bin/python3" ]]; then
	exec "$script_dir/.venv/bin/python3" "$script_dir/pdu_gui.py"
fi

if python3 -c 'import can, canopen, tkinter' >/dev/null 2>&1; then
	exec python3 "$script_dir/pdu_gui.py"
fi

echo "GUI dependencies are not installed." >&2
echo "Follow docs/GUI_MANUAL.md, then run this launcher again." >&2
exit 1

