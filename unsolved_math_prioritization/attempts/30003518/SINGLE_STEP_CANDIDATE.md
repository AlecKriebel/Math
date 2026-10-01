# Global convergence of the single-step Lck proofreading core

**Scoped partial candidate, unreviewed.** This is the result of substantive author turn 1 for record 30003518. It does not settle arbitrary-chain asymptotics, the full Altan–Bonnet–Germain network, or the imported bundled target. The cooperative-compartmental contraction mechanism is classical; historical novelty is unconfirmed.

## 1. Exact scope

Consider the Lck-only, one-phosphorylation mass-action core of Brechmann (2024), equations (2.2), (2.3), and (5.5). All six rates k1,...,k6 and conserved totals Rtot,Mtot,Etot are strictly positive. Free receptor r, free ligand m, free Lck e, unphosphorylated complex c, enzyme-substrate complex b, and phosphorylated complex z satisfy

\[
\begin{aligned}
\dot r=\dot m&=-k_1rm+k_2c+k_6z,\\
\dot c&=k_1rm-k_2c-k_3ce+k_4b,\\
\dot b&=k_3ce-(k_4+k_5)b,\\
\dot z&=k_5b-k_6z,\qquad \dot e=-\dot b.
\end{aligned}
\]

The conserved totals are
\[
r+c+b+z=R_{\rm tot},\quad m+c+b+z=M_{\rm tot},\quad e+b=E_{\rm tot}.
\]
There is one ligand species; neither phosphatase feedback, CD8 nor ZAP-70 is included. No enzyme-bound-complex dissociation reaction is added. Parameters are arbitrary positive rates of this specified network, with no physiological interpretation claimed.

**Theorem.** Each such conservation class has exactly one strictly positive equilibrium. Every nonnegative physical solution converges to it exponentially, with constants depending on the fixed class and rates. In particular, the equilibrium is globally asymptotically stable relative to the class.

Brechmann's dissertation establishes uniqueness and local stability in this case, and gives sufficient parameter conditions for global stability in Theorem 10. The argument below is self-contained for the stated all-positive-rate single-step claim. Its source applicability is to this exact core, not every reaction in the original 2005 network.

## 2. A convex invariant domain

Set Delta=Mtot-Rtot and eliminate m=r+Delta and e=Etot-b, but retain four coordinates x=(r,c,b,z). Define f(r)=k1*r*(r+Delta). The equations become
\[
\begin{aligned}
\dot r&=-f(r)+k_2c+k_6z,\\
\dot c&=f(r)-k_2c-k_3c(E_{\rm tot}-b)+k_4b,\\
\dot b&=k_3c(E_{\rm tot}-b)-(k_4+k_5)b,\\
\dot z&=k_5b-k_6z.
\end{aligned}\tag{1}
\]
The physical domain is the convex compact polytope
\[
D=\{r,c,b,z\ge0:\ r+\Delta\ge0,\ b\le E_{\rm tot},\ r+c+b+z=R_{\rm tot}\}.
\]
On either possible free-pool boundary, r=0 or r+Delta=0, f vanishes and r' is nonnegative. On c=0, b=0 and z=0 the corresponding derivatives are nonnegative. On b=Etot the derivative b'=-(k4+k5)Etot is negative. The sum of the four derivatives vanishes. Thus D is invariant. Polynomial local existence, uniqueness, and boundedness imply global forward existence in D.

## 3. Unique interior equilibrium

For 0<b<Etot set
\[
z(b)=\frac{k_5}{k_6}b,\qquad
c(b)=\frac{k_4+k_5}{k_3}\frac b{E_{\rm tot}-b},\qquad
w(b)=c(b)+\left(1+\frac{k_5}{k_6}\right)b.
\]
w is continuous and strictly increasing from zero to infinity. There is a unique beta in (0,Etot) with w(beta)=min(Rtot,Mtot). For 0≤b≤beta define
\[
F(b)=k_1(R_{\rm tot}-w(b))(M_{\rm tot}-w(b))-k_2c(b)-k_5b.
\]
On (0,beta), the first term strictly decreases and the subtracted terms strictly increase. Moreover F(0)=k1*Rtot*Mtot>0 and F(beta)<0. There is exactly one root b* in (0,beta). Set c*=c(b*), z*=z(b*), r*=Rtot-w(b*), m*=Mtot-w(b*), e*=Etot-b*. All six species are positive. These formulas satisfy every equilibrium equation, since the r,b,z equations vanish and conservation supplies the c equation.

