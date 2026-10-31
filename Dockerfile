# ─────────────────────────────────────────────────────────────
# WARRIOR WORLD WEB3 BRAIN — build once, live on Akash
# Base: the official Hermes image built by CI from public source
# (warriorworld/hermes-brain:base-20261031). This layer adds the
# Warrior World mission seed + gateway boot.
#
# Docker semantic (official Architecture B): the image's own
# ENTRYPOINT (entrypoint-dispatch.sh) runs s6-overlay; the CMD is
# the supervised "main program". We DO NOT override the entrypoint
# (that was the v1 crash bug — it double-started the gateway). Our
# CMD is the main program: seed on fresh volume, then the gateway.
# ─────────────────────────────────────────────────────────────
FROM warriorworld/hermes-brain:base-20261031

# The brain's born-knowing context: MISSION, SOUL, org, memories.
COPY seed/ /opt/data-seed/

# Main-program boot: seed (idempotent) then start the gateway.
COPY brain-boot.sh /usr/local/bin/brain-boot.sh
RUN chmod +x /usr/local/bin/brain-boot.sh

# Leave the official ENTRYPOINT untouched (s6 supervisor).
# CMD = main program: /usr/local/bin/brain-boot.sh
# (env GATEWAY_MODE=api|gateway; default api → OpenAI-compatible
#  completions endpoint the worker's AGENT_URL expects)
ENTRYPOINT ["/usr/local/bin/brain-boot.sh"]
CMD []