# Three arbitrary known detonation times: candidate proof

## Scope and status

This is an authored PASS2 construction under the original two-dimensional king-move, Angel-first, one-announcement-per-round contract. It proves a restricted theorem for **three known allowed time coordinates**, with an adaptive Devil and arbitrary repeated announcements. It does not prove survival for four or arbitrarily many known deadlines, and it does not settle the unrestricted conjecture. Independent audit is requested. No novelty claim or authenticated companion-journal proof claim is made.

**Theorem.** Given any three known positive integers `U<V<W`, the Angel has a single online strategy surviving forever when every announced bomb has time coordinate in `{U,V,W}`.

The proof changes the terminal geometry and retains both total mass and peak of every update kernel. It reserves the announcement immediately after each lethal move. Every block traversal is used only in an interval containing no allowed intermediate lethal time.

## 1. Four-child terminal geometry

Let `E_0={-1,0,1}^2`. Recursively, for `k>=1`, set

`E_k = union_{epsilon in {-1,1}^2} [2^k epsilon + E_(k-1)]`.

The four translates are disjoint. Put

`a=2^k`, `R_k=2a-1`, `N_k=|E_k|=9a^2`.

Every endpoint in `E_k` lies at king distance at most `R_k` from the origin. From a center with exactly `R_k` moves remaining, choosing one of the four translates and moving to its center takes exactly `2^k=a` king moves. The remaining time is `R_(k-1)=a-1`. The child endpoint set has `9(a/2)^2` elements. This is repeated until `E_0`, when exactly one move remains and all nine endpoints are reachable.

For an arbitrary remaining time `r>=1`, choose the largest `k` with `R_k<=r` and wait `w=r-R_k` moves. Maximality gives

`0<=w<=2a-1`.

At every branch, choose a child with average currently observed hazard at most the parent average. Disjointness and equal child cardinality justify this choice. Traversal is legal, and future adaptive updates are charged only after they occur.

If each round adds a nonnegative hazard field of total mass at most `beta`, the final average, starting from zero, is at most

`beta [w/(9a^2) + (4/9)(1-1/a)]`

`<= beta [4/9 - (2a+1)/(9a^2)]`.

The traversal identity follows from summing `2^j/(9*4^(j-1))` for `j=1,...,k`. Thus **every terminal hazard process of per-round total mass at most `9/4` is avoidable**, with a strict final average below 1. The initial wait and all traversals use exactly `r-1` moves, so their announcements end at the round before the terminal move.

For unit point-bomb updates, initial mass `m` on the initial translate of `E_k` is tolerable whenever

`m+w < 5a^2+4a`.

In particular, reserving both the boundary announcement and the maximum permitted wait leaves the positive denominator

`D_a=5a^2+2a`.

## 2. Mass/peak version and backward certification

An update kernel is a nonnegative finitely supported function whose translations may be selected adaptively. Suppose kernel type `i` has total mass at most `beta_i` and maximum point value at most `alpha_i`. On any set of `9b^2` points its average contribution is at most

`C_b = max_i min(beta_i/(9b^2), alpha_i)`.

For a phase with scale `a=2^k`, initial hazard mass `m` on its endpoint set, and wait `w`, the final average is at most

`m/(9a^2) + w C_a + sum_{b=1,2,...,a/2} 2b C_b`.

All sums indexed by powers of two here and below are dyadic sums. The formula includes only the phase's own announcements, after its starting boundary announcement.

For backward certification from a preceding lethal time, additionally reserve that boundary announcement. A sufficient positive denominator is

`D = 9a^2 [1 - 2a C_a - sum_{b<a} 2b C_b]`,

because `w+1<=2a`.

Let `h(x)` denote the downstream hazard field. Define the new earlier hazard as

`f(x) = indicator_of_earlier_bombs(x) + sum_{y in E_k} h(x+y)/D`.

If `f(x)<1` at the earlier deadline, that deadline is safe and the pre-boundary downstream mass is strictly below `D`. The boundary update adds at most `9a^2 C_a`; the subsequent wait and traversals contribute the remaining displayed charges. Therefore the downstream terminal hazard is strictly below 1. This proves the required statement for **every** legal boundary announcement, not merely the announcement already observed.

Smoothing a downstream kernel of bounds `(beta,alpha)` produces bounds

`beta' = 9a^2 beta/D`,

`alpha' = min(9a^2 alpha,beta)/D`.

Both estimates are immediate from the finite convolution. A new bomb at the earlier deadline instead creates a unit point kernel `(1,1)`.

For a family of profiles, define its infinite terminal cost

`F = sum_{b=1,2,4,...} 2b C_b`.

If `F<1`, the four-child construction wins at **every** initial deadline, starting from zero. Indeed, its traversal sum is the prefix with `b<a`; its wait contribution is at most `(2a-1)C_a`, strictly less than the next single summand `2a C_a` when `C_a>0`. The rest of the infinite sum is nonnegative. In this application `C_a>0` because the unit point update is always among the available types.

## 3. Last gap

Let `c` be the dyadic scale for the gap `W-V`. Use the conservative denominator

`D_c=5c^2+2c`, and write `B_c=9c^2/D_c=9c/(5c+2)`.

At time `V`, the hazard

`h_V(x)=indicator_of_V_bombs(x) + |B_W intersect (x+E_c)|/D_c`

certifies survival at both `V` and `W`. Here `E_c` denotes the endpoint set at dyadic scale `c`, and `B_W` is the observed set of positions already bombed at time `W`. Strict hazard below 1 certifies the boundary update and the subsequent phase by Section 2.

