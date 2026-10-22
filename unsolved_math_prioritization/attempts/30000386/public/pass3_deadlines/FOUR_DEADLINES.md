# Four arbitrary known detonation times

## Result and exact scope

**Theorem (computer-assisted restricted result).** For any four known positive integers `T1<T2<T3<T4`, a speed-one Angel in two dimensions has one online strategy surviving forever against every adaptive Devil whose announced time coordinates belong to that set. The announcement budget remains one pair per round, after the Angel's move. Repeated pairs, repeated positions, and announcements for past allowed times are permitted.

The proof uses a finite integer/rational certificate after an analytic reduction of all possible gaps to 180 dyadic-scale triples. The first deadline is arbitrary and is not bounded or enumerated. Bomb positions and future announcements are never assumed known.

This is not a theorem for arbitrary finite sets, not a resolution of the unrestricted Time-Bomb conjecture, and not a novelty claim. The accepted PASS2 three-time theorem and all earlier files remain unchanged.

## 1. Endpoint geometry and exact profiles

Use the accepted four-child geometry. In one dimension let `A_0={-1,0,1}`, and recursively

`A_k=(-2^k+A_(k-1)) union (2^k+A_(k-1))`.

The translates are disjoint. Let `E_k=A_k x A_k`. At dyadic scale `a=2^k`,

`|A_k|=3a`, `|E_k|=9a^2`, and `R_k=2a-1`.

A parent center reaches a selected child center in `2^k` king moves; the remaining time is exactly the child's `R_(k-1)`. At the last scale all nine points in `E_0` are reachable in one move. For a gap `r`, choose maximal `k` with `R_k<=r`, then wait `w=r-R_k`, where `0<=w<=2a-1`.

For nonnegative translated update kernels `K_i`, let

`C_b=max_i max_x sum_{y in x+E_j} K_i(y)/(9b^2)`, where `b=2^j`.

A phase's terminal average, starting with hazard mass `m` in its initial endpoint set, is at most

`m/(9a^2) + w C_a + sum_{b<a} 2b C_b`.

Each branch selects a least-average child using only observed hazards. During its traversal, each adaptive update is charged at the corresponding `C_b`. All sums over `b` are over powers of two.

To reserve the announcement immediately after the preceding lethal move as well as the maximum wait, define

`D=9a^2 [1-2a C_a-sum_{b<a}2b C_b]`.

When `D>0`, the earlier hazard

`f(x)=indicator_of_earlier_bombs(x)+sum_{y in E_k} h(x+y)/D`

strictly below 1 ensures immediate safety and sufficient downstream reserve **for every legal boundary announcement**. The initial downstream mass is strictly below `D`; its boundary and subsequent phase charges sum to at most `1-D/(9a^2)`. Thus the downstream terminal hazard is strictly below 1.

This transformation creates the update family consisting of a unit point kernel and the kernels `1_(E_k)*K_i/D`. Every intermediate lethal time is therefore checked at a phase boundary. No block traversal contains an allowed lethal time in its interior.

Define the infinite first-phase cost

`F(K)=sum_{b=1,2,4,...}2b C_b`.

If `F(K)<1`, the terminal strategy succeeds for every first deadline, starting from zero hazard. Its traversal sum is a prefix of this series and its wait charge `(2a-1)C_a` is smaller than the next term `2a C_a`. This argument does not require a bound on the first deadline.

## 2. Bounds inherited from the three-time proof

Exact concentration never exceeds the total-mass/peak bound used in the accepted PASS2 proof. Its denominators are therefore at least those of that proof, and the resulting kernels are pointwise no larger than their corresponding coarser kernels.

After one backward smoothing at scale `s`, the conservative unit-bomb denominator and mass are

`D_s=5s^2+2s`, `B_s=9s^2/D_s<9/5`.

The family consisting of the unit point kernel and this smoothed kernel has infinite profile cost at most `4/7`. Indeed, that cost is

`(4/9)[1+(B_s-1)/s]`,

and the dyadic inequality `(B_s-1)/s<=2/7` was proved in PASS2.

After two backward smoothings, the accepted three-time proof gives:

