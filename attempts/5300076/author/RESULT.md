# Power-law interval lifts: proved controls and the remaining convergence gap

Problem 5300076 / AMR-052-0076; queue rank 649. Author-stage status: **unsolved**, five substantive approaches. Date: 2026-10-04. This is an authored mathematical analysis, not a claimed resolution or novelty assertion. Independent audit is pending.

## 1. The two sequences must be distinguished

Fix a real number \(\alpha>1\), put \(\beta=1/\alpha\), and set
\[
 P_k(x)=k(1-|2x-1|^\alpha),\qquad 0<k\leq1.
\]
Work with continuous strictly unimodal maps \(f:[0,1]\to[0,1]\) having a unique turning point \(c\in(0,1)\), increasing on \([0,c]\), decreasing on \([c,1]\), and \(f(0)=f(1)=0\). These hypotheses ensure the following lift is a homeomorphism; maps with flat intervals would require an additional convention.

Write \(k=f(c)\). The increasing homeomorphism solving \(P_k\circ h=f\) is
\[
 h(x)=\begin{cases}
 \frac{1-(1-f(x)/k)^\beta}{2},&x\leq c,\\
 \frac{1+(1-f(x)/k)^\beta}{2},&x\geq c.
 \end{cases}                                                    \tag{1}
\]
Define \(f_{n+1}=h_n\circ P_{k_n}=h_n\circ f_n\circ h_n^{-1}\),
where \(k_n=f_n(c_n)\). Each new critical point is \(c_{n+1}=1/2\), and
\[
 k_{n+1}=h_n(k_n).                                                \tag{2}
\]
There are distinct possible conclusions:

* **Lift convergence:** \(P_{k_n}\) converges uniformly. This is exactly the scalar assertion that \(k_n\) converges, because \(\|P_k-P_l\|_\infty=|k-l|\).
* **Conjugated-map convergence:** \(f_n\) converges, for example uniformly.
* **Common-limit convergence:** both sequences converge to the same member of the lift family.

The 1990 primary source, §3 on printed pp. 8–9, first gives a polynomial theorem about the lift sequence, separately discusses experimental convergence of the conjugated maps, and then asks Question 2 for the power-law family. It does not assign a topology or explicitly identify the output sequence in that final question. Accordingly, this packet treats lift convergence for the full requested kneading class as the unresolved target. Section 6 disproves the stronger universal conjugated-map assertion under the stated interval-map regularity. That result is not relabeled as a resolution of the lift question.

Periodic or eventually periodic kneading is symbolic information. It does **not** imply that the critical orbit is a finite set. For example, \(f(x)=x(1-x)=P_{1/4}(x)\) for \(\alpha=2\) has critical point \(1/2\), and its critical value and all subsequent iterates lie strictly between 0 and \(1/2\). Its kneading itinerary is constant left, but its critical orbit decreases strictly to 0 and never reaches 0. The algorithm is stationary for this example because the initial map already belongs to the lifting family. It nevertheless disproves the proposed implication from periodic symbolic data to critical finiteness.

## 2. Exact finite critical-orbit pullback

Suppose the critical orbit really is finite. Include it, the critical point, and the two endpoints in an ordered marked set, and let \(\sigma\) describe the forward image of each label. From step 1 onward the critical label \(d\) is located at \(x_d=1/2\). Write \(v=\sigma(d)\), so \(k=x_v\), and let \(s_i=-1\) for labels left of \(d\) and \(s_i=+1\) for labels right of \(d\). The marked-point update induced by (1) is
\[
 y_d=1/2,\qquad
 y_i=\frac{1+s_i(1-x_{\sigma(i)}/x_v)^\beta}{2}\quad(i\ne d).       \tag{3}
\]
In particular endpoints remain 0 and 1. These are the coordinates of the conjugacy images of the old marked points; the new dynamics has the same label map \(\sigma\). Formula (3), rather than arbitrary choices of signs in an inverse-root iteration, is the reproducible finite algorithm used here.

All image labels have coordinates at most \(x_v\). Order within each lap, and the reversed order of image labels in the decreasing lap, show that the formula preserves the strict order of the marked points. A finite critical orbit cannot have \(k<1/2\): if it did, strict increase on the left lap would give \(0<f(k)<k\), and repeated left-lap iteration would be strictly decreasing and positive, contradicting finiteness. Thus the finite configurations relevant here have \(k\geq1/2\).

