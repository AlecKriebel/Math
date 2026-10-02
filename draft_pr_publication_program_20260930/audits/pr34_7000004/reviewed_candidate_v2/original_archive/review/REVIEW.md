# Independent review of the injective binormal obstruction

**Verdict: PASS for the unresolved obstruction and source-scope report, after the three narrow clarifications below were incorporated and checked.** This is a source-scope and local-argument review. It does not certify a solution, a counterexample, or the full numerical example in the cited paper.

Problem 7000004 / AMR-069-0004. Reviewed on 30 September 2026 by a separate gpt-6-astra agent at xhigh effort. Initial reviewed `OBSTRUCTION.md` SHA-256: `8be32eb4ac09ebac4018774194af299a8fd81b54a514dfa1bb69af04548701f3`.

## Exact source and scope

The full [Ghomi survey](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), printed p. 6, was checked around Problem 1.4. It allows a smooth closed **immersed** center curve and a **continuous** injective binormal field, using continuously chosen osculating planes that contain the first two derivatives. Curvature-zero points are expressly compatible with this definition. The preceding tight-surface discussion and the warning about unwarranted regularity in an earlier approach are relevant to the exact question.

The intended spherical, nonvanishing unit-binormal convention should be stated as a convention rather than silently derived from the text: the 2019 statement does not literally specify unit length. Dividing an arbitrary vector-valued field by its length need not preserve its injectivity. This ambiguity is not used as a purported counterexample.

