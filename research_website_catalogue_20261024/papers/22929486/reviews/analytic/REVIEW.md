# Independent analytic review: Zenodo 22929486

**Verdict: PASS within the stated mathematical scope.** No substantive defect was found in the published v1.0.1 proof or its finite certificates. The explicitly specified group of order 100,920 satisfies

\[
b_f(G)=b(G)=3<4=\mu'(G).
\]

This conclusion covers all permutation representations, including nonfaithful and intransitive actions, with bases understood for the permutation image. It gives the claimed counterexample to the question stated in Kourovka Notebook Problem 16.45. It does not establish smallest possible order, bibliographic priority, human expert acceptance, or a proof-assistant formalization.

Review completed 2026-10-25 UTC. Completion: 100% of the assigned analytic review. No manuscript, website, spreadsheet, Git, or Zenodo changes were made.

## Exact material and independence

Fresh primary acquisition obtained both files listed by the Zenodo v1.0.1 record, verified the record's MD5 checksums and the inventory expectations, and safely extracted all 166 source-package members. All 168 downloaded/extracted file hashes were rechecked unchanged at completion.

| Material | SHA-256 |
|---|---|
| Published nine-page PDF | `6225ed0ba605c1014c0e5e4954d97011f33eb8fa4c2b6243e4d071d5d82122df` |
| Published source/verification ZIP | `16495c3c54db97c6cbba4a1688a876e400902f90cfd3034debff7187316aaf11` |
| Current proof.tex | `2c74f1291c165dbefe72ebddda0b0a47784b8202811b162cc4496d59acd04af4` |

The source-package PDF is byte-identical to the separately published PDF. A fresh Tectonic compilation of the current source produced exactly the same extracted text across all nine pages. The rebuilt binary hash differs, as expected for independently generated PDF metadata. Page 5's small matrix and formulas were also inspected in a rendered image.

**Independence qualification:** the full proof reconstruction and initial fresh 50-check program were completed before opening any supplied verifier code or historical review conclusions. Later, while reading the README for reproduction instructions, its “Audit outcome and correction” section exposed favorable historical review summaries and an old, already corrected product-order typo. Root was notified immediately. No historical review report bodies or current sibling opinions were read. The completed review therefore is **not wholly blind**. `independence_disclosure.json` records this qualification; the original pre-exposure control source and results are retained with matching hashes. The final verdict rests on the current proof and fresh calculations, not the historical statements.

## Coverage

Read all nine actual published PDF pages, the full current TeX proof, the exact group specification, both principal verifier implementations, their certificate-comparison program, and all three additional mathematical audit scripts explicitly documented for reproduction. Reconstructed every numbered result, the normality obstruction, and the characteristic-11 boundary example. Inspected current exact certificate structures and compared their full subgroup sets and affine-element hash to fresh results.

Historical referee narratives, previous manuscript revisions, exploratory MILP programs and small-group searches, original research logs, and package-upload utilities are not premises of the published mathematical argument. They were not used to validate it. No floating-point optimization result is used. This review does not assert that every archival exploratory calculation is correct.

## Exact question and primary-source checks

The current official notebook's Problem 16.45 asks whether the largest inclusion-minimal base size, maximized over permutation representations of a finite group, equals the largest independent-subset size. Its alternative formulation asks whether a maximum-rank Boolean meet-semilattice embedding can have normal bottom. The manuscript answers precisely this question, rather than the different problems of smallest base size, sequentially irredundant bases, transitive actions only, or independent generating sets of the entire group.

Primary material checked:

