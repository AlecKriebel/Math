# Independent adversarial audit: link counts and endpoint spectra

PR #872, problem 30006628 / OWR-14299911-031. Frozen head: `e3d77731b45b5f463df46e769faa01d65fe193ec`.

**Verdict: PASS within the assigned counting and spectral scope.** No mathematical defect requiring a repair was found in Sections 2, 2.1, 4, and 5 of the frozen candidate. The all-residue degree growth in (4.3) also follows from the audited estimates. This is an AI mathematical audit, not human peer review, formal verification, a novelty certificate, or independent verification of every external theorem used later in the argument.

The exact frozen `PROOF.md` has SHA256 `3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`. The candidate concerns a fixed finite alphabet partitioned into at least three nonempty factors, with an inversion involution preserving each factor. The alphabets, their factor sizes, and the density are fixed before the length tends to infinity. The argument cannot be promoted to a uniform result over changing alphabets.

## Independence and original model

I read the frozen proof and source manifest, then saved `INDEPENDENT_RECONSTRUCTION.md` before reading any inherited audit verdict or candidate checker. In fact no inherited audit, second review, or candidate checker was used in this family. The new diagnostic program was written independently from the definitions and oriented relator corners.

I separately read Definition 1.1, Question 1.9, and the two-factor parity remark in the [official arXiv v2 HTML of Random Quotients of Free Products](https://arxiv.org/html/2502.08630v2). They specify indexed syllable words, cyclic reduction at the last/first boundary, independent sampling with replacement, and the limit through all lengths. Question 1.9 itself permits two factors; this candidate explicitly addresses at least three factors. This family did not independently certify the OWR restriction to at least three factors; that target-scope comparison remains part of the parent audit. The full arXiv paper and other cited external proof bodies were not audited by this family. The primary HTML retrieval is pinned in `PRIMARY_READING_RECEIPT.json` and kept private.

## 1. Exact corner count, including orientations and rejection

Write a retained three-block word as `u v w`; its link has edges `{u^{-1},v}`, `{v^{-1},w}`, and `{w^{-1},u}`. Vertices are all oriented blocks, including both members of each inverse pair. Formal generators are only chosen once per inverse pair; that does not halve the link's vertex set.

For one corner and the ordered assignment `x=u^{-1}, y=v`, the joining condition is

`A[f(x),f(y)] = 1`.

The remaining block begins in a factor different from `l(y)` and ends in a factor different from `l(x)`. Requiring that it belong to `V_h` gives exactly `T_h(l(y),l(x))` completions. Each completion determines one indexed syllable sequence at the fixed cut positions. No quotient by cyclic rotations is being taken, and no extra length or rotation factor belongs in this count. The same reasoning applies to a corner crossing the last/first cut, by placing the prescribed blocks back at their fixed positions.

For the reverse orientation, assign `u=y^{-1},v=x`; the same joining constraint remains and the count is `T_h(l(x),l(y))`. Reversal of a reduced word preserves membership in `V_h`, so these two completion counts agree. Equivalently, if `C_h[a,b]` counts words in `V_h` with endpoints `a,b`, then `C_h` is symmetric and

`T_h = A C_h A`.

Thus each oriented type incidence contributes precisely the kernel in (4.1). The oriented incidence matrices are

- equal lengths: `[6]`;
- lengths `(L,L,L+1)`: `[[2,2],[2,0]]`;
- lengths `(L,L+1,L+1)`: `[[0,2],[2,2]]`.

There are six oriented edge incidences per retained sample. In particular a same-type undirected corner contributes two incidences of that type. For different types, its two directions contribute to opposite entries. These multiplicities are essential.

There is no loop: `x=y` would give `A[f(x),f(x)]=0`. Repeated edges and repeated sampled relators are counted with multiplicity, as required. The three corners of one relator need not be independent; the calculation uses only linearity of expectation. Each original sample is drawn from all `Z_ell` words, so the normalization is `N_ell/Z_ell`, not conditional normalization by the retained word count. Discarding a sample is represented by zero contribution. As a concrete diagnostic, for three involution letters and length nine there are 510 cyclic words but only 66 retained ones. Directly accumulated adjacency has total mass `6*66`, not `6*510`.

It follows analytically, not just in the finite tests, that

`bar E[x,y] = (N_ell/Z_ell) c_tu A[f(x),f(y)] T_h(l(x),l(y))`.

## 2. Inverse-fixed deletion and uniform endpoint errors

The full endpoint count is `(A^(t-1))[a,b]`, because these are actual free-product normal forms. Even-length inverse-fixed words are impossible: the middle two syllables would lie in the same factor. For odd `t=2s+1`, an inverse-fixed word is determined by its first `s` syllables and a self-inverse middle letter. The first/last endpoints must be inverse letters; this is a restriction, not an additional family of uncounted fixed words.

There is a useful exact integer formula, implemented independently in the diagnostic program. Let `j(a)=a^{-1}` and let `q_d` be the number of self-inverse letters in factors different from the factor of `d`. For `s>=1`, the removed endpoint matrix is zero except at `(a,j(a))`, where its value is

`sum_d (A^(s-1))[a,d] q_d`.

For `t=1`, the removed matrix is the diagonal indicator of self-inverse letters. These formulas agree entry by entry with direct enumeration for lengths one through four in all five diagnostic alphabets, including a factor containing both an inverse pair and a self-inverse letter.

To justify the asymptotic estimate uniformly, let `lambda` be the Perron eigenvalue of `A`. Since `A` is symmetric and primitive, its operator norm is `lambda`, and its nonprincipal eigenvalues have absolute value strictly below `lambda`. For `s>=1`,

`|W_s| = 1' A^(s-1) 1 <= k lambda^(s-1)`.

Consequently the total odd-length deletion is at most `k |W_s| = O(lambda^s)`. It bounds every deleted endpoint class as well. Fix any

`eta in (max(max_nonprincipal |mu|/lambda, lambda^(-1/2)), 1)`.

Finite-dimensional diagonalization and the deletion bound give

`C_t[a,b] = lambda^(t-1) r_a r_b (1 + O(eta^t))`

uniformly over all `a,b`. Here uniformity is over the finitely many endpoint indices for the one fixed alphabet. Positivity of the minimum Perron coordinate is what permits conversion of the absolute error to a relative error, including endpoint pairs in the same factor. Thus every class is eventually nonempty; this statement is not asserted for every small length.

Multiplying `C_h` on both sides by the fixed matrix `A`, and using `Ar=lambda r`, gives

`T_h[p,q] = lambda^(h+1) r_p r_q (1 + O(eta^h))`

uniformly over `p,q`. This supplies (2.1) and (2.2) with exponentially decaying errors. It does not assume independent endpoints, and no parity problem survives the exponentially small deletion.

All three block lengths in each cut pattern are at least `L`. Therefore products, endpoint sums, and degree normalization below have uniform `O(eta^L)` errors. The constants can depend strongly on the fixed alphabet and its Perron coordinates.

## 3. Degree scale and the potentially dangerous unequal sizes

For a fixed type `u` and endpoint pair `c,f`, multiply the leading factors from its vertex-class size and the completion count:

`lambda^(u-1) r_c r_f * lambda^(ell-t-u+1) r_b r_f`.

Their powers combine to `lambda^(ell-t)`, regardless of whether `u=L` or `L+1`. The endpoint sum is

`sum_c,f A[a,c] r_c r_f^2 = lambda r_a`.

It follows that the expected degree is

`bar d_x = (N_ell/Z_ell) lambda^(ell-t+1) r_a r_b h_t (1+O(eta^L))`,

where `h_t=sum_u c_tu`. This confirms (4.2). A spurious factor `lambda` from the larger type must not be retained in the limiting type walk: its class-size factor cancels the complementary block's count exactly.

Since `Z_ell=lambda^ell(1+o(1))`, flooring `Z_ell^d` changes it by relative `o(1)`. Positive fixed Perron coordinates and `t<=ceil(ell/3)` give the stated lower bound for `delta_ell`. The estimate `|W_t|<=k lambda^(t-1)` and at most two length types give the stated upper bound for `M_ell`. These estimates apply to every residue. In particular `delta_ell` grows exponentially for any fixed `d>1/3`, while `log M_ell=O(ell)`.

## 4. Exact compression, stationary weights, and tensor spectrum

For each endpoint label `alpha=(t,a,b)`, every full adjacency entry to a fixed destination class is constant over the source class. The degrees are also constant there. The full walk maps all functions into the space of functions constant on endpoint classes. Every nonzero eigenvalue therefore lies in the restriction to that space; the remaining full-walk eigenvalues are zero. This is an exact finite-dimensional statement, independent of the asymptotic calculation.

The compressed transition is

`hat P[alpha,beta] = v_u(c,f) bar E[x,y] / bar d_x`.

Its exact reversible weights are `v_t(a,b) bar d_x`. Asymptotically these weights, normalized to sum one, tend to

`pi(t,a,b) = (h_t/6) r_a^2 r_b^2`.

The cancellation of the type-length powers occurs again here. For the two unequal residues, the limiting type masses are respectively `(2/3,1/3)` and `(1/3,2/3)`, not a uniform measure. These weights give an alternative route to spectral continuity: conjugate the compressed reversible walks by their positive square-root stationary weights. Their symmetric matrices converge in the fixed dimension, so the ordered real eigenvalues converge.

The limiting transition entries are precisely

`Q[t,u] P[a,c] r_f^2`.

Thus the operator is `Q tensor P tensor R`. The type matrix has eigenvalues `1,-1/2` in either unequal residue, and only `1` in the equal residue. The letter walk is similar to `A/lambda`. To check the sign claim, on the codimension-one subspace `sum z_a=0`, the quadratic form of `A` is nonpositive. Hence it has at most one positive eigenvalue. Perron positivity, connectivity, and the triangle show that its sole positive eigenvalue is simple and dominates all other absolute eigenvalues strictly. Therefore the remaining eigenvalues of `P` lie in `[-rho,0]`, with `rho<1`.

The matrix `R[b,f]=r_f^2` has simple eigenvalue one and the remaining eigenvalues zero. All tensor products are consequently as claimed. In unequal residues, products of `-1/2` with negative eigenvalues of `P` are positive and their maximum is `rho/2`. Ignoring those products would be a genuine mistake; the candidate includes them. In the equal residue every nonprincipal limiting eigenvalue is nonpositive, with zeros from the class complement or from `R` as appropriate. The principal eigenvalue is simple.

The limit's Laplacian gap is at least `1-rho/2`, exceeding

`gamma = 1/2 + (1-rho)/4`

by `(1-rho)/4>0`. Fixed-dimensional convergence therefore supplies the candidate's eventual bound (5.2). Taking a maximum of the three eventual length thresholds covers all positive length residues. The additional alternation in inverse-fixed deletion as `L` changes parity is already absorbed in the uniform exponential error.

A useful limiting boundary check is factor sizes `(1,1,M)`. The extreme eigenvalues are `(1+sqrt(1+8M))/2` and `(1-sqrt(1+8M))/2`, with another eigenvalue `-1`. Thus `rho=1-1/lambda`, and the unequal-residue gap above one half tends to zero as `M` grows. This does not contradict the theorem's fixed-alphabet quantifiers, but it rules out silently claiming a uniform gap in that enlarged setting.

## 5. Reproducible finite diagnostics and their limits

`independent_link_enumeration.py` uses only Python's standard library and imports no candidate checker. It directly generates reduced syllable sequences, checks the last/first boundary, rejects inverse-fixed blocks, and accumulates every corner's two ordered adjacency contributions. It separately counts completions and compares the candidate kernel against every ordered vertex pair. Thus it does not generate a link by assuming (4.1).

The five inversion alphabets can be realized by `C2*C2*C2`, `C3*C2*C2`, `C4*C2*C2`, `(C2 x C2)*C2*C2`, and `C2*C3*C4` with all nonidentity elements as alphabets. Lengths six through eleven are used for the first two configurations, and six through eight for the other three. This tests every residue both with and without inverse-fixed deletions, several unequal factor sizes, inverse pairs, and mixed involution behavior.

The final runs verified:

- 21 finite cases, 129,434 cyclic relators, and 95,628 retained relators;
- all 47,816 ordered expected-link entries;
- 26,932 source-vertex/destination-class row checks for exact compression, and exact rational detailed balance and row sums;
- 13 small full-walk spectra against compressed spectra with the necessary zero eigenvalues appended;
- the per-sample bound of three on each vertex degree, including repeated block letters;
- 120 larger-length endpoint/degree/compressed-entry/stationary-weight diagnostic rows, at `L=4,5,8,9,16,17,24,25` across all residues and five alphabets;
- tensor-spectrum diagnostics for five part-size vectors, including the imbalanced `(1,1,32)` case.

Endpoint and completion counts in these calculations are exact integers, and compressed walk fractions and detailed-balance checks are exact rationals. The eigensolver and Perron-limit error comparisons use floating point and are only diagnostics. Their finite symmetric eigensolver residuals were below `1.8e-13` in the direct enumeration cases. No numerical assertion is used as the proof of an asymptotic statement.

Two deliberate kernel errors are exposed. Halving the oriented incidence count changes 21,330 tested entries. Omitting the inverse-fixed deletion from the remaining block changes 9,710 tested entries. The program also supports these two mutations as explicit flags. Each mutated program run terminates with the intended kernel-mismatch error in both normal and optimized Python: four expected rejections in total. These failures use actual runtime guards, not `assert` statements. The two full successful runs under CPython 3.14.6, with `-I -S -B` and with the additional `-O`, produced byte-identical results. `REPLAY_RECEIPT.json` records the commands, script hash, results hashes, and return statuses.

To reproduce the successful diagnostics, run the script with `--output` pointing to a fresh results file. To reproduce expected failures, add `--mutation single-orientation` or `--mutation omit-fixed-completion`; repeat with `-O` if desired. These computations can falsify finite kernel or compression errors. They cannot by themselves establish property (T), certify all asymptotics, exhaust every possible factor alphabet, or establish priority.

## Final disposition

The strongest result verified here is the exact mean-link kernel with inverse-fixed deletion, the uniform fixed-alphabet endpoint asymptotics, the all-residue degree scale, and the limiting mean-link gap strictly above one half. No repair is requested for these steps. This assigned audit is complete (100%). The full theorem still relies on the parent audit's validation of the original target scope, triangular spectral criterion, concentration and transfer steps, and separate priority and publication reviews. No claim is made here that those separate checks have been completed, or that the result has been human reviewed or formally proved.