The [Ghomi–Raffaelli paper](https://link.springer.com/article/10.1007/s12220-025-02200-3), published 9 October 2025, still states the related embedded-surface question as Problem 1.1. Its hypotheses in Sections 1–2 include an embedded orientable surface of class at least $C^3$, negative Gauss curvature, and a closed asymptotic curve. Consequently the center curve is simple and its Darboux normal has nonvanishing derivative. These are genuine additional hypotheses. Injectivity of a merely continuous spherical field does not imply a nonzero derivative, a finite length, or even differentiability.

A sufficiently small normal push-off of a compact smooth embedded curve is disjoint from the center curve by the tubular-neighborhood theorem, even for a continuous nonvanishing field. For an immersed center curve this requires separate care. Linking can be defined for two disjoint immersed cycles; it is not the occurrence of self-intersections alone that makes every such definition impossible. The artifact correctly identifies possible failure of disjointness as a caveat, not as a universal failure or a counterexample to the intended question.

## Frame identities and the linking formula

With arclength parameter, $T=\Gamma'$, a unit binormal $B$, and $N=B\times T$, differentiating orthonormality and using $B\cdot T'=0$ gives

$$T'=\kappa_sN,\qquad N'=-\kappa_sT+\tau B,\qquad B'=-\tau N.$$

Thus regularity of $B$ gives $|B'|=|\tau|>0$, so continuous $\tau$ has fixed sign. The twist integrand is

$$T\cdot(B\times B')=\tau,$$

which agrees with the sign and normalization in the artifact. This calculation remains valid when $\kappa_s=0$; division by curvature is unnecessary. The standard smooth embedded ribbon identity is $\operatorname{Lk}=\operatorname{Wr}+\operatorname{Tw}$. Neither nonzero torsion nor nonzero twist alone rules out cancellation by writhe.

The cited Theorem 1.2 was matched to its proof, not merely to its displayed statement. Let $u$ be generic and not parallel to a tangent, and write $a=u\cdot T$, $b=u\cdot N$, $c=u\cdot B$. Their derivatives are

$$a'=\kappa_sb,\qquad b'=-\kappa_sa+\tau c,\qquad c'=-\tau b.$$

For $v=(u\times T)/|u\times T|=\cos\theta\,N+\sin\theta\,B$, one has $\cos\theta=c/\sqrt{b^2+c^2}$ and $\sin\theta=-b/\sqrt{b^2+c^2}$, hence

$$\theta'=-\tau+\frac{\kappa_sac}{b^2+c^2}.$$

At a zero of $c$, $b\ne0$, so $c'\ne0$ and $\theta'=-\tau$. These zeros are isolated and finite. Counting the two regular values with angles $\pi/2$ and $3\pi/2$ gives $\operatorname{Rot}(v,B)=-\frac12\#\{c=0\}\operatorname{sign}\tau$. The planar blackboard framing has linking equal to the signed crossing sum. Therefore

$$\operatorname{Lk}(\Gamma,B)=\operatorname{Cr}(\Gamma_u)+\frac12\#\{u\cdot B=0\}\operatorname{sign}\tau.$$

This verifies the sign and factor of the imported formula under its smooth embedded hypotheses. The first term is a **signed** diagram crossing sum, not a nonnegative crossing count or knot crossing number. Controlling its cancellation remains an unproved global step in the attempted route.

## Inflections and orientation

The spherical curvature numerator is

$$B''\cdot(B\times B')=\tau^2\kappa_s.$$

With the outward orientation of the sphere, its signed geodesic curvature is $\kappa_s/|\tau|$, and spherical arclength is $|\tau|\,ds$. Thus its curvature integral is $\int\kappa_s\,ds$; changing orientation may change the sign but not the absolute-value argument. This formulation works for both signs of torsion and avoids an unwarranted replacement of $|\tau|$ by $\tau$.

A regular simple spherical curve bounds a Jordan region of area strictly between $0$ and $4\pi$. Gauss–Bonnet gives an absolute curvature integral below $2\pi$. If $\kappa_s$ had one sign, this would contradict Fenchel's lower bound $2\pi$ for the total curvature of a closed regular space curve. The artifact's inflection obstruction is therefore valid in the smoother setting it explicitly assumes. It cannot be extended to the source's continuous field merely by asserting that an approximation exists.

For planar curves the precise local observation is that on any subarc of nonzero curvature the continuous unit binormal is constant. A closed regular planar curve has such a subarc, so its binormal cannot be injective. An arbitrary nonstraight planar arc may contain a straight interval on which compatible binormals can vary; the original wording should be narrowed accordingly.

## Source discrepancy in Example 4.2

There is a concrete omission in the displayed formula of Example 4.2 in arXiv v2, the journal HTML, and the [author-hosted PDF](https://ghomi.math.gatech.edu/Papers/asymptotic.pdf) dated 19 September 2025. The two printed planar coordinates have squared sum $(3+\sin t)^2\ge4$, making the displayed third coordinate $\sqrt{1-n_1^2-n_2^2}$ nonreal.

The linked [primary Mathematica notebook](https://ghomi.math.gatech.edu/MathematicaNBs/Asymptotic-Examples.nb), Second Example, The Binormal, input cell In[1], divides **both** planar coordinates by $6$. Its radicand is then at least $5/9$. This is direct primary-source evidence for the missing factors, rather than a guessed repair. The notebook was read as text, not executed. Its SHA-256 is `89791fab271dacd16351bd21c1162c02ecbe26ee506a0dbffd8d76cda03fbd5d`.

The scaled spherical map is smooth, regular, and injective: in polar coordinates its radius is $(3+\sin t)/6>0$ and angle is $(5/2)\cos t$, whose range has length $5<2\pi$. Equality of planar points therefore forces equality of both sine and cosine. The polar velocity cannot vanish because its two terms would require both $\cos t=0$ and $\sin t=0$. This limited check does **not** certify the global construction of the closed center curve or its claimed linking number $2$.

The artifact may credit the paper's reported example and its Note 5.5 criticism of the older inflection-count formula, with the explicit source qualification above. Neither example settles the current target. No new official erratum, universal proof, or counterexample was located in the bounded searches; that is not an exhaustive status certificate.

## Reproducible verification and disposition

The submitted `verify.py` was copied unchanged and replayed in this review directory. It passes. The independent script adds **38 exact assertions**, all passing, including both torsion signs, the angular crossing calculation, the ruled-strip curvature $-\tau^2$, and the printed/notebook normalization discrepancy.

From this review directory run `python3 submitted_verify.py` and `python3 independent_checks.py` with Python 3 and SymPy 1.14.0. Both scripts write only their deterministic result files. The tests are local controls, not a topological linking certificate.

The remaining task is exactly the one identified by the author: prove that an injective compatible binormal excludes the required cancellation, or construct a valid disjoint zero-linking push-off under all intended source hypotheses. The attempted work establishes neither. Preserve the **unsolved** disposition and do not promote the package to a solved or novel-result claim.

## Final snapshot coverage

The author incorporated exactly the three requested clarifications: the unit-field convention, the planar-subarc wording, and the explicit Example 4.2 source discrepancy. The complete diff was checked on 30 September 2026 at 05:33 UTC. No other mathematical change was present, and no required correction remains.

Final reviewed `OBSTRUCTION.md` SHA-256: `6689fb008c098f14fc6cb99bfd761b72728a391330f9888f0e106c344537955f`.

**Final verdict: PASS for an explicitly unresolved source/obstruction package.** The full open problem remains unresolved in this attempt. The review is AI-generated and unrefereed; it certifies neither novelty nor the complete published example.
