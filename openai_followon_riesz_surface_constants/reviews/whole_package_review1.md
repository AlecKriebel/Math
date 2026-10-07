# Fresh independent whole-package adversarial review 1

Reviewed on 2026-10-06T21:26:03.201660-07:00 (2026-10-07T04:26:03.201660+00:00). Reviewer: independent subagent `whole_package_review1`. Original task: exact ordered-pair constant for every real s>2; smooth compact embedded surface transfer, explicit boundary/ambient convention, and unit-sphere coefficient; no crystallization, finite uniqueness, or new s≤2 claim.

## Verdict

**REPAIR BEFORE PUBLICATION: mathematical argument passes this review; two concrete package documentation/attribution defects require repair, and one diagnostic-reproduction scope statement should be clarified.** No material mathematical gap, counterexample, incorrect factor, unfulfilled geometric hypothesis, or unsupported headline novelty claim was identified in the actual manuscript and dependency chain inspected here. This verdict is for the exact candidate below. It is not a favorable verdict for bytes changed later. A fresh complete-package reviewer should inspect the repaired candidate from scratch before publication.

The proof establishes the required exact minimum-value consequence of the retained OpenAI theorem. It does not establish microscopic crystallization or any s≤2 theorem. The substantial new input belongs to OpenAI; the finite/periodic and manifold reductions are inherited. A narrowly titled and credited consequence note is a defensible publication of this explicit planar corollary on the evidence inspected; it must not be advertised as an independent solution of universal optimality, a newly invented reduction, or a firstness result. Negative searches cannot certify first public priority.

## Exact reviewed candidate

`publication/CANDIDATE_MANIFEST.json` identity:

`1e2d272246398abd2ff4186ea9857a756fdc829e0e9d164c56e376c7ff1a77c3`

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| publication/main.tex | 17096 | 1dd9b9a88304d580bede386f12acacf55a803063d3cfca7d7d0de0cfa453b698 |
| publication/upload-kit/paper.pdf | 87034 | 79d21f3d716c983abaff4078e9243eb43a58cdcc0fc23502d768c3d9bd8b27a3 |
| publication/upload-kit/source-and-verification.zip | 98012 | 75f4d84a507245b63d0aaf9725042f797d9788912600211a547de32fff75a774 |
| zenodo-deposit.json | 3140 | c62abfe8db3da9e3dd3833002a115a2248f5c64164a76bd07a1df97ea93bad01 |

I independently recomputed the candidate identity, checked all 31 manifest file size/hash pairs, checked every one of the 28 archived file pairs and the exact ZIP name set, and checked that `PACKAGE_CONTENTS.json` agrees with the manifest. No unexpected archive member, third-party manuscript/source copy, cache, token, or private tracker file is included. Credential-pattern checks found no GitHub token, AWS key, or private-key marker. The contents are an explicit allowlist; this check does not purport to prove absence of every conceivable secret by regex alone. `publication/metadata.json` exactly equals the deposit manifest's metadata object. Author, ORCID, date, title, s>2 scope, boundary/ambient convention, license and related identifiers agree with the paper.

The retained external source pin is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. A read-only `git ls-remote` check during this review again returned that exact public main commit. No later correction was substituted. The source clone was not modified, built in place, or contacted through any individual.

## Required repairs and evidence

### R1 — reproduction guide references a proof absent from the deposited archive

`reproducibility/README.md` begins, “Read publication/main.tex and proofs/bridge_independent.md.” The exact ZIP contains `proofs/FINITE_TRANSFER.md`, **not** `proofs/bridge_independent.md`. I checked the actual ZIP entries rather than inferring them from the builder. Thus a depositor following the guide from the archive cannot open the promised second file. Replace this reference with the included detailed proof or include the referenced proof, then regenerate the ZIP/manifest and review those exact bytes. This is a bounded reproducibility-documentation defect; the standalone paper and included detailed proof already contain the needed argument.

### R2 — supplementary proof retains superseded novelty wording

