# Minkowski question-mark fixed points: audited partial results

Problem 30002046 / OWR-11784-003, queue rank 713. Queue: unsolved, 5/5 substantive approaches. The exact-count problem remains unresolved in this bounded investigation. This is an unrefereed AI-assisted research and verification packet, not a solution, novelty claim, global-openness certificate, or proof-assistant certificate.

## Controlling reading and frozen history

The implemented tests use strict inequalities. This is the controlling clarification of the frozen PROOFS.md wording: strict rectangle inequalities are sufficient, not mathematically necessary. Strict monotonicity also permits the corresponding weak inequalities on nondegenerate intervals, with endpoints handled separately. This clarification does not change the verified certificate and licenses no uniqueness inference.

The immutable author/ and independent_audit/ directories preserve the exact reviewed bytes. Historical author statements that review was pending, and author/audit statements that no remote writes had occurred, describe their freeze times. They are superseded for this assembled packet by the completed PASS WITH SCOPE LIMITS audit and this publication guide. They were not silently edited.

## Strongest retained results and remaining gap

For the standard function Q on [0,1], the proofs classify the rational fixed set as {0, 1/2, 1}, exclude quadratic irrational fixed points, and establish at least two additional symmetric roots. The nontrivial lower-half fixed set K is nonempty, compact, and contained in (2/5, 3/7); the full fixed set is {0, 1/2, 1} union K union (1-K).

A complete exact partition has 275 nodes and 138 leaves, with 137 exclusions and one retained interval at depth 128. Every point of K is enclosed between

- 196891866281783104237450 / 468374932927154430517551
- 73080867820262788865501 / 173847946133977969489589

Its exact width is 1/81426020110025487843678548887211712316576276539. One interval is not one root. Opposite endpoint signs establish existence there, not uniqueness or an exact root count. Tangencies, multiple roots, and infinite fixed subsets are not eliminated.

A separate rational-sign bisection constructs one computable irrational, nonquadratic fixed point, with a replayed 160-step instance. The selected point is not certified least, greatest, unique, or transcendental. Conditional derivative and rational-displacement uniqueness criteria remain conditional. The complete enumeration of 342090 reduced rational arguments below 1/2 through denominator 1500 is finite evidence only; it proves no eventual all-denominator bound.

The audit independently reconstructs all terminal intervals, exact endpoint images, adjacency, depths, sign exclusions, the 160 bisections, and the rational scan using a different arithmetic implementation. Six corrupted certificates are rejected. Same-sign endpoint, sign-preserving contact, three-root tiny-interval, and other negative controls guard against overinterpretation. These finite controls supplement the written proofs.

## Source boundaries

The primary [OWR report](https://ems.press/content/serial-article-files/46395), printed page 1323, supplies the intended solution-count question. The conventional [0,1] domain is followed; integer-translated roots of a different real-line extension do not resolve this question. The paragraph itself does not specify that extension.

Fresh audit retrievals matched the recorded PDF hashes and sizes for OWR, the [Gayfulin–Shulga arXiv v2](https://arxiv.org/abs/1811.10139), and [Hussain–Smith–Zhang (2025)](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.699.pdf); relevant rendered pages were inspected. The final Gayfulin–Shulga journal PDF was not inspected. The exact aggregator page returned HTTP 403, and its wording and unavailable raw-corpus contents or hashes are unverified. Other manuscript, abstract-only, and historical-status inspection limits remain in the frozen public source metadata. No exhaustive current literature review or global-openness assertion follows.

Only authored proofs, code, certificates, audits, and public verification metadata are included. No source PDFs, source text extracts, source images, raw external records, private sources, private personal data, or private coordination files are redistributed.

## Portable verification

From any working directory, run Python 3 with no third-party packages or network:

    python3 /path/to/30002046/verify_release.py --self-test
    python3 -O /path/to/30002046/verify_release.py --self-test

The release verifier uses explicit checks active under -O, binds both original manifests and the audit report, enforces the exact file inventory and scope, and runs the independent verifier in the selected normal/optimized mode. It always runs the frozen author's assertion-based verifier without optimization. The -O command therefore does not pretend the author's assertions survive optimization. Both output files must reproduce byte for byte; actual temporary-file corruption tests check the release boundary. REPLAY_RESULTS.json records stable public test outcomes. Repository CI, if absent, is not a pass.

Five-route investigation completion: 100%. Exact-count discovery completion: 0% certified toward a resolution, without discounting the retained partial results. The unresolved uniqueness/count gap is controlling.

Publication preparation checkpoint: 2026-10-05 UTC. Both frozen packets were verified before packaging; the final receipt separately records the exact remote head and readback.
