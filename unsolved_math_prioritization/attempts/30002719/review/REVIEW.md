# Independent review of the Waring-series return-time obstructions

**Verdict: PASS_SCOPED_RETURN_AND_FINITE_STATE_OBSTRUCTIONS.** No mandatory correction was found. Recommend **unsolved, 2/5** for the original probabilistic-interpretation problem. The reversible first-return obstruction and the finite-state hitting-time obstruction are proved within their stated classes. They neither disprove coefficient positivity nor exclude nonreversible infinite-state constructions or other random variables.

Reviewed on 30 September 2026 by a separate GPT-6 Astra agent at xhigh effort. This is an independent AI mathematical review, not human peer review or a novelty certification. The frozen OBSTRUCTION.md has SHA-256
**6faa3211dd30fe4495259bd878d0db8ed6c2523f9a6483fd30bc9a1c5f9d480d**.

## Exact source and prior work

I independently read the Fill–Sokal contribution in [OWR 50/2014](https://publications.mfo.de/bitstream/handle/mfo/3440/OWR_2014_50.pdf?isAllowed=y&sequence=1), pp. 2845–2848, and visually checked the definitions and coefficient-stabilization identity on p. 2847 and the question on p. 2848. The source asks for a readily described random variable with the displayed probability-generating function; it does not restrict the answer to Markov first returns.

The chosen formal root has constant term one. The candidate uses the correct normalization of the logarithmic coefficient and the correct strict inequality $k<n$ in the stabilization statement. The source credits small-$n$ probability results and nonprobabilistic positivity for $n=4,5$, as the artifact reports.

I also checked Theme 3, pp. 5–6, of [Sokal's primary proposal](https://www.homepages.ucl.ac.uk/~ucahad0/sokal_EPSRC_research.pdf). It explicitly credits Fill's $n=2,3$ birth-and-death interpretations and their failure to extend to $n\ge4$. The package acknowledges that prior limitation. The broader reversible-return certificate is not accompanied by a historical-priority claim. The proposal gives no detailed chain construction, and none is inferred here.

The inspected [Kuznetsov preprint](https://arxiv.org/abs/2412.02462) concerns zero expansions and related positivity evidence. Its current arXiv page has only v1. The cited recurrence and scope are consistent with the artifact; the paper's complete analytic proofs are not inputs to this audit.

## Renewal transform and reversible moment necessity

Let $f_j$ be the first positive return probabilities to $o$, including the possibility that their sum is below one. Decomposition according to the first return gives, for $k\ge1$,
\[
P^k(o,o)=\sum_{j=1}^k f_jP^{k-j}(o,o).
\]
This finite identity at each degree proves the formal renewal equation. Neither recurrence nor finite expectation is required. Thus the proposed first-return PGF forces
\[
\sum_{k\ge0}P^k(o,o)y^k=(1-F_n(y))^{-1}=A_n(y)^{-1/n}.
\]

Under the stated detailed-balance assumptions, $\pi$ is invariant. For a finitely supported function $h$, Jensen's inequality and nonnegative summation give
\[
\sum_x\pi(x)|Ph(x)|^2
\le\sum_{x,y}\pi(x)P(x,y)|h(y)|^2
=\sum_y\pi(y)|h(y)|^2.
\]
Consequently $P$ extends to a contraction on $\ell^2(\pi)$. Detailed balance gives symmetry on the dense finitely supported subspace and hence self-adjointness of the bounded extension. Finite total mass is unnecessary; the assumption $0<\pi(o)<\infty$ makes the normalized point vector legitimate.

For $e=\mathbf1_{\{o\}}/\sqrt{\pi(o)}$, direct evaluation shows $\langle e,P^ke\rangle=P^k(o,o)$. Therefore the Hankel quadratic form for any real polynomial is $\|q(P)e\|^2\ge0$. Equivalently, the spectral measure is a probability measure on $[-1,1]$. Nothing in the argument restricts it to $[0,1]$. This correctly avoids the stronger, inapplicable nonnegative-spectrum requirement.

## Exact polynomial certificate and infinite-$n$ coverage

I independently reconstructed $A_n$ directly from the literal expansion of $\log(1+(f-1))$, grouping integer partitions of the $x$-degree. I then formed $A_n^{-1/n}$ by the ordinary formal binomial series, without using the submitted connected-graph or Newton recurrences. This reproduces all displayed moments through degree eight.

For
\[
q(t)=-1+132t-108t^2-264t^3+240t^4,
\]
the quadratic forms are exactly
\[
-\frac{25059}{32},\quad -\frac{1016}{5},\quad
-\frac{153}{2},\quad -\frac{2070}{7},\quad
-\frac{2265}{8}
\]
for $n=4,5,6,7,8$, respectively. Each is strictly negative.

For $n\ge9$, the credited equality $F_n\equiv F\pmod{y^n}$ remains valid after inverting the unit series $1-F_n$ and $1-F$. It therefore identifies all required moments through degree eight with those of $U$. The leading-root equation is
\[
f(-U,y)=1-U+\frac y2U^2-\frac{y^3}{6}U^3+
\frac{y^6}{24}U^4+O(y^{10})=0.
\]
The terms with index at least five begin in degree ten. At each positive degree, the new coefficient of $U$ occurs with coefficient $-1$; every other contribution uses earlier coefficients. Successive solution gives the submitted stable row and the quadratic-form value **$-255$**.

This proves the obstruction for every $n\ge9$, rather than extrapolating the finite screen. Together with the five smaller cases it excludes all $n\ge4$ in precisely the stated reversible first-return class, including defective laws.

The warning about log-convexity is mathematically appropriate: a nonnegative spectral support would imply the relevant log-convex inequalities, but reversibility alone does not. The argument does not use log-convexity as a characterization. As an independent control, the $n=3$ moments match the affine image $-1/2+(3/2)X$ of a Beta$(2/3,1/3)$ probability law. This has permissible negative spectral support while $g_1g_3-g_2^2=-1/24$.

## Coefficient recurrences and the branch obstruction

The connected-graph formula follows from the labeled exponential formula: all simple graphs have total weight $(1+v)^{\binom n2}$, and logarithm extracts connected components. Conditioning on the connected component of vertex one gives exactly the submitted recurrence. Its factorial and alternating signs agree with the definition of $A_n$.

For $B=A^s$, coefficient comparison in $AB'=sA'B$ yields the stated rational recurrence. The factor multiplying $a_i b_{j-i}$ is $(s+1)i-j$, with the overall denominator $j$; there is no lost normalization.

Connected graphs on $n$ vertices have at least $n-1$ edges, and spanning trees give a strictly positive coefficient at that degree. Therefore $A_n$ has a zero of exact order $n-1$ at $y=1$, with positive leading coefficient when expressed in $1-y$.

If $1-F_n$ were rational, its order at $1$ would be an integer. Its $n$th power would have order divisible by $n$, contradicting $n-1$. This proves nonrationality for all $n\ge2$ without making any coefficient-positivity assumption.

A finite-state time-homogeneous hitting-time PGF is a finite matrix-resolvent expression, with a possible constant term for an initial state in the target. The inverse $(I-yQ)^{-1}$ exists formally at zero whether or not the target is reached almost surely. Separating the first step handles first positive returns. All such PGFs are rational, so the claimed finite-state exclusion is valid, including defective cases and arbitrary fixed initial distributions.

The infinite-mean conclusion is correctly conditional. If $F_n$ is a PGF, then $1-F_n(y)>0$ for $0\le y<1$ and its $n$th power is $A_n(y)$. Near one it is a positive analytic factor times $(1-y)^{(n-1)/n}$. Differentiation gives divergence of $F_n'(y)$, and monotone convergence of the nonnegative PGF coefficients yields infinite expectation. This neither establishes nonnegativity nor assumes a finite mean.

## Verification, limitations, and publication

All **2,728** submitted exact assertions replay successfully and reproduce the original receipt byte for byte. The submitted checker includes **1,098** exhaustively enumerated small graphs and the explicitly bounded positivity screen.

My independently written verifier passes **346** exact assertions. It uses a different literal-logarithm and binomial-expansion calculation, checks the zero orders directly from the resulting polynomials, solves the leading-root equation coefficient by coefficient, and tests the quadratic-form identity on 100 exact two-state reversible chains, including negative nontrivial eigenvalues.

These checks support the written proofs; they do not prove arbitrary-degree coefficient positivity. The simple countdown construction for an already specified distribution assumes that positivity and does not furnish the requested explanatory interpretation. Hitting a different state in an infinite chain, nonreversible chains, transformed stopping times, and other random variables remain outside the obstruction.

The original target remains **unsolved, 2/5**. The frozen author file is unchanged. Eight self-contained publication files, including the required snapshot and exact check receipts, are listed in review_summary.json. Source PDFs, source images, and redundant stdout captures are excluded.