The opening of `proofs/FINITE_TRANSFER.md` says it “proves the **new reduction** conditional on that dependency.” The final manuscript, dependency ledger and primary-source priority audit correctly identify the finite/periodic reduction as established machinery (HSS2014 Theorem 3.2; HLSS2018 Proposition 3.1). The derivation was independently prepared in this effort, but that does not make the reduction itself new. Remove the novelty adjective and add a concise current attribution/disposition, while preserving the legitimate historical statement about independent preparation. Propagate the correction into the deposited archive. This is an attribution-consistency defect, not a flaw in its equations.

### C1 — clarify the scope of an audit command outside the archive

`agent_notes/formal_audit.md` tells readers to run `python3 audit_sources.py` from `reproducibility/formal`. That script and directory are absent from the published ZIP, whose formal evidence is intentionally restricted to hashes and results. The paper correctly disclaims a complete Lean build, so this omission does not hide a formal-verification dependency. Nonetheless, make explicit that the command names a research-checkout step, or distribute a portable own-authored diagnostic runner. Do not imply that the deposited archive alone provides that particular command. Third-party Lean copies should remain excluded unless separately licensed for redistribution.

The root research README still says input validation/conditional bridge research; it is outside this candidate ZIP. Its final status should be brought current after the publication outcome is known, without making a deposit claim before publication.

## Mathematical falsification and independent checks

### Exact finite transfer

I read the complete standalone `main.tex` and the full included `proofs/FINITE_TRANSFER.md`, reconstructing the inequalities independently.

- The covolume of the displayed triangular basis is b times b^(-1), hence one. The lattice sum counts every nonzero displacement once per outgoing row and therefore matches the ordered finite energy; there is no half-pair factor.
- For a fixed finite motif in `[0,L)^2`, uniqueness modulo LZ² excludes a zero denominator. The sup-norm translation shell has exactly 8m vectors and denominator at least Lm/2 for m≥2, so the row tail is bounded by a constant times Σ m^(1−s), finite precisely for s>2.
- Shifted square tilings give each motif coset's centered-disk count πR²/L²+O(R/L+1). Completing full rows gives the upper bound. Retaining length≤T rows from B_(R−T), then taking R→∞ before T→∞, gives the lower bound. This proves the exact centered-disk ordinary limit and per-particle normalization for every fixed motif; no averaging-convention replacement or uniform-in-N limit is used.
- Scaling lengths by λ multiplies density by λ^(-2) and per-particle energy by λ^(-s). The gap motif has density (1+ε)^(-2), so compression by λ=(1+ε)^(-1) restores density one and multiplies energy by (1+ε)^s, the direction needed for the claimed lower inequality.
- The cross-cell sum explicitly includes i=j for nonzero translations. For every original distinct finite configuration, a coordinate with |k_a|=m gives distance at least √N((1+ε)m−1)≥ε√N m. Summing N² motif choices and dividing by N gives exactly 8 ε^(-s) ζ_R(s−1) N^(1−s/2). This bound does not require separation or bounded local occupancy.
- The correct limit order is fixed N,ε disk radius→∞, then N→∞ at fixed ε, then ε↓0. Since s>2 is fixed, the displayed error vanishes. The estimate is not uniform as s↓2 and makes no claim at s=2.
- The fundamental-cell area argument gives at least N triangular sites in side √N+2D. Choosing any exact-N subset can only decrease the positive outgoing row energy. Rescaling produces the asserted limsup with no exact crop-count assumption and no uncontrolled discarded tail. Its combination with the liminf proves an actual limit.
- N=1, closed-square endpoints, collisions assigned +∞, disconnected surfaces and arbitrary close motif points cause no contradiction. Positive area excludes the zero-measure branch. The proof claims no all-minimizer classification.

The optional square-periodic variational formulation in the detailed proof is also sound. Its unresolved P_s=Z_s step is expressly marked equivalent to the needed energy lower bound, rather than misrepresented as a new proof. The exact triangular lattice need not possess an axis-aligned square period; the separate triangular crop supplies P_s≤Z_s.

### Pivotal OpenAI analytic input

I did not accept U just because it appears as a theorem or because finite certificates pass. In the pinned **main** manuscript I read the exact theorem/definitions, the complete cardinal/Fourier, positive quadrature/finite-data, infinite correction, global-sign, Gaussian energy-transfer and shifted-mixture core sections (sections 02–07), and the scalar portion of section 08 through its start of the unrelated field-energy appendix. I read the supplied main numerical checker in full and compared its mass matrix, projected jets, target/extras, power sums, parameter boxes, deleted Taylor moments, Bernstein conversion and grouped rational tail against the actual formulas. The conditional floor-matrix route and renormalized field/jellium appendices are not dependencies of this note and were not revalidated.

