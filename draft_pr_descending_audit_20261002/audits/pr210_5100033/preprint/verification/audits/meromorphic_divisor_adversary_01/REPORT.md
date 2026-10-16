# PR210 independent meromorphic-divisor adversarial audit

Audit target: PR210, problem 5100033 / AMR-050-0033, immutable head `2180d64b648b81ac660a792f7823d0b715f9cf12`.

Final mathematical assessment: **clean pass for the submitted signed-area constancy theorem in its stated nondegenerate elliptical, odd least-period scope, including every coprime star turning number. No blocking analytic gap or counterexample was found.** This is a mathematical audit of that theorem, not a novelty, priority, or publication-readiness assessment. The numerical controls are supporting evidence; the universal conclusion rests on the derivations below.

Final UTC checkpoint: 2026-10-15T12:07:21Z. Best-guess completion of this assigned audit: 100%.

## Independence and inputs

I read the intake and immutable original `PROOF.md` and `SOURCES.md`, then froze `INDEPENDENCE_FREEZE.md` at 2026-10-15T11:57:13Z. At that point I had not read any inherited review, checker, verification output, root research note, or other new review. I never subsequently opened the inherited review/checkers or another shard's files. The source PDF manifest was read after the freeze. I independently wrote `check_meromorphic.py`; it neither imports nor invokes inherited code.

After the independent derivations and the first successful fresh control run, the parent sent a short source-scope observation and reported its own lack of a formal pole/divisor gap. This arrived after the material mathematical assessment was made. Its useful presentation caveat is preserved below: primitive/repetition/star conventions should be described as the proof's scope or a deduction, rather than attributed verbatim to the source papers.

The three private primary PDF files reused from the preceding case match the submitted SHA256 values exactly:

| File | SHA256 |
| --- | --- |
| invariants_v11.pdf | c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da |
| invariants_final.pdf | c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42 |
| stachel_published.pdf | 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8 |

`results.json` also verifies the intake hashes of the immutable proof, source list, and source PDF manifest. Private text extracts and the one page image used to check the source-paper sign typo remain under excluded `private/`. No primary PDF was copied or redistributed.

Primary references consulted:

