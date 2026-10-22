# Phase asymptotics for repeated running LCM tails

## Publication edition

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance is limited to the stated partial analytic result. No external human peer review, journal acceptance, formal proof-assistant certification, exhaustive priority search, or novelty certification is claimed.

This prose-only edition preserves the complete mathematical arguments. References below to programs, finite-check results, and original packet integrity describe the historical verification record of 10 October 2026. Programs, detailed outputs and original executable packets are not distributed here; this edition is not an executable reproduction package. The source comparison is to the retained hash-pinned manuscript, not a verified latest online revision. Edition preparation added no scholarly-source retrieval or inspection.

## Result and scope

The original question remains unresolved here. For a finite set $P$ of at least two primes, list **every** positive $P$-smooth integer, including 1, as $a_1<a_2<\cdots$. Erdős's question is whether

$$
R_P=\sum_{n\ge1}\frac1{\operatorname{lcm}(a_1,\ldots,a_n)}
$$

is irrational. Equal successive LCMs contribute repeatedly. The 1973 letter explicitly separates this question from its distinct-value version [1].

This note makes one attack on the residual case with multiplicities: can the polynomial growth of normalized tails be removed by polynomial corrections so that a bounded-state irrationality argument becomes available? The answer is **no**, even if one may choose arbitrarily among any fixed finite collection of real polynomials. We prove an explicit phase asymptotic for the actual repeated tails. On every arithmetic progression their leading normalized values have a nondegenerate interval of subsequential limits. For $P=\{2,3,5\}$, the oscillation has an explicit positive lower bound. In particular, every fixed-period quasipolynomial correction leaves an error at least of quadratic size along a subsequence.

These are statements about the original repeated tails, not a replacement numerator sequence. They do not prove irrationality: a rational value would supply integral carries that need not be quasipolynomial.

Relative to the inspected 5 October 2026 manuscript of Cook [2], the additional statements are the phase-profile asymptotic, its interval of limits on **each** arithmetic progression without assuming rational independence of reciprocal prime logarithms, and the resulting obstruction to every finite collection of polynomial corrections. Cook's Sections 8–9 give quadratic upper and lower bounds; Section 9 explicitly does not assert an asymptotic constant. Sections 5.5 and 12.2 explain unbounded tails and the survival of boundary strips in weighted differences. The present argument does not repeat that finite-difference counterexample, the distinct-value proof, or the finite residue scans. This is a comparison with that manuscript, not a claim to an exhaustive priority search.

## 1 The actual tails and the phase profile

Let $P=\{p,q_1,\ldots,q_s\}$, where $p=\min P$, so $s=|P|-1\ge1$. Put

$$
H(x)=\prod_{r\in P}r^{\lfloor\log_r x\rfloor},\qquad
P_a=H(p^a),\qquad
X_a=\frac{P_a}{p}\sum_{\substack{n\ P\text{-smooth}\\n\ge p^a}}\frac1{H(n)}.
\tag{1}
$$

The running LCM at cutoff $x$ is $H(x)$: each smooth number at most $x$ divides it, and the largest permitted power of each prime is itself in the prefix. Thus (1) retains all occurrences. Also $H(n)>n^{s+1}/\prod_{r\in P}r$, so convergence follows from the product of the $s+1$ convergent geometric series obtained by summing $n^{-(s+1)}$ over smooth $n$.

Write

$$
\lambda_j=\log_p q_j>1,\quad \theta_j=1/\lambda_j,\quad
x_a=(\{a\theta_1\},\ldots,\{a\theta_s\}),\quad
C_P=\frac1{p\,s!\,\prod_{j=1}^s\lambda_j}.
$$

For $x\in[0,1]^s$, including the closed faces, define

$$
I_P(x)=\int_0^\infty
p^{-\lfloor u\rfloor}\prod_{j=1}^s q_j^{-\lfloor x_j+\theta_j u\rfloor}\,du,
\qquad F_P(x)=C_P I_P(x).
\tag{2}
$$

**Theorem 1 (phase asymptotic).** For the repeated tails (1),

