# Reproduce the scoped PSC checks

Recorded environment: Python 3.12.14, SymPy 1.14.0. `requirements.txt` pins SymPy; dependencies are not vendored. Use an environment with that version installed. A different version can pass but is reported. The scripts need no source PDF, corpus, repository, secret, network call or external input dataset.

## Exact commands

From this directory:

    python3 -I -S -B verify_manifest.py
    python3 -I -B run_checks.py
    python3 -I -B -O run_checks.py
    python3 -I -B test_corruption_controls.py
    python3 -I -B -O test_corruption_controls.py

`-S` is valid for the standard-library-only manifest verifier. Do not apply it to the symbolic runner: SymPy must remain importable. `-I` isolates Python from environment variables, user site packages and script-directory imports; installed system/virtual-environment packages remain available. `-B` prevents bytecode writes. This is input/filesystem isolation, not an OS or network sandbox.

The manifest verifier checks the exact payload file inventory, byte counts and SHA-256 digests, rejects symlinks, and checks the frozen acceptance and unchanged-copy provenance records. Only MANIFEST.json itself is excluded to avoid circular hashing. Integrity against this manifest is not independent authentication.

The runner copies only verify_curvature_identities.py into a fresh temporary directory, then runs it normally and with `-O`. It requires zero exit status, empty stderr, exact JSON agreement against both shipped reference results, and no unexpected output files. It rejects assert statements in the four checker/wrapper programs. All validation uses explicit exceptions and is active under optimization. It never rewrites the references or package files.

## What is checked

The original self-contained checker computes Christoffel symbols, Ricci tensor and scalar contraction for the three-dimensional coordinate metric f(x)²(dr+a(x)dy)²+dx²+dy², and compares with the one-dimensional-fiber scalar formula. It also checks the conformal quotient identity for base dimension two, the dimension-dependent gradient coefficient m/(m−1), and the slow-cylinder formula specialized to a general warped product. SymPy simplification returns exact zero for all four residuals. No floating-point tolerance is used.

These are symbolic sanity checks of an explicit coordinate family and algebraic coefficients, not general geometric proof certificates. In particular they do not establish the full normal deformation, boundary gluing, classification, or imported surgery theorems by computer. Those arguments and hypotheses are in the authored reports and independent mathematical audit.

## Negative controls and recorded runs

`test_corruption_controls.py` makes disposable package copies and tests five mutations in both execution modes: a same-size manuscript byte change, missing file, extra file, wrong saved reference JSON, and a wrong symbolic scalar-curvature coefficient. Each must fail with its expected diagnostic. It modifies neither the package nor the original research files. The wrong-reference test changes both references consistently, so rejection depends on comparison with a fresh computation, not just disagreement between references. The wrong-coefficient test invokes the symbolic guard, not merely the manifest hash.

REPLAY_VERIFICATION.json records normal and optimized outer-wrapper runs, each of which also runs normal and optimized children. CORRUPTION_CONTROLS.json records both outer execution modes and all ten selected mutations in each. These outcomes can be regenerated from the frozen package with the commands above. Both manifest modes and both complete replay modes were checked again after final manifest generation.

## Historical evidence boundary

SOURCE_METADATA.json, SOURCE_CHECKS.json and CORPUS_VERIFICATION.json are historical public verification metadata. Their PDF/corpus hash values are not re-fetched or recomputed by these replay commands; no third-party source text or dataset contents are shipped. SOURCE_GATE.md documents inspection depth and temporal search limits. PROVENANCE.json records byte-for-byte preservation of the original authored files. AUDIT_ACCEPTANCE.json freezes the exact accepted report versions.

Overall status remains **UNSOLVED (five avenues)**. Successful replay does not turn the partial results into a solution of the original question.
