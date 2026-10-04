# Independent audit of the interval exchange recurrence packet

Problem 30001211 / OWR-3396-010, rank 613. Audit date: 2026-10-04 UTC.

## Verdict

**PASS as an explicitly unsolved partial investigation, with nonblocking precision notes.** No fatal gap was found in the stated conditional theorems or the Borel construction. This audit does not approve a complete positive or negative answer to the finite minimal IET question, a novelty claim, or a claim that the current literature has been exhaustively checked.

The exact reviewed author manifest has SHA-256

`96e071e004aef40ae132a5ec27c8c8aaacf55b5fd52202ef1da25999771db544`.

Its nine listed files all match their declared byte counts and SHA-256 digests. The author packet was not edited. All 105,120 author assertions replayed with byte-for-byte identical JSON. A separate implementation supplies 175,860 new finite assertions, including 11,575 interval cylinders. Neither count is a proof of an asymptotic or universal assertion.

The original existential all-pairs problem remains unresolved **by this work**. The arXiv status inconsistency remains unresolved as a literature matter. The published full text was not obtained and must not be represented as having been checked.

## Scope and method

The review independently checked all mathematical arguments in RESULT.md, the bounded verification program and its actual output, the target quantifiers and metric conventions, and the cited external input needed by the three-interval obstruction. Source PDFs and page images were read privately; no source PDF, screenshot, full corpus, or substantial source transcription is part of this audit package. The audit made no remote write or external communication on the project's behalf.

The five ledger entries describe five materially different mechanisms. They consistently record five used approaches and no complete candidate. This verifies consistency of the frozen ledger, not the authenticity of an otherwise unavailable turn-by-turn transcript. Likewise, the prior repository absence and duplicate checks are author provenance records; this mathematical audit does not independently certify live GitHub state.

The proof assessment below is analytic. Finite tests are used to detect implementation, constant, indexing, endpoint, and hypothesis errors.

## Target and primary source verification

The target is

`exists a finite minimal IET T, for every x,y in [0,1), liminf(n |T^n(x)-y|)=0`.

Equivalently, after choosing T, x, y, epsilon > 0 and N, some n >= N satisfies the indicated bound. The index may depend on all these choices. A bad rotation or a family of excluded IETs is not a negation of this existential statement. An almost-everywhere theorem is not an all-pairs theorem.