$$
\boxed{\quad X_a=a^sF_P(x_a)+o(a^s)\quad(a\to\infty).\quad}
\tag{3}
$$

No rational-independence assertion about $1,\theta_1,\ldots,\theta_s$ is used. The only logarithmic irrationality needed in the counting step is that one $\lambda_j$ is irrational, which follows from unique factorization.

The integral is positive and continuous on the **closed cube**, and obeys the face identities

$$
I_P(x_1,\ldots,x_{j-1},1,x_{j+1},\ldots,x_s)
=q_j^{-1}I_P(x_1,\ldots,x_{j-1},0,x_{j+1},\ldots,x_s).
\tag{4}
$$

It consequently does not define a continuous function on the torus obtained by identifying opposite faces. Those nontrivial face jumps will be essential.

## 2 Uniform counting in a simplex

We use the following elementary uniform form of irrational-rotation equidistribution.

**Lemma 2.** Let $\lambda_1,\ldots,\lambda_s>0$, with $\lambda_1$ irrational. For $T>0$, let

$$
\mathcal T_T=\{k\in\mathbb Z_{\ge0}^s:k\cdot\lambda<T\}.
$$

Uniformly over intervals $J\subset[0,1)$,

$$
\#\{k\in\mathcal T_T:\{k\cdot\lambda\}\in J\}
=|J|\frac{T^s}{s!\prod_j\lambda_j}+o(T^s).
\tag{5}
$$

Endpoints may be assigned by any fixed half-open convention.

**Proof.** First,

$$
\#\mathcal T_T=\frac{T^s}{s!\prod_j\lambda_j}+O(T^{s-1}).
\tag{6}
$$

Indeed, surround every lattice point by its unit cube. These cubes contain the nonnegative simplex of parameter $T$ and are contained in the simplex of parameter $T+\sum_j\lambda_j$, up to boundary sets of measure zero. Taking volumes proves (6).

For an irrational rotation $\lambda_1$, for every $\varepsilon>0$ there is $A_\varepsilon$ such that, for every integer $L\ge0$, phase $z$, and interval $J$,

$$
\left|\sum_{i=0}^{L-1}{\bf1}_J(\{z+i\lambda_1\})-L|J|\right|
\le\varepsilon L+A_\varepsilon.
\tag{7}
$$

For completeness, the normalized exponential sum at every nonzero integer frequency $h$ is bounded by $2/(L|1-e^{2\pi i h\lambda_1}|)$, independently of $z$. Approximate continuous periodic functions by trigonometric polynomials to obtain uniform equidistribution in $z$. Approximate interval indicators from above and below using a fixed fine grid and continuous functions; only finitely many grid endpoints occur, giving uniformity in $J$. The finitely many small $L$ are absorbed into $A_\varepsilon$. This proves (7).

Fix $k_2,\ldots,k_s$. The allowed $k_1$'s form an initial interval of integers, so (7) applies to that row. There are $O(T^{s-1})$ rows, and their lengths sum to $\#\mathcal T_T$. Summing (7), dividing by $T^s$, and then letting $\varepsilon\downarrow0$, proves (5). For $s=1$, there is a single row. The argument is unchanged at strict endpoints. ∎

In particular, (5) applies uniformly to step functions with a bounded number of pieces and uniformly bounded values: write the weighted sum as the sum over its disjoint interval pieces. This remains valid when the interval endpoints depend on $T$.

## 3 Proof of the phase asymptotic

Let

$$
s_a=\sum_{\substack{n\ P\text{-smooth}\\p^a\le n<p^{a+1}}}H(n)^{-1},
\qquad M_a=P_a s_a.
$$

An integer with $p$-free part $\prod_jq_j^{k_j}$, whose logarithm to base $p$ is $w=k\cdot\lambda<a+1$, has exactly one multiple by a nonnegative power of $p$ in this shell. It is

$$
n=p^{a-\lfloor w\rfloor}\prod_jq_j^{k_j}=p^{a+\{w\}}.
$$

Therefore the **exact** shell identity is

$$
M_a=\sum_{k\in\mathcal T_{a+1}}
\prod_jq_j^{-\lfloor (x_a)_j+\theta_j\{k\cdot\lambda\}\rfloor}.
\tag{8}
$$

