# A sharp dyadic threshold in a characteristic-two random-cone construction

This note refines the exact October 4 OpenAI construction. Its new result is model-specific: q=32 is the least dyadic q>=4 for which the unchanged seven-extra squared turn weights have exponential word-mass decay. Exact rational positive-vector certificates prove contraction at 32 and exponential growth at 4,8,16, independently of the allowed inverse pairing. Propagating the source estimates gives its asymptotic random-cone construction on a 532-edge rose instead of 8260. The lower-order obstruction concerns this decay criterion, not nonexistence of other constructions.

The idempotent and projective-cancellation consequences were already stated in the author's public triage, conditional on auditing the source; they are inherited and accurately attributed. Classical HNN embedding supplies a two-generator finitely presented torsion-free host with a finite two-dimensional classifying complex. This is no global 532-generator optimum, new embedding theorem or independent discovery of the base counterexample.

For every characteristic-two field K, S=K[H] contains a scalar idempotent e=1-ba other than 0 and 1. P=eS is a nonzero cyclic projective right module, S is isomorphic to S direct-sum P, and [P]=0 in K_0(S). A zero class does not make P zero. No characteristic-zero, odd-characteristic, reduced-C*-algebra or matrix-only conclusion is asserted.

## Files

- main.tex: standalone source with bibliography, supported by the native LaTeX editor/compiler.
- paper.pdf: exported downloadable preprint, separately uploaded from the source archive.
- verification/verify_parameter.py: exact rational matrix, degree, capacity and expansion certificates.
- verification/verify_plane32.py and data/plane32_incidence.json: finite F32/PG(2,32), Fano types and inverse-letter certificate.
- verification/verify_embedding.py: exact formal word identities for the classical HNN encoding.
- verification/verify.py: original source's Fano/contraction and abstract-ring boundary checks.
- notes/EXTENSION_PARAMETER_AUDIT.md, notes/EXTENSION_PARAMETER_FALSIFICATION.md, notes/EXTENSION_PRIORITY_ATTACK.md and notes/EXTENSION_EMBEDDING_AUDIT.md: exact extension audits.
- reviews/source_combinatorics.md and reviews/source_topology.md: independent detailed audits of the original probability and cone-picture arguments.
- notes/PRIORITY_AUDIT.md and notes/CLASSICAL_PROVENANCE_AUDIT.md: primary provenance and affirmative duplication evidence for the original core.
- sources/SOURCE_MANIFEST.json and sources/PRIORITY_SOURCE_MANIFEST.json: precise upstream and primary-source identities/hashes. Research-only source copies are excluded from the deposit.
- CURRENT_THEOREM.md, DEPENDENCY_LEDGER.md and APPROACH_TABLE.md: claim scope and validation basis.
- LICENSES.md and LICENSE_CODE.txt: rights for newly authored material and retained upstream license notice.

The historical core-only candidate and its two complete reviews remain preserved in versions/duplicate-core-candidate2 and reviews/package_review_one.md /package_review_two.md in the repository. They do not certify the changed refinement package. Its complete-package review reports, response records and exact manifests are retained separately in reviews/ to avoid self-referential archive hashes. See the project repository for current publication and review status; this archive's contents remain frozen at the reviewed version.

## Reproduction

Run python3 verification/verify_parameter.py, python3 verification/verify_plane32.py, python3 verification/verify_embedding.py and python3 verification/verify.py from this folder. All finite certificates use only the standard library. Plane data are reconstructed exactly and compared byte-for-byte with the companion JSON. These computations do not produce a random matching or verify a target group-ring multiplication.

Run python3 verification/reproduce.py with Python 3.10+, Tectonic, pdfinfo, pdffonts and pdftotext available. The script creates missing output directories, performs all four checks, builds main.tex in a clean project-local temporary directory, exports paper.pdf, and records versions, source/PDF hashes and fonts in receipts/clean_reproduction.json. The native compiler is independently available in the desktop editor. The tested environment is Python 3.14.6, Tectonic 0.16.9 and Poppler 26.08.0. Render the PDF with pdftoppm for visual checking. Build timestamps may change PDF bytes across runs.

To inspect the pivotal dependency, obtain OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a and compare its exact files with the source manifest. See the manuscript's linked references. The source audit is proof-based and automated; compilation is a document check. Earlier family 197 Lean declarations have torsion and do not verify the October 4 input. No Lean build or full formalization is claimed.

The matching outcome and sufficiently large parameter m are existential. A finite tree-relator and scalar-sum recipe is supplied, but no numerical matching, numerical presentation, reduced idempotent support or multiplication certificate is claimed. The finite incidence data certify only the label model.

## Author and disclosure

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. No affiliation or coauthor is inferred. AI tools were used extensively in research, drafting and verification, including independent automated adversarial reviews. This preprint has not undergone conventional human peer review or refereeing. The upstream AI-produced construction is attributed to OpenAI according to its supplied citation. No first-priority or endorsement claim is made.
