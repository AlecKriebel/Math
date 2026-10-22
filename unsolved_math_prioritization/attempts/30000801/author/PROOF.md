# A conditional Pohozaev obstruction to multiple positive bubbles

## 1. Target and limits of the claim

The target equation, in four dimensions, is

\[
\Delta^2u_k=\lambda_k u_k e^{2u_k^2},\qquad u_k>0,\qquad
u_k=\Delta u_k=0\text{ on }\partial\Omega,
\]

The parameters are positive constants tending to zero, and
\(\int_\Omega|\Delta u_k|^2=\lambda_k\int_\Omega u_k^2e^{2u_k^2}\to\Lambda>0\).
The known quantum is \(Q=16\pi^2\). The unresolved target is the simplicity
statement called \(L=I\) in the original report, beyond \(\Lambda=LQ\).

There is a counting subtlety: the report's extraction theorem labels selected
centers \(x_k^{(i)}\), separated relative to their own bubble scales. It does not
state that all limiting \(x^{(i)}\) are distinct. Thus counting distinct limiting
spatial locations, selected profiles, and all bubble-tree levels must not be
silently interchanged. The criterion proved below concerns a single *interior*
spatial location containing a specified finite family of positive bubbles. It
neither excludes boundary concentration nor establishes that the original
extraction captures every level.

The analyst's convention \(\Delta=\sum_{j=1}^4\partial_j^2\) is used throughout.
All integrations below concern smooth classical solutions on a neighborhood of
a closed ball contained in \(\Omega\). No assertion about rough-domain traces
or weak solutions beyond the cited source is added.

## 2. Exact standard-bubble normalization

Let \(\eta(x)=-\log(1+|x|^2)\). Radial differentiation in dimension four gives

\[
\Delta\eta=-\frac{4(|x|^2+2)}{(1+|x|^2)^2},\qquad
\Delta^2\eta=\frac{96}{(1+|x|^2)^4}=96e^{4\eta}.
\]

Since \(|S^3|=2\pi^2\), substitution \(t=r^2\) gives

\[
96\int_{\mathbb R^4}e^{4\eta}dx
=96\pi^2\int_0^\infty\frac{t}{(1+t)^4}dt=16\pi^2.
\]

For a selected bubble of height \(M_k=u_k(x_k)\to\infty\), use the source
normalization \(\lambda_k r_k^4M_k^2e^{2M_k^2}=96\) and
\(\eta_k(y)=M_k(u_k(x_k+r_ky)-M_k)\). On every fixed rescaled ball,
\(\eta_k\to\eta\) implies

\[
r_k^4\lambda_k u_k(x_k+r_ky)^2e^{2u_k(x_k+r_ky)^2}
=96(1+\eta_k/M_k^2)^2e^{4\eta_k+2\eta_k^2/M_k^2}
\longrightarrow96e^{4\eta}.
\]

First pass \(k\to\infty\), then let the rescaled radius tend to infinity.
Every such bubble has energy \(Q\). Fixed-radius bubble balls about distinct
selected centers are disjoint for sufficiently large \(k\), by their relative
scale separation. Positivity and summation therefore give \(\Lambda\ge IQ\).
Combined with the established integer quantization, this yields the elementary
special case \(0<\Lambda<2Q\Rightarrow L=I=1\). This is a consequence of known
results, not a resolution at arbitrary energy.

## 3. A local identity with all boundary terms

Write
\[
f_k(t)=\lambda_k t e^{2t^2},\qquad
F_k(t)=\frac{\lambda_k}{4}(e^{2t^2}-1),\qquad F_k'=f_k.
\]
For a ball \(B_r(a)\Subset\Omega\), set \(X=x-a\) and define

\[
P_r(v)=\int_{\partial B_r(a)}
\left[(X\cdot\nabla v)\partial_n\Delta v
-\Delta v\,\partial_n(X\cdot\nabla v)
+\frac{X\cdot n}{2}(\Delta v)^2\right]dS.
\]