Each factor in (8) has at most one jump as the fractional part varies over $[0,1)$, because $0<\theta_j<1$. The product is between $1/\prod_jq_j$ and 1 and has at most $s$ jumps. Lemma 2 thus gives

$$
M_a=\frac{a^s}{s!\prod_j\lambda_j}
\int_0^1\prod_jq_j^{-\lfloor (x_a)_j+\theta_jt\rfloor}\,dt+o(a^s).
\tag{9}
$$

Replacing $(a+1)^s$ by $a^s$ changes only $O(a^{s-1})$. Importantly, the discrepancy estimate is uniform over the moving step-function endpoints.

For an integer $r\ge0$, exact floor addition gives

$$
\frac{P_a}{P_{a+r}}=p^{-r}\prod_jq_j^{-\lfloor (x_a)_j+r\theta_j\rfloor}.
\tag{10}
$$

Using (9) at $a+r$, multiplication by (10) joins the two floor differences, so its limiting integral becomes the part of (2) over $[r,r+1)$. Since

$$
X_a=\frac1p\sum_{r\ge0}\frac{P_a}{P_{a+r}}M_{a+r},
\tag{11}
$$

summing these pieces proves (3), provided that the passage through the infinite sum is justified.

Here is a uniform summable bound. Because each $\lambda_j>1$, the $s$ exponents in $\mathcal T_{b+1}$ each lie between 0 and $b$, and (8) gives $M_b\le(b+1)^s$. With $Q=\prod_jq_j$, (10) gives

$$
0<\frac{P_a}{P_{a+r}}\le Qp^{-(s+1)r}.
$$

For $a\ge1$, the $r$-th summand in (11), divided by $a^s$, is consequently at most

$$
\frac Qp\,p^{-(s+1)r}(r+2)^s.
$$

This is summable, independently of $a$. First keep finitely many $r$, use (9), and then send the truncation to infinity. The same majorant applies to the integrals. This proves (3).

Finally the integrand in (2) is bounded by $pQ\,p^{-(s+1)u}$, independently of $x\in[0,1]^s$. For a convergent sequence of phases it converges pointwise except at a countable set of $u$'s. Dominated convergence proves continuity on the closed cube. Positivity is immediate. Shifting one face coordinate from 0 to 1 shifts its floor by exactly 1, proving (4). ∎

## 4 Oscillation on every arithmetic progression

**Theorem 3.** For every integer $m\ge1$ and residue $r$, the sequence

$$
\left(\frac{X_a}{a^s}\right)_{a\to\infty,\ a\equiv r\pmod m}
$$

has a nondegenerate interval of positive subsequential limits. In particular it has at least two distinct positive subsequential limits. This holds for every finite prime set with at least two elements.

We include the torus argument to avoid assuming the stronger assertion, not proved here, that $1$ and the reciprocal prime logarithms are rationally independent.

**Torus lemma.** Let $\theta\in\mathbb R^s$, with every coordinate irrational. The closure of $(r+mn)\theta\bmod1$ is a coset of a compact subgroup $K$ of the torus. Its identity component $K^0$ has positive dimension and has nontrivial projection onto every coordinate circle. Every nonempty relatively open subset of this coset is visited infinitely often.

**Justification.** Let

$$
\Lambda=\{h\in\mathbb Z^s:m h\cdot\theta\in\mathbb Z\}.
$$

The subgroup defined by $h\cdot x\in\mathbb Z$ for all $h\in\Lambda$ is a finite union of subtori: choose a finite integer basis of the subgroup $\Lambda\subset\mathbb Z^s$ and use Smith normal form on the resulting integer matrix. Geometric summation of each character shows that the Cesàro Fourier coefficients of $nm\theta$ equal those of Haar measure on this subgroup. Trigonometric-polynomial approximation gives equidistribution there, hence identifies it with $K$ and proves the infinite-visit assertion; translation gives the coset for $r$. If the tangent space of $K^0$ had zero projection on coordinate $j$, then the entire coordinate image of $K$ would be finite. This would make $m\theta_j$, and hence $\theta_j$, rational, a contradiction. These facts also show that $K^0$ has positive dimension.

