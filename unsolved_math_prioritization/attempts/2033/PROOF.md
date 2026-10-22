# Partial avoidance theorems for harmonic denominators

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial theorems; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests and rigorous arithmetic bounds are described, but executable programs, detailed receipts, full computational certificates, raw datasets, and copied source documents are omitted. This edition is not an executable reproduction package. Edition preparation did not rerun mathematical tests or newly inspect scholarly sources.

## Status and scope

The assertion that `gcd(a_n,L_n)=1` for infinitely many `n` is **not proved or refuted here**. Here `L_n=lcm(1,...,n)` and `a_n=L_n H_n`, with `H_n=sum_{j=1}^n 1/j`. We prove two unconditional statements on the coprime side of the question:

1. Every fixed finite set of prime obstructions can be avoided on arbitrarily large intervals of relative length `1/5`; the corresponding finite-prime survivor set even has positive lower natural density. A quantitative construction uses elementary simultaneous approximation and makes no independence assumption about reciprocal prime logarithms.
2. If one deletes only the universally bad leading digits `p-1`, simultaneously for every odd prime, the survivors have lower logarithmic density strictly greater than `283/2000`, hence greater than `0.14`. Thus those universal digits alone do not account for a possible failure of coprime infinitude.

The second statement is supported by historically verified exact finite rational bounds, whose mathematical derivation and endpoints are retained here; full computational certificate contents are omitted. The remaining obstruction consists of the other harmonic zero digits. No claim of novelty is made. The leading-digit criterion is prior work; the proofs and certificate below are authored for this attempt.

## 1. The exact local criterion

Write `H_n=c_n/d_n` in lowest terms and put `q_n=L_n/d_n`. Because `a_n=c_n q_n` and `L_n=d_n q_n`,

`gcd(a_n,L_n)=q_n`.

Fix a prime `p<=n`. Let `p^e<=n<p^(e+1)` and `m=floor(n/p^e)`, so `1<=m<p`. Write `L_n=p^e M`, with `p` not dividing `M`. In the sum defining `a_n`, terms indexed by integers not divisible by `p^e` vanish modulo `p`. The remaining indices are `r p^e`, `1<=r<=m`. Therefore

`a_n = M (1+1/2+...+1/m) (mod p)`.

All displayed inverses exist modulo `p`, and `M` is a unit. Define

`E_p={m: 1<=m<p and sum_{r=1}^m r^(-1)=0 (mod p)}`.

Then

`p|q_n  <=>  m in E_p`.                                             (1)

In particular `1` is never in `E_p`. For `p=2` it is the only possible leading digit, so `q_n` is always odd. For an odd prime, pairing `r` with `p-r` shows `p-1 in E_p`. The exact prime obstruction is

`Q_p = union_{m in E_p, e>=1} ([m p^e,(m+1)p^e) intersect N)`.        (2)

These are Shiu's Theorem 2 conditions, with the multiplier `M` retained in the modular calculation. The exponent restriction `e>=1`, equivalently `n>=p` for the local criterion, is essential. The already-known noncoprime infinitude is not a result of this attempt.

## 2. Avoiding every prime in a fixed finite set

### Theorem A

Let `S` be a nonempty finite set of odd primes, let `r=|S|`, and let `P=max S`. Set

`eta=log(6/5)`, and choose an integer `Q>=log(P)/eta`.

For every real `X>=2P`, there is an integer `j`, `1<=j<=Q^r`, such that every integer in

`I=[(5/4) X^j,(3/2) X^j]`

satisfies `gcd(q_n,product_{p in S} p)=1`. The interval has real length `X^j/4`, and the ratio of its endpoints is `6/5`.

#### Proof

For each `p in S` put `alpha_p=log(X)/log(p)`. Partition the unit `r`-cube into `Q^r` half-open cubes of side `1/Q`. Among the `Q^r+1` points

`({k alpha_p})_{p in S}`, for `0<=k<=Q^r`,

two lie in the same cube. Subtraction gives `1<=j<=Q^r` and integers `b_p` such that

`|j alpha_p-b_p|<1/Q` for every `p in S`.

Consequently

`|j log(X)-b_p log(p)|<log(p)/Q<=eta`.

The integers `b_p` are positive, since `X>=2P` and the last error is smaller than `log(6/5)`. If `n in I`, division by `p^(b_p)` gives

`25/24 < n/p^(b_p) < 9/5 < 2`.

Since `p>=3`, `p^(b_p)` is exactly the largest power of `p` not exceeding `n`, and the leading base-`p` digit of `n` is `1`. Equation (1) excludes every `p in S` from `q_n`. This proves the theorem. No rational independence was used. □

### Corollary A1

For each fixed `y`, there are arbitrarily long intervals on which `q_n` is either `1` or has every prime factor greater than `y`.

#### Proof

Take `S` to be the odd primes at most `y`, apply Theorem A as `X` tends to infinity, and use oddness of `q_n`. The case of empty `S` is immediate. □

