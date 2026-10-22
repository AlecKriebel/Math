# Detailed verification of Toppila's counterexample

The construction is Toppila's 1983 Theorem 2, cited in [README.md](README.md). The estimates below are independently derived to check every hypothesis of the exact question. They assert no mathematical novelty.

Put \(q=e^4\), \(t=\sqrt q=e^2>4\), and
\[
E=[0,\infty)\cup\bigcup_{k=1}^{\infty}\overline D(q^k,1).
\]
The disks are locally finite, so their union with the closed ray is closed. Including the origin removes any possible convention about the phrase “positive real axis”; it does not affect the proof.

## 1. The bounded entire witness

Take \(f(z)=e^{-z}\). Every point of \(E\) has nonnegative real part, because \(q^k>1\). Consequently \(|f|\le1\) on \(E\). The function is entire and transcendental.

## 2. The second witness exists and is transcendental

Define
\[
g(z)=\prod_{k=1}^{\infty}(1-z/q^k).
\]
For every compact disk \(|z|\le R\), the sum \(\sum Rq^{-k}\) converges. The standard locally uniform convergence criterion for infinite products therefore makes \(g\) entire. It satisfies \(g(0)=1\), and vanishes at every \(q^k\). Hence it is not the zero function and cannot be a polynomial.

We now verify a global positive lower bound, without relying on a sampled graph.

Set
\[
c=1-q^{-1/2}=1-t^{-1}>3/4,
\qquad C=1-\frac{\sqrt q}{q-1}=1-\frac{t}{t^2-1}>1/2.
\]
For \(0\le x_j<1\), finite induction gives
\(\prod_{j=1}^N(1-x_j)\ge1-\sum_{j=1}^N x_j\).
Passing to limits gives
\[
\prod_{j\ge1}(1-q^{1/2-j})\ge C>0. \tag{1}
\]
The inequality \(C>1/2\) follows from \(t>4\) and \(t^2-1>2t\).

Let \(z\) lie outside all the open disks \(D(q^k,1)\); this includes \(\mathbb C\setminus E\). Write \(r=|z|\). If \(r\le\sqrt q\), the reverse triangle inequality and (1) show \(|g(z)|\ge C\).

If \(r\ge\sqrt q\), choose \(n\ge1\) with
\[
q^{n-1/2}\le r\le q^{n+1/2}.
\]
Shared endpoints may be assigned to either interval. For \(k<n\),
\[
|1-z/q^k|\ge\frac r{q^k}(1-q^k/r)\ge c\frac r{q^k}.
\]
For the central factor, the disk exclusion gives
\(|1-z/q^n|\ge q^{-n}\).
For \(k=n+j>n\), the remaining factors have product at least the left side of (1). Multiplying,
\[
|g(z)|\ge Cc^{n-1}r^{n-1}q^{-n(n-1)/2-n}
\ge C A_n,
\]
where
\[
A_n=c^{n-1}q^{(n^2-4n+1)/2}.
\]
The ratios satisfy
\[
A_2/A_1=c/\sqrt q<1,
\qquad A_{n+1}/A_n=cq^{n-3/2}>1\quad(n\ge2).
\]
Indeed the second ratio is at least \(ct=t-1>3\). Thus \(A_n\ge A_2=cq^{-3/2}\), and
\[
|g(z)|\ge Ccq^{-3/2}>\tfrac12\cdot\tfrac34\cdot4\,q^{-2}
=\tfrac32q^{-2}>q^{-2}.
\]
In the small-radius case, \(C>1/2>q^{-2}\) as well. We have established the sufficient uniform bound
\[
|g(z)|\ge e^{-8}\qquad (z\in\mathbb C\setminus E). \tag{2}
\]
The constant is deliberately nonoptimal. All products used in the inequalities are limits of finite products with positive lower bounds.

## 3. Every simultaneous entire witness is constant

Suppose an entire function \(h\) satisfies
\[
|h(z)|\le M\quad(z\in E),\qquad
|h(z)|\ge m>0\quad(z\notin E).
\]
For each integer \(k\ge1\), let
\[
r_k=e^{4k+2},\qquad A_k=\{z:r_k/e<|z|<er_k\}.
\]
No disk \(\overline D(e^{4j},1)\) meets \(A_k\): those with \(j\le k\) lie inside its inner boundary, and those with \(j\ge k+1\) lie outside its outer boundary. In particular,
\[
e^{4k}+1<e^{4k+1},\qquad e^{4k+4}-1>e^{4k+3}.
\]
Both follow immediately from \(e>2\), and they also handle every other disk by monotonicity.

The only part of \(E\) in \(A_k\) is the ray. Each point of that ray inside \(A_k\) is a limit of points of \(A_k\setminus E\), so continuity extends \(|h|\ge m\) to all of \(A_k\). In particular \(M\ge m\). The function
\[
u_k(z)=\log(|h(z)|/m)
\]
is nonnegative and harmonic on \(A_k\). Harmonicity of log-modulus uses only that \(h\) is zero-free there; no single-valued analytic logarithm on the annulus is required.

Fix \(z=r_ke^{i\theta}\) with \(0\le\theta<2\pi\), and set
\(z_j=r_ke^{ij\theta/32}\), \(0\le j\le32\).
Every disk \(D(z_j,r_k/2)\) lies in \(A_k\), since
\(1/e<1/2\) and \(3/2<e\). Successive centers obey
\[
|z_j-z_{j-1}|\le r_k\theta/32<\pi r_k/16<r_k/4.
\]
The usual disk Harnack bound, at distance at most half the disk radius, gives
\(u_k(z_j)\le3u_k(z_{j-1})\).
This also holds for a nonnegative harmonic function by applying the positive version to \(u_k+\varepsilon\) and letting \(\varepsilon\downarrow0\). Iterating at most 32 times,
\[
u_k(z)\le3^{32}u_k(r_k)\le3^{32}\log(M/m).
\]
The upper bound is independent of \(k\) and \(\theta\), so
\[
|h(z)|\le K:=m(M/m)^{3^{32}}
\qquad(|z|=r_k).
\]
The maximum-modulus principle bounds \(h\) by \(K\) inside each of these circles. Since \(r_k\to\infty\), \(h\) is bounded on the whole plane and Liouville's theorem makes it constant.

The lower-bound premise excludes the zero constant; nonzero constants do satisfy both bounds for suitable \(m,M\). None is transcendental. Together with Sections 1–2, this proves the exact requested implication false.

## Scope controls

- The ray is essential to the displayed rigidity argument: it supplies a bounded base point on every large comparison circle.
- The disks are essential for the separate product witness: they contain its zeros and remove neighborhoods where a uniform nonzero lower bound would fail.
- The hypotheses are global uniform inequalities, not eventual bounds or almost-everywhere assertions.
- The witnesses are entire, not merely meromorphic.
- No unproved choice of growth order or approximation theorem is used.
- These verifications credit a known 1983 counterexample; they do not repair a failed original theorem or establish priority for this packet.
