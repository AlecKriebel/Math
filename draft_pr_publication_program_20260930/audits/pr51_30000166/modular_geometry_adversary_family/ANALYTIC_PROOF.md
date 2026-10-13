# Independent analytic reconstruction of PR51's exact theorem

This is a checkable review derivation, not a novelty claim or a new paper.
The target is the nonnegativity of all Fourier coefficients of

\[
S_N(\tau)=\eta(N\tau)^{\varphi(N)}\prod_{d\mid N}\eta(d\tau)^{-\mu(d)}
\quad(N\in\mathbb Z_{>0}).
\]

The source comparison is documented separately in REPORT.md. The theorem and
the general theta identity are credited to Berkovich and Garvan. The derivation
below exposes their classical combinatorial foundation and analytic uniqueness
step so that an imported finite-computation verdict is unnecessary.

## A. Core lattice identity by charged beta sets

Use the usual beta-set encoding of a partition \(\lambda\):
\(B_\lambda=\{\lambda_j-j:j\ge1\}\). Its vacuum is
\(B_0=\{-1,-2,\ldots\}\). These sets differ only finitely, and the number
of added nonnegative positions equals the number of removed negative positions.
Conversely a set with these finite-tail and balance properties determines a
unique partition by listing its elements in descending order and putting
\(\lambda_j=b_j+j\). The size is the sum of added positions minus the sum
of removed positions. This follows by cutting both descending lists far enough
into their common negative tail and subtracting their finite sums.

Fix \(a\ge1\). Split the integer positions into runners \(i+a\mathbb Z\),
\(0\le i<a\). The runner charge \(n_i\) is its number of added positions
minus its number of removed positions; the global balance is \(\sum_i n_i=0\).
The unique downward-closed runner with charge \(n_i\) contains precisely
the positions \(i+ak\) with \(k<n_i\). The resulting balanced beta set
is an \(a\)-core. To check this characterization, beta-set hook lengths
are positive differences of occupied positions and unoccupied positions below
them. A hook divisible by \(a\) is exactly a bead/gap pair in the same
runner. Such a pair exists exactly when that runner is not downward closed.
In particular downward closure rules out both a hook of length \(a\) and
every positive multiple of \(a\).

For a core runner, its size contribution is

\[
\sum_{k=0}^{n_i-1}(i+ak)
 =i n_i+\frac a2n_i(n_i-1)
\quad(n_i\ge0).
\]

For \(n_i<0\) it is instead minus the sum from \(k=n_i\) to \(-1\),
which gives the same polynomial. Summing and using the zero charge yields

\[
|\operatorname{core}(n)|=Q_a(n)
 =\frac a2\sum_i n_i^2+\sum_i i n_i.
\]

Each coordinate contribution in the triangular expression is nonnegative:
for \(n_i=-k<0\) it equals
\(k[a(k+1)/2-i]>0\), and for \(n_i\ge0\) it is nonnegative directly.
Therefore \(Q_a\ge0\), and \(Q_a=0\) on the balanced lattice only at
\(n=0\).

For an arbitrary partition's runners, translate each runner by its charge to
make its beta set balanced. These normalized runners encode unique partitions
\(\nu_0,\ldots,\nu_{a-1}\). This operation and its inverse, translating
the runners back and taking their union, are a bijection. Relative to the core
thresholds, moving positions on runner \(i\) changes their actual integer
positions by \(a\) times the runner change. Thus

\[
|\lambda|=Q_a(n)+a\sum_i|\nu_i|.
\]

Euler's partition product follows by independently choosing the multiplicity
of each positive part. Applying it to the displayed bijection gives

\[
\frac1{E(q)}=
\left(\sum_{\sum n_i=0}q^{Q_a(n)}\right)\frac1{E(q^a)^a},
\qquad
\sum_{\sum n_i=0}q^{Q_a(n)}=\frac{E(q^a)^a}{E(q)}.
\]

The sum is the core-counting generating function, so it has nonnegative
integer coefficients. This reconstructs the classical Littlewood and
Klyachko/Garvan–Kim–Stanton identities in the conventions needed here. For
\(a=1\), the only core and lattice vector are empty/zero, and the ratio is 1.

## B. Holomorphic theta uniqueness

For \(a\ge2\), \(0<|q|<1\), \(z\ne0\), define

