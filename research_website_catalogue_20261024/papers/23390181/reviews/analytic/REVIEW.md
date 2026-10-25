# Independent analytic review — Zenodo 23390181

**Verdict: the stated fixed-data theorem is supported. No substantive mathematical defect was identified.** I reconstructed the complete argument in the seven-page publication and its authored mathematical supplement. The exact sampling law, unequal block lengths, torsion deletion, finite-index image, mean spectrum and concentration steps fit together. The cited established property (T) criterion and matrix concentration results have the required scope.

This is an AI mathematical review, not human peer review, a proof-assistant certificate, or a novelty/priority certificate. Finite tests supplement the analytic argument and do not prove the asymptotic theorem. No repair, outreach, website, spreadsheet, Git or publication action was taken.

## 1. Publication binding and independence

- Title: *Property (T) above one-third density in random free-product quotients*.
- Author: Alec Kriebel. Version **1.0.0**, dated **2026-10-15**.
- [Zenodo record](https://zenodo.org/records/23390181), [DOI](https://doi.org/10.5281/zenodo.23390181).
- Published `property-t-free-product-note.pdf`: **96,815 bytes, seven pages**, SHA256 `860c28002e29a84522c850e66679c9e344caddf650f1db43038044f139cdac58`, MD5 `eb2e09080b1a696dde35f696a0c30731`.
- Published `property-t-free-product-verification.zip`: **453,413 bytes**, SHA256 `c300b11741b2f8da35febe771114b5def4489bf91bf6d87d19debc5e6bc57731`, MD5 `a586bc85cfea2e5a2f8737212ba473cd`.
- The extracted `note.pdf` is byte-identical to the primary PDF. All source identities above were rechecked against the fresh receipt. Additional inspected-source hashes are retained separately.

I read all seven published pages and all 214 lines of the authored `source/PROOF.md`. Before archived diagnostic replay, I saved my independent mathematical checkpoint in `INDEPENDENT_PROOF_CHECKPOINT.md`. No sibling report or historical mathematical audit report was read. The acquisition record and authored proof contain incidental descriptions of historical acceptance, audit and priority work; those statuses were visible but were not used as mathematical evidence. Archive names and checker paths were also visible. The replay machinery authenticates bytes of audit documents but does not make their arguments evidence for this verdict.

## 2. Exact claim and boundaries

Fix, before the length tends to infinity:

1. An integer n at least three and nontrivial finitely generated groups G_i.
2. In each G_i, a finite, nonempty, inverse-closed generating **set of nonidentity elements** B_i. The alphabet is their disjoint union. Different elements in a factor are different letters, rather than duplicate labels for the same element.
3. A real density d satisfying 1/3 < d < 1.

Let F be the free product of the factors. S_ell consists of rooted words of exact syllable length ell, with adjacent factors different and the last factor different from the first. Rotations and inverses are not identified. Draw floor(|S_ell|^d) **independent uniform samples with replacement**, and quotient F by their normal closure. Theorem 1 asserts that this quotient has property (T) with probability tending to one as ell tends to infinity through **all integer lengths**.

The proof covers arbitrary torsion and infinite or non-finitely-presented factors; it uses the free-product normal form and the finite alphabets, not an algorithm for a factor's word problem. Fixed-radius word-ball alphabets are included. There is no claimed uniformity when alphabets, factor number, radius or density vary. There is no result here at d = 1/3 or for two factors. The assertion is an upper-density sufficient condition, not a sharp threshold or a finite-length guarantee. The range above 1/2 is consistent with the previously known finite collapse; the argument itself does not need that collapse theorem.

The linear-normal-word variant in Section 6 is a further consequence by thinning, with its different law explicitly distinguished below.

## 3. Independent proof reconstruction

### 3.1 Counting matrix and inverse-fixed deletion

Define A_ab = 1 when a and b are in different factors and zero otherwise. This symmetric complete multipartite graph is connected and has a triangle because n >= 3. It is primitive, has Perron eigenvalue lambda >= 2, and has a strictly positive unit eigenvector r. Identical rows within a part force equal Perron coordinates there, so r_a = r_(a inverse).

For any real z,

`z^T A z = (sum_a z_a)^2 - sum_i (sum_(a in B_i) z_a)^2`.

On the codimension-one subspace sum z_a = 0 this is nonpositive. The min–max principle therefore gives at most one positive eigenvalue; Perron–Frobenius supplies exactly one, with all other absolute values strictly less than lambda. Thus the conjugate stochastic matrix P_ab = A_ab r_b/(lambda r_a) has simple eigenvalue 1 and other eigenvalues in [-rho,0] for some fixed rho < 1. This sign information, stronger than just mixing, is essential later.

Normal forms give exactly (A^(t-1))_ab reduced words of length t with endpoint letters a,b and exactly tr(A^ell) rooted cyclic words of length ell. Spectral decomposition gives tr(A^ell) ~ lambda^ell and uniform exponential endpoint errors. The normal-form uniqueness is valid for arbitrary factor groups with the stipulated alphabets.

If a reduced word has even length, equality to its inverse would force its two middle syllables to be inverse elements of the same factor, contradicting reducedness. For length 2s+1, an inverse-fixed word is determined by its length-s prefix and a central involution. There are O(lambda^s) such words. Since every Perron coordinate is positive and the number of endpoint classes is fixed, subtracting this total bound from any endpoint count gives

`v_t(a,b) = lambda^(t-1) r_a r_b (1 + O(eta^t))`

for a fixed eta < 1, uniformly in endpoints. In particular, every endpoint class of V_t is eventually present. This remains true when every original letter is an involution.

Likewise, the unrestricted completion count between exterior endpoint letters p,q is (A^(h+1))_pq. Removing inverse-fixed middle blocks changes it by only O(lambda^(h/2)), giving

`T_h(p,q) = lambda^(h+1) r_p r_q (1 + O(eta^h))`.

Inversion of the middle block swaps its endpoint factors; A is constant under inversion within a factor. Consequently T_h(p,q) = T_h(q,p) exactly. Neither endpoint independence nor uniformity in varying alphabets is being assumed.

### 3.2 Triangular presentation and the index bound

The fixed cut lengths are (L,L,L), (L,L,L+1), and (L,L+1,L+1) for the three residues of ell. The signed generator alphabet is the disjoint union of V_t at the occurring lengths, paired by inversion. Distinct lengths are distinct free-product normal forms, and deletion makes each inverse pair have two members.

Only sampled words whose three blocks lie in their respective V_t are retained. Their triangular relation maps to an original relator in G_ell. This gives a well-defined surjection from the finite triangular presentation Gamma_ell onto H_ell generated by the block images. No claim that Gamma_ell has the original random quotient law is needed.

The formal triangle is cyclically reduced: adjacent inverse blocks would have matching factor labels at their touching syllables, contradicting the original cyclic reducedness. Its three link edges are {u inverse,v}, {v inverse,w}, {w inverse,u}. There are no loops. Repeated edges and repeated relator cells are retained with multiplicity; a duplicate cell does not alter the presentation group. The spectral criterion applies to this multigraph presentation link.

For the deterministic transfer, fix any letters a,b. Choose a factor C different from both their factors. When L is even, any reduced suffix of length L-1 starting in C works: both av and b inverse v are even reduced words and hence not inverse-fixed. When L is odd and at least five, use an even suffix of length L-1 starting and ending in C. The sequence C,D,E,C exists at length four with three distinct factors, and appending D,C gives every longer even length. Both resulting blocks then have different first and last factors and cannot equal their inverse.

The group identity `(av)(b inverse v) inverse = ab` shows that the block subgroup contains every two-letter product, including products in the same factor. Let K be generated by these products. It is normal because `c(ab)c inverse = (ca)(b c inverse)` is again in K for each alphabet letter c. In F/K, all alphabet letters have the same image of order at most two. Since the alphabets generate the factors, they generate F, and [F:K] <= 2. Thus [F:<V_L>] <= 2 and [G_ell:H_ell] <= 2. No factor embedding in the random quotient, finite presentation of the factors, or substitution of a different sampling model is used.

### 3.3 Exact expected-link kernel

The number of oriented corners of each ordered type pair is

```
C_0 = [6],       C_1 = [[2,2],[2,0]],       C_2 = [[0,2],[2,2]].
```

Take x in V_t and y in V_u with endpoint letters (a,b) and (c,f). For a fixed oriented corner whose prescribed adjacent blocks are x inverse,y, their common boundary contributes A_ac. The remaining block has length h = ell-t-u, must belong to V_h, and must close the two remaining boundaries. Its exact number is T_h(f,b) = T_h(b,f). Every such completion is exactly one word at the designated cut positions. The reverse oriented corner has the same count. Summing all positions therefore gives

`Ebar_xy = (N_ell/Z_ell) c_tu A_ac T_h(b,f)`.

This derivation explicitly includes rejection of inverse-fixed blocks. It does **not** condition on the number of surviving samples, assume independence of the three corners, or require rotating unequal-length blocks to preserve the fixed-cut rule. The diagonal vanishes because A_aa = 0.

Summing over destination endpoint classes, the powers of lambda are `lambda^(u-1) lambda^(h+1)`, while the first-endpoint sum contributes `sum_c A_ac r_c = lambda r_a` and the last-endpoint sum contributes `sum_f r_f^2 = 1`. Hence

`dbar_x = (N_ell/Z_ell) lambda^(ell-t+1) r_a r_b h_t (1+o(1))`,

where h_t is the row sum of C. All errors are uniform for the fixed data. With floor rounding absorbed, the minimum expected degree is at least a positive constant times lambda^(d ell-ceil(ell/3)), and the number of signed vertices is at most a constant times lambda^ceil(ell/3). Thus the minimum degree grows exponentially for every fixed d > 1/3, whereas log M_ell grows only linearly. This is the precise place where the density restriction is used.

### 3.4 Mean spectral gap, including the unequal residues

Rows of the mean walk depend only on type and the two endpoint letters, and each individual entry depends only on the source and destination endpoint labels. Thus the image lies in the space of class-constant functions. The compressed chain has entries `v_u(c,f) Ebar_xy/dbar_x`, at most 2k^2 states, and reversible measure proportional to class size times expected degree. Every nonzero eigenvalue of the full walk is an eigenvalue of this compression; all remaining full-walk eigenvalues are zero.

The compressed chain converges to Q tensor P tensor R, where Q_tu = c_tu/h_t and R_bf = r_f^2. Q has eigenvalue 1 only in the equal-length case and eigenvalues {1,-1/2} in both unequal cases. R has eigenvalues 1 and zero. P has one eigenvalue 1 and all others in [-rho,0].

Consequently, the limit has a simple eigenvalue 1. In unequal residues, the largest possible other eigenvalue is rho/2, produced by multiplying the negative type eigenvalue -1/2 with a negative eigenvalue of P. Ignoring this product would be wrong, but the publication includes it. For equal lengths, the other full-walk eigenvalues are at most zero. Extra zero modes present no problem in either case.

The compressed dimension is fixed, its spectra are real by reversibility, and its characteristic polynomial varies continuously. Thus, eventually, the full mean graph is connected and its normalized Laplacian gap is at least

`gamma = 1/2 + (1-rho)/4 > 1/2`.

The gap between the limiting unequal-case bound 1-rho/2 and gamma is (1-rho)/4, strictly positive. Taking the maximum of the three residue-specific starting lengths makes the bound valid through all integer lengths. No bound uniform in rho approaching one is asserted.

### 3.5 Whole-relator concentration and the change of degree weights

For one draw, the link Laplacian L_j is either zero or the sum of three edge Laplacians. It is positive semidefinite, has row sum zero and norm at most six. These matrices are independent across sampled words; the three edges within one sample need not be independent.

Normalize by the deterministic expected degree matrix: X_j = Dbar^(-1/2) L_j Dbar^(-1/2). Every X_j kills z = Dbar^(1/2)1 and has norm at most 6/delta_ell. Restriction to z-perpendicular is to a common deterministic invariant subspace, so it preserves self-adjointness, positivity and independence. The expected sum there has minimum eigenvalue at least gamma. Tropp's lower tail therefore gives the failure bound

`M_ell exp(-epsilon^2 gamma delta_ell/12)`.

If the actual expectation eigenvalue exceeds gamma, the event at the smaller threshold is contained in the event at the larger one, and weakening the exponent to gamma is valid.

A fixed signed vertex can receive at most one incidence from each block occurrence: the incoming occurrence is at the block and the outgoing occurrence at its distinct inverse. Thus its degree increment lies in [0,3], even for repeated blocks or triple parallel edges. The scalar upper tail, rescaled by three and union-bounded over vertices, gives

`M_ell exp(-epsilon^2 delta_ell/9)`.

No independence between degrees of different vertices is required. Both failure bounds vanish because delta_ell grows exponentially while log M_ell is O(ell).

On the resulting event, for every g satisfying g^T Dbar 1 = 0,

`g^T L g >= (1-epsilon) gamma g^T Dbar g`,

and D <= (1+epsilon)Dbar. The first inequality forces the kernel of L to be one-dimensional: a kernel of dimension at least two would intersect this codimension-one subspace nontrivially. Since the vertex count is eventually greater than one, the actual link is connected with positive degrees.

For the generalized eigenvalues of (L,D), the second eigenvalue equals the maximum, over all codimension-one subspaces, of the minimum Rayleigh quotient on that subspace. Using the Dbar-centered subspace is therefore legitimate and gives

`lambda_1 >= (1-epsilon) gamma/(1+epsilon)`.

It is unnecessary to replace Dbar-orthogonality by D-orthogonality. Choosing epsilon strictly between zero and (2gamma-1)/(2gamma+1) makes this lower bound greater than 1/2. This proves the random-link condition needed for property (T).

The established triangular-link criterion gives property (T) for Gamma_ell. Its quotient H_ell inherits it, and the index-at-most-two inclusion transfers it to G_ell. This completes the exact theorem.

### 3.6 Linear-word thinning in Section 6

For uniformly sampled linear reduced words, the universe has size U_ell = 1^T A^(ell-1)1 ~ lambda^(ell-1)(sum r_a)^2. The cyclic fraction tends to lambda/(sum r_a)^2 > 0. Among floor(U_ell^d) independent linear draws, the number of cyclic draws is binomial with mean of order lambda^(d ell).

Choose a fixed d-prime strictly between 1/3 and d. The target floor(Z_ell^(d-prime)) is negligible relative to that mean, so the count exceeds it with probability tending to one. Conditional on the marks identifying cyclic draws, the retained words are independent uniform cyclic words; their identities are independent of the mark count. Apply Theorem 1 to the prescribed initial retained sample. The full linear presentation has additional relators and is a quotient, so it also has property (T). This supports the paper's clarification of the workshop's abbreviated normal-word definition without identifying the two probability laws.

## 4. Primary imports and limits of that checking

1. **Kotowski–Kotowski, arXiv:1106.2242v2.** I read the primary definitions and Remarks 2.10–2.11, Definition 2.12 and Theorem 2.13. The normalized graph Laplacian counts parallel edges. The criterion requires a connected presentation link with first nonzero normalized eigenvalue strictly greater than 1/2 and concludes property (T); the relevant permanence statements cover quotients and finite-index extensions. Global inversion carries the publication's edge convention to theirs. Repeated cells are legitimate indexed relator occurrences in the same presentation complex and only contribute repeated link edges. Their discussion of distinctness as a probabilistic fact below density 1/2 is not a prerequisite of the deterministic criterion. [Primary source](https://arxiv.org/pdf/1106.2242v2).

2. **Tropp, arXiv:1004.4389v7.** I checked Corollary 5.2, Remark 5.3 and the adjacent lower/upper-tail derivations. They apply to finite independent positive semidefinite self-adjoint summands with an almost-sure uniform norm bound. The paper's constants follow after the stated normalization and restriction; the one-dimensional upper tail gives the degree estimate. These are established imported results, not claimed to be independently reproved here. [Primary source](https://arxiv.org/pdf/1004.4389v7).

3. **Einstein–Krishna–Montee–Ng–Steenbock, arXiv:2502.08630v2.** Definition 1.1 uses fixed-radius nonidentity word-ball alphabets, cyclic boundary restriction and sampling with replacement. Theorem 1.2 and Question 1.9 were checked for model and scope. The theorem under review answers the at-least-three-factor part, not the entire two-factor question. [Primary source](https://arxiv.org/html/2502.08630v2).

4. **Oberwolfach report 8/2026.** I checked the model shorthand on printed p. 523 and Problem 16 on pp. 535–536. The question explicitly concerns at least three factors and density above 1/3. The workshop shorthand omits an explicit wrap-around condition; the publication's separate thinning argument covers that reading. This checks the stated target's scope, not worldwide historical openness or priority. [Primary source](https://ems.press/content/serial-article-files/53603).

The primary PDF URLs, lengths, retrieval times and SHA256 values are retained in `reference_receipts.json`. The full literature-priority comparison, dates of first public release of antecedents, and later improvements in other random-group models were not independently audited in this analytic review. Ashcroft and Drutu–Mackay are precedents here; their results are not needed to fill an unproved step in the reconstructed suffix or block argument. No extrapolation from ordinary free-group models was used.

## 5. Reproduction and fresh controls

The primary ZIP, extracted PDF and inspected source bytes were bound before execution. I read the closed-inventory and replay runners and inspected archived checker import/call structure for side effects. The full published verifier was run with `-I -S -B`, using the SHA256 of the index obtained from the freshly bound ZIP. It executed authenticated copies in relocated temporary directories.

**Published replay: PASS.** It authenticated 143 package members, 15 frozen original files and 26 members of the three inner archives. All **14** exact positive/negative diagnostic receipts matched in normal and optimized Python. The optional replay of three separately supplied historical corpora and six pinned reference PDFs was not run; those provenance inputs were not supplied. That omitted optional mode checks historical-source provenance rather than extending the finite mathematical tests run here. No source files were changed. The archived checkers' success is finite diagnostic evidence, not an asymptotic certificate or a substitute for this proof reconstruction.

The fresh `independent_controls.py` imports no supplied checker. It independently builds reduced words, performs arithmetic in free products of cyclic groups, counts endpoint classes, and forms the link directly. It passed **747,840 assertions in 23 families**:

- **23 complete rooted-word enumerations**, containing **211,058 cyclic word instances** in total. Alphabets have sizes (1,1,1), (2,1,1), (2,2,2), (1,2,3) and (1,1,1,1). The enumerations cover all residues, self-inverse letters, nontrivial inverse pairs, rejected blocks and repeated link edges. They compare **64,616** ordered vertex-pair counts to the exact kernel.
- **1,582 suffix witnesses**, each checked for length, reducedness, absence of inverse fixing and the two-letter group identity in independently implemented cyclic-factor normal forms; lengths range from four through seventeen.
- **364** exact endpoint comparisons checking a separately derived inverse-fixed deletion formula.
- **72** finite factor-compressed mean matrices across twelve combinations of alphabet sizes and length residues, with L = 4,8,16,32,64,128. Exact integer count construction precedes explicitly numerical symmetry and eigenvalue diagnostics. The highly skewed case (1,1,40) has rho approximately 0.894272 and unequal-residue limiting gap approximately 0.552864, correctly above one-half but well below one. This tests the negative-times-negative type-eigenvalue contribution.
- Three seeded samples of 5,000 whole relators at lengths 12,13,14 independently test the deterministic common kernel and the mean-centered min–max comparison. All actual gaps exceed the derived comparison bounds. These samples are diagnostics, not empirical proof of the probability limit.
- Negative controls show an inverse-fixed torsion block, the failure of strictness in the two-factor tensor (nonprincipal eigenvalue exactly one-half), and the loss of exponential degree growth at the critical density.

Exact integer tests and floating eigenvalue diagnostics are distinguished by their family names in the result file. Assertion counts are parameter instances, not independent mathematical discoveries. No formal interval enclosure was constructed for the floating diagnostics; the universal spectral proof rests on the analytic tensor argument, not those numerics.

## 6. Strongest verified result and exact remaining gap

**Strongest verified result:** for the exact rooted, cyclically reduced, independent-with-replacement law and fixed data stated in Theorem 1, including arbitrary fixed finite inverse-closed generating alphabets and torsion, the probability of property (T) tends to one for every fixed 1/3 < d < 1 through all integer lengths. The separate linear-normal-law consequence is also supported by thinning.

**Identified substantive defects:** none. No repair is proposed or attempted.

**Remaining mathematical gap in the stated proof:** none identified beyond the explicitly cited established spectral/concentration and standard normal-form/linear-algebra inputs. This means the argument survived this AI review; it does not mean logical infallibility or human/formal certification.

**Unresolved scope outside this review:** exhaustive novelty, priority, journal acceptance and independent human peer review; two-factor and critical-density extensions; uniformity under growing data; sharp finite-length thresholds. The numerical controls do not settle any of these.

All evidence, source hashes, reference URLs, diagnostic code/results and checkpoint timestamps are retained in this analytic folder. Downloaded reference PDFs, extracts and other caches are ignored locally.
