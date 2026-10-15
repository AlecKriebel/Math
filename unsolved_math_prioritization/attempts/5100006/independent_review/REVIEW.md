# Independent adversarial review: 5100006 / k114

**Verdict: PASS_COMPLETE_PRIMITIVE_ELLIPTICAL_CAUSTIC_PROOF. No mandatory mathematical correction.**

The submitted cyclic-norm argument proves the focal-distance product invariant for the source's nondegenerate confocal-ellipse billiard families of least period \(N\equiv2\pmod4\), including primitive star orbits. Both focal products are equal. The proof correctly distinguishes the full real billiard period from the smaller period lattice of its paired elliptic function.

Reviewed snapshot: SHA-256 **f70821b0d44e96f6be9427f906cecc5d1aff8bbd7ab09a71ddec9d75d31ef2d5**.

All **29,397** submitted exact assertions and **210** separately labelled numerical diagnostics reproduced with a byte-identical receipt. A new standard-library checker passes **5,198** exact controls, including negative parity and nonprimitive controls. The universal conclusion follows from the written divisor argument, not from either finite computation.

## 1. Exact source and imported input

The original [Reznik–Garcia–Koiller Table 2](https://arxiv.org/abs/2004.12497v11), printed p.5, visibly lists k114 as the product of distances from the orbit vertices to one focus for \(N\equiv2\pmod4\). The [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 2 on printed p.345, retains the same statement. I inspected both source-table renderings and their surrounding definitions. The introductory geometric setting is a strictly nested confocal pair of ellipses.

The candidate keeps the ordinary Poncelet \(N\)-gon/least-period convention explicit. It does not call an odd-period polygon traversed twice a primitive even polygon. Its claim covers all turning numbers coprime to \(N\), not merely simple polygons. Hyperbolic caustics, focal separatrix limits and degenerate two-bounce trajectories lie outside this source setting and outside the theorem. These limitations must remain explicit in publication.

The decisive imported parametrization is [Stachel, *On the motion of billiards in ellipses*](https://doi.org/10.1007/s40879-021-00524-2), published Theorem 4.3 and equation (4.9), printed p.1614. I checked the full available paper, the theorem's rendered page, and the relevant derivation. It states the parametrization
\[
P(u)=(-a\,\operatorname{sn}u,\ b\,\operatorname{cn}u),
\]
the step \(2v\), the modulus \(k=c/\alpha\), and
\[
a=\alpha\frac{\operatorname{dn}v}{\operatorname{cn}v},
\qquad b=\frac{\beta}{\operatorname{cn}v}.
\]
Here \(\alpha,\beta\) are the caustic semiaxes, so the modulus is its eccentricity. Replacing it by \(c/a\) would be incorrect; the candidate does not do that.

For the chosen orientation \(0<v<K\), the real parametrization has least period \(4K\). Thus a primitive \(N\)-orbit has \(v=2K\tau/N\), with \(\gcd(\tau,N)=1\) and \(0<\tau<N/2\). The source theorem explicitly allows the turning number. This applies equally to primitive stars.

The Jacobi pole and shift data were checked directly in current [DLMF §22.4](https://dlmf.nist.gov/22.4), Tables 22.4.1 and 22.4.3, with simple-pole meromorphicity also checked in [§22.2](https://dlmf.nist.gov/22.2). The adjacent erroneous sign in Stachel's displayed \(dn(u+2K)\) line is not used; the same issue is visible in the published text as well as the preprint. The candidate's actual identities agree with DLMF.

## 2. Antipodal pairing and ordinary distance normalization

Set \(N=2m\). Since \(N\equiv2\pmod4\), \(m\) is odd. Primitivity gives odd \(\tau\) and \(\gcd(\tau,m)=1\). After \(m\) billiard steps,
\[
u\longmapsto u+2mv=u+2K\tau.
\]
Both \(sn\) and \(cn\) change sign under this shift. Hence the vertex list is paired exactly by \(P_{j+m}=-P_j\).

For any real point on \(x^2/a^2+y^2/b^2=1\), direct squaring gives
\[
|(x,y)-(c,0)|=a-cx/a,\qquad
|(x,y)+(c,0)|=a+cx/a.
\]
Both right sides are positive because \(a>c\) and \(|x|\le a\). There is consequently no complex-square-root or signed-distance substitution in passing to
\[
F(u)=a^2-c^2sn^2u,\qquad
R(u)=\prod_{j=0}^{m-1}F(u+2jv).
\]
Each factor represents the product of the distances from one antipodal pair to a **single** focus. The same pairing gives the identical expression for the other focus. It is not necessary to infer one-focus constancy from only the product of the two focal products.

## 3. Divisor reconstruction and multiplicities

On
\[
T=\mathbb C/(2K\mathbb Z+2iK'\mathbb Z),
\]
\(sn^2u\), and therefore \(F\), is single-valued and elliptic. This is the correct lattice for \(F\), although \(sn\) itself has real period \(4K\).

There is exactly one pole class of \(sn\) on this smaller torus, at \(p=iK'\), and it is simple. Thus \(F\) has precisely one double pole there. The nonzero coefficient \(c^2\) prevents its removal.

The quarter-period identity
\[
sn(z+K+iK')=\frac{dn z}{k\,cn z}
\]
and the axis relation locate zeros at \(p+K+v\) and \(p+K-v\). They are distinct modulo the lattice because \(0<v<K\), and neither equals the pole class. A nonconstant elliptic function has total zero multiplicity equal to its total pole multiplicity. The two distinct displayed zeros therefore exhaust the divisor and are both simple:
\[
\operatorname{div}F=[p+K+v]+[p+K-v]-2[p].
\]

As an independent multiplicity check, the Jacobi differential identity gives, at either zero,
\[
(F')^2
=4c^4 sn^2u(1-sn^2u)(1-k^2sn^2u)
=\frac{4a^2b^2(a^2-\alpha^2)}{\alpha^2}\ne0.
\]
This uses strict nesting and provides a second verification that no zero was counted with the wrong multiplicity.

## 4. Cyclic cancellation and universal constancy

Let \(\delta=2v=2K\tau/m\). Its order on \(T\) is exactly \(m\). The real period lattice is \(2K\mathbb Z\), and coprimality gives this order directly.

Since \(mv=K\tau\) with odd \(\tau\),
\[
K\equiv mv\pmod{2K}.
\]
For odd \(m\), the two zero shifts are therefore
\[
K+v\equiv\frac{m+1}{2}\delta,\qquad
K-v\equiv\frac{m-1}{2}\delta\pmod{2K}.
\]
In the product defining \(R\), each of these two zero lists is a permutation of the same \(m\)-point pole orbit. At each point the two simple zeros cancel the double pole exactly. There are no other divisor points.

Hence \(\operatorname{div}R=0\). The product is a meromorphic function on the compact connected torus, so it extends to a constant holomorphic function. It is neither identically zero nor infinite, since for real \(u\),
\[
F(u)\ge a^2-c^2=b^2>0.
\]
This proves constancy at every real starting phase, for every admissible modulus and primitive turning number.

The argument does not need a numerical limit, a density argument over rational rotation numbers, or a closed formula for the constant. The displayed evaluation at \(u=0\) is valid but not needed for the existence of the invariant.

For \(N\equiv0\pmod4\), \(m\) is even and the proposed zero shifts occupy the other half-step coset. The cancellation just proved is unavailable. For an odd polygon artificially repeated twice, \(\tau\) would be even in the unreduced \(N\)-description, invalidating the antipodal step. The candidate correctly excludes that reinterpretation rather than silently assuming its pairing.

## 5. Reproduction and independent controls

The author files were copied into author_replay/ and run there, preserving the author's directory. The 29,397 exact assertions pass. The 210 high-precision diagnostics also pass, with the saved maximum relative error unchanged; these remain explicitly numerical evidence rather than proof.

My independent checker uses integer indices on a denominator-\(2m\) circle to reconstruct the full zero-minus-pole multiplicity vector. It tests primitive rotations with both odd and even \(m\), so the excluded parity is checked as a negative control. It also checks ordinary focal-distance identities, strict axis inequalities, the derivative-square multiplicity formula, the two exact six-bounce focal products, and the failure of antipodal pairing for a repeated odd orbit. All 5,198 assertions pass. This checker uses only Python's standard library and performs no numerical Jacobi evaluations.

The copied proof and verifier hashes match the assigned frozen snapshot. The submitted verification receipt reproduces byte for byte.

## 6. Credit and publication recommendation

Recommend **claimed_solved, 2/5**, with the explicit primitive, nondegenerate elliptical-caustic scope retained. No mathematical correction is required.

Stachel's canonical parametrization, DLMF's Jacobi identities and the earlier Akopyan–Schwartz–Tabachnikov complex pole-cancellation method are substantive prior inputs and are appropriately credited. The earlier campaign's six-bounce geometry is only a control here; the full proof does not depend on its sibling theorems. A bounded current search did not establish a prior exact k114 proof or historical priority.

The proof should continue to be described as AI-generated, separately AI-reviewed and unrefereed. The verdict certifies the mathematical deduction from the stated classical inputs; it does not claim independent reconstruction of all of Stachel's analytic theorem or a first discovery.

