# An exact scalar reduction and a sharp three-equilibrium bound for four sites

**Target:** 30003741 / OWR-15993-009.  
**Status:** scoped partial result, original higher-multiplicity question unresolved after two approaches; separate adversarial review pending. No historical-priority, dynamical-stability, or physiological claim.

## 1. Exact source and model

The complete [OWR contribution, printed pp.487–489](https://ems.press/content/serial-article-files/46732), asks whether more than three steady states can occur. Its discussion uses one ligand amount L and dissociation rate \(\nu\), together with the agonist response formula and three-state result from [Rendall–Sontag (2017)](https://www.sontaglab.org/FTPDIR/2017_rendall_sontag_tcells_royal_open_reprint.pdf). That paper treats two ligands generally, but its Theorem 3.1 and subsequent higher-N count question concern the **agonist-only restriction**.

We preserve that narrower interpretation rather than silently introducing a second ligand. The OWR prose does not repeat all model hypotheses, so this distinction remains a source qualification. Below, \(N\ge1\) is an integer and all rates and conserved totals are strictly positive. We count positive equilibria in one fixed conservation class, without a stability requirement.

A [September 2026 external unrefereed candidate](https://evidencepress.org/releases/tcell-exactly-five/) claims exactly five equilibria for the full **two-ligand** model at \(N=100\) and explicitly leaves the agonist-only question unresolved. Its proof and verifier were not independently audited here. It is neither an ingredient of the deductions below nor a claimed resolution of the narrower source target.

Let \(C_j\) be receptor–ligand complexes with j phosphorylations and S active phosphatase. Write \(\Sigma=\sum_{j=0}^N C_j\). The conserved total ligand, receptor and phosphatase are \(L,R,S_T\); the rate constants are \(\alpha,\beta,\gamma,\phi,\kappa,\nu,b>0\). The ODE is
\[
\dot S=\alpha C_1(S_T-S)-\beta S, \tag{1}
\]
\[
\dot C_0=\kappa(L-\Sigma)(R-\Sigma)
 +(b+\gamma S)C_1-(\phi+\nu)C_0, \tag{2}
\]
\[
\dot C_j=\phi C_{j-1}+(b+\gamma S)C_{j+1}
 -(\phi+b+\gamma S+\nu)C_j,\quad1\le j<N, \tag{3}
\]
\[
\dot C_N=\phi C_{N-1}-(b+\gamma S+\nu)C_N. \tag{4}
\]
For \(N=1\), (3) is absent and \(C_1=C_N\). The positive physical region is
\[
C_j>0,\quad0<S<S_T,\quad\Sigma<L,\quad\Sigma<R. \tag{5}
\]
Antagonist species are absent, rather than asserted positive on this boundary restriction of the larger model.

Summing the receptor equations gives
\[
\dot\Sigma=\kappa(L-\Sigma)(R-\Sigma)-\nu\Sigma. \tag{6}
\]
At equilibrium \(\Sigma=\sigma\), where \(\sigma\in(0,\min(L,R))\) is unique: the right side is positive at zero, negative at the other endpoint, and has negative derivative on that interval. The quantity \(\Sigma\) is not conserved; its **equilibrium** value \(\sigma\) is determined by the fixed rates and totals.

## 2. Positive recurrence and exact reconstruction

Set
\[
t=\frac{\gamma S}{\phi},\quad d=\frac{b+\nu}{\phi},\quad
v=\frac{\nu}{\phi},\quad h=\frac{\gamma S_T}{\phi},\quad
A=\frac{\alpha\sigma}{\beta},\qquad u=d+t. \tag{7}
\]
Thus \(d>v>0\), \(h,A>0\), and the physical interval is \(0<t<h\).

Define polynomials in u by
\[
P_0=D_0=1,\qquad P_1=u,\quad D_1=1+u,
\]
and, for \(m\ge2\),
\[
P_m=uP_{m-1}+vD_{m-2},\qquad
D_m=D_{m-1}+P_m=\sum_{i=0}^mP_i. \tag{8}
\]
All coefficients are nonnegative for \(v>0\), and all values are positive for \(u>0\). Induction gives: \(P_m\) is monic of degree m, its coefficient of \(u^{m-1}\) is zero for \(m\ge1\), and
\[
D_m(u)=u^m+u^{m-1}+\text{lower-degree terms}\quad(m\ge1). \tag{9}
\]
For \(P_1\), the zero coefficient is its constant coefficient.

**Reconstruction lemma.** At every positive equilibrium,
\[
C_j=\sigma\,\frac{P_{N-j}(d+t)}{D_N(d+t)},\qquad0\le j\le N. \tag{10}
\]
Conversely, for any \(t>0\), these expressions solve all receptor steady-state equations, with \(S=\phi t/\gamma\).

**Proof.** For \(T_j=\sum_{i=j}^N C_i\), summing steady equations from index j to N gives
\[
\phi C_{j-1}=(b+\gamma S)C_j+\nu T_j. \tag{11}
\]
Starting with \(C_N=c\), this yields \(C_{N-1}=uc\) and successively \(C_{N-m}=cP_m(u)\). Summing gives \(\sigma=cD_N(u)\), proving (10) and uniqueness. Conversely, (8) reconstructs (11). Differences of successive tail equations yield (3), and the final tail equation yields (4). Since (6) vanishes at \(\sigma\), equation (2) follows as well. \(\square\)

The remaining phosphatase equation is exactly
\[
F_N(t)=tD_N(d+t)-A(h-t)P_{N-1}(d+t)=0. \tag{12}
\]
For \(t\ge h\) this polynomial is strictly positive. Every positive root therefore lies in \((0,h)\). Formula (10), the bound on \(\sigma\), and \(S=\phi t/\gamma\) reconstruct all quantities in (5), including positive free receptor, free ligand and inactive phosphatase. Thus positive roots of (12) are in bijection with physically positive equilibria. Clearing this denominator loses no solutions and creates no physical extra roots.

## 3. A uniform count bound

**Theorem.** The agonist-only N-site model has at most
\[
B_N=\begin{cases}N,&N\text{ odd},\\N-1,&N\text{ even}\end{cases} \tag{13}
\]
distinct physically positive equilibria. In particular, the four-site model has at most three for all positive rates and totals.

**Proof.** Equations (8)–(9) show that \(F_N\) has degree \(N+1\), leading coefficient one, and coefficient of \(t^N\)
\[
Nd+1+A>0. \tag{14}
\]
The term \(-AhP_{N-1}(d+t)\) has degree at most \(N-1\) and cannot alter these two leading coefficients. Also
\[
F_N(0)=-AhP_{N-1}(d)<0. \tag{15}
\]
The nonzero coefficient list in increasing degree therefore begins negative and ends with two positive terms. Its number of sign changes is odd and at most N. The largest odd integer at most N is \(B_N\). Descartes' rule bounds positive roots, counted with multiplicity, by that number. Apply the reconstruction lemma. \(\square\)

For odd N this recovers the elementary bound recorded in the 2017 paper; for even N it improves the bound stated there by two. This is not a uniform three-root theorem for all N. Historical novelty of the coefficient observation is unconfirmed.

## 4. An exact sharp witness at four sites

Choose
\[
N=4,\qquad \alpha=\beta=\gamma=\phi=L=R=1,\qquad
\kappa=\frac1{5000},\qquad
\nu=b=\frac1{10000},\qquad S_T=20. \tag{16}
\]
All rates and totals are strictly positive. Equation (6) gives \(\sigma=1/2\), because
\[
\frac1{5000}(1-\tfrac12)^2=\frac1{10000}\,\frac12.
\]
Hence \(d=1/5000,\ v=1/10000,\ A=1/2,\ h=20,\ t=S\).

Multiplication of \(F_4\) by \(625000000000000>0\) gives
\[
\begin{aligned}
Q(t)={}&625000000000000t^5+938000000000000t^4\\
&-5624249850000000t^3+621812687520000t^2\\
&+624093093765001t-625250050000.
\end{aligned} \tag{17}
\]
Exact evaluations are
\[
Q(0)=-625250050000<0,\qquad
Q(1/100)=\frac{567224734905201}{100}>0,
\]
\[
Q(1)=-2815969318764999<0,\qquad
Q(3)=83466222268925003>0. \tag{18}
\]
There are consequently three distinct roots in
\[
(0,1/100),\qquad(1/100,1),\qquad(1,3).
\]
The upper bound excludes every further positive root. Since it counts multiplicity, these three scalar roots are simple.

For explicit reconstruction,
\[
\begin{aligned}
P_0&=1,&P_1&=u,&P_2&=u^2+v,\\
P_3&=u^3+2vu+v,&
P_4&=u^4+3vu^2+2vu+v^2+v.
\end{aligned}
\]
At each root take \(u=t+1/5000\), \(v=1/10000\), and \(C_j=P_{4-j}(u)/(2D_4(u))\). Their sum is \(1/2\); all receptor species are positive, both free pools equal \(1/2\), and inactive phosphatase is \(20-t>0\). The three equilibria lie in the same fixed conservation class.

Scalar simplicity alone does not classify the full ODE Jacobian. No dynamical-stability, bistability, or physiological-relevance conclusion is asserted.

## 5. Higher-N route and precise gap

The first approach produced the recurrence, the count bound and the sharp four-site result. The remaining possibility of more than three in this restriction begins at \(N\ge5\).

The second approach considered
\[
H_N(t)=\frac{tD_N(d+t)}{(h-t)P_{N-1}(d+t)},\qquad0<t<h.
\]
Equilibria are its intersections with the level A, and
\[
\frac{H_N'}{H_N}
=\frac1t+\frac1{h-t}
+\frac{D_N'(d+t)}{D_N(d+t)}
-\frac{P_{N-1}'(d+t)}{P_{N-1}(d+t)}. \tag{19}
\]
A bounded exploratory scan tested 240 parameter triples at \(N=5,6,8,12,20,50\), with 801 sample points each. It found at most two sampled derivative sign changes. This is not an upper bound on all turning points or equilibria: a finite numerical grid can miss narrow features and gives no certification between sample points.

No all-parameter control of (19), or agonist-only parameter set with more than three certified equilibria, was obtained. The exact scalar root-count problem (12) remains open here. The external two-ligand candidate does not supply that missing argument.

Recommended outcome: **unsolved, 2/5**, with the rigorous sharp four-site result and explicit source-scope qualification.

