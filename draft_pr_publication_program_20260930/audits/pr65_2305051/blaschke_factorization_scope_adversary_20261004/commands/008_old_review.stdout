# Independent adversarial review: 2305051 / Holland Problem 5.51

**Verdict: PASS_COMPLETE_EXPLICIT_CONSTRUCTION, with historical priority unestablished.** The frozen candidate gives a deterministic recursive construction of a nonconstant infinite Blaschke product \(B\), with \(B(0)=0\), whose Cayley transform \((1+B)/(1-B)\) is Bloch. No required mathematical correction was found.

This is a separate AI mathematical review (gpt-6-astra, xhigh), completed 2026-09-30, not human peer review or a novelty certificate.

Frozen CANDIDATE.md SHA-256:
0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4

Author verifier SHA-256:
f7c373029005f3d1ba397aa849280f46ee4c599bca1358ff19ab168a172c473c

## 1. Target, explicitness and attribution

The complete Hayman–Lingham2018 source was checked at printed p.105, including the rendered page (PDF page106). Problem5.51 takes existence as known and asks for an explicit construction of a Blaschke product with precisely the normalization and Bloch Cayley transform asserted here. It does not impose a particular formula for the zero sequence.

The candidate specifies:
- an integer recursion with every tie resolved;
- a finite rational-inner formula at every stage, with algebraic coefficients;
- one limit and an explicit compact-uniform convergence modulus.

This qualifies as an explicit recursive construction in the ordinary constructive meaning of the source request. It does not qualify as a short closed-form zero list, which the candidate expressly does not claim. There is no hidden generic parameter, good-shift search, unspecified measure choice or covering map in its definition.

The absorbed-walk and neighbor-balancing method is closely related to credited classical work. Cantón's full1998 paper explicitly develops four-adic, neighbor-directed singular-measure constructions with varying barriers and step sizes. AAN1999 gives stronger existence results by a different method. The present review validates this specified construction, not historical priority. No claim that the result is a new existence theorem, or that no prior explicit construction exists, is justified by the bounded literature audit.

## 2. The all-stage recursion

A positive integer parent has first and last increments in \(\{-1,1\}\), so the required middle sum is \(-2,0\), or \(2\). The lexicographic rule selects a unique pair, always giving two upward and two downward steps. Nonnegativity, mass preservation, the unit-step bound and the growth bound \(v_j^{(n)}\le n+1\) follow inductively. A zero parent is absorbing.

The circular neighbor proof is valid in all cases. For unequal positive parents with signed difference d, the new facing difference is d minus twice its sign; if \(|d|\le2\), its absolute value is still at most2. For equal positive parents the prescribed asymmetric tie choices give facing values differing by2. At a zero/positive boundary, the positive parent is at most2 and its facing child is one smaller. Both-zero boundaries and within-parent boundaries are immediate. The cyclic edge, including the first one-cell stage, is covered.

Under Lebesgue measure, conditional transition probabilities are exactly one half in each direction until absorption, regardless of where the children are placed. The finite-barrier stopping argument proves absorption at zero almost surely. There is no assumption of uniform integrability of the martingale.

## 3. Measure existence, non-atomicity and singularity

The consistency of cell masses gives a unique probability measure. A weak-limit construction can be made without circular reasoning about endpoints: for any fixed point and sufficiently fine generation, take a small open neighborhood covered by at most two adjacent cells. All later density measures give that neighborhood mass at most \(2(n+1)4^{-n}\). The open-set part of Portmanteau passes this upper bound to any weak limit, so the limit has no atoms. The cell boundaries are consequently continuity sets, and the prescribed masses pass to the limit. The interval algebra determines the measure uniquely.

Every cell that reaches zero has zero limiting mass. The countable union of such cells has full Lebesgue measure by absorption, and zero measure for \(\mu\). Thus \(\mu\) is singular, atomless and of total mass one.

