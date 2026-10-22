# Independent adversarial audit: Erdős Problem 100 / ID 1929

## Verdict

**PASS within the scope below. No mathematical corrections required.**

The frozen packet correctly remains **unresolved, 5/5 approach families exhausted**. Its nine retained propositions, the normalization objections, the energy limitation, and the Piepmeyer reconstruction are sound. Neither the author's finite controls nor this audit proves the general linear-diameter conjecture. This is an independent AI-assisted mathematical audit, not human peer review or a novelty certification.

Audit date: 2026-10-05 UTC. The auditor was not an author of the frozen packet. No source file was modified, no helper was delegated, and no remote write was made.

## Frozen input and integrity

- Archive: `ERDOS_1929_AUTHOR_SAFE_FREEZE.zip`
- Archive size: 20,826 bytes
- Archive SHA-256: `eab5d5ccc69c6fd8ef9771d14ca78c9da36fc31ddfc32052b718bce97684ce62`
- Author manifest SHA-256: `6156bec0ed953bc03854b4f6926b10eb9d8a4c3a1e676247716374e712a3bedc`

Both expected pins matched. All nine archive members exactly matched the corresponding regular files in the author directory. The eight manifest entries matched their sizes and hashes, with no extra member, directory, symlink, PDF, extracted source text, raw dataset, or private coordination material. This audit is a separate sidecar and leaves the author freeze unchanged.

## Exact target and quantifiers

The target concerns distinct planar points, minimum positive distance at least one, and **unequal distance values** at least one apart. Repeated distances are allowed; integrality is not required. An attained minimum of exactly one is an additional hypothesis, not a valid normalization of a general instance.

The intended conclusion is an absolute positive constant times n, eventually uniformly over all admissible configurations. Changing a strict diameter inequality to a weak one only changes the constant. The eventual n−1 conjecture is stronger. A fixed nine-point counterexample to the unqualified n−1 inequality refutes neither eventual assertion.

The original 1985 source explicitly contains both separation conditions. The indexed Problem 100 statement agrees. The current FormalConjectures definition allows coinciding points within distance comparisons, so comparing a positive distance with zero also enforces the minimum-distance condition. This is consistent with the packet's interpretation.

## Claim-by-claim adversarial review

### Proposition 1: spectrum counting — PASS

Summing the k−1 gaps gives D ≥ m+k−1. Taking floors yields precisely k ≤ floor(D−m)+1 ≤ floor(D), including k=1. No distinct-pair-count hypothesis has been substituted for a distinct-value-count hypothesis.

### Proposition 2 and the energy discussion — PASS

A finite nonempty positive spectrum has positive minimum and, when applicable, positive minimum successive gap. Scaling by the larger reciprocal makes both constraints hold. The single-value case is correctly separated.

For B=n(n−1)/2 unordered pairs, Cauchy–Schwarz gives B² ≤ k∑f(s)² and hence D ≥ B²/∑f(s)². A uniform O(n³) energy bound would imply a linear diameter estimate, but scaling preserves equality multiplicities. The standard square-grid distinct-distance estimate, imported and credited to the Guth–Katz introduction, implies energy at least a constant times n³√log n on that family. Thus admissibility alone cannot furnish that proposed uniform energy bound. This obstruction does not claim to disprove a scale-sensitive linear-diameter theorem.

### Proposition 3: two anchors and two circles — PASS

For a closest pair at distance m, each other point has positive radii in the global spectrum and satisfies |r−s|≤m. Separation of spectrum values gives at most floor(m) values on each side of a fixed radius, including endpoints correctly. Distinct centers ensure at most two circle intersections for any ordered radius pair, including tangent or disjoint cases. Therefore n−2≤2k(2floor(m)+1)≤6mD; the last step uses m≥1. The bounded-minimum linear conclusion is correctly conditional on a fixed absolute upper bound for m.

### Proposition 4: packing and the explicit exponent — PASS

Open disks of radius m/2 are pairwise disjoint and contained in a disk of radius D+m/2 about any selected point. Area comparison gives m(√n−1)≤2D. Substitution into Proposition 3, for n≥3, proves D≥√((n−2)(√n−1)/12). The denominator is positive and the inequality direction is correct. The resulting n^(3/4) order is credited as historical, with a nonoptimal constant; it is not advertised as the strongest retained literature bound.

The corollary m_j→∞ along any n_j→∞, D_j/n_j→0 sequence follows directly from m_j≥(n_j−2)/(6D_j).

### Proposition 5: attained unit distance — PASS

For a unit anchor pair, unequal positive anchor radii must differ by exactly one; anchor endpoints themselves are handled separately by their radii 0 and 1. Equality in the reverse triangle inequality places the point on the anchor line. Equal radii place it on the perpendicular bisector. Unit point separation gives at most floor(D)+1 points on either line. Summing is valid even when the lines intersect, because overcounting only weakens the upper bound.

The admissible 3–4–5 triangle scales to distance gaps 1/3 at unit minimum, decisively invalidating the proposed general normalization. The audited PRV preprint's final paragraph expressly uses attained unit minimum, so its stated special case is not promoted to a resolution of the broader target.

### Propositions 6 and 7: strip bounds — PASS

