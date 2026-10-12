# A sharp obstruction when at most two unrestricted-partition factors are signed

## Status and exact scope

This is an authored computer-assisted partial result for David Newman's unrestricted-partition sign problem. It does **not** settle the unrestricted problem, and no novelty or priority claim is made.

Work in the formal power-series ring \(\mathbb Z[[q]]\). For a finite set \(S\subset\mathbb N\), write
\[
P_S(q)=\prod_{m\in S}\left(1+\sum_{j\ge1}\epsilon_{m,j}q^{mj}\right)
       \prod_{m\notin S}(1-q^m)^{-1},\qquad \epsilon_{m,j}\in\{-1,1\}.
\]
Every sign in each active factor is independent; there is no periodicity, digit-multiplicativity, uniform-sign, or geometric-series restriction on the active factors. Constants remain +1. The inactive factors remain the original positive geometric series.

**Theorem (finite and sharp).** If \(|S|\le2\), it is impossible to have
\[
|[q^n]P_S(q)|\le1\quad(0\le n\le86).
\]
There is a choice with \(S=\{1,2\}\) satisfying these inequalities through degree 85. Thus 86 is the sharp universal first unavoidable obstruction degree for the class with at most two active factors.

In particular, an affirmative solution of the original unrestricted problem must contain negative coefficients in at least three distinct factors, already among coefficients of degree at most 86. This conclusion imposes no restriction on how many factors may be signed in the original question.

The proof consists of a finite reduction, an exact exhaustive recurrence, and an independently checked finite computation. No search budget, random choices, beam truncation, symmetry identifications, or heuristic pruning enters the certificate.

## 1. Reduction to exactly 39 pairs

If neither factor 1 nor factor 2 is active, the coefficient of \(q^2\) is 2: its contributions are the term \(q^2\) in factor 1 and the term \(q^2\) in factor 2. Thus every candidate set must contain 1 or 2.

The exhaustive recurrence below gives these two singleton facts:

- With only factor 1 active, the first empty feasible frontier is degree 31.
- With only factor 2 active, the first empty feasible frontier is degree 11.

Suppose 1 is active. If another active index \(b\) exceeds 31, that factor cannot affect any coefficient through degree 31, so the singleton obstruction applies. The only potentially relevant pairs are therefore \(\{1,b\}\) with \(2\le b\le31\), **including** \(b=31\).

If 1 is inactive, 2 must be active. The second active index must be \(3\le b\le11\), **including** \(b=11\), by the analogous singleton argument. Thus there are 30+9=39 pairs to check, together with the two singleton checks that justify the reduction. Empty and singleton active sets are covered as well. This argument also applies to a finite prefix: factors whose first negative term lies beyond the prefix can be treated as inactive there.

## 2. Exact feasible-frontier recurrence

Fix one of these sets \(S=\{a\}\) or \(S=\{a,b\}\), with \(a<b\) in the latter case. Put
\[
T_S(q)=\prod_{m\notin S}(1-q^m)^{-1}=\sum_{n\ge0}t_nq^n.
\]
The tail coefficients are determined, through any desired degree, by either of two integer computations:

