# Waring-series return-time obstructions

Status: the original probabilistic interpretation remains **unsolved, 2/5 substantive approach families**. Separate adversarial review is pending. This note gives an exact obstruction to a restricted realization, not a counterexample to coefficient positivity. No novelty claim is made.

## 1. Exact question and credited starting point

James Allen Fill's contribution, joint with Alan D. Sokal, to *Probability, Trees and Algorithms*, Oberwolfach Report 50/2014, printed pp.2845–2848, defines
\[
f(x,y)=\sum_{j\ge0}\frac{x^j y^{j(j-1)/2}}{j!},\qquad
A_n(y)=(-1)^{n-1}n[x^n]\log f(x,y),\qquad
F_n(y)=1-A_n(y)^{1/n}.
\tag{1}
\]
The formal root is the one with constant term one. The nontrivial probability question concerns integers \(n\ge2\). It asks for a readily describable random variable with PGF \(F_n\). The source already proves the PGF assertion for \(n=2,3\), and states that nonprobabilistic methods give coefficient positivity for \(n=4,5\).

Write \(U(y)=-x_0(y)\), where \(x_0\) is the formal leading root, so \(U(0)=1\), and set \(F=1-U^{-1}\). The source's equation (1), printed p.2847, gives
\[
F_n\equiv F\pmod{y^n},\qquad
G_n:=\frac1{1-F_n}=A_n^{-1/n}\equiv U\pmod{y^n}.
\tag{2}
\]
We use this credited coefficient-stabilization identity. It is not a result of our finite computations.

Sokal's primary EPSRC research proposal, Theme 3, printed pp.5–6, explicitly credits Fill with birth-and-death interpretations for \(n=2,3\) and reports that this interpretation cannot extend to \(n\ge4\). Thus the birth-and-death obstruction is already known. The certificate below explains a broader reversible-return obstruction without claiming priority for that extension. It leaves unrestricted random variables and nonreversible constructions open.

## 2. A single polynomial excludes reversible returns for every n at least four

**Theorem.** For every integer \(n\ge4\), \(F_n\) cannot be the first positive return-time generating function at a state of a time-homogeneous, countable-state reversible Markov chain. Here reversibility means detailed balance with respect to a measure \(\pi\) having \(0<\pi(x)<\infty\) at each state in the communicating class under consideration. The measure need not have finite total mass. A possibly defective first-return law is also excluded.

**Proof.** Suppose the first-return series is \(F_n\), and let \(g_k=P^k(o,o)\), with \(g_0=1\). Decomposition at the first positive return gives the formal renewal equation
\[
\sum_{k\ge0}g_k y^k=1+F_n(y)\sum_{k\ge0}g_k y^k=G_n(y).
\tag{3}
\]
This identity does not assume recurrence or finite mean return time.

The transition operator \(P\) is a self-adjoint contraction on \(\ell^2(\pi)\). Indeed, detailed balance gives self-adjointness on finitely supported vectors, while Jensen's inequality and invariance of \(\pi\) give the contraction bound; these extend the operator and identity to all of \(\ell^2(\pi)\). With \(e=\mathbf1_{\{o\}}/\sqrt{\pi(o)}\), we have
\[
g_k=\langle e,P^ke\rangle.
\]
Consequently, for every real polynomial \(q(t)=\sum_i q_i t^i\),
\[
\sum_{i,j}q_iq_jg_{i+j}=\|q(P)e\|^2\ge0.
\tag{4}
\]

Take the integer polynomial
\[
q(t)=240t^4-264t^3-108t^2+132t-1.
\tag{5}
\]
The exact coefficients of \(G_n\) through degree eight are listed below. The first four entries, common to all rows, are
\[
(g_0,g_1,g_2,g_3)=(1,1/2,1/2,11/24).
\]

| n | g4 | g5 | g6 | g7 | g8 | sum q_i q_j g_(i+j) |
|---|---|---|---|---|---|---|
| 4 | 85/192 | 157/384 | 461/1152 | 589/1536 | 9167/24576 | -25059/32 |
| 5 | 11/24 | 69/160 | 407/960 | 49/120 | 767/1920 | -1016/5 |
| 6 | 11/24 | 7/16 | 167/384 | 971/2304 | 53/128 | -153/2 |
| 7 | 11/24 | 7/16 | 7/16 | 1721/4032 | 755/1792 | -2070/7 |
| 8 | 11/24 | 7/16 | 7/16 | 493/1152 | 2605/6144 | -2265/8 |
| every n≥9 | 11/24 | 7/16 | 7/16 | 493/1152 | 163/384 | -255 |

Every entry in the last column is negative, contradicting (4). For \(n=4,\ldots,8\), the table follows directly from (1) and the rational coefficient recurrence in Section 3. For all \(n\ge9\), equation (2) reduces the required eight coefficients to the one formal identity
\[
1-U+\frac y2U^2-\frac{y^3}{6}U^3+\frac{y^6}{24}U^4
\equiv0\pmod{y^9}.
\tag{6}
\]
Terms from \(j\ge5\) begin in degree ten. Solving successively, using the coefficient \(-1\) of \(U\) in degree zero, gives exactly the last row. This proves the assertion for infinitely many \(n\), rather than extrapolating a finite test. QED.

In particular, passing from birth-and-death chains to arbitrary reversible chains does not repair that particular first-return construction. Hitting a different state, nonreversible chains, transformed stopping times, and other random variables are not covered by this theorem.

## 3. Exact coefficient calculations

