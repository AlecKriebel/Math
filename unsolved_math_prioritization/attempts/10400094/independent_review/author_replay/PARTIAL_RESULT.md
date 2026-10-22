# Fox 7-colorings and the (4,∞) skein module: two restricted diagnostics

**Original target unresolved, two approaches; independent review pending.** Problem 4.16 of Ohtsuki's collection, proposed by J. Przytycki, asks which coefficients make the (4,∞) skein module measure the number of Fox 7-colorings. No answer to that full question is claimed here.

## 1. Exact scope recovered from the primary source

The [original collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed pp.450–453, defines a module of unoriented framed links over a commutative ring R, with a,b₀,b₃ invertible, relations
\[
b_0L_0+b_1L_1+b_2L_2+b_3L_3+b_\infty L_\infty=0,
\qquad L^{(1)}=aL.
\]
The local diagrams in Figure15 are successive two-strand half-twists and the other smoothing. Problem4.16 is on p.452. The p.453 discussion motivates recovering coloring numbers through squared norms of specialized link invariants. Thus “measured” is not restricted to requiring the raw integer count itself to satisfy the displayed linear relation. A reported unpublished observation of Jaeger is historical context, not a proof certificate.

The primary [Przytycki lecture notes](https://indico.ictp.it/event/a08157/session/33/contribution/18/material/0/0.pdf), p.28, likewise discuss squared-norm recovery and a possible Gaussian-sum mechanism. No complete current coefficient classification was verified. A later bibliographic lead is Goldschmidt–Jones, *Metaplectic link invariants* (1989); this package does not assert that its normalization or local relation has been matched to the present source.

Throughout the direct count below, C₇(L) includes the seven constant colorings of every nonempty link. We derive the test counts directly from crossing equations and do not rely on a convention-dependent identification with branched-cover homology.

## 2. Raw-count obstruction over characteristic zero

**Proposition.** There is no nonzero fixed scalar relation
\[
b_0C_7(L_0)+b_1C_7(L_1)+b_2C_7(L_2)+b_3C_7(L_3)+b_\infty C_7(L_\infty)=0
\tag{1}
\]
valid for every such local skein quintuple, with coefficients in any characteristic-zero field. In particular the raw count cannot define a linear evaluation of the source module with its required invertible end coefficients.

**Proof.** Rotate the local picture to vertical two-strand braid convention. Attach an external two-strand braid with −j half-twists and take its usual braid closure, for j=0,1,2,3,4. The four twist fillings give the closures of the two-strand braids with k−j half-twists, k=0,1,2,3. The other smoothing closes to one circle, with possible framing twists, so its Fox count is seven. This last assertion can also be seen by propagating the equal colors imposed by its cap and cup through every external crossing.

At a crossing the color pair transforms by
\[
A=\begin{pmatrix}2&-1\\1&0\end{pmatrix}=I+N,
\qquad N^2=0
\]
over F₇. Reversing the choice of positive half-twist uses A^{-1} instead and does not change any of the following counts. For any integer r, A^r=I+rN. Closure requires A^r x=x. The kernel has dimension two if r≡0 mod7 and dimension one otherwise. Hence the braid closure has 49 colorings in the former case and seven in the latter.

For the five exterior choices, write B=b₀+b₁+b₂+b₃+b∞. Equation(1), divided by seven, becomes
\[
B+6b_j=0\quad(j=0,1,2,3),\qquad B=0\quad(j=4).
\]
It follows that every b_j=0 and then b∞=0. Equivalently the five-by-five normalized test matrix is
\[
\begin{pmatrix}
7&1&1&1&1\\
1&7&1&1&1\\
1&1&7&1&1\\
1&1&1&7&1\\
1&1&1&1&1
\end{pmatrix},
\]
whose determinant is 6⁴. □

The same argument works in any field whose characteristic is neither2,3 nor7. In characteristics2 and3 the raw counts, being powers of seven for nonempty links, all become one, so such reductions discard the count information. No classification over arbitrary rings is claimed. Dividing the nonempty-link count by seven does not remove the characteristic-zero obstruction. The count is framing-independent, so a nonzero characteristic-zero linear evaluation would also force a=1.

**Scope warning.** This is not a negative answer to Problem4.16. An auxiliary complex invariant can obey a linear relation even when its squared magnitude, from which a count is recovered, obeys no such relation.

## 3. A local Gaussian identity, without a global link-invariant claim

Let ζ=exp(2πi/7), and put
\[
s=\zeta+\zeta^2+\zeta^4,\qquad \bar s=\zeta^3+\zeta^5+\zeta^6.
\]
Then s+\bar s=−1, s\bar s=2, and (s−\bar s)²=−7. On the vector space C^{F₇}, define the diagonal operator D and the rank-one projection Π₀ by
\[
D e_x=\zeta^{x^2}e_x,\qquad \Pi_0 e_x=1_{x=0}e_x.
\]
There is the exact identity
\[
D^3-sD^2+\bar sD-I+(s-\bar s)\Pi_0=0.
\tag{2}
\]
Indeed the nonzero squares modulo7 are1,2,4, and
\[
P(t)=\prod_{q\in\{1,2,4\}}(t-\zeta^q)
=t^3-st^2+\bar st-1.
\]
Thus P(D) vanishes off e₀, while P(1)=\bar s−s. This proves (2). Its four distinct eigenvalues1,ζ,ζ²,ζ⁴ show that D has minimal polynomial (t−1)P(t); no nonzero scalar cubic in D alone vanishes. The rank-one correction is essential.

Formula(2) supplies a mathematically explicit local coefficient pattern
\[
(b_0,b_1,b_2,b_3,b_\infty)=(-1,\bar s,-s,1,s-\bar s)
\]
for this **specified operator model only**. We have not identified D with the source's normalized framed crossing or Π₀ with its cap-cup smoothing. In particular cap-cup maps in a tangle functor need not be normalized projections; a scaling would change b∞. Changing crossing normalization also changes the other coefficients and framing factor. Therefore the displayed tuple is not asserted to answer Problem4.16.

Taking any linear functional on these five operators preserves(2), but that alone does not produce a link invariant. Missing are a compatible tangle composition/duality structure, the framed Reidemeister or braid-and-Markov verification, exact smoothing/framing normalization, and an all-link formula recovering C₇ from the resulting evaluation. Merely calculating eigenvalues cannot replace those requirements.

## 4. Verification and disposition

The exact verifier enumerates the two-strand Fox equations over F₇ for a range of positive and negative twists, verifies the five closure tests and their determinant, and checks the cyclotomic identities modulo Φ₇(z)=1+z+⋯+z⁶. No floating-point approximations are used. These are controls on the two proved diagnostics, not on a global quantum or Gaussian link invariant.

The two substantive approaches are (i) testing a direct count-valued linear skein relation and (ii) constructing a local Gaussian operator relation. The first is rigorously ruled out in characteristic zero; the second reaches a local identity but stalls at the global topological and recovery requirements. Original status: **unsolved,2/5**. No coefficient classification, novelty, or human peer review is claimed.

Actual model metadata: inherited runtime; exact model identifier not exposed; no model or reasoning switch made.