\[
C_a(z;q)=\sum_{\sum n_i=0}\sum_{j=0}^{a-1}
 q^{Q_a(n)}z^{a n_j+j},
\quad
R_a(z;q)=E(q)E(q^a)^{a-2}
 \frac{[z^a;q^a]_\infty}{[z;q]_\infty}.
\]

On each compact subset of \(\mathbb C^\times\), the lattice summands
are bounded by a Gaussian in \(\|n\|\) times an exponential linear in
\(\|n\|\). The positive quadratic term of \(Q_a\) consequently proves
normal convergence and holomorphy of \(C_a\). The normally convergent
bracket products define \(R_a\). The denominator's zeros \(z=q^k\)
are simple; the numerator has a simple zero at each of them, so all apparent
poles are removable. No pole or convergence assumption is hidden here.

Let \(T_0(n)=(n_1,\ldots,n_{a-1},n_0)\). For \(1\le j<a\), let
\(T_j(n)=T_0(n)+e_{j-1}-e_{a-1}\). These affine maps preserve the
balanced lattice and are bijections. Direct expansion gives

\[
Q_a(T_jn)-Q_a(n)=a n_j+j.
\]

Writing \(F_j\) for the individual \(j\)-sum, changing variables by
\(T_j\) gives \(F_j(qz)=z^{-(a-1)}F_{j-1}(z)\), with indices cyclic
and the \(j=0\) case supplied by \(T_0\). Hence
\(C_a(qz)=z^{-(a-1)}C_a(z)\). The elementary product identity
\([qz;q]_\infty=-z^{-1}[z;q]_\infty\) gives the same equation for
\(R_a\).

At a nontrivial \(a\)-th root of unity \(\zeta\), each lattice summand's
inner sum is \(\sum_j\zeta^j=0\), and the numerator product vanishes,
while its denominator does not. At \(z=1\), the removable quotient limit
is \(a E(q^a)^2/E(q)^2\), so both sides equal
\(a E(q^a)^a/E(q)\) by A.

Here is a proof of the uniqueness assertion rather than an appeal to a
finite number of numerical evaluations. If a nonzero holomorphic function
\(H\) on \(\mathbb C^\times\) satisfies \(H(qz)=z^{-m}H(z)\),
differentiate logarithmically and integrate on a zero-free circle. The
logarithmic-derivative integral on the inner circle of radius \(|q|R\)
is the outer integral on radius \(R\) minus \(m\); the complex rotation
by \(q\) does not change a full-circle integral. By the argument principle,
\(H\) has exactly \(m\) zeros with multiplicity in the intervening annulus.
Choose \(1<R<|q|^{-1}\) with zero-free boundary circles. If
\(H=C_a-R_a\) were nonzero, it would have \(m=a-1\) zeros there, but
all \(a\) distinct \(a\)-th roots of unity lie inside and are zeros.
This contradiction proves the theta identity for every stated parameter.
It is the independently checked analytic mechanism of Berkovich–Garvan
Theorem 1.2, not a new attribution.

## C. Specialization, integral powers, and finite coefficients

Substitute \(z=q^r\) and replace the base in B by \(q^M\), where
\(M,r\in\mathbb Z\) and \(0<r<M\). The exponent becomes

\[
e(n,j)=M Q_a(n)+r(a n_j+j)
 =(M-r)Q_a(n)+r Q_a(T_jn)\ge0.
\]

Every exponent is integral, despite the half in the quadratic definition.
Moreover, it has a positive definite quadratic part, so only finitely many
vectors contribute below any degree. For an explicit bound set
\(L_i=Mi+ra\delta_{ij}\), and let \(L^\perp\) be its projection to
the zero-sum hyperplane. Completing a square gives

\[
e(n,j)\ge\frac{Ma}{4}\|n\|^2
 -\frac{\|L^\perp\|^2}{Ma}.
\]

This proves coefficient finiteness and provides the certified coordinate
cutoffs in the new diagnostic code. Hence \(C_a(q^r;q^M)\) is a
nonnegative integer power series. Its constant coefficient is 1. The
bracket quotient is nonsingular for an interior specialization when
\(0<|q|<1\); the series also extends to \(q=0\) by this construction.

Multiplying by the core series from A gives

\[
D_a(q^r;q^M)=\frac{E(q^{aM})^a}{E(q^M)}C_a(q^r;q^M)
 =E(q^{aM})^{2a-2}
 \frac{[q^{ar};q^{aM}]_\infty}{[q^r;q^M]_\infty}
 \in\mathbb Z_{\ge0}[[q]].
\]