Formula (3) reduces an actually finite orbit to finitely many variables, but does not prove convergence. A compact closure can contain collisions of distinct marked points; an existence argument for a fixed point would not show that every starting point approaches it. In particular, no global Euclidean contraction follows from taking roots: a coordinate derivative with respect to an image value has magnitude
\[
 \frac{\beta}{2k}(1-x_{\sigma(i)}/k)^{\beta-1},                    \tag{4}
\]
which is unbounded as that image approaches the critical value. Section 3 shows this obstruction even in a case which does converge in a better metric.

A useful conditional criterion is the following. If a continuous update \(T\) has a fixed point \(x_*\), strictly decreases the distance to \(x_*\) away from \(x_*\), and the forward orbit of \(x\) has compact closure in its metric domain, then \(T^n x\to x_*\). Indeed, the nonincreasing distances tend to \(L\). If \(L>0\), choose a convergent subsequence \(T^{n_j}x\to y\). Continuity gives \(d(y,x_*)=d(Ty,x_*)=L\), contrary to strict decrease. If \(L=0\), convergence is immediate. For (3), the missing inputs are precisely an appropriate global metric/decrease assertion, a fixed point in the relevant domain, and control of boundary degeneration. None is assumed in this packet.

## 3. Complete lift convergence for critical periods one and two

### Fixed critical point

If \(f_0(c_0)=c_0\), then (2) and \(h_0(c_0)=1/2\) give \(k_1=1/2\). Conjugacy preserves critical fixedness, so \(k_n=1/2\) for every \(n\geq1\). Therefore all subsequent lifts are exactly \(P_{1/2}\). This says nothing by itself about convergence of \(f_n\).

### Exact period two

Assume \(c_0\) has exact period two under \(f_0\). At every step \(n\geq1\), the critical point is \(1/2\), its critical value satisfies \(k_n>1/2\), and \(f_n(k_n)=1/2\). The inequality follows because a left-lap point \(k_n<1/2\) would satisfy \(f_n(k_n)<f_n(1/2)=k_n\), while \(k_n=1/2\) has period one. Also \(k_n<1\), because \(f_n(1)=0\).

Using the right branch in (1),
\[
 k_{n+1}=G_\alpha(k_n):=\frac{1+(1-1/(2k_n))^{1/\alpha}}2.         \tag{5}
\]
Set \(t_n=2k_n-1\in(0,1)\) and \(q_n=-\log t_n\in(0,\infty)\). Then
\[
 t_{n+1}=\left(\frac{t_n}{1+t_n}\right)^{1/\alpha},\qquad
 q_{n+1}=H_\alpha(q_n):=\frac{\log(1+e^{q_n})}{\alpha}.             \tag{6}
\]
The function \(H_\alpha\) maps the complete metric space \([0,\infty)\) into itself and
\[
 0<H'_\alpha(q)=\frac{e^q}{\alpha(1+e^q)}<1/\alpha<1.
\]
The mean value theorem therefore gives a global Lipschitz constant \(1/\alpha\). The contraction theorem yields a unique fixed point \(q_*\) and
\[
 |q_n-q_*|\leq\alpha^{-(n-1)}|q_1-q_*|\quad(n\geq1).              \tag{7}
\]
Writing \(t_*=e^{-q_*}\) and \(k_*=(1+t_*)/2\), the same fixed point is uniquely specified by
\[
 t_*^{\alpha-1}(1+t_*)=1,\qquad0<t_*<1.                           \tag{8}
\]
Uniqueness in (8) also follows directly because its left side is strictly increasing from 0 to 2. Consequently \(P_{k_n}\to P_{k_*}\) uniformly, with
\[
 \|P_{k_n}-P_{k_*}\|_\infty\leq\tfrac12\alpha^{-(n-1)}|q_1-q_*|.
\]
For \(\alpha=2\), \(t_*=(\sqrt5-1)/2\). The convergence proof is valid for every real \(\alpha>1\), not just sampled exponents.

In contrast, differentiating (5) gives
\[
 G'_\alpha(k)=\frac{\beta}{4k^2}(1-1/(2k))^{\beta-1}\longrightarrow+\infty
 \quad(k\downarrow1/2).
\]
Thus a global Euclidean-Lipschitz argument is genuinely unavailable even on this solved one-dimensional subsystem. The logarithmic coordinate is essential to this proof, and no multivariable extension of its contraction estimate is supplied.

### Endpoint-preperiodic control

If the critical value is 1, the critical orbit is \(c\mapsto1\mapsto0\mapsto0\). Since \(h_n(1)=1\), all \(k_n=1\) and all lifts are \(P_1\). This is a second exact, strictly preperiodic control; it does not cover general preperiodic itineraries.

