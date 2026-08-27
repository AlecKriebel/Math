# Work log

## 2026-08-26/27 — active finite-universe reconstruction

Referee issue addressed: the earlier release began downstream of the complete
four-port primitive universe.  A new dedicated workstream was created here so
that the complete relation ledger can be produced and checked without
modifying the manuscript or shared release manifests during development.

The producer independently derived the primitive census
`6 x 2814 x 24 = 405216` and the 27,834 post-topology census.  It compiled
13,686 compatible target/permutation maps and found 4,379 unique literal map
descriptors including the sources.  Exact source ranks were
`20, 21, 21, 21, 23, 24`.

An initial diagnostic partition reproduced the historical rank bucket by
treating point ranks as upper ranks.  That route was rejected: a nonzero
Jacobian minor proves only a lower bound.  It was replaced by exact
coefficientwise polynomial-vector-field syzygies.  The exact identity
`dim E(ker A) = rank([A;E]) - rank(A)` now supplies the upper-rank mechanism.

The syzygy ansatz did not give a strict enough upper for 88 raw presentations.
Rather than inflate the rank claim, a literal transported three-leaf
`H_14` marginal quartic was regenerated for them.  Every target pullback is
zero coefficientwise; every source pullback is nonzero and evaluates nonzero
at a strict rational physical point.

Final producer run completed at 2026-08-27T04:33Z in 769.35 seconds.  It
derived the following exact partition:

- topology excluded: 377,382;
- syzygy-rank excluded: 23,054;
- exact quadratic separated: 1,968;
- transported `H_14` marginal separated: 88;
- isomorphic: 30;
- ordinary-triangle redirected: 114;
- restoration obligations: 2,540;
- final complete residue: 40.

The final residue is exactly 38 presentations in fourteen double-coset orbits
plus two separately classified sink swaps.  The restoration set has exactly
2,540 unique primitive raw identities in 997 K3P-local classes and matches the
active forest root invariants bijectively.

Current best-guess completion toward closing the finite-universe referee
issue: **94%**.  Remaining work at this checkpoint is one complete run of the
independent implementation, the coherent mutation suite, and final evidence
hash/report binding.  No manuscript or shared release manifest has been
changed, and no commit or push has been made in this workstream.

## 2026-08-27 — independent closure

The separate verifier completed the full replay in 1,513.24 seconds.  It did
not import the producer or the historical atlas compiler and did not read the
frozen raw ledger or fourteen-orbit lock.  It reconstructed all primitive
graphs, topology restrictions, 4,379 literal K3P maps, exact Jacobian minors,
3,064 coefficientwise syzygy upper certificates (including explicit nonzero
evaluation-image minors), quadratic and transported \(H_{14}\) pullbacks,
semi-directed graph relations, the full raw ledger, and the double-coset
quotient.  The output was
`K3P_FULL_FOUR_PORT_INDEPENDENT_VERIFICATION_PASS`.

Restoration was bound without transferring historical class ordinals: the
2,540 independently derived `(source,target,permutation)` presentations match
the active forest roots bijectively, and those roots match the active K3P
restoration ledger.  All 36,568 first-layer children and the 43 four-port
probe anchors were cross-checked against their active proof packages.

The coherent mutation suite completed in 26.38 seconds and rejected all six
tests: a hash-resealed raw omission, isomorphic/triangle reclassification,
restoration/quadratic reclassification, internally rank-consistent forged
syzygy ranks, an orbit omission, and optimized Python execution.  Its output
was `K3P_FULL_FOUR_PORT_COHERENT_MUTATIONS_PASS`.

After adding an explicit mutation-output path for drift-free suite execution,
the independent report was replayed in 1,501.20 seconds and its final logical
payload is
`4b92446a2cd8afae0a1966fe3c2670c92ba27f3700e47deecafa5d9f68edd77d`;
the mutation-report logical payload is
`2b4eb58b109a6f84bfbc2dea5dd6d008e4c11ef4b1cfbb2ad242d593072773f2`.
Operational runtimes and paths are excluded from both logical payloads.

Best-guess completion toward closing the finite-universe referee issue:
**100%**.  The dedicated producer, independent verifier, sealed artifacts,
active restoration/probe bindings, and fail-closed mutations now form a
complete checkable package.  Repository integration, commit, and push remain
with the parent workstream.