The stronger density assertion is genuinely pointwise. Along each chosen nested half-open cell sequence, its density is either eventually zero, or its successive differences always have absolute value one. Neither behavior converges to a finite positive value. This statement is valid at four-adic endpoints using the stated nesting convention, and is substantially stronger than almost-everywhere singularity.

## 4. Global Zygmund estimate and the Bloch input

For the periodic primitive \(H_n=\int_0^x(f_n-1)\), the increment has zero integral on each parent cell and derivative bounded by1 there. Hence its uniform norm is at most the parent length. Summation gives the stated tail bound \((4/3)4^{-n}\) and \(\|H\|_\infty\le4/3\).

At scale \(4^{-n}\le h<4^{1-n}\), the interval \([x-h,x+h]\) meets at most nine consecutive cells. The circular neighbor bound controls the density differences there by18, a safe overestimate. The primitive second difference is at most \(18h\), and the uniform-tail contribution at most \((16/3)4^{-n}\). Their sum is below \(24h\). For \(h>1/4\), the uniform norm alone gives the same asserted constant. There is no unexamined boundary at the origin of the circle.

The correspondence between this primitive and the measure is \(dH=d\mu-dx\). Equal arc lengths cancel the Lebesgue contribution, so the arbitrary adjacent-arc estimate follows.

I independently retrieved AAN's [full author PDF](https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf), matching the author's source hash, and visually checked printed p.333. The proof of Theorem3.5 explicitly states that the Herglotz transform of a positive measure is Bloch exactly when the measure is Zygmund. This imported classical criterion applies to the proved global arc estimate. Normalized angular length versus radians only rescales its finite constant.

The proof does not infer a uniform Bloch bound from the atomic approximants. Those approximants have boundary poles in their Herglotz transforms. It applies the criterion to the atomless limiting measure, which is the correct argument.

## 5. Innerness and nonconstancy

For the probability Herglotz transform, \(F(0)=1\) and \(\operatorname{Re}F>0\). Therefore \(B=(F-1)/(F+1)\) maps the disk into itself and \(B(0)=0\).

The Poisson integral of the singular measure has radial limit zero Lebesgue-almost everywhere. The displayed identity for \(1-|B|^2\), together with \(|F+1|\ge1\), gives radial modulus one almost everywhere. The usual boundary theorem for bounded analytic functions supplies the radial values, so B is inner.

The nonconstancy argument is valid: the only constant F with the prescribed value at0 is1, whose Herglotz measure is Lebesgue measure by uniqueness. It cannot equal the singular probability measure constructed here.

As an independent check, the second-generation masses already certify a nonzero Fourier coefficient. All mass lies in the two quarter-arcs on which \(\sin(4\pi x)\ge0\), and mass \(3/4\) lies where this sine is at least \(\sqrt2/2\). Thus \(\int\sin(4\pi x)\,d\mu\ge3\sqrt2/8>0\). Nonconstancy does not rely on numerical evaluation near the boundary.

## 6. Singular-factor exclusion: detailed audit

This is the essential part; compact-uniform limits of finite Blaschke products alone would not suffice.

Suppose B has a nonzero singular inner factor \(S_\nu\). For \(\nu\)-almost every point \(\xi\), differentiation of Lebesgue measure with respect to the singular measure gives
\(\nu(I(\xi,t))/t\to\infty\).
For z in a fixed Stolz cone at \(\xi\), with \(\delta=1-|z|\), the Poisson kernel is bounded below by a positive cone-dependent multiple of \(1/\delta\) on an arc centered at \(\xi\) of length comparable to \(\delta\). Therefore \(P[\nu](z)\to\infty\) throughout that cone, not merely along a radial subsequence.

It follows that \(|S_\nu(z)|\to0\) nontangentially. Every other inner factor has modulus at most1, so \(B(z)\to0\) and then \(F(z)\to1\) nontangentially at these points.