The [OWR report](https://ems.press/content/serial-article-files/46214?nt=1), printed pp.747-748, was independently read in text and visually on both pages. Page 747 defines the distance to the nearest integer; p.748 Question 2 asks whether a minimal IET can have vanishing critical connectivity for every pair and records the exclusion of exchanges of at most three intervals. The proposed transformation is existentially quantified. This is connectivity, with recurrence only its diagonal restriction.

The pinned catalogue record uses ordinary absolute value. The [arXiv version](https://arxiv.org/abs/0910.5422v2), Section 13 Problem 3, printed p.21, also displays the Euclidean formula and the all-pairs quantifier. Although it does not repeat minimality there, an all-target zero gauge would itself imply every forward orbit is dense. The supplied PDF identifies itself as v2 dated 11 April 2011, while its running typesetting header says 19 November 2018. The packet correctly records this discrepancy without pretending that it is a new publication date.

For each fixed interior y, the Euclidean and circle critical liminfs agree, including infinite values. Set r=min(y,1-y)>0. Circle distances smaller than r cannot be produced by crossing the cut at 0, so then the two distances agree. Any subsequence realizing a finite critical circle liminf has unscaled circle distance tending to zero and eventually enters this region. In the infinite case use circle distance <= Euclidean distance. This proves the stated comparison for arbitrary sequences, not only IET orbits.

The boundary restriction is real: z_n=1-1/n^2, n>=2, has n times circle distance to 0 equal to 1/n, while n|z_n| tends to infinity. Therefore the packet is correct not to assert blanket equivalence at y=0. Every IET exclusion actually proved in the packet can be witnessed at an interior target and hence obstructs both formulations.

### Status conflict

The arXiv paper's Section 2.1 defines measurable maps to be Borel maps and allows an empty set P(T) of invariant Borel probability measures. Section 4.2, printed p.9, announces exclusion of all 1-collapsing measurable maps for which P(T) is nonempty, while asking about the existence of measurable collapsing maps. Section 13, p.21, nevertheless lists the IET case as an open problem. Since an IET preserves Lebesgue probability, the announcement and the open IET status cannot both provide a coherent resolution certificate as printed.

The announcement has no accompanying proof establishing that general exclusion in the inspected text. It is not an admissible theorem dependency for this packet. The ordinary definition of measurable map does not secretly require injectivity; the separate Borel construction therefore is legitimately relevant to the broader printed question, but its historical novelty is not established.

The stored response from the [publisher](https://link.springer.com/article/10.1007/s00222-012-0413-4) is an HTML landing page with bibliographic information and access prompts, not the final full text. The metadata gives Inventiones mathematicae 192 (2013), 375-412. Fresh web requests did not recover the published article. No conclusion is drawn about whether the conflicting arXiv passages survived publication or whether a later source settled the target. A bounded search returned no verified resolution; that negative search result is not a completeness certificate.

The three privately inspected PDFs match the source hashes in SOURCES.json:

- OWR: `cf7057c80890e200147778ce762d981d7ca2cfe7c97b0b28b83dcda01f1ad764`
- Boshernitzan-Chaika arXiv: `2d9ec3d1deca1375c6ecba8ad17ad1d3cb4d41a2ef9015ac8d075726dcbf3d24`
- Bugeaud-Harrap-Kristensen-Velani: `37b6a301db776509a0d39c2297862b484486968eed217dcc78aad1e318543e04`

## Claim by claim mathematical assessment

### Theorem 1 and the degree barrier

**Accepted under absence of periodic points.** A length-n itinerary gives delta=sum h_i in the fixed field even when the starting x is not in that field. Thus the argument does not require algebraic initial points. Clearing the translation denominators puts D delta in Z[sqrt(d)]. Nonzero displacement and the injectivity of the field embeddings imply that its norm is a nonzero integer. The lower bound is exactly

`|delta sigma(delta)| >= D^(-2)`.

Since |sigma(delta)| <= nH, this gives n|delta| >= 1/(D^2 H). The factor D^2 is necessary; integrality of D delta does not yield D rather than D^2 here. H>0 follows from absence of the identity map.

For the circle version, -1<delta<1 and delta!=0 ensure delta-m!=0 for a nearest integer m in {-1,0,1}. Subtracting m preserves integrality after multiplying by D and adds at most 1 to the conjugate bound. Therefore

`n ||delta|| >= n/[D^2(nH+1)] >= 1/[D^2(H+1)]`.

All constants and inequality directions are correct. Choosing an interior x and y=x supplies a bad pair. The minimality claim for the illustrative irrational rotation is analytic, not inferred from a sampled orbit.

For a field of degree q, the norm has q embeddings, with complex embeddings counted individually. The product bound gives the stated factor D^(-q) and exponent q-1. Positive upper bounds on the conjugates remove zero-bound notation issues. For q>2 this does not imply a positive critical n-scale bound. No unrestricted conclusion is justified.

Dependencies: finite translation partition, a common real quadratic field, common denominator D, no periodic points, and the elementary algebraic norm fact. No unverified literature assertion enters this proof.

### Lemma 2 and Corollary 3

**Accepted.** From q_k<=Hk and T^k x=S^(q_k)x one obtains

`k d(T^k x,y) >= (1/H) q_k d(S^(q_k)x,y)`.

Restricting a liminf to an increasing subsequence cannot lower it. For infinite c apply arbitrary finite eventual lower bounds. A section rescaling of length L divides distances, and hence the gauge, by L. There is no lost reciprocal clock or length factor.

The sole non-elementary input is Corollary 1 of [Bugeaud-Harrap-Kristensen-Velani](https://irma.math.unistra.fr/~bugeaud/travaux/BHKV.pdf), equation (5) on p.2 and Corollary 1 on p.3. These were independently checked: for every real alpha the set of targets satisfying a uniform positive lower bound on q||q alpha-b|| has Hausdorff dimension one. Only nonemptiness for irrational alpha is used. The packet does not need to reprove that external theorem.

The set defined with **positive liminf** is invariant under b -> b+k alpha: substitute n-k for n and use n/(n-k)->1 after discarding finitely many indices. It is important that the packet uses liminf for this invariance; a bound over every n could be spoiled by a finite exact hit. Irrational orbit density then moves a bad target into any desired open section interior, after translating by the chosen initial point x.

An irrational rotation hits the interior of a nondegenerate interval within uniformly bounded time. The inverse images of that interior under positive iterates cover the compact circle, so a finite subcover supplies the uniform bound. Applying this at every return bounds the k-th return time by Hk, including initial points at section boundaries.

The three-interval reduction is also correct. The reducible permutations preserve a proper initial interval. Of the remaining three permutations, the two cyclic orders reduce to rotations by merging equal-translation neighbors. For the reversal, put C=1+b=a+2b+c and theta=b+c. On the first piece, x+theta lies in [b+c,1). On the middle piece it lies in [1,C), and the second iterate equals x+c-a in [c,c+b). On the third piece the first iterate wraps once and equals x-a-b in [0,c). Thus the first-return times are exactly 1,2,1, including the left endpoints. Rational theta/C would make the ambient rotation periodic and its first return periodic; minimality therefore forces irrationality.

Consequently every minimal IET on at most three intervals has an interior bad pair. This is a recovery of a known exclusion. It does not identify an inducing rotation for a general higher-genus IET.

Dependencies: the cited BHKV nonemptiness theorem, irrational-rotation minimality, compactness, the exact permutation classification, and Lemma 2. The upper return-clock bound is essential, as the new countercontrol below demonstrates.

### Lemma 4 and the local potential criterion

**Accepted.** The integrability hypothesis excludes an atom at y. For each a>0 and t=|z-y|>0, the number of positive integers satisfying n<a/t is at most a/t. Tonelli therefore bounds the sum of the target-ball measures by a P_mu(y). Invariance is then needed to identify these measures with the measures of the orbit-hit events. The first Borel-Cantelli lemma requires no independence. A countable intersection over positive integers a gives n|S^n x-y| -> infinity almost surely.

The annulus estimate is valid: on the j-th dyadic annulus the reciprocal distance is at most 2^(j+1), and the mass is at most C 2^(-j(1+eta)). The resulting series converges. The complement of a sufficiently small ball contributes a bounded integrand.

The necessary infinite-potential condition for every invariant probability and every target is valid for the packet's Euclidean all-pairs problem. For a circle obstruction the direct inference is made at interior targets, as explicitly stated. Lebesgue potential diverges at both interior points and the endpoint; Lebesgue preservation alone supplies no finite-potential target. The proof does not claim existence of the required measure or target for an arbitrary remaining IET.

Dependencies: Borel measurability, an actual invariant Borel probability, finite reciprocal potential, Tonelli and first Borel-Cantelli. Finite potential without invariance is not enough.

### Lemma 5 and compact avoidance sets

**Accepted.** Including 0 in D covers the leftmost continuity cylinder. The full preimage cuts at depths 0 through n-1 refine a partition on which T^n is a translation. Extra cuts are harmless. On a half-open cylinder with left endpoint u, the translation formula holds at u itself because the convention is right-continuous and all branches preserve orientation. Consequently the displacement at any x in that cylinder is T^n u-u.

Writing u=T^(-j)d, 0<=j<n, places u and T^n u=T^(n-j)d in the two-sided set E_n. Minimality excludes their equality. Therefore their Euclidean distance is at least the minimum separation of **distinct** elements of E_n. The use of two-sided endpoint orbits, the inclusion of 0, the absence of periodic points and the half-open convention are genuine dependencies, not cosmetic details.

The asserted lower bound and the conditional positive-diagonal consequence follow. The necessary condition inf_n n e_n=0 for a hypothetical collapsing IET is correct. It is not sufficient and is not proved to fail for every IET.

For the compact survivor formulation, every constraint is closed in the fixed compact interval [a,b]. The finite-intersection property is therefore equivalent to nonemptiness of the full intersection; one can equivalently use the nested finite prefixes. Minimality alone is not supplied as a proof of the finite-intersection property. The packet correctly leaves this as the missing step rather than silently applying compactness to possibly empty sets.

### Lemma 6 and Proposition 7

**Accepted.** If the finitely many balls cover an interval of length L, subadditivity of length gives L<=2 epsilon sum_(n=N)^M 1/n. For N>=2, monotonicity of 1/t gives the stated integral upper bound log(M/(N-1)), hence the exponential lower bound on M. Open covers of a compact target interval have finite subcovers, but no useful upper bound on their last index follows. Arbitrarily large covering horizons are compatible with the question's quantifiers.

The rational sequence construction is well-defined. At each finite step a and ell are rational; the candidate points are distinct as m varies and lie strictly within the prescribed middle-third interval. Finitely many forbidden earlier centers cannot exhaust them. If a stage never ended, all its widths would have been 1/(kn), whose tail sum diverges, contradicting a<1 throughout. Thus each stage is finite and reaches 1 exactly.

Every target, including both endpoints of [0,1] and every shared bin boundary, lies in a bin whose center is within 2ell/3. The global indexing then gives n|z_n-y|<=2/(3k). The witnessing indices lie in successive disjoint finite stages and tend to infinity. This proves the universal all-target zero liminf analytically. The finitely computed stages are not a substitute for the harmonic-divergence argument.

Dependencies: harmonic divergence, exact rational construction, finite exclusion of used values and the middle-third location. No property of IET orbits is proved by constructing this arbitrary sequence.

### The Borel map

**Accepted as a map outside the target class.** The distinctness of z_j makes the successor assignment a function on Z. Every subset of the countable Z is Borel; F^(-1)(B) is such a subset, with I\Z added exactly when z_1 is in B. This establishes Borel measurability for every Borel B.

Outside Z the forward orbit at time n is z_n; from z_j it is z_(j+n). A finite forward index shift preserves zero critical liminf by multiplying the sequence bounds by n/(n+j), tending to one. The resulting all-target approximation implies that every forward orbit is dense. The construction is stronger than merely giving one dense orbit.

If a Borel probability were invariant, F^(-1)(Z)=I would force mu(Z)=1. The preimage of {z_1} is I\Z, so its mass is zero. The singleton-preimage recursion then makes every {z_j} have mass zero, contradicting countable additivity. Thus no invariant Borel probability exists. Independently, the uncountably many points outside Z all map to z_1, so F is not injective and cannot be a finite IET. In particular it cannot preserve Lebesgue probability.

This construction invalidates any attempted exclusion based only on Borel measurability and dense forward orbits. It does not refute an exclusion hypothesis which includes invariant probability, does not realize a finite IET, and is not a resolution of the audited problem.

## Reproducibility and adversarial controls

The original command was executed against the frozen script, with output saved separately as audit/replay.json. Its JSON is byte-for-byte identical to public/verification/result.json, SHA-256 `dbcdc07b361bcd52cc53b5a64dbf4b066bcba24d779c36fe707eaf4fdc30d492`. The original 105,120 count is correct: 6 parameter checks, 102 inverse checks, 204 inducing checks, 102,000 orbit/norm checks, 1,872 endpoint-cylinder checks, 9 finite potential checks, 924 sweep checks and 3 negative controls.

The audit's independent discriminating_checks.py does not import the author's program. It uses rational square-root enclosures from integer square roots for quadratic ordering, rather than the author's rational-square sign formula. Its final output records 175,860 successful finite assertions:

- 46,080 norm and circle-bound checks over five squarefree quadratic fields, three denominators, 12 initial points and 64 iterates per fixture, including rotation discontinuity points
- 125,783 cylinder and two-sided inverse checks over all permutations of three rational four- or five-piece length fixtures, depths 1 through 7, covering 11,575 cylinders and testing each cylinder's left endpoint and two interior points
- 2,160 reversal first-return and exact-clock checks over all 120 positive length triples summing to 17, at left endpoints and two interior points of every piece
- 254 metric-boundary checks, 127 unbounded-clock checks, 127 missing-invariance checks, 9 in-domain potential sums and 16 strict-count checks
- 696 covering checks and 585 index-shift checks using independently chosen rational centers through three complete stages, plus integrity and mutation checks

The rational IET fixtures are generally periodic and are explicitly not claimed minimal. When testing Lemma 5's local displacement conclusion, its nonzero-displacement hypothesis is checked; zero displacements supply a control showing that the hypothesis cannot simply be removed.

The new discriminating witnesses include these exact mechanisms:

1. Dropping aperiodicity fails for the identity, whose endpoint gap is positive but displacement is zero.
2. Using only original endpoints fails for lengths (3,5,7,8)/23 and order (0,1,3,2): a second-iterate displacement is 1/23, smaller than the original endpoint gap 3/23. This is a finite algebraic stress test, not a minimal counterexample.
3. Boundary metric equivalence fails for z_n=1-1/n^2 and y=0, as established above.
4. The clock bound cannot be dropped. On the metric subspace {0,2} union {1/m:m>=1}, let S(2)=1, S(1/m)=1/(m+1), S(0)=0, and choose the return section {0,2} union {1/k^2:k>=1}. From x=2 to y=0 the ambient critical product is identically 1, whereas q_k=k^2 and the induced critical product is 1/k. This is an exact counterexample to the unbounded-clock variant of Lemma 2.
5. Invariance cannot be dropped from Lemma 4. For S(z)=z/2, mu=delta_(1/2) and y=0, the potential equals 2, but the orbit product n/2^(n+1) tends to zero. This mu is not invariant.
6. Repetition of a center with different successor values would make the successor prescription ambiguous. The actual construction excludes repetitions and avoids this failure.

The covering stages end at global indices 1, 11 and 231 in both implementations; the centers differ. The independent tests verify strict open-ball coverage with radius 1/(kn), so shared bin endpoints and y=0,1 do not slip through a closed-versus-open convention.

An initial audit test run did not detect the original-endpoint mutation because its first two rational length fixtures included a unit grid cell, forcing their original gap down to the grid spacing. Adding the third, coarser-endpoint fixture produced the explicit mutation witness above. This was a weakness in that audit fixture, not a failure of the author packet. The final retained script and output include the discriminating fixture.

## Precision notes and release limitations

1. **Clarify the meaning of aperiodic.** Theorem 1 uses the pointwise statement T^n x!=x for every x and every n>=1. It should be read as absence of periodic points, not merely measure-theoretic aperiodicity. Minimality, which is the actual application, supplies the stronger condition. This is a wording clarification, not a defect in the IET obstruction.
2. **Finite potential fixture has an out-of-domain atom.** The author's finite probability fixture puts mass at 1 although I=[0,1). Its tested Tonelli inequality is valid on the real line, so the nine assertions remain correct and no proof is invalidated. It should not be described as an invariant probability example on the stated half-open I. The independent audit replaces that atom by 7/8. Neither fixture includes dynamics, and neither tests the full invariant-measure theorem.
3. **Keep the source-status caveat.** No already-solved label, no assertion of present-day global openness, and no assertion about the final published article follows from the inspected evidence. The safe claim is that this investigation has not solved the target and that its bounded literature check did not verify a resolution.
4. **Do not upgrade finite evidence.** Original tests use one quadratic 3-IET; the added tests broaden algebraic and endpoint coverage but still prove neither minimality from data nor any unbounded-time universal statement. The analytic proofs are the basis for the accepted partial results.
5. **Keep the frozen/public distinction.** The frozen packet accurately says independent review was pending at its freeze. This separate audit now supplies the review outcome for exactly that manifest. If a revised release changes any original file, retain the original binding and identify the new release hash; do not pretend this audit reviewed unrecorded edits.

No mathematical correction to a stated theorem is required. The two minor clarifications above can be recorded as an audit addendum without altering the frozen originals.

## Remaining gap and publication recommendation

A positive answer still needs a single finite minimal IET with zero critical connectivity for every ordered pair, including exceptional initial points and the boundary target. A negative answer still needs a bad pair for every minimal finite IET, with endpoint-aware metric handling. The packet covers quadratic translations, bounded induced rotations, a specified endpoint-separation condition and a specified invariant-potential condition. None is shown to exhaust arbitrary higher-interval IETs. The Borel construction violates both bijectivity and invariant-probability existence and cannot fill that gap.

It is reasonable to release this as an AI-assisted, unrefereed, independently audited **partial investigation with five unsuccessful approaches**. It is not reasonable to label it a solution, a proof that the target is currently open, a priority result, or a fully reconciled literature survey. Human expert review remains valuable before any theorem is promoted beyond this explicit partial scope.