The inspected mechanism is checkable and does not assume the target optimality conclusion:

1. Compact spectral measures with node-independent variation bounds realize the unweighted ℓ¹ cardinal lists and all jets. The actual planar complex-Gaussian transform has the factor γ^(-1); uniform positive real parts give genuine Schwartz functions and Fourier involution, rather than a formal operation on a folded contour.
2. Positive degree-383 quadrature bounds exact spectral integrals by the stated Cauchy remainder uniformly in all required nodes/derivatives. The numerical arrays implement that exact quadrature and use strict Arb comparisons, not point samples of the continuum signs.
3. The finite paired block has inverse norm below 40. The full ℓ¹ Schur complement uses the small distant **output** bound δ and the possibly large finite-tail bound 4000; δ(1+40·4000)<1 is a genuine bounded inverse criterion. All omitted target and quadrature residuals are included in the full-list correction.
4. Near-node sign propagation deletes exact value/slope jets before estimating quotients. Containing parameter boxes, Bernstein positivity and analytic Taylor bounds cover whole intervals and every finite Gaussian parameter. The tail remainder has exact double zeros at the appropriate nearest node and a uniform second derivative bound; the positive sine-product/rational part dominates it on the same quadratic scale. This includes the origin, ties, exact nodes and the unbounded range.
5. The density-only LP proof compares finite measures with a larger disk. Its integrable Schwartz tail is uniform in every competitor location, and positive-definite Cauchy–Schwarz plus overlap dominated convergence gives the correct density factor. It removes exactly N_R diagonal terms. Gaussian complementation uses the dimension-two reciprocal coefficient and the rotated dual triangular lattice.
6. Positive mixtures use Fatou along every radius sequence and Tonelli for nonnegative finite sums. The shift is removed in the lattice series after the energy lower bound, not illicitly through the configuration liminf. Endpoint atoms and divergent cases are handled in the source.

For the retained Riesz specialization there is also a simpler independently checkable mixture: with p=s/2>1,

`t^(−p) = π^p/Γ(p) ∫_0^∞ α^(p−1) exp(−παt) dα`.

Applying the Gaussian lower bound along an arbitrary radius sequence, Fatou to these nonnegative Gaussian sums, and Tonelli to the nonzero lattice sum yields U_s directly. This confirms that no singular-kernel limit or measurable choice of auxiliary functions is hidden in the needed specialization.

For the atomic companion I read its actual theorem and normalization, inspected its reported full analytic audit, independently reran its exact finite checker, and read the independent rational/spectral diagnostic code/results. I did **not** reread all 2473 atomic manuscript lines or certify every atomic analytic lemma independently in this whole-package pass; the independently inspected main proof supplies the retained analytic route. The two manuscripts should not be described as independently kernel-verified by this review.

### Classical theorem, corrections and boundary

I inspected the primary Hardin–Saff PDF/text at definition (19), Theorems 2.1/2.4 and the full relevant s>d addendum argument. Its C_(s,d) is the ordered-pair unit-cube limit, H^d is normalized to unit planar-cube measure, and distance is ambient Euclidean. The smooth compact surface's finite chart cover satisfies the precise open-neighborhood bi-Lipschitz definition. Boundary charts extend to full neighborhoods; shrinking the extension makes its derivative uniformly close to a full-rank linear map, which gives a positive lower Lipschitz bound along line segments. Compact subcharts provide the required compact K_k. Smooth boundary is therefore allowed in this s>d branch. The no-boundary smooth-manifold hypothesis in the critical s=d branch is not imported.

The addendum's unrestricted unbounded-neighborhood wording would be unsafe, as the saved audit explains. The note does not use it: a finite union of bi-Lipschitz images of closed cubes is a compact d-regular thickening containing the chart pieces. In this compact setting the closure/positive-distance step is valid. The deletion count, separated near-K selection, projection to K and subsequent liminf inequality in the correction have the correct inequality direction. The cited corrected theorem thus gives precisely Z_s A^(−s/2) N^(1+s/2). The unit sphere has area 4π and chordal distance, giving Z_s/(4π)^(s/2).