I independently retrieved [Carmona–Donaire's full published PDF](https://msp.org/pjm/1999/191-2/pjm-v191-n2-p02-p.pdf), matching the source hash, and checked printed pp.207–208 in text and visually. The recalled Loomis theorem states that a finite nontangential limit of a positive Poisson integral gives the ordinary derivative defined through **all** shrinking intervals containing the point. Its separate radial assertion gives only the symmetric derivative. The candidate invokes the stronger, correctly applicable nontangential statement.

The disk normalization can be checked directly. After rotating \(\xi\) to1, put
\[
 w=i\frac{1-z}{1+z},\qquad s=\tan(\pi x).
\]
If \(\sigma\) is the pushforward of \(\mu\) under x to s, the circle Poisson integral becomes the half-plane Poisson integral of
\[
 d\tau(s)=\pi(1+s^2)\,d\sigma(s),
\]
apart from a possible harmonic term due to an atom at the antipodal point (there is no such atom here). The integrability condition is
\(\int(1+s^2)^{-1}d\tau=\pi\mu(\mathbb T)<\infty\).
Near0, \(ds/dx=\pi\); these factors cancel, so half-plane density1 is exactly density1 relative to normalized angular length. Conformal maps preserve the local nontangential approach condition at this regular boundary point.

The ordinary derivative includes arbitrarily unbalanced intervals with the point strictly inside. It also forces one-sided densities: compare \((\xi,\xi+h)\) with \((\xi-h^2,\xi+h)\); positivity and the symmetric interval of radius \(h^2\) make the extra mass \(O(h^2)\). The same argument works on the other side. Thus four-adic endpoints are covered.

A derivative equal to1 would force the density ratios of the nested four-adic cells to converge to1, contradicting the pointwise unit-step/absorption alternative. Hence \(\nu=0\). Canonical inner factorization now makes B a pure Blaschke product. No Frostman shift has been used.

## 7. Infiniteness, rational stages and error bound

A nonconstant finite Blaschke product maps the boundary circle onto itself and has nonzero derivative at points mapped to1. Its Cayley transform has a simple boundary pole; along an inward radius its derivative grows like \((1-r)^{-2}\), violating the Bloch bound. Thus the present product is infinite. Equivalently, such a pole would contribute an atom to its Herglotz measure, while \(\mu\) is atomless.

The midpoint atomic measure has the exact limiting mass of every generation-n cell. The angular derivative of the Herglotz kernel is bounded by
\(4\pi r/(1-r)^2\) on \(|z|\le r\). Midpoint transport costs at most half a cell length, giving the factor \(2\pi\) in the F-error. The exact Cayley difference identity and the lower bounds for both denominators then give
\[
 \sup_{|z|\le r}|B-B_n|
 \le\frac{4\pi r}{(1-r)^2}4^{-n}.
\]
There is no boundary-uniform convergence claim.

For each n, the rational Herglotz function has positive real part in the disk and purely imaginary boundary values off its atoms. Its poles become removable points of the Cayley transform, with value1. Thus \(B_n\) is rational inner, hence finite Blaschke. Its coefficients are algebraic because its weights are rational and its atoms are roots of unity. Every \(B_n(0)=0\). The polynomial formula's denominator is nonzero at0 and throughout the disk after cancellation.

## 8. Exact diagnostics and recommendation

The submitted script was replayed unchanged in an isolated directory with its required sibling candidate. All **2,884 assertions** and the receipt reproduced byte for byte.

The separately written checker imports no author code and passes **37,154 exact integer/rational assertions**, through stage7 (16,384 cells). It checks local facing cases at small and large heights, every circular edge and parent consistency, the independent absorbed-walk survival formula, primitive increments and translated rational arc differences, exact midpoint transport, the nonconstancy mass witness, the first two rational-inner formulas, and the Cayley difference identity.

These checks support the proof; they do not establish boundary factorization by finite sampling. The all-stage and analytic reasoning above is the basis of the verdict.

The frozen candidate may be published as a complete explicit-construction claim, with the classical method attribution and unestablished priority stated prominently. The precise output is an explicit recursive limit with a quantitative error bound, not a closed-form zero sequence. No mandatory correction is required.
