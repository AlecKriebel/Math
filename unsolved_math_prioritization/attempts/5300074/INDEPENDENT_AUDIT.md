# Publication context for the independent audit

The complete authored mathematical audit follows unchanged. Its execution paragraphs describe the earlier audit stage, not a fresh replay by this publication. The historical runner, original full report, historical execution receipts and source bodies are omitted. The historical runner command at the end is archival context and is not an entrypoint supplied here. Their replay and historical patch application are NOT_RUN. The current entrypoint is authenticated BOOTSTRAP.py, with full-count/no-skip guarded verification documented in CHECKS.md.

The accepted current mathematical report is RESULT.md, SHA-256 b1cbc9b5b77060b8ba57faabcd7927d49df6579a1381ef6dea95b750a2790be1. The authored correction patch is historical context only; removed text is superseded. The problem remains exhausted at 5/5 approaches, with disconnected neutral-boundary continuity and initially accessible indifferent-point compatibility unresolved.

# Independent mathematical and reproducibility audit

Target: 5300074 / AMR-052-0074. Audit date: 8 October 2026.

## Verdict

**Accept the reviewed packet as partial results only.** The strictly repelling continuity argument survives the audit after the proof expansions specified below. The original question is neither solved nor disproved. The remaining neutral-boundary limit for disconnected Julia sets, together with compatibility at an initially accessible indifferent point, remains open in this packet. The five-approach stopping point is preserved; this audit completes and checks existing arguments rather than introducing another strategy. No novelty or complete prior-resolution claim is accepted.

The original RESULT.md has SHA-256 eff6ed1cb24828829c9c48956a0af61315662df7da3db10b0705c49c96ca8c24. All original files, including their modes, were preserved. The reviewed RESULT.md and CHECKS.md contain the clarifications, and their exact hashes are recorded in the reviewed packet manifest.

## Corrections and required clarifications

1. **Finite rotation sets.** Levin's definition permits forward invariance. A finite forward-invariant set need not be permuted: doubling sends both 0 and 1/2 to 0. The cyclic-shift/cardinality formula is now expressly restricted to finite sets on which the map is a cyclic-order-preserving permutation. The landing sets used here have the required finite-cycle property. This clarification does not change Lemmas 2.1-2.3.
2. **The inverse image is a component.** In Proposition 3.2, V_t is the inverse-image component containing the marked point, not the full polynomial inverse image. Levin's construction is applied to the open domain V_(dt) and its specified inverse branch, rather than to an ambiguously named closed inverse image.
3. **Persistence requires derivative control and component identification.** The expanded proof derives joint spatial smoothness at positive potential from a common Böttcher domain after a finite iterate. It then persists the Jordan boundaries, identifies the enclosed sublevel components by the maximum principle, and preserves the degree-one map using a uniformly univalent disk. The inverse branch contracts after a Riemann-map normalization. No continuity of the filled Julia set is assumed.
4. **Collision angles are handled one-sidedly.** The expanded argument uses only fixed compact positive-potential ray segments. Parameter persistence for each collision-free angle follows by the nonsingular ODE and isolation of the relevant level component. Density at exceptional angles follows from PZ's one-sided uniform convergence and separation of distinct regular level components. Neither arbitrary turns nor continuity of complete landing rays is substituted for that argument.
5. **Wringing must be normalized explicitly.** Levin's section 4 develops an invariant-Beltrami construction with an additional fixed-slope parametrization. The pure shear in the packet is not obtained by setting that parametrization's stretching factor to 1 while keeping a free twist. The reviewed proof instead writes the shear directly, verifies its dilatation and commutation, integrates the invariant structure, establishes convergence by normalized quasiconformal compactness, and rescales its conformal coordinate to obtain an exactly monic marked family. This proves the stated critical-orbit angle shift rather than leaving a normalization factor unexamined.
6. **Enumeration is not a distinct-orbit count.** The original 616 cases are correct but include repetitions across rational grids. There are 150 distinct pairs consisting of the degree and angle set. CHECKS.md now says so. The numerical verifier itself required no repair.

These are proof-completeness, convention, and reporting corrections. No counterexample to the scoped continuity theorem was found.

## Claim-by-claim decision

- **Lemma 2.1, bounded-slope extension: accepted.** For ordered lifted points at distance less than 1, monotonicity gives a lift increment in [0,1]; congruence with multiplication by d rules out a negative integer correction. The resulting increment is at most d times the input distance. Affine interpolation on gaps retains that bound, including the one-point case. Longer distances follow by subdivision/periodicity.
- **Lemma 2.2, translation-number continuity: accepted.** Monotonicity and degree one bound the displacement oscillation of every iterate by 1. The superadditive/subadditive bounds give the translation number and the claimed finite-iterate error. Uniform convergence of a fixed number of iterates then yields continuity. Nothing relies on invertibility.
- **Lemma 2.3, abstract Hausdorff compactness: accepted.** Equicontinuous normalized lifts have a limit agreeing with multiplication by d on the limiting set. Forward invariance passes to the Hausdorff limit. The lemma does not identify such a limiting set with the landing set of a limiting polynomial.
- **Proposition 3.1, local constancy at a smooth periodic access: accepted.** The cited stability theorem expressly allows disconnected Julia sets but requires an ordinary rational ray landing at a repeller. Broken rays and neutral multipliers are not covered. Continued marked fixed points are indeed 0 in this family.
- **Proposition 3.2 and Corollary 3.3, continuity on U_d: accepted in the expanded reviewed version.** The construction uses a persistent univalent sublevel pair and only one-sided positive-level persistence. Every limiting circle extension agrees with the original landing set, which is enough to identify its rotation number. An unproved upper semicontinuity theorem for landing sets is not used.
- **Section 4, uniqueness for either convention: accepted in the expanded reviewed version.** The generalized domain contains U_d. For the smooth convention, the shear moves each of finitely many critical-orbit angles with a nonzero slope; countably many forbidden parameters suffice to remove all broken periodic rays. The finite/Cantor dichotomy then gives a smooth marked access. Continuity of coefficients, rather than invariance of the multiplier under a quasiconformal map, keeps the point repelling. Density implies at most one extension, not existence.
- **Section 5, connected neutral-boundary limit: accepted.** Squaring the connected Yoccoz disk gives the stated circle-distance bound. The logarithm branch is harmless after passing to R/Z. The disconnected disk has the access-angle denominator; no uniform bound is silently imported, and the irrational zero-access case remains excluded from that estimate.
- **Section 6, failed multiplier shortcut: accepted.** Exact coefficients yield a second fixed-point multiplier -i/2 and centered parameter 1/16-i/4. The connected quadratic has its fixed angle-zero ray landing at the marked repeller, giving rotation zero although the multiplier argument is nonzero. The topological retraction does not repair that mismatch.
- **Section 7, remaining gap: accepted as a scope statement.** It expressly retains both disconnected neutral-boundary continuity and initially accessible indifferent-point compatibility. Neither the exact tests nor abstract compactness settles them.

