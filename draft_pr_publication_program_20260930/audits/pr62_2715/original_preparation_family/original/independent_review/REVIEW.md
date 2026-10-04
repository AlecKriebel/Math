# Independent review: 2715 / KP 1.56

**Verdict: PASS_SCOPED_OBSTRUCTION_AND_KNOWN_CASE.** No required mathematical correction was found. The artifact correctly preserves the unresolved general endpoint-isotopy question. Its positive knot-theoretic conclusions are credited consequences of existing theorems.

Reviewed 2026-09-30 by a separate adversarial AI reviewer (gpt-6-astra, xhigh). This is not human peer review.

Frozen OBSTRUCTION.md SHA-256:
d6fa375ecd946908b8426140ba74e30aeb11d175ad750c3ba2d1462d4567856b

Author verifier: 51eb5213c04602630e62bd677cb67594d4bb9295ee609e1892687b966a04ab58  
Author receipt: d3bb6070256ff2db6f7fb2dbf668c0b9309e1dbdaae95349fc1ff462980a73f9

## 1. Original question and direction

The full K3 passage at printed pp. 55–56 was checked, including rendered p. 55. Problem 1.56 concerns endpoint knots with isomorphic hat knot Floer homology and a ribbon concordance between them. It is separate from the neighboring question about fibering a particular concordance.

The operational convention \(J\le K\), with births and saddles but no maxima from J to K, matches the direction of the injection in [Zemke's published article](https://annals.math.princeton.edu/wp-content/uploads/annals-v190-n3-p05-s.pdf). [Boninger's paper](https://msp.org/pjm/2025/335-1/pjm-v335-n1-p04-p.pdf) uses the opposite verbal from/to description but the same inequality convention. I independently downloaded Boninger's PDF; its hash matches the author's source. No direction reversal contaminates the application of Gordon's lemma.

## 2. Split injectivity and equal ranks

Zemke's Theorems 1.1–1.2 and §3 establish a bigrading-preserving injection, with left inverse induced by the reversed decorated concordance. At equal finite total dimension the injection is an isomorphism. More precisely, every bidegree has a nonnegative dimension deficit, and their finite sum is zero, so every deficit vanishes.

Consequently the strict-total-rank-increase formulation is exactly equivalent to the original endpoint-isotopy question under the ribbon hypothesis. Equality of ungraded ranks without the degree-zero injection would not justify this conclusion.

If \(GF=I\) and the spaces have equal finite dimension, \(G=F^{-1}\). This proves only an algebraic inverse. The reversed movie exchanges births and maxima; it is not automatically ribbon. Agol's antisymmetry theorem needs ribbon comparability in both directions.

The warning attributed to Zemke is explicit in §3: the composite concordance need not be isotopic to the product although its map is the identity. The two-object poset functor is a valid logical diagnostic, not a knot realization or a counterexample.

## 3. Credited residual-nilpotence case

Boninger's printed p. 88 was checked in text and visually. Residual nilpotence is required of the **commutator subgroup** of the successor's knot group. Lemma 4.1, citing Gordon's Lemma 3.4, has precisely the hypotheses and conclusion used: \(J\le K\), that property for K, and equal Alexander degree imply isotopic endpoints.

The normalized graded Euler characteristic of HFK gives the Alexander polynomial. Therefore equality of bigraded HFK implies equality of Alexander degree, and the credited deduction is valid. Laurent span is consistent with the relevant polynomial normalization.

For a fibered knot, the infinite cyclic cover is the fiber times the line, and its fundamental group is the knot group's commutator subgroup. The fiber has free fundamental group, which is residually nilpotent. Standard HFK fiberedness detection transfers fiberedness across equal bigraded HFK. Hence a counterexample must have both endpoints nonfibered and the successor outside the stated residual-nilpotence class.

The full Gordon1981 proof was not recovered; the exact published-restatement qualification must remain. This review checks the application of that imported theorem, not its entire group-theoretic proof. Boninger's Mayland–Murasugi statement also retains the pseudoalternating and prime-power-leading-coefficient restrictions.

## 4. Band-twist exclusion and corrected Khovanov source

Wang's full [arXiv2006.01070v1](https://arxiv.org/abs/2006.01070v1), Theorems 1.3 and 1.8, gives the specified equal-HFK family and its Khovanov decomposition. The band must be nontrivial and join a split two-component link. The formula holds for all integer full-twist parameters.

The decomposition has one fixed summand and a nonzero finite-support summand shifted by \((2n,4n)\). All total dimensions agree. An isomorphism for distinct parameters would, after pointwise cancellation of the fixed dimension function, make a finite nonempty subset of \(\mathbb Z^2\) invariant under a nonzero translation. Maximizing its dot product with the translation vector gives a contradiction.

I independently retrieved and read the complete corrected [Levine–Zemke arXiv1903.01546v2](https://arxiv.org/abs/1903.01546v2), dated July20,2021. Theorem1 gives a grading-preserving split injection. Its short proof uses dotted-cobordism neck-cutting relations for the composite map. It holds over any coefficient ring; over \(\mathbb F_2\), signs are irrelevant. A ribbon concordance in either direction between Wang-family members would thus force a graded isomorphism by equality of total dimensions, contradicting the preceding paragraph.

The publisher flags a [2020 erratum](https://doi.org/10.1112/blms.12333). Its full notice was checked: it corrects copyright statements in a batch of articles, not this mathematical theorem. The current arXiv v2 separately advertises corrections to the earlier version and retains split injectivity. There is no mathematical blocker from that publisher notice.

Wang's journal-typeset edition was not independently recovered. The author's edition-numbering caveat is appropriate; the accessible full preprint provides exactly the implications used.

## 5. Recent scope and the conditional chain bound

The current arXiv records and relevant introductory statements for Baldwin–Hanselman–Sivek2602.21109, Hom–Park2608.06625 and Dunkerley2606.20802 were checked. Their stated scopes match the artifact: fibered-predecessor finiteness, fixed-companion cable rigidity, and particular ribbon-minimal examples. None of those stated theorems establishes arbitrary equal-HFK endpoint rigidity. This is not a full independent audit of all proofs in those preprints.

The total hat HFK dimension is odd because, modulo two, the alternating Euler sum at \(t=1\) equals the total dimension and the normalized Alexander polynomial evaluates to one. If the missing rigidity assertion held, strict downward ribbon steps would decrease this odd rank by at least two, yielding the claimed bound. Without it, a nonincreasing integer rank eventually becomes constant but the corresponding knots need not have been shown constant. The conditional status is correctly retained.

## 6. Exact diagnostics and publication recommendation

The author verifier was replayed in an isolated directory with its required sibling proof. The supplied receipt reproduced byte for byte: **564 assertions pass**. No author source or receipt was changed.

A separately written self-contained checker, importing no author code, passes **20,223 exact assertions**:
- nonnegative graded deficits and equality in every grading;
- rectangular split injections over \(\mathbb F_2\), their projectors, and inverses at equal dimensions;
- finite-support grading shifts, including collisions against a fixed summand, and failure of graded injections in both directions;
- the poset functor, Euler parity, conditional odd-rank drops and Morse-index reversal.

These are algebraic diagnostics, not new knot Floer computations, knot searches or evidence of a geometric counterexample.

Publish only as a scoped unresolved record with its credited known affirmative class. Keep **unsolved, one substantive attempt, no novelty claim**. Preserve the full-Gordon-text and recent-preprint proof-audit limitations. No mandatory mathematics change is required.

Optional source improvement: cite Levine–Zemke's corrected v2 directly and note the copyright-only erratum. This report already records both.
