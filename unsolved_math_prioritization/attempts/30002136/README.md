# Universal SL3 trace-equivalence: incomplete research

UnsolvedMath 30002136 / OWR-12007-016, queue rank 435. **NO FULL RESOLUTION; five of five substantive author turns exhausted.**

Exact target: find two fixed nonconjugate words u,v in F2=<a,b> such that tr(u(A,B))=tr(v(A,B)) for every A,B in SL3(C), or prove that no such pair exists. A finite list of equal matrix traces is not a proof of universal equality. A single exact unequal trace does disprove a proposed pair.

Source: Ilya Kapovich, Question 0.1, Oberwolfach Report 35/2012, printed p2195, https://ems.press/content/serial-article-files/46404 , DOI https://doi.org/10.4171/OWR/2012/35 . The original definition uses standard traces. See TURN_1.md for the proof relating this universal condition to characteristic polynomials in dimension three.

Prior credit: Lawton–Louder–McReynolds, Groups Geom. Dyn. 11 (2017), 165–188, https://arxiv.org/abs/1312.1261 , §§4.2–4.3; GMU MEGL Special Words project (2016–2017), https://megl.science.gmu.edu/wp-content/uploads/2021/03/MEGL_Summer_2016_Final.pdf . No novelty claim is made for the elementary reductions or short-word obstructions. Aougab–Lahn–Loving–Miller, Math. Ann. 392 (2025), §1.2, still identifies the higher-dimensional trace-pair question as open: https://link.springer.com/article/10.1007/s00208-025-03103-y . Literature checked 2026-10-03; no later full resolution located.

Source metadata: UnsolvedMath Contributors, ulamai/UnsolvedMath snapshot 37e53eabe540fb458758e198be61634bd02ee008, CC-BY-4.0; original publications retain their terms. Both corpus hashes were checked against repository manifest 55589bae6bad2d3e2f696e08645330ff1219b709 before work. The current problem has no keyed imported research report; imported triage and repository desk assessment consume no author turns. Source/prior gate found no previous target attempt in checked user/repository sources.

Lawton–Louder–McReynolds §4.3 additionally reports a computer search with no SL3-equivalent pairs through length20, in the discussion of positive candidates. Smaller checks here are reproducibility controls, not improved search bounds.

Strongest partial result: no nonconjugate universal trace companion exists if, in some free basis, a cyclically reduced word contains either at most three occurrences of one generator with arbitrary signs, or at most five occurrences all of the same sign. The other generator's exponents are unbounded. The candidate companion is arbitrary in all F2; unsigned-count and exponent-sum invariants force it into the same form before coefficient reconstruction. See TURN_5.md for the combined theorem and LOW_MINORITY_PROOF.md for that essential invariant.

Run `python check_turn_1.py` through `python check_turn_5.py` for exact checks (Python3 and SymPy; check_turn_2.py needs only the standard library). `python verify_manifest.py` verifies the final file-hash binding. The numbered proof notes supply general arguments; their finite sanity checks do not settle the full target. Earlier TURN_n_MANIFEST files record their historical checkpoint bytes; mutable ledger/log files should be checked against the final manifest, or at the corresponding historical commit.

These are work-in-progress mathematical notes and reproducible exact checks, awaiting independent audit. No queue status, result PR, or full-solution/novelty claim is implied by a checkpoint. The full unrestricted existence question remains open in this work.
