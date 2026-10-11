# Checkable fresh derivation and attempted escapes

This companion expands the independent analytic conclusion. Its first
reconstruction and the tilt mechanism were recorded before previous or family
review access. Later comparison confirmed agreement. Neither an earlier claim
nor finite matrix code is used to certify the stochastic limiting argument.

## Local weak identities with moving tests

Put \(\|h\|_A=\|h\|+\|Ah\|\). For
\(f\in C^1([0,T];D(A),\|\cdot\|_A)\), uniformly approximate its continuous
derivative by finite-span continuous polygonal paths \(p_k\). Define
\(f_k(s)=f(0)+\int_0^s p_k(r)\,dr\). Then \(f_k,f_k'\) converge uniformly
in graph norm to \(f,f'\), and each takes values in a finite-dimensional span
of fixed elements of \(D(A)\). Applying this to finitely many columns, and
keeping deterministic \(C^1\) matrix coefficients, gives tests \(v_k(s)\)
for which the product rule is a finite scalar calculation. Their ranks are
bounded by the number of columns, regardless of the size of their fixed span.

Let \(\tau_m=\inf\{s:\|X_s\|_1>m\}\), taking \(\tau_m=0\) on the
time-zero event \(\|X_0\|_1>m\). All integration estimates below concern
\(s<\tau_m\), so \(\|X_s\|_1\le m\). The endpoint at zero need not be
integrable: deterministic test convergence times finite \(\|X_0\|_1\)
gives almost-sure convergence. On the event \(\tau_m=0\), the integration
interval has length zero.

For \(w_k=v_k-v\), drift errors are bounded by

\[
mT\sup_{s\le T}(\|w_k'(s)\|+\|Aw_k(s)\|+\|(Aw_k(s))^*\|),
\]

and the \(Q\)-drift is bounded by
\(|\alpha|T\|Q\|\sup_s\|w_k(s)\|_1\). The latter tends to zero because
\(\operatorname{rank}w_k\le2n\) and \(\|w_k\|_1\le2n\|w_k\|\).
The noise integrand error is \(2\sqrt X w_k\sqrt Q\), with

\[
\|2\sqrt X w_k\sqrt Q\|_2^2
\le4m\|Q\|\|w_k\|^2.
\]

The Itô isometry and the maximal inequality give stopped convergence in
\(L^2\), uniformly in time. Therefore the moving scalar identity holds.
Countably many approximants allow one common event of probability one.
Trace-norm continuity makes \(\sup_{s\le T}\|X_s\|_1<\infty\) almost
surely, so the stopped identities exhaust every finite interval. This provides
a local scalar semimartingale identity; no trace-class-valued stochastic
differential for the entire operator is presumed.

For \(\ell\in D(A^2)\), \(S(s)\ell\) meets the graph-\(C^1\) condition:
its derivative is \(S(s)A\ell\), whose image under \(A\) is
\(S(s)A^2\ell\). The squared-resolvent approximation makes \(D(A^2)\)
dense. Thus arbitrarily large finite domain-admissible orthonormal systems
exist. The use of this smaller test domain does not reduce the dimensions
available to the proof.

## Backward transform, signs, and filtration

With \(B=S(s)L\), \(D=I+2L^*C_sL\), differentiation yields
\(B'=AB\), \(D'=2B^*QB\), and

\[
\psi'=A\psi+(A\psi)^*-2\psi Q\psi,
\qquad \phi'=\alpha\operatorname{tr}(Q\psi).
\]

The weak drift paired with a self-adjoint test \(v\) is
\(\alpha\operatorname{tr}(Qv)+\operatorname{tr}[X(Av+(Av)^*)]\).
The two noise terms have combined matrix-direction functional
\(E\mapsto2\operatorname{tr}(\sqrt Q v\sqrt X E)\), represented under
the real Hilbert-Schmidt pairing by \(2\sqrt X v\sqrt Q\). Hence its
bracket is \(4\operatorname{tr}(XvQv)\,ds\). They use the same Brownian
motion, so their cross variation is essential.

For \(Z_s=-\phi_{T-s}-\operatorname{tr}(\psi_{T-s}X_s)\), the drift is
\(-2\operatorname{tr}(X_s\psi_{T-s}Q\psi_{T-s})\). Half of its bracket
is the positive opposite term. Thus \(F=e^Z\) is a local martingale.
Positivity bounds it by the deterministic finite constant
\(\exp(\sup_{r\le T}|\phi_r|)\), for every real \(\alpha\). It is a true
martingale and gives the conditional transform relative to \(\mathcal F_0\).
This uses Brownian noise relative to the solution filtration, as explicitly
stated in the current candidate.

The tower property then conditions on \(X_0\). A disintegration of the joint
law of \((X_0,J^*X_TJ)\) exists on standard Borel state spaces. A countable
dense set of positive matrix tests fixes one common initial-value null set;
continuity extends the conditional transform throughout the closed positive
cone. No law of a conditioned entire stochastic path is required.

## Independent finite-positivity mechanism in all dimensions

Whiten one conditional law to have transform

\[
L(v)=\det(I+2v)^{-\alpha/2}
\exp[-\operatorname{tr}\{Bv(I+2v)^{-1}\}],\qquad B\ge0.
\]

For \(r>0\), tilt its probability measure by
\(e^{-r\operatorname{tr}Y}/L(rI)\). Under this measure rescale by
\(a=1+2r\). Direct division of the transforms gives

\[
L_r(v)=L(rI+av)/L(rI)
=\det(I+2v)^{-\alpha/2}
\exp[-a^{-1}\operatorname{tr}\{Bv(I+2v)^{-1}\}].
\]

Differentiation under the tilted measure is legitimate because a polynomial
in \(\operatorname{tr}Y\) times \(e^{-r\operatorname{tr}Y}\) is bounded.
The mean trace after rescaling is \(n\alpha+\operatorname{tr}B/a\).
After excluding negative \(\alpha\) by the scalar-transform growth test,
these means are bounded for \(r\ge1\). Positive matrices of bounded trace
form compact sets, so the laws are tight. A subsequential weak limit as
\(r\to\infty\) has the central full-matrix transform
\(\det(I+2v)^{-\alpha/2}\). This explains why any finite noncentral matrix
cannot rescue a forbidden central parameter.

Let \(\mathcal D_{ii}=\partial_{v_{ii}}\) and
\(\mathcal D_{ij}=\tfrac12\partial_{v_{ij}}\) for \(i<j\). Then
\(\det(-\mathcal D)e^{-\operatorname{tr}(vY)}
=\det(Y)e^{-\operatorname{tr}(vY)}\).
At \(v=sI>0\), derivatives through order \(n\) may be passed under the
expectation: each \(|Y_{ij}|\le\operatorname{tr}Y\), and the exponential
damps every required polynomial in the trace. No unweighted determinant
moment is assumed.

The derivative at \(sI\) has the form
\((1+2s)^{-n\alpha/2-n}P_n(\alpha)\). The coefficient \(P_n\) is a
polynomial of degree at most \(n\), by differentiating the exponential of
\(-\tfrac\alpha2\log\det(I+2v)\). For every integer \(m\ge n\), the
explicit Gaussian matrix \(Y=GG^*\), with \(G\) an \(n\)-by-\(m\) matrix
of independent standard real Gaussians, has that transform at \(\alpha=m\).
Cauchy-Binet and row independence give

\[
\mathbb E\det(GG^*)=\binom mn\mathbb E(\det G_{n\times n})^2
=\binom mn n!=\prod_{j=0}^{n-1}(m-j).
\]

Tilting all Gaussians by \(e^{-s\operatorname{tr}(GG^*)}\) rescales their
variance by \((1+2s)^{-1}\), with normalizing factor
\((1+2s)^{-nm/2}\). Therefore polynomial interpolation at infinitely many
integer \(m\) proves, for every real \(\alpha\),

\[
\mathbb E[\det Y\,e^{-s\operatorname{tr}Y}]
=\prod_{j=0}^{n-1}(\alpha-j)
(1+2s)^{-n\alpha/2-n}.
\]

This interpolates a finite derivative of an explicit analytic function; it
does not posit any noninteger law. For noninteger \(\alpha\ge0\), choose
\(n=\lfloor\alpha\rfloor+2\). Exactly the last factor is negative, a
contradiction to the nonnegative left side. The new Fraction Taylor-jet
program independently checks the normalization in dimensions 1--4 and tests
the noncentral tilted determinant at \(\alpha=3/2\). This mechanism is
supplementary; the candidate's imported GMM fixed-law argument is valid.

## Counterexample searches and exact boundaries

Take \(H=L^2(0,\infty)\), \((S(t)f)(x)=f(x+t)\), and \(Q=I\).
This strongly continuous contraction has a nontrivial kernel for every
positive time. Its generator \(Af=f'\), \(D(A)=H^1(0,\infty)\), is
unbounded. Fubini gives \(C_t f(x)=\min(t,x)f(x)\). Its quadratic form is
strictly positive, but it has an infinite-dimensional eigenspace at eigenvalue
\(t\) on functions supported beyond \(t\). Thus it is noncompact and not
trace class. Disjoint smooth normalized bumps supported strictly within
\((0,T)\) are in \(D(A^2)\), killed by \(S(T)\), and have positive
diagonal compressed covariance. Symmetric bumps on \((a,b)\subset(0,T)\)
have diagonal covariance \((a+b)/2\). This directly stresses both extensions.

In one dimension noninteger nonnegative drift is possible for squared Bessel
processes; thus a finite-dimensional version of the asserted conclusion is
false. With rank-one \(Q\), the scalar process embeds in infinite dimension,
so removing injectivity is also false. At \(\alpha=0,X_0=0\), the identically
zero process solves every displayed scalar equation, including for the above
unbounded shift generator. Negative \(\alpha\) is impossible because the
one-dimensional conditional transform grows above one at large tests.

The heavy-tailed law \(\mathbb P(Z=2^k)=2^{-k}\), \(k\ge1\), has finite
values almost surely and infinite mean. Hypothetical initial data
\(X_0=Z e\otimes e\) therefore test the necessity argument's absence of
initial moments. The stopped estimates and bounded exponential above remain
valid. This stress test constructs initial data, not a Wishart solution for
arbitrary operators or parameters.

No tested escape supplied a counterexample under the exact hypotheses.
