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

# 2) Root .env: model keys + WEB3 DEPLOY CREDENTIALS (injected by the SDL).
if [ ! -f "$HERMES_HOME/.env" ]; then
  : > "$HERMES_HOME/.env"
  for V in OPENROUTER_API_KEY DEEPSEEK_API_KEY API_SERVER_KEY LITELLM_MASTER_KEY \
           STORJ_ACCESS_KEY STORJ_SECRET_KEY STORJ_ENDPOINT STORJ_BUCKET \
           CF_API_TOKEN CF_ZONE_ID GITHUB_TOKEN; do
    eval "VAL=\${$V:-}"
    [ -n "$VAL" ] && echo "$V=$VAL" >> "$HERMES_HOME/.env"
  done
fi

# 2b) Every PROFILE gets its own .env with the FULL key set —
#     multiplex auth + full autonomous powers (model + Web3 deploys).
if [ -n "${API_SERVER_KEY:-}" ]; then
  for pd in "$HERMES_HOME"/profiles/*/; do
    [ -d "$pd" ] || continue
    if [ ! -f "$pd.env" ]; then
      echo "[brain-boot] powering profile $(basename "$pd")"
      echo "API_SERVER_KEY=$API_SERVER_KEY" > "$pd.env"
      for V in OPENROUTER_API_KEY DEEPSEEK_API_KEY \
               STORJ_ACCESS_KEY STORJ_SECRET_KEY STORJ_ENDPOINT STORJ_BUCKET \
               CF_API_TOKEN CF_ZONE_ID GITHUB_TOKEN; do
        eval "VAL=\${$V:-}"
        [ -n "$VAL" ] && echo "$V=$VAL" >> "$pd.env"
      done
    fi
  done
fi

# 2c) Deploy kit — every profile can push to Storj + Cloudflare.
if [ -d /opt/data-seed/tools ] && [ ! -f "$HERMES_HOME/tools/deploy-assets.py" ]; then
  cp -rn /opt/data-seed/tools/. "$HERMES_HOME/tools/" 2>/dev/null || true
  chmod +x "$HERMES_HOME"/tools/*.py 2>/dev/null || true
fi

# 3) Start the gateway (host gateway serves every profile's API server).
echo "[brain-boot] hermes gateway run (profiles: $(ls $HERMES_HOME/profiles 2>/dev/null | tr '\n' ' '))"
exec hermes gateway run