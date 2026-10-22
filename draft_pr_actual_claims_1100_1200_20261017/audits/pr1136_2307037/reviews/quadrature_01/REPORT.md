# Independent adversarial audit: PR1136 quadrature construction

Date: 2026-10-17 UTC. Reviewer scope: Input B and Section 1 of the supplied proof, including its source hypotheses, arbitrary positive masses, overlaps, repeated centers, boundedness, null boundary, exact area, and every component of the complement.

**Verdict: PASS within this scope.** The imported quadrature theorem applies as used. A complete hypothesis check and the derivation below establish a bounded open set Omega, containing neighborhoods of all nodes, with null boundary, total area equal to total mass, and the required pointwise inverse-square identity everywhere outside its closure. I found no missing hypothesis or counterexample. This verdict does not cover the Eremenko-Hamilton estimate, the later localization estimate, historical priority, or novelty.

The principal artifact reviewed is `inputs/PROOF.md`, SHA-256 `32e68249400aad782b77c74405890f9929fc8576ab8a13d59a3b8db75dea9bdc`. The supplied PR sourcehead is `cbbe7826cca914588018c840ba99c6b7a59fa7f5`. Both reviewed inputs were verified byte-identical to their blobs under `unsolved_math_prioritization/attempts/2307037/` at that commit. The separate workspace HEAD at audit start was `fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9`. Input byte pins, rather than the workspace HEAD, identify the reviewed text. I read PROOF and README before obtaining the sources. I did not read AUDIT, SOURCE_HYPOTHESES, SOURCE_REVIEW, AUTHOR_CHECKS, or another reviewer's artifacts. No Git refs/index, PR, deposit, paper, or tracker were changed.

## Primary source and verified interface

