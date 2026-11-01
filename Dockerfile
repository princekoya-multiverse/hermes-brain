# ─────────────────────────────────────────────────────────────
# WARRIOR WORLD WEB3 BRAIN — build once, live on Akash
# Base: the official Hermes image built by CI from public source
# (warriorworld/hermes-brain:base-20261031). This layer adds the
# Warrior World mission seed + gateway boot.
#
# CRITICAL (v5): DO NOT override ENTRYPOINT. The base image's
# entrypoint-dispatch.sh boots s6-overlay as PID 1 — the container's
# supervision tree. `hermes gateway run` DETECTS s6 and hands its
# own supervision to it ("running under s6 supervision"); without
# s6 (enforced by our old ENTRYPOINT override, which made brain-boot
# PID 1) that handoff fails and the gateway exits (was exit-crash on
# 2Gi pod: v1–v4 all died here).
#
# So: ENTRYPOINT stays the official dispatcher; CMD = the "main
# program" s6 runs after boot == brain-boot.sh (seed + gateway run).
# ─────────────────────────────────────────────────────────────
FROM warriorworld/hermes-brain:base-20261031

# The brain's born-knowing context: MISSION, SOUL, org, memories.
COPY seed/ /opt/data-seed/

# Main-program boot: seed (idempotent) then start the gateway.
COPY brain-boot.sh /usr/local/bin/brain-boot.sh
RUN chmod +x /usr/local/bin/brain-boot.sh

# WEB3 DEPLOY POWER: boto3 so the deploy kit can push to Storj from the brain.
COPY deploy-requirements.txt /tmp/deploy-requirements.txt
RUN /opt/hermes/.venv/bin/pip install --no-cache-dir -r /tmp/deploy-requirements.txt || true

# Deploy kit (pure stdlib + boto3) — every manager's power tool.
COPY tools/deploy-assets.py /opt/data-seed/tools/deploy-assets.py
RUN chmod +x /opt/data-seed/tools/deploy-assets.py || true

# Inherit the official ENTRYPOINT (entrypoint-dispatch.sh → s6 as PID 1).
# Main program: /usr/local/bin/brain-boot.sh → runs under s6 supervision.
CMD ["/usr/local/bin/brain-boot.sh"]