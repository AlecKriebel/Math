# A degree-three smoothness certificate for real osculating Schubert curves

**20000236 / AIM-ALGEBRAIC_GEOMETRY-0236. Status: unsolved, 2/5 approaches. Independent review pending.** The original general complex-smoothness question remains unresolved. This package extends the imported degree-two argument to a conditional degree-three criterion and one explicit infinite family. No priority claim is made.

## 1. Exact source and credited prior work

Let E=H^0(P^1,O(n−1)), G=G(k,E), N=k(n−k), and let x_1,...,x_s be distinct **real** points. Partitions lambda_i lie in the k by (n−k) rectangle, and sum |lambda_i|=N−1. Let S be the scheme-theoretic intersection of their osculating Schubert varieties. AIM Problem10.4 asks whether the entire complex curve S is smooth, beyond the known smoothness of its real locus. The preceding Theorem10.3 supplies the real hypothesis; the trailing Osserman sentence introduces a different Problem10.6.

We use the standard proper-intersection theorem and the reducedness/real-smoothness results recalled and proved in Levinson, *One-dimensional Schubert problems with respect to osculating flags*, Corollaries2.9–2.10. His Conjecture4.4 is the same general complex-smoothness question. Corollary2.10 also shows that each irreducible component has a nonempty real normalization and a separating real locus. These results are credited dependencies, not reproved in full here.

The full imported upstream report was read. It already proves smoothness for Plucker degree at most2, the two-condition Richardson case, and the exact alternating-form kernel criterion for all-box G(2,n) curves. It also supplies the degree-two G(2,6) families (2,2)+three boxes and (3,2)+two boxes. Those are **prior imported contributions**, not new work of this campaign. The Wronskian-kernel criterion does not by itself prove emptiness of the complex singular incidence.

## 2. A conditional degree-three criterion

**Theorem.** Under the source's real distinct-point assumptions, if

    deg_Plucker(S)<=3 and chi(O_S)>=1,

then S is smooth over C.

Here chi means h^0−h^1, even if S is disconnected. One must not substitute h^1 or a connected-curve genus without proving connectedness.

First, every irreducible component is defined over R. This follows from Levinson's Corollary2.10, and can be checked directly from total reality as follows. Add a single-box condition at a variable real y distinct from all marked points. Properness makes S intersect that Schubert hyperplane in a finite scheme, and the Mukhin–Tarasov–Varchenko theorem makes every intersection point real. Every positive-degree component meets the hyperplane. As y varies through infinitely many values, any fixed point U of G can occur for only finitely many y, because its nonzero Wronskian has finite degree. Thus each component contains infinitely many real points. An irreducible complex curve and its conjugate sharing infinitely many points coincide, so each component is defined over R. The Wronskian is nonzero: in characteristic zero, a basis of polynomials with distinct leading degrees has a Wronskian with nonzero leading coefficient, the Vandermonde determinant of those degrees. This argument concerns only an added box, not an assertion that all prescribed partitions are boxes.

Let nu:tilde(S)->S be the normalization, with r irreducible components, and let g_1,...,g_r be their normalization genera. Reducedness and purity give the exact sequence

    0 -> O_S -> nu_* O_tilde(S) -> Q -> 0,

where Q has finite length delta, supported on the singular locus. Hence

    delta = r − sum_j g_j − chi(O_S).                       (1)

All real points of S are smooth. Conjugation pairs its nonreal singular points and preserves their local normalization defects, so delta is even. Since each component has positive integer degree, r<=3.

If r<=2, (1) and chi>=1 give 0<=delta<=1. Evenness forces delta=0. If r=3, all three components have degree1, hence are lines, each defined over R. Distinct real projective lines, if they meet, meet at a real point. Such an intersection is singular in a reduced pure union of distinct lines, contradicting real smoothness. Therefore the three lines are pairwise disjoint and themselves smooth, so again delta=0. A normal curve over C is smooth. This proves the theorem.

The chi hypothesis matters: a real line union a real conic can have two nonreal intersection singularities and chi=0. The imported example z(x²+y²+z²)=0 illustrates exactly this failure. It does not refute the theorem above or the original Schubert conjecture.

## 3. A concrete longer-partition family

**Corollary.** For every n>=5 and any four distinct real osculation points, the curve in G(2,n) defined by

    lambda=(n−3,n−5) at x_0, and a single box at x_1,x_2,x_3

