# Glued figure-eight exteriors: exact matching reductions

**Problem:** 10900004 / AMR-108-0004, Danciger Question 1.4, queue rank 508.

**Status: unsolved 5/5.** This attempt does not settle whether every torus gluing of two figure-eight exteriors admits a convex projective structure. The known double is credited to Ballas--Danciger--Lee.

The package proves scoped limitations of five approaches: topological transfer from the double, algebraic gluing, spectral matching, bending/scaling families, and finite-cover descent. In particular, an infinite-order gluing matrix cannot match one fixed full-rank diagonal peripheral model, even if the two models are independently scaled along the same ray. This does not rule out different convex structures with genuinely different peripheral shapes.

- [RESULT.md](RESULT.md): exact conventions, five approaches, complete elementary proofs, and remaining gaps
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): primary sources, current-literature limits, and duplicate checks
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated attempt record and completion estimates
- [checks/check.py](checks/check.py): standard-library exact matrix verification
- [checks/results.json](checks/results.json): reproducible check results

A useful convention check is `H_1(N_A;Z)=Z/bZ` for `A=[[a,b],[c,d]]` acting on slope columns; `b=0` means `Z`. Consequently the shears `[[1,k],[0,1]]` include integral homology spheres and cyclic-homology manifolds, not just another description of the double.

All explicit four-dimensional matrices here certify peripheral examples only. No new global figure-eight holonomy, all-representations obstruction, full solution, or historical novelty claim is made. OpenAI tools assisted research, drafting, and verification. The author package is frozen for a fresh independent audit before publication.
