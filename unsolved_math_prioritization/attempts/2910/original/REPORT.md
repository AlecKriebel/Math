# Research report: complement-torus unknotting

## Disposition

The full KP-4.34 problem remains unresolved by this work. Stop: stalled partial audit, 3/5 approaches, with explicit geometric gaps. No new solution, counterexample to the target, or novelty claim is made.

The exact target is the surface-unknotting question in K3 Problem 4.34, not an older problem sharing a numerical label. The primary statement allows smooth and locally flat categories. This packet studies the smooth version and requires standard `S^4` after every individual surgery, rather than just after a whole collection. It does not silently narrow the target to spun, orientable, or genus-zero surfaces.

## Literature findings, checked 2026-10-06

K3, printed pp. 218–219, still presents the general question and distinguishes the unrestricted-ambient result, special spinning constructions, and a proposed stabilization route. Its report of the two-surgery/light-bulb route is not an ambient-preserving proof. The primary PDF was downloaded, text-inspected, and the problem page visually inspected. The numeric UnsolvedMath page failed retrieval (web error; direct HTTP 403); exact identity was instead established by the hash-bound source record and actual primary statement.

Larson's paper is published at **109–124**, not 171–190. The inspected arXiv v2 supplies canonical framing conventions, the single-torus homology calculation, product spinning, and an ambient-standardness theorem for unknotted surgery tori. These are existing results, not discoveries of this packet. The cited Theorem 3.9 has no hypothesis that the classical knot is fibered.

Larson–Meier, *Fibered ribbon disks*, Theorem 1.5, concerns spins of fibered classical knots. Its statement uses one link of tori when the fiber genera agree and two sets when they differ. This restricted theorem does not imply the general problem. The arXiv v2 landing page identifies an accepted version and gives the 2015 published journal reference.

Baykur–Sunukjian, *Round handles, logarithmic transforms, and smooth 4-manifolds*, Theorem 9 and the introduction, address ambient cobordisms; intermediate manifolds need not retain the original diffeomorphism type. Their Proposition 13 explicitly treats stabilization by a manifold containing `S^1 × S^3`. Thus applying their general cobordism result does not supply the missing stagewise relative statement. Their arXiv v3 is a submitted manuscript associated with the 2013 journal article.

No full-resolution claim was identified in the bounded primary-source/current-search pass. This is not an exhaustive literature guarantee, and absence of search hits supplies no mathematical or novelty evidence.

## Three approaches and stopping points

1. **Canonical slope and marked-exterior reduction.** Proved the standard `H_1 = Z/pZ` calculation directly. Only `p=±1` can pass the ambient test; the marked exterior also requires a nonabelian quotient calculation. Missing: the required tori and a standard-sphere recognition proof for each output.
2. **Spin classical surgeries and audit partial fillings.** Recovered the known sequential spun-knot route. Constructed a two-torus product example with final ambient `S^4` but no permissible first surgery in either order. Missing: a spinning or equally strong local model for an arbitrary surface. The example rejects a proof shortcut, not the target conjecture.
3. **Stabilization and relative extension.** Proved that complement surgery preserves surface type and normal data, and that an exterior extension preserving the surface makes the surgery pair-neutral. Missing: a genus-preserving, surface-tracked replacement of a stabilization–isotopy–destabilization process with every ambient stage standard. The direct approaches stalled; two further approaches were not spent on restating the same gap.

## Verification limits

Finite Smith-invariant diagnostics independently test the algebraic presentation in Proposition 1 on a deterministic family of unimodular gluing matrices and check the Hopf-link homology distinction. They cannot certify an embedded torus, smooth standardness, or a surface isotopy. The written geometric arguments remain subject to independent mathematical review.

The initial inherited-work gate inspected the complete exact-ID record and report. The report was empty and the record only had literature triage, so substantive work was permitted. Bounded connector checks covered exact ID/problem-number PRs, commits, branches, default-branch code, and a target status-file path; no prior target proof artifact was returned. Broader torus-surgery PR hits concerned other problems. This is bounded repository triage, not a claim that every repository ref was exhaustively inspected.

## Sources

- [K3 primary book](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Problem 4.34.
- [Larson, arXiv:1502.06834v2](https://arxiv.org/abs/1502.06834v2), §§2.1–2.3, Proposition 3.6, Theorems 3.9 and 5.1.
- [Larson–Meier, arXiv:1410.4854v2](https://arxiv.org/abs/1410.4854v2), Theorem 1.5; [published DOI](https://doi.org/10.1142/S0218216515500662).
- [Baykur–Sunukjian, arXiv:1009.0514v3](https://arxiv.org/abs/1009.0514v3), introduction, Theorem 9, Proposition 13; [published DOI](https://doi.org/10.1112/jtopol/jts027).