- [Official Kourovka Notebook, October 2026 PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf), Problem 16.45 and its semilattice reformulation. Only the statement through the proposer's name was extracted for review; any later solution/status note was excluded. SHA-256 `f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118`.
- [Cameron, 2014 preprint](https://arxiv.org/abs/1408.0968), §2 definitions and §3 Propositions 3.1–3.2 and Corollary 3.3, read directly. These explicitly allow nonfaithful actions and identify the normal-bottom condition. PDF SHA-256 `f65c1b2ac82e4c5a6813297d0f39fae49304f7bcbc3d180d9e3926a9307836c5`.
- [Cameron, 2024 published paper](https://msp.org/mt/2024/3-2/mt-v3-n2-p08-p.pdf), §6, particularly printed pp. 428–429: all representations, the three base parameters, and Proposition 2's semilattice characterization. PDF SHA-256 `c76ce4bd536172e75843d837d87829d5be21bda0da1e5847747a579e08e64335`.
- Cameron's own [2010 exposition](https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/) and [2014 exposition](https://cameroncounts.wordpress.com/2014/08/06/groups-lattices-and-bases/) corroborate the parameter conventions and the open question. The manuscript supplies the needed proofs itself.

The cited September notebook URL returned HTTP 404 during this review. The live official October replacement supplies the exact problem statement. The manuscript's retrospective claim about its bounded September literature search was not independently established; it is explicitly disclaimed as a priority guarantee and is not a mathematical premise. An initially guessed publisher PDF URL retrieved the wrong article; its title was checked, it was rejected, and the correct Cameron PDF was acquired. This acquisition mistake is preserved explicitly in `primary_acquisition.json` and has no bearing on the proof.

The spherical triangle presentation used to identify the complement can be bypassed completely: fresh exact simultaneous group generation constructs the displayed isomorphism with all determinant-one matrices over F5, and a quotient map onto all 60 even permutations on five letters with kernel {I,-I}. Thus no unverified classification or triangle-presentation citation is needed for the reviewed construction.

## Reconstruction of the proof

### 1. Action kernels and subgroup families (pp. 1–3)

For a finite group, any base in an infinite permutation domain has a finite subbase: choose a moved point for each nonidentity element of the finite image. Inclusion-minimality then makes the base finite. The trivial group and trivial action have empty minimal bases.

A minimal base gives an irredundant family of point stabilizers with intersection equal to the normal action kernel. Conversely, the disjoint union of left coset actions for subgroups L_i has kernel equal to the core of their intersection. If that intersection N is normal, the identity cosets therefore form a minimal base. For faithful actions N must equal 1. This proves both the subgroup formulation and b(X)=max over normal N of b_f(X/N).

An arbitrary meet-irredundant family yields independent elements x_i in every subgroup except L_i; conversely, the omission-generated subgroups of an independent set are meet-irredundant. The latter intersection need not be normal. Restriction to any one L_i preserves the other witnesses, giving t-1 ≤ μ′(L_i), or t-1 ≤ b_f(L_i) when the total intersection is trivial. No assumption that the subgroups are maximal or conjugate is introduced.

The Boolean embedding A ↦ intersection of L_i for i outside A preserves meets and top; each x_i distinguishes the required images. No join-preservation or identity-bottom assertion is smuggled in.

### 2. Complement H (pp. 3–4)

The two printed matrices generate 120 determinant-one matrices. The central involution is -I, and the explicit quotient is A5. The displayed identities A²=B³=(AB)^5=-I hold.

The proper-subgroup classification of A5 used here is elementary. An intransitive subgroup fixes a letter or preserves a 2+3 partition, placing it in A4 or S3. A proper transitive subgroup has order divisible by 5; orders 15 and 20 would have a normal Sylow 5-subgroup and are incompatible with its order-10 normalizer, while order 30 would produce a nontrivial index-two quotient despite generation by 3-cycles. The remaining cases lie in D10. Each of A4, S3, and D10 has maximum independent-subset size two. Removing one element of an independent set in A5 proves its size at most three; the natural five-point action gives the lower bound. The stated simplicity argument from conjugacy-class sizes is also valid and freshly checked.

In odd characteristic a determinant-one matrix squaring to I is diagonalizable with both eigenvalues equal, so -I is H's unique involution. Every even-order subgroup contains it; every odd-order subgroup embeds in A5 and has order 1, 3, or 5. If an independent family's images modulo the center are dependent, deletion leaves a subgroup not containing the center, hence of odd prime order or trivial, limiting that family to size two. Otherwise its size is at most μ′(A5)=3.

A trivial-intersection subgroup family in H must include an odd-order member. A nontrivial such member has prime order, and one other subgroup already cuts it to 1. Therefore b_f(H)≤2; subgroups of orders 3 and 5 give equality.

The three printed R_i generate H independently. Their omission groups have orders 8, 12, and 20 and common intersection {I,-I}. The associated pair-product orders are 4, 3, and 10, exactly as printed in v1.0.1. The intersection is normal in H, giving b(H)=μ′(H)=3 while b_f(H)=2.

### 3. All subgroups missing the translation group (p. 5)

For F_p ⋊ C with faithful scalar action and C a cyclic 2-group, a subgroup missing F_p embeds in C and has independence number at most one. A subgroup containing F_p projects onto a subgroup D of C. For nontrivial D, every generating set contains an element projecting to a generator because D has a unique maximal subgroup. The geometric sum shows this element has order |D|; any generator outside its complement combines with it to generate the subgroup. Thus the independence number is at most two. The trivial-projection case is cyclic of prime order. The cyclic-2-group hypothesis is used, not silently omitted.

For a line W in F29², the scalar action H_W→F29× has trivial kernel: any nontrivial determinant-one unipotent kernel element has order 29, impossible in H of order 120. Hence H_W is cyclic of order dividing gcd(120,28)=4, and H is irreducible.

For K≤G missing V, the intersection K∩V is either 1 or a line, since 29 is prime. In the first case K embeds in H and inherits b_f≤2. In the second case its projection lies in H_W; a Sylow 2-subgroup complements the line and acts faithfully, putting K under the preceding scalar lemma. Thus every such K has b_f(K)≤2. This is a universal argument, not a sample or subgroup-lattice cutoff.

### 4. Universal upper bounds (p. 6)

Any faithful meet-irredundant family in G has a member missing V; otherwise its intersection contains V. Restriction into that member gives t-1≤2, hence b_f(G)≤3.

For any nontrivial normal N, irreducibility makes N∩V either 1 or V. If it is 1, then [N,V]=1. Faithfulness of H's action gives C_G(V)=V, so N≤V and N=1, a contradiction. Consequently every nontrivial normal subgroup contains V. Every nonfaithful action therefore factors through H, where b(H)=3. This proves b(G)≤3 for all actions without equating faithful and arbitrary invariants in the complement.

For unrestricted meet-irredundant families, all members containing V descend irredundantly to H and give size at most three. Otherwise restriction into a member with K∩V=1 gives size at most four; a line intersection gives at most three. Therefore μ′(G)≤4, without a normality premise on the intersection.

### 5. Lower bounds, normality obstruction, boundary (pp. 6–8)

The translation e1 together with the three R_i is independent: the linear omissions are detected by projection to H, and the translation is outside the complement. Irreducibility makes this set generate G. Its omission orders are exactly 120, 6,728, 10,092, and 16,820.

The three order-58 subgroups printed on page 7 have pairwise intersections {1,(0,-I)}, {1,(2e1,-I)}, and {1,(-2e2,-I)}, with triple intersection 1. Their identity cosets form a faithful minimal base of size three in degree 5,220. This supplies the matching lower bound.

The four omission subgroups of the independent set intersect in the complement's central order-two subgroup. Translation conjugation sends its nonidentity element to (2e1,-I), outside that subgroup, so it is not normal in G. The four normal cores are 1,V⋊Z,V⋊Z,V⋊Z; taking cores destroys essentiality. No quotient by that nonnormal intersection appears in the proof.

The explicit characteristic-11 construction gives a faithful minimal four-family, with deletion intersections of orders 11,11,5,2. This verifies the warning against extending the argument without the 2-group line-stabilizer condition. As another fresh negative control, replacing the third order-58 subgroup's offset 2e1 by zero leaves a common involution and destroys faithfulness, exactly as expected.

## Reproduction and evidence

`initial_independent_control.py` and its results preserve the initial fresh program, written before supplied verifier source was opened. `independent_control.py` adds only canonical subgroup and affine-element exports. Its 50 named exact checks include:

- All 76 actual subgroups of H; all 1,215,450 proper four-subgroup families and all 67,525 triples.
- The explicit SL2(5) identification, A5 quotient, unique involution, normal subgroups, and elementary simplicity control.
- All 30 projective line stabilizers, including injectivity of their scalar actions.
- All 100,920 generated affine elements, every omission group, the nonnormal intersection, the faithful three-family, and two negative controls.

The supplied Python and C++ verifiers both passed. Their subgroup exports agree as actual matrix sets, independently of index order. All 76 also agree with my fresh reconstruction and the archived published certificate. The full affine-element hash in all three reconstructions is `2f4c3b8353a9a5cd7d2cbbeb8a0d48dd0e203f4371652fd25c5ca2936fff5efc`. Published and freshly generated summary data agree after removing elapsed time.

The three additional documented mathematical audit scripts were read and rerun from copies in the ignored build cache, without opening their historical reports. All passed. Their successful replay is corroboration, not the basis for claiming independent authorship of those scripts.

Default `make` initially failed because the system selected an unaccepted Xcode license; direct Command Line Tools compilation then needed an explicit existing SDK/header path. The successful replay used the existing compiler and MacOSX14.4 SDK with source code unchanged. No license was accepted or environment installed. Failed and successful command logs are retained. These are local environment issues, not mathematical or package-source defects.

## Strongest verified claim and exact remaining gap

The strongest verified claim is the full stated theorem, including b_f(G)=b(G)=3 and μ′(G)=4 for the precisely specified semidirect action over F29, and the explicit obstruction to replacing the four-family's nonnormal bottom by normal cores.

**Remaining mathematical gap found in the published theorem: none.** This is an independent analytic and exact-computation review with an explicit late historical-summary exposure, not an infallibility claim. Full G-subgroup enumeration is unnecessary and was not performed; the universal conclusions follow from the reconstructed structural proof. No claim about smallest order, uniqueness of the counterexample, historical priority, current community acceptance, or conjectural extensions is promoted.
