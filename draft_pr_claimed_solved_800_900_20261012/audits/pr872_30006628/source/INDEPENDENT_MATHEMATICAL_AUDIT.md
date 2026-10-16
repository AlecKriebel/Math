# Independent mathematical audit: random free-product quotients

Date: 2026-10-06 UTC. Target: 30006628 / OWR-14299911-031, rank 924.

## Decision and immutable object

**Decision: ACCEPTED within the stated n >= 3, fixed-alphabet scope by this independent AI mathematical audit.** I found no mathematical gap requiring a correction to the pinned proof. This is a mathematical review, not formal verification, human peer review, journal acceptance, or an exhaustive novelty certification.

The exact accepted object is `PROOF.md`, 19,961 bytes, SHA256:

`3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`

No bytes of that proof were changed. No derivative mathematical repair is needed for this audit's acceptance. The author archive containing it has 12 members, is 20,225 bytes, and has SHA256:

`f5c4e06b7c535a98aa37520ff616b4b63b4bdd7eb100e461de733f7fd7192134`

The author external manifest is 3,285 bytes, SHA256:

`46011dfd09c59dc52c561886c31b0e8ed0c823f5d5f446baf2c5aa35448fdaf0`

Acceptance is based on the proof below the pin, not on the archive's self-reported status or passing finite tests. The archive deliberately records the earlier author-freeze status; this separate report records the audit decision.

## 1. Exact problem and source scope

The actual OWR Problem 16 appears on printed pages 535-536 of *Median Geometry and Applications*, Oberwolfach Report 8/2026. Its property-(T) question concerns at least three factors. I independently inspected the relevant text and the rendered page. The complete exact-ID inherited problem record asks this same property-(T) question, rather than requiring a separate proof of every adjacent conjecture in the workshop report.

Einstein--Krishna--Montee--Ng--Steenbock, arXiv:2502.08630v2, Definition 1.1 on page 2, chooses uniformly with replacement from rooted normal-form syllable sequences, with adjacent factors different also across the last/first boundary. The fixed alphabets are nonidentity radius-m balls in the factor word metrics. These are finite, inverse closed, nonempty, and generate their factors. This is precisely the model used in the candidate; taking the integer part of the sample count has no asymptotic effect.

The public arXiv record identifies v2 as submitted September 28, 2026 and says it is to appear in *Transactions of the AMS*. The PDF carries September 29 internally. Its Question 1.9 on page 4 is still explicitly presented as open. That question is written in the paper's broader n >= 2 framework. The present proof resolves the n >= 3 OWR question, **not every case of the paper's Question 1.9**. The source itself notes that the two-factor odd-length relator set is empty. The candidate does not overextend to it.

The following quantifiers matter: n, the factor groups, their finite generating sets, the radius m, and d in (1/3,1) are fixed before the relator length tends to infinity. The proof treats every sufficiently large integer length, not just a subsequence. It gives no threshold equality result, no varying-alphabet uniformity, and no n = 2 theorem. The more general claim for any fixed finite inverse-closed generating subset in each factor is justified by the same argument.

