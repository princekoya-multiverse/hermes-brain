# ─────────────────────────────────────────────────────────────
# WARRIOR WORLD WEB3 BRAIN — build once, live on Akash
# Base: the official Hermes image built by CI from public source
# (warriorworld/hermes-brain:base-20261031). This layer adds the
# Warrior World mission seed (MISSION, SOUL, org, memories).
# ─────────────────────────────────────────────────────────────
FROM warriorworld/hermes-brain:base-20261031

# The brain's born-knowing context: MISSION, SOUL, org, memories.
# /opt/data is HERMES_HOME — the official image seeds config there
# at boot. We stage our context pack so the first boot already
# knows Warrior World.
COPY seed/ /opt/data-seed/

# On boot the stage2 hook seeds HERMES_HOME from the baked context
# if the volume is empty (idempotent), then stays in the s6 tree.
COPY brain-init.sh /usr/local/bin/brain-init.sh
RUN chmod +x /usr/local/bin/brain-init.sh

ENTRYPOINT ["/usr/local/bin/brain-init.sh"]
CMD ["hermes", "gateway", "start"]