## Mathematical PASS within scope; FORMAL REPRODUCIBILITY HOLD

This AI-assisted authored audit finds no mathematical gap in the prior
Tokengrinder argument for irrationality of sum sigma_k(n)/n! for every integer
k >= 0. Credit remains with the prior author. The complete seven-step
reconstruction is retained without mathematical changes: exact factorial-tail
integrality, the scaled Stirling remainder, progression means including k = 1,
a fixed coprime finite-difference grid, squared CRT moduli, the isolated-shift
contradiction, and the separate positive-tail proof for k = 0.

The target is the ordinary convergent divisor-power factorial series. The
proof uses ordinary CRT progressions and no simultaneous-prime-values
hypothesis; no uniformity in k is needed. No new proof, novelty, priority,
external human peer review, journal acceptance or formal certification is
claimed. This audit edition is unrefereed.

FORMAL REPRODUCIBILITY HOLD remains uncleared. No independent Lean build,
transitive compiler/dependency/kernel closure or final-theorem axiom report
has been obtained. No fresh kernel replay or second-kernel verification was
run. The author's reported compilation and axiom results retain their
attribution. Static inspection and finite tests are not compiled verification.

The audited public claim is pinned at
[46b9fd26361faf669bcd7e4495e63678bfa6a735](https://github.com/tokengr1nder/Erdos252/tree/46b9fd26361faf669bcd7e4495e63678bfa6a735).
The complete [20-page manuscript](https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/PROOF.pdf)
and 60,831-byte main Lean module were read in the recorded audit. Ten direct
Mathlib imports were retrieved at official revision
0df444a360eaa60ab8c11dca51a86af692955474. The toolchain pin is Lean 4.33.1,
and the eight inherited package pins agree with the official mathlib manifest.
This is not a transitive source, compiler-binary or olean audit.

The [author verification boundary](https://github.com/tokengr1nder/Erdos252/blob/46b9fd26361faf669bcd7e4495e63678bfa6a735/VERIFICATION.md)
states that a clean-machine dependency download was not separately tested.
The advertised SHA256SUMS path returned 404 at the pinned commit. This is a
metadata/reproducibility defect, not a mathematical counterexample. The
main-source hash agrees with the value printed on manuscript page 20.

Historical exact finite checks passed under normal Python, -O and -OO with
identical recorded outputs: 630 divisor/phase cases, 972 Stirling-error cases,
819 polynomial-tail cases, 7,200 affine-count cases, 16,200 prime-refinement
cases, 7,873 coprimality pairs, 326 grouped cancellations and four negative
controls. These bounded checks corroborate identities and indexing; the full
written argument supplies the general mathematical reconstruction. Edition
preparation did not rerun mathematical test programs, execute Lean or external
proof code, install software, or retrieve/inspect new scholarly sources.

Public metadata preserves source versions, hashes, sizes, titles, URLs and
historical retrieval/inspection boundaries. Historical papers were checked
for relevant statements and hypotheses, not independently audited in full.
No exhaustive current-literature or priority certificate is claimed.

Exactly seven authored audit/acceptance and public metadata files are proposed
as additions under unsolved_math_prioritization/attempts/2009/. The full
substantive audit is preserved, with tracked editorial framing and historical
labels. This prose-only edition excludes copied PDFs/source extracts,
Lean/library code, executable programs, detailed test outputs, raw datasets,
private sources, personal data and private coordination material.

## Exact public-file identities

- `ACCEPTANCE.md`: 2,937 bytes; SHA-256 `8e6c284ce0458dc3b03b6e545abd293288f424e8945aa0b21590d57a59cc9f44`.
- `MANIFEST.json`: 1,662 bytes; SHA-256 `708a0fbef29592689cd17b9b5b2e79c32a6c8b279f359aca4d30c9c65724a59e`.
- `MATHEMATICAL_AUDIT.md`: 19,076 bytes; SHA-256 `4facc22f43a1c62318351decf66c5b6eade8996f52501782c04081492df50fb3`.
- `README.md`: 3,655 bytes; SHA-256 `3ebf94e2e7fd87474a4a53e8d0c99e1112d94beac91735e6ae04c8ac71d512b1`.
- `SOURCE_METADATA.json`: 12,722 bytes; SHA-256 `1821335550c23561d185e3077ae590e2ef2c348e3ed6ba6812677fbb169a406f`.
- `STATUS.json`: 1,732 bytes; SHA-256 `c4cb9ca070845376ec8937eafb3cdb970f820114a32e5c975e4bf3014bbdc386`.
- `VERIFICATION_SUMMARY.md`: 3,389 bytes; SHA-256 `3b062efbb3e82d28813fa12f2ecb3fc380157cb0e3c66022d46eea41c40e40b6`.

MANIFEST.json lists all seven members and hashes the other six; this body independently pins its digest.

