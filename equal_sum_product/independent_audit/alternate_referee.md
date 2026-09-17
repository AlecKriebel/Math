# Independent adversarial mathematical review

Review checkpoint: 2026-09-17T03:44:36Z. Reviewer: an independent Codex subagent.

Scope: independently attempt to falsify the stated theorem before reading its supplied proof, then audit every mathematical argument and numerical example in `notes/equal_sum_product_note.tex`. No other review was read. No external communication was undertaken. The derivation below was developed before opening the supplied note; it was not copied from that note. This is a mathematical review, not a certification of historical novelty or of every recorded execution claim.

Checkpoint: mathematical review 100% complete. Verdict: the theorem, stronger proposition, identities, and boundary examples are correct. No mathematical correction is required.

## Exact claim and independent derivation

The claim concerns an `m` by `n` matrix of **globally pairwise distinct positive integers**, with `m >= 3`, `n >= 2`, each row summing to `N` and each column having product `N`. Positivity and global distinctness are substantive assumptions.

Before reading the proof, I obtained the following slightly stronger exponent-dependent inequality. Suppose common row sum and common column product are `S` and `P`, respectively. Set `r = m-1 >= 2`. For one column `b_1,...,b_m`, arithmetic–geometric mean applied to the `r` nonnegative quantities `b_k^{-r}` with `k != i` gives

\[
\frac{b_i}{P}=\prod_{k\ne i}\frac1{b_k}
\le \frac1r\sum_{k\ne i}\frac1{b_k^r}.
\]

Sum over `i`. Every reciprocal power on the right appears exactly `r` times, so

\[
\frac{\sum_i b_i}{P}\le\sum_i\frac1{b_i^{m-1}}.
\]

Summing over columns, using the row sums, and letting `M` be the greatest matrix entry gives

\[
\frac{mS}{P}
\le\sum_{i,j}a_{ij}^{-(m-1)}
\le\sum_{k=1}^{M}\frac1{k^{m-1}}
\le\sum_{k=1}^{M}\frac1{k^2}
\le 2-\frac1M<2.
\]

The second inequality uses global distinctness, the third uses `m-1 >= 2`, and the final non-strict inequality follows by bounding `1/k^2 <= 1/(k(k-1))` for `k >= 2` and telescoping. Thus `S=P` would force `m<2`, contrary to `m>=3`. This works also for `n=1` and proves the note's stronger proposition as well.

This independent derivation converges to the same broad reciprocal-bound mechanism as the supplied proof, but uses all rows and exponent `m-1`, rather than selecting three rows or selecting two cyclic neighbors. It should not be described as an unrelated proof family.

An earlier elementary edge check also ruled out `n=2`: every row contains an entry at least `N/2`; among three rows, two such entries occupy one column, forcing `N >= N^2/4`, hence `N<=4`. But `2m` globally distinct positive entries have total sum at least `m(2m+1)`, whereas the row condition gives total `mN`; consequently `N>=2m+1>=7`, a contradiction. This limited check is independent of reciprocal estimates and cannot by itself settle unrestricted `n`.

## Line-by-line audit of the supplied mathematical arguments

1. **Selecting three rows:** every omitted factor is an integer at least one. Therefore `N >= x_j y_j z_j` is valid, including `m=3` where the omitted product is empty and equals one. The selected rows alone contribute normalized sum exactly three.
2. **Dividing by the column product:** because all numerators and denominators are positive, `N >= xyz` implies `(x+y+z)/N <= (x+y+z)/(xyz)`. Expanding the latter gives the three claimed reciprocal products, with the correct inequality direction.
3. **Sum-of-squares identity:** expanding each squared difference yields exactly two copies of each reciprocal square and minus two copies of each reciprocal pair, so the factor one-half gives precisely the displayed identity. No equality assumption is used.
4. **Distinct-integer bound:** the selected `3n` entries form a subset of `{1,...,M}`, with no multiplicity. Adding missing positive summands is allowed. The finite telescoping identity and strict terminal bound `<2` hold also for `M=1`, although that value is incompatible with distinct selected entries here. Thus the chain rigorously yields `3<2`.
5. **Stronger cyclic proposition:** when `m>=3`, the two positions `i+1` and `i+2` modulo `m` differ from each other and from `i`. Dropping other denominator factors can only enlarge the reciprocal. The pairwise square bound is correct. In the sum over `i`, each position occurs in exactly two neighbor slots, so the total coefficient is one. This proves `mS/P<2` for any `n>=1`; `P>0` justifies rearranging it as `S<2P/m`.
6. **Two-row exception:** with `m=2`, dividing an entry by its column product leaves the reciprocal of the other entry, rather than a product of two reciprocals. The stated normalized identity is valid. The convergent reciprocal-square argument therefore does not apply.
7. **Scaling:** scaling by a common factor `c` multiplies each row sum by `c` and each column product by `c^m`. For preservation of the positive-integer domain, `c` must make every scaled entry a positive integer; the example uses `c=2` and satisfies this condition.
8. **One-row boundary:** for `n>=2`, every column contains one entry and therefore must equal `N`. The row sum becomes `nN>N`, since `N>0`. The note's statement that only two rows can realize equality is explicitly within this `n>=2` scope. The excluded `m=n=1` case is possible and is not contradicted.

## Independently recomputed numerical examples

The calculations below used a fresh Python standard-library script, not a package checker or a package-generated certificate report.

| Example | Row sums | Column products | Distinct entries |
|---|---|---|---|
| Listed 2 by 10 source control | `840, 840` | Ten copies of `840` | `20` of `20` |
| Listed ordinary 3 by 2 control | `24, 24, 24` | `840, 840` | `6` of `6` |
| 3 by 4 matrix consisting of twos | `8, 8, 8` | Four copies of `8` | `1` of `12` |
| Twice the 2 by 10 control | `1680, 1680` | Ten copies of `3360` | `20` of `20` |

Exact rational summation of the twenty reciprocals in the 2 by 10 control gives exactly `2`. These checks confirm every numerical matrix, reciprocal, and scaling assertion in the note.

The combinatorial counts in the validation table are also arithmetically consistent: `40^3=64000`, `2^12-1=4095`, `10*12*3=360` arrays, and `10*3*(1+...+12)=2340` columns. Confirming that all recorded tests were actually executed is a separate reproducibility task; the theorem does not depend on those finite tests.

## Falsification outcome and limitations

No counterexample is compatible with the exact hypotheses. The repeated-entry example shows that dropping global distinctness can destroy the conclusion. The separate-sum/product example shows that confusing ordinary sum–product matrices with the equality case would misstate the result. The two-row control shows that the lower bound on the row count cannot be relaxed to two. None of these exposes a proof gap.

The strongest independently checked result is the finite inequality

\[
\frac{mS}{P}\le\sum_{i,j}a_{ij}^{-(m-1)}<2
\qquad(m\ge3),
\]

which implies the supplied theorem. No mathematical gap remains. Priority, source attribution, actual package test execution, and publication integration require their own checks and are not certified by this review.