The progressions in each bracket count with multiplicity if \(M=2r\).
That case remains valid; the later all-N factorization uses odd \(M\)
and avoids it. The conditions cannot be removed silently: for
\(a=2,n=(1,-1),j=1,r=M+1\), one exponent equals \(-1\). For
\(r=-1,n=0,j=1\), an exponent is again \(-1\). At \(r=0,M\),
removable continuation is required and the constant multiplicity changes;
the PR does not use those endpoints.

## D. Exact eta normalization and all-N conclusion

Directly substituting \(\eta(d\tau)=q^{d/24}E(q^d)\) gives
\(S_N=q^{A_N}\widetilde S_N\) with

\[
A_N=\frac{N\varphi(N)-\sum_{d\mid N}d\mu(d)}{24},\qquad
\widetilde S_N=E(q^N)^{\varphi(N)}
 \prod_{d\mid N}E(q^d)^{-\mu(d)}.
\]

The leading exponent can be fractional; coefficient signs are unaffected
by shifting the support. In particular \(A_2=1/8\), \(A_3=1/3\),
and \(A_6=5/12\). The Fourier expansion means the expansion at infinity
in the source's convention, not simultaneous positivity at every cusp.
Since \(\eta(\tau+1)=e^{\pi i/12}\eta(\tau)\), the T multiplier
of the unnormalized product is \(e^{2\pi i A_N}\). A blanket assertion
that these are integral-character forms on \(\Gamma_0(N)\) would fail
already for these examples. The PR never needs such an assertion, a
Sturm bound, or a cusp-form sign theorem.

For an additional algebraic cusp diagnostic, write
\(u_d=\varphi(N)\mathbf1_{d=N}-\mu(d)\). For \(N>1,c\mid N\),
put \(t=\varphi(N)/N\) and \(v=\prod_{p\mid c}p\). Multiplying
the prime-by-prime Möbius factors yields

\[
\sum_{d\mid N}\frac{u_d\gcd(c,d)^2}{d}
 =t\left(c^2-(-1)^{\omega(c)}v\right).
\]

It is zero for \(c=1\), positive for every \(c>1\), and at \(c=N\)
reduces to \(24A_N\). Under appropriate modularity hypotheses this
is the usual eta cusp-order expression up to its positive cusp-width
factor. Here it is an independent consistency diagnostic; no integral
Dirichlet-character theorem is being applied to parameters that fail its
congruence conditions. The source's prime modular/lattice discussion
explicitly takes \(p\ge5\). Its character and cusp-order route is not
being extrapolated to prove the composite result.

Finally Möbius inversion gives
\(\prod_{d\mid M}E(q^d)^{\mu(d)}=\prod_{(k,M)=1}(1-q^k)\).
For odd \(M>1\) and a prime \(p\nmid M\), pair the reduced residues
\(r,M-r\). There are \(\varphi(M)/2\) such pairs, so the brackets
in C give exactly

\[
\widetilde S_{pM}(q)=
 \prod_{\substack{1\le r<(M/2)\\(r,M)=1}}D_p(q^r;q^M).
\]

The E exponent is \((2p-2)\varphi(M)/2=\varphi(pM)\); the bracket
ratio is the quotient of the two Möbius products at \(q^p\) and \(q\).
This does not require squarefree \(M\). For
\(N=p^\alpha M\), \(p\nmid M\), set \(N'=pM,t=p^{\alpha-1}\).
The nonzero Möbius divisor factors coincide for \(N,N'\) and
\(\varphi(N)=t\varphi(N')\), giving

\[
\widetilde S_N=
 \left(\frac{E((q^{N'})^t)^t}{E(q^{N'})}\right)^{\varphi(N')}
 \widetilde S_{N'}.
\]

The new factor is a positive integral power of a core series. If \(M=1\),
use \(\widetilde S_p=E(q^p)^p/E(q)\) and this lift; do not use an
empty residue pairing. Every even N is covered by removing the full power
of 2, and every odd N by removing the full power of any chosen prime
divisor. N=1 is exactly 1. This exhausts every positive integer, including
nonsquarefree integers and integers with arbitrarily many prime divisors.
Zeros are permitted: the two-core series has coefficient zero at degree 2.
