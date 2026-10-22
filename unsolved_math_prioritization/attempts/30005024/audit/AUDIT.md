# Independent audit: finite-mean coding radius

Problem 30005024 / OWR-9790359-005 / rank 787. Audit date: 2026-10-05.

## Decision

**PASS for the scoped auxiliary results and the unresolved disposition. The general problem remains UNSOLVED after 5/5 substantive approaches.** This audit finds no mathematical correction required in the frozen research note. It does not certify a solution, novelty, formal verification, human peer review, or publication acceptance.

The central all-orders determinant argument is valid. Its consequence is exclusion of every **finite-state** hidden Markov representation of the two specified critical coloring laws. It does not exclude countably infinite hidden states, and does not prove an intrinsic infinite-mean coding obstruction. The author states these limits correctly.

An omitted provenance item is supplied: the independently reconstructed catalog review hash is `fb5ee42c259cebb1c28137995be1214779f6c5a20c8e56a417fe7429b3b463fc`. The original author files are preserved byte for byte under `author/`; this addendum does not replace or silently edit that freeze.

## 1. Identity, scope, and source checks

The author ZIP has 19,304 bytes and SHA-256 `0f5e6dfb82fa255889d917eba93535e1912785787276f5a3f63e85a9abddc144`. Its manifest has SHA-256 `6e85d6ff39d8c353145140f1122f00861c95ed200f0f35a5445a007dfda2c825`. All nine manifested payload files agree with the manifest.

All three complete input corpora were read and hashed independently, rather than trusting extracted target records. Their byte counts and SHA-256 values agree with the author metadata. Exactly one catalog entry and one problem entry match the target ID; the rank is 787. The 143-byte UTF-8 statement matches its catalog hash. The complete research dictionary has no exact problem-code entry, so the repository's documented review-hash rule uses the empty object for that component. Applying that rule to the complete selected problem record reproduces the hash above. `SOURCE_AUDIT.json` and `PROVENANCE_RESULTS.json` contain verification metadata only.