I also checked the exact BHS2012 Conjecture 2/Proposition 1 and KS1998 Conjecture 1/energy definition from their primary texts. KS uses i<j; doubling its coefficient and covolume-normalizing its shortest-vector-one lattice gives exactly this note's sphere constant. The apparent BHS coordinate typo is avoided by the note's explicit correct basis.

## Priority, attribution and formal-scope review

I read the saved full priority/attribution audit and its source evidence manifests/citation metadata, inspected HSS2014 Theorem 3.2 and HLSS2018 Proposition 3.1 from the primary texts, and performed fresh web discovery queries for the exact planar hypersingular/OpenAI/C_(s,2) consequence. I searched the four pivotal family-090 companion source directories for the finite hypersingular constant/Hardin–Saff linkage. No exact duplicate finite/surface theorem with its proof was found there; the Coulomb companion concerns a different s=0 linear term. Current discovery results did not yield an already public exact duplicate. These are targeted checks, not an exhaustive novelty proof. No evidence justifies claiming firstness.

The final title, abstract, introduction, README and Zenodo description already credit OpenAI's theorem as the substantive input, HSS/HLSS as the reduction machinery, and Hardin–Saff as surface universality. “Resolves the d=2, s>2 case” is scoped as a consequence, not an independent base breakthrough. The wording repair R2 is needed to bring the supplement into this same disposition. The upstream September manuscript labels are not used as proven earlier public-disclosure dates.

I inspected the actual `OAI.AtomicTriangular.universal_energy_minimum` declaration, `Energy/Basic.lean` definitions and selected potential-transfer assembly, not the intentional-sorry Comparator as a proof. Definitions match locally finite sets, centered closed disks, ordered off-diagonal pairs, ENNReal lower limit, complete monotonicity and the covolume-one series. The final theorem has no optimality premise. The source-inspection/227-module scope audit is accurately limited in the package. I did not perform a full pinned Lean/Mathlib build, Comparator run or transitive axiom check; neither did the retained reports claim success at those steps. That absence is disclosed and is not replaced by “a Lean directory exists.”

## Independent clean reproduction and PDF review

I extracted the **actual reviewed ZIP** to an owned review directory and ran its own `reproducibility/reproduce.py`, with the exact pinned read-only upstream clone, Python 3.14.6, python-flint 0.9.0 and Tectonic. The runner's temporary copies stayed inside the dedicated effort. Receipt: `reviews/whole_package_review1_reproduction.json`.

All 34 pinned input hashes passed. The standalone TeX rebuilt successfully; its PDF was **byte-identical** to the deposit PDF (SHA-256 `79d21f3d...b27a3`). The main interval checker independently completed all 37,310 Bernstein and ten tail comparisons (exit 0); the scalar checker passed (exit 0); the atomic exact checker passed (exit 0). Main numeric elapsed time was about 93.45 seconds; atomic 3.85 seconds. There is no inferred success from file presence or static certificate metadata. I also independently ran the atomic checker once before this archive-based reproduction, with assertions enabled.

I visually inspected all five rendered pages of the actual exported PDF, checked equations/references/page breaks and PDF metadata, and found no clipping, overlap, illegible glyphs or broken citations. The two underfull bibliography warnings are harmless spacing and visibly legible. The PDF is an actual unencrypted downloadable file, not merely a native-editor preview. Author/title/subject metadata agree. Own artifacts are licensed CC BY 4.0 following the documented project default, while third-party sources remain linked/hashed and attributed rather than redistributed.

## What this review does not certify

This is an automated adversarial mathematical/package review, not human peer review or a formal proof. It supplies no statement about all microscopic minimizers, s≤2, subleading terms or other dimensions. It does not certify absence of every unindexed prior disclosure, nor does it establish first public priority. It did not stage/publish a Zenodo deposit or update the tracker, whose actual outcomes must be verified later. It did not modify candidate files, shared Git, upstream source, unrelated projects, or external services, and no individual was contacted.

Review-task completion estimate: 100% mathematical/package review performed for this exact candidate. Overall publication is **not** achieved by this review; R1/R2 must be repaired and a new complete-package review must assess the revised exact bytes.
