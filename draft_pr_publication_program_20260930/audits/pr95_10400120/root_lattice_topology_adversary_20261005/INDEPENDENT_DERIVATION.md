# Independent root-lattice derivation

Recorded 2026-10-05 20:33 UTC, before opening the incoming author proof, code, prior review, or old independent checker. The submitted target values were known as hypotheses, but no submitted calculation was used.

## Established source and full specialization

The mathematical input is S. K. Hansen and T. Takata, *Reshetikhin–Turaev invariants of Seifert 3-manifolds for classical simple Lie algebras, and their asymptotic expansions*, [arXiv:math/0209403v2](https://arxiv.org/pdf/math/0209403v2), Theorem 5.1 on printed p.39. The source was independently downloaded and its p.39 was rendered and visually checked. Sections 2, 4, and 5 supply the relevant conventions: long roots have square length 2; Y∨ is the coroot lattice, dual to weight lattice X; r=mκ with κ≥h∨; the simply laced case has m=1; indices are shifted by ρ. The rank D is defined in (26), the phase ω in (28), and the invariant has τ(S³)=D⁻¹. Lens space L(p,q) is unknot surgery with coefficient −p/q, with gcd(p,q)=1. The theorem requires p≠0 and does **not** require gcd(p,r)=1. Proposition 5.2's coprime simplification is unavailable here and is not used.

For g=sl₅(C), the corresponding simply connected compact group is SU(5). Take

\[
H=\{x\in\mathbb R^5:\sum_i x_i=0\},\quad
Y=Y^\vee=H\cap\mathbb Z^5,\quad
\alpha_i=e_i-e_{i+1}\quad(1\le i\le4).
\]

The Weyl group is S₅ acting by coordinate permutations, det(w) is permutation parity, ℓ=4, |Δ₊|=10, h∨=5, dim(g)=24, and ρ=(2,1,0,−1,−2), so |ρ|²=10. Thus WZW level k=5 means shifted κ=k+h∨=10, and HT's r=10. All theorem hypotheses hold. The Cartan Gram matrix has diagonal 2, adjacent −1, other entries 0; the determinant recurrence dₙ=2dₙ₋₁−dₙ₋₂, d₀=1,d₁=2 gives d₄=5. Hence vol(Y)=√5 and vol(X)=1/√5. Formula (26) therefore specializes to D=100√5/P with

\[
P=\prod_{1\le i<j\le5}2\sin\frac{\pi(j-i)}{10}>0.
\]

For p>0 write \(\mathcal S(q/p)=12s(q,p)\), with
\(s(q,p)=\sum_{n=1}^{p-1}((n/p))((qn/p))\), and \(((x))=x-\lfloor x\rfloor-1/2\) off integers and 0 on integers. Theorem 5.1 gives

\[
\tau(L(p,q))=
\frac{i^{10}}{(10p)^2\sqrt5}
e^{\pi i\mathcal S(q/p)}
\sum_{w\in S_5}\det(w)e^{-2\pi i\langle\rho,w\rho\rangle/(10p)}
\sum_{\nu\in Y/pY}
e^{\pi i(10q/p)|\nu|^2}
e^{(2\pi i/p)\langle\nu,q\rho-w\rho\rangle}.
\tag{1}
\]

Here i¹⁰=−1. This phase, the Dedekind factor, and √5 are retained, rather than silently discarded. The underlying modular category and its mirror can reverse phases, but leave the magnitude being tested unchanged.

## Lattice sum collapses by character orthogonality

Set p=5. A complete representative set of Y/5Y is

\[
\nu(a)=(a_1,a_2-a_1,a_3-a_2,a_4-a_3,-a_4),\quad 0\le a_i<5,
\]

since the simple roots are a free Z-basis. There are exactly 5⁴=625 classes. The quadratic factor in (1) is exp(2πiq|ν|²)=1 because |ν|² is an integer (indeed even). For any integral sum-zero v,

\[
\sum_{\nu\in Y/5Y}e^{2\pi i\langle\nu,v\rangle/5}
=\prod_{j=1}^4\sum_{a=0}^4e^{2\pi i a(v_j-v_{j+1})/5}
=\begin{cases}625,&v_1\equiv\cdots\equiv v_5\pmod5,\\0,&\text{otherwise.}\end{cases}
\tag{2}
\]

Equivalently v∈5X, **not** necessarily v∈5Y. Ignoring this distinction would incorrectly remove four surviving permutations. Since ρ's five coordinates exhaust F₅, for each common residue c there is exactly one permutation with wρ≡qρ−c(1,1,1,1,1) mod5. Consequently precisely five permutations survive for each nonzero q mod5.

Let z=e^{2πi/50}, t=z⁵=e^{πi/5}, and define

\[
B_q=\sum_{w:\,q\rho-w\rho\in5X}\det(w)z^{-\langle\rho,w\rho\rangle}.
\]

The following table is checkable by direct coordinate dot products and inversion counts. It lists wρ, sign, and dot product; the independent code enumerates all 120 permutations and all 625 representatives as a redundant check of (2).

| q | surviving wρ | sign | ⟨ρ,wρ⟩ |
|---|---|---:|---:|
|1|(2,1,0,−1,−2)|+1|10|
|1|(1,0,−1,−2,2)|+1|0|
|1|(0,−1,−2,2,1)|+1|−5|
|1|(−1,−2,2,1,0)|+1|−5|
|1|(−2,2,1,0,−1)|+1|0|
|2|(2,0,−2,1,−1)|−1|5|
|2|(1,−1,2,0,−2)|−1|5|
|2|(0,−2,1,−1,2)|−1|−5|
|2|(−1,2,0,−2,1)|−1|0|
|2|(−2,1,−1,2,0)|−1|−5|

Thus the full double sum in (1) is 625 Bq and

\[
B_1=t^{-2}+2+2t,\qquad B_2=-(1+2t^{-1}+2t).
\tag{3}
\]

## S³ normalization and real embedding

At p=1 the lattice quotient has one point and the Dedekind symbol is 0, so define

\[
A=\sum_{w\in S_5}\det(w)e^{-2\pi i\langle\rho,w\rho\rangle/10}.
\]

The Weyl denominator identity gives A=(−2i)¹⁰∏sin(π(j−i)/10)=−P. Put r=√5 with its **positive real embedding**. The standard exact trigonometric values yield

\[
P=(2\sin18^\circ)^4(2\sin36^\circ)^3(2\sin54^\circ)^2(2\sin72^\circ)=5r-10,
\]

because (2sin18°)(2sin54°)=1, (2sin36°)(2sin72°)=r, and (2sin36°)²=(5−r)/2. Therefore

\[
A=10-5r,\quad |A|^2=225-100r>0,\qquad
\tau(S^3)=\frac{-A}{100\sqrt5}=D^{-1}>0.
\tag{4}
\]

Since |t|=1 and t+t⁻¹=(1+r)/2, equation (3) gives

\[
|B_1|^2=11+2r,\qquad |B_2|^2=9+4r.
\tag{5}
\]

For example B₁B̄₁ expands to 9+4(t+t⁻¹)+2(t²+t⁻²)+2(t³+t⁻³). Substitute t²+t⁻²=(r−1)/2 and t³+t⁻³=−(t²+t⁻²) to obtain 11+2r. Also B₂=−(2+r), immediately giving its square.

Writing \(\widehat\tau(M)=\tau(M)/\tau(S^3)\), cancellation of the covolume and level prefactors gives

\[
\widehat\tau(L(5,q))=25e^{\pi i\mathcal S(q/5)}B_q/A,
\qquad |\widehat\tau(L(5,q))|^2=625|B_q|^2/|A|^2.
\]

As (225−100r)(225+100r)=625, exact substitution yields

\[
\boxed{|\widehat\tau(L(5,1))|^2=3475+1550\sqrt5},\qquad
\boxed{|\widehat\tau(L(5,2))|^2=4025+1800\sqrt5}.
\tag{6}
\]

They are positive, hence both invariants are nonzero, and their difference is 550+250√5>0. A single normalization by a fixed nonzero constant cannot alter equality of magnitudes.

The code proves the needed integer-polynomial identities in Z[z]/Φ₅₀, where Φ₅₀=z²⁰−z¹⁵+z¹⁰−z⁵+1. It sets √5=1+2(z¹⁰+z⁻¹⁰); this squares to 5 exactly, and the positive embedding follows analytically from cos72°>0. Numerical values are merely diagnostic and play no role in (6).

## Orientation, inversion, and boundary controls

HT uses −p/q surgery. A convention using +p/q changes orientation. Replacing q by −q conjugates (1): send w to w₀w, with w₀ρ=−ρ and det(w₀)=(−1)¹⁰=+1, and use s(−q,p)=−s(q,p). Thus B₋q=B̄q exactly, and the full Dedekind factor conjugates as well. For p=5, \(\mathcal S(1/5)=12/5\), \(\mathcal S(2/5)=\mathcal S(3/5)=0\), \(\mathcal S(4/5)=−12/5\). Inversion q→q⁻¹ exchanges 2 and 3, and their independently enumerated B sums are equal. The q=1 and 4 norm sums are equal. Periodicity q→q+5 was checked at 6 and 7. These controls prevent surgery sign or inverse-q conventions from removing the magnitude discrepancy.

For p=1, equation (1) has numerator A, quotient size 1, Dedekind factor 1, giving normalized value 1. The theorem explicitly includes q=0,p=±1 as S³ and treats p=0,q=±1 separately as S¹×S²; division by p is never applied there. Values with gcd(p,q)>1 are outside its lens-space hypotheses. Levels κ<h∨ and the unavailable gcd(p,r)=1 simplification are likewise excluded.

## Topology and target scope

Dehn filling the unknot exterior produces a connected compact manifold with its single torus boundary filled, hence a connected closed 3-manifold. It inherits an orientation from the surgery gluing. The unknot exterior is a solid torus with fundamental group generated by the unknot meridian μ; the preferred longitude λ is nullhomotopic there. Filling coefficient −p/q kills the slope μ⁻ᵖλᵠ, so van Kampen gives π₁=⟨μ|μᵖ=1⟩≅Z/|p|. Hence both spaces in (6) have π₁≅Z/5.

Independently downloaded [Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds* (2002)](https://msp.org/gtm/2002/04/gtm-2002-04-024p.pdf), Chapter 7 p.471, defines the quantum G invariants on closed oriented 3-manifolds with shifted r=k+h∨. Its Conjecture 7.5 on p.474 attributes the claim to [158], Guadagnini–Pilo (1998), and asserts that the magnitude of a nonzero quantum G invariant is determined by π₁. There is no SU(2)-only restriction in the conjecture as printed. SU(5), r=10, and the two nonzero lens-space invariants satisfy the printed hypotheses. Equations (6) therefore disprove that printed claim.

## Independent judgment before author comparison

The target magnitude identities and refutation of the printed Conjecture 7.5 pass this independent root-lattice derivation. No mathematical gap remains for these narrow statements, conditional only on the cited established RT theorem/category identification. The independent proof above avoids modular-matrix construction, integrable-weight sums, and submitted code entirely. The still-open audit tasks are author comparison, artifact closure, and reporting. Audit completion estimate: 75%.

Novelty and historical priority are **not** established. An obvious source hazard is HT Remark 5.3(a), printed p.44, discussing separation of L(64,9),L(64,25) by an sl₄ invariant. Separation of complex invariants alone does not prove separation of magnitudes, so that remark cannot be promoted to an earlier counterexample without checking it. It should be included in a later authorized priority audit. The original conjecture citation [158] should likewise be examined in that audit. No such global audit was begun here.