## 4. Why direct polynomial continuation is insufficient

The even-integer case is the classical polynomial setting. A single-valued holomorphic function on a neighborhood of 0 cannot restrict to \(|u|^\alpha\) on a two-sided real interval unless \(\alpha\) is an even integer. To see this, take its first nonzero Taylor coefficient, of integer order \(m\). On positive reals, matching the leading asymptotic forces \(m=\alpha\) and that coefficient to be 1. Matching on negative reals then forces \((-1)^m=1\). This rules out the naive substitution of a noninteger local degree into the same holomorphic-polynomial proof. It does not rule out a different geometric construction.

There is an exact affine coordinate relation with the common alternative family. For fixed \(k\), put \(b=(2k)^{1/(\alpha-1)}\) and \(u=b(2x-1)\). Then
\[
 u\circ P_k\circ u^{-1}(z)=a-|z|^\alpha,\qquad a=b(2k-1).         \tag{9}
\]
The affine change depends on \(k\), so comparing iterations in these two normalizations requires carrying the changing normalization along with the marked points. Equation (9) does not turn a theorem on monotonicity of \(a\)-parameters into a theorem about convergence of the sequence (2).

## 5. Local attraction and exponent approximation do not settle the target

The May 2026 manuscript of Benedicks and Rodrigues introduces a finite critical-orbit inverse-root operator, studies a proposed Teichmüller contraction for certain rational exponents, and states kneading/entropy monotonicity results. The conclusion needed here is stronger and different: global convergence of the normalized real lift sequence from every allowed initial interval map, including symbolic eventual periodicity without critical finiteness. No theorem with those quantifiers was found in the inspected manuscript. This packet does not independently certify or refute its proposed geometric construction.

Even a verified derivative bound \(\rho(DT(x_*))<1\) establishes local attraction at an existing fixed point, not global attraction from all initial configurations. And convergence for approximating exponents cannot be passed to their limit using finite-time continuity alone. A precise countercontrol is the continuous family of self-maps of \([-1,1]\)
\[
 R_\varepsilon(x)=-(1-\varepsilon)x,\quad0\leq\varepsilon\leq1.
\]
For every \(\varepsilon>0\), every orbit tends to 0. At \(\varepsilon=0\), the orbit of any nonzero point alternates. Nevertheless, \(R_\varepsilon\to R_0\) uniformly and every fixed finite iterate depends continuously on \(\varepsilon\). This countercontrol is not a power-law counterexample. It isolates the missing uniform-in-time estimate in an exponent-continuation route.

Levin, Shen and van Strien's 2020 work supplies a local transfer-operator framework and explicitly records a general noninteger lifting-property gap, together with restricted large-exponent results. Bonifant, Milnor and Sutherland's polynomial work imposes combinatorial conditions and treats collision phenomena separately. Neither inspected result has been promoted here to a general noninteger power-law convergence theorem.

## 6. Explicit conjugated-map two-cycles for every lifting exponent

This section proves a negative result for the stronger \(f_n\)-convergence assertion. The lift sequence remains constant, so there is no contradiction with a lift-convergence theorem.

Fix \(\alpha>1\) and set \(\omega=\pi/\log\alpha\). Choose \(\varepsilon>0\) and \(A>\varepsilon\sqrt{1+\omega^2}\). For \(s>0\), define
\[
 L_\theta(s)=s\{A+\varepsilon\sin(\omega\log s+\theta)\},
 \qquad
 g_\theta(t)=\exp[-L_\theta(-\log t)]\quad(0<t<1),                \tag{10}
\]
with \(g_\theta(0)=0\), \(g_\theta(1)=1\). The bounds
\((A-\varepsilon)s\leq L_\theta(s)\leq(A+\varepsilon)s\)
prove continuity at both endpoints. Moreover,
\[
 L'_\theta(s)=A+\varepsilon\sin(\omega\log s+\theta)
                 +\varepsilon\omega\cos(\omega\log s+\theta)>0.
\]
Thus \(g_\theta\) is an increasing homeomorphism of \([0,1]\).

Define
\[
 f_\theta(x)=\frac{1-g_\theta(|2x-1|)}2.                          \tag{11}
\]
It is continuous, strictly increasing then strictly decreasing, maps both endpoints to 0, and has a fixed critical point \(1/2\). Its critical-value kneading sequence is constant critical. Its chosen lift is always \(P_{1/2}\).

