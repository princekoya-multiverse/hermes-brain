#!/bin/sh
# brain-boot.sh — first-boot seed, then start the Hermes gateway.
# Runs as the container's main program under the official s6 tree.
# The official image reconciles per-profile gateways from
# $HERMES_HOME/profiles/ at boot; `hermes gateway run` hosts them
# (each profile's OpenAI-compatible api_server on :8642).
set -e
HERMES_HOME="${HERMES_HOME:-/opt/data}"
mkdir -p "$HERMES_HOME/memories" "$HERMES_HOME/profiles"

# 1) Seed the mission context on first boot (idempotent).
if [ -d /opt/data-seed ] && [ ! -f "$HERMES_HOME/memories/MISSION.md" ]; then
  echo "[brain-boot] seeding Warrior World context"
  cp -rn /opt/data-seed/. "$HERMES_HOME/" 2>/dev/null || true
fi

# 1b) Ensure the ROOT config enables the api_server (the worker's
#     AGENT_URL expects an OpenAI-compatible completions endpoint).
if [ -d /opt/data-seed ] && [ ! -f "$HERMES_HOME/config.yaml" ]; then
  echo "[brain-boot] seeding root config (api_server :8642)"
  cp -n /opt/data-seed/config.yaml "$HERMES_HOME/config.yaml" 2>/dev/null || true
fi

# 2) Ensure .env has the model key (injected by the SDL).
if [ ! -f "$HERMES_HOME/.env" ]; then
  : > "$HERMES_HOME/.env"
  [ -n "${OPENROUTER_API_KEY:-}" ] && echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" >> "$HERMES_HOME/.env"
  [ -n "${DEEPSEEK_API_KEY:-}" ] && echo "DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY" >> "$HERMES_HOME/.env"
  [ -n "${API_SERVER_KEY:-}" ] && echo "API_SERVER_KEY=$API_SERVER_KEY" >> "$HERMES_HOME/.env"
  [ -n "${LITELLM_MASTER_KEY:-}" ] && echo "LITELLM_MASTER_KEY=$LITELLM_MASTER_KEY" >> "$HERMES_HOME/.env"
fi

# 3) Start the gateway (host gateway serves every profile's API server).
echo "[brain-boot] hermes gateway run (profiles: $(ls $HERMES_HOME/profiles 2>/dev/null | tr '\n' ' '))"
exec hermes gateway run