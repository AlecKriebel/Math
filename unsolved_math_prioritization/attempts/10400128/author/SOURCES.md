# Primary sources and scope qualifications

Checked 2026-10-06. This bibliography reports inspected primary statements; it does not certify independent re-proofs of the long cited theorems. No complete source document or reading copy is distributed with the authored packet.

## S1. Exact source problem and normalization

T. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), 377–572; publisher PDF says published 1 June 2004.
https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf

Inspected section 7.1, printed page 471, and section 7.3, printed pages 481–483. Problem 7.13 is on printed page 482, PDF page 110, confirmed visually. It concerns the ordinary SU(2) root and an optimistic prescription; the adjacent remark warns about the missing rigorous definition. The source does not restrict the problem to integral homology spheres or three exceptional fibers. The preceding conjecture has an additional 2 pi i factor. These conventions must not be suppressed.

The editor's solutions page was also checked:
https://www.kurims.kyoto-u.ac.jp/~tomotada/solution.html
It has no 7.13 entry. This page is sparse and its absence is not proof of current openness.

## S2. Original optimistic prescription

Hitoshi Murakami, *Optimistic calculations about the Witten–Reshetikhin–Turaev invariants of closed three-manifolds obtained from the figure-eight knot by integral Dehn surgeries*, RIMS Kokyuroku 1172 (2000), 70–79; arXiv:math/0005289v1.
https://arxiv.org/abs/math/0005289
https://arxiv.org/pdf/math/0005289

Inspected introduction and sections 2–3, especially equations (3.1)–(3.6), Definition 3.1, and Remarks 3.3–3.5. The recipe replaces finite products by a potential, exponentiates stationary equations, and adds logarithmic correction terms at a selected solution. It leaves contour and solution choices unresolved. The L(8,1) calculation here is our transparent application of that recipe to a different elementary surgery expression; it is not presented as Murakami's own example or as a proof of its invariant meaning.

## S3. Classical RP3 control and surgery conventions

Robion Kirby and Paul Melvin, *The 3-manifold invariants of Witten and Reshetikhin–Turaev for sl(2,C)*, Inventiones Mathematicae 105 (1991), 473–545.
Author-hosted reading copy:
https://math.berkeley.edu/~kirby/papers/Kirby%20and%20Melvin%20-%20The%203-manifold%20invariants%20of%20Witten%20and%20Reshetikhin-Turaev%20for%20sl%282%2C%20C%29%20-%20MR1117149.pdf

The author copy is an 80-page scanned manuscript, not the final publisher pagination. Its manuscript/PDF page 51, equation (5.12), was inspected visually: it states the even-level secant formula and odd-level vanishing for RP3. Equation (5.11) gives the S2 x S1 normalization. Do not cite manuscript page 51 as a journal page. The exact classical example blocks an ordinary-log substitution, not a formal optimistic limit.

## S4. Broad Seifert asymptotics, qualified

Soren Kold Hansen, *Analytic asymptotic expansions of the Reshetikhin–Turaev invariants of Seifert 3-manifolds for SU(2)*, arXiv:math/0510549v1 (2005), 107 pages.
https://arxiv.org/abs/math/0510549
https://arxiv.org/pdf/math/0510549

Inspected Theorem 1.4 and its discussion, Theorems 4.1 and 4.4, and normalization in section 4.4. Theorem 1.4 treats orientable positive-genus bases and nonorientable even-genus bases. For base S2 it proves the phase-identification claim with at most three exceptional fibers; its larger-fiber formula may retain extra terms. Small additional RP2 cases are stated separately. The paper uses tau(S3)=sqrt(2/N) sin(pi/N), differing by D_N from our sphere-one convention. Its arXiv page lists only v1; no final journal comparison was established here. It must not be advertised as an unrestricted all-Seifert optimistic-limit theorem.

## S5. Current homology-sphere result

Jorgen Ellegaard Andersen, Li Han, Yong Li, William Elbaek Mistegard, David Sauzin, Shanzhong Sun, *A proof of Witten's asymptotic expansion conjecture for WRT invariants of Seifert fibered homology spheres*, arXiv:2510.10678v1 (12 October 2025), 68 pages.
https://arxiv.org/abs/2510.10678
https://arxiv.org/pdf/2510.10678

Inspected introduction, Conjecture 1.1, and Theorem 1.1 with formula (1.8). It gives an exact resurgent decomposition implying the full asymptotic expansion conjecture for Seifert integral homology spheres. The level is k-2 and WRT_k(S3)=1. This is a strong credited result in its stated subclass. It neither states an all-Seifert optimistic prescription nor permits replacing a phase sum by one unqualified logarithm. The live arXiv page lists only v1 and no journal reference. We call it a preprint; no human peer-review status is inferred. Its entire 68-page proof has not been independently audited here.

## S6. Torus surgeries at a different root

Hitoshi Murakami and Anh T. Tran, *Quantum invariants of three-manifolds obtained by surgeries along torus knots*, Quantum Topology 13 (2022), 691–795, DOI 10.4171/QT/175; publisher copyright 2023.
https://doi.org/10.4171/QT/175
https://content.ems.press/assets/public/full-texts/serials/qt/13/4/9208291/online/10.4171-qt-175.pdf
Preprint also inspected: https://arxiv.org/pdf/2011.05484

Inspected publisher introduction and Main theorem (Theorem 9.8), with cross-check against the preprint statement. It uses the alternative invariant at exp(4 pi i/n), odd n, for positive coprime torus parameters a,b and surgery hypotheses p>ab and gcd(p,ab)=1. Its phase/torsion result cannot be imported without changing the target's root and manifold scope. No claim of equivalence between its alternative invariant and the one in Problem 7.13 is made.

## S7. Classical Verlinde input

Georgios Daskalopoulos and Richard Wentworth, *Factorization of rank two theta functions. II. Proof of the Verlinde formula*, Mathematische Annalen 304 (1996), 21–51.
https://math.umd.edu/~raw/papers/verlinde.pdf

Inspected equations (1.1)–(1.2), Theorem 1.4 and displayed specialization (1.5) on the first two PDF pages. We use the theorem together with (1.1)–(1.2): raising sqrt(2/(k+2)) to power 2-2g gives the factor ((k+2)/2)^(g-1). The scanned display (1.5) appears instead to print exponent 1/2; that inconsistent display is not used as authority for the prefactor. Both pages were inspected visually. The trace and modular-functor inputs are standard TQFT facts. The elementary sine inequalities in PROOF.md then prove the displayed polynomial bounds directly. No novelty is claimed for the product-manifold consequence.

## Search boundary

Targeted searches included the problem number, problem ID, exact optimistic-limit terminology with Seifert/lens/Murakami, the editor's solution index, broad Seifert asymptotic-expansion literature, and the currently posted homology-sphere preprint. Unrelated search results and secondary AI summaries were not used as mathematical authority. A bounded search cannot prove that no other later resolution exists.
