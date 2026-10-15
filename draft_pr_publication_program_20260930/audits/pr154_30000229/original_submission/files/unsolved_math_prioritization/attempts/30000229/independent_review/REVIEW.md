# Independent adversarial review: 30000229 / OWR-829-001

**Verdict: PASS_COMPLETE_ENDPOINT_COUNTEREXAMPLE. No mandatory mathematical correction.**

The candidate supplies an actual lower bound for best piecewise-constant \(H^{-1}\) approximation, uniformly over every admissible conforming newest-vertex-bisection mesh. It does not infer that conclusion merely from a data estimator. The endpoint \(s=1/2\) is explicitly included in the original conjecture, so this gives a complete negative answer to its universal implication.

Reviewed snapshot: SHA-256 **dfe3713adae5e5beda588087f3b3e0c4f2c3e809749aee3330730edf8b5cb705**.

All **3,890** submitted exact assertions reproduced with a byte-identical receipt. An independent standard-library implementation passed **4,542** exact controls. The credited Cohen–DeVore–Nochetto construction and mesh theorems remain substantive prior inputs. Historical priority and human peer review are not established.

## 1. Exact source and admissible setting

I read the complete relevant Stevenson contribution in [OWR 24/2005](https://ems.press/content/serial-article-files/45998?nt=1), printed pp.1306–1307, and visually inspected the rendered concluding page. It specifies two-dimensional Poisson, linear finite elements and newest vertex bisection. Its final paragraph conjectures existence of piecewise-constant data approximants at rate \(n^{-s}\) for \(s\in(0,1/2]\) whenever \(u\in A^s\). It then distinguishes that existence statement from an algorithm that constructs the approximants.

The same paragraph expressly discusses \(f\in H^{-1}(\Omega)\) outside \(L^2(\Omega)\). The candidate therefore does not evade an \(L^2\) hypothesis by choosing distributional data. A failure at the included endpoint refutes the universal assertion; no failure at every subcritical exponent is needed.

The adopted dual norm is the dual of the gradient norm on \(H^1_0\). This is the natural Poisson energy norm. Replacing it by an equivalent full Sobolev norm on the fixed square would not change the rate conclusion.

I also read the full relevant parts of [Cohen–DeVore–Nochetto's author manuscript](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf): §2 for compatible NVB labels, completion and overlay, §6.2 for edge distributions, and §6.4 for the endpoint construction. The latter explicitly concerns its localized data estimator. The candidate correctly proves an additional annihilation argument rather than identifying that estimator with best \(P_0\) approximation.

## 2. The decisive mean-zero bubble bridge

On a triangle \(K\) incident to edge \(e=AB\), write
\[
\psi_e=4\lambda_A\lambda_B-20\lambda_A\lambda_B\lambda_C.
\]
The exact barycentric integration formulas give
\[
\int_K4\lambda_A\lambda_B=|K|/3
=\int_K20\lambda_A\lambda_B\lambda_C.
\]
Consequently \(\int_K\psi_e=0\). On \(e\), its trace is \(4\lambda_A\lambda_B\); on the other two edges it vanishes.

The two definitions on the adjacent triangles agree along \(e\), regardless of their respective third vertices. Extension by zero is continuous across all other supporting edges and has zero boundary trace. Thus \(\psi_e\in H^1_0(\Omega)\), including when an endpoint of the interior edge lies on the domain boundary. Its edge integral is \((2/3)|e|\).

Affine scaling in dimension two bounds its gradient norm by a constant depending only on shape regularity. NVB supplies that uniform shape regularity throughout the entire mesh family. The norm is not allowed to deteriorate with the smallest edge length.

For the edge distribution \(S=\sum_eJ_e\delta_e\), choose
\[
v=\sum_{e\in E_*}J_e|e|\psi_e.
\]
Every triangle meets at most three selected edge bubbles. Hence
\[
\|\nabla v\|^2\le 3C_b\sum_{e\in E_*}J_e^2|e|^2.
\]
Every \(g\in P_0(T)\), with arbitrary real coefficients, satisfies \(\int gv=0\) element by element. Traces on unselected edges vanish, so
\[
\langle S-g,v\rangle=\frac23\sum_{e\in E_*}J_e^2|e|^2.
\]
If the sum is nonzero, division by the gradient bound proves the claimed dual lower bound; if it is zero, the inequality is trivial.

This verifies the essential bridge to **best** \(H^{-1}\) error. Neither a bound on the coefficients of \(g\) nor a sign condition on the jumps is required. Cancellation between different edge distributions does not invalidate the chosen dual test.

## 3. Admissibility and approximation of the solution

The dyadic squares
\[
Q_j=[2^{-j},2^{1-j}]\times[0,2^{-j}]
\]
have disjoint interiors and lie in the closed unit square. Their scaled center hats vanish along each supporting square boundary, so their zero extensions belong to \(H^1_0(\Omega)\), even where those boundaries meet \(\partial\Omega\).

At level \(j\), there are \(4^j\) hats, each with amplitude \(4^{-j}\) and squared energy norm \(4\). Their supports have disjoint interiors. Orthogonality of their gradients therefore gives
\[
\|\nabla u\|^2=4\sum_{j\ge1}4^{-j}=4/3,\qquad
\|\nabla(u-V_n)\|^2=\frac43\,4^{-n}.
\]
This proves convergence in the actual energy space, not merely pointwise convergence of a formal series. Defining \(f=-\Delta u\) weakly yields \(f\in H^{-1}\), and the Dirichlet Laplacian is an isometry for this choice of dual norm. Formula (5)'s exact tail follows.

The initial four-triangle square pattern and the specified edge labels satisfy the cited compatibility condition. The construction uses genuine NVB refinements. Reaching a dyadic square of generation \(j\) takes \(O(j)\) local bisections. Filling it with \(4^j\) base patterns takes \(O(4^j)\). One direct count uses two uniform NVB generations per dyadic subdivision: \(4\) triangles become \(16\), and after \(j\) such subdivisions there are \(4\cdot4^j\) triangles, requiring \(4(4^j-1)\) bisections. This supplies a valid explicit bound without relying on an exact leading constant in the source's informal fill count.

Summing these costs through \(n\), then applying the cited linear-complexity conforming completion, gives \(\#T_n\le C_0 4^n\), with \(V_n\) continuous piecewise linear on \(T_n\). Monotonicity of best error between successive geometric budgets gives \(u\in A^{1/2}\). For Poisson, the Galerkin energy projection realizes the best approximation in each finite element space.

## 4. The all-mesh lower bound

The lower-bound quantifier is correctly ordered: first fix an arbitrary admissible \(T\) with \(\#T\le4^n\), then take the common refinement
\[
T^*=T\oplus T_n.
\]
The NVB forest overlay is conforming and satisfies
\[
\#T^*\le\#T+\#T_n-\#T_0\le C_1 4^n.
\]
Every original \(P_0(T)\) function is still piecewise constant on \(T^*\). Meanwhile \(V_n\) is affine on its triangles, so \(-\Delta V_n\) consists entirely of constant interior-edge jump distributions. Boundary terms vanish against \(H^1_0\).

The selected center-to-lower-left-corner segment in each small square has length \(h_j/\sqrt2\). The unscaled center hat has gradient jump \(2\sqrt2/h_j\); multiplying by its amplitude \(h_j=4^{-j}\) gives jump magnitude \(2\sqrt2\). Hence its absolute jump times its length is exactly \(2\,4^{-j}\).

No other hat changes this jump on the segment interior. The proof does not need to assert that all other jumps vanish. The selected segments have disjoint interiors, and each is a union of fine edges of \(T^*\), even if completion already subdivided it.

If \(m_\sigma\) counts its fine edges, the first Cauchy–Schwarz estimate gives
\[
\sum_{e\subset\sigma}J_e^2|e|^2
\ge \frac{J_\sigma^2|\sigma|^2}{m_\sigma}.
\]
Distinct selected segments use distinct fine edges, so
\[
\sum_\sigma m_\sigma\le\#\mathrm{edges}(T^*)\le3\#T^*.
\]
Each of the \(n\) levels contributes exactly \(2\) to
\(\sum_\sigma |J_\sigma||\sigma|\). A second Cauchy–Schwarz estimate therefore yields
\[
\sum_{\text{selected fine }e}J_e^2|e|^2
\ge c\,n^2 4^{-n}.
\]
All constants depend only on the initial shape-regular mesh and the fixed domain, not on \(n\), \(T\), or \(g\).

Applying the mean-zero bubble lemma on \(T^*\), then subtracting the exact \(H^{-1}\) tail, gives
\[
\|f-g\|_{H^{-1}}
\ge (c_2n-2/\sqrt3)\,2^{-n}
\]
for **every** original \(g\in P_0(T)\). Taking both infima is therefore valid. Multiplication by \(\sqrt{4^n}\) leaves a quantity diverging linearly in \(n\), which disproves the required \(O(N^{-1/2})\) rate.

The argument is not restricted to the approximating meshes \(T_n\) used for \(u\); it defeats every admissible mesh of the data budget. It makes no claim about unrestricted anisotropic triangulations. If a convention permits nonconforming NVB partitions before completion, the same negative rate conclusion follows by linear-cost conforming completion and a constant rescaling of the budget.

## 5. Exact controls, prior work and verdict

The submitted verifier was replayed beside an unchanged copied snapshot; all 3,890 assertions pass and its receipt is byte-identical.

The independent checker integrates polynomial coefficients by exact factorial formulas, checks traces and the full three-bubble energy Gram matrix, verifies two-dimensional affine scale invariance, constructs labelled NVB children through four dyadic generations, and checks the multiscale energy/cost formulas. It also verifies a sum-of-squares form of the allocation inequality. All 4,542 assertions pass using Python's standard library. These controls supplement the uniform functional-analytic proof; no finite set of meshes is presented as a substitute for it.

Recommend **claimed_solved, 2/5** for the original universal implication, with the endpoint-only conclusion stated prominently. No mandatory mathematical correction is required.

The solution construction, its endpoint motivation, and the mesh-complexity inputs are explicitly credited to Cohen–DeVore–Nochetto. Their paper also discusses why older data-approximation assumptions do not follow automatically from solution approximation. This review certifies the written bridge and resulting negative answer; it does not certify that the deduction is historically new.

Preserve the distinctions between estimator and best approximation, existence and algorithm construction, the endpoint and subcritical exponents, and general \(H^{-1}\) data versus \(L^2\) data. The report is separate adversarial AI review, not human peer review.

