# Independent audit: RBM(4,3) obstruction

## Verdict: PASS

The frozen author packet correctly supports a negative answer to the recovered
fixed-architecture question. The Euclidean closure of the classical real binary
RBM with four visible and three hidden units is a proper subset of the
15-dimensional probability simplex. A strictly positive target is excluded too.
No fatal mathematical gap or required correction was found.

**Recommended campaign disposition:** `already_solved`, one substantive approach
out of five, credited as a verified prior negative resolution. This disposition
records the result of the exact reconstruction and analytic audit. It must retain
the source's status as an **unrefereed, AI-assisted candidate**. It is not a claim
of journal acceptance, human specialist endorsement, formal proof-assistant
verification, historical priority, or a new result by this investigation.

**Credit:** Anonymous, *An eight-point obstruction to universality of RBM(4,3)*,
v0.2.0-candidate, 6 September 2026, DOI 10.5281/zenodo.22550044. Public provenance
identifies Ian Pitchford / Evidence Press as operator/publisher and OpenAI Codex
assistance. No authorship connection to Alec Kriebel was established.

The audited author ZIP has SHA-256
`023751c3c9d7d97dbd860ba42e260e35b3de8563c8ba257baf98b00b22991d06`,
19,315 bytes and 15 files. All 15 remain byte-for-byte identical to the freeze;
its manifest checks. The author packet was not edited.

## 1. Scope and source correspondence

The full paired problem record and prior research report concern whether the
visible **closure** of RBM(4,3) fills the simplex. The catalog's local-surjectivity
title describes earlier partial work, not the question to be answered. This audit
rehashed both complete public corpora, located the unique target record, checked
its statement variants against its paired research record, and verified that the
inspected prior-report copy contains every string field of that research record.
Only dataset hashes, sizes and match results are recorded here.

