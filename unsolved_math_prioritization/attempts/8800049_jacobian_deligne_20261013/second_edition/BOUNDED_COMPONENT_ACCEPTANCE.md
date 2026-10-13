# Independent acceptance of the bounded good-point theorem

## Verdict and scope

**Accepted without a required mathematical correction.** The theorem in *A uniform odd-extension bound for the Beauville–Ritzenthaler construction*, together with its source and validation record, proves the stated bound

\[
\#\Sigma_A(\mathbb F_Q)\le
2Q^2+18Q^{3/2}+2321Q+24\sqrt Q+2270
\]

for a geometrically indecomposable principally polarized abelian threefold with a smooth rational theta divisor. It proves that, for \(Q\ge81\), more than one sixth of its rational points are good. The prescribed least positive odd extension degree is at most seven. The proof includes characteristics two and three and does not need ordinarity.

This acceptance concerns that quantitative geometric replacement. It does not independently re-audit every dependency of the earlier aggregate counted-model recognition algorithm, establish an efficient implementation, or certify a nontrivial end-to-end geometric execution. No optimality or worldwide novelty conclusion follows.

## 1. Descent and the two exceptional components

The hypotheses match Beauville–Ritzenthaler (BR): finite fields are perfect; geometric indecomposability gives the geometric genus-three Jacobian; smooth theta puts the curve in the nonhyperelliptic branch. Proposition 3.1 gives a curve over the counting field and the quadratic twist through negation. Proposition 2.1 and §3.3 identify the exceptional support and the good-intersection condition. The characteristic-two caution attached to BR Lemma 2.7 is not an obstruction: this argument uses the alternative definition in §3.3, valid in all characteristics. [BR](https://arxiv.org/abs/1005.3683v1)

There is no hidden choice of a rational theta characteristic. The map
\(E\mapsto2E-K_C\) is intrinsically defined on \(\operatorname{Sym}^2 C\), while residual canonical intersection gives the regular involution \(E\mapsto\langle K_C-E\rangle\). Its regularity can also be seen by restricting the automorphism \(L\mapsto K_C\otimes L^{-1}\) of \(\operatorname{Pic}^2(C)\) to the smooth Abel image. Their equivariance identities descend the map after twisting both sides by the same constant group of order two.

The resulting source is smooth, projective, and geometrically connected. Finiteness is checked after algebraic closure, where the map is a restriction of multiplication by two, followed by a translation. This argument does not require multiplication by two to be étale. Likewise, exchanging the factors of \(C\times C\) is the source action that makes the difference map equivariant for negation. The constant Galois group remains étale in characteristic two; it is not \(\mu_2\).

## 2. Symmetric-square cohomology and its twist

The finite quotient \(C\times C\to\operatorname{Sym}^2 C\) has orbit fibers on geometric points. Constant-sheaf invariants are consequently the constant sheaf on the quotient. Finite pushforward has no higher direct images, and taking invariants is exact with rational \(\ell\)-adic coefficients. These statements remain valid for a wild quotient. One may, in particular, choose an odd prime \(\ell\ne\operatorname{char}K\), so the averaging projector already exists at every finite coefficient level. The relevant standard inputs were checked in Milne's finite-pushforward, proper-base-change and Künneth statements. [Milne, *Lectures on Étale Cohomology*](https://www.jmilne.org/math/CourseNotes/LEC.pdf)

An independent graded-swap calculation gives the following dimensions in degrees zero through four:

- Product cohomology: \((1,12,38,12,1)\).
- Trace of factor exchange: \((1,0,-6,0,1)\).
- Invariant cohomology: \((1,6,16,6,1)\).

The minus sign on the diagonal of \(H^1\otimes H^1\) is essential. It gives the exterior square, of dimension fifteen, and the outer degree-two terms supply the remaining invariant dimension. Twisting preserves these dimensions but need not preserve Frobenius. Applying the trace formula and pure weights to the actual descended smooth projective surface gives exactly

\[
\#S(K)\le Q^2+6Q^{3/2}+16Q+6\sqrt Q+1.
\]

## 3. Collision locus and rational image points

The proof correctly avoids the generally false inequality that a rational image has no more rational points than its source. If two geometric source points map to the same image, their difference is a nonzero geometric two-torsion point. The bound of 63 counts geometric points only. It follows from scheme length 64 in every characteristic and is conservative in characteristic two.

For each such \(t\), the theta divisors \(D\) and \(D+t\) are different: otherwise \(t\) lies in the kernel of the principal polarization. Their intersection is a codimension-two complete intersection in a smooth threefold, hence Cohen–Macaulay and pure of dimension one. Nonreduced structure contributes positive multiplicities to the intersection cycle; it cannot create an uncounted isolated support component.

In the rational \(|3\Theta|\) embedding, the projection formula yields

\[
\deg([2]_*[D\cap(D+t)])=(12\theta)\theta^2=72.
\]

Translations preserve the numerical polarization class, and a polarized geometric isomorphism preserves that class as well. Thus the calculation is in the correct embedding even if the intermediate theta translate is not defined over the counting field. The standard inputs are \(\theta^3=6\), numerical pullback \([2]^*\theta=4\theta\), and very ampleness of \(3\Theta\). [Milne, *Abelian Varieties*](https://www.jmilne.org/math/CourseNotes/AV110.pdf)

The factor of two in the pushforward-cycle inequality is justified componentwise on the target. Translation by \(t\) acts without fixed geometric points and preserves each fiber of multiplication by two. Every geometric generic fiber over an image component therefore contains at least two points. If translation interchanges source components, their generic degrees are added; if it preserves one, that component alone has at least two geometric generic points. Positive source multiplicities and inseparable degrees only increase the resulting coefficient. Hence each reduced image has degree at most 36 and the reduced union has total degree at most \(63\cdot36=2268\).

Outside this union, a rational image point has a unique geometric preimage. Frobenius must fix it. A unique geometric point in a finite fiber over a perfect field has residue field equal to the base field; nilpotents do not change this conclusion. Thus

\[
\#\Sigma'_A(K)\le \#S(K)+2268(Q+1).
\]

## 4. Independent check of the geometric curve point bound

Theorem 2.1 of Lachaud–Rolland explicitly allows algebraic sets over the algebraic closure and counts their intersection with the finite-field projective points. Because the collision union is pure of dimension one, its cumulative degree is its usual degree. Its use here is valid. [Lachaud–Rolland](https://arxiv.org/abs/1405.3027)

For completeness, the particular curve bound also has a short independent proof. Consider one irreducible geometric projective curve of degree \(d\). If it lies in a geometric hyperplane, eliminate a coordinate whose coefficient in that hyperplane is nonzero. The coordinate projection restricts to a linear isomorphism of that hyperplane with a lower-dimensional projective space; it preserves the curve's degree and injects its finite-field points into finite-field points. Iterate until the image spans \(\mathbb P^r\).

If \(r=1\), the bound is immediate. Otherwise every rational hyperplane meets the curve in at most \(d\) geometric points. Counting incidences between its \(M\) rational points and rational hyperplanes gives

\[
M\pi_{r-1}\le d\pi_r,
\qquad
\pi_r/\pi_{r-1}=Q+1/\pi_{r-1}\le Q+1.
\]

Thus \(M\le d(Q+1)\). Summing over the geometric irreducible components proves the bound used in the manuscript. No descent of the individual components is needed.

## 5. Exact difference-component counts

The nonhyperelliptic condition excludes a degree-two pencil. Consequently equality \(p-r=p'-r'\ne0\) implies equality of the effective divisors \(p+r'\) and \(p'+r\), and hence equality of the ordered pairs. All diagonal pairs map to the single rational point zero.

For the untwisted target, the unique off-diagonal pair is rational precisely when both entries are rational, giving \(N_1(N_1-1)+1\). For the nontrivial twist, Frobenius interchanges the entries; the pairs are exactly \((p,\operatorname{Frob}_Q p)\) with \(p\in C(\mathbb F_{Q^2})\setminus C(K)\), giving \(N_2-N_1+1\). This also handles curves with no rational points, because zero is counted separately. There is no rational-preimage assumption at the contracted diagonal.

The stated uniform upper bound

\[
Q^2+12Q^{3/2}+37Q+18\sqrt Q+1
\]

follows by using the upper genus-three Weil bound in the positive square and the lower bound in the subtracted term. The potentially negative lower bound at small \(Q\) is harmless. The nontrivial-twist estimate is smaller coefficientwise.

## 6. Constants, density, and all starting fields

An independent integer-polynomial computation assembled the surface, collision, and difference terms before comparing with the displayed \(B(Q)\). It reproduced all its coefficients. With \(s=\sqrt Q-9\), the coefficients in ascending powers of \(s\) were independently found to be

\[
L-B:\quad(45413,144600,57661,10150,958,48,1),
\]
\[
5L-6B:\quad(10334,670992,284526,50660,4788,240,5),
\]

where \(L=(\sqrt Q-1)^6\). Every coefficient is positive. At \(Q=81\), the independently checked values are \(L=262144\) and \(B=216731\). The ordinary abelian-variety Weil lower bound therefore proves the strict density conclusion throughout \(Q\ge81\), not just at tested integer squares.

For \(q=2\), the least sufficient odd degree is seven; for \(q=3,4\), it is five. For \(5\le q<81\), degree one fails while degree three succeeds because \(5^3>81\). For \(q\ge81\), degree one suffices. These arguments cover all prime powers, with no omitted small-field branch. An independent exhaustive integer check of \(2\le q<81\) additionally verified every nontrivial case. Oddness preserves the value of the order-two character on Frobenius, including in characteristic two.

## Inspection and validation limits

The full retained seven-page BR text was read. The point-bound definitions, theorem, and relevant surrounding argument in Lachaud–Rolland, the cited cohomological statements in Milne, and the relevant standard abelian-variety formulas were inspected. This is a source-hypothesis audit and a proof review; it is not a new proof of all the cited source theorems.

The finite computations independently check graded linear algebra and exact arithmetic identities. They do not simulate theta geometry and are not substituted for the mathematical arguments above. The original validation record accurately states those limits. No mathematical repair is required before using this theorem as the stated bounded-search replacement.
