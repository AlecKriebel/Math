# Independent priority findings: PR623 / 30001184

Reviewed at 2026-10-13 UTC after the mathematical gate passed. Frozen proof
SHA-256: `f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3`.
Frozen public head: `947442c091ae617804c6a0d07b98ff2c50368798`.

## Recommendation

**Accept the precise negative source resolution with mandatory antecedent
credit and corollary framing. Do not certify universal first priority or a
new general dilation method.** The existing wrapper already disclaims
verified literature priority, so this is a repair to its antecedent discussion
and mathematical positioning, not a reversal of the correctness verdict.

No primary publication expressly stating the exact forward-generation,
fixed-expectation-GNS negative source theorem was located. However, its
negative conclusion is a short, checkable consequence of a substantial
published antecedent: Burgarth, Facchi and Hillier's point-localized clock
dilation. `PRIOR_IMPLICATION.md` proves that consequence without relying on
problem labels or on an abstract's use of the word dilation. The candidate's
small M2/C2 model, explicit kernel element, and all-positive-time failure are
useful formulation-specific details; this audit cannot certify their first
appearance in all literature.

## The material antecedent

[Burgarth, Facchi and Hillier](https://arxiv.org/abs/2010.00279v2),
*Control of quantum noise: on the role of dilations*, v1 submitted
1 October 2020, v2 submitted 25 July 2022, journal
[online 24 July 2022](https://doi.org/10.1007/s00023-022-01211-y), constructs
an autonomous clock dilation from a finite-unitary path, with an initial
point-localized clock state. The relevant locations are Section 2's
amplitude-damping example, Section 3 Option 1, Definition 4.1, and
Theorem 4.4 Step 2 equation (11). Its authors explicitly place their dilation
in the general C*-framework. No fixed-GNS kernel theorem or OWR generation
counterexample is stated in the inspected text.

The candidate's continuous matrix field, evaluation at zero, and translated
coboundary unitary cocycle therefore belong to an established construction
family. Its compactification and forward-generated restriction adapt that
family to the stated problem. Credit merely to broad product-system papers
does not adequately identify this mechanism antecedent.

[Dive, Mintert and Burgarth](https://arxiv.org/abs/1503.01010), published in
[PRA in 2015](https://doi.org/10.1103/PhysRevA.92.032111), give finite
time-dependent unitary dilations and identify the initial singularity for
dissipative Markov dynamics. Their Appendix B and quantum Zeno discussion
are antecedents for the square-root-angle behavior, not an autonomous
generated-algebra GNS counterexample by themselves.

[vom Ende, Theorem 1](https://arxiv.org/abs/2211.08351v3), public since 2022
and published in 2023, proves that a finite-system quantum dynamical
semigroup admitting a bounded-total-Hamiltonian Stinespring curve is
unitary. Its first-derivative argument is closely related to the reviewer
obstruction below. It is not literally a theorem about a general
conditional-expectation dilation's fixed GNS representation.

## Exact implication and its limits

If the fixed GNS image R is finite-dimensional and its kernel is invariant
for every positive time, point-norm continuity induces a differentiable
endomorphism semigroup on R. Its generator delta is a derivation. The
expectation descends to a B-bimodule expectation pbar, so

    L(bc)=pbar(delta(bc))=L(b)c+bL(c).

Thus the compressed generator is a derivation. On C2 every derivation is
zero, while the candidate has L(1,0)=(-1/2,+1/2). This is a complete
analytic obstruction, not a sampled computation and not an assumption of
strongness on all A.

The literal BFH amplitude-damping path has finite limits at both ends of
the real line. It therefore extends to the two-point compactification.
Restricting its clock dynamics to the forward-generated observable algebra
gives a unital separable, injective, point-norm continuous general dilation.
Evaluation followed by finite bath compression yields a finite GNS image.
Its decaying projection satisfies T_t(q)=exp(-t)q, contradicting the
derivation condition. Hence the universal source proposal fails as a short
corollary of the existing explicit clock model. There is no mathematical
gap in this reviewer-derived implication.

The exact symmetric P in PR623 also follows by inserting the standard
bit-flip finite unitary in that clock construction. A fully explicit M4/C2
version and its conditional expectation are recorded in
`PRIOR_IMPLICATION.md`; `verify_prior_implication.py` independently checks
its exact compression and that of the BFH amplitude-damping model.

The generic BFH unitary theorem's strong continuity is insufficient on its
own to assert point-norm continuity on all C_b(R). The finite endpoint
limits of the particular paths used above close that possible gap. The
candidate's two-point compactification accomplishes the same purpose.
Its initial angle cusp is compatible with continuous E0 dynamics; the
bounded-Hamiltonian obstruction applies to the proposed finite descended
dynamics, not directly to the infinite clock algebra.

The derivation proves that invariance cannot hold at *all* times. The
candidate's explicit witness/strict concavity calculation proves the
stronger statement that every positive time fails. BFH and the
first-derivative theorem alone do not state that refinement. Its small
matrix realization is a legitimate concrete improvement in presentation
and explicitness; no searched primary source was found duplicating those
exact details. Absence of a found match is not a first-discovery certificate.

## Other potentially misleading prior claims

The [2009 OWR source](https://ems.press/journals/owr/articles/3392) is the
fixed general dilation's two-stage proposal, and expressly suggests
generation by the observed algebra and its shifts. The precise negative
reading is therefore supported. A counterexample to descent defeats that
conjunction. It does not supply a useful stronger/incomparable smallness
criterion or settle extension once descent is assumed.

[Skeide and Sumesh, v2 Section 5 p.34](https://arxiv.org/abs/1210.7491v2)
poses the corresponding fixed-action intertwining question. Its CPH
existence results construct a different structured dilation; they do not
assert the offered universal generation-only descent theorem.

[Shalit and Skeide, v3 Appendix B(i)](https://arxiv.org/abs/2003.05166v3)
separates general compression, strongness on all A, and weak corner
dilations. Its principal theorems concern weak dilations. Neither
algebraic minimality within that category nor the fact that weak Markov
dilations are strong can be imported into this unital general example.

[Kaad and Skeide](https://arxiv.org/abs/2101.03030) addresses kernels of
non-adjointable module maps and double orthogonal complements; it is a
different kernel problem. [Paired E0-semigroups](https://arxiv.org/abs/2303.05249v4)
concerns product-system commutants and faithful von Neumann dynamics, and
provides no matching result in its inspected treatment. The 2026
[Mickelson thesis](https://arxiv.org/abs/2605.04096) is an exposition of
finite dynamical-curve dilations and initial singularities; no source
fixed-GNS counterexample was found there.

Bare nonfaithfulness is not itself the claimed result. A translated
evaluation state is a standard way to move a GNS kernel, but with scalar
observed algebra the exact forward-generated algebra is just scalar.
One must also preserve nontrivial Markov compression and exact generation.
Similarly, requiring stationary states, complete multitime Markov moments,
normality, faithfulness, or a corner introduces assumptions absent here.
`METHOD_COMPARISON.md` records these distinctions.

## Chronology and current public checks

Unauthenticated current GitHub API reads confirm that the repository is
public, PR623 is accessible, its creation was `2026-10-04T16:57:00Z`, and
its head remains the frozen head. The associated author/commit timestamp is
`2026-10-04T16:56:02Z`. These are bounded public records: the PR creation
is stronger publication evidence than a Git timestamp, but current public
visibility alone does not prove continuous public access since October 4.
There is no present exact contemporaneous matching publication whose date
must be compared to that PR. See `CHRONOLOGY.md` and
`CURRENT_PUBLIC_VISIBILITY.json`.

The current EulerSolve paper catalogue and full sitemap were checked
directly, supplementing search-engine queries for OWR-3392-012, 30001184,
GNS, and Skeide. No mathematical target match was found. The guessed
exact-label paper permalink returned HTTP 404. Initial default-client
requests returned 403; normal browser-user-agent reads succeeded. The
catalogue contains 217 papers (218 paper URLs including its index in the
sitemap). A case-insensitive raw HTML GNS hit was the substring in *signs*;
visible text and target tokens have no matching result. This is a bounded
catalogue check, not a finding that no unpublished, unindexed, renamed,
or later work exists.

## Mandatory repair and strongest permissible claim

Add BFH to the candidate's Sources and status discussion and explicitly
connect its evaluation/clock/cocycle construction with the earlier method.
Add the relevant finite-unitary/first-derivative antecedents if discussing
the mechanism or the obstruction. Keep the existing no-verified-priority
disclaimer.

The defensible framing is: an explicit small-matrix counterexample to the
forward-generation-only fixed-GNS proposal, obtainable as a
formulation-specific corollary of known point-localized clock machinery,
with an exact witness and failure at every positive time. A claim to a new
general dilation method, first universal negative resolution, or material
priority over BFH is unsupported. The broader stronger-minimality,
conditional-extension, different-dilation, normal W*-promotion, and
future-algebra problems remain outside the result.

If only substantially new mathematical discoveries qualify for this
research programme, the corollary's degree of novelty requires that
separate policy decision. This review recommends the requested negative
resolution be accepted after the above repair because it is exact and
checkable, while its small explicit realization supplies an identifiable
formulation-specific contribution. It does not recommend presenting the
negative phenomenon itself as a previously unavailable mechanism.

No external person, author, other shard, or organization was contacted.
No PR, queue, remote, Zenodo, GWS, or native candidate was mutated.
All authored artifacts are confined to `reviews/priority_01`; raw sources
are in ignored `sources.private/`, rendered pages in ignored `tmp/`.
