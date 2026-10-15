# Independent reproduction and counterexample audit of PR149 / 5100006 / k114

**Verdict: SCOPED PASS.** The authenticated submission reproduces its advertised controls. No counterexample was found to the stated theorem for a strictly nested, nondegenerate confocal elliptical caustic and **least** period (N\equiv2\pmod4). Exact counterexamples confirm that the stated parity and least-period exclusions are essential. This is a computational/elementary-algebra audit, not a source audit or priority determination.

This first report was formed independently of other audit agents' findings. Original scripts and reports were treated as hypotheses; scripts were inspected before being copied and executed. All work was confined to this folder. No originals, prior PR148 files, Git state, publication state, or external individuals were changed/contacted.

## 1. Exact claim and falsification criteria

For an outer ellipse (x^2/a^2+y^2/b^2=1), (a>b>0), (c^2=a^2-b^2), and a strictly nested confocal elliptical caustic with positive semiaxes, the ordinary products

\[
\prod_{j=0}^{N-1}|P_j-(c,0)|,\qquad
\prod_{j=0}^{N-1}|P_j-(-c,0)|
\]

are hypothesized to be equal positive constants across the Poncelet family when the orbit's **least** period is (N\equiv2\pmod4). Primitive star polygons are included. Counterexamples within that scope, incorrect multiplicities or antipodal pairing, branch/sign errors in ordinary distances, or failure of the recorded verification totals would reject the submission. Samples alone cannot establish the universal claim.

## 2. Unmodified replay

Authenticated proof SHA-256: `f70821b0d44e96f6be9427f906cecc5d1aff8bbd7ab09a71ddec9d75d31ef2d5`.

| Replay | Exact assertions | Rotation cases | Separate numerical diagnostics | Result |
| --- | ---: | ---: | ---: | --- |
| Author `verify.py` | 29,397 | 4,141 primitive | 210 at 85 digits | PASS |
| Submitted independent checks | 5,198 | 766 primitive, including negative controls | 0 | PASS |

The author count consists of seven controls per primitive rotation (28,987), four symbolic algebra/six-bounce controls, and 406 integer positivity controls. Thus 29,397 is an assertion count, not a count of independent mathematical mechanisms. The 210 diagnostics comprise 126 real-phase product comparisons and 84 complex-zero evaluations over 42 modulus/rotation combinations. Their maximum reported error matches the original `1.843997e-85` exactly.

The submitted independent rotation controls split into 394 odd-(m) admissible cases and 372 even-(m) excluded cases. The original result dictionaries and local replays match. The supplied bundled Python and default system Python lacked SymPy; an already-existing local Python 3.11 environment containing SymPy 1.14.0/mpmath 1.3.0 was used with bytecode writes disabled. No package was installed or altered. The runtime and all input hashes are recorded in `runtime_and_input_manifest.json`.

## 3. Independent universal arithmetic lemma

The new route classifies the subgroup and its cosets, including nonprimitive rotations, rather than only checking the submitted odd-(m) permutation formula.

Let (N=2m), (0<\tau<m), and (g=\gcd(m,\tau)). On the denominator-(2m) grid the translation generator is (2\tau). Its subgroup is

\[
H=\{0,2g,4g,\ldots,2m-2g\}\pmod{2m}.
\]

This follows from Bézout and has order (m/g). In (m) factors every class of (H) occurs with multiplicity (g). Assuming the submitted complete divisor of (F), poles occur with multiplicity (2g) on (H), and the two zero divisors occur with multiplicity (g) on the cosets (H+(m+\tau)) and (H+(m-\tau)). Distinct subgroup cosets are disjoint, so cancellation holds exactly when both shifts belong to (H), equivalently

\[
2g\mid m+\tau\quad\text{and}\quad2g\mid m-\tau.
\]

After division by (g), the coprime integers (m/g) and (\tau/g) must both be odd. This is equivalent to

\[
\frac{2m}{\gcd(\tau,2m)}\equiv2\pmod4,
\]

the actual least-period condition. If the rotation is primitive, (g=1) and (\tau) is odd, so cancellation is exactly the advertised odd-(m) case. This also handles repeated admissible even-period orbits without relying on a possibly incorrect pairing at the nominal half-period. It rejects repeated odd-period orbits.

This elementary arithmetic lemma is proved for all positive integer (m,\tau) in the stated range. The new script additionally checks the closed-form coset multiplicities against direct incidence counts for **all 3,160 rotations with (1\le m\le80)**, including nonprimitive ones. Its universal application to the analytic norm remains conditional on the elliptic parametrization and complete divisor, which this audit does not independently source-establish.

For a primitive (N=2m) rotation, the half-displacement is (2K\tau). Since (\tau) is odd, the published sn/cn shifts make the vertices antipodal. When (\tau) is even at a nominal even period, that particular half-period argument is invalid; the least period must first be reduced.

## 4. Ordinary distances and exact geometric controls

The ordinary-distance identity has a direct universal algebraic proof. Eliminating (y^2=b^2(1-x^2/a^2)) gives

\[
(x\mp c)^2+y^2=(a\mp cx/a)^2.
\]

Since (|x|\le a) and (a>c>0), the positive square root is (a\mp cx/a), with no branch ambiguity. A real antipodal pair therefore contributes (a^2-c^2x^2/a^2>0). New rational-conic controls verify this independently at 183 rational points on three ellipses with rational (a,b,c).

