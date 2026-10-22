# 6200025: equivariant uniqueness of EZ-boundaries

**Already solved, negative; 3/5 substantive approaches used.** A consequence of the published Guilbault–Healy–Pietsch suspension-boundary construction answers Kapovich's exact equivariant question negatively. In the example both boundaries are topological 2-spheres, but the EZ action has two global fixed points and the canonical Gromov action has none.

- [Prior resolution](submission/PRIOR_RESOLUTION.md) gives the source-defined hypotheses and theorem application.
- [Independent audit](audit/AUDIT_REPORT.md) checks those hypotheses and the proof dependencies.
- [Direct special-case check](audit/SPECIAL_CASE_CHECK.md) constructs a compact ball and verifies nullity and the extended action for the surface example.
- [Citation addendum](CITATION_ADDENDUM.md) corrects the Section 3 locator while preserving the frozen originals.

The `submission` and `audit` directories are exact frozen packages, including their original manifests. Statements there about pending review or remote writes refer to the respective freeze times. The completed audit accepts the negative disposition with one citation correction.

From this directory run `python3 verify_publication.py`. It checks the exact file set, all byte counts and hashes, the frozen package bindings, both control replays, and corruption-detection controls. To include the queue check, add `--queue ../../QUEUE.md`.

Finite controls supplement the mathematical arguments; they do not formally verify the cited deep theorems or analytic proof. No new result, earliest priority, or general topological-classification claim is made. Only original exposition and permitted public verification metadata are included.