## Primary-source verification

The four declared PDF byte counts, hashes, and page counts match the local source files. Their public URLs were independently opened and their identities checked. Critical formulas and conventions were also visually checked; this is not a claim of a new byte-for-byte publisher download or an independent proof of every cited theorem.

- [Bielefeld, Conformal Dynamics Problem List](https://www.math.stonybrook.edu/preprints/ims90-1.pdf), printed page 8: the family, unrestricted Julia connectedness, initial ray-landing domain, uniqueness question, and required unit-multiplier value agree with the packet. The short original question does not settle the smooth/broken convention separately.
- [Goldberg-Milnor, Fixed points of polynomial maps II](https://www.numdam.org/item/10.24033/asens.1667.pdf), Appendices A-B: the generalized rays are prescribed one-sided limits; Lemma B.1 stabilizes a smooth rational landing ray at a repeller. Example B.3 permits the full portrait to gain rays. It therefore supports local constancy of rotation but not equality of all landing-angle sets under perturbation.
- [Levin, Disconnected Julia set and rotation sets](https://www.numdam.org/article/ASENS_1996_4_29_1_1_0.pdf), printed pages 6-9: Proposition 2.3 supplies the finite-interval extension for a singleton repeller with a self-inverse-branch domain. Section 4 supplies the invariant-structure method. Section 5 states the connected disk and the disconnected disk with access angle; Remark 5.1 gives zero access angle in the irrational case. The reviewed shear calculation is explicit rather than attributed as a verbatim source specialization.
- [Petersen-Zakeri, Periodic Points and Smooth Rays](https://arxiv.org/pdf/2009.02788), introduction and sections 2.2-2.5: the finite/Cantor landing dichotomy, nondegenerate-component smooth-access theorem, finite positive-level collision set, and one-sided uniform ray convergence are the precise ingredients used. The Levin-Przytycki theorem is accepted through this explicit modern restatement and attribution; the original LP article has not been independently proof-audited here.

## Exact verification and mutation testing

The original five-test suite passed normally, with -O, and with -OO. Each run reported 616 cases. The code contains no Python assert statements or floating-point literals and imports only fractions, math and unittest. Its tests are arithmetic checks, not analytic proof certificates.

A separate exact verifier passed four tests in each mode:

- an integer-modular orbit enumeration independent of the tested implementation: 616 cases and 150 distinct degree/set pairs;
- every invariant nonempty subset of grids with denominators 2 through 12 in degrees 2 through 6: 238 accepted rotation sets, 423 rejected non-rotation sets, with exact affine/degree-one/orbit checks;
- the shear's Beltrami-modulus identity and commutation with multiplication by the degree;
- the translated quadratic polynomial identity at exact rational-complex inputs.

Eleven semantic mutants were tested, each in all three optimization modes. All 33 guarded mutant runs failed through active test failures/errors, without syntax/import failures:

1. external angle substituted for the rotation number;
2. reversed rotation number;
3. wrong affine-gap denominator;
4. omitted degree-one translation increment;
5. truncation toward zero instead of floor at negative inputs;
6. removed affine interpolation;
7. one too few iterates;
8. wrong centered-parameter sign;
9. wrong other-fixed-point multiplier sign;
10. missing disk cross-term factor;
11. reinstatement of the erroneous negative fixture {1/15,2/15,4/15,8/15}.

The last set really is a rotation orbit, so rejecting it is correctly detected as a test failure. Mutation testing here does not measure coverage of the analytic proof.

## Actual read-only execution

Guarded runs used real uid=euid=1000, not root. Target files had mode 0444 and target directories mode 0555; the effective user had no write access. Opening the target for update and creating a new file in its directory both raised EACCES (errno 13). A Python runtime audit hook then rejected attempted writes, filesystem mutations, socket operations, and subprocess creation. The original suite, independent suite, and all semantic mutants were run under that guard in all three modes, using -B to suppress bytecode-cache writes. Original contents and modes were rechecked after the work.

Public deliverables contain only authored mathematical text, source metadata, exact verifiers, and verification results. Third-party PDFs/extractions, source-page images, and private execution material are not included. Nothing was published or changed remotely by this audit.

To reproduce all 39 guarded runs (3 original, 3 independent, and 33 semantic-mutant runs), run `python3 -B run_independent_audit.py` from the reviewed packet directory as a nonroot user. The controller creates temporary copies; only its tested child processes are claimed to be read-only. Results are emitted as JSON on standard output.