The new exact polygon checker verifies every vertex's outer-ellipse equation, every edge's tangency to the declared caustic, distinct vertices, and the reflection law. It does not merely assume that supplied coordinates are billiard orbits. Reflection is checked by equality of the squared unit tangential components with matching tangential sign; strict convexity supplies the opposing incoming/outgoing normal signs.

For (a=2,b=1), two exact six-period orbits have caustic semiaxes squared (32/9,5/9). The horizontal orbit has vertices

\[
(2,0),(4/3,\sqrt5/3),(-4/3,\sqrt5/3),(-2,0),
(-4/3,-\sqrt5/3),(4/3,-\sqrt5/3),
\]

and the vertical orbit has vertices

\[
(0,1),(-4\sqrt2/3,1/3),(-4\sqrt2/3,-1/3),(0,-1),
(4\sqrt2/3,-1/3),(4\sqrt2/3,1/3).
\]

The direct ordinary products for **both foci and both orbits** are exactly (64/9). These are exact validated examples, not an all-phase proof.

## 5. Exact negative controls

### Excluded primitive four-period family

For the same outer ellipse (a=2,b=1), caustic semiaxes squared (16/5,1/5), the diamond ((2,0),(0,1),(-2,0),(0,-1)) is a billiard with each focal product (4). The rectangle with corners ((\pm4/\sqrt5,\pm1/\sqrt5)), taken cyclically, is a billiard for the **same** caustic with each focal product (64/25). The exact checker verifies all geometric conditions. Thus the (N\equiv0\pmod4) extension fails.

### Odd orbit repeated twice

Set

\[
q=(-4+\sqrt{13})/3,
\quad \alpha^2=3+q^2,\quad\beta^2=q^2.
\]

The strict confocal caustic is shared by the exact triangles

\[
T_V=\{(0,1),(2\sqrt{1-q^2},q),(-2\sqrt{1-q^2},q)\}
\]

and

\[
T_H=\{(2,0),(-\alpha,\sqrt{1-\alpha^2/4}),
(-\alpha,-\sqrt{1-\alpha^2/4})\}.
\]

Their edges and reflection laws pass exactly. They have three distinct vertices, hence least period 3. Their plus-focus products are

\[
R_V=2(1+3q^2)=64/3-16\sqrt{13}/3,
\qquad R_H=(2-\sqrt3)(2+\sqrt3\alpha/2)^2.
\]

The script certifies rational bounds (3.605<\sqrt{13}<3.606), (1.732<\sqrt3<1.733), and (1.737<\alpha<1.738). These imply **(R_V<11/5) and (R_H>3)**. Traversing each triangle twice gives a nominal six-vertex list whose products satisfy **(R_V^2<121/25)** and **(R_H^2>9)**. This is an exact counterexample to admitting doubled odd periods as primitive (N=6) orbits. It supports, rather than contradicts, the submission's explicit exclusion.

Boundary checks cover the absence of an integer (0<\tau<N/2) for (N=2), the zero-shift coincident caustic, the (v=K) axes-formula singularity, (k=1) degenerate minor caustic axis, and the separately trivial (k=0) circle. Near-boundary admissible cases are also tested numerically below. No assertion is made for hyperbolic caustics.

## 6. Independent reflected-ray diagnostics

After Jacobi functions bootstrap axes for each desired rational rotation, the iteration uses only ordinary conic geometry: a tangent contact point on the caustic, the other intersection of a line with the outer ellipse, and Euclidean specular reflection. All focal distances are computed directly as square roots of Cartesian squared distances; neither the submitted paired-product formula nor its cyclic norm is used to obtain these products.

At **100 digits**, **560 full reflected orbits** cover **112 modulus/period/turning combinations**, five phases each, (k\in\{0.01,0.2,0.75,0.999999\}), and (N\in\{6,10,14,18,22,30,34,102\}). All primitive positive turning numbers are used up to (N=34); (N=102) uses (\tau=1,49). Both simple and primitive star paths are included. Checks require closure, the claimed turning number, antipodal half-period vertices, caustic tangency, equality of the two direct focal products, and phase constancy.

| Diagnostic | Maximum error |
| --- | ---: |
| Closure, normalized by (a) | (2.484090676\times10^{-94}) |
| Antipodal pairing, normalized by (a) | (2.922286152\times10^{-94}) |
| Normalized caustic tangency | (2.471307548\times10^{-100}) |
| Turning number | (3.956199398\times10^{-95}) |
| Difference of logs of the two focal products | (2.778847405\times10^{-92}) |
| Phase variation of log focal product | (7.663750575\times10^{-93}) |

These are numerical diagnostics with a (10^{-70}) tolerance. They independently test geometric behavior of sampled families, including extreme eccentricity and high-turning stars. They are not validated interval computations or universal proofs. In particular, a shared axis construction is still an input; ray closure supplies selected-case support for it.

## 7. Strongest result and exact remaining gap

The advertised replay totals are reproduced; **355,864 new exact assertions** pass. The ordinary-distance normalization and subgroup/coset classification above are independently justified elementary deductions. Several admissible and excluded individual billiards are exactly verified, including substantive excluded-scope counterexamples. Actual reflected paths support the proposed theorem numerically throughout the tested families.

The universal focal-product theorem still requires independently checking the published canonical parametrization, Jacobi periods/poles/shifts, and the complete analytic divisor argument. This audit does not certify those sources or priority. It found **no substantive defect in the scoped computational claims**. Promotion of the theorem should rely on the separate analytic/source audits in addition to these artifacts.

Audit work completion: **100%** for the assigned reproduction/counterexample family. Discovery certainty is not assigned a numerical probability; the remaining universal analytic/source gap is expressly retained.