**Proof of Theorem 3.** Each $\theta_j=\log_{q_j}p$ is irrational by unique factorization, so apply the lemma. Write $L$ for the tangent space of $K^0$. Each coordinate functional is nonzero on $L$, so $L$ is not the union of their finitely many kernels. Choose $v\in L$ with every $v_j\ne0$.

Choose a point $z$ in a connected component of the orbit coset with at least one coordinate equal to zero on the torus. Such a point exists because the component's projection onto each coordinate circle is surjective. The small arc $z+tv$ remains in that component. Let $J\ne\varnothing$ be the set of coordinates of $z$ equal to zero. For small $t\ne0$, lift all coordinates to $(0,1)$. The two one-sided limits of $F_P(z+tv)$ exist by closed-cube continuity. By (4), their ratio, or its reciprocal depending on orientation, is

$$
\prod_{j\in J}q_j^{\operatorname{sgn}(v_j)}.
\tag{12}
$$

It is not 1: its factors are distinct primes with nonzero exponents $+1$ or $-1$. Both limits are positive. Infinite visits to arbitrarily small relatively open neighborhoods on either side of the arc supply subsequences of the **specified arithmetic progression** approaching these two limits. Combining with (3) proves the two-limit assertion. No approximation rate for those subsequences is needed.

To obtain an interval of limits, use the rationality of the tangent space $L$: it is the nullspace of integer equations from the torus lemma. We may therefore choose $v$ above to be an integer vector, still with every coordinate nonzero. Choose a point $z$ of the component with no coordinate on a face. Such points exist because no coordinate is constant on the component, so finitely many coordinate hyperplanes cannot cover it. The path $z+tv$, for $0\le t\le1$, is a closed loop. Its coordinates cross faces at only finitely many times.

Suppose that $F_P$ were constant on every open arc between consecutive crossings. Passing each crossing multiplies its one-sided value by the factor in (12), with the positive orientation of $t$. Over one full loop, coordinate $j$ crosses $|v_j|$ times, each with sign $\operatorname{sgn}(v_j)$. The total multiplicative change would be $\prod_j q_j^{v_j}$. But the initial and final phases are the same nonsingular point, so this product would have to be 1. Unique factorization contradicts the choice of the nonzero integer vector $v$.

Consequently $F_P$ is nonconstant on at least one nonsingular open arc. It is continuous there, so its image contains a nondegenerate closed interval of positive values. Every phase on that arc is a limit of the orbit of the specified arithmetic progression; at a nonsingular phase the profile is continuous. Infinite visits and (3) show that every value in this interval is a subsequential limit of $X_a/a^s$. ∎

## 5 Explicit quantitative obstruction at three primes

Now take $P=\{2,3,5\}$, $\lambda=\log_2 3$, $\mu=\log_2 5$, and $I=I_P$. Theorem 1 reads

$$
\frac{X_a}{a^2}=
\frac1{4\lambda\mu}I(\{a\log_3 2\},\{a\log_5 2\})+o(1).
\tag{13}
$$

**Corollary 4 (uniform progression oscillation).** For every $m\ge1$ and residue $r$,

$$
\limsup_{a\equiv r\ (m)}\frac{X_a}{a^2}
-\liminf_{a\equiv r\ (m)}\frac{X_a}{a^2}
\ \ge\ \frac{I(0,0)}{30\lambda\mu}
\ \ge\ \frac1{30\lambda\mu}>0.
\tag{14}
$$

The ratio of this progression's limsup to its liminf is at least $5/3$.

**Proof.** In Theorem 3 choose $z$ with its 3-coordinate zero. If its 5-coordinate is an interior point $y$, the one-sided integral values are $I(0,y)$ and $I(0,y)/3$. Monotonicity in the second coordinate gives $I(0,y)\ge I(0,0)/5$, so their difference is at least $2I(0,0)/15$. If both coordinates cross zero, the two values are either $I(0,0)$ and $I(0,0)/15$, or $I(0,0)/3$ and $I(0,0)/5$. In the latter case their difference is exactly $2I(0,0)/15$; in the former it is larger. Divide by $4\lambda\mu$ to get (14). The possible ratios in these cases are 3, 15 and $5/3$. Finally the integrand at phase $(0,0)$ equals 1 for $0\le u<1$, because $\log_3 2,\log_5 2<1$, so $I(0,0)\ge1$. ∎

