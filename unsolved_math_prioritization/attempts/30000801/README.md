# Fourth-order Navier strong quantization: audited conditional result

**Problem 30000801 / OWR-1591-003, rank 816: unsolved, 5/5 approaches.**
Independent acceptance is **ACCEPT_CONDITIONAL_RESULT_ONLY_FULL_TARGET_UNRESOLVED**, with no mandatory mathematical correction. This package does not solve strong quantization at arbitrary energy and makes no novelty claim.

## Accepted mathematics and exact limits

The equation is Delta²u_k = lambda_k u_k exp(2u_k²) in dimension four, with positive spatially constant lambda_k tending to zero and Navier data u_k = Delta u_k = 0. The quantum is Q = 16pi². The catalog's legacy nonlinearity is inconsistent; its corrected statement matches the original source.

The [authored proof](author/PROOF.md) and [independent mathematical audit](audit/MATHEMATICAL_AUDIT.md) establish n0 = m²/Q under an exterior logarithmic profile in C³ and a finite primitive-mass limit that is the same on every sufficiently small fixed-radius ball. A specified finite bubble family with strictly positive, finite normalized height weights and both weighted-mass exhaustion identities then has exactly one bubble. These additional assumptions are explicit and are not derived here from the original Navier hypotheses.

Integer energy quantization is weaker than the target L=I. Relative-scale separation allows selected centers to share a limiting location, so selected profiles, spatial points and all bubble-tree levels cannot be identified. Ordinary no-neck energy does not supply weighted no-neck. The elementary consequence for 0<Lambda<2Q gives L=I=1 only in that low-energy regime. Algebraic and nonnegative-measure controls are not PDE counterexamples.

See the [acceptance report](audit/INDEPENDENT_AUDIT.md), [five approaches](author/APPROACHES.md), [source scope](author/SOURCE_AUDIT.md), and [current verdict](VERDICT.json). Finite symbolic checks support the written audit; they do not prove missing analytic estimates or provide formal proof-assistant certification.

## Unchanged freezes and source limits

The 11 author members, 10 audit members and both safe ZIPs are byte-for-byte unchanged. Author ZIP: 22,361 bytes, SHA-256 45ab3bf6abaa90e865cba7899a509de3a8343ab44b32bb09dbbad7ccd9f46434. Audit ZIP: 24,188 bytes, SHA-256 326136d76eb46725806875d906dc6bb19833f9e8de17ab45d33d8143a0dad1bf. Preparation-stage no-publication and pending-audit language remains historical to each freeze.

The author checker accepts deliberately resealed catalog-rank and well-formed PDF-digest changes. The independent external ZIP pin rejects those modified artifacts; a resealed manifest is not the accepted freeze. Offline PASS is not live verification of a cited PDF. The audit inspected targeted source statements, not every paper's entire proof, and its bounded literature search is not a guarantee of worldwide completeness or present-day global openness. Public source metadata records retrieval limits and manuscript versions. Historical full-source results remain historical; fresh results are recorded separately in PUBLICATION_TEST_RESULTS.json.

## Reproduction

Python 3 and SymPy 1.14.0 are required. From this directory:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 verify_package.py --adversarial

The verifier checks the complete inventory, sizes and hashes, exact ZIP identities and member equality, and normal/optimized author and independent checks. Adversarial mode runs 24 original mutations, 36 additional mutations, four archive corruptions, ten audit-inventory corruptions, and relocation controls. Optional corpus/PDF replay, including source-corruption controls, uses:

    python3 verify_package.py --adversarial --inputs /path/to/catalog.json /path/to/problems.json /path/to/reports.json --pdf-inputs /path/to/owr.pdf /path/to/struwe.pdf /path/to/robert.pdf /path/to/martinazzi.pdf

Omitted external inputs are explicitly NOT_REQUESTED, never PASS. The inventory excludes its own manifest; compare its hash or the package to a trusted Git commit or receipt. These checks do not protect against a malicious replacement of all code and pins and do not prove the missing analytic hypotheses.

Only this target row's Status and Turns change to unsolved and 5/5. Every other queue byte, including the preexisting header, is preserved. No global queue/state regeneration is performed. Only authored mathematics/code/audit/results, public verification metadata and the two intact safe archives are added. Source PDFs, extracts, corpus contents, private sources and private coordination are excluded. Draft review only; no merge, release, DOI or outreach.