### Corollary A2

For every fixed finite prime set `S`, the set

`G_S={n: gcd(q_n,product_{p in S}p)=1}`

has positive lower natural density.

#### Proof

Discard `2`, which never divides `q_n`. Consider the continuous homomorphism

`Phi(t)=(t/log(p) mod 1)_{p in S}`

into the finite torus, and its compact closure `G`. Let `V` be the open neighborhood of zero given by coordinate distances less than `eta/log(p)`, with the same `eta=log(6/5)`. Since the orbit is dense in `G`, finitely many translates `Phi(t_i)+V` cover `G`. Put `B=max_i |t_i|`.

For every real `t` there is an `i` for which `Phi(t-t_i) in V`. Thus some `u in [t-B,t+B]` satisfies

`|u-b_p log(p)|<eta` for integers `b_p` and all `p in S`.

For sufficiently large `t` these `b_p` are positive, and the same calculation as in Theorem A makes every integer of `[(5/4)e^u,(3/2)e^u]` a member of `G_S`.

Given sufficiently large `x`, take `t=log(2x/3)-B`. The resulting interval lies below `x` and has length at least `x e^(-2B)/6`. Its integer count is at least that length minus `1`. Hence

`liminf_{x->infinity} |G_S intersect [1,x]|/x >= e^(-2B)/6 >0`.       (3)

This proof uses recurrence on the actual orbit closure, rather than asserting that the closure is the whole torus. It therefore remains valid in the presence of any higher-dimensional linear relations. □

## 3. The universal p minus 1 obstruction

For each odd prime define the smaller obstruction

`C_p=union_{e>=1} ([(p-1)p^e,p^(e+1)) intersect N)`.

By (1), `C_p` is contained in `Q_p`. Put

`U=N \ union_{p odd prime} C_p`,

and define lower logarithmic density by

`lower_delta(A)=liminf_{x->infinity} (1/log x) sum_{n<=x,n in A} 1/n`.

### Theorem B

`lower_delta(U)>283/2000>7/50`.

This theorem does not assert that the numbers in `U` are coprime cases. For example, `33 in U` but `q_33=11`; its leading base-`11` digit is `3`, and `H_3=11/6`.

### 3.1 One-prime and two-prime logarithmic densities

Set

`delta_p=log(p/(p-1))/log(p)`.

For a fixed `p`, the logarithmic density of `C_p` is `delta_p`: in logarithmic time `t=log x`, membership is, after an initial finite interval, periodic with period `log(p)` and occupied interval length `log(p/(p-1))`.

For distinct primes `p,l`, the logarithmic density of `C_p intersect C_l` is

`delta_p delta_l`.                                                   (4)

Here is why the only independence required in (4) is known. A nontrivial integer relation between `1/log(p)` and `1/log(l)` would make `log(p)/log(l)` rational. Exponentiating would make a positive power of `p` equal a positive power of `l`, contrary to unique factorization. Thus for every nonzero integer pair `(h,k)`,

`(1/T) integral_0^T exp(2 pi i t (h/log(p)+k/log(l))) dt ->0`.

Approximation by trigonometric polynomials, and then approximation of rectangle indicators from above and below, proves uniform distribution of this two-coordinate continuous flow. The rectangle's area is exactly the product in (4). This argument uses no assertion about three or more reciprocal prime logarithms.

For completeness, continuous logarithmic averages agree with the discrete harmonic averages used here. Every endpoint of a real obstruction interval is an integer. On `[n,n+1)`, each indicator is therefore constant and equal to its value at `n`. The discrepancy is bounded by

`sum_{n>=1} (1/n-log(1+1/n)) < infinity`.

The same statement applies to finite intersections and differences. Therefore

`delta(C_p \ C_3)=(1-delta_3) delta_p` for `p>=5`.                   (5)

### 3.2 A uniform bound for infinitely many primes

For integer `A<B`,

`sum_{A<=n<B} 1/n <= log(B/A)+1/A`.

At most `log(x)/log(p)` intervals defining `C_p` can meet `[1,x]`. The sum of their lower-endpoint errors is at most

`sum_{e>=1} 1/((p-1)p^e)=1/(p-1)^2`.

Thus, uniformly in `x` and `p`,

`sum_{n<=x,n in C_p} 1/n <= delta_p log(x)+1/(p-1)^2`.              (6)

We next prove convergence and an explicit upper bound for

`D=sum_{p odd prime} delta_p`.

Let `m=2^j`, `j>=1`. Every prime in `(m,2m]` divides the integer `binom(2m,m)`, which is smaller than `4^m`. The number of those primes is therefore at most `2m/j`. For each of them,

`delta_p < 1/(m j log(2))`.

It follows that

`sum_{2^j<p<=2^(j+1)} delta_p < 2/(j^2 log(2))`.

In particular the series defining `D` converges. Because `log(2)>2/3`,

`sum_{p>2^20} delta_p < 3 sum_{j>=20} 1/j^2`

