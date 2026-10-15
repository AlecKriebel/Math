# Fresh sequential adversarial review 02 — PR256 / 5100017 / AMR-050-0017 / k307

**Disposition: PASS. No actionable scientific, manuscript, attribution, metadata,
or portable-package finding was identified in the reviewed candidate.**

Review completed 13 October 2026 UTC. Review completion estimate: 100% of this
assigned fresh finished-candidate audit. This is independent AI adversarial
review, not external human peer review, formal proof-assistant verification, or
an exhaustive historical priority certificate.

## Independence and scope

`INDEPENDENT_PLAN.md` was recorded before reading the candidate source or any
prior proof/report. The independent mechanism was direct real projection and a
paired-edge Cartesian moment matrix with endpoint potentials. The complete
manuscript source and all five PDF pages were inspected. The independent
real-coordinate derivation/checker were authored before reading the archive's
Cartesian derivation. `review_01` was never read. Existing packaged proofs and
reports were consulted later to check scope and documentation consistency.

The exact accepted claim is a phase-independent **signed** area centroid of
ordered perpendicular feet onto the full outer tangent lines, for a noncircular
ellipse, strict confocal elliptic caustic, and least even period at least four,
where the signed area is nonzero. The classification is no excluded pedal
points for `d>=0`, and exactly the fixed circle `|M|^2=-2F/d` for `d<0`.
Primitive stars are allowed. Simple winding-one even families have `d>=0`.
Least period four is equivalent to `d=0`, with centroid `M/3`.

## Direct mathematical audit

The written proof is an all-period argument. Its geometric, algebraic, and
definedness steps were checked directly; finite tests were used only as
corroboration. `INDEPENDENT_REAL_DERIVATION.md` supplies the checkable alternate
derivation and detailed boundary reasoning.

- The commuting Poncelet map/half-turn group is finite. Its action on a finite
  orbit is faithful because a finite-order orientation-preserving circle
  homeomorphism with a fixed point is the identity. Its circular-order action
  is cyclic, giving the unique involution `T^(N/2)=A`. Least period is essential;
  padded odd cycles do not silently acquire the hypothesis.
- The strict origin-inside-caustic condition places the origin left of each
  positive oriented tangent chord. Forward lifted normal steps lie strictly in
  `(0,pi)`, including stars. Therefore `S(0)>0`, and adjacent outer tangent
  intersections remain finite.
- The eccentric-angle chord tangency equation converts to the displayed support
  identity. Both `F±ed` are strictly positive. The squared-support dot relation
  is used only as a consequence of actual billiard supports, never to construct
  an orbit, so no extraneous squared solutions enter the theorem.
- The doubled-normal lemma and origin-area relation telescope in trajectory
  order without requiring simplicity. `S_Z` is nonzero for `d!=0`; its sign is
  allowed to vary between trajectory types.
- Antipodal paired averages remove the specified odd-support terms without a
  factor-two error. The full linear and cubic moments agree with the direct
  real-coordinate matrix/potential expansion. A separate Laurent check verifies
  the manuscript's displayed `c`, `b`, `r`, `s` coefficients and local telescope.
- Translation changes the raw signed moment by `6cS`, including zero-area and
  self-intersecting polygons. Dividing only at the last step gives exactly the
  stated explicit complex centroid formula and its denominator `G`.
- The four-period forward implication follows by adding the two sign-reversed
  consecutive support identities. Its converse fixes each normal step at
  `pi/2`; the independent rectangle calculation supplies `S=2AB` and
  `T=4ABM`. This avoids all intermediate divisions by `d` or `S_Z`.
- For every simple winding-one even `N>=6`, the first half of the doubled normals
  are at least three distinct circularly ordered circle points; the full polygon
  traverses their convex polygon twice. Its positive area implies `d>0`.
  Together with period four this proves validity for **every** real pedal point
  in every simple even family.
- The zero-area classification is exact. The exact primitive 8/3 star has
  `d=-120/221`, `F=2795/1728`, `v=7/13`, and zero radius squared `123539/20736`.
  Direct unrestricted Cartesian projections reproduce every displayed area and
  cubic-moment polynomial. Exact reflection, caustic tangency, primitive period,
  winding three, reversal, and reflection controls pass. At the displayed zero
  point the moment is the stated nonzero vector, so no removable-zero reading
  rescues that diagnostic centroid.

No hidden extension to circular boundaries, hyperbolic or degenerate caustics,
unsigned union centroids, or odd primitive periods was found. Units of the
support, area, raw cubic moment, and centroid formulas are consistent.

## Checkable evidence and package replay

