# Geometric research log for Kourovka 21.139

Author metadata: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Independent internal research; no outside outreach.

## 2026-10-17T21:36:44.425362+00:00 — checkpoint 1

Goal-completion best guess: **12%** for the full unrestricted problem, **60%** for isolating and validating the geometric reduction. These are subjective research-progress estimates, not probabilities of truth.

- Read the project AGENTS.md and exact PROBLEM.md. No other approach files read.
- Exact hypothesis: one uniform bound on rational b2 over all finite-index subgroups. Passing to a torsion-free compact-special finite-index subgroup preserves it.
- Primary Wilton v3 (22 January 2026), Theorem A, yields a one-ended infinite-index quasiconvex subgroup when the compact-special group is neither free nor a surface group. It does not state nonzero ordinary or virtual H2.
- Independent candidate amplification: a quasiconvex infinite-index A with b2(A)>0 embeds quasiconvexly as a factor of A*Z; cyclic covers give arbitrarily many copies of H2(A); virtual retraction promotes them to finite-index homology. A child adversarial verifier is checking exact theorem hypotheses and finite-index transfer.
- Central exact gap: prove that a one-ended hyperbolic compact-special group has some finite-index subgroup with nonzero rational H2. Merely stating that claim would transfer the main difficulty; route is blocked at this point until a new mechanism is found.
- Next investigation: make the amplification proof and positivity equivalence fully checkable; test hierarchy/Mayer–Vietoris and immersed-complex shortcuts for hidden assumptions.

## 2026-10-17T21:40:47.213216+00:00 — checkpoint 2

Goal-completion best guess: **18%** for the full problem, **90%** for the geometric reduction/audit subtask. The percentage reflects clarified reductions; no proof of the central missing assertion was obtained.

- Verified Proposition 4.1 (amplification) with an independent adversarial child agent. Arzhantseva Theorem 1 supplies the exact quasiconvex A*Z combination. A single Haglund–Wise virtual retraction yields finite-index pullbacks with b2 at least n·b2(A0), index exactly n times a fixed ambient index.
- Located this same mechanism explicitly in Fruchter–Morales v3, Section 3. It is established background rather than a novel result.
- Proved the exact positivity formulation P is equivalent to the unrestricted target using Wilton and amplification. Marked that route blocked at the missing positive virtual H2 class; P cannot be assumed.
- Developed the sharper candidate equivalent formulation Z2: a hyperbolic compact special group of rational cohomological dimension at most two with zero virtual b2 must be free. The all-dimensions reduction uses induction on cube dimension and a cutting hierarchy with free edge groups. Root independently checked the local geometry; a fresh independent adversarial reviewer is now auditing the full argument.
- Explicitly tested and rejected shortcuts through abstract doubles, folded cube-complex doubles, arbitrary immersed complexes, and unquantified Mayer–Vietoris ranks.
- Downloaded five primary sources with SHA-256 metadata. The first attempt to append Haglund–Wise metadata raced the still-running initial download batch; the append was retried after the batch completed, and no source content was lost.
- Wrote approach_geometry.md. No Git, remote publication, PR, release, queue, or other researchers' files were changed.

## 2026-10-17T21:42:29.552648+00:00 — checkpoint 3, adversarial precision correction

Full-problem completion estimate remains **18%**; geometric reduction/audit subtask **95%** pending final fresh review.

- A fresh independent reviewer found no central circularity on first pass through Section 6, but correctly required separating a finite two-dimensional classifying-space claim from a cohomological-dimension statement after finite-index passage.
- Corrected the cutting lemma to assume embedded two-sided hyperplanes and use subdivision only. The zero-homology induction may first choose a two-sided finite cover; proving that cover free suffices because the original group is torsion-free and virtually free. No unsupported descent of a finite 2D classifying space is used.
- Expanded the edge-group injection argument using convex intersections in the universal cover. Expanded the reversed hierarchy construction using realizations of injective edge homomorphisms, Van Kampen, and the Bass–Serre tree of contractible lifted spaces.
- Root independently checked this local geometry. The fresh adversarial review is still underway; Section 6 remains labeled a candidate until the reviewer finishes.
- All five primary-source files and two derived text files match the recorded SHA-256 hashes.
- No assertion of a solution, new discovery, or outside communication was made.