1. Start \(t_0=1,t_n=0\) for \(n>0\). For each allowed part \(m\notin S\), in increasing order, replace \(t_n\) by \(t_n+t_{n-m}\) for increasing \(n\ge m\). After part \(m\), the array counts partitions using the allowed parts at most \(m\); this proves the update by the number of copies of the new part.
2. Set \(s_k=\sum_{d\mid k,\ d\notin S}d\). Then
\[
t_0=1,\qquad nt_n=\sum_{k=1}^n s_k t_{n-k}. \tag{1}
\]
Indeed, formal logarithmic differentiation gives \(qT'_S/T_S=\sum_{k\ge1}s_kq^k\), proving (1). This recurrence is used by a separately written verifier, rather than the producer's partition update.

A state at level \(n\) is the pair of sign strings
\[
(\alpha_1,\ldots,\alpha_{\lfloor n/a\rfloor});
(\beta_1,\ldots,\beta_{\lfloor n/b\rfloor}),
\]
with the second string absent for a singleton. Constants \(\alpha_0=\beta_0=1\) are implicit. A state is feasible when its truncated active factors, multiplied by \(T_S\), have every coefficient through degree \(n\) in \(\{-1,0,1\}\).

Begin with the unique empty state at level zero. From a level-\(n-1\) state calculate
\[
A_n=\sum_{\substack{0\le i\le\lfloor(n-1)/a\rfloor\\
                   0\le j\le\lfloor(n-1)/b\rfloor\\ai+bj\le n}}
       \alpha_i\beta_j t_{n-ai-bj}. \tag{2}
\]
For a singleton, use just \(j=0\). Define the possible new first-factor contribution to be
\[
E_n=\begin{cases}\{-1,1\},&a\mid n,\\\{0\},&a\nmid n,\end{cases}
\]
and define \(D_n\) analogously for \(b\), or \(D_n=\{0\}\) in a singleton case. Append the relevant fresh signs for **every** pair \((e,d)\in E_n\times D_n\) satisfying
\[
-1\le A_n+e+d\le1. \tag{3}
\]
If neither factor has a fresh coefficient, keep the state precisely when \(|A_n|\le1\).

**Completeness proof.** A term newly introduced at level \(n\) has degree exactly \(n\). Consequently it contributes to degree \(n\) only by multiplying constants in all other factors, and cannot affect smaller degrees. Two fresh nonconstant terms have degree \(2n>n\). Therefore (3) is the exact new coefficient condition, not merely a necessary test. Inductively, every appended state is feasible. Conversely, restricting any feasible level-\(n\) state gives a feasible level-\(n-1\) state, and its fresh signs appear among precisely the tested choices. Thus no feasible assignment can be omitted by the recurrence.

There is no quotienting of states: distinct sign strings remain distinct, even if some current product coefficients agree. The calculation terminates at the first empty frontier for each case.

## 3. Exhaustive arithmetic result

Applying (1)–(3), or equivalently the partition-tail update followed by (2)–(3), gives the following first empty degrees. Grouped rows cover every indicated integer index.

| Active factors | First empty degree |
|---|---:|
| \(\{1\}\) | 31 |
| \(\{2\}\) | 11 |
| \(\{1,2\}\) | 86 |
| \(\{1,3\}\) | 59 |
| \(\{1,4\}\) | 84 |
| \(\{1,5\}\) | 31 |
| \(\{1,6\}\) | 59 |
| \(\{1,b\},\ 7\le b\le31\) | 31 |
| \(\{2,3\}\) | 40 |
| \(\{2,4\}\) | 81 |
| \(\{2,5\}\) | 23 |
| \(\{2,b\},\ 6\le b\le11\) | 11 |

The full check has 41 cases and 23,683 nonempty states, counting each case's root separately. In the largest case \(S=\{1,2\}\), there are 11,620 nonempty states and the largest frontier contains 462 states.

For reproducibility, the exact frontier cardinalities for \(S=\{1,2\}\), beginning at degree zero and ending at degree 86, are

```
1,
2,4,6,18,26,53,67,79,49,52,38,76,90,178,107,204,239,462,
246,435,241,214,211,374,193,194,85,81,88,85,49,94,114,92,
112,191,198,325,331,280,286,265,251,352,184,146,74,105,120,
151,134,241,252,405,220,319,194,200,101,181,154,55,49,47,
23,16,16,31,32,34,38,82,82,89,57,103,98,103,61,70,64,88,
52,5,6,0.
```

These counts are diagnostic checks on the recurrence, not a substitute for checking its complete frontiers. The retained machine certificate lists every sign-string state at every level for every case. The separately written verifier recomputes the tail using (1), calculates (2) directly, constructs all children satisfying (3), and compares that set with each certified frontier. It checks the root, sign alphabets, string lengths, uniqueness, complete pair coverage, all transition sets, the first-empty property, counts, and the explicit degree-85 witness. It does not accept a certificate merely because counts or checksums match. Deliberately deleting a feasible state, inserting an infeasible state, or omitting a case is rejected. Normal Python, optimization level 1, and optimization level 2 all return the same result; the verifier uses explicit checks rather than removable assertions.

## 4. All six final states and the sharpness witness

Here is a compact exact description of the six degree-85 states for \(S=\{1,2\}\). Every nonconstant sign not specified as positive is negative, within the truncations \(1\le i\le85\), \(1\le j\le42\).

Let
\[
U=\{1,2,3\}\cup\{16,17,\ldots,35\}\cup\{69,75,76,77\},
\quad
V=\{4,5,\ldots,8\}\cup\{16,17,\ldots,24\}\cup\{34,38,39,41\}.
\]
For each row, the positive \(\alpha_i\) indices are \(U\) together with the listed extra indices; the positive \(\beta_j\) indices are as specified. These are multiplicity indices in factor 2, so \(\beta_j\) is the coefficient of \(q^{2j}\).

| State | Extra positive \(\alpha_i\) indices | Positive \(\beta_j\) indices | \(A_{86}\) |
|---|---|---|---:|
| 1 | 82,84 | \(V\cup\{42\}\) | −8 |
| 2 | 82,83,84 | \(V\cup\{42\}\) | −6 |
| 3 | 82,83,84,85 | \(V\cup\{42\}\) | −6 |
| 4 | 81,82,83 | \(V\cup\{42\}\) | −4 |
| 5 | 81,82,83,85 | \(V\cup\{42\}\) | −4 |
| 6 | 81,82,83,84,85 | \(V\) | −8 |

At degree 86 the only new signs are \(\alpha_{86}\) and \(\beta_{43}\), whose sum lies in \(\{-2,0,2\}\). Even the largest residual, −4, therefore gives a coefficient at most −2. None of the six states extends.

For a direct sharpness check, use state 1. Exact multiplication by \(T_{\{1,2\}}\) gives its coefficients from degree 0 through degree 85 as follows:

```
1,1,0,1,-1,-1,1,-1,0,0,0,0,-1,-1,-1,0,1,1,-1,0,-1,0,0,-1,
1,0,0,0,0,-1,0,0,1,1,0,1,-1,-1,1,-1,0,1,0,1,-1,0,0,0,
1,1,0,1,-1,-1,1,0,1,0,0,0,-1,-1,0,-1,0,0,0,-1,-1,1,0,-1,
-1,-1,0,0,1,1,0,0,0,-1,-1,-1,0,1.
```

Choose any signs for the as-yet-unspecified later terms in the two factors; later terms cannot change this verified prefix. This proves the degree-85 existence claim. The case table and reduction prove the obstruction by degree 86 for every set of at most two active factors, completing the theorem.

## 5. Source history and limitations

- [David Newman, Open Problem Garden, “Dividing up the unrestricted partitions”](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions) states the full independently signed unrestricted product. Its historical search discussion mentions exponents around 110. The present degree-85 witness is for a substantially narrower class and is not a record claim for the original problem.
- [David Newman, MathOverflow, “A Product Related to Unrestricted Partitions”](https://mathoverflow.net/questions/146359/a-product-related-to-unrestricted-partitions), posted 30 October 2013, contains the earlier odd-binomial suggestion and Aaron Meyerowitz's degree-28 obstruction discussion. That route is not represented here as a new construction or a full-problem obstruction.
- [David Newman, MathOverflow, “A simplified version of an old problem about the generating function for unrestricted partitions”](https://mathoverflow.net/questions/272822/a-simplified-version-of-an-old-problem-about-the-generating-function-for-unrestr), posted 22 June 2017, has Aaron Meyerowitz's revised computational answer giving the first-factor-only degree-31 obstruction. Newman's 25 June 2017 comment explicitly asks about changing the first two factors. We independently reproduce the single-factor result as a control. These are public question-and-answer statements, not a claim of journal-refereed status.
- [George E. Andrews and David Newman, “Binary Representations and Theta Function,” Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf), published 13 April 2018, distinguishes the unrestricted question from its affirmative identities for specific sets of dilates. Neither its odd-dilate identity nor its triangular-number identity licenses discarding inactive factors from the present product.

No theorem about the original problem with three or more active factors is proved here. In particular, finite impossibility in this restricted class cannot be transferred to the unrestricted sign array. The computation is finite and exhaustive only for the explicitly described 41 cases; the source search is not an exhaustive novelty search.