For an arbitrary increasing homeomorphism \(g\), substituting (11) in (1) and evaluating \(h\circ P_{1/2}\) shows that the induced transformation on \(g\) is
\[
 (\mathcal U_\alpha g)(t)=g(t^\alpha)^{1/\alpha}.                 \tag{12}
\]
Indeed, in centered coordinate \(u=2x-1\), the interval map is \(-g(|u|)\), the lift is \(-|u|^\alpha\), and the increasing lifting homeomorphism is
\(H(u)=\operatorname{sgn}(u)g(|u|)^{1/\alpha}\). Its composition with the lift is \(-g(|u|^\alpha)^{1/\alpha}\), proving (12).

Because \(\omega\log\alpha=\pi\), (10) gives
\[
 \alpha^{-1}L_\theta(\alpha s)=L_{\theta+\pi}(s).
\]
Consequently \(\mathcal U_\alpha g_\theta=g_{\theta+\pi}\) and
\(\mathcal U_\alpha^2g_\theta=g_\theta\). These are nontrivial two-cycles: for \(\theta=0\), take
\[
 s_0=\exp(\pi/(2\omega))=\sqrt\alpha,\qquad t_0=e^{-s_0}.
\]
Then \(g_0(t_0)=e^{-s_0(A+\varepsilon)}\) and
\(g_\pi(t_0)=e^{-s_0(A-\varepsilon)}\), which differ. At
\(x_0=(1+t_0)/2\), the maps \(f_0\) and \(f_\pi\) therefore differ by the positive amount
\[
 \tfrac12e^{-s_0A}(e^{s_0\varepsilon}-e^{-s_0\varepsilon}).       \tag{13}
\]
The full sequence \(f_n\) alternates between these two maps and does not converge even pointwise at \(x_0\), although it is postcritically finite and every lift is exactly \(P_{1/2}\). This proof is analytic; numerical controls are only implementation checks.

There is an even simpler common-limit obstruction. Choosing \(g(t)=t^\gamma\), \(\gamma>0\), makes (12) stationary. Thus \(f(x)=(1-|2x-1|^\gamma)/2\) is fixed by the tower transformation for every \(\alpha>1\). Unless \(\gamma=\alpha\), its constant sequence does not equal the constant lift sequence. This also demonstrates why invariant kneading data do not force a unique full-map representative.

No smoothness at the interval endpoints is asserted for the two-cycle examples (10). Their continuity and strict unimodality match the explicitly stated class. If stronger endpoint or global smoothness is required, that is a materially different hypothesis and this exact example should not silently be used to address it. The fixed power-law example alone may have greater regularity, but it only refutes common-limit convergence, not convergence of \(f_n\) itself.

## 7. Exact residual target and limits

The remaining lift question asks whether \(k_n\) converges for every fixed real \(\alpha>1\) and every admissible starting map with periodic or eventually periodic kneading. The finite-orbit case beyond the controlled periods is not proved here; the broader symbolic class cannot be replaced by it. The all-exponent period-two contraction, finite pullback formula, and explicit full-map two-cycles are the strongest self-contained conclusions of this attempt.

Recommended queue disposition is **unsolved, 5/5**. The stronger full-map claim has a rigorous counterexample, but the primary source's polynomial theorem and wording make it unsafe to declare the whole imported entry solved on that interpretation alone. Historical novelty of the elementary constructions is unestablished. No human peer review is claimed.

## References

1. B. Bielefeld (editor), *Conformal Dynamics Problem List* (1990), §3, printed pp. 8–9. https://arxiv.org/abs/math/9201271
2. A. Bonifant, J. Milnor, S. Sutherland, *The W. Thurston Algorithm Applied to Real Polynomial Maps*, Conformal Geometry and Dynamics 25 (2021), 179–199; §§2, 4 and Appendix B. https://arxiv.org/abs/2005.07800
3. G. Levin, W. Shen, S. van Strien, *Positive Transversality via transfer operators and holomorphic motions with applications to monotonicity for interval maps*, Nonlinearity 33 (2020), 3970–4012; §2.9 and Appendix A. https://arxiv.org/abs/1902.06732
4. M. Benedicks, A. Rodrigues, *Topological Entropy for Power-Law Unimodal Maps*, arXiv:2605.12238v1 (2026); §§2–4. https://arxiv.org/abs/2605.12238v1
5. G. Tiozzo, *Metrics on trees I. The tower algorithm for interval maps*, arXiv:2112.02398; §1, §5, and Appendix Theorem 5.4. Its constant-slope counterexamples concern a different lifting family, while its appendix carefully separates polynomial lifts from conjugated maps. https://arxiv.org/abs/2112.02398