is complex-smooth. In particular, (3,1) plus three boxes in G(2,6) is smooth.

The partition is valid, |lambda|=2n−8, and |lambda|+3=2n−5=dim G(2,n)−1. We prove its degree and Euler characteristic scheme-theoretically rather than inferring them from real point counts.

Choose a basis adapted to the flag at x_0. The Schubert inequalities for lambda are exactly

    U subset F_5,       dim(U intersect F_2)>=1.

Thus the Schubert variety is the same four-dimensional variety inside G(2,F_5), independent of n. Write its surviving Plucker coordinates as

    w=p_12,   (u_1,u_2,u_3)=(p_13,p_14,p_15),
               (v_1,v_2,v_3)=(p_23,p_24,p_25).

All p_ij with 3<=i<j<=5 vanish. The remaining Plucker relations are exactly the three 2 by2 minors of the matrix with rows u and v. This is a scheme description: the rank-at-most-one projection U->F_5/F_2 imposes those vanishing coordinates, and substitution into the Grassmannian Plucker ideal gives the stated minors. Consequently its homogeneous coordinate ring is

    A=C[w,u_1,u_2,u_3,v_1,v_2,v_3]/I_2([u;v]).             (2)

This is the projective cone over the Segre P^1 times P^2. For clarity, the algebra used here is the standard codimension-two maximal-minor case of Hilbert–Burch. The ideal has height2: rank-one 2 by3 matrices form a four-dimensional affine cone in six variables, parameterized by an outer product; the minors generate its prime ideal. The two row syzygies give the exact graded resolution over the seven-variable polynomial ring R,

    0 -> R(−3)^2 -> R(−2)^3 -> R -> A -> 0.

The ideal is perfect, so A is Cohen–Macaulay of dimension5, and

    Hilb_A(t)=(1−3t²+2t³)/(1−t)^7=(1+2t)/(1−t)^5.         (3)

Each remaining box condition is a Plucker hyperplane. By properness of distinct-point osculating intersections, its three linear equations have joint height3 in A. In a Cohen–Macaulay ring they are a regular sequence. The resulting curve's coordinate ring therefore has

    Hilb_S(t)=(1−t)^3 Hilb_A(t)=(1+2t)/(1−t)^2.             (4)

For every positive integer m, its Hilbert function is (m+1)+2m=3m+1. Thus the Plucker degree is3 and chi(O_S)=1. Reducedness and smoothness at real points come from the credited Schubert theorem. The criterion in Section2 now proves the corollary for all distinct real configurations. No general-position substitution for distinct real points has been made.

As a separate check, the complementary partition in the 2 by(n−2) rectangle is (3,1). Repeated Pieri gives the degree f^(3,1)=4!/(4*2*1*1)=3, in agreement with (4). This degree computation alone would not establish chi or smoothness.

## 4. Verification and remaining gap

The exact controls check the Plucker specialization, both determinantal syzygies, Hilbert-series identity, Hilbert coefficients, hook-length/Pieri count, and the partition/flag indices for a range of n. These algebraic checks are not a computer enumeration of all real configurations. The written determinantal-ring and normalization arguments supply the all-configuration theorem.

This result does not settle general Schubert curves of larger degree, the all-box G(2,6) problem, arbitrary complex osculation points, collided points, or the stable boundary of a compactified family. In particular it does not show that the imported Wronskian-kernel incidence has empty image over every real configuration. Those are the original unresolved difficulties. The earlier degree-two and kernel results are retained as credited upstream context only.

Work used the inherited native runtime without model or reasoning changes; its exact model identifier was not exposed. No novelty, publication priority or human peer-review claim is made. Separate adversarial review is required before a PR.

### Primary sources and standard algebra

- AIM, Problem10.4 and preceding hypotheses: https://aimath.org/pastworkshops/degenalggeomproblems.pdf
- Levinson, Corollaries2.9–2.10 and Conjecture4.4: https://arxiv.org/abs/1504.06542 ; published DOI https://doi.org/10.4153/CJM-2015-061-1
- Mukhin–Tarasov–Varchenko, total reality theorem: https://doi.org/10.4007/annals.2009.170.863
- Standard Hilbert–Burch theorem is used only for the explicit height-two maximal-minor ideal in (2); its resolution and all shifts are displayed above.
