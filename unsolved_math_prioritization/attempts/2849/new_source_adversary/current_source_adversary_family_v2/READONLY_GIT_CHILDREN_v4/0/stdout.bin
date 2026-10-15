# The degeneracy gap in Kirby Problem 3.51

**Outcome: unresolved.** One proof route was examined. The known Morse–Bott argument does not extend merely from the set-theoretic absence of irreducible representations. This note gives an explicit circle-invariant local diagnostic, and checks a recent stronger Alexander-polynomial assertion against trefoil surgery. Neither diagnostic is a counterexample to the original instanton L-space question. Separate review is pending; no discovery or priority claim is made.

## 1 Exact target and known theorem

For a closed oriented rational homology 3-sphere $Y$, suppose every homomorphism $\pi_1(Y)\to SU(2)$ has abelian image. The question is whether
\[
\dim_{\mathbb C} I^\#(Y;\mathbb C)=|H_1(Y;\mathbb Z)|.
\]
No irreducibility, surgery presentation, cyclic-homology condition, or nondegeneracy assumption is part of the target. The source is K3 Problem 3.51, printed pages 167–168, proposed and scribed by J. Baldwin; both rendered pages were inspected. [Original source](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

Baldwin–Sivek, *Stein fillings and SU(2) representations*, Geometry & Topology 22 (2018), §4.1, Propositions 4.4–4.5 and Theorem 4.6, proves the conclusion under cyclic finiteness. Under the reducible-only hypothesis this is equivalent to the Morse–Bott condition, and to vanishing of $H^1(Y;\operatorname{ad}\rho)$ for every representation. Central representations are automatically nondegenerate. Cyclically finite here refers to the covers determined by $\ker(\operatorname{ad}\rho)$, not an unrestricted claim about all finite covers. The published proof, pages 4350–4357, was read. [Published paper](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf)

## 2 What the representation set establishes

Put $A=H_1(Y;\mathbb Z)$, a finite abelian group, and let $\widehat A=\operatorname{Hom}(A,U(1))$. Every representation under consideration can be conjugated to
\[
\rho_\chi(g)=\operatorname{diag}(\chi(g),\chi(g)^{-1}).
\]
Two such representations are conjugate exactly when the characters agree or are inverses. If $\chi^2=1$, the orbit is one point. Otherwise its centralizer is $U(1)$, and its orbit is $SU(2)/U(1)\cong S^2$. There are finitely many orbits. Each is closed, and these are the connected components of the representation set.

Writing $c=|\{\chi:\chi^2=1\}|$, its ordinary homology therefore has total complex dimension
\[
c+2\frac{|A|-c}{2}=|A|.
\]
This is the elementary orbit count in Baldwin–Sivek's proof. It describes the critical set's topology, not the kernel of the Hessian transverse to it.

Indeed, the infinitesimal deformation quotient is $H^1(Y;\operatorname{ad}\rho_\chi)$. The adjoint local system splits as a trivial real line and the realification of the complex rank-one local system $\mathbb C_{\chi^2}$. Consequently
\[
\dim_{\mathbb R}H^1(Y;\operatorname{ad}\rho_\chi)
=2\dim_{\mathbb C}H^1(Y;\mathbb C_{\chi^2}),
\]
since $H^1(Y;\mathbb R)=0$. The square is essential. Absence of a curve of actual nonabelian representations does not, without another theorem, say that all first-order normal solutions vanish: those solutions may be obstructed at higher order.

If every character squares to one, all representations are central and the known theorem applies. More generally, when the displayed cohomology vanishes for all characters, the known Morse–Bott spectral sequence gives the rank upper bound, and the Euler characteristic gives the matching lower bound. These are credited special cases, not a removal of the hypothesis.

## 3 An explicit diagnostic for the proposed extension

Consider the real analytic function on $\mathbb C^2$
\[
f(z_1,z_2)=(|z_1|^2-|z_2|^2)(|z_1|^2-2|z_2|^2).
\]
It is invariant under scalar circle multiplication, including the weight-two action $z\mapsto e^{2i\theta}z$ occurring in a noncentral reducible normal representation.

**Claim.** The origin is its only critical point, the Hessian there is zero, and its local critical groups over $\mathbb C$ have total dimension three despite Euler characteristic one.

**Proof.** Set $x=|z_1|^2$, $y=|z_2|^2$. The two complex-coordinate gradient equations, up to a nonzero common real factor, are
\[
z_1(2x-3y)=0,\qquad z_2(-3x+4y)=0.
\]
If both coordinates are nonzero, the coefficient matrix has determinant $-1$, forcing $x=y=0$, a contradiction. If one is zero, the other equation forces the remaining coordinate to vanish. The Hessian at zero vanishes because $f$ is homogeneous of degree four.

On the unit 3-sphere, $x+y=1$, so the nonpositive lower link is
\[
L=\{f\le0\}\cap S^3
=\{1/2\le |z_1|^2\le2/3\}\cong T^2\times[1/2,2/3].
\]
Both coordinates stay nonzero; their two arguments and the first squared modulus give the indicated product homeomorphism. For a small closed ball $B$, the set $X=\{f\le0\}\cap B$ is a cone on $L$. Hence $X$ is contractible and $X\setminus\{0\}$ deformation retracts onto $L$. The relative homology groups defining the local critical groups satisfy
\[
H_k(X,X\setminus\{0\};\mathbb C)\cong\widetilde H_{k-1}(T^2;\mathbb C).
\]
They are $\mathbb C^2$ in degree 2 and $\mathbb C$ in degree 3, and vanish in other degrees. Their total dimension is three and their Euler characteristic is $2-1=1$. ∎

Thus even analyticity, circle symmetry, an isolated actual critical set, and the expected Euler characteristic do not justify replacing a degenerate local contribution by the homology of one point. This example is **not asserted to be a Chern–Simons local model of a 3-manifold**. Its role is to falsify that abstract inference, not KP-3.51. A proof for the actual gauge-theoretic functional must use additional structure.

## 4 A precise current-source check

Bascapè's *Some knots with no SU(2)-abelian surgeries*, arXiv:2608.20551v1, August 20, 2026, Definition 5.3, page 9, defines SU(2)-clean using every integer surgery coefficient $r$ with SU(2)-abelian filling and **unsquared** $r$-th Alexander roots. There is no exclusion of reducible fillings in that definition. Section 2, page 3, uses the usual meridian–null-longitude slope $r\mu+\lambda$. Corollary 5.4, on the same rendered page 9, says “The following knots are SU(2)-clean” and includes “torus knots $T(p,q)$.” [Versioned preprint](https://arxiv.org/abs/2608.20551v1)

The right-handed trefoil with $r=6$ checks this assertion directly.

**Surgery calculation.** The standard annular van Kampen decomposition of the trefoil exterior gives
\[
\pi_1(E(T_{2,3}))=\langle a,b\mid a^2=b^3\rangle.
\]
The common element $h=a^2=b^3$ is the regular fiber. In the peripheral torus it is $\mu^6\lambda$: a parallel of a $(2,3)$-torus knot in its containing torus has linking number $2\cdot3=6$, while $\lambda$ is the zero-linking longitude. Equivalently one may choose $\mu=a^{-1}b^2$ and $\lambda=h\mu^{-6}$. Filling at slope6 kills $h$, so van Kampen gives
\[
\pi_1(S^3_6(T_{2,3}))
=\langle a,b\mid a^2=b^3=1\rangle=C_2*C_3.
\]
Its abelianization is $C_2\oplus C_3\cong C_6$. The filling is a closed oriented rational homology sphere. This calculation is also explicitly recorded by Sivek–Zentner, *Surgery obstructions and character varieties*, Proposition4.3, page 14: it is $L(2,3)\#L(3,2)$, equivalently $\mathbb{RP}^3\#L(3,2)$. [Primary paper](https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content)

**Representation calculation.** If $A\in SU(2)$ satisfies $A^2=I$, its eigenvalues are reciprocal unit complex numbers whose squares equal one. Hence $A=I$ or $-I$. Every representation of $C_2*C_3$ therefore sends the first generator to a central matrix; its image is generated by that matrix and the image of the second generator, so it is abelian. This proves the required property for every representation, not just a selected family.

**Alexander calculation.** The usual torus-knot formula gives
\[
\Delta_{T_{2,3}}(t)
=\frac{(t^6-1)(t-1)}{(t^2-1)(t^3-1)}=t^2-t+1=\Phi_6(t).
\]
It vanishes at $e^{\pi i/3}$, which is a sixth root of unity. Thus the trefoil does not satisfy Definition 5.3 as printed. The preprint's own Theorem 3.5 on page 5 includes the slope $2p$ for $T_{p,2}$; the Corollary 5.4 proof on page 9 omits this family when reducing integral slopes to $pq\pm1$. This is a specific inconsistency in that auxiliary claim, not a statement about the paper's other results.

There is no counterexample here to Baldwin–Sivek's test or to KP-3.51. If $\zeta^6=1$, then $\zeta^2$ has order dividing 3, and $\Phi_6(\zeta^2)\ne0$. Equivalently,
\[
\gcd(\Delta(t),t^6-1)=\Phi_6(t),\qquad
\gcd(\Delta(t^2),t^6-1)=1.
\]
The squared test succeeds, so the known cyclic-finiteness theorem says this very filling is an instanton L-space. The example only prevents silently strengthening that test by deleting the square.

## 5 Other current sources and the remaining gap

Li–Ye, arXiv:2511.17877v1, Lemma 7.1 on page 32, treats SU(2)-abelian knot surgeries whose numerator is a prime power or twice a prime power; its proof explicitly uses squared roots. It does not remove the general degeneracy hypothesis for arbitrary rational homology spheres. [Primary preprint](https://arxiv.org/abs/2511.17877v1)

Bascapè, arXiv:2408.16635v2, Theorem 1.5, proves a **Heegaard Floer** L-space conclusion for a specified two-piece graph-manifold family. That cannot be substituted for the instanton statement without an additional theorem. Its introductory attribution of an “if and only if” instanton criterion is not established by the cited Baldwin–Sivek Theorem 4.6, which supplies the sufficient direction. No necessity claim is used here. [Primary preprint](https://arxiv.org/abs/2408.16635v2)

The first route stops at this precise gap: either prove that every reducible representation under the target hypotheses has vanishing normal deformation cohomology, or control the actual degenerate Chern–Simons local Floer contributions and differentials without assuming that vanishing. The representation set alone and its ordinary homology do not supply this control. No applicable general theorem or counterexample was found in the checked sources as of September 30, 2026.

The exact checks in `verify.py` certify polynomial identities, circle symmetry, elementary lower-link homology arithmetic, and finite-character counts. All 114 assertions pass. They do not compute instanton homology or realize the local model by a manifold. The original target remains unresolved; no full-solution PR should be created from this package.