Freshly retrieved [Levine-Peres author manuscript](https://lionellevine.github.io/scalinglimit.pdf), dated May 1, 2009, and [arXiv:0712.3378v2](https://arxiv.org/pdf/0712.3378v2). Exact retrieval and body identities are in SOURCE_PINS.json. Relevant PDF/printed pages coincide. Pages 6, 14-17, 54-55, 58-59, and 66-67 have byte-identical extracted text across the two PDFs. I visually inspected pages 16, 58, and 59. The final-journal endpoint returned HTML, so I do not claim final-PDF verification.

The following is the source interface; all subsequent arguments are the audit's deductions.

- Definition (4), p. 6: binary smash sum is the union of its inputs and its obstacle noncoincidence set.
- Proposition 2.12, p. 16: bounded compactly supported, almost-everywhere continuous densities with values outside a fixed gap below 1 give a null boundary for the enlarged occupied set.
- Corollary 2.13 and Lemma 2.15, p. 17: binary sums of bounded open null-boundary sets preserve area additively; bounded densities of compact support have bounded noncoincidence sets.
- Lemma 6.1, pp. 54-55: the sum is associative for these inputs.
- Proposition 6.6, pp. 58-59: balls of arbitrary positive volumes and arbitrary centers satisfy the superharmonic quadrature inequality for integrable functions on their sum. Distinctness is absent. Its auxiliary proof uses doubled densities on half-volume balls; that strict-density condition is not imposed on the original balls.

## Exact claim and universal derivation

Let n be a finite positive integer, a_j complex numbers, and m_j positive real numbers, with M=sum_j m_j. Let B_j be the open disk centered at a_j with radius sqrt(m_j/pi). We must establish the existence of a bounded open Omega such that:

1. every B_j is contained in Omega;
2. its boundary has planar Lebesgue measure zero and |Omega|=M;
3. every real harmonic h integrable on Omega satisfies

   integral_Omega h(w) dA(w) = sum_j m_j h(a_j).

For normalized squared poles, m_j=pi*lambda_j and M=pi. No source result needs n, the centers, or the masses to satisfy an additional quantitative bound.

### Construction, regularity, and area

Define U_1=B_1 and U_{k+1}=U_k smash B_{k+1}. We prove by induction that U_k is bounded and open, contains its constituent disks, has null boundary, and has area sum_{j<=k} m_j.

For k=1 these statements are elementary properties of a disk. At the next step put sigma=1_{U_k}+1_{B_{k+1}}. This function has values in {0,1,2}; hence, for example, every value is either at most 1/2 or at least 1. This checks the density-gap requirement pointwise, including on the boundaries under the open-set indicator convention.

The function is bounded by 2. Its support is contained in the compact union of the two bounded closures. An indicator of an open set is continuous off its boundary. Therefore sigma is continuous off a subset of the union of the two boundaries, a null set by induction. Also {sigma>=1}=U_k union B_{k+1}, already open. Thus the enlarged set in Proposition 2.12 is exactly U_{k+1}, and it has null boundary. The definition makes U_{k+1} open and ensures containment of both inputs. Lemma 2.15 makes the added noncoincidence set bounded, so U_{k+1} is bounded. Finally Corollary 2.13 gives

|U_{k+1}| = |U_k| + |B_{k+1}| = sum_{j<=k+1} m_j.

This closes every induction hypothesis; it does not assume the future set is already regular. In particular, it does not attempt to apply a smooth-density theorem directly to discontinuous indicators. Set Omega=U_n. Associativity allows the usual unparenthesized sum, although a fixed left-associated construction already suffices for existence. Commutativity follows directly from the symmetric binary density and union, so neither a pole ordering nor a grouping affects the result.

The source hypotheses do not require the disks to be disjoint. Overlap increases sigma to 2, a value safely above the gap. Coincident disks or coincident centers have the same property. Arbitrary small positive masses give small genuine disks and do not invalidate the finite induction. Arbitrarily distant centers still give compact support at each step. No universal bound on the diameter is needed.

Now let S=closure(Omega). Boundedness makes S compact. Since Omega is open, S minus Omega equals its boundary, so |S|=|Omega|=M exactly. Every node a_j has the open neighborhood B_j inside Omega. A null boundary is essential for this closure step; area conservation of Omega alone would not suffice.

### Harmonic quadrature and repeated centers

Take an integrable real harmonic function h on Omega. Both h and -h are superharmonic there and integrable. The source quadrature inequality applied to h gives

integral_Omega h <= sum_j m_j h(a_j).

The same inequality applied to -h reverses this inequality. All displayed quantities are finite because h is integrable and harmonic values at the finitely many interior nodes are finite. Therefore equality follows. No limiting argument, boundary extension of h, or simply connectedness is required.

For repeated centers, one may instead first replace all terms with center a by one term with mass sum_{j:a_j=a} m_j. This preserves the atomic measure and the target rational function and gives a direct construction for the combined list. The existence claim needs only one such construction. It does not require an independent proof that combining repeated centers produces a different construction equal as an open set. The stronger source statement already permits repeated centers.

### Exterior field in every component

Fix any z outside S. Because S is closed, delta=dist(z,S)>0. For w in Omega,

|1/(w-z)^2| <= delta^(-2),

so the kernel is absolutely integrable, with integral of its absolute value at most M/delta^2. The same function is holomorphic on an open neighborhood of S: take, for example, all points of distance less than delta/2 from S. Its real and imaginary parts are bounded integrable harmonic functions on Omega. Applying the real equality to each part gives

integral_Omega dA(w)/(w-z)^2 = sum_j m_j/(a_j-z)^2.

For m_j=pi*lambda_j the right side is pi*g(z), because the square removes the sign of a_j-z. Under T f(z)=-(1/pi) integral f(w)/(w-z)^2 dA(w) outside the support closure, this gives T 1_Omega(z)=-g(z).

The argument begins with an arbitrary point of the entire set C minus S. Its only geometric input is positive distance to S. Thus it applies pointwise in bounded holes as well as in the unbounded component. There is no analytic continuation across S, no differentiation at its boundary, no principal value at a pole, and no almost-everywhere-to-everywhere promotion. The exterior integral itself supplies the canonical pointwise representative of T. The usual L2 realization agrees with it almost everywhere where the later estimate uses T.

S was constructed solely from the finite masses and centers. The choice of an observation radius R never enters this construction or equality.

## Attempts to falsify the hypotheses

### An actual bounded complementary component

Take three centers a_j=(2/3)*exp(2*pi*i*j/3), j=0,1,2, with lambda_j=1/3. Their disks have common radius r=1/sqrt(3). Adjacent centers have distance 2r, so the open disks are disjoint and the closed disks tangent. The density of their open union is at most 1. The corresponding obstacle is already superharmonic (its distributional Laplacian is proportional to sigma-1<=0), so its least superharmonic majorant equals it. Consequently the smash sum equals the open union; there is no redistribution.

The triangle with these centers as vertices has its entire boundary covered by the closed disks, since each side is covered by its two radius-r endpoint disks. The point z=0.02+0.01i lies inside that triangle and outside all three disks. Its complement component is therefore bounded: any path from it to infinity must cross the triangle boundary. Its distance to the disks is strictly positive. The disk mean-value theorem individually yields the desired inverse-square identity at this hole point. This tests a genuine hole in C minus S and not a point merely outside the convex hull.

An additional independent closed form is

g(z)=z*(z^3+2*c^3)/(z^3-c^3)^2, where c=2/3.

It follows by differentiating the elementary logarithmic derivative of z^3-c^3. The numerical control compares direct boundary integration to both the atomic sum and this rational expression.

### Entire harmonic moments would be insufficient

The annulus A={1<|w|<sqrt(2)} has area pi. For every entire harmonic function h, the disk mean-value property gives integral_A h=pi*h(0). For |z|>sqrt(2), expanding (w-z)^(-2) in nonnegative powers of w and integrating angles gives integral_A (w-z)^(-2) dA=pi/z^2. But for 0<|z|<1, expansion in negative powers of w shows the same integral is zero: every angular term has nonzero frequency. At z=1/2 the purported atomic value is 4*pi, not zero.

This is a counterexample to a weakened inference from entire moments or the unbounded exterior field to all complementary components. It is not a counterexample to Proposition 6.6: its node lies in the annular hole, and the full on-domain harmonic identity fails. The audited proof invokes the full on-domain harmonic statement, so it passes this adverse test.

### Ordinary union would be insufficient for overlapping disks

Take radius sqrt(1/2) disks centered at +/-1/2. Their intended total mass is pi. Their overlap area is pi/4-1/2>0, so their ordinary union has area pi-(pi/4-1/2), strictly less than pi. Its field also differs from the sum of the two full disk fields. The construction correctly uses smash sum instead of ordinary union.

For an independent positive overlapping example, use the star-shaped oval with polar boundary rho(theta)^2=1+(1/2)*cos(2*theta). Its area is pi. Set

Q(z)=sqrt(3/16+z^2/4), Q(0)>0,

and S_o(z)=z*(1/2+Q(z))/(z^2-1/4).

The branch points +/-i*sqrt(3)/2 lie outside the oval, which is simply connected; hence the indicated square root is holomorphic inside and near its closure. The quartic boundary equation implies S_o(z)=conjugate(z) on the boundary, with the branch fixed at the positive real intercept and continued along the boundary. Its only interior poles are +/-1/2, each with residue 1/2. Green's theorem and residues therefore give, for every f holomorphic near the closed oval,

integral_Oval f dA=(pi/2)*(f(1/2)+f(-1/2)).

This independently proves the exact field oracle used for the numerical overlapping controls; it does not assume the source proposition to produce the expected values. It also exhibits the correct sign and factor pi for the Beurling normalization. A point just outside the largest real intercept sqrt(3/2) tests sensitivity near the boundary.

### Other failure modes checked

- A large enclosing disk would contain all poles but generally have the wrong area and moments. Containment alone was never used as a substitute for quadrature.
- A bounded open set need not have null boundary: removing a positive-area closed nowhere-dense subset of the unit disk leaves a dense open set whose closure has greater area. Proposition 2.12 supplies the needed extra fact in this construction.
- A finite-point numerical test cannot establish arbitrary masses, arbitrary overlap, null boundary, or a universal statement over complement points. Those are established by the deductions above.
- Vanishing weights are outside the stated positive-mass hypothesis; zero terms can simply be discarded. Negative or complex weights are outside this proof's scope. There is no claim for infinite source lists.

## Checkable computation and reproducibility

`check_quadrature.py` is a standard-library-only control program. It evaluates Green boundary integrals directly on explicit circles and the independently specified oval. It covers a non-normalized mass 0.37, a translated node, repeated centers, mass ratio 1e-8:(1-1e-8), the tangent-ring bounded hole, overlapping nodes, exact areas, the sign/factor pi, and an observation point near the oval boundary. The ordinary-union and annulus models are required to fail their respective false identities. This is diagnostic floating-point integration; differences under refinement are not claimed as rigorous interval error bounds.

Results are stored separately for normal and optimized Python execution. Each successful run reports 13 positive checks and 2 adverse rejections. Both modes pass. The largest positive absolute error was approximately 7.68e-12, in the near-boundary oval integral, against a predeclared tolerance of 1e-8. The ordinary-union field discrepancy was approximately 0.0677959359, while its 8192-to-16384 refinement difference was approximately 3.97e-10. The annulus hole discrepancy was 4*pi, approximately 12.5663706144.

All runtime checks use explicit exceptions, not Python assertions. A deliberate +1 corruption of the first expected value fails with exit code 2 and an explicit error in both normal and optimized modes. This confirms that optimized execution does not disable the verifier. The resulting stdout, stderr, and exit codes are retained in `results/`; code and input-pin hashes are also recorded inside successful results.

From this folder, reproduce with:

```text
python3 check_quadrature.py
python3 -O check_quadrature.py
python3 check_quadrature.py --perturb-oracle
python3 -O check_quadrature.py --perturb-oracle
```

The last two commands must fail. Mathematical source bodies, extracted text, renderings, retrieval headers, and raw comparison material are confined to ignored `sources/private/`. The source-page hash comparison contains no source text. No third-party body is a public artifact. ARTIFACT_RECEIPT.json lists every authored public file with a SHA-256 digest and records the intentionally excluded private material.

## Strongest verified result and remaining boundary

For every finite positive atomic source measure, the imported results yield exactly the regular quadrature set required by the target proof; the complete derivation above proves the inverse-square identity pointwise on its entire closed-set complement, including genuine bounded holes. No correction to Input B or Section 1 is required. The remaining boundary of this review is explicit: later analytic estimates and priority are separate questions; final-journal pagination was not independently compared. This is an independent AI-assisted mathematical audit, not external human peer review or formal proof-assistant certification.