Primary sources: [OWR report](https://ems.press/content/serial-article-files/53603), [current free-product paper, v2](https://arxiv.org/abs/2502.08630v2).

## 2. Alphabet counting and Perron analysis

I independently checked the adjacency matrix A of the complete multipartite alphabet graph. It is symmetric and irreducible. Because at least three parts are nonempty, it contains an odd cycle and is primitive. Its Perron root is at least 2, and its positive unit Perron vector is constant within each factor part, including each inverse pair.

For any vector z, the displayed quadratic form in the proof is correct. On the codimension-one space where the total coordinate sum is zero it is nonpositive. The min-max principle therefore permits at most one strictly positive eigenvalue. The Perron root supplies that eigenvalue, so every other eigenvalue is nonpositive. Primitivity rules out eigenvalue -lambda. Consequently the transformed stochastic matrix P has spectrum 1 and numbers in (-1,0], with rho < 1 as claimed. This fact is particularly important for the mixed-length residues: merely establishing expansion of the letter graph would not be enough for the stated strict margin.

The normal-form count with fixed first and last letters is exactly (A^(t-1))[a,b], and the cyclic sequence count is exactly trace(A^ell). These count sequences with their starting position, as required by the source sampling model; they do not accidentally count conjugacy classes or unoriented cyclic words. Since A is finite and symmetric, its spectral decomposition gives the claimed endpoint-uniform exponential error. Positivity of finitely many Perron-vector coordinates converts the additive error to the required relative error.

**Verdict:** valid for every fixed finite alphabet in the theorem; no assumption that the parts have equal sizes is used.

## 3. Torsion deletion and endpoint classes

A reduced syllable word equal to its inverse must match the reversed, syllablewise-inverted normal form. An even-length such word would have its middle adjacent syllables in the same factor, contradicting reduction. An odd-length word of length 2s+1 is determined by a reduced prefix of length s and a self-inverse middle letter. There are at most k times the number of such prefixes, hence O(lambda^s), regardless of how many letters in a factor are involutions.

Removing all these words therefore removes only exponentially negligible endpoint counts compared with lambda^(t-1). This remains true even for an endpoint class on which every removed word could be concentrated. All endpoint classes consequently exist eventually. The finite constants may become poor for a very unbalanced fixed alphabet, which is permitted by the theorem's quantifiers.

The retained vertex alphabet V_t is genuinely inverse closed without fixed points. It is a set of actual distinct free-product normal forms; different lengths cannot collide in the original free product. Later coincidences in the random quotient do not prevent defining a homomorphism from a presentation on formal generators.

The exact completion count over all words is A^(h+1), and deleting at most O(lambda^(h/2)) choices gives the completion asymptotic. Symmetry of T_h is valid: reversing and inverting exchanges endpoint factor conditions, and inversion preserves every factor part. Its dependence only on the factors of its two external letters is exact.

**Verdict:** valid with torsion, with many involutions in a factor, and without a finite presentation of the factor groups.

## 4. The triangular group and the actual finite-index image

Each inverse pair of retained block words yields one formal generator. This correctly implements formal inverse symbols rather than identifying distinct words with the same generator. For all three length residues, a retained sampled word yields exactly the indicated three-letter relation. Its image in the desired quotient is the original sampled relator. Therefore the displayed homomorphism onto the subgroup generated by the retained block alphabet is well defined and surjective onto that subgroup.

No triangular relation has adjacent inverse formal letters. If two adjacent blocks were inverses as normal forms, their meeting syllables would lie in the same factor, contrary to the original cyclic reduction. The last/first corner obeys the same condition. Thus the link is loop-free. Repeated edges and repeated relators cause no cancellation of edge multiplicity.

The finite-index argument is stronger than a heuristic about long words generating most of a group. Given arbitrary alphabet letters a,b, the proof constructs a common reduced suffix v so that both av and b^(-1)v belong to V_L. For even L, inverse-fixed words are impossible. For odd L >= 5, first and last suffix factors can both be chosen in a third factor C, different from the factors of a and b. A factor pattern C,D,E,C has length 4; inserting a C,D,C detour extends this by two without destroying reduction. Thus every required even suffix length occurs. Both full words then have different first and last factors, so neither is inverse fixed. Their product (av)(b^(-1)v)^(-1) is exactly ab in the original free product.

Let K be generated by every product of two alphabet letters. Conjugating a generator ab by a letter c gives (ca)(bc^(-1)), which lies in K because the alphabet is inverse closed. Hence K is normal. In the quotient by K, all letters have one common image and that image squares to the identity, so the quotient has order at most two. The original subgroup generated by V_L contains K; its index is at most two. Its image in the random quotient still has index at most two, and adjoining the other block length cannot increase index.

This proves the necessary statement about an **actual subgroup of the actual random quotient**. It does not assume that the triangular group is a subgroup, or that a random model remains unchanged after replacing factors by free groups.

**Verdict:** the triangular homomorphism and finite-index transfer are valid for all three residues and all allowed factors.

## 5. Exact expected-link kernel

I rederived formula (4.1) directly at the individual-vertex level. With vertices x,y, one oriented corner has first block x^(-1) and second block y. Its mutual boundary is permitted exactly when their first letters lie in different factors. The missing block must fit between the last letter of y and the first letter of x^(-1), producing the T_h condition on the last letters of x and y. These are the three boundary conditions, with none omitted. Symmetry of T_h handles the reversed orientation.

There are six oriented incidences when all lengths agree. For (L,L,L+1), the type-incidence matrix is [[2,2],[2,0]], and for (L,L+1,L+1) it is [[0,2],[2,2]]. For the edge crossing the fixed last/first cut, specifying the two endpoint blocks and the missing block still determines precisely one rooted cyclic syllable sequence. No invariance of an unequal-length block pattern under a literal cut rotation is needed; uniform enumeration of the corresponding positional corner is enough.

The factor N/Z is correct because discarded samples contribute zero, without conditioning the distribution of retained samples. The vertex restriction handles inverse-fixed endpoint blocks, while T_h handles inverse-fixed missing blocks. This avoids introducing dependence by selecting a predetermined number of retained relators.

For a destination type u, multiply the completion asymptotic by the endpoint-class size. The powers of lambda give lambda^(ell-t), and the endpoint sum is lambda r_a because sum_f r_f^2 = 1. This yields (4.2), including its lambda^(ell-t+1), h_t, and r_a r_b factors. As an independent consistency check, summing its leading term over all source vertices gives N h_t for a type t and hence 6N in total, matching six incidences per almost-always-retained relator.

**Verdict:** formula (4.1) and expected degree growth are correct, including all inversions and unequal type multiplicities.

## 6. Spectral gap of the mean

The endpoint compression is exact because rows of the mean walk depend only on block length and the two endpoint letters. The image of the operator lies in the endpoint-class-constant subspace. Nonzero eigenvalues are thus those of the compression, and the remaining eigenvalues are zero. Reversibility of the full weighted graph gives reversibility and real spectrum of the compressed walk.

The compressed dimension is at most 2k^2, fixed independently of ell, and every class exists for all sufficiently large ell. Substitution into the exact transition probabilities yields precisely Q[t,u] P[a,c] r_f^2. The source last endpoint b disappears at the limit, as it should. The limiting stationary weights are proportional to h_t r_a^2 r_b^2, another check on the normalization. Thus the tensor decomposition is legitimate even for highly unequal alphabet sizes and unequal block-type population sizes.

For equal block lengths, all nonprincipal limiting eigenvalues are nonpositive, apart from added zeros. For either unequal-length case, Q has nonprincipal eigenvalue -1/2. Multiplication by the negative eigenvalues of P creates positive nonprincipal eigenvalues up to rho/2. The candidate explicitly retains this term instead of mistakenly dismissing all nonprincipal eigenvalues as nonpositive. Since rho < 1, it leaves a strict gap above 1/2.

Finite-dimensional spectral continuity then applies separately to the three residue sequences. There is a common eventual bound because there are only three sequences. The proposed gamma = 1/2 + (1-rho)/4 leaves positive slack below the limiting gap 1-rho/2. The principal eigenvalue is eventually simple; each mean graph is eventually connected. Extra zero eigenvalues of the full walk are harmless.

**Verdict:** the decisive strict gap is correct. It is not uniform when the fixed alphabet parameters are subsequently allowed to vary, and no such uniformity is claimed.

## 7. Dependence-aware concentration and change of normalization

The proof uses independence of sampled relators, not independence of the three edges generated by a relator. This distinction is correct for the exact with-replacement source model. A rejected sample contributes the zero matrix; a retained sample contributes the sum of three edge Laplacians. These are independent positive semidefinite matrix summands with norm at most six.

Normalizing by the deterministic expected degree matrix gives a per-sample norm bound 6/delta. Every such matrix annihilates the same deterministic vector z = barD^(1/2)1, so the restriction to z-perpendicular is well defined and remains self-adjoint and positive semidefinite. The mean restricted sum has minimum eigenvalue at least gamma. Tropp's lower-tail bound gives the displayed exponent epsilon^2 gamma delta/12. Replacing an actual larger mean minimum eigenvalue by gamma weakens the event and bound in the valid direction.

A fixed link vertex receives at most three degree contributions per sampled triangular relation. More explicitly, each block occurrence produces one endpoint at that block word and one at its inverse; since no word is its own inverse, a fixed signed vertex receives at most one contribution per block occurrence. This proves the bound three even when blocks repeat. Scalar Chernoff on contributions divided by three gives exponent epsilon^2 delta/9 after the standard upper-tail simplification and union bound.

The prefactor M grows exponentially in ell, but its logarithm is O(ell), whereas delta grows at least as a positive constant times lambda^((d-1/3)ell-O(1)). Both failure bounds therefore tend to zero. The density restriction is used exactly here, with fixed d > 1/3.

Finally, the comparison of expected and actual degree normalizations is legitimate. On the codimension-one space f^T barD1 = 0, the Laplacian energy has the stated lower bound and the actual D-norm has the stated upper bound. Any extra kernel direction would intersect this subspace, contradicting the lower bound; hence the actual graph is connected and has positive degrees. The generalized Courant--Fischer formula maximizes over all codimension-one subspaces. It does not require the chosen subspace to be D-orthogonal to constants. Therefore the resulting gap bound (1-epsilon)gamma/(1+epsilon) is valid. The displayed epsilon restriction makes it strictly greater than 1/2.

**Verdict:** valid matrix concentration, valid handling of within-relator dependence, and valid transfer to the actual normalized gap. No adjacency-matrix concentration or independent-degree assumption is being silently used.

## 8. Property-(T) criterion and transfer

I inspected Kotowski--Kotowski, arXiv:1106.2242v2, pages 6-7, especially Definition 2.12 and Theorem 2.13. Their link allows multiple edges, assumes cyclically reduced relators to exclude loops, and its normalized spectral gap threshold is strictly greater than 1/2. The candidate's link convention is conjugated to theirs by global inversion of all signed vertices, preserving spectrum and connectivity.

Retaining repeated sampled relators as repeated relation occurrences is legitimate: a presentation can be treated as an indexed family of attaching triangular cells, including redundant cells. The multigraph spectral criterion counts the corresponding incidences. Removing duplicates would change the link, so the candidate correctly keeps them throughout its probabilistic construction. The underlying presented group is unchanged by those repetitions.

The hypotheses of the criterion hold on the event established in Section 6 of the proof. Thus the triangular group has property (T). The property passes to its quotient image subgroup and from a finite-index subgroup to the ambient group, as also recorded in Kotowski--Kotowski Remarks 2.10-2.11. No properness, factor hyperbolicity, factor finite presentation, or injectivity of the block map is needed for these transfers.

Primary dependencies: [Kotowski--Kotowski](https://arxiv.org/abs/1106.2242v2), [Tropp](https://arxiv.org/abs/1004.4389v7).

## 9. Artifact, source, and finite-diagnostic verification

I independently verified the archive hash and size, exact member list, all 12 member byte counts and SHA256 hashes, and byte equality of the archived members with the frozen working copies. The archive contains authored mathematics, authored diagnostic code/results, and verification metadata. It contains no copied primary PDFs, extracted primary-source text, raw corpus records, or private coordination files.

I independently fetched all six primary PDFs again from the exact public retrieval URLs in the source manifest. Every fresh download returned HTTP 200 and matched the author's full byte count and SHA256 hash. I inspected the essential source passages, including the displayed model and open question, the spectral theorem, and Tropp Corollary 5.2 / Remark 5.3. The companion retrieval receipt records the six matches without redistributing source files.

I independently hashed all bytes of the three supplied corpus files, parsed their full contents, selected the unique exact-ID records, and recomputed the canonical full problem/report pair with sorted keys and default JSON separators. The result is 3,767 bytes, SHA256 f49c17584ada1a931294e4222414fc5b57ee1d60afca82d6818029457badf17f. It matches both the author manifest and the catalog review hash; the complete report record is empty. This is verification of the supplied corpus, not a claim of a freshly downloaded corpus or of access to the blocked target webpage.

The author's mathematical and provenance checkers were rerun in both normal and optimized Python. Positive outputs were required to match the recorded bytes. The eight mathematical and four provenance mutation runs were required to reject for their specific documented reason, not merely return a nonzero exit code. This distinction matters because a generic checker failure would not establish that the intended mutation had been detected.

I also wrote an independent per-vertex expected-kernel diagnostic, without importing the author's checker. It exhaustively checks 13 small spaces across all three residues, including multiple self-inverse letters in one part, nontrivial inverse pairs, and unequal part sizes. Its two Python modes produce identical passing results. This is complementary to the author's endpoint-aggregated diagnostic, and remains only finite evidence. Neither test suite proves Perron asymptotics, concentration, finite-index transfer in general, or property (T); those claims were reviewed analytically above.

## 10. Literature and remaining limits

The inspected 2022 Ashcroft result concerns random elements from word-metric annuli in a non-elementary hyperbolic group. It cannot simply be substituted for the present fixed syllable-alphabet model with arbitrary factor groups. The September 2026 Oppenheim preprint concerns the Gromov model and a density above 1/4 along lengths divisible by four. It is not a dependency and does not directly settle this exact free-product model. The candidate correctly distinguishes both sources.

I found no contrary prior result in the inspected primary material or targeted public searches. That is not exhaustive novelty verification. The live unsolvedmath target page was not independently verified in this audit; identification rests on the complete exact-ID corpus record and the primary OWR passage. Acceptance here establishes that the pinned argument, using its explicitly cited standard theorems, answers the scoped mathematical question. It does not authorize a claim of human certification or publication in a refereed journal.

Additional inspected primary sources: [Ashcroft](https://arxiv.org/abs/2202.12318v2), [Oppenheim](https://arxiv.org/abs/2609.21255v1).

## Final acceptance statement

For fixed n >= 3 nontrivial finitely generated factors, fixed finite inverse-closed generating alphabets, and fixed d in (1/3,1), the candidate establishes that the random quotient in the specified with-replacement free-product density model has property (T) with probability tending to one along all integer relator lengths. The proof pin stated at the beginning is accepted unchanged by this audit. No repository write or queue change was performed as part of this review.
