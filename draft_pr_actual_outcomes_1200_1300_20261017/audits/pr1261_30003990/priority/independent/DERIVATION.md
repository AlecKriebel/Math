# Checkable deduction from older ingredients

Date of assembly: 2026-10-17 UTC. This is a deduction assembled during this audit, after reading the original bounded AUDIT.md. It is not evidence that any cited author stated, discovered, or disclosed the target theorem. It uses a different existing endpoint kernel theorem from the elementary Dirichlet-power construction summarized in that audit. Independent adversarial checking of this deduction remains a later step for the parent audit.

## Exact target

For a fixed compact convex \(K\subset\mathbb R^d\), \(d\ge1\), with nonempty interior, and a fixed real polynomial \(f\), put
\[
H_r=\inf\{\int_K f q\,dx:q\in\Sigma[x],\ \deg q\le2r,\ \int_Kq\,dx=1\}.
\]
The claim is \(0\le H_r-\min_K f\le C_{K,f}/r^2\) for every integer \(r\ge1\), with one real global square as a witness. No computable minimizer, dimension-free constant, arbitrary reference measure, or restriction to \(q=s(f)\) is asserted.

## Prior theorem actually used

[Totik–Varga 2012, Theorem 2.1](https://doi.org/10.1016/j.jmaa.2012.03.006), retained S08, PDF p.2 / printed p.379, gives degree-\(m\) polynomials \(P_{m,a}\) under conditions on an increasing nonnegative function \(\psi\). The statement and its functional argument were checked in the rendered page, and the proof on PDF pp.3–4 was read.

Choose \(\psi(v)=\sqrt v\). Every hypothesis is satisfied:
\(\psi(0+)=0\), \(\psi(v)=\sqrt2\psi(v/2)\), and
\(\int_1^\infty\psi(v)v^{-2}dv=2<\infty\).
Choose their parameter \(a=0\), an allowed endpoint of \([0,1/2]\).
There are constants \(A,c>0\), fixed independently of \(m\), and real polynomials \(P_m\) with
\[
\deg P_m\le m,\quad P_m(0)=1,\quad
|P_m(t)|\le2\quad(0\le t\le1),\qquad
|P_m(t)|\le A e^{-c(m^2t)^{1/4}}\quad(0<t\le1).
\]
Indeed the argument of \(\psi\) in the printed theorem is \(m|t|/(\sqrt{|t|}+\sqrt a)\), which becomes \(m\sqrt t\). If the polynomial-field convention were uncertain, its real part has the same value at zero and the same bounds, so a real choice suffices.

The use below is of Theorem 2.1, which has no measure hypothesis. It does **not** invoke Theorem 4.1 on zero spacing and does not assume that an endpoint growth bound implies doubling on every interval.

## Scalar lemma with every measure hypothesis exposed

Let \(\nu\) be a finite, nonzero positive Borel measure supported in \([0,1]\). Write \(F(t)=\nu([0,t])\) for \(t>0\), including \(t>1\). Assume that some fixed \(s\ge0\) satisfies
\[
 F(t)\le(t/h)^sF(h)\quad(0<h\le t).
\tag{G}
\]
This implies \(F(h)\ge h^sF(1)>0\) for \(h\le1\).

Markov's inequality on \([0,1]\) gives
\(\|P_m'\|_\infty\le2m^2\|P_m\|_\infty\le4m^2\).
The precise interval form is printed in [Slot–Laurent, Lemma 11, PDF p.18](https://arxiv.org/pdf/1905.08142v2), retained S02.
Thus, for \(h_m=1/(8m^2)\), \(P_m(t)\ge1/2\) on \([0,h_m]\). In particular
\[
 Z_m=\int P_m^2\,d\nu\ge\tfrac14 F(h_m)>0.
\tag{D}
\]
The core contributes at most \(4h_mF(h_m)\) to \(\int tP_m^2d\nu\).

For \(E_j=\{2^jh_m<t\le2^{j+1}h_m\}\), \(j\ge0\), the endpoint kernel and (G) give
\[
 \int_{E_j}tP_m(t)^2d\nu(t)
 \le A^2 2^{s+1}h_mF(h_m)
       2^{(s+1)j}\exp[-2c(2^j/8)^{1/4}].
\]
Empty shells cause no issue. For large \(j\), support in \([0,1]\) makes them empty, but extending the nonnegative bound to all \(j\ge0\) is valid. The series
\[
 S_{s,c}=\sum_{j\ge0}2^{(s+1)j}\exp[-2c(2^j/8)^{1/4}]
\]
is finite: its consecutive-term ratio tends to zero, since the negative exponential increment is a positive constant times \(2^{j/4}\), while the power-of-two ratio is fixed.

With \(B_{s,A,c}=4+A^2 2^{s+1}S_{s,c}<\infty\), (D) yields
\[
 \frac{\int tP_m^2d\nu}{\int P_m^2d\nu}
 \le 4B_{s,A,c}h_m=\frac{B_{s,A,c}}{2m^2}.
\tag{R}
\]
This is a complete normalized first-moment bound. An upper estimate for a Christoffel function alone would not have proved (R).

## Verify (G) for the target

Choose a global minimizer \(z\in K\). Let
\[
 H=\max_K\|\nabla^2f\|_{\rm op},\quad
 \gamma=1+H/2,\quad
 g(x)=\nabla f(z)\cdot(x-z)+\gamma\|x-z\|^2.
\]
For every \(x\in K\), the right derivative of \(u\mapsto f(z+u(x-z))\) at zero is nonnegative, so
\(\ell(x):=\nabla f(z)\cdot(x-z)\ge0\).
Taylor's theorem along the segment in \(K\) gives
\(0\le f(x)-f(z)\le g(x)\).
This quadratic upper-proxy reduction is already explicit in [de Klerk–Laurent 2017 preprint, Corollary 4.3, PDF pp.7–8](https://arxiv.org/pdf/1703.00744), S12, and in S02 Lemmas 1 and 4. The added \(1\) merely ensures strict positivity away from \(z\) in degenerate cases.

Let \(G=\max_Kg\). Full dimension and \(\gamma>0\) imply \(G>0\); set \(u=g/G\), so \(0\le u\le1\) on \(K\) and \(\deg u\le2\). Take \(\nu=u_\#(dx|_K)\), a finite nonzero positive Borel measure supported in \([0,1]\). For \(\alpha\in[0,1]\),
\[
 g(z+\alpha(x-z))=\alpha\ell(x)+\alpha^2\gamma\|x-z\|^2
 \le\alpha g(x).
\]
Hence for \(0<h\le t\), the homothety
\(x\mapsto z+(h/t)(x-z)\) injects \(\{u\le t\}\cap K\) into \(\{u\le h\}\cap K\), with Jacobian \((h/t)^d\). This proves (G) with \(s=d\), including \(t>1\). No smoothness or semialgebraicity of \(K\) and no density formula for \(\nu\) is needed.

For \(r\ge2\) choose \(m=\lfloor r/2\rfloor\). Then
\[
 q_r(x)=\frac{P_m(u(x))^2}{\int_KP_m(u)^2dx}
\]
is one real global square with unit mass. Its square root has degree at most \(2m\le r\), so \(\deg q_r\le2r\). Positivity of \(u\) outside \(K\) is irrelevant. Since \(m\ge r/3\),
\[
0\le H_r-f(z)\le
 G\frac{\int tP_m^2d\nu}{\int P_m^2d\nu}
 \le \frac{9GB_{d,A,c}}{2r^2}.
\]
For \(r=1\), the constant density \(1/\operatorname{vol}K\) has error at most \(G\). Enlarging the constant proves the exact all-integer target.

## Priority consequence and limitation

The implication above verifies every external theorem hypothesis and each category interface. It establishes a **now-assembled deduction from older printed ingredients**, not a found earlier explicit printed resolution of OWR-16633-006. Totik–Varga already use relative shell mass against local core mass in their Christoffel proof (PDF pp.7–9). Thus a broad claim that endpoint localization or relative-mass shell cancellation is a new method is not supported.

No historical discovery date, transmission, priority, or current worldwide open status follows from this implication. A new consequence of older results can still be a mathematical contribution; determining how that consequence was previously stated or used requires historical evidence.

