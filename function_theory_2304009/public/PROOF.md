# Verification of the negative answer to Function Theory 4.9

## 1. Exact target and attribution

For a monic polynomial `f` of positive degree `n`, write

`E(f) = {z in C : |f(z)| <= 1}`.

The catalogue asks whether, for every `c > 0`, there is a finite number `A(c)`, independent of `n` and `f`, bounding the number of connected components of `E(f)` whose Euclidean diameter exceeds `1 + c^2`.

This universal assertion is false. The negative answer is attributed to Christian Pommerenke (1961) in Hayman and Lingham's Update 4.9 and in Erdős's 1976 account. Huang's 2025 v2 gives a later proof and explicitly acknowledges the earlier resolution. We reconstruct the capacity-and-approximation argument, with explicit geometric choices and all normalization steps. This is verification of known mathematics.

## 2. Standard input and conventions

We use logarithmic capacity, denoted `cap`. Its energy convention is

`cap(K) = exp(-inf_mu integral integral log(1/|z-w|) dmu(z) dmu(w))`,

with the infimum over probability measures supported on the compact set `K`. In particular, capacity is monotone under inclusion. The kernel is `log(1/|z-w|)`, not `1/log|z-w|`.

We use the classical one-variable Hilbert lemniscate theorem in this precise form:

If `K` is compact and `C \ K` is connected, then for each `epsilon > 0` there is a polynomial `r` for which

`K subset {z : |r(z)| <= ||r||_K} subset {z : dist(z,K) <= epsilon}`.

This statement is recorded in Bloom–Levenberg–Lyubarskii, *A Hilbert Lemniscate Theorem in C^2*, introduction, equation (1.1), and in their arXiv version, equation (1). Only the one-variable statement is used.

Two standard capacity identities used below can also be read from Green functions at infinity:

1. If an exterior conformal map has expansion `F(w) = b w + O(1)`, `b > 0`, from `|w| > 1` onto the exterior of a Jordan compact set, that compact set has capacity `b`.
2. If `q(z) = alpha z^n + ...`, `alpha != 0`, then `cap(E(q)) = |alpha|^(-1/n)`.

For completeness, the second identity follows by setting `g(z) = (1/n) log|q(z)|` on `C \ E(q)`. The complement has no bounded component: on any such component `log|q|` would be positive and harmonic, with zero boundary values, contradicting the maximum principle. Thus `g` is the Green function with pole at infinity. Its expansion is `log|z| + (1/n)log|alpha| + o(1)`, whose constant term is `-log cap(E(q))`. The boundary limit is zero, directly from continuity of `q`. This proves the identity, including its sign.

## 3. Strengthened known assertion

**Theorem.** For each real `d` with `0 < d < 4` and positive integer `N`, there exists a monic polynomial `p` of positive degree for which `E(p)` has at least `N` distinct connected components, each with diameter strictly greater than `d`.

### Step A: an explicit capacity-one container

Set

`t = d/4`, `A = 1+t`, `B = 1-t`, `L = 1+3d/4`, `a = L/2`.

Then `0 < t < 1`, `B > 0`, and

`d < L < 2A < 4`.

Let `Omega` be the open ellipse `x^2/A^2 + y^2/B^2 < 1`. The map

`F(w) = w + t/w`

maps the exterior unit disk conformally onto the exterior of the closed ellipse. Indeed, its boundary values are `A cos(theta) + i B sin(theta)`. For two distinct exterior points, equality of their images would imply `w1*w2 = t`, impossible since `|w1*w2| > 1 > t`; the map has no exterior critical point and maps infinity to infinity. The boundary parametrization and the argument principle identify its image as the exterior ellipse. Its leading coefficient is one, so `cap(closure(Omega)) = 1`.

### Step B: arbitrarily many separated long segments

Put `m = 1-(a/A)^2`, which lies strictly between zero and one, and `h = B*m/4 > 0`. Define

`y_j = -h + 2h*j/(N+1)`, for `j = 1,...,N`,

and the horizontal closed segments

`K_j = [-a,a] + i*y_j`, `K = union_j K_j`.

Each segment has diameter `L > d`. The segments are pairwise disjoint, with adjacent vertical separation `2h/(N+1)`. The entire rectangle `[-a,a] x [-h,h]` lies strictly in `Omega`, since

`a^2/A^2 + h^2/B^2 = 1-m + m^2/16 < 1`.