A real-valued **fixed-period quasipolynomial** means a sequence $Q(a)$ that agrees, on each residue class modulo some fixed $m$, with a real polynomial in $a$, for all sufficiently large $a$.

**Corollary 5 (no quasipolynomial subtraction).** There is no fixed-period quasipolynomial $Q$ such that $X_a-Q(a)=o(a^2)$ for the repeated $\{2,3,5\}$ tails. More precisely, on each progression where the defining polynomial has degree at most two,

$$
\limsup_{a\equiv r\ (m)}\frac{|X_a-Q(a)|}{a^2}
\ge\frac{I(0,0)}{60\lambda\mu}.
\tag{15}
$$

If that polynomial has degree above two, the limsup is infinite. The corresponding qualitative assertion $X_a-Q(a)\ne o(a^{|P|-1})$ holds for every finite $P$ with at least two elements.

**Proof.** A polynomial of degree at most two divided by $a^2$ converges to its quadratic coefficient. Any constant lies at distance at least half the gap between the two extreme subsequential limits in (14) from one of those limits. A polynomial of greater degree is incompatible with the boundedness of $X_a/a^2$, already supplied by Theorem 1. Apply this on each residue class. The general assertion follows in the same way from Theorems 1 and 3. ∎

In particular, no such subtraction leaves a bounded tail, an $O(a)$ tail, or an $O(a^{2-\varepsilon})$ tail for any $\varepsilon>0$. This includes the proposed simple strategy of removing a quadratic main term and then applying a bounded-state argument.

**Corollary 6 (no finite collection of polynomial corrections).** For any finite prime set $P$ with $s=|P|-1\ge1$, any finite nonempty collection of real polynomials $Q_1,\ldots,Q_N$, and any fixed arithmetic progression,

$$
\limsup_{a\to\infty\text{ in the progression}}
\min_{1\le j\le N}\frac{|X_a-Q_j(a)|}{a^s}>0.
\tag{16}
$$

Thus allowing an arbitrary choice of polynomial at each index, including a choice controlled by any finite state process, does not yield an $o(a^s)$ remainder.

**Proof.** Suppose instead that the nonnegative minimum tended to zero. Since $X_a/a^s$ is bounded, any polynomial of degree above $s$ can be omitted for all sufficiently large $a$. The remaining polynomials divided by $a^s$ converge to a finite set of leading coefficients, where a smaller degree contributes 0. The supposed approximation would force every subsequential limit of $X_a/a^s$ to lie in that finite set. This contradicts the interval of limits in Theorem 3. If all polynomials have degree above $s$, the displayed limsup is infinite directly. ∎

## 6 Exact checks and what they establish

The historical companion Python program, omitted from this prose-only edition, uses only the standard library and exact integers or rational intervals. It has two independent finite constructions:

1. A heap enumeration of smooth integers with a literal running-LCM update, retaining each term.
2. Enumeration by the odd part $3^j5^k$, with exact integer comparisons against the internal prime-power jumps in each dyadic shell.

These agree on all 16 shells below $2^{16}$, covering 283 smooth terms. In the shell $[16,32)$, all seven terms yield $m_4=65$; replacing them by the three distinct denominators would give 19. The program explicitly rejects that substitution and the missing factor $1/2$.

For numerical checks of (13), the program encloses $X_a/a^2$ and $F_P(x_a)$ using rational intervals. The actual-tail enclosure truncates 24 shells and uses the elementary bound

$$
X_b\le60\left(\frac{(b+1)^2}{7}+\frac{2(b+1)}{49}+\frac9{343}\right).
\tag{17}
$$

To prove (17), use $M_{b+r}\le(b+r+1)^2$ and $P_b/P_{b+r}\le15\,8^{-r}$ in (11), then sum the three geometric moments. This deliberately loose bound suffices for certified enclosures.

