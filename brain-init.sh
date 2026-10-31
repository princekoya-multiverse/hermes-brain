#!/bin/sh
# brain-init.sh — first-boot seed + handoff to the official s6 entrypoint.
# If HERMES_HOME (/opt/data) is empty (fresh Akash persistent volume),
# unpack the baked Warrior World context so the brain is born knowing
# the mission. Idempotent: existing state (managers' memories) survives.
set -e
HERMES_HOME="${HERMES_HOME:-/opt/data}"
mkdir -p "$HERMES_HOME"

if [ ! -f "$HERMES_HOME/memories/MISSION.md" ] && [ -d /opt/data-seed ]; then
  echo "[brain-init] seeding Warrior World context into $HERMES_HOME"
  cp -rn /opt/data-seed/. "$HERMES_HOME/" 2>/dev/null || true
fi

# Hand off to the official Hermes entrypoint (s6 supervision tree).
exec /opt/hermes/docker/entrypoint-dispatch.sh "$@"