Here \(n\) is the outward unit normal. Two integrations by parts yield
\[
\int_{B_r}(X\cdot\nabla v)\Delta^2v
=P_r(v)+\frac{4-d}{2}\int_{B_r}(\Delta v)^2.
\]
Indeed, the interior term after the integrations is
\(\int\Delta v[2\Delta v+X\cdot\nabla\Delta v]\), whose second summand is
\(\frac12\int_{\partial B_r}(X\cdot n)(\Delta v)^2-
\frac d2\int_{B_r}(\Delta v)^2\). At \(d=4\) the interior quadratic term
vanishes. Applying \(\Delta^2u_k=f_k(u_k)\), and integrating
\(X\cdot\nabla F_k(u_k)\), gives the exact identity

\[
\boxed{P_r(u_k)=r\int_{\partial B_r(a)}F_k(u_k)dS
-4\int_{B_r(a)}F_k(u_k)dx.}\tag{1}
\]

There is no sign assumption on the individual terms of \(P_r\). Equation (1)
is valid locally and does not require Navier data on this artificial sphere.

## 4. Conditional limiting mass identity

Let \(c_k>0\) be normalization constants tending to infinity. Assume, in
addition to the equation, that for some \(\rho>0\), \(m>0\), \(n_0\ge0\):

(H1) On the punctured ball \(B_\rho(a)\setminus\{a\}\),
\[
c_ku_k\longrightarrow U=\frac{m}{8\pi^2}\log\frac1{|x-a|}+h(x)
\quad\text{in }C^3_{\rm loc},\qquad h\in C^3(B_\rho(a)).
\]
Here \(h\) and its derivatives are bounded on each smaller closed ball,
including at \(a\).

(H2) For every sufficiently small fixed radius \(r\),
\[
\lim_{k\to\infty}4c_k^2\int_{B_r(a)}F_k(u_k)dx=n_0.
\]

The boundary limit needed below follows already from (H1): on a fixed sphere,
\(U_k=c_ku_k\) is bounded and
\(c_k^2F_k(u_k)=\frac{\lambda_k}{2}U_k^2(1+O(c_k^{-2}))\to0\) uniformly.

Then
\[
\boxed{n_0=\frac{m^2}{16\pi^2}.}\tag{2}
\]

