# Higher-rank continuation files

Status: **EXACT THEOREM PROVED FOR FIXED FINITE RANK AND FIXED POSITIVE DATA
IN THE NO-DIRECT-PORTAL CLASS; GROWING/SINGULAR RANK AND GENERAL PORTAL
NETWORKS OPEN**.

- `HIGHER_RANK_SEPARATION_THEOREM.md` gives the fixed-finite-incidence-rank
  affine separation for `3/2<=r<=2` and the resulting no-go for every fixed
  `r>=3/2` in its exact asymptotic scaling.
- `verify_higher_rank_separation.py` is the exact certificate.  Run from the
  repository root with
  `.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/asymmetric_portal_incidence/verify_higher_rank_separation.py`.
- `search_higher_rank_no_portal.py` is the fast load-fraction discovery
  search and exact type-mixture optimizer.
- `search_higher_rank_full.py` retains every labelled portal subset while
  using the better load-fraction coordinates.
- `search_two_portal_classes.py` implements the exact two-class count
  lumping.
- `search_growing_portal_classes.py` implements its growing-class boundary
  process.
- `HIGHER_RANK_RESEARCH_LOG.md` records the derivation and status boundary.

The search files produce numerical discovery evidence only.  The theorem
depends solely on the exact trace derivation and verifier.
