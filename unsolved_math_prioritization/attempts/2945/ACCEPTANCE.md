# Acceptance: KP-4.69 / 2945

Date: 8 October 2026. Disposition: **accepted unchanged as partial/unresolved, unsolved 5/5**.

This publication packages the complete original report and full independent mathematical audit. Their imported dependencies remain explicit. No original file is changed, no proof correction is required, and there is no newly claimed solution.

## Accepted mathematics

For the connected oriented Friedman–Witt–Kwasik–Schultz test family M = Y1 # Y2 and its separating twist tau:

1. The derivative of the separating twist is null-homotopic; the stabilized derivative obstruction cannot distinguish this endpoint.
2. The twist extends over every matching boundary-connected-sum filling by an explicit rotation of its joining handle. This does not establish extension over the cylinder with its bottom fixed.
3. The standard cover associated to G1 * G2 → G1 × G2 is a connected sum of (|G1|−1)(|G2|−1) copies of S²×S¹. Its natural lifted twist is smoothly isotopic to identity without an equivariance assertion. For the Dic_3 pair the degree is 144 and the number of summands is 121.
4. The endpoint problem is equivalent to a diffeomorphism of the two mapping tori preserving the specified parametrized, cooriented fiber. Their ordinary homology, Euler characteristic, and signature do not distinguish the test case. An unmarked diffeomorphism would be insufficient.
5. Supported relative Casson–Sullivan realizations on the finite-group pieces span the cylinder's entire relative obstruction group. Boundary-fixed maps act trivially on that group. Hence the obstruction of a chosen topological cylinder map can be cancelled without changing its prescribed endpoints. Existing stable smoothing results then give a diffeomorphism of the cylinder after some finite number of interior S²×S² stabilizations, with the same boundary values.

The fifth conclusion does not show that the number of stabilizations is zero, give a uniform bound, remove the new summands, or construct a diffeomorphism of the original cylinder. The original existence problem and the named unstabilized test case remain unresolved by this packet. Nonorientable possibilities are not excluded.

## Imported theorem and source boundaries

The topological cylinder map is an imported FW–KS result. The original Kwasik–Schultz paper was not obtained in full; the candidate and audit identify K3 and Galvin's thesis as the supporting statements. The original Friedman–Witt paper's narrower cases are not conflated with the later whole-family formulation.

Galvin's final v2 author manuscript supplies the Casson–Sullivan composition rule, relative realization construction, and stable smoothing input. The audit traces Proposition 4.10's relative incoming and lateral boundary markings to obtain the genuinely boundary-fixed map needed for extension by the identity. It explicitly discusses closed/compact wording inconsistencies and the source's instability-inequality typo. Supported excision and duality, triviality of the boundary-fixed pullback, and the fixed-boundary stable smoothing convention are separately justified. Realization uses finite groups of the pieces; no good-group theorem is applied to their ambient free product.

These are accepted mathematical dependencies, not theorems machine-proved by the arithmetic scripts. The source search is bounded and does not prove global openness, historical novelty, or the absence of an unindexed solution. The full source/proof qualifications remain in the unchanged [report](original/public/MATHEMATICAL_REPORT.md) and [audit](audit/AUDIT.md).

## Immutable evidence

- Original manifest SHA-256: `5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901`
- Original candidate tree SHA-256: `9373856af6e529c088f6df98cc42e147f3b8730e00494a90af7781e62d90cf83`
- Audit manifest SHA-256: `b07bc7e3914bf3f361f310c2a884199f32838bf3217346fc1346e1aa00985884`

The frozen audit records nine matching PDF identities, two matching corpus-file identities, one exact problem-record match, and absent corresponding research keys. The wrapper authenticates these historical records; it does not rerun their underlying PDF, text, visual-page, web, or corpus inspections. Fresh source and corpus bindings are explicitly **NOT_RUN**. Public titles, URLs, hashes, sizes, inspection history, and manuscript-status records are permitted metadata; no source bodies or datasets accompany them.

## Reproducibility contract

The externally authenticated bootstrap pins the exact publication manifest and verifier. The verifier hard-pins all accepted original and audit bytes in addition to validating exact recursive inventory, schema, path safety, and SHA-256/size pairs. Its checks remain active under normal Python, `-O`, and `-OO`.

On actual UID/EUID 1000 it copies only authenticated bytes to temporary read-only directories, confirms that attempts to change an existing file or create a file fail, and executes:

- The original exact checker, byte-for-byte against `EXACT_CHECKS.json`.
- The independently implemented matrix-ring/cycle-basis checker, byte-for-byte against `INDEPENDENT_CHECKS.json`.
- The original audit-bundle verifier against its external manifest pin.
- The entire unchanged audit harness: 36 child runs across normal, `-O`, and `-OO`, including 30 rejected semantic mutations.

The unchanged native harness preserves permissions with `copytree` while preparing its independent checker and mutations; those preparation writes require writable staging. The wrapper supplies a separate authenticated disposable writable staging copy for this preparation only. The supplied packet stays read-only, staging bytes are checked unchanged, and the harness then makes every actually executed specimen 0555/0444 and proves write denial under UID 1000. The native harness is therefore not represented as directly accepting an all-read-only source tree. An initial prepublication attempt with an entirely read-only source argument failed during preparation when adding `independent_checks.py`; that profile did not pass and is a harness limitation, not a mathematical failure. The published wrapper uses the disclosed staging flow, with exact staged-source inventory, byte-count, and SHA-256 verification before and after execution.

The full native receipt is compared to the historical receipt with exact value **and type** equality. Only the Python-version string and the complete stderr hashes of rejected children are normalized, because tracebacks include fresh temporary paths. The fresh version must equal the actual runtime; every failed child must still have return code 1, a nonempty hashed traceback, its exact historical `RuntimeError` final line, expected runtime identity/optimization, and the exact remaining receipt fields. No mathematical result, failure message, count, or disposition is normalized away.

The separately authored mutation driver rejects changed/missing/extra members, symlinks and special files, malformed schemas and numbers, self-consistent repinning of accepted evidence, and substitution of a wrapper behind the trusted external bootstrap. It also reruns after relocation from a genuinely read-only packet and hostile read-only working directory. Integrity success does not certify the geometric proof, any imported theorem, or novelty.

## Publication scope

This draft adds this source-free packet and changes only problem 2945's Status, Turns, and Findings cells in the existing full queue. All unrelated queue text, notes, and links are preserved. Source retrieval and audits earn no additional mathematical-turn credit. Publication does not authorize merging or releasing.