The [official Oberwolfach report](https://publications.mfo.de/bitstream/handle/mfo/3933/OWR_2022_08.pdf?isAllowed=y&sequence=4) was freshly retrieved; printed pages 447-449 were also visually inspected. The target question is on p.448. The report begins with countable state spaces but explicitly permits more general spaces for coding. It imposes no finite-alphabet or entropy restriction on the IID source. The author analyzes countable output with standard-Borel input and discloses that scope. That restriction must not be used to redefine or claim exhaustion of the broader question. The workshop/report year is 2022; [publisher metadata](https://ems.press/journals/owr/articles/9790359) gives publication on 11 March 2023.

The report's reference [9] indeed names a subcritical-Ising paper. The appropriate finite-dependence result and 8/r estimate were verified in [Spinka, Finitely dependent processes are finitary](https://arxiv.org/abs/1901.00123), including the countable-output assumption and Remark 3. The source's product-input convention additionally specifies finite-bit determination. The author does not incorrectly infer that every spatially finitary continuous-input representation has that property.

All ten PDF byte counts and hashes were confirmed by new downloads. The 2026 quantum paper was checked at abstract/metadata level only. Inspection scopes, versions, URLs and limitations are recorded in `SOURCE_AUDIT.json`. The bounded current search identified no resolution; that is not a worldwide nonexistence or priority claim.

## 2. Quantifier audit

The target is a property of a law: an example must rule out every admissible IID source and every integrable spatial-radius coding of that law. The following distinctions are correctly retained:

- One coding with infinite mean versus absence of all finite-mean codings.
- Almost-sure finite radius versus deterministic bounded radius versus integrable radius.
- Spatial radius versus number of random bits, source entropy, and coding volume.
- A finite hidden-state space versus a countably infinite one.
- Translation equivariance versus full isometry equivariance.
- Finite dependence of separated sigma-fields versus pairwise independence or conditional mixing.
- First radius moment versus second moment, or the dimension-dependent volume moment.

Coordinatewise generation of standard-Borel IID symbols from uniform IID inputs does not enlarge spatial radius. It need not preserve finite-bit determination for a given coding. For a countable IID alphabet, inverse-transform intervals determine each sampled symbol after finitely many bits almost surely; a finite input window therefore needs only finitely many bits, with no spatial enlargement. This restricted reduction still reaches only the countable-state conclusion of [Holroyd-Hutchcroft-Levy, Theorem 2](https://arxiv.org/abs/1706.09526).

## 3. Proof audit by approach

### Approach 1: tail integrability and inefficient representations

The tail-sum identity follows from monotone convergence. Grouping decreasing tails in dyadic blocks proves the dyadic criterion, and the last half of a tail sum proves that integrability implies r P(R>r) tends to zero. The example of a survival function comparable to 1/(r log r) correctly shows the converse fails. An upper bound of order 1/r alone gives no divergence conclusion.

For the delayed-bit construction, the map from output site i to the input bit coordinate (i+N_i,N_i) is injective after all selectors are fixed. Thus every finite output vector is conditionally a product of fair bits, with the same law for every selector realization. The output law is IID. For r<N_i, the selected bit lies outside the observed spatial window and remains an independent fair bit, proving essential non-determination; radius N_i suffices. The specified selector mass telescopes to P(N_i>r)=1/(r+2), hence infinite mean. The radius-zero alternative for the same output law is decisive. No all-codings obstruction follows.

### Approach 2: coloring lower bounds and closure operations

The atom-cylinder event has probability p^(2r+2). The two adjacent radius-r windows then have the same translated value. Conditional determinacy of both outputs would force equality, contrary to proper coloring. A union bound gives the stated factor 1/2. It is a summable lower bound and disappears for atomless sources; it cannot settle the target.

The radius of a fixed local transformation is bounded by its deterministic range plus the maximum of finitely many translated coding radii. Bounding that maximum by the sum proves the expectation bound without independence. Enlarging the dependency sets proves the stated finite-dependence range. The finite independent-product assertion is also valid.

[Finitary Coloring](https://arxiv.org/abs/1412.2725), Theorem 2(ii), concerns E[R^2], not E[R]. Its Corollary 25 excludes stationary finitely dependent 3-colorings in dimensions at least two altogether. Those higher-dimensional examples cannot supply a finitely dependent counterexample here. The summable inverse-tower bounds in dimension one also give no infinite-first-moment obstruction.

### Approach 3: all-orders Hankel determinants

The source cylinder formulas were checked against [Holroyd-Liggett, Section 3](https://arxiv.org/abs/1403.2448). For an alternating word of length n, an interior deletion destroys properness, while the two endpoint deletions give the shorter alternating word. With the length-one base case, this yields B(w_n)=2^(n-1).

For H4, row multiplication by 2(2i+s)! produces monic polynomial columns of degrees s-1,s-2,...,0 at x_i=2i. Column reversal contributes (-1)^(s(s-1)/2); the monic change of basis has determinant one. The Vandermonde is 2^(s(s-1)/2) times the product of r! for 1<=r<s. Undoing row scaling gives the author's formula.

For H3, factoring 2^(2i) from rows and 2^j from columns contributes exponent (3s^2+s)/2. The Vandermonde contributes a further s(s-1)/2, totaling 2s^2. The factorial shifts and sign are correct. Both determinant formulas are nonzero for every positive s.

Finite-state hidden Markov word probabilities factor through their finite hidden dimension, so a hidden model with m states has every word-Hankel minor of order m+1 equal to zero. The displayed minors therefore exclude all finite m. Infinite rank is compatible with countably many states. No step in this argument establishes the missing countable-state exclusion. The different alternating-extension ratios at lengths n and n+2 separately exclude finite-order Markov laws once those lengths exceed the proposed order.

The nowhere-dense positive-measure example is also sound as a warning about one representation: on its positive-measure one-set, no finite binary cylinder forces membership, because the complement contains an open subinterval in every such cylinder. It says nothing about an alternative bit-finitary coding of the resulting IID law.

### Approach 4: information and conditional-dependence barriers

For the finite blocks used in the note, finite dependence makes the left block independent of the far-right block. The chain rule bounds the remaining conditional mutual information by the entropy of the k-site boundary strip. The stated entropy bound and increasing-block passage are correct under the finite-entropy condition given.

A tail event is measurable outside each finite neighborhood and hence independent of every finite cylinder sigma-field. A monotone-class argument makes it independent of itself. This proves ordinary tail triviality, not every stronger conditional-tail assertion.

The residue classes modulo k+1 consist of jointly independent single-site variables. Holder's inequality over the (k+1)^d classes, followed by the independent bounded-variable exponential estimate, gives the constant stated. This is an additive-observable bound. The note does not replace it with concentration for arbitrary nonlinear local observables.

For X_i=U_i XOR U_(i+1), separated input pairs prove 1-dependence and radius at most one. Conditioning the 2m-site bridge on alternating observations leaves precisely two equally weighted alternating strings. The final boundary value changes the posterior of U_1, giving 5/9 and 4/9 exactly. Both conditioning events have positive probability for every m. The persistent 1/9 difference therefore disproves a uniform conditional-decoupling inference, while its bounded-radius representation prevents misuse as a coding obstruction.

The current [Chazottes-Gallo-Takahashi v2](https://arxiv.org/abs/2602.14618) requires a second coding-volume moment in Theorem 3.1; Theorem 3.3 uses a first moment with the additional short-range factorization condition of Definition 3.2. Neither gives the universal first-radius-moment implication that a new obstruction would require.

### Approach 5: synchronizing finite-state construction

Primitivity supplies a common length L with a path from every state to a fixed terminal state. Let S_t be the states that can reach that terminal in exactly t steps. At update t, choosing an edge into the next predecessor set for states currently in the appropriate set constructs supported maps whose composition is constant. Values outside the set can be filled with any supported outgoing edge. Independent rowwise random maps assign positive probability to this exact word.

Independent disjoint L-blocks supply the geometric failure bound. The coding itself uses all update times and the most recent successful block; it introduces no global grid phase. Coalescence makes the past-start limit consistent, stationary and translation equivariant. Each current random map is independent of the resulting past, so the desired transition kernel is obtained. This is a correct coupling-from-the-past construction with exponential spatial tail.

For a stationary finitely dependent finite-state Markov chain, deleting zero-mass states leaves P^(k+1)(x,y)=pi(y)>0. This is primitive. Passing to overlapping block states for a finite-order finite-alphabet Markov law enlarges the finite-dependence range by a finite amount and justifies the corollary. No such finite-state reduction was proved for general finitely dependent laws.

## 4. Computation and independence of the audit

The author's manifest verifier and diagnostic program both passed unmodified. The author diagnostic result was then rebuilt without importing or executing its verification code:

- Subset-insertion dynamic programming checks the building counts used in every finite cylinder test; longer alternating words use their two-endpoint recurrence.
- Row-denominator clearing followed by integer Bareiss elimination independently checks the rational determinants.
- Weighted two-state transfers check the conditional bridge, rather than enumerating complete bit strings.
- The selector and synchronizing tests are reconstructed independently.

All **9,093 original cases** and their per-category counts match. A separate **3,787 additional exact checks** extend each determinant sequence through size 12 and test the synchronizing construction on all **139 primitive three-state directed supports**, for each terminal state. Counts include individual supported-choice tests and five comparisons with the recorded author result. These finite tests support arithmetic and transcription checks; the all-orders conclusions rest on the mathematical arguments above.

## 5. Prior attempts and publication boundaries

The pinned main snapshot `9df7afb24b53ca5b57727409e5d76fc8926711a7` contains 63 entries in its attempt directory and no target folder. Fresh all-state PR searches for the exact ID, exact problem number and finitely-dependent phrase returned no matches. These checks reproduce the author's bounded provenance, without purporting to exclude deleted, unindexed, differently named or inaccessible work. The catalog's desk review is not a proof attempt.

The five approaches are substantively distinct and all leave explicit gaps. This review is an audit of them, not a sixth research approach. The author freeze is retained unchanged. This package contains authored audit text/code/results and public verification metadata only, with no source PDFs, extracted text, screenshots, raw corpora or coordination files. No remote write was performed.

**Final status: UNSOLVED, 5/5.** Suitable description: a checked partial research record with a valid finite-state hidden-Markov obstruction, valid auxiliary barriers, and a constructive finite-order Markov subclass result. It must not be described as a general finite-mean counterexample or universal integrable-coding theorem.
