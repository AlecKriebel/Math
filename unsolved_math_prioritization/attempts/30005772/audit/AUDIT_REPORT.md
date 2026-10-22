# Independent audit of negative k arrangement models

Problem 30005772 · OWR-14298158-017 · rank 494  
Audit date: 3 October 2026

## Verdict and scope

**PASS_PARTIAL.** The frozen packet's stated mathematical results are correct: its global ordered-prefix construction gives a finite unsigned set and an actual transported sign-reversing involution at every even size; its local model works at `k=-1`; its negative-cycle obstruction has the stated narrow scope; and its eventual unsigned transfer model works for each negative integer at every size `N >= 4(1-k)`.

**The original all-size interpretation problem remains unresolved by this packet.** Retain the status `partial_original_all_size_problem_unresolved` and five completed mathematical approaches. Neither the word “natural” nor an unqualified “solved” classification is warranted. There is no claim of historical priority, a comprehensive literature search, or human peer review.

No blocking mathematical defect or required formula correction was found. A naturalness qualification concerning the eventual model's finite terminal seeds is recorded below and must travel with this verdict. All six author files match their frozen hashes. Replaying the author's checker reproduces its recorded output byte for byte: **124,917 assertions**. The separate, independently implemented controls pass **245,193 assertions**, including seven rejected mutations. Finite checks support the universal arguments; their counts are not a proof certificate for infinite claims.

## Primary source and attribution

