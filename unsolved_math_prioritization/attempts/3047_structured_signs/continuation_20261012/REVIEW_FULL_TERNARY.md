# Independent acceptance: the full ternary-digit obstruction

## Verdict and exact scope

**ACCEPT** the complete mathematical theorem and exact finite computation described below. This is independent AI-assisted review, not external human peer review. The programs and raw frontier certificates used for the historical verification are not distributed in this appendix.

The accepted theorem is:

> No product retaining every original partition factor, with each factor ternary-digit multiplicative and all ternary digit signs independently selectable, has every total Taylor coefficient in \(\{-1,0,1\}\).

The full ternary family is excluded, including infinitely many noncyclotomic blocks. The original problem with arbitrary independent coefficients within each factor remains unresolved by this result. Binary and ternary digit families are incomparable. The analytic pruning assumes the global coefficient bound **one**, not an unspecified finite bound.

Degree 59 is the first empty frontier of the combined coefficient-and-Jensen search used here. It is **not** a claimed sharp coefficient-only obstruction degree, and this audit does not assert that every finite ternary prefix fails by degree 59. The earlier accepted zero-sparsity/common-factor/finite-budget packet is separate and was not overwritten.

## 1. Grouping and deferred choices are complete

At exponent \(n\), the labels \((m,j)\) satisfying \(m3^j=n\) number \(d_n=1+v_3(n)\). Choose:

\[
0\le c_n\le d_n,\qquad
0\le k_n^-\le d_n-c_n,\qquad
0\le k_n^+\le c_n.
\]

These encode, respectively, the number of positive linear signs and the numbers of negative quadratic signs among the negative-linear and positive-linear blocks. The four multiplicities are

\[
(d_n-c_n-k_n^-,\ c_n-k_n^+,\ k_n^-,\ k_n^+).
\]

Every legal quadruple is realized by the original labeled blocks, and groups at different exponents have disjoint labels. Thus no products are omitted by counting commuting blocks.

At degree \(N\), all linear signs through exponent \(N\) matter, but quadratic signs only through exponent \(\lfloor N/2\rfloor\) matter. Treating later quadratic signs as positive is an exact provisional convention. Replacing a positive quadratic sign at exponent \(l\) changes the block first by \(-2q^{2l}\). Hence, at even degree \(N=2l\), after selecting \(k^-+k^+\) defects and a fresh linear count \(c\), the new coefficient is exactly

\[
 A_N-2(k^-+k^+)+2c-d_N.
\]

No coefficient below degree \(N\) changes. At odd \(N\), the defect choices are absent. Every allowed count is enumerated, without merging distinct histories.

Any hypothetical infinite solution induces these finite states. Its coefficient condition and its global analytic necessary inequalities hold at every stage. Consequently its induced state must survive every transition. The proof needs this forward implication only; it never assumes that all retained finite states extend to infinite solutions.

## 2. Analytic pruning is valid for partial assignments

Let \(\varphi=(1+\sqrt5)/2\). A noncyclotomic block \(1\pm q^n-q^{2n}\) contributes exactly

\[
(\log\varphi+n\log r)_+
\]

to the Jensen zero sum, counting its \(n\) inner roots with multiplicity. Cyclotomic blocks contribute zero inside the unit disk. The full block product converges uniformly on compact subsets, and its sufficiently late tail is the exponential of a uniformly convergent sum of analytic logarithms. Therefore zeros persist; coincidences add multiplicities, and no tail cancellation occurs.

If all total coefficients have modulus at most one, Jensen and Parseval imply

\[
\sum_n b_n(\log\varphi+n\log r)_+
\le-\tfrac12\log(1-r^2). \tag{1}
\]

Only finitely many terms are positive for fixed \(r<1\). Boundary roots contribute zero, justified by limiting radii. These analytic details were independently proved in the first accepted packet and were checked again against the present self-contained proof.

Known defects are permanent selections in a partial assignment. Omitting unknown defects only decreases the left side of (1), because every omitted contribution is nonnegative. Thus rejection using the known defects is sound even though infinitely many further signs remain undecided. Only the total number of defects at each exponent enters the zero mass; the signs of their inner roots are irrelevant, so caching by this profile is valid.

## 3. Exact algebraic inequalities

For \(r=a/b=(b-1)/b\), retain precisely the known defect exponents with \(\varphi r^n>1\). If their multiplicity sum is \(K\) and exponent sum is \(S\), inequality (1) requires

\[
 A\varphi^{2K}\le B,\qquad
 A=(b^2-a^2)a^{2S},\quad B=b^{2S+2}. \tag{2}
\]

All comparisons are strict when rejecting. Equality, if encountered, is retained.

The independent implementation does not use the producer's Fibonacci/Lucas formula. It calculates integer pairs \((U_K,V_K)\) by

\[
(U_0,V_0)=(1,0),\qquad
(U_{K+1},V_{K+1})=(3U_K+5V_K,U_K+3V_K).
\]

Then

\[
\varphi^{2K}=(U_K+V_K\sqrt5)/2^K.
\]

Writing \(\Delta=2^KB-AU_K\), violation of (2) occurs exactly when \(\Delta<0\), or when \(\Delta\ge0\) and

\[
5A^2V_K^2>\Delta^2.
\]

Both sides use arbitrary-precision integers. For \(K=0\), a zero-free partial profile cannot violate (1), so it is accepted directly.

The independent positive-contribution cutoff also uses a different formula. Since \(\varphi^{-1}\) is the positive root of \(x^2+x-1\),

\[
\varphi(a/b)^n>1
\iff a^{2n}+(ab)^n>b^{2n}.
\]