The [official AIM workshop report, page 2](https://aimath.org/pastworkshops/boltzmannrep.pdf)
independently confirms arbitrary approximation throughout the simplex. Its general
eight-vertex discussion is a proposed outline. The new obstruction therefore does
not contradict a completed theorem stated in that report.

The pinned [source repository](https://github.com/ipitchford/rbm43-eight-point-obstruction/tree/fac57cd9a497a509d443f34f9b9843f6c7a7042f)
was checked through a freshly retrieved, untruncated Git tree. The seven supplied
source files match both their SHA-256/size records and the fresh Git blob hashes.
The annotated candidate tag resolves to precisely the pinned commit. The public
[GitHub release](https://github.com/ipitchford/rbm43-eight-point-obstruction/releases/tag/v0.2.0-candidate)
is a non-draft prerelease published on 2026-09-06 at 19:07:48 UTC.

The full proof and appendix were read. The provenance, status, assurance,
citation and review-response records were also inspected. The [publisher page](https://evidencepress.org/releases/rbm43-eight-point-obstruction/)
continues to state the candidate and review limitations. The DOI URL did not open
through the web tool, so independent confirmation of the Zenodo deposit itself
is not claimed. Public GitHub availability and its publication date are directly
verified. No main-source PDF inspection is claimed.

The third-party producer's executables were neither retrieved for execution nor
run. The author's newly written verifier was reviewed and replayed, but the
verdict does not rest on that replay: the new audit implementation below supplies
a separate exact computation.

## 2. Fresh finite reconstruction

The mathematical input is the printed appendix, cross-checked against the
machine JSON with multiplicities preserved. The audit code requires their exact
public hashes and never imports either the producer or author verification code.

### Different feature representation

For joint index j = 8v + h, the low three bits encode hidden units. The audit
checks twenty Walsh characters: the constant, seven single-spin characters and
twelve visible/hidden pair characters. The spin coordinates are 1 - 2x and
1 - 2h, in least-significant-bit order. This differs from the author's
most-significant-bit Boolean feature implementation.

The change of feature basis is invertible: a pair character equals
1 - 2x - 2h + 4xh. Consequently equality of all checked spin sums is exactly
equality of the augmented Boolean sufficient-statistic sums. This addresses
bit-endianness, spin-versus-Boolean and interaction-order mistakes directly.

### Different symmetry construction

The audit generates each cube group by closure under coordinate flips and
adjacent coordinate transpositions. It does not construct the maps from a
permutation-list formula. The full visible group has 384 elements, exactly six
preserve the target support, and the hidden cube group has 48 elements.
Every transformed identity is checked again in all twenty coordinates.

Only binary-cube coordinate symmetries are used. Arbitrary permutations of the
eight hidden labels are not presumed to preserve the RBM. More importantly, the
coverage computation uses all hidden labels without normalizing any selector,
so no unchecked quotient or representative argument is a premise of the verdict.

### Exact outcomes

- 42 printed identities agree exactly with the JSON multisets
- 12,096 transformed identities pass all feature, support and exponent checks
- 6,608 distinct unrestricted selector conditions
- Degrees: seven identities of degree 2, twenty-five of degree 4, one of degree
  5, eight of degree 6 and one of degree 7
- Maximum degree divided by off-support multiplicity is exactly 4
- 64,569,344 cylinder cardinalities counted with overlaps
- All 16,777,216 unrestricted selectors covered; zero uncovered

Each right-hand multiset specifies a consistent partial selector: repeated
occurrences of a visible state require the same hidden label. Repetitions are
kept in the feature sum and the degree, but correctly collapse to one selector
condition. Left-side repetitions remain in the off-support multiplicity.

### Two new coverage algorithms

1. **Shannon complement counting.** A recursive node holds the remaining partial
   assignments. A completely unconstrained assignment covers its entire remaining
   subcube; an empty assignment list leaves that subcube uncovered. Otherwise the
   next selector variable is fixed to each of its eight labels, and incompatible
   conditions are discarded. Counts add over these disjoint children. Memoization
   merges identical residual problems only. The unrestricted calculation has
   83,326 distinct recursive nodes and returns zero uncovered selectors.

2. **Interleaved truth-matrix evaluation.** Selector positions 0,2,4,6 form a row
   label and positions 1,3,5,7 form a column label. There are 4,096 of each. For
   each row, the program ORs the column predicates of all compatible certificate
   conditions. It checks the resulting 16,777,216-bit truth matrix and finds every
   bit set. This evaluates predicates rather than marking free-digit cylinders.

These differ from the author's all-selector byte-array marking and from each
other. The complete truth matrix has 2,097,152 bytes and SHA-256
`4bda3a28f4ffe603c0ec1258c0034d65a1a0d35ab7bd523a834608adabf03cc5`.
The matrix itself is not included.

As an additional check, fixing the first selector value to zero leaves 4,648
conditions, 8,071,168 overlapped cardinalities and all 2,097,152 normalized
selectors covered. This agrees with the publication's count without being needed
for the unrestricted proof.

## 3. Analytic bridge: adversarial review

Let S be the eight-state support specified in the pinned source, Q a finite
joint RBM law and p its visible marginal. Let eta = min over S of p(x),
m = eta/8 and r = p(S-complement).

**Equal degrees and normalization.** A sufficient-statistic identity equates the
constant coordinate as well as all parameter coordinates. Both joint-probability
products therefore have denominator Z to the same degree D; every parameter
exponent also agrees. No unnormalized-to-normalized mismatch remains.

**Choice of hidden states.** For each of the eight visible states, choose an
actual maximum among its eight joint masses. Its mass is at least p(x)/8 and
hence at least m. Ties cause no problem because the certificate covers every
possible selector, including any tie-breaking choice. No threshold-realizability
restriction on selectors is needed: the exhaustive statement is stronger.

**Direction of the inequality.** The selected right product is at least m^D.
Each left factor outside S is at most r, including every repeated occurrence.
All other left probabilities are at most one. The exact product identity thus
implies m^D <= r^o. Here o >= 1 and D <= 4o. Since 0 < m <= 1, taking the
positive o-th root yields r >= m^(D/o) >= m^4. Reversing the last inequality
would be a serious error; the published direction is correct. The argument uses
D/o, not a false claim that D itself is at most four.

**Entire closure.** The inequality holds at every finite real parameter vector.
The maps p to p(S-complement) and p to min over S of p(x) are continuous in the
finite-dimensional simplex. Therefore the closed set defined by the inequality
contains the entire visible closure. This includes arbitrary escaping parameter
sequences, multiple asymptotic scales and boundary limits. It does not assume
that parameters converge, that hidden maximizers stabilize, or that joint limit
supports have already been classified. When eta = 0 the limit inequality is the
valid trivial bound r >= 0.

**Actual exclusion.** Any law with support exactly S has r = 0 and eta > 0,
so violates the inequality. This excludes approximation, not merely exact
finite-parameter realization of a distribution containing zeros.

No analytic gap was found in these steps.

## 4. Quantitative and strictly positive target checks

For q uniform on S and delta = TV(p,q), event bounds give
p(S-complement) <= delta and min over S of p(x) >= 1/8 - delta. If
 delta >= 1/128 the claimed bound is immediate. Otherwise the leakage inequality
forces delta > (15/1024)^4 > 2^(-25). Thus the stated infimum lower bound
2^(-25) is valid; it is not claimed sharp.

For epsilon = 2^(-25), the law q-plus = (1-epsilon)q + epsilon times the uniform
law on all sixteen states has probabilities 67108863/536870912 on S and
1/536870912 off S. Exact arithmetic confirms positivity and total mass one.
Its off-support mass is 2^(-26), and it directly violates the leakage inequality.

The audit also checks TV(q,q-plus) = 2^(-26), so the triangle inequality transfers
the certified exclusion distance to at least 2^(-26) for q-plus. This proves
failure even to approximate every strictly positive target. The small scale of
these certified bounds supports no practical training-error claim.

## 5. Auxiliary checks and scope discipline

Although not needed for the negative result, the parity-plus-one construction
was checked independently using the public auxiliary data. Exact enumeration of
all 128 joint states confirms ten maximizing states, maximum log-weight four,
gap one quarter and projection onto precisely the nine stated visible states.
A fraction-free determinant check gives one for the specified interpolation
minor; both products with the supplied rational inverse are the identity.

The full-row-rank interpolation permits arbitrary finite log-masses on the
exposed joint face. Scaling the exposing functional suppresses all other states;
normalization then gives the prescribed face distribution. Splitting the one
repeated visible mass between its two joint states supplies arbitrary positive
visible weights on the stated support. Zero weights follow from closure. No
universal claim about other nine-state supports is made.

The earlier local Jacobian witness was recomputed by clearing row denominators
and using fraction-free Bareiss elimination. Its determinant agrees exactly with
the prior value and is nonzero. It proves local full dimension only. It does not
establish density, control escaping limits, or conflict with this obstruction.

The [2018 review, Sections 6 and 9](https://arxiv.org/html/1806.07066v1)
explicitly records a six-hidden-unit upper bound for four visible bits. Combining
that bound with the present three-hidden-unit obstruction gives 4 <= m-min <= 6.
The lower bound uses nesting of the smaller models into the three-hidden-unit
model by adding uncoupled hidden units. Neither four-hidden sufficiency nor the
exact minimum is settled here.

The unused broad support search, solver discoveries, uncompleted classification,
complex generic-rank results and supermodular-rank relaxation are not proof
premises. The author report correctly maintains these distinctions. Its bounded
repository search is not promoted here to an exhaustive absence or priority
claim.

## 6. Controls, reproducibility and limits

Normal and optimized Python runs give identical mathematical results. Fifteen
auditor checks cover altered states, deleted repeated factors, side reversal,
missing forbidden factors, negative and altered exponents, wrong support, empty
and insufficient covers, exact singleton/free-variable counts, independent
matrix-versus-Shannon checks on incomplete covers, and 48 direct-enumeration
comparisons on smaller domains. All pass. The author's eight hostile controls
were separately replayed in normal and optimized modes and all reject as claimed.

The new implementation uses only the Python standard library. Correctness gates
are explicit exceptions, so python -O does not remove them. Receipts, program
source and public source metadata are included, but no source text, machine
certificate, imported dataset contents, scholarly PDF or private coordination
material is included in this audit directory. Public external data are required
for replay.

This is an exact computational and written mathematical audit by a fresh
assistant worker, not an unaffiliated human or formal-methods certification.
No remote writes were performed. The author freeze is unchanged. There are no
required revisions before the parent makes its publication decision within the
existing authorization.
