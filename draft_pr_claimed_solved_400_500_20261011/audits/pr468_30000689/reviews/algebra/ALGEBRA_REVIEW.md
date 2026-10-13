# PR468 independent algebra-family adversarial review

Scope: problem 30000689; exact author head `8527ccdba064bca52035fc6c8d96caa750ac9c00`. Review completed 2026-10-12 UTC. Assignment completion estimate: **100%**.

## Verdict and exact scope

**PASS for the dimension-jump argument and the obstruction to PL embedding (PROOF.md Sections 1–2, lines 15–75).** No substantive mathematical gap was found in this family. The source sphere need not be PL. The ambient sphere supplied by a hypothetical PL embedding can be taken to be PL and to retain the original complex without subdivision. The same generic coefficient field serves both rings.

This is a bounded mathematical verdict. It does not certify the separate topological-to-PL theorem in Section 3, the dimension-four bistellar transfer in Section 4, or priority/novelty. Those require the other assigned families. In particular, this report alone does not justify declaring the entire original topological problem solved.

Independence: I read only the frozen author proof, source gate, and explanatory addendum before recording INITIAL_VERDICT.md. I have not read any old audit or any other new review. No PR, QUEUE, Git index, branch, publication, or external communication was changed.

## 1. Arbitrary topological source: local links are sufficient

For a nonempty face sigma of dimension k and a point x in its relative interior, the simplicial local model gives

`H_i(|S|, |S| minus {x}; Z) = reduced H_{i-k-1}(link_S(sigma); Z)`.

One can obtain this directly from the local product `R^k times cone(link(sigma))`, using excision and the relative product formula. The left group is Z only in degree 2d and zero otherwise, since |S| is a topological 2d-manifold. Therefore each link has the homology of `S^{2d-k-1}`. The empty face is covered by the global hypothesis |S| homeomorphic to S^{2d}. Purity follows by applying the local calculation at a point interior to each maximal simplex: its dimension must be 2d.

This proves the local, integral homology-sphere condition, rather than merely a global homology condition. It does not claim that a link is homeomorphic to a sphere. The universal coefficient theorem carries the result to any field. Reisner's criterion then gives Cohen–Macaulayness, and the homology-sphere form gives the Gorenstein reduction with socle degree r=2d+1. Thus the h-vector is the Hilbert function after a regular linear parameter sequence and is symmetric: `h_d=h_{r-d}=h_{d+1}`. Equivalently, the nondegenerate graded Poincare pairing of the Artinian Gorenstein reduction gives the same equality.

The published KX article explicitly distinguishes this local definition in Section 2.1, p.1315; its Section 2.3, p.1317, records the Gorenstein generic reduction. The proof's use of local homology is valid even for noncombinatorial high-dimensional triangulations.

## 2. Exact quotient jump: independent derivation

Write `R=F[x_v : v in V(S)]`, `A=R/I_S`, `C=R/I_K`, and `B=R/I_L`. The first faces removed from S to form K have d+2 vertices. Hence `(I_S)_j=(I_K)_j` for every j<=d+1, with the same multiplication maps whose total degree stays in that range. In particular, the identity applies to both differentials in

`C_{d-1} tensor wedge^2 F^r -> C_d tensor F^r -> C_{d+1}`.

For a regular sequence Theta on A, positive Koszul homology on A vanishes. Therefore `H_1(Theta;C)_{d+1}=0`. This is not a claim that C itself is Cohen–Macaulay, or that Theta is regular on C.

Because T is a missing face and every proper subset is already present, adding T introduces exactly one surviving monomial in total degree d+1, namely x_T; lower pieces are unchanged. Let `M=ker(B->C)`. Then `M_j=0` for j<=d and `M_{d+1}=F x_T`. Since every theta_i has degree one,

`H_0(Theta;M)_{d+1} = (M/Theta M)_{d+1} = M_{d+1}`.

The short exact sequence of graded modules `0->M->B->C->0` gives a short exact sequence of their Koszul complexes, whose long homology sequence in this degree is

`H_1(Theta;C)_{d+1} -> H_0(Theta;M)_{d+1} -> H_0(Theta;B)_{d+1} -> H_0(Theta;C)_{d+1} -> 0`.

Its left term is zero. Thus the monomial survives after taking the quotient, and its kernel dimension is exactly one. Together with agreement in degree d and agreement of A/C in degree d+1, this proves the two displayed dimensions in the author proof.

Potential circularity falsified: this uses regularity on A alone, established from the original topological sphere. It does not use Lefschetz for S, a possible embedding of L, or an unsupported regularity assertion on B.

## 3. Generic restrictions and the ambient extension

