# Final mathematical-claims acceptance audit

Date: 2026-10-21 UTC. This accepts a bounded partial-research report, not a solution of the original problem and not any novelty claim.

## Claims checked

1. **Explicit mismatch over Q_p(t), p odd:** accepted. A nonsquare unit u defines the unramified quadratic extension of Q_p; the quaternion symbol (u,p) has invariant 1/2. Residue at t sends (u,p,t) to this class. The finite-support family with this local degree-3 class at t and zero elsewhere pairs nontrivially with the invariant mod-2 dual generator. It cannot be global. Harari–Scheiderer–Szamuely, arXiv:1307.4783v2, Proposition 2.1 and Theorem 2.3, supply exactly the sum pairing and terminal exact sequence used. This is a formal cohomological witness, not a point-evaluation witness on an algebraic variety.

2. **Finite-stage lifting/orbit criterion:** accepted. Degree-4 finite obstruction vanishes at cd=3; rigidified lifts form an H^3 torsor. Local base-section loops act on that torsor, and the ordinary component test uses their orbits. All globally matching stage-2 components must be excluded. The corrected countable finite-module Mittag-Leffler proof is valid; potential lim^1 H^2 contributions and actual profinite section comparisons remain separate.

3. **Rational surface pi_3:** accepted. For simply connected rational surfaces, H_2 is free of rank r and H_3=0. Whitehead's sequence identifies pi_3 with Gamma(Z^r) modulo the image of the fundamental class. Gamma has rank r(r+1)/2. The intersection-form relation is primitive: in the quadratic basis its diagonal and mixed coefficients encode a unimodular integral intersection form (up to the standard dual-basis conventions), so they cannot all have a common divisor greater than 1. The quotient is consequently free of rank r(r+1)/2-1. This also handles Hirzebruch minimal models; it does not rely on every rational surface literally being a blowup of P^2. The checks for P^2 and P^1 x P^1 are correct. The complex computation supplies no arithmetic Galois action or arithmetic k-invariant by itself.

4. **R-equivalence pruning and split products:** accepted. Properness extends rational connecting maps from P^1; removing a third rational point gives A^1 connections. Geometric étale A^1-contractibility in characteristic zero makes the full point-to-section evaluation constant along these connections. A common global rational point therefore matches all local points when each local R-equivalence set is a singleton. In particular split P^1 x P^1 cannot separate the obstruction sets. Pál's arXiv:1002.1731v5, Proposition 7.8 and Definition 12.4, support the stated factorization. The unrigidified evaluation, not an arbitrary choice of rigidified difference class, is what factors.

5. **G/T versus Tian's construction:** accepted. The homotopy long exact sequence gives pi_2(G/T)=pi_1(T) and pi_3(G/T)=pi_3(G); for simple simply connected complex G the latter is Z. Whitehead's cokernel determines integral H_3, so rational surjectivity cannot substitute for integral surjectivity. For split SL_2/G_m, Hilbert 90 makes every point lift to SL_2(F), and elementary matrices supply actual A^1 chains to the identity. Thus its full point evaluation is constant even without properness. Tian's representation quotient instead shifts the first nonzero group one degree higher: its geometric pi_1 through pi_3 vanish. The detailed proof and exact full-tower caveat are in INDEPENDENT_OBSTRUCTION_AUDIT.md.

## Source checks

- Harari–Scheiderer–Szamuely: https://arxiv.org/pdf/1307.4783 , Theorem 2.3 (PDF page 8), pairing in Proposition 2.1.
- Kasprowski–Powell–Teichner: https://arxiv.org/pdf/2006.06127v4 , Theorem 2.13 and Lemma 2.16 (PDF page 25). The alternative Southampton-hosted PDF returned HTTP 403 in this audit; the arXiv version was inspectable.
- Pál: https://arxiv.org/pdf/1002.1731 , Proposition 7.8 and Definition 12.4. Proposition 5.4 also provides a precise characteristic-zero base-extension comparison for smooth geometrically irreducible quasi-projective varieties.
- Tian: https://arxiv.org/html/2606.27699v1 , Construction 5.1. Its stated cohomological separation is not substituted for the requested homotopy separation.

## Acceptance boundary

The report is accepted only as partial analysis with the full reconstruction unverified. The 2024 announced result remains acknowledged; failure to recover its proof is not evidence that no example exists. Neither geometric H_3=0 nor homology-blindness is imposed as an extra requirement on the entire original question: those describe the source's highlighted subclass. No new variety or adelic witness meeting all acceptance conditions has been supplied.