- infinite profile cost at most `4/5`;
- every update kernel has total mass at most `27/8`.

For the second assertion: in the earlier-scale-smaller regime the farthest mass is below `(9/5)^2<27/8`; in the other regime it is `9a^2/[lambda(c)a^2+2a]<=27/8`, since `lambda(c)>=8/3`. The point and middle kernels satisfy the same bound.

We also use the following consequence. If a downstream family has infinite cost at most `eta<1`, then its backward denominator satisfies

`D>=9a^2(1-eta)`.

The reserved charge `2a C_a+sum_(b<a)2b C_b` is a prefix of the infinite cost. Thus a one-stage downstream family gives `D>=3(9a^2)/7`; a two-stage downstream family gives `D>=9a^2/5`.

## 3. A mass/peak summation bound

A kernel of total mass at most `beta` and peak at most `alpha` has average on an endpoint set of size `9b^2` at most

`min(beta/(9b^2),alpha)`.

Its infinite cost is bounded by

`G(beta,alpha)=sum_b 2b min(beta/(9b^2),alpha) <= (8/3)sqrt(beta alpha)`.

If `x=sqrt(beta/(9alpha))<=1`, the entire series is at most `4beta/9`, which satisfies the stated bound. Otherwise choose the first dyadic `b0>=x`, so `x<=b0<2x`. The portion below `b0` is below `2alpha b0<=4alpha x`; the tail is `4beta/(9b0)<=4beta/(9x)`. Their sum gives the bound. Zero kernels are trivial.

For a baseline update family plus extra kernels all bounded by one mass/peak pair, the combined cost is at most the baseline cost plus `G`. This uses `max(base,extra)<=base+extra`, not an extra announcement allowance.

## 4. Analytic reduction of all three gaps

Let `a,b,c` be the dyadic scales for the three gaps `T2-T1`, `T3-T2`, and `T4-T3`, respectively. In every phase we conservatively use the maximum wait `2a-1`, `2b-1`, or `2c-1`. Smaller actual waits only decrease the required charges; all boundary announcements remain reserved.

### Case A: `a>=32`

The downstream two-stage family has cost at most `4/5` and kernel masses at most `27/8`. Hence the new denominator is at least `9a^2/5`. Every non-point kernel after this smoothing has

`beta<=135/8`, `alpha<=15/(8a^2)`.

The peak bound uses `max_x sum_(y in E)K(x+y)<=total_mass(K)`. The first-phase family is therefore bounded by the point kernel, whose cost is `4/9`, plus this envelope. Section 3 gives

`F<=4/9+15/a<=263/288<1`.

### Case B: `b>=max(16,4a)`

At the middle smoothing, the downstream one-stage family has cost at most `4/7`, so its denominator is at least `3(9b^2)/7`. Every resulting non-point kernel has peak at most

`(9/5)/(3(9b^2)/7)=7/(15b^2)`.

Because `b>=4a`, this is less than `1/(9a^2)`. During the entire scale-`a` phase, the point kernel's average is at least `1/(9a^2)`, so these non-point kernels never determine the maximum charge. The earliest denominator is exactly `D_a=5a^2+2a`.

The baseline point kernel and its single smoothing have cost at most `4/7`. The remaining kernels have

`beta<=243/40`, `alpha<=21/(25b^2)`.

Their product, with `b^-2` factored out, is `5103/1000<25/4`. Therefore

`F<4/7+20/(3b)<=4/7+5/12=83/84<1`.

### Case C: neither A nor B holds, and `c>=64`

The omitted cases imply `a<=16` and `b<=32`. Thus `c>=2b` and `c>=4a`.

At the middle smoothing, the last kernel is too spread out to dominate the point kernel at any scale up to `b`; equivalently `D_c>=5c^2>9b^2`. Its denominator is exactly `D_b`. The additional far kernel then has peak at most

`B_b/D_c<=9/(25c^2)<1/(9a^2)`.

It likewise cannot alter the earliest phase's charges. The earliest denominator is exactly that of the baseline three-time construction on the first three deadlines, using the same exact-profile recurrence. That baseline's cost is at most `4/5`.

