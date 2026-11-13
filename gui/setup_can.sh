#!/usr/bin/env bash
set -euo pipefail

interface="${1:-can0}"
bitrate="${2:-500000}"

if [[ ! "$interface" =~ ^[a-zA-Z0-9_.:-]+$ ]]; then
	echo "Invalid CAN interface name: $interface" >&2
	exit 2
fi

case "$bitrate" in
	125000|250000|500000|1000000) ;;
	*)
		echo "Unsupported CAN bitrate: $bitrate" >&2
		exit 2
		;;
esac

if ! ip link show dev "$interface" >/dev/null 2>&1; then
	echo "CAN interface $interface was not found. Is the PEAK adapter connected?" >&2
	exit 3
fi

details="$(ip -details link show dev "$interface")"
if grep -q 'state UP' <<<"$details" && grep -Eq "bitrate[[:space:]]+$bitrate([[:space:]]|$)" <<<"$details"; then
	echo "$interface is already active at $((bitrate / 1000)) kbit/s"
	exit 0
fi

if (( EUID != 0 )); then
	exit 77
fi

ip link set dev "$interface" down
ip link set dev "$interface" type can bitrate "$bitrate" restart-ms 100
ip link set dev "$interface" up
echo "$interface started at $((bitrate / 1000)) kbit/s"
