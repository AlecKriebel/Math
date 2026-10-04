# Five substantive approaches: KP-4.51 / 2927

All times are UTC on 2026-10-04. Estimates describe subjective progress toward a complete resolution, not probabilities or fractions of cases. All five approaches were carried out in this attempt; no sixth search turn is proposed. Source checking and exact controls are part of these approaches, not additional hidden attempts.

## 1. Integral specialization and low-rank algebra

10:29–10:33; full-target completion estimate 5%.

Mechanism: start with the exact Hermitian isometry question and test whether augmentation or rational/complex diagonalization could force an integral basis.

Work: checked the primary K3 statement and its smooth/topological distinction; proved rank-one extension using the Laurent unit group; decomposed the explicit rank-four matrix by its Schur complement. The Schur congruence uses 1/2 and works on every unit-circle fiber, while the integral extension fails for this known matrix.

Result: rank zero and one are settled; augmentation and pointwise definiteness cannot establish integral extension. The known non-extended matrix supplies a concrete adversarial control.

Exact gap: a Laurent-integral, unimodular basis change cannot be recovered merely from rational fiberwise congruences. Blocked as a full route.

## 2. Stabilization, cancellation, and finite-index amplification

10:31–10:35; estimate 10%.

Mechanism: use stable L-theoretic extension and amplify indefiniteness through finite cyclic covers, then try to cancel or descend.

Work: read HT97 Theorem 2 and its threshold; translated r−|s|≥6 into min(b₂⁺,b₂⁻)≥3. Verified that finite covers multiply b₂ and signature, so every indefinite example has covers in that range. Tracked subgroup restriction separately from reduction modulo xⁿ−1.

Result: the high-indefinite region is settled by the cited theorem. Stabilizing the known positive non-extended form with three hyperbolic planes illustrates the invalidity of unrestricted cancellation.

Exact gap: cancelling in minimum index one or two, or descending a splitting from a finite cyclic cover. No such theorem was verified. Blocked.

## 3. Finite-cover gauge obstruction

10:31–10:38; estimate 15%.

Mechanism: exhibit a nonstandard definite lattice in a cyclic cover, then obstruct smoothness using Donaldson.

Work: reconstructed the published characteristic-vector witness for the HT form. Its norm is 4n−8 for n≥3, smaller than the rank 4n. Verified the complete integral matrices, determinants, characteristic parity, positive LDL pivots and witness norms for n=1,…,12. Explained why primitive-circle surgery preserves the ordinary form and produces a simply connected smooth manifold, avoiding an unstated version of Donaldson.

Result: rigorous exclusion of the classical candidate, with attribution to FHMT07. The first two cover degrees are negative controls for the short-characteristic test.

Exact gap: excluding this family is not a proof that every non-extended form has an obstructing finite cover. Extended to a separate general definite argument in approach 4.

## 4. Fourier localization and prime deck orbits

10:33–10:41; estimate 25%.

Mechanism: recover a Laurent orthonormal basis from standard lattices of arbitrarily large prime cyclic quotients.

Work: obtained a uniform lower eigenvalue bound on all unit-circle fibers. Bounded support of integral norm-one vectors independently of cover degree. Split supports into short-range graph components and unwrapped a component in a sufficiently long cyclic quotient. Used strict Cauchy–Schwarz to turn coefficient norm one into Laurent norm one. Used the trace-zero prime deck action to get exactly r full root-line orbits, then a unit-determinant Laurent basis.

Result: full Proposition 4.1 and the definite smooth corollary are written in PROOF.md. This is an independently derived proof of a partial conclusion also claimed in prior literature, not a novelty assertion. It is frozen for independent audit.

Exact gap: indefinite norms give no positive bound on coordinate size, and their norm-one vectors do not form the finite signed orthonormal root set used in the proof. This route does not cover minimum index one or two.

## 5. Low-indefinite constructions and geometric descent audit

10:35–10:44; estimate 25%.

Mechanism: try to turn the explicit non-extended topological form into an indefinite smooth counterexample by one negative stabilization; in parallel reconstruct the published double-cover descent claim.

Work: constructed the five explicit basis vectors in PROOF.md Section 5, yielding det P=−1 and P*(L⊕[−1])P=[1]⊕H⊕I₂. All polynomial coefficients were checked exactly. Read Kawauchi's 2013 proof through the double-cover, leaf and intersection-vanishing reductions, plus its 2014/2018 follow-ons. Compared the primary census v1 and v2 texts and the 2026 journal text.

Result: the proposed one-negative-direction counterexample loses its non-extension obstruction by an explicit integral isometry. Located the unverified prior descent dependencies: Lemma 2.2, Lemmas 2.3–2.4, Sublemma 2.3.1, and the cited exact-leaf criterion. No false-step or counterexample to that source is claimed without proof.

Exact gap: general low-index cancellation/descent or a different closed smooth counterexample. Bibliographic conflict remains unresolved. Full target stays unsolved in this attempt, with prior claims expressly unverified.

## Budget and status

Proposed own queue fields only: Status `unsolved`, Turns `5/5`. No Findings-field change, novelty designation, or `already_solved` status is proposed. The independent audit may falsify or correct this frozen package; it must not silently become additional proof-search turns.
