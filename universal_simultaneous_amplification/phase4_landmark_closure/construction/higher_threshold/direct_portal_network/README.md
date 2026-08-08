# Direct portal network branch

This folder studies the direct-portal gap left by the fixed-rank
no-direct-portal theorem.

- `DIRECT_PORTAL_TRACE_AND_Q2_SEPARATOR.md` gives the exact general trace and
  proves the two-portal, one-blade-type obstruction for every `r>=3/2`.
- `verify_q2_scalar_separator.py` regenerates and checks the exact uniform
  rational Bernstein certificate.
- `verify_direct_trace_exact.py` independently rebuilds the full labelled
  direct-portal trace on a rational `Q=3,T=2` instance.
- `search_q2_map.py` and `search_general_map.py` are numerical hostile-search
  tools only.
- `RESEARCH_LOG.md` records the branch history and status distinctions.

No result here is a universal graph obstruction.  Higher-rank direct portal
networks remain open.