Conversely, any equilibrium in D must be interior. If b=0, its equation forces c=0 (e=Etot>0), then z=0 and c'=k1*Rtot*Mtot>0, a contradiction. If b=Etot, b'<0. Thus 0<b<Etot; b'=z'=0 force the displayed c(b),z(b)>0. If r or m were zero, r'=k2c+k6z>0. Every equilibrium therefore gives the unique root of F.

## 4. Cooperative dynamics and a uniformly mixing difference equation

The ambient Jacobian of (1) is
\[
J(x)=\begin{pmatrix}
-f'(r)&k_2&0&k_6\\
f'(r)&-k_2-k_3e&k_3c+k_4&0\\
0&k_3e&-k_3c-k_4-k_5&0\\
0&0&k_5&-k_6
\end{pmatrix},\qquad f'(r)=k_1(r+m)\ge0.\tag{2}
\]
Its off-diagonal entries are nonnegative, and every column sums to zero. Convexity of D allows the exact mean-value formula, for y(t)=x(t)-x*,
\[
\dot y=A(t)y,\qquad A(t)=\int_0^1J(x^*+\theta(x(t)-x^*))\,d\theta.\tag{3}
\]
The matrix A is bounded, Metzler, and has zero column sums. In addition to the constant positive edges c→r, b→c, b→z and z→r, it has
\[
A_{c,r}=k_1(r(t)+r^*+\Delta)=k_1(r(t)+m^*)\ge k_1m^*>0,
\]
\[
A_{b,c}=\frac{k_3}{2}(e(t)+e^*)\ge\frac{k_3e^*}{2}>0.
\]
These six directed edges form a strongly connected graph, with a path of length at most three between each ordered pair. The bounds hold even for boundary initial data. They do not assume prior convergence or persistence.

For completeness, choose a constant M>0 such that A(t)+MI is entrywise nonnegative for every t, and choose delta>0 smaller than all six displayed edge lower bounds. Let P(t+1,t) denote the fundamental matrix of (3) over a unit interval. The Peano–Baker expansion of the shifted nonnegative system gives, for any directed path of length ell≤3,
\[
P_{ij}(t+1,t)\ge e^{-M}\frac{\delta^\ell}{\ell!};
\]
the diagonal uses ell=0. Indeed each path contributes a product of ell off-diagonal entries integrated over an ordered unit simplex of volume 1/ell!. All remaining summands are nonnegative. Thus every entry of P is bounded below by a fixed epsilon>0; reduce epsilon if needed so epsilon≤1/8. Nonnegativity of P follows from the same expansion, and zero column sums of A imply that P is column stochastic.

For any vector v with coordinate sum zero, write Q=P-epsilon*11^T. Then Q is nonnegative with column sums 1-4epsilon, and Pv=Qv. Consequently
\[
\|P v\|_1\le(1-4\epsilon)\|v\|_1.\tag{4}
\]
The difference y has sum zero by conservation. Iterating (4), and using ordinary l1 nonexpansion of the stochastic transition matrix on intervening time intervals, gives
\[
\|x(t)-x^*\|_1\le(1-4\epsilon)^{\lfloor t\rfloor}\|x(0)-x^*\|_1.
\]
This is global exponential convergence. The same nonexpansion also proves Lyapunov stability relative to D. Recovering m=r+Delta and e=Etot-b gives convergence and stability for every original species. This proves the theorem.

## 5. Boundaries and remaining target

Strict positivity of all six rates and three totals is essential to the assertion as stated. Zero rates or zero pools are excluded; no uniform rate is claimed over parameter limits. The result covers arbitrary unequal receptor/ligand totals and all nonnegative initial data in their physical class. It is not a statement that a source equilibrium count alone proves stability.

For N≥2, eliminating free Lck creates negative cross-derivatives between different bound-enzyme complexes, so the cooperative argument does not automatically extend. Multistationarity of that different-dimensional network is already established in Brechmann's Theorem 3. Its full asymptotic classification, and the source's larger module with additional molecular species, remain unresolved here.

Primary sources: [OWR2017, pp.1775–1776](https://ems.press/content/serial-article-files/46689); [Brechmann 2024, Sections 2.4 and 5.2](https://openscience.ub.uni-mainz.de/bitstreams/a948dbbc-0daf-4167-bfd8-23ab6e574d64/download); [Altan–Bonnet–Germain 2005 and supplements](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0030356).