**Proof.** Multiply (1) by \(c_k^2\), using the quadratic homogeneity of
\(P_r\). By (H1), all derivatives needed on a fixed sphere converge uniformly,
so \(P_r(c_ku_k)\to P_r(U)\). By (H2) and the preceding boundary estimate, \(P_r(U)=-n_0\).
Put \(A=m/(8\pi^2)\), \(w=A\log(1/r)\). Direct differentiation gives
\(rw'=-A\), \(\Delta w=-2A/r^2\),
\(\partial_r\Delta w=4A/r^3\), and \(\partial_r(rw')=0\).
Consequently \(P_r(w)=-4\pi^2A^2\). In \(P_r(w+h)-P_r(w)\), every mixed
term tends to zero as \(r\downarrow0\): the potentially largest ones have
sizes \(O(r)\), since \(X\cdot\nabla h=O(r)\),
\(\partial_n(X\cdot\nabla h)=O(1)\), and surface area is \(O(r^3)\).
Pure \(h\) terms also tend to zero. Thus
\(-n_0=-4\pi^2A^2=-m^2/(16\pi^2)\), proving (2). \(\square\)

The coefficient in (H1) is the natural source-mass normalization: in four
dimensions \(\Delta^2[(8\pi^2)^{-1}\log(1/|x|)]=\delta_0\).
This follows either distributionally from the Laplacian's fundamental solution
or from the flux \(\int_{\partial B_r}\partial_n\Delta[-\log r]=8\pi^2\).
Crucially, (H1) is an explicit extra hypothesis here; convergence of unweighted
energy measures is not asserted to imply it.

## 5. Conditional one-bubble theorem

Suppose a finite family of \(q\ge1\) spherical bubbles at the same interior
point has heights \(M_{j,k}\to\infty\). Assume there is a common normalization
\(c_k\to\infty\) with
\[
a_j:=\lim_{k\to\infty}c_k/M_{j,k}\in(0,\infty),\qquad 1\le j\le q.
\]
Suppose (H1)--(H2) hold and the *two weighted masses are exhausted by these
bubbles*, in the precise sense
\[
m=Q\sum_{j=1}^q a_j,\qquad n_0=Q\sum_{j=1}^q a_j^2.\tag{3}
\]
Then \(q=1\).

**Proof.** The weights in (3) are dictated by direct rescaling, not convention:
on the \(j\)-th bubble, \(c_kf_k(u_k)\,dx\) has iterated limiting mass
\(Qa_j\), while \(4c_k^2F_k(u_k)\,dx\) has mass \(Qa_j^2\).
For the latter, the subtracted term contributes
\(\lambda_kc_k^2r_{j,k}^4=96(c_k/M_{j,k})^2e^{-2M_{j,k}^2}\to0\)
on each fixed rescaled ball. These local calculations alone do not establish
(3) over the whole shrinking neighborhood; exhaustion is an assumption.
Substitution in (2) yields
\[
\sum_j a_j^2=\left(\sum_j a_j\right)^2,
\qquad 2\sum_{i<j}a_i a_j=0.
\]
All \(a_j\) are strictly positive. Hence there can be no pair and \(q=1\).
\(\square\)

This also explains why vanishing normalized weights cannot simply be retained
in the conclusion: \((a_1,a_2)=(1,0)\) passes the moment identity although it
has two formally listed components. Sign-changing weights are even worse:
\((1,1,-1/2)\) also pass. Neither control is a solution of the target PDE;
they certify which assumptions the algebra actually uses.

## 6. Exact weighted-defect formula and unresolved step

Write the possible leftover source and primitive masses in units of \(Q\) as
\[
m/Q=S_1+d_1,\qquad n_0/Q=S_2+d_2,\quad
S_1=\sum a_j,\quad S_2=\sum a_j^2,
\]
with nonnegative defects \(d_1,d_2\) when a positive decomposition is justified.
Equation (2) becomes the exact obstruction
\[
\boxed{d_2-2S_1d_1-d_1^2=2\sum_{i<j}a_i a_j.}\tag{4}
\]
For example, two positive weights \((1,1/2)\), \(d_1=0\), \(d_2=1\) satisfy
(4). Thus the Pohozaev identity *by itself* does not exclude a double bubble.
This is only a consistent moment configuration, not a PDE counterexample.

To use the theorem for the original question one would need to establish a
common normalization with all relevant height ratios in \((0,\infty)\), the
exterior logarithmic profile (H1), the finite primitive-mass limit (H2), and
the exhaustion (3), for every potentially multiple cluster, while also handling
the selected-center versus distinct-point distinction and any boundary regime.
None of those difficult estimates is supplied by the elementary algebra above.

Ordinary energy exhaustion cannot simply replace weighted exhaustion. With
\(e_k=\lambda_ku_k^2e^{2u_k^2}\), at positive \(u_k\) the two weighted densities
are exactly
\[
c_kf_k(u_k)=(c_k/u_k)e_k,\qquad
4c_k^2F_k(u_k)=(c_k/u_k)^2(1-e^{-2u_k^2})e_k.
\]
The factors \(c_k/u_k\) need not stay bounded on necks. At the level of
nonnegative measures, neck energy \(\varepsilon^2\) and weight
\(c_k/u_k=1/\varepsilon\) give source contribution \(\varepsilon\) but primitive
contribution approaching 1 if \(u_k\to\infty\). Thus a vanishing energy neck can
remain visible to the squared weighted moment. This model identifies a failed
inference; it does not assert that such a neck is realized by a solution.

Finally, a Cauchy--Schwarz argument yields only the already expected *lower*
energy bound. On a ball define \(E_k=\int e_k\),
\(m_k=\int c_kf_k(u_k)\), and
\(\widetilde n_k=\lambda_kc_k^2\int e^{2u_k^2}\).
Then \(m_k^2\le E_k\widetilde n_k\) exactly. If in addition
\(\lambda_kc_k^2|B_r|\to0\), so that \(\widetilde n_k\to n_0\),
(2) gives \(E\ge Q\), not \(E\le Q\). Reversing that inequality would falsely
turn the necessary condition into a simplicity proof.

**Final mathematical status:** the conditional theorem and identities above are
proved; the global strong-quantization problem is unresolved by this package.