The profile integral is computed by ordering the actual integer prime powers between $2^a$ and $2^{a+24}$. On each intervening interval the kernel is constant; its logarithmic length is enclosed using the convergent identity

$$
\log(n/d)=2\sum_{k\ge0}\frac{((n-d)/(n+d))^{2k+1}}{2k+1},\qquad 1\le n/d\le2.
$$

Fixed-point interval arithmetic rounds every multiplication and division outwards. For 100 terms, the positive remainder is at most $9/(4\cdot201\cdot3^{201})$, below $10^{-80}$. The integral remainder uses $I(x,y)\le22/7$, obtained by bounding the first unit interval by 1 and later intervals by $15\,8^{-r}$.

Illustrative rounded midpoints from the certified enclosures are:

| $a$ | $X_a/a^2$ | $F_P(x_a)$ | Difference |
|---:|---:|---:|---:|
| 100 | 0.097193428 | 0.091293007 | 0.005900421 |
| 187 | 0.027455558 | 0.026609417 | 0.000846141 |
| 252 | 0.026597665 | 0.025960756 | 0.000636909 |
| 317 | 0.078441215 | 0.076955242 | 0.001485973 |
| 512 | 0.078789747 | 0.077857803 | 0.000931945 |
| 800 | 0.044666823 | 0.044345346 | 0.000321476 |

Every displayed actual or profile enclosure has width less than $10^{-14}$. The constant on the right of the first inequality in (14) is approximately 0.0127214469683. The exact rational enclosures, initial shell data and all sample results were retained in the historical `CHECKS.json`, which is omitted from this prose-only edition.

The scan checks normalization, multiplicities, exact floor comparisons, and agreement with the predicted scale. It does **not** prove the $o(1)$ assertion, the infinite progression oscillation, cofinal residue certificates, or irrationality. Those infinite analytic statements come from Sections 2–5, and irrationality is not asserted at all.

## 7 The remaining obstruction

If $R_P$ were rational, the strict-prefix clearing factor $P_a/p$ would make an appropriate fixed integer multiple of every sufficiently late $X_a$ integral. Cook's residue formulation for $\{2,3,5\}$ retains exactly this possibility [2, Sections 9–10]. Theorems 1 and 3 constrain the leading behavior of that possible integer sequence, but integrality alone does not force it to be quasipolynomial. The elementary example $\lfloor a^2F_P(x_a)\rfloor$ already has the same leading profile and is integral; it is not claimed to satisfy the required tail recurrence.

Thus the present attack establishes a genuine obstruction to a specified polynomial-subtraction method, while leaving the decisive arithmetic obstruction intact: exclude every eventual integral reduced-tail sequence for the **actual** numerators. At $P=\{2,3,5\}$ the phase error in (3) is $o(a^2)$, not $o(1)$, and gives no control of fractional parts. Replacing that missing control with a finite experiment would be invalid.

## References

[1] Paul Erdős, letter dated 1 January 1973, *The Fibonacci Quarterly* 12 (1974), p. 335. [Original one-page letter](https://www.fq.math.ca/Scanned/12-4/letter.pdf). This is the source of the repeated-summand question and its distinction from the duplicate-removed variant.

[2] Will Cook, *Running least common multiples: distinct values and multiplicities*, July 2026, revised 5 October 2026, 73-page author manuscript. [Full manuscript](https://wcook04.github.io/plectis/papers/erdos269-running-lcm-reasoning-surface.pdf). Relevant comparison: Sections 5.5, 7–12, especially Lemma 8.3, Theorem 9.1, and Sections 12.1–12.2. The manuscript's two-prime transcendence statement is credited there to Fan's Hecke–Mahler reduction; that external value theorem and its acceptance status are not audited or used here. The author describes substantial AI drafting and incomplete independent checking. This note treats the manuscript as prior research to distinguish scope, not as an accepted proof of the unresolved repeated case.

The arguments above are self-contained apart from elementary compact-torus and Fourier-approximation facts explained in the proofs. Source hashes, byte counts and inspection scope are recorded separately. No third-party source text or dataset is included in this packet.