The normalization factor `9a^2/D` is at most `7/3`, by the one-stage downstream bound. The sole additional farthest kernel has

`beta<=189/25`, `alpha<=21/(25c^2)`.

Section 3 yields

`F<=4/5+168/(25c)<=181/200<1`.

### Remaining cases

If Case A fails, `a` belongs to `{1,2,4,8,16}`. If Case B also fails, then `b<max(16,4a)<=64`, so `b` belongs to `{1,2,4,8,16,32}`. If Case C fails as well, `c` belongs to the same six-element set.

Consequently the analytic cases leave only the following **180** triples:

`a in {1,2,4,8,16}; b,c in {1,2,4,8,16,32}`.

The certificate checks this entire rectangle, including harmless overlaps with the analytic cases. Thus no possible dyadic-scale triple is omitted.

## 5. Exact finite certificate

The remaining 180 cases are checked by `verify_four_deadlines.py`, using Python integers and exact rational `Fraction` arithmetic only. There is no floating-point numerical step.

Every update kernel is separable: it has the form

`K(x,y)=p(x)p(y)/d`,

where `p` is the convolution of at most three one-dimensional endpoint indicators and `d` is a positive rational product of denominators. A new point kernel has `p=delta_0,d=1`; smoothing convolves `p` with the selected endpoint indicator and multiplies `d` by the new denominator.

For each endpoint scale, the checker computes the exact largest one-dimensional translated sum of `p` over `A_k`. Its square divided by `d` is exactly the largest two-dimensional translated mass, because translations in the two coordinates can be optimized independently. Taking the maximum over the finite update family gives the exact `C_b` used in Section 1.

For `k>=1`, the endpoint set has the explicit form

`A_k={x: |x|<2^(k+1), x is not divisible by 4}`.

Once the endpoint window is at least three sites longer than the finite support of `p`, its maximal translated sum equals

`sum(p)-min_r sum_(x congruent r mod4)p(x)`.

The upper bound holds because every translated endpoint set omits one whole residue class. Equality is attainable: the length condition permits a full-support window with every one of the four residue alignments. This exact identity makes the remaining infinite-scale tail geometric. It does not truncate the cost series.

The checker verifies the endpoint recursion, compares the large-window identity with direct integer convolution on representative kernels, computes all three positive denominators in every case, and checks the exact infinite cost.

**Certificate result:** all 180 cases have positive denominators and infinite cost strictly below 1. The maximum is

`34777/50976 < 1`,

at gap scales `(a,b,c)=(2,2,2)`.

`FOUR_DEADLINES_CERTIFICATE.json` contains all 180 exact costs and denominator triples. `FOUR_DEADLINES_CHECK.json` records the result and artifact hashes. The checker regenerates the certificate from the stated recurrence; it does not merely trust or reread a supplied result table.

The finite computation is part of this computer-assisted proof, unlike an experiment suggesting a general theorem. The analytic reduction proves that the finite list covers every remaining parameter regime, and the infinite-tail identity proves that each listed cost covers every first deadline.

## 6. Online strategy and stopping condition

Before play, the four known deadlines determine the three gap scales and the static kernel normalizations. During the first phase, the hazard field starts at zero and receives one translated kernel per effective announcement. Choose least-average endpoint children using only the currently observed field. The analytic or finite certificate proves that its first terminal hazard is below 1.

At `T1`, this certifies immediate survival and a winning continuation for every post-move announcement. Execute the certified second phase. Its terminal hazard at `T2` is below 1, again certifying the next boundary announcement. Repeat at `T3`, then survive `T4`. There are no other permitted lethal times between these boundaries. After `T4`, all allowed detonation times are past, so remaining moves are harmless.

Thus the proof constructs a single online strategy against every adaptive legal announcement sequence in this four-time restriction. It does not select a path after seeing future bombs.

## 7. Limitation

The proof does not supply a uniform invariant for an unbounded number of deadlines. In particular, a finite number of additional backward smoothings must not be extrapolated into an all-finite-set result. The known positive-linear local composition obstruction remains relevant. This report closes the four-time task only; no unrestricted solution is claimed.