`                         <= 3(1/400+integral_20^infinity t^(-2)dt)`

`                         = 63/400`.                               (7)

The exact rational computation in Section 3.4 certifies

`sum_{3<=p<=2^20} delta_p <47/50`.

Consequently

`D<47/50+63/400=439/400`.                                           (8)

Equations (6) and (7) also justify passage from finite prime unions to the infinite union. For `y` tending to infinity, the upper logarithmic density of `union_{p>y} C_p` is at most `sum_{p>y} delta_p`, which tends to zero. Indeed sum (6) over those primes; the total endpoint error is bounded by the convergent series `sum_{p>y}1/(p-1)^2`, independently of `x`.

### 3.3 Finishing the density lower bound

Split off `C_3` and use (5) for the other primes. A finite union bound, followed by the preceding uniform tail argument, gives

`upper_delta(union_p C_p) <= delta_3+(1-delta_3) sum_{p>=5} delta_p`.

Therefore

`lower_delta(U) >= (1-delta_3)(1-D+delta_3)`.                        (9)

The exact inequalities `(3/2)^3>3` and `(3/2)^5<3^2` give

`1/3<delta_3<2/5`.

Combining these inequalities with (8) in (9), both factors being positive, yields

`lower_delta(U) > (3/5)(1-439/400+1/3)=283/2000>7/50`.

This proves Theorem B. □

### 3.4 The finite certificate

The original candidate's standalone standard-library program, omitted from this edition, generated every prime at most `2^20` by an ordinary exact sieve. Its logarithm enclosures used only integer arithmetic and

`log(a/b)=2 sum_{j>=0} z^(2j+1)/(2j+1)`, where `z=(a-b)/(a+b)`.

For `1<=a/b<=2`, `0<=z<=1/3`. The first `K=16` terms are bounded by directed integer rounding at scale `R=10^24`. The omitted tail is at most

`2 z^(2K+1)/((2K+1)(1-z^2))`.

For `log(p)`, write `p=2^k r`, `1<=r<2`, and bound `k log(2)+log(r)`. Bounds for `log(p/(p-1))` and `log(p)` give rational interval bounds for their quotient. Summing over all `82,024` odd primes at most `2^20` gives

`934535274480325630395660 / 10^24`

` <= sum_{3<=p<=2^20} delta_p`

` <= 934535274480325643460226 / 10^24 <47/50`.

The historical finite computation used no floating-point inputs, logarithm-library calls, downloaded programs, or probabilistic primality tests. The analytic infinite-prime step is (7), not an extrapolation from this finite sum.

## 4. What remains and why the attempt stops short

Define the non-universal obstruction

`R_p=union_{m in E_p \ {p-1}, e>=1} ([m p^e,(m+1)p^e) intersect N)`.

Equation (2) makes the exact unresolved set

`G={n:q_n=1}=U \ union_p R_p`.                                    (10)

Theorems A and B do not give a uniform bound for the rightmost union inside the set `U`. In particular:

- The finite-prime theorem fixes the prime set before sending `n` to infinity. Its bound `j<=Q^r` deteriorates with the number and size of the primes. It does not apply to all potentially obstructing primes at the produced value of `n`.
- The positive lower logarithmic density in Theorem B concerns only `p-1` digits. The example `n=33` prevents identifying `U` with `G`.
- Formula (4) is only pairwise independence. It does not justify a product formula for a growing family of harmonic obstructions.
- Wu–Yan's conditional upper-density-one theorem concerns `q_n>1`, and gives no lower bound on the set in (10).

A sufficient, genuinely additional statement would be

`upper_delta(U intersect union_p R_p)<283/2000`.

Together with Theorem B this would prove positive lower logarithmic density, and hence infinitude, of `G`. No such bound is proved here; it is substantially stronger than the expected sparse-coprime heuristic would suggest and is not advanced as a plausible conjecture. The sharp remaining target is simply that the difference in (10) is unbounded; stating it is a reduction, not a solution.

## Public sources

1. Peter Shiu, *The denominators of harmonic numbers (Revised)*, arXiv:1607.02863v2, 30 July 2024. Theorem 2 gives the exact local obstruction; Theorem 3 gives its one-prime harmonic density; Sections 5 and 7 explain the conditional alignment and remaining coprime conjecture. https://arxiv.org/abs/1607.02863v2
2. Bing-Ling Wu and Xiao-Hui Yan, *On the denominators of harmonic numbers. IV*, Comptes Rendus Mathématique 360 (2022), 53–57, DOI 10.5802/crmath.282. Their Conjecture 1 and Theorem 2 give a conditional upper-density-one result for noncoprime cases. https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.282/

The original candidate and audit recorded complete inspection of their retained primary sources. Their results are not treated as proving either Theorem A or Theorem B by citation; the proofs above supply those statements directly. Historical inspection details and limits appear in SOURCES.json; this edition performed no new scholarly-source inspection.