Let \(C_n(v)\) be the sum of \(v^{|E|}\) over connected simple graphs on the labeled vertex set \([n]\), and put \(\bar C_n(y)=C_n(y-1)\). The exponential formula gives
\[
A_n(y)=\frac{(-1)^{n-1}}{(n-1)!}\bar C_n(y).
\tag{7}
\]
For completeness, the total weighted sum over all graphs is \((1+v)^{\binom n2}\). Decomposing the connected components is precisely the labeled exponential formula, hence the logarithm in (1) extracts \(C_n/n!\). Alternatively, specifying the component of vertex 1 gives the finite recurrence
\[
\bar C_1=1,\qquad
\bar C_n=y^{\binom n2}-\sum_{k=1}^{n-1}\binom{n-1}{k-1}\bar C_k\,y^{\binom{n-k}2}.
\tag{8}
\]
This is also recorded in Kuznetsov's 2024 primary preprint, equation (5).

If \(A=\sum a_i y^i\), \(a_0=1\), and \(B=A^s=\sum b_jy^j\), \(b_0=1\), logarithmic differentiation \(AB'=sA'B\) gives
\[
b_j=\frac1j\sum_{i=1}^{\min(j,\deg A)}((s+1)i-j)a_i b_{j-i}.
\tag{9}
\]
Use \(s=-1/n\) for the displayed return coefficients, and \(s=1/n\) for \(1-F_n\). All table entries therefore have short exact rational certificates. The accompanying checker also derives \(A_n\) independently from Newton's power-sum recurrence and enumerates all simple graphs through five vertices to verify (7).

A simpler proposed positivity shortcut fails even before the reversible obstruction: the coefficients of \(G_n\) are not log-convex. For \(n=3\), \(g_1g_3-g_2^2=-1/24\); for every \(n\ge4\), it is \(-1/48\). The case \(n=3\) is consistent with an actual reversible birth-and-death construction: log-convexity would correspond to a nonnegative spectral support, whereas reversible transition operators may have negative spectrum. We do not confuse this stronger condition with the positive-semidefinite condition (4).

## 4. Finite-state hitting times and infinite mean

**Proposition.** For every \(n\ge2\), \(F_n\) is not a rational function. It therefore cannot be the ordinary step-count hitting-time PGF of a time-homogeneous finite-state Markov chain, for any fixed initial distribution and target set. First positive returns are included after separating the first step.

**Proof.** Every connected graph has at least \(n-1\) edges, and the coefficient of that lowest power in \(C_n(v)\) is the positive number \(\tau_n\) of labeled spanning trees. Equation (7) gives
\[
A_n(y)=\frac{\tau_n}{(n-1)!}(1-y)^{n-1}
+O((1-y)^n).
\tag{10}
\]
Thus \(A_n\) has a zero of exact order \(n-1\) at one. If \(1-F_n\) were rational, its order at one would be an integer, and the equation \((1-F_n)^n=A_n\) would force \(n\) to divide \(n-1\), impossible. For a finite-state chain, the transient-to-target generating function is a finite matrix expression involving \((I-yQ)^{-1}\), hence rational, even if the hitting law is defective. QED.

Conditionally on \(F_n\) being a probability generating function, its random variable has infinite expectation. Indeed, along real \(y\uparrow1\), (10) and the nonnegative root give
\[
1-F_n(y)\sim \left(\frac{\tau_n}{(n-1)!}\right)^{1/n}(1-y)^{(n-1)/n}.
\]
Differentiating the analytic factor multiplying this fractional power shows \(F_n'(y)\) tends to infinity. Monotone convergence then gives infinite mean. This argument does not assert coefficient positivity.

For comparison, the known case \(n=2\) is \(F_2=1-\sqrt{1-y}\). It is the Sibuya law of parameter \(1/2\), with
\[
\Pr(N=k)=\frac{\binom{2k}{k}}{(2k-1)4^k},\quad k\ge1.
\]
This is only a credited elementary control, not a solution of the general problem.

## 5. Exact remaining gap and literature limits

We have neither proved nor refuted nonnegativity of every coefficient of \(F_n\) for every \(n\ge2\), nor produced the requested non-tautological probabilistic description. A countable nonreversible countdown chain can encode any already-known positive distribution: from state zero choose a length using its probabilities and count down deterministically. That construction assumes the very coefficient positivity at issue and supplies no explanation of the connected-graph polynomials.

Kuznetsov's full primary preprint, arXiv:2412.02462v1, studies expansions of individual zeros and supplies evidence for the related Sokal conjectures; it does not prove this general Waring-series PGF assertion. Its current arXiv page lists only v1, submitted 3 December 2024, and no journal reference or withdrawal notice. We did not independently audit all of its analytic proofs. Sokal's proposal already identifies the small-n birth-and-death limitation, so no discovery credit is inferred from the overlap.

The finite coefficient screen is evidence only. Its rational arithmetic passes for \(2\le n\le16\) through degree160, but this neither establishes positivity at every degree nor over all \(n\). Numerical root-location diagnostics from preliminary triage are not used as certificates. The original target remains unresolved; the reversible-return route is closed by the exact theorem above.

## Sources

1. J. A. Fill, joint with A. D. Sokal, contribution pp.2845–2848 in [Oberwolfach Report 50/2014](https://publications.mfo.de/bitstream/handle/mfo/3440/OWR_2014_50.pdf?isAllowed=y&sequence=1), DOI10.4171/OWR/2014/50. Full contribution read; formulas and question on pp.2847–2848 visually verified.
2. A. D. Sokal, [Positivity problems at the boundary between combinatorics and analysis](https://www.homepages.ucl.ac.uk/~ucahad0/sokal_EPSRC_research.pdf), EPSRC research proposal, Theme3, printed pp.5–6. Full proposal retrieved. No publication date is inferred from the undated title page.
3. A. Kuznetsov, [On series expansions of zeros of the deformed exponential function](https://arxiv.org/abs/2412.02462), v1, 3 December2024; full PDF retrieved. Introduction, equations(3)–(6), main statements and conjecture scope checked.