AP v3 Theorem 2, p.1, assumes a finite complex X and a PL embedding into a PL manifold M. It returns a triangulation of M containing X itself. The next paragraph explicitly allows changing the map; the proof on pp.3–5 uses subdivisions and contractions in the PL category. Thus applying it with X=L and M the standard PL sphere yields a finite PL ambient triangulation P containing the unsplit L. The hypothesis does not require that the original source S be PL or that its higher-dimensional simplices be contained in P. [Full author source](https://arxiv.org/pdf/2404.12265v3).

Relabel P so that V(S)=V(L) is a subset of V(P). Coefficients `a_ij` for the columns in this subset remain algebraically independent. For every r-vertex facet of S, the determinant of its parameter submatrix is a nonzero polynomial in these independent indeterminates. Consequently the restricted parameters form an l.s.o.p. on A. A is Cohen–Macaulay, so this ordered parameter sequence is regular. The extra coefficient columns are a field extension and preserve both these facts and all graded dimensions. No parameter specialization is needed, and there is no conflict between choosing generic parameters for P and for S.

A subtle point is that the quotient on B uses all r ambient linear forms, even though its Krull dimension is d+1. Overlong linear quotients are legitimate; the argument makes no claim they are a regular sequence or an l.s.o.p. on B for d>=1.

## 4. KX applicability and descent of multiplication

Published KX Theorems 1.2–1.3, p.1314, give anisotropy of the form `l^{n-2m}u^2` with `l=sum x_j`, over the generic rational-function field `Q(a_ij)` when the (n-1)-complex is a homology sphere over F2. Section 2.3, p.1317, specifies the generic coefficients. P is an integral homology sphere, so it satisfies the F2 requirement. Taking n=r=2d+1 and m=d gives exponent one. This is exactly the form used by the author. The characteristic-zero statement is Theorem 1.3; Theorem 1.2 supplies its referenced form. Theorem 1.3's proof in Section 5, pp.1329–1330, supports the stated field change. [Published source](https://www.numdam.org/item/10.5802/alco.298.pdf).

If multiplication by l kills u in degree d, it also kills u^2 in degree 2d+1. Anisotropy gives u=0. Gorenstein symmetry on P makes the adjacent degrees equal in dimension, turning this injection into a surjection.

The inclusion L subset P gives a surjective graded homomorphism `F[P]->F[L]`, using ghost variables outside V(L). Its kernel contains all variables outside L and all further nonfaces. Both Theta and l have the intended restricted images, so there is a surjective graded map of the reductions. In a commutative multiplication square, surjectivity of the top horizontal map and both vertical maps implies surjectivity of the bottom map: lift a target class, choose a preimage upstairs, and project it. Injectivity is not needed to descend. The target's dimension is h_d+1 while the domain's is h_d, contradicting surjectivity. This completes the PL obstruction.

## 5. Independent exact controls and adverse parameter choice

`independent_face_ring_controls.py` imports no author checker, author results, or old audit. It works over the prime field of order 1009. It first eliminates the linear parameters and then computes ideal relations as polynomials in the remaining free variables. Every numerical parameter matrix used as valid is separately certified by full-rank minors on every source facet.

There are 16 valid cases: d=1,2,3,4; spheres `boundary(Delta^d) * boundary(Delta^{d+1})`, both unchanged and with one stellar facet subdivision; two deterministic parameter choices each. In every case the independently expanded h-vector and the three reductions give

`A_d=C_d=B_d=h_d`, `A_{d+1}=C_{d+1}=h_{d+1}`, and `B_{d+1}=h_{d+1}+1`.

In all eight d<=2 cases, a second calculation forms the actual total-degree Koszul differentials in monomial bases and verifies `dim H_1(Theta;C)_{d+1}=0` by exact ranks.

An adverse d=1 control uses Theta=(x_0,x_1,x_2), where T={0,1}. This matrix is full row rank but is not an l.s.o.p. on the source; some facet minors fail. The restored monomial x_0*x_1 dies in the quotient, B_2 and C_2 have the same dimension, and the independent Koszul calculation finds H_1 dimension one. This confirms that full row rank and pre-quotient monomial counting alone would be inadequate. The actual proof supplies the missing hypothesis.

A separate d=0 external-singleton control uses two source points and a ghost third vertex. The reductions give dimensions (1,1) and (1,2) in degrees (0,1), respectively. These are consistency checks, not numerical substitutes for the generic algebraic theorem or any topological theorem.

## 6. Boundary and wording recommendations

- For d>=1 every singleton in T is a proper subset, so the missing-face hypothesis forces all its vertices to be actual source vertices. There is no hidden extra-vertex issue. For d=0 the usual actual-vertex convention is vacuous; the alternative convention produces three points in a two-point space, as the proof states.
- PROOF line 49 says Theta is not an l.s.o.p. on B because its dimension is d+1. That explanatory sentence should be explicitly scoped to d>=1: at d=0, r=d+1=1. This is a minor boundary wording issue, not a failure of the theorem.
- The phrase “over any field” in Section 1 is valid as a conditional lemma with a regular linear sequence. A generic linear l.s.o.p. over a finite base field can require a coefficient extension. The actual use is over Q(a_ij), so no finite-field existence issue enters the proof. State this condition explicitly in a polished paper.

## Mechanism / evidence / status / exact gap

| Mechanism | Checkable evidence | Status | Exact gap |
| --- | --- | --- | --- |
| Local topological links imply CM/Gorenstein source | Local relative homology formula; generic facet determinants; source theorem locators | PASS | None for algebraic use; no PL source is inferred |
| Added face survives quotient | Explicit graded Koszul sequence and vanishing proof; 16 quotient controls, 8 Koszul controls, one adverse control | PASS | None; finite controls are not the general proof |
| Hypothetical PL target preserves L | Independently retrieved AP full author theorem and proof | PASS | Published version DOI full text was inaccessible; exact used statement verified in v3 |
| Ambient generic anisotropy | Independently retrieved/visually inspected KX published theorem page and complete relevant sections | PASS | None for the integral/F2 sphere actually used |
| Quotient inherits middle surjection | Explicit graded lifting argument | PASS | None |
| Arbitrary topological embedding in d>=3 and d=2 | Outside this family's assigned verification | NOT CERTIFIED HERE | Requires separate topological review |
| Original-problem priority | Not begun, per assignment | NOT AUDITED | Requires mathematical gate plus later primary-source priority audit |

Strongest verified result: for every finite triangulation S of the topological sphere S^{2d} and every missing d-face T, the augmented d-skeleton has no PL embedding into the standard PL sphere of dimension 2d. The proof of this result has no remaining substantive algebraic gap.