- Reznik, Garcia, Koiller, [arXiv:2004.12497v11](https://arxiv.org/pdf/2004.12497v11), Table 7, printed p.9: the primed focal-pedal area product is k605,a, with odd parity.
- Their [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 7 and §3.7, printed p.349: the primed product is k606 and the unprimed product k605. The section identifies the primes with the outer polygon.
- Stachel, [On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2), Theorem 4.3 and (4.9), printed p.1614: the canonical coordinate, step, modulus, and semiaxes used in the proof.
- Live primary NIST [DLMF §22.4, Tables 1 and 3](https://dlmf.nist.gov/22.4), [§22.8](https://dlmf.nist.gov/22.8), and [§22.13, Table 1](https://dlmf.nist.gov/22.13), read on 2026-10-15. Periods and quarter shifts were checked against Table 22.4.3, and derivatives against Table 22.13.1.

## Exact claim, assumptions, and success criterion

Fix semiaxes a>b>0 with c²=a²-b², and a strictly nested nondegenerate confocal elliptical caustic with semiaxes α>β>0. Set k=c/α, k'=β/α, and K=K(k), K'=K(k'). For a primitive N-periodic family use

\[
P(w)=(-a\operatorname{sn}w,b\operatorname{cn}w),\qquad
v=\frac{2K\tau}{N},\quad\delta=2v,\quad
\gcd(N,\tau)=1,\quad0<\tau<N/2,
\]

\[
a=\alpha\frac{\operatorname{dn}v}{\operatorname{cn}v},\qquad
b=\frac{\alpha k'}{\operatorname{cn}v}.
\]

Here 0<k<1 and 0<v<K, so all displayed real denominators are positive. Reversing the orientation replaces τ by N-τ and lets us impose the stated range; it changes both signed pedal areas' signs. Odd N≥3 is required for the final focus/half-period identification. Coprimality and least period are used in the singular-orbit count.

These parameters have the expected geometry: with S=sn(v), C=cn(v), D=dn(v),

\[
a^2-b^2=\alpha^2\frac{D^2-k'^2}{C^2}=\alpha^2k^2=c^2,
\qquad D^2-C^2=k'^2S^2>0.
\]

Thus a>α and b>β. Stachel's theorem supplies the billiard step δ for all the stated coprime turning numbers, not only τ=1.

The outer polygon consists of the ordered intersections of tangents at consecutive P(w+jδ). Let B₊,B₋ be the signed cross-product areas of the ordered focal feet on its successive side lines. The success criterion is a proof that B₊(w)B₋(w) is independent of real w for every such odd primitive family. A formula for the constant is not required by the target. Hyperbolic and collapsed caustics are not included.

## 1. Exact focal foot and the real construction

For the tangent normal n=(-s/a,t/b), s=sn(w), t=cn(w), the Euclidean projection formula is

\[
f_++\frac{1-n\cdot f_+}{n\cdot n}n.
\]

Using s²+t²=1 and a²-b²=c², its cancelled expression is

\[
Q(w)=\left(\frac{a(c-as)}{a-cs},\frac{ab t}{a-cs}\right),
\qquad Q_x^2+Q_y^2=a^2. \tag{A}
\]

I checked both coordinates and the circle identity by independent polynomial reduction, and derived the focus identity

\[
Q_-(w)=-Q(w+2K).
\]

For real w, a-cs≥a-c>0, so every foot is finite. The real parametrization is injective modulo 4K and P(w+2K)=-P(w). Because 0<δ<2K, consecutive vertices are neither equal nor antipodal. Tangents to a nondegenerate ellipse are parallel only at equal or antipodal points, so every consecutive tangent intersection is finite. Three distinct tangents to a nondegenerate conic cannot meet at a point: from a point there are at most two distinct tangents. Hence neighboring outer vertices are distinct, and their connecting side is exactly the tangent at the shared original vertex. This validates the side-line correspondence even when the ordered polygon is a star.

Define

\[
T(w)=\frac12\sum_{j=0}^{N-1}\det(Q(w+j\delta),Q(w+(j+1)\delta)). \tag{B}
\]

A cyclic index change identifies B₊(w)=T(w) and B₋(w)=T(w+2K). The identity (A) is a bilinear polynomial identity in the complex continuation; replacing it by a Hermitian norm identity would be wrong. The areas have length-squared units and the product length-fourth units. The controls normalize accordingly.

## 2. Exact Jacobi lattices and complete pole catalogue

Write p=iK' and r=K+p. The required transformations are

\[
\operatorname{sn}(w+2p)=\operatorname{sn}w,\quad
\operatorname{cn}(w+2p)=-\operatorname{cn}w,\quad
\operatorname{dn}(w+2p)=-\operatorname{dn}w.
\]

Thus sn lives on the rectangular small torus (4K,2p). Q, whose second coordinate contains cn, must instead be regarded on (4K,4p). The primitive cn lattice can equivalently be generated by 4K and 2K+2p; it does not make 2p a period. This distinction is essential and is correctly respected by the submission.

All three principal Jacobi functions have their simple poles at 2mK+(2n+1)p. On the large rectangular torus the four representatives are p,2K+p,3p,2K+3p. At any such common sn/cn pole, divide the numerator and denominator of each coordinate of (A) by sn. The normalized denominator tends to -c≠0. The result extends holomorphically. More explicitly, the limiting values are

\[
Q\to(a^2/c,iab/c)\quad\text{at }p,2K+p,
\]

and (a²/c,-iab/c) at 3p,2K+3p. Therefore these common Jacobi poles contribute no poles to Q or T. This is a genuine removal, not an omission from the catalogue.

At every remaining point sn and cn are finite, so Q's only possible poles are the roots of a-c sn(w). The exact quarter identities are

\[
\operatorname{sn}(r+z)=\frac{\operatorname{dn}z}{k\operatorname{cn}z},\quad
\operatorname{cn}(r+z)=-\frac{ik'}{k\operatorname{cn}z},\quad
\operatorname{dn}(r+z)=\frac{ik'\operatorname{sn}z}{\operatorname{cn}z}. \tag{C}
\]

They give roots z₋=r-v and z₊=r+v. They are distinct on (4K,2p) because 0<2v<2K. They are simple: cn(r±v)=-ik'/(kC)≠0 and dn(r±v)=±ik'S/C≠0. The derivative of the denominator is -c cn(w)dn(w).

There cannot be additional roots. The small sn torus has precisely two simple poles, so sn-a/c has total pole degree two and therefore total zero degree two. The two exhibited simple roots exhaust it. On the large rectangular torus, the roots are z₋,z₊ and z₋+2p,z₊+2p. The numerator vectors at all four are nonzero, so these are exactly Q's four simple poles. The target value a/c is not a branch value: D/C>1, hence a/c>1/k, consistently with the nonzero derivatives.

No hidden singularity occurs at zeros of cn, dn, or at a+c sn=0. The cancelled formula (A) is globally the meromorphic continuation of the real foot map; at any finite Jacobi value outside a-c sn=0 it is regular. In particular the cancelled a+c sn factor is not to be restored as a new pole.

## 3. Explicit residues and adjacent collisions

At z₋,z₊ the values are sn=a/c, cn=-ib/c. Both numerator vectors in (A) are

\[
U=-\frac{ab^2}{c}(1,i).
\]

The denominator derivatives are respectively

\[
h'(z_-) = \frac{\alpha k'^2S}{C^2},\qquad
h'(z_+) =-\frac{\alpha k'^2S}{C^2}.
\]

Consequently the residues have the particularly simple explicit form

\[
R_-=-\frac{a}{kS}(1,i),\qquad R_+=\frac{a}{kS}(1,i)=-R_-. \tag{D}
\]

These are nonzero, opposite, collinear isotropic vectors. Their 2p translates are obtained by J=diag(1,-1), so the other imaginary copy has the reflected isotropic direction. This explicitly validates both numerator and derivative signs; collinearity alone would suffice for the order bound.

Now fix a possible pole phase w=z₋-jδ. The jth endpoint is at z₋ and the (j+1)st at z₊. For another vertex to hit z₋, (l-j)τ must be divisible by N, forcing l=j modulo N. To hit z₊, (l-j-1)τ must be divisible by N, forcing l=j+1 modulo N. These implications use gcd(τ,N)=1. The imaginary copy cannot mix with this one because all steps are real while 2p is not a large-torus period. Thus precisely two adjacent vertices are singular at each phase, including when the pair crosses the cyclic cut. This applies without change to N=3 and every coprime star.

For their shared edge, the coefficient of ε⁻² is det(R₋,R₊)=0. Every other incident edge has just one singular endpoint and has order at most one. With N=3 the remaining regular vertex belongs to two distinct incident edges; each has order at most one. The submitted proof therefore correctly bounds the entire cyclic area by a simple pole.

In fact the shared edge is better behaved than the bound requires. Put U_j=Q_{jx}+iQ_{jy}, V_j=Q_{jx}-iQ_{jy}; then U_jV_j=a². Near the collision V₁ has residue 2R₋x and V₂ its negative, so V₁/V₂ and V₂/V₁ are analytic and both approach -1. Hence

\[
\det(Q_1,Q_2)=\frac{a^2}{2i}\left(\frac{V_1}{V_2}-\frac{V_2}{V_1}\right)
\]

is holomorphic and vanishes at ε=0. This is an independent strengthening, not a required repair. The submitted weaker order bound is fully adequate. It also explains why a numerical calculation of that edge has severe cancellation and must use adequate precision.

## 4. Reduced lattice and pole divisor

Reindexing (B) gives period δ, because Nδ=4Kτ is a true period of Q. Q also has period 4K. Choose integers A,B with Aτ+BN=1. Then Aδ+B(4K)=4K/N=:L is a period of T. Bezout is valid for every coprime turning number, including stars.

Modulo L the phases z₋-jδ all agree with z₋; z₊ agrees too because z₊-z₋=δ=τL. On

\[
X=\mathbb C/(L\mathbb Z+4p\mathbb Z)
\]

T therefore has only two possible poles, b₀+p and b₀+3p, with b₀=K-v, each of order at most one. Descending through a period sublattice is an unramified quotient; the local order does not become multiplied by N. No minimality assertion about L is needed. The two points remain distinct because 2p is not an element of this lattice.

The finite exact enumeration tests the entire collision assertion, not merely distinct orbit length. For every primitive (N,τ) with 3≤N≤151 and 0<τ<N/2 it enumerates every possible pole phase, identifies the two singular indices and their root labels, checks adjacency across the index cut, checks the pole-orbit collapse, verifies a Bezout certificate, and verifies the odd/even focus congruence. There are 3,503 primitive pairs and 354,690 checked phases. The imaginary-copy separation is supplied by the proof, and each real phase represents two such copies. The finite enumeration supports, but does not replace, the modular proof above.

## 5. Characters, zero function, divisor count, and constant product

The Jacobi transformations give Q(w+2p)=JQ(w). Taking determinants gives T(w+2p)=-T(w). They also give Q(2K-w)=JQ(w). Reflection of the phase reverses the cyclic edges; the reversal and det(J)=-1 cancel. Thus T(2K-w)=T(w). Combining this reflection with the period 2v gives T(2b₀-w)=T(w).

Set F(z)=T(b₀+z). It is even, has periods L and 4p, has anti-period 2p, and has at most simple poles at p and 3p. There are two branches:

1. If there are no poles, compactness makes F constant and the anti-period makes that constant zero. The desired product is zero everywhere. No division by F is permitted or needed.
2. If any pole is present, the anti-period supplies its partner with the same order, so both are simple. F is nonconstant and has total pole multiplicity two.

In the second branch take z₀=p+L/2. Evenness followed by period L gives F(z₀)=F(-p+L/2); the 2p anti-period then gives F(z₀)=-F(z₀). This is a regular point: its real half-period separation from each possible pole is not a real period. Thus F(z₀)=0. The 2p translate 3p+L/2 is a second distinct zero.

The argument principle applied to F'/F on a translated fundamental parallelogram gives equal total zero and pole multiplicities: opposite-edge integrals cancel. One can choose the parallelogram boundary to avoid the finitely many zeros/poles. Therefore these two regular zeros exhaust the zero divisor and are simple. No unsupported assumption about their simplicity has been made.

Each possible pole of F(z)F(z+L/2) is canceled by a zero of the other factor, with the same multiplicity. The product is holomorphic on X and hence constant. This includes the identically-zero branch separately, so it does not assume a nonzero area, residue of T, or proportionality constant. The proof does not require T's possible poles actually to survive the cyclic sum.

Finally, if N is odd, 2K=(N/2)L≡L/2 modulo L. Hence

\[
B_+(w)B_-(w)=T(w)T(w+2K)=T(w)T(w+L/2)
\]

is constant. If N is even, 2K is instead a full reduced period, yielding focus-area equality. It provides no constant-product conclusion, consistently with the deliberately varying even controls.

## 6. Fresh exact and 140-digit controls

`check_meromorphic.py` is standalone and uses the prescribed scientific runtime, Sympy 1.14.0 and mpmath 1.3.0. Final run: 2026-10-15T12:03:54.862491Z to 12:04:20.198396Z, with 140 decimal digits. No inherited checker was read, copied, imported, or invoked. All assertions pass.

The exact symbolic controls verify both foot coordinates, the bilinear auxiliary-circle equation, the opposite-focus identity, both pole numerator coordinates, the explicit residue (D), isotropy, and the shared-edge double-pole cancellation. A deliberately reflected wrong second residue has nonzero determinant 2i a²/(k²S²), showing that the cancellation check distinguishes an actual dangerous double pole.

| k | N | τ | Purpose |
| --- | ---: | ---: | --- |
| 10⁻⁸ | 3 | 1 | N=3; small modulus / circular approach |
| 0.2 | 5 | 2 | primitive star |
| 0.67 | 9 | 4 | near-maximal star |
| 0.93 | 15 | 2 | composite odd period, coprime star |
| 1-10⁻¹² | 5 | 1 | near-degenerate complementary modulus |
| 0.67 | 31 | 1 | small step |
| 0.67 | 31 | 15 | near-antipodal step |
| 0.67 | 101 | 1 | v/K=2/101, deliberate small-v family |
| 0.67 | 101 | 50 | v/K=100/101, deliberate v→K family |
| 0.67 | 8 | 1 | even parity control |
| 0.93 | 8 | 3 | even star control |

For every family the controls independently construct consecutive outer tangent intersections, project both foci onto the lines through consecutive outer vertices, and compute signed cross-product areas. They compare these geometric areas with T and T(w+2K), and compare products at three real phases. In the nine odd cases the largest normalized product spread is 1.260×10⁻¹³⁹. The even product spreads are about 5.5515×10⁻⁵ and 4.6305×10⁻³, decisively distinguishing the parity claim.

Complex controls check all three quarter-shift identities, the real dn shift sign, Q's imaginary reflection, T's anti-period and reduced real period, F's evenness, both forced zeros, the half-period product at three complex phases, and the focus congruence. The largest error among the nonsingular character/geometry controls is 2.439×10⁻¹²⁵. All four common Jacobi pole representatives are approached along a complex direction and converge to the derived regular limits; the largest error at |ε|=10⁻³² is 5.572×10⁻³¹.

At both adjacent focal poles the controls test the explicit opposite Q residues along ε=10⁻ᵈ(0.6+0.8i), d=12,24,36. They compare εT to the independently predicted residue

\[
\tfrac12\{\det(Q(r-3v),R_-)+\det(-R_-,Q(r+3v))\}.
\]

The last error is at most 4.577×10⁻⁷¹. They track ε²T tending to zero, and the shared-edge determinant tending to zero, while a deliberately reflected wrong endpoint has the predicted nonzero ε⁻² coefficient. Thus these controls exercise simultaneous singularities rather than avoiding them. Assuming cn has period 2p gives a relative residual 2, and assuming dn changes sign under 2K likewise gives residual 2. These negative controls fail decisively.

These are arbitrary-precision floating-point checks, not interval bounds. The finite limiting samples do not claim to prove behavior at k=0, k=1, v=0, or v=K. Those points are excluded by the theorem; the universal proof explicitly uses their strict inequalities.

Reproduction from any working directory, with an isolated output path if desired:

```text
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python -B /Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr210_5100033/initial_review_20261015/meromorphic_divisor_adversary_01/check_meromorphic.py --output /ABSOLUTE/ISOLATED/PATH/results.json
```

The script reads the immutable sources and existing private PDF paths relative to its own saved location. It writes only the supplied result path, or its own `results.json` by default. It creates no environment, cache, provider state, or Git state.

## Findings, optional clarifications, and exact remaining gap

**No required mathematical repair.** Every premise needed by the meromorphic argument is supplied by a checked classical input or derived above. No central difficulty has been shifted to an unsupported equivalent invariant.

Optional clarifications useful to readers:

- State explicitly that sn's smaller torus is used solely for degree counting, while Q and T use the larger rectangular torus before real-period reduction. The submission already does this correctly.
- The explicit residues (D) make the signs easy to check. The submitted collinearity/opposite-derivative calculation is already sufficient.
- The shared singular edge is actually regular and zero there. The submitted at-most-simple statement remains correct.
- Distinguish the paper's printed target/parity/outer construction from the proof's explicit primitive/star conventions. Source text inspected here does not itself spell out all primitive/repetition/star conventions. The universal star coverage is a deduction from the canonical theorem and proof, not a quotation of an explicit source restriction. If odd repeated traversal words are desired as an additional scope, an m-fold repetition multiplies each signed area by m and the product by m²; that extension is elementary and not needed for the stated least-period theorem.
- Stachel printed p.1613 contains a sign typo in the displayed dn(u+2kK) formula. A fresh rendering confirms it is present in the PDF, not an extraction artifact. Correctly, dn(u+2K)=dn(u), as DLMF records. The submitted proof never imports the erroneous sign and uses the correct shifts; its canonical input Theorem 4.3/(4.9) remains usable.

The strongest verified result is the submitted universal odd primitive/star signed outer focal-pedal area-product constancy theorem, with a complete pole and character/divisor proof. The exact remaining gap for this assigned mathematical audit is **none identified**. Novelty, historical priority, broad literature status, and final publication decisions are outside this shard's conclusion. No outreach, Git writes, provider writes, or other-shard communication occurred.