`fresh_real_coordinate_checks.py` passed **79 fresh exact assertions** with
SymPy 1.14.0. Its receipt is `FRESH_EXACT_RECEIPT.json`.
`written_laurent_checks.py` passed **13 focused manuscript-local exact
assertions**, recorded in `WRITTEN_LAURENT_RECEIPT.json`.

The first custom checker invocation was stopped because its nested-rational
expansion was unnecessarily expensive. Combining/factoring the rational
expression before simplification made the same exact checks complete. No
failed mathematical identity was produced. This diagnostic is recorded in the
research log.

The supplied ZIP was extracted into this review directory after rejecting
absolute/traversal paths, duplicate member names, and symlinks. An independent
manifest scan verified all **37 authored files** and the manifest's complete
coverage of the **38-file archive** except itself. Archived paper source,
metadata, README, requirements, runner and license match the candidate copies
byte for byte. `metadata.json` equals the metadata object in
`zenodo-deposit.json`; both declared deposit files exist. The title, version,
publication date, author, ORCID, license, signed-domain description, and AI/
unrefereed disclosures agree across source, rendered PDF, README and metadata.

The documented default `run_verification.py` was executed normally using the
specified scientific runtime from the independent extraction. It passed the
integrity check and all **three** selected portable programs, including the
4355-assertion rational checker, the real Cartesian symbolic certificate, and
the exact winding certificate. All return codes are zero and their generated
receipts are preserved under the extraction's `replay-output/`.
`PACKAGE_RECEIPT.json` records package integrity and runtime versions. A prior
complete seven-program replay was already available; no redundant broad rerun
was performed in this review.

The archived raw numerical failure history states that initial full failing
scripts were not retained and labels its reconstructed reproducer honestly.
README explains that timestamped numerical reports need not be byte-identical,
that numerical checks corroborate the written proof, and that the earlier
pending-stage audit statements are historical. The portable runner uses copied
scripts and temporary working directories, leaving archived evidence unchanged.

All five rendered PDF pages are legible, with complete equations, references,
page numbering and disclosure text, and no clipping or missing glyphs observed.

## Attribution and bounded-priority wording

The original [Reznik–Garcia–Koiller arXiv v11](https://arxiv.org/abs/2004.12497v11)
and final publisher PDF were checked at their signed-area definition, Section
3.4 and Table 4. They identify `k307` as the outer-pedal area-centroid observation
and distinguish `k306`, the vertex centroid. The original Bialy–Tabachnikov
publisher text was checked at Theorem 4.1 (k306/k302) and Theorem 4.3's classical
even-period symmetry. The original
[Schwartz–Tabachnikov paper](https://arxiv.org/abs/1607.04766) explicitly uses
signed area centroids for nonembedded Poncelet polygons. These support the
manuscript's credit and distinctions.

The paper does not claim firstness, newness of the cyclic lemma, or novelty for
classical symmetry/support/signed-moment methods or the reused exact star.
Its statement that two documented bounded audits found no earlier covering
proof is supported by the packaged audit reports. Their precise residual
historical uncertainty is retained. This fresh review checks the accuracy and
modesty of that wording; it does not impose or claim an exhaustive new priority
search.

## Pinned reviewed candidate and final integrity

| Artifact | SHA-256 |
|---|---|
| `outer_pedal_centroid.tex` | `c740565076e9a1aa67ce6cb9a4ec64d4110ac55adaeb339d9d1b16089cabd88a` |
| `outer_pedal_centroid.pdf` | `988ff679538849d4bfaa6c7bdd60077e35533aa24baa17cf1e386ec57fb40411` |
| `metadata.json` | `9cb5db7dd13fc98085bcb8e1395de4613912fb0b43dd16b763766a6685d5a483` |
| `zenodo-deposit.json` | `f32f9684f61e6d05ab21b2fafb1876672e37c594c1106585fa9c11bf102e49bb` |
| `outer-pedal-centroid-verification.zip` | `7c2a3ce49e095b4d0e045cf60c1c19d7137dc6a659a699d922b400493f07bf33` |

`initial_hashes.json` and `FINAL_INTEGRITY_RECEIPT.json` compare the beginning
and end of this review. All **47 scientific/package files** covered by that
comparison are unchanged. Three parent-maintained checkpoint/publication
bookkeeping files changed during the review (`CANDIDATE_CHECKPOINT_RECEIPT.json`,
`PACKAGE_STATE.json`, `publish_checkpoint.py`); they are not part of the
manuscript/metadata/verification artifacts assessed here. No scientific file
was edited, no provider or Git mutation was made, and no external individual
was contacted.

**No required fix remains from this review.** The PASS is scoped to the exact
hash-pinned candidate and the hypotheses/disclosures stated above.