For 0≤h<1, equal horizontal coordinates would violate unit separation, and every successive horizontal gap is at least √(1−h²). Summing proves the stated lower bound. For arbitrary finite width, disks of radius 1/2 are contained in a rectangle with side lengths D+1 and h+1. Their area gives D≥πn/[4(h+1)]−1. These arguments need only point separation and are correctly limited to fixed width for a uniform linear bound. For a sublinear-diameter sequence, the inequality actually forces the minimum enclosing strip width to tend to infinity.

Brass's abstract describes a sharper asymptotic result with an additional half-strip restriction. The packet does not claim that its two elementary estimates reprove or subsume that result.

### Proposition 8: square grids — PASS

Grid squared distances are integers at most 2a². Rationalizing their square-root difference gives a lower bound 1/(2√2 a), so scale 4a is safely admissible. The realized distances a and √(a²+1) force t≥√(a²+1)+a>2a for every admissible dilation. Both diameter constants and the strict lower inequality are correct, including a=1. With n=(a+1)² this excludes the canonical normalized grid family as a sublinear-diameter counterexample, without excluding other configurations.

### Proposition 9: Piepmeyer reconstruction — PASS

The original Erdős source attributes the construction to Lothar Piepmeyer. The reconstructed two equilateral triangles have parallel sides and corresponding-vertex displacement x. The three additional points are verified as the appropriate four-endpoint circle centers. The three signed radii and three directions yield nine distinct points.

A fresh verifier uses the primitive element t=√2+√3 with t⁴−10t²+1=0, rather than importing or reusing the author's biquadratic arithmetic implementation. It checks the positive radical branches, reconstructs the points after a rational translation, and checks all 36 Cartesian squared distances independently. The six block counts match the written partition; the four total multiplicities are 6,18,6,6.

It also verifies that x is the unique root of X⁴+4X³−4X²−4X+1 in (1249/1000,1250/1000), using exact opposite endpoint signs and a strictly positive derivative throughout that interval. Rational interval arithmetic verifies the distance ordering, minimum x>1, three gaps with minimum exactly one, and 4663/1000<D<4664/1000. Positivity makes equality of squared lengths sufficient. A perturbed-coordinate construction and the negative seed root are rejected. The rescaled middle gap is 1/x<1, so normalization fails here too.

## Imported theorem and literature-status boundary

The Guth–Katz publisher page and published Theorem 1.1 explicitly give an absolute-constant n/log n lower bound for planar distinct distances. Combining it with Proposition 1 is valid. The full incidence proof is imported, not independently re-proved. The packet consistently acknowledges this stronger partial result and makes no best-known-bound certification beyond the literature it retained.

Fresh direct access to the live Erdős Problem 100 page returned HTTP 403. A separate indexed retrieval, reported as approximately three months old, marks the problem open and describes the same partial results. That is not a live status or comment-count certificate.

A fresh GitHub connector read of FormalConjectures/ErdosProblems/100.lean returned blob `394a51ed60e5646efa1f701fa6ba992978c05af2`, matching the author metadata. Both the general conjecture and eventual n−1 variant are marked research open. Declarations with `sorry` are not proof certificates. The linked formalization of the finite Piepmeyer construction was not compiled by this audit and is not treated as a solution of the general conjecture.

The old source's Kanold attribution and the publisher's Brass abstract were independently checked. The original Kanold proof, the full Brass proof, and an exhaustive present-day literature search remain outside scope. The bounded search found no verified full resolution. These limits match the frozen packet's caveats.

## Executable checks

- Author mathematical output exactly equals CONTROL_RESULTS.json
- Author manifest replay passes all ten stated mutation controls
- Author mathematical checker correctly rejects Python optimized mode
- Independent primitive-element algebra and all 36 construction pairs pass
- Independent rational root-gap bracket cross-checks: 11,175
- Independent grid sizes: 80; adjacent-gap checks: 70,281
- Independent radius-neighbor/constant controls: 2,025
- Independent unit-anchor coordinate identities: 2,883
- Independent pinned-input integrity rejects seven mutation classes
- Independent verifier produces identical output in normal and optimized mode, because its checks do not rely on Python assertions

Finite controls do not certify universal geometry claims. The preceding proof review is the basis for accepting the quantified assertions.

## Scope exclusions and publication guidance

The public repository dataset manifest was freshly retrieved at the pinned commit, and its hashes, sizes, record count, and Git blob matched the metadata. This audit did not re-read the complete raw datasets, repeat all earlier repository-absence searches, certify historical timestamps, or verify every past retrieval action. Those historical provenance assertions are not transformed into fresh independent certificates by this PASS.

Required corrections: **none**. Preserve the frozen author package and attach this independent audit as a separate record. Preserve the unresolved status, five exhausted approaches, known-result credits, failed-live-access caveat, and no-novelty language. Do not describe this PASS as proving Erdős Problem 100, as a new n^(3/4) result, or as human peer review.

## Reproduction

From the directory containing the author packet and this audit:

    python erdos_1929_independent_audit/independent_verify.py erdos_1929/safe_output
    python -O erdos_1929_independent_audit/independent_verify.py erdos_1929/safe_output
    python erdos_1929_independent_audit/verify_audit_manifest.py

Compare the first two outputs with INDEPENDENT_RESULTS.json. The mathematical checker also runs without its optional author-directory argument, in which case it omits the frozen-input integrity section. Source inspection is documented separately and is not performed by that mathematical checker.
