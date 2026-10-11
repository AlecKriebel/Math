# Acceptance audit for real elliptic divisor spaces

## Verdict

**Accepted as a previously stated result, with a complete independent
verification of the genus-one proof.** The frozen candidate has no core
mathematical error. Its compressed covering argument is valid when expanded
as in `PROOF.md`. No novelty or higher-genus resolution is asserted.

The input candidate is 3,888 bytes with SHA-256

`505d07b2a8864509a60c036722559315a22daf730df2116c82f5a4f3ff19d300`.

It was independently checked against the supplied freeze record and was
left unchanged. This audit supplies elaboration, not a correction to the
claimed genus-one formula.

## Review status

This proof and audit were prepared with AI assistance. No external human
mathematical review of these artifacts has been obtained. The acceptance
verdict records this audit’s mathematical assessment, not referee
certification.

## Source and attribution controls

The original definition and result were checked directly against the
[publisher PDF](https://ems.press/content/serial-article-files/46800),
including a visual inspection of printed p. 1289, PDF page 45. The exact
source locators and PDF fingerprint appear in `SOURCE_MANIFEST.json`.

The cubic classification was already stated in that report. The proper
assessment of the specific question is therefore prior resolution. This
does not classify the general real-curve problems discussed nearby. The
attribution in `PROOF.md` preserves the source's limited credit for the
initial examples and observations; it does not invent a separate
publication or assign the independent proof to a source author.

## Mathematical checks

1. **Correct space.** The proof uses the unordered reduced totally real
   part of a fixed complete linear system. It does not silently replace
   the original space by a labeled configuration space or remove the
   divisor-class constraint.
2. **Natural topology.** The symmetric-product topology, the product of
   unordered circle configurations for a fixed distribution, and the
   subspace topology from the complete linear system agree.
3. **Real equivalence.** Complex linear equivalence of the real divisors
   descends to real linear equivalence by an explicit constant rescaling
   of the rational function. No additional real obstruction occurs.
4. **Nonidentity cosets.** A common parametrization of the identity circle
   is translated to every occupied component. The component offsets
   remain fixed because the exact counts remain fixed.
5. **Circle cover.** Increasing lifts form a nonempty convex set. The
   cyclic shift followed by one integer increment is the complete deck
   generator, including when there is just one point in a block.
6. **Covering property.** Disjoint arc charts explicitly give evenly
   covered neighborhoods. Identification of fibers alone is not used
   as a substitute for this topological check.
7. **Unweighted sum map.** One application of the cyclic deck generator
   raises a block's coordinate sum by exactly one. The map on deck
   groups is the sum of the exponents, not a sum weighted by the counts.
8. **Nonempty convex fibers.** A common translation in any occupied
   block realizes every real value of the total sum. Every integer
   slice is therefore nonempty and contractible.
9. **Single-slice quotient.** The full deck group acts transitively on
   slice indices. The stabilizer is the kernel of the exponent-sum
   map. A local chart proof identifies the quotient topology and proves
   that restricting to a slice is itself a covering.
10. **Free and proper action.** The block-sum changes detect every
    nontrivial deck element and bound possible translates on compact
    sets. Unordered configurations, including symmetric ones, create
    no additional stabilizers.
11. **Connected component.** Distribution counts are locally constant,
    and the fixed-count fiber is connected. The theorem consequently
    computes the full component based at the given divisor.
12. **Boundary cases.** Degree one yields a point; one occupied circle
    yields a contractible space; two occupied circles yield fundamental
    group ℤ. Zero counts are omitted rather than treated as occupied
    blocks. The empty degree-zero divisor is outside the statement.
13. **Independent homotopy check.** An explicit sum-preserving,
    deck-equivariant equal-spacing homotopy retracts the quotient onto
    a torus of dimension $k-1$.

## Acceptance limits

The proof establishes the claimed result for every positive-degree
reduced totally real divisor on a smooth real genus-one curve with real
points, in its own fixed-distribution component. This includes the
nine-point cubic instance in full.

It establishes no conclusion for higher-genus curves, arbitrary
embedding spaces, the full space obtained by allowing collisions or
nonreal pairs, or a variable linear-equivalence class. Distinct
admissible support distributions may give distinct components of the
same linear system. No claim that the whole reduced real linear system
is connected is made.

The audit involved primary-source inspection and a mathematical proof.
It used no source-author program, numerical approximation, or finite
experiment as a substitute for proof. No external publication,
repository change, or external communication was performed.