During the preceding phase, updates to this hazard have profiles

- a time-`V` bomb: `(1,1)`;
- a time-`W` bomb: `(B_c,1/D_c)`.

For a dyadic endpoint-set scale `b`, the corresponding average update bound is exactly

`C_b=1/(9b^2)` if `b<c`,

`C_b=B_c/(9b^2)` if `b>=c`.

To check the crossover: if `b<c`, then `b<=c/2`, hence `9b^2<D_c`; if `b>=c`, the future kernel's total-mass bound applies and `B_c>1`.

## 4. Earlier gap and the two scale regimes

Let `a` be the dyadic scale for `V-U`. Applying the preceding profile formula to the backward denominator yields:

### Regime A: `a<c`

All traversal scales and the boundary scale are below `c`, so

`D=5a^2+2a=D_a`.

Write `B_a=9a^2/D_a`. The time-`U`, time-`V`, and time-`W` updates to the first-phase hazard have respective profiles

`(1,1)`,

`(B_a,1/D_a)`,

`(B_a B_c,B_a/D_c)`.

At dyadic scale `b`, the maximizing profile is respectively:

- the unit point kernel, for `b<a`;
- the middle kernel, for `a<=b<c`;
- the far kernel, for `b>=c`.

For example, between the two scales the comparison is `D_c>=9b^2`, since `b<=c/2`. Below `a`, the far kernel's peak is smaller than the middle kernel's peak because `9a^2<D_c`. Thus the stated maxima account for all three profiles.

The infinite first-phase cost is

`F = (4/9)(1-1/a) + (4 B_a/9)(1/a-1/c) + 4 B_a B_c/(9c)`

`= (4/9)[1 + g(a) + B_a g(c)]`,

where `g(x)=(B_x-1)/x=(4x-2)/(x(5x+2))`.

For dyadic `x>=1`, `g(x)<=2/7`: equality holds at `x=1`, while for `x>=2` the stronger `g(x)<=1/4` follows from `(5x-4)(x-2)>=0`. Here `c>=2`, so `g(c)<=1/4`, and `B_a<9/5`. Consequently

`F < (4/9)[1+2/7+(9/5)(1/4)] = 27/35 < 1`.

### Regime B: `a>=c`

Summing the two ranges of update charges gives

`D = a^2 [5-4(B_c-1)/c] + 2 B_c a`.

Equivalently,

`D/B_c = lambda(c) a^2+2a`,

where

`lambda(c) = (25-6/c+8/c^2)/9`.

For dyadic `c>=1`,

`8/3 <= lambda(c) <= 3`.

The lower bound follows from `(c-2)(c-4)>=0` for `c` in `{1,2,4,8,...}`; the upper bound follows from `(c+4)(c-1)>=0`. In particular, `D>0`.

The far kernel dominates the middle kernel in both mass and peak. Put

`h = B_c/D = 1/[lambda(c)a^2+2a]`.

It is sufficient to retain the two profiles

`(1,1)` and `(9a^2 h,h)`.

For `b<a`, the point kernel dominates: `b<=a/2` gives `1/(9b^2)>=4/(9a^2)>h`, since `lambda(c)>=8/3`. For `b>=a`, the far kernel dominates, since `9a^2 h>1` follows from `lambda(c)+2/a<=5<9`.

The infinite first-phase cost is therefore

`F=(4/9)(1-1/a)+4a h`

`=4/9-4/(9a)+4/[lambda(c)a+2]`.

If `a=1`, then also `c=1`, `lambda(c)=3`, and `F=4/5`.

If `a>=2`, use `lambda(c)>=8/3` to obtain

`F <= 4/9-4/(9a)+12/(8a+6) < 4/5`.

For an explicit algebra check, the difference between `4/5` and the middle expression has positive denominator `45a(8a+6)` and numerator

`4[32(a-2)^2+57(a-2)+16]`.

Thus `F<=4/5<1` throughout Regime B.

## 5. Complete online chronology

The times `U,V,W` determine the two dyadic scales and the fixed denominators before play. During rounds before `U`, form the first-phase hazard from the currently observed bomb sets, using the two backward smoothing steps. It starts at zero and receives only translations of the three bounded update types above. By Sections 2 and 4, the four-child strategy obtains hazard strictly below 1 at time `U`.

That condition ensures immediate survival at `U` and, for every announcement made after move `U`, certifies the robust phase ending at `V`. Run that phase using the currently observed downstream hazard. There are no lethal times strictly between `U` and `V`. At `V`, the resulting downstream hazard is strictly below 1, ensuring immediate survival and, for every round-`V` announcement, certifying the final phase ending at `W`. There are no lethal times strictly between `V` and `W`. The final phase therefore survives `W`.

After `W`, every allowed lethal time has passed. The Angel may stay forever. All choices use only the finite observed history; no future bomb positions or schedule are assumed known. Repeated announcements can only lower the added hazard mass, and announcements at a past allowed time are harmless.

## 6. General-induction boundary

This proof gives the first three-deadline step for this construction. It does not prove that arbitrary further backward smoothing preserves positive denominators or a terminal cost below 1. The profile family grows with each extra deadline; the two-scale algebra above exploits the specific three-kernel structure. No induction is claimed without a bound for those larger families.

A failure of a denominator or profile estimate would be a failure of this sufficient certificate, not a Devil-winning instance. In particular, the earlier PASS1 estimate `36/25` for `{13,17,21}` is superseded as an obstruction to that old estimate only; it never asserted a loss.
