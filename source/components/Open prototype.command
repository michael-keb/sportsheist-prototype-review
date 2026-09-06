#!/bin/bash
# Double-click this to open the SportsHeist prototype.
#
# It serves the folder on localhost first, because browsers refuse microphone
# access to pages opened straight from disk (file://). Dictation and voice notes
# need a real origin; typing works either way. Close this window to stop.

cd "$(dirname "$0")" || exit 1

PORT=8912
while lsof -i :$PORT >/dev/null 2>&1; do PORT=$((PORT+1)); done

echo "SportsHeist prototype"
echo "  serving  $(pwd)"
echo "  at       http://localhost:$PORT/prototype.html"
echo
echo "Leave this window open while you review. Close it when you are done."
echo

python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT INT TERM

sleep 1
open "http://localhost:$PORT/prototype.html"

wait $SERVER
