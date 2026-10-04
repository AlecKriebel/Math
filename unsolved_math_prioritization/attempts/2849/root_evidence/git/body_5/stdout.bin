# Independent review of the instanton degeneracy obstruction

**Verdict: PASS for the explicitly unresolved obstruction and the narrowly stated source check.** No mandatory mathematical correction was found. The local quartic is not a manifold counterexample, and trefoil 6-surgery satisfies the known instanton L-space criterion. Neither settles KP-3.51 negatively.

Problem 2849 / KP-3.51. Reviewed 30 September 2026 by a separate gpt-6-astra agent at xhigh effort. Frozen `OBSTRUCTION.md` SHA-256: `8822d3fb47154229752a40e3f3fcc22b09a823b653521da2344b26bc1a2d31d4`. The author's artifact was not edited.

## Original target and the known sufficient theorem

The complete [K3 Problem 3.51](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp. 167–168, was checked. It concerns every rational homology 3-sphere with only abelian SU(2) representations and asks for equality between the complex dimension of framed instanton homology and the order of first homology. It does not assume irreducibility of the manifold, a knot-surgery presentation, cyclic first homology, or Morse–Bott nondegeneracy.

The published [Baldwin–Sivek paper](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf), Propositions 4.4–4.5, Theorem 4.6, and Proposition 4.7, printed pp. 4353–4356, were read. They support exactly the conditional conclusion used in the artifact. Under the reducible-only hypothesis, Morse–Bott nondegeneracy is equivalent to vanishing of adjoint $H^1$ for **all** representations and to the relevant adjoint-kernel cyclic covers being rational homology spheres. This does not mean that every finite cover must be a rational homology sphere. The spectral-sequence upper bound and Euler-characteristic lower bound give equality under that hypothesis.

## Representation topology versus deformation data

Every abelian SU(2) representation can be diagonalized. Characters of the finite group $H_1(Y)$ give conjugacy classes, with precisely the inversion identification. Central characters give single-point orbits, and noncentral characters give $SU(2)/U(1)\cong S^2$. Finitely many disjoint compact orbits are the components of the representation set. The total ordinary homology rank is therefore the order of $H_1(Y)$, as in the published proof.

This does not identify the transverse Hessian kernel. The off-diagonal adjoint action of $\operatorname{diag}(a,a^{-1})$ multiplies the complex coordinate by $a^2$. Thus the rank-one coefficient system is $\chi^2$, not $\chi$. The adjoint system splits into a trivial real line and the realification of that complex system. Since the rational homology sphere has trivial real first cohomology, the stated dimension formula follows. Actual isolated representation orbits can still have obstructed first-order normal deformations; no contradiction is present.

The known theorem applies when all characters are central, or more generally when every displayed twisted cohomology group vanishes. The artifact correctly credits these cases and does not infer the missing vanishing solely from the set of representations.

## Quartic local diagnostic

For $x=|z_1|^2$ and $y=|z_2|^2$, the function is $x^2-3xy+2y^2$. The two coefficient equations in its gradient are $2x-3y=0$ and $-3x+4y=0$ when both coordinates are nonzero. Their determinant is $-1$. On either coordinate axis the remaining equation also forces the origin. The Hessian vanishes there by degree four homogeneity. Scalar circle multiplication, including weight two, preserves both squared norms.

On $S^3$, put $s=|z_1|^2$, so the lower-link condition becomes $(2s-1)(3s-2)\le0$. The interval is exactly $[1/2,2/3]$. Both complex coordinates are nonzero throughout this interval, and the explicit parametrization

$$(s,e^{i\theta_1},e^{i\theta_2})\longmapsto
(\sqrt{s}\,e^{i\theta_1},\sqrt{1-s}\,e^{i\theta_2})$$

is a product homeomorphism from the interval times $T^2$ onto the lower link. Homogeneity makes the local nonpositive sublevel set a cone on this link. The punctured cone retracts onto $T^2$, so the long exact sequence of the pair gives $H_2\cong\mathbb C^2$, $H_3\cong\mathbb C$, and zero in other degrees. Total rank three and Euler characteristic one are correct.

This falsifies the proposed abstract shortcut that an isolated analytic circle-invariant critical set with the expected Euler characteristic must have the local homology of a point. It proves nothing about realizing this particular germ as a Chern–Simons slice. Equivariant Floer data, gauge-theoretic restrictions, and differentials are not replaced by ordinary local homology. The artifact expressly retains this limitation, which is essential to its correctness.

## Versioned SU(2)-clean claim and trefoil surgery

The current arXiv record for [Bascapè, 2608.20551](https://arxiv.org/abs/2608.20551) lists only v1, submitted 20 August 2026. I read its global conventions, Section 2, Theorem 3.5 on p. 5, Definition 5.3 and Corollary 5.4 on p. 9, and the associated proof. Pages 5 and 9 were visually checked.

Definition 5.3 uses every applicable integer surgery coefficient and **unsquared** roots of unity. No irreducibility requirement on the filling, exclusion of the reducible torus-knot slope, or coprimality condition excluding slope 6 appears there. The meridian/null-longitude convention is the usual one. The phrase nontrivial surgery excludes the meridional filling; the positive integer slope 6 is not excluded. Corollary 5.4 lists torus knots, while the preceding Theorem 3.5 explicitly includes the additional slope $2p$ for $T_{p,2}$.

The surgery computation is independently supported by [Sivek–Zentner, Proposition 4.3, p. 14](https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content), including its proof, which was read and rendered. For the trefoil, the $pq=6$ filling has group $C_2*C_3$. The source writes the connected sum as $L(2,3)\#L(3,2)$; lens-space orientation conventions do not affect the group and cohomology checks here. The artifact's peripheral calculation, killing the regular fiber $\mu^6\lambda$, gives the same group and $H_1\cong C_6$.

In SU(2), an element with square equal to the identity is $I$ or $-I$: diagonalize the unitary matrix and use its determinant-one condition. Hence every representation of $C_2*C_3$ sends the order-two generator to a central matrix. Its image is abelian (indeed finite cyclic), regardless of the choice of the order-three image.

The trefoil Alexander polynomial is $\Phi_6(t)=t^2-t+1$. Thus

$$\gcd(\Phi_6(t),t^6-1)=\Phi_6(t),\qquad
\gcd(\Phi_6(t^2),t^6-1)=1.$$

The positive slope-6 filling therefore fails the unsquared condition as printed, while meeting the squared condition in Baldwin–Sivek Proposition 4.7. This establishes the specific inconsistency in the torus-knot clause of Corollary 5.4 under its printed Definition 5.3. It does not evaluate the other results of the 2026 paper or ascribe a reason for the omission. It is not an accusation, an official erratum, or a claimed new resolution of KP-3.51.

There is an additional direct check of the square distinction. A scalar coefficient system on $C_2*C_3=\langle a,b\mid a^2=b^3=1\rangle$ has character values $\alpha,\beta$. Its 1-cocycles $(u,v)$ satisfy

$$(1+\alpha)u=0,\qquad (1+\beta+\beta^2)v=0,$$

and coboundaries span $(\alpha-1,\beta-1)$. For the six characters of $C_6$, the unsquared complex $H^1$ dimensions are $0,1,0,0,0,1$. For their squares, $\alpha^2=1$ and the corresponding dimensions are all zero. Thus the relevant adjoint cohomology vanishes for every representation of this filling. The established theorem gives instanton rank $6$, not a counterexample to its conclusion.

## Other source boundaries and reproducibility

[Li–Ye, 2511.17877v1](https://arxiv.org/abs/2511.17877), Lemma 7.1 on p. 32, explicitly uses squared roots and the prime-power or twice-prime-power numerator condition. It does not settle arbitrary rational homology spheres. The current arXiv record still lists v1. In [Bascapè 2408.16635v2](https://arxiv.org/abs/2408.16635), Theorem 1.5 is about Heegaard Floer L-spaces in a specified graph-manifold family. Its p. 1 introductory biconditional is indeed stronger than the sufficient instanton implication proved in the cited Baldwin–Sivek theorem; no necessity assertion is used here. The p. 3 statement gives that sufficient implication correctly. These are source-scope distinctions, not a conclusion about the validity of the graph-manifold classification.

The submitted verifier was copied before execution. All **114 submitted assertions** pass. The independent verifier passes **100 exact assertions**, including the six-character cocycle calculation, the adjoint square weight, local critical-group arithmetic, and three-factor finite character groups. The tests do not compute instanton homology or provide a manifold realization of the quartic.

Run `python3 submitted_verify.py` and `python3 independent_checks.py` from this review directory with Python 3 and SymPy 1.14.0. The scripts write only their deterministic review result files.

**Required corrections: none.** The full target remains **unsolved** after the author's one attempted route. Preserve the narrow limits of the local diagnostic and versioned source check, all prior-result credit, and the absence of novelty and full-resolution claims. This AI review is unrefereed and covers the frozen snapshot only.
