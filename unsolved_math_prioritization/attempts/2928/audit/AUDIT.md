# Independent audit: Kirby 4.52, ID 2928

## Decision

Accept the separately frozen orientation-clarified derivative as an **unsolved partial result, 3/5 approaches**. The original author archive is preserved byte for byte. The original exact-orbit claim needed an explicit orientation-quantifier clarification before acceptance as a statement of the literal source problem. This audit establishes no general solution, qualifying counterexample, novelty claim, or global open status. It is an independent AI review, not human peer review or formal proof certification.

The accepted bytes are named in `release_pins.json`; the original is not silently replaced. `orientation_clarification.patch` was applied to a clean extraction, and every resulting member was compared with the corrected release.

## Identity and inherited work

All three complete corpus files matched their advertised byte counts and SHA-256 hashes. The unique catalog and problem records identify rank 919, ID 2928, code KP-4.52. The statement digest and the complete-record/report-pair digest match. The pair was recomputed with default Python JSON formatting, sorted keys, and the full record. The associated report key is absent and therefore supplies the stipulated empty object. The entire inherited record was read; it contains background and dated literature triage, not an inherited mathematical attempt. These claims do not rely on its turn count. See `dataset_verification.json`; no corpus contents are included.

The public K3 source was independently inspected at printed/PDF pages 231–232, including both rendered pages. Its main problem concerns closed orientable topological four-manifolds, good fundamental group, initial simple homotopy equivalence, stable homeomorphism, and the existence of some simple equivalence in the identity Wall orbit. The separate spin question must not be substituted for it. The source also records trivial and cyclic positive cases. The live detail-page failures in the author log are historical acquisition limitations, not evidence about mathematical status. [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

## Mathematical audit

### 1. Orbit exactness and orientation quantifiers

Good-group topological surgery exactness is an imported theorem. With the identity as base structure, the zero normal-invariant fiber is the Wall orbit of that structure. One cannot conclude that this fiber contains a structure with underlying manifold N merely from stable homeomorphism.

For a fixed simple equivalence f, every other simple equivalence g factors up to homotopy as (g composed with a homotopy inverse of f) composed with f. The inverse is simple because the Whitehead inverse formula sends zero torsion to zero; the composition formula then gives zero torsion for the self-equivalence. This proves the exact criterion when the allowed self-equivalences match the allowed maps.

The original used only orientation-preserving self-equivalences after choosing an orientation through f. Its proof therefore directly establishes the version with orientations fixed and all maps degree one. K3 specifies orientability, not a separately prescribed orientation on N. Choosing the orientation through one f does not make every candidate g degree one for that same choice. The derivative uses all simple self-equivalences for the literal formulation, with each source orientation induced by its candidate map, and separately states the orientation-preserving subgroup criterion for the fixed-oriented variant. It does not assert that the two branches coincide. This is a quantifier repair, not an asserted counterexample to the old branch.

### 2. Composition, signs, and markings

The packet's direct orbit criterion wisely avoids an untwisted additive formula. For the degree-one convention, Kirby–Taylor equation (17) gives

η(h composed with f) = η(h) + (h inverse)*η(f).

The second term is inverse pullback. The induced fundamental-group automorphism must also be respected when transporting Wall groups; it is not legitimate to keep every marking fixed while replacing the composite by a naive sum. No such invalid step is used in the derivative. Nor is a degree-minus-one version of this coordinate formula needed for its elementary all-map factorization. The normal invariant is based at the identity throughout. Good-group exactness and the structure-set conventions were checked against the relevant sections of [Kirby–Taylor, arXiv:math/9803101v1](https://arxiv.org/pdf/math/9803101v1), with equation (17) visually checked on p.15.

### 3. Spherical cancellation

For a degree-one equivalence, the integer signature coordinate is zero. The phrase “represented by an immersed sphere” thus refers to the mod-two homology class Poincaré dual to the codimension-two normal invariant.

KL Lemma 3.3 has the required local cancellation hypothesis: a spherical invariant with vanishing evaluation of w2. It constructs a self-equivalence φ with the same normal invariant as f; composing with its inverse gives a zero-invariant equivalence. This route avoids an unjustified sign convention. The lemma does not require importing the paper's global four-dimensional group or degree-one classifying-map assumptions into this local statement. The additional Wh(π)=0 in Proposition 2 ensures the resulting equivalence is simple. Goodness then provides the stated unstabilized Wall-orbit conclusion. Pages 6–7 were independently read and rendered. [KL v3](https://arxiv.org/abs/2007.03399v3)

For the stated almost-spin sufficient condition, Wh=0 is still part of Proposition 2's assumptions. Hence f is simple, its simple surgery obstruction vanishes, and the simple characteristic-class formula gives κ2^s(c_*PD(kerv(f)))=0. Injectivity forces the pushed-forward class to vanish. The low-degree universal-cover homology sequence and Hurewicz theorem make the class spherical; almost spin makes w2 evaluate trivially. This is a valid conditional inference. It neither proves injectivity nor Wh=0 for all good groups. KNV's h-decorated argument must not be substituted for the s-decorated one without the stated hypotheses. Its corresponding simple variant and characteristic-class discussion were checked. [KNV v2, §2.2 and Remark 4.2(d)/Proposition 4.3](https://arxiv.org/abs/2405.06637v2)

### 4. Torsion-free three-manifold groups

HKPR Theorem 12.6 is a bound on s-cobordism classes, but its proof contains the stronger intermediate fact the packet uses: homotopy-equivalent manifolds with equal Kirby–Siebenmann invariants admit a zero-normal-invariant equivalence. The proof obtains a spherical class using assembly injectivity; a nontrivial w2 evaluation would force different Kirby–Siebenmann invariants. Wh vanishes for the groups under discussion. Stable homeomorphism supplies equality of Kirby–Siebenmann invariants since S²×S² has zero invariant and connected sum is additive. Applying good-group surgery exactness then gives the desired orbit conclusion for the additional good-group subcases. The source expressly does not assume every torsion-free three-manifold group is good. Its solvable subcases are stated to be good. The packet's use is a prior-result consequence, not a new theorem. [HKPR v1, pp.60–61](https://arxiv.org/abs/2508.07504v1)

### 5. The remaining gap

Stable classification concerns normal-type bordism with its automorphism identifications. This is different from finding a normal bordism over the unstabilized M ending in a simple equivalence from N. Neither a stable homeomorphism nor the existence of a stable self-equivalence proves that the necessary normal invariant is realized or canceled by a simple self-equivalence before stabilization. The derivative preserves this gap. No implication in the audit removes it.

### 6. Literature exclusions

- HU Corollary D, combined with KNV Theorem C, gives homotopy-equivalent examples lacking simple equivalence even after stabilization. Such pairs fail the initial simple-equivalence hypothesis here. They are not qualifying counterexamples. [HU v1](https://arxiv.org/abs/2602.05003v1)
- Kupers–Powell v2 concerns smooth h-cobordism/torsion realization under its explicitly additional assumptions. Its Theorem A and Corollary B do not furnish the missing general cancellation. [KP v2](https://arxiv.org/abs/2604.27635v2)
- The stable exotica abstract concerns a smooth/topological distinction and nonorientable examples. [SE v2](https://arxiv.org/abs/2508.10499v2)
- The fillings abstract/introduction concerns boundary and stable diffeomorphism. A failed abstract-page retrieval was recovered through versioned HTML. No full-paper verification is claimed. [SEF v1](https://arxiv.org/html/2608.23523v1)

## Artifact and source audit

Every one of the original nine ZIP members matched the external manifest, including sizes and SHA-256 hashes; the ZIP itself and external manifest matched the supplied independent pins. All nine corrected members were separately pinned. The original eight tamper scenarios were independently replayed in normal and optimized modes. Sixteen additional scenarios cover type errors, source/identity fields, malformed manifests, symlinks, and directories. For both original and corrected releases, all 48 tamper-mode cases rejected. Both packets passed relocated positive runs in normal and optimized Python, from a different working directory with spaces and non-ASCII characters. The full replay was additionally launched under optimized Python and gave byte-identical results.

Two trust-boundary probes intentionally reseal an altered unchecked rank or altered prose. The packet checker accepts them, as expected: a modifiable local manifest is not an independent trust root, and this checker is not a prose theorem verifier. The pinned external member checks reject the alterations. The audit therefore requires the exact archive and external-manifest pins, not just a local PASS message. These probes are disclosed rather than mislabeled as rejected by the packet checker.

Six author-used PDF pins were independently rehashed and their cited material inspected from fresh text extraction. Relevant K3, KL, HKPR and KNV pages were also rendered and viewed. KT was independently retrieved and pinned. Online version metadata was checked for the arXiv sources; cited published status for KL and KNV is supported by their public records. The historical KL v2 bytes were rechecked but are not substituted for the cited v3. Raw PDFs, extracts and page images remain outside all safe deliverables. See `source_verification.json` for exact limits.

Bounded GitHub searches were repeated read-only for all five PR queries, default-branch code, commit messages and both branch pages. They reproduced no matching target attempt and the two documented unrelated hits. This does not prove novelty or exhaust repository history. See `history_verification.json`.

## Acceptance limits

Only the clarified exact reduction, restricted consequences of imported results, source-scope audit, and conservative 3/5 disposition are accepted. The finite checks validate bytes and selected fields. They do not compute a geometric normal invariant, certify surgery theorems, show an arbitrary group is good, or prove a solution or obstruction for general KP-4.52.