The complement of `K` is connected. To see this directly, a point at a height different from every `y_j` can be joined by a horizontal segment to the half-plane `x > a`. A point in the complement at one of the exceptional heights is already strictly to the left or right of all the segments; in the left half-plane it can first move a little vertically to a nonexceptional height. All resulting paths join the same right half-plane.

We can choose explicitly

`epsilon = min(h/4, h/(3(N+1))) > 0`.

The closed epsilon-neighborhoods of the `K_j` are pairwise disjoint because `2 epsilon < 2h/(N+1)`. They all lie in `Omega`. Indeed, a point in any such neighborhood has `|x| <= a+epsilon` and `|y| <= h+epsilon`. Since `epsilon <= B*m/16`, `B <= A`, and `a/A < 1`,

`x^2/A^2 + y^2/B^2 <= (a/A + m/16)^2 + (5m/16)^2`

`<= 1-m + m/8 + 26m^2/256`

`<= 1 - 198m/256 < 1`.

### Step C: polynomial approximation preserves the large components

Apply Hilbert's theorem to `K` and this `epsilon`. The resulting polynomial `r` is nonconstant, since its sublevel set in that theorem is bounded and contains `K`. Also `M = ||r||_K` is positive: otherwise a nonzero polynomial would vanish on an entire nondegenerate segment. Define `q = r/M` and `S = E(q)`. Then

`K subset S subset K_epsilon subset Omega`.

Each connected set `K_j` is contained in a connected component `C_j` of `S`. No two such `C_j` coincide: the disjoint, positively separated neighborhoods of the segments disconnect `K_epsilon` into `N` pieces, and any connected subset of their union belongs to one piece. Consequently `S` has at least `N` distinct components with diameter at least `L > d`.

### Step D: monic normalization cannot shorten the components

Write `q(z) = alpha z^n + ...`, `alpha != 0`. Monotonicity and Step A give

`|alpha|^(-1/n) = cap(S) <= cap(closure(Omega)) = 1`.

Thus `|alpha| >= 1`. Choose any complex `w` satisfying `w^n = alpha` and define `p(z) = q(z/w)`. Its leading coefficient is `alpha/w^n = 1`, so it is monic. Furthermore

`E(p) = w S`.

Multiplication by `w` is a homeomorphism and multiplies all diameters by `|w| = |alpha|^(1/n) >= 1`. The images of the `N` components therefore remain distinct and retain diameter greater than `d`. This proves the theorem.

## 4. Deduction for the catalogue and limits

Take `d = 2` and `c = 1`. For any proposed finite `A(1)`, choose an integer `N > A(1)`. The theorem produces a monic polynomial with at least `N` components of diameter greater than `2 = 1+c^2`, a contradiction. More generally, the same argument works for every fixed `c` with `0 < c < sqrt(3)` by taking `d = 1+c^2`.

No degree bound in terms of `N,d`, explicit coefficient list, or asymptotic lower rate of component growth is supplied. The theorem permits the degree to grow as required by Hilbert approximation. It does not prove the update's statements for every sufficiently large prescribed degree, nor either of its proposed `o(n)` or `o(n^epsilon)` estimates. None of those strengthenings is needed to disprove the exact imported target.

## References

- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)* (2018), Problem and Update 4.9, printed pp. 74–75, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2).
- Ch. Pommerenke, *On metric properties of complex polynomials*, Michigan Math. J. 8 (1961), 97–115, [DOI](https://doi.org/10.1307/mmj/1028998561). Historical credit is corroborated by the primary accounts below; this paper's full text was not retrieved successfully in this verification.
- P. Erdős, *Extremal problems on polynomials*, Approximation Theory II (1976), 347–355, §3, printed p.349, [author archive](https://users.renyi.hu/~p_erdos/1976-12.pdf).
- L. Huang, *Many lemniscates with large diameter* (2025), Theorem 1.1, §2, and the v2 note on p.2, [arXiv:2509.11597v2](https://arxiv.org/abs/2509.11597v2).
- T. Bloom, N. Levenberg and Yu. Lyubarskii, *A Hilbert Lemniscate Theorem in C^2*, Ann. Inst. Fourier 58 (2008), 2191–2220, introduction equation (1.1), [publisher](https://aif.centre-mersenne.org/articles/10.5802/aif.2411/).