The target is Natasha Blitvić and Miklós Bóna, *A probabilistic interpretation points to new combinatorial results for k-arrangements*, printed pp. 302–304 in *Mini-Workshop: Permutation Patterns*, Oberwolfach Reports 21 (2024), report 6, pp. 273–308. [Publisher report](https://ems.press/content/serial-article-files/48646), [DOI](https://doi.org/10.4171/OWR/2024/6).

This audit inspected the supplied primary-source text and the already-rendered images of printed pages 303 and 304. Page 303 asks both for negative-integer evaluations generally and, separately, for even-size evaluations at all integer parameters. Page 304 already identifies the even-fixed-point count minus the odd-fixed-point count and explicitly supplies negative odd-size examples. It proposes an almost-bijection leaving unmatched arrangements. Therefore the signed enumeration is background, and negative odd values cannot be advertised as a counterexample resolving the intended problem.

The supplied Blitvić–Steingrímsson manuscript, *Permutations, moments, measures*, was checked at Theorems 1–2 and Remark 3. Its labeled-history/continued-fraction framework is prior mathematics; its Remark 3 already raises interesting negative-color combinatorial structures and eventual positivity. The OWR contribution cites the published remark number 3.8. [Prior paper](https://arxiv.org/abs/2001.00280).

The frozen packet properly credits the fixed-point polynomial, recurrence, exponential generating function, shifted-exponential moments, and classical Laguerre/history ingredients. No new independent broad literature or repository search was undertaken in this audit. The author's bounded-search statements remain bounded-search statements; they are not upgraded into absence, novelty, or priority certificates.

## Permutation and history correspondence

At a scan boundary, the two lists have equal size because the numbers of incoming and outgoing edges across the boundary agree. Earlier sources and earlier targets are ordered by their vertex labels. Each nonfixed vertex falls into exactly one of the four comparisons of its predecessor and successor with the current vertex; a fixed vertex necessarily has both equal to itself.

The inverse operations assign exactly one incoming and one outgoing edge at every vertex. Opening a source and a target at a valley does not assign either prematurely. A horizontal U step closes an earlier source and opens the current one; a horizontal L step closes an earlier target and opens the current one. A downstep closes one of each, with independent ranks in the two lists. The lists are empty at the end of a closed history. There is no hidden restriction on the two ranks: even selecting corresponding vertices is allowed and produces a legitimate 2-cycle.

Moving the first downstep rank to its stack-matched upstep is invertible. Both matched steps cross the same height edge, so the transferred rank is in the correct alphabet. Thus each direction across `{h-1,h}` has exactly `h` labels. Reversing a symmetric history preserves vertical label validity. Keeping horizontal U/L types unchanged also preserves validity because both types have the same height-dependent alphabet. Reversal need not implement permutation inversion; only its history-space bijectivity is used.

These points establish the symmetric integer Jacobi matrix

`J[h,h] = 2h+k`, `J[h,h+1] = J[h+1,h] = h+1`

and the formal finite-walk identity `A(N,k) = (J^N)[0,0]`. At `k=0` the fixed-point alphabet is empty. For positive parameters all labels have positive sign; for negative parameters the history sign is exactly fixed-point parity. Empty objects handle size zero correctly.

The independent controls recover scan ranks directly from boundary-crossing permutation edges, rather than copying the author's mutable-list encoder. They exhaust all closed symmetric histories through size six with zero, one, or two fixed-point colors, compare entire decoded classes with direct colored permutations, and check both injectivity and surjectivity.

## Ordered prefix cancellation and the even involution

For fixed length, endpoint, and parameter, the specified code is a genuine total order on a finite set. Height never exceeds length, and each step has finitely many labels. In the stack algorithm, every unmatched element has the same sign by induction: an opposite next sign pops one element, while a like sign appends. Consequently all survivors at a fixed endpoint have the same sign, including the possibility of an empty survivor set.

The partner map is fixed by the complete ordered-prefix list. It is not recomputed from an individual full history, so changing one prefix cannot change its paired status or the partner of another prefix. The first-half-first rule is essential. If the first prefix is paired it remains paired after applying its partner; otherwise the second-prefix rule remains the first applicable rule. Applying the full map twice is therefore the identity. In every nonfixed case precisely one factor changes sign. Changing both matched halves would instead preserve sign and is explicitly rejected by a negative control.

Every closed history of length `2n` splits uniquely into a prefix and the reversed suffix of length `n`, sharing an endpoint. Conversely every such ordered pair concatenates into a valid closed history. Surviving pairs have positive product sign, even when both survivors are negative. Every negative full object is paired with a positive one. Transport through the verified history bijection yields the claimed involution on the actual colored permutations.

Thus the residual cardinality is

`sum_h |R(n,h;k)|^2 = sum_h (J^n)[0,h]^2 = A(2n,k)`.

This is an explicitly specified finite-set model without querying `A` to decide prefix membership. It is also generic global cancellation whose answer depends on an arbitrarily fixed order. The involution can change many fixed points, and it supplies no bounded-local rule or intrinsic pattern description. It must be described as a weak algorithmic answer to the even-size subquestion, not as an independently established natural interpretation. Independent exhaustive pair-space checks include `n=4, k=-1`, beyond the author's tested half-length range, and verify all 40,320 full length-eight histories in that case.

## Matrix identities and the local model

All matrix products are locally finite. No bounded-operator, self-adjoint-extension, convergence, or interchange-of-infinite-sums assumption is needed. A length-`N` walk from index `i` stays within `0,...,i+N`. An entry of any power is therefore computed correctly in a sufficiently large finite truncation.

The Laguerre normalization `Q_h=(-1)^h L_h` has unit norm, and multiplication by `y+k-1` gives exactly this symmetric `J`. The coefficient formula and Rodrigues integral agree:

`c(N,h;k) = binom(N,h) integral_0^infinity (y+k-1)^(N-h) y^h exp(-y) dy`

for `h<=N`, and `c(N,h;k)=0` for `h>N`. The endpoint `h=N` is included. Boundary terms vanish in the repeated integrations by parts: at zero, the requisite lower derivatives of `y^h exp(-y)` vanish; at infinity, exponential decay dominates. The explicit finite-sum formula has integral summands for integer `k`.

The three nonzero bands of `J^2` in equation (10) are correct, including the lower boundary `h=0`. At `k=-1` they are all nonnegative; the missing distance-one edge between zero and one causes no disconnection problem, since the distance-two edge is present. The diagonal loop multiplicity at zero is two. The graph counts give the stated even values.

Direct multiplication gives `J(-1)^5 e0 = (8,120,320,480,360,120,0,...)`. It is a finite nonnegative terminal vector, so the same graph counts every odd size at least five. Sizes one and three remain negative. The independent controls verify local even sizes through 60 and local odd sizes through 65. The truncation mutation omitting vertex two incorrectly gives four instead of eight at size four, demonstrating why excursion height cannot be ignored.

For `k=-2s`, the triangle `(s-1,s,s+1,s-1)` has a negative product. For `k=-(2s+1)`, the four-cycle `(s-1,s,s+2,s+1,s-1)` does too, without using the zero edge. All vertices are nonnegative and every used edge is nonzero. Diagonal sign switching preserves a cycle product because each vertex sign appears twice. This proves the claimed obstruction only for diagonal sign switching of `J^2`. Taking absolute values entrywise is not a legitimate replacement: at `k=-2`, three steps in the absolute-weight graph give 325, whereas `A(6,-2)=261`.

## Eventual entrywise positivity

The triple Laguerre generating function is correct:

`sum ell(i,j,h) u^i v^j w^h = 1/(1-uv-uw-vw-2uvw)`.

Formal coefficientwise integration is legitimate because every coefficient integrates a finite polynomial against `exp(-y)`. The two-variable specialization proves orthonormality. The triple coefficients are exactly linearization coefficients by orthonormality and degree. Their five-letter word interpretation proves both integrality and nonnegativity. The coefficient of `uvw` is two, not one. Independent controls compare the word recurrence with exact triple polynomial integrals, using polynomials built from the three-term recurrence rather than the author's coefficient implementation.

For `r=1-k>=2`, the uniform estimate in Lemma 5 is valid. If `N-h` is even, the Rodrigues integrand is nonnegative and positive on a set of positive measure. Otherwise its negative part is bounded above by

`r^(N+1) h! (N-h)! / (N+1)! <= r^(N+1)/(N+1)`.

This drops the factor `exp(-y)<=1` in the correct direction. On the positive half, substituting `y=x+r` gives the lower bound `exp(-r) N!`, since `(x+r)^h >= x^h`. With `M=N+1>=4r`, the integral lower estimate for `log(M!)` yields

`log(M!/r^M) >= M(log(M/r)-1)+1 >= 4r(log 4-1)+1 > r`.

The middle expression is increasing for `M>=4r`; the final strict inequality follows from `log 4>5/4`. Thus the positive contribution strictly dominates, uniformly for all `0<=h<=N`. There is no hidden large-`h` exception.

Expanding `Q_i Q_j` with the nonnegative linearization coefficients gives

`(J^N)[i,j] = sum_h ell(i,j,h) c(N,h;k)`.

Terms with `h>N` vanish by orthogonality. The remainder is nonnegative for every pair of indices whenever `N>=4r-1`. The proof establishes an infinite entrywise statement rather than extrapolating a finite matrix experiment. The independent controls nevertheless test starting vertices as large as 1,000, the exact threshold, and all `r=2,...,20`.

## Eventual graph and terminal seed qualification

For `s=4r`, the submitted edge multiplicities equal `J^s` and vanish whenever `|i-j|>s`. Each vertex has finite degree and finite integer edge multiplicities. The terminal vector of type `t` has support in `0,...,s+t`. A length-`q-1` walk from zero reaches at most `(q-1)s`, so the count is finite even on this infinite graph. The exact decomposition `N=qs+t`, `q>=1`, `0<=t<s`, gives

`e0^T (J^s)^(q-1) J^(s+t) e0 = A(N,k)`.

The independent block-walk controls cover every remainder for `r=2,...,6` and `q=1,...,4`, and independently compare word-defined transfer weights with Jacobi multiplication.

**Qualification:** the statement that no value of `A` is used as a prescribed multiplicity can only mean that the displayed coefficient formulas provide the multiplicities without calling an `A` oracle. Numerically, `v_0^(t)=c(s+t,0;k)=A(s+t,k)`. In the first block `s<=N<2s`, the walk has length zero, so the object is simply one of these terminal colors. This is an explicitly formula-seeded counting model, not an intrinsic combinatorial explanation of its seed interval. The equality does not invalidate Theorem 6, nonnegative transfer, or equation (19), but it strengthens the naturalness limitation and forbids presenting the eventual model as a seed-free structural solution. The frozen files already disclaim naturalness and an all-size resolution; this audit makes that particular limitation explicit.

The bound is sufficient, not asserted optimal. Choosing the even block length `4r` also avoids any ambiguity about residues and terminal positivity. The unbounded family of short odd ranges as `k` varies remains outside this unsigned model.

## Odd signs and remaining problem

The derivative identity `dA(N,k)/dk = N A(N-1,k)` follows coefficientwise and is strictly positive when `N` is odd. Each odd-degree polynomial is therefore strictly increasing with one real zero. This is sign information, not a new interpretation.

For fixed `r`, the odd partial sums decrease up to their turning region and then increase toward `exp(-r)>0`, by the exact increment formula. Since the first odd value is negative, there is at most one negative-to-positive crossing. The proof correctly avoids asserting that an integer parameter can never give equality.

Unequal-length half-path products need not have a common sign. At `k=-1`, the products `(-4,0,12)` sum to the positive value eight. The even involution does not cancel across their endpoints, so simply reusing it does not solve the odd case. A generic global ranking of all remaining objects would not provide the missing structural account. The packet explicitly maintains this distinction.

## Reproduction and release boundary

Run `python3 audit_controls.py` in this audit directory and compare its deterministic output with `audit_controls.json`. The script uses only the Python standard library, imports no author code, reads no source or private records, uses exact integer/rational arithmetic, and performs no network operations. Its expected total is 245,193 assertions with seven negative controls. The independent author replay is preserved separately as `independent_author_rerun.json`.

The frozen inputs and their hashes are recorded in `FROZEN_INPUTS.json`. `AUDIT_MANIFEST.json` seals the portable audit files and the exact verdict. No frozen author file was edited. No remote action, source-document creation, or upload occurred. Only the manifest-listed original report, verification code, and JSON records belong in a portable audit release. Primary PDFs, full extracted source text, source-page images, corpus records, private research/history, and Python cache files are excluded.

**Final recommendation: accept the demonstrated partial mathematics, retain five completed approaches and the unresolved original all-size status, and preserve both the global-cancellation and formula-seeded-model qualifications.**