This determines each last positive exponent exactly, with no floating-point screening, logarithmic approximation, or unchecked enclosure. The finite radius list matches the complete theorem and the independently checked exhaustive computation.

## 4. Independent coefficient arithmetic

The producer uses direct truncated polynomial updates with rational replacement kernels. The independent verifier instead uses formal logarithmic derivatives.

For a primitive block \(B_{a,b}(x)=1+a x+b x^2\), write

\[
\frac{xB'_{a,b}(x)}{B_{a,b}(x)}=\sum_{j\ge1}\ell_j(a,b)x^j.
\]

The exact recurrence is

\[
\ell_1=a,\qquad \ell_2=2b-1,\qquad
\ell_j=-a\ell_{j-1}-b\ell_{j-2}\quad(j\ge3).
\]

At stage \(N\), sum the dilated block log derivatives over proper divisors of \(N\), using the previously fixed group multiplicities and provisional positive quadratic signs for the pending group. Denote the resulting coefficient by \(h_N^{(0)}\). If \(p_0=1\) and the earlier product coefficients and log-derivative coefficients are known, the residual is

\[
 A_N=\frac{h_N^{(0)}+\sum_{j=1}^{N-1}h_jp_{N-j}}{N}.
\]

The division is checked for exact integrality. A newly negative quadratic sign changes \(\ell_2\) by \(-4\). At \(N=2l\), this changes \(h_N\) by \(-4l=-2N\), hence changes \(p_N\) by \(-2\). The fresh group's linear count changes \(h_N\) by \(N(2c-d_N)\). These identities independently recover the transition formula, without polynomial convolution or division kernels.

All verifier arithmetic uses Python integers. Its finite limit of 60 is an acceptance guard: reaching a surviving branch beyond the limit raises an error. It is not used to discard a possible state. Exhaustion occurs earlier, at degree 59.

## 5. Complete state verification and diagnostics

Every certificate record was compared to an independently generated state, not merely to a count or digest. The verifier loads exact state sets, rejects duplicate or partial records, generates every legal transition, removes each resulting state from the corresponding certificate set, and requires no unvisited certified state to remain. It starts from the unique implicit root.

Results:

- 831,371 total states, including the root
- Largest frontier: 101,822 states at degree 39
- Degree 58: 136 states
- Degree 59: empty
- Exact Jensen-rejected attempts: 461,708
- Coefficient-rejected choices: 1,724,844
- All 60 supplied frontiers match, including the empty truncation-margin level 60

The independent zero cache includes the empty defect profile, while the producer skips testing that profile. This accounts for the harmless one-profile difference: 32,209 independent profiles versus 32,208 nonempty producer profiles. Rejection decisions, frontier contents, and transition statistics agree exactly.

Normal Python, `-O`, and `-OO` verification outputs are byte-identical. No verification check relies on removable assertions.

Five adversarial certificate controls were rejected without modifying frozen inputs:

1. Deleting a feasible degree-39 record
2. Duplicating a record
3. Corrupting a group-code domain
4. Inserting a false terminal state
5. Truncating a file in the middle of a record

The historical storage-integrity check also confirmed exactly 60 frontier payloads, exact equality after decompression to the independently checked frontiers, and agreement with every recorded payload identity. No archive or raw payload is distributed here.

## 6. Producer overflow and replay

The frozen C++ producer checks every polynomial multiply-and-add in signed 128-bit arithmetic before converting back to signed 64-bit arithmetic. Products of two signed 64-bit values plus one signed 64-bit value fit signed 128-bit range, so the guard itself does not overflow. An out-of-range result aborts the run.

The small unchecked polynomial expressions are safe:

- The inverse series of \(1+x+x^2\) and \(1-x+x^2\) have coefficients in \(\{-1,0,1\}\), by \((1-x)/(1-x^3)\) and \((1+x)/(1+x^3)\), respectively.
- Every coefficient of a provisional block product in degree \(t\le60\) has modulus at most the ordinary partition number \(p(t)\). A selection of digit monomials determines an ordinary partition uniquely by ternary expansion; the sign only changes its weight. Thus \(p(t)\le2^{t-1}\) for \(t\ge1\), by injection into compositions. Adding the small transition counts is far below the 64-bit limit, so the absolute-value test is safe.
- The degree counts are at most four through degree 60; radius denominators are at most 2048; the loop indices and integer radius prefactors are within their fixed machine ranges. The large powers and golden-ratio comparisons use GMP integers.

The frozen source was independently compiled with

`-O2 -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all`

and rerun independently. It completed with empty sanitizer stderr. All 60 replayed frontier payloads and the complete stdout log equal the frozen originals byte for byte. Independently, the arbitrary-precision verifier already establishes the correctness of the mathematical output without relying on the producer's fixed-width arithmetic.

## 7. Public evidence limits and final conclusion

The complete transition rules, count domains, state encoding and exact arithmetic are given in [the theorem](FULL_TERNARY_OBSTRUCTION.md) and in this review. Independent reproduction requires implementing those specifications and enumerating all states. The historical verification was run in normal and both optimized execution modes, and its adversarial controls were run separately. No executable program or raw complete-frontier certificate is supplied in this appendix.

The mathematical inference is now complete: a globally coefficient-bounded ternary solution would induce a retained state in every frontier, but the exact complete degree-59 frontier is empty. Therefore no such ternary solution exists.

Acceptance is restricted to the stated theorem. It does not establish a general bound on the earliest bad coefficient for all arbitrary prefixes, a classification of all zero-free signed series, any claim of unbounded coefficients for every ternary product, or a resolution of the fully independent-sign partition problem. No novelty or source-priority claim is made. The acceptance is limited to this restricted-family mathematical result.
