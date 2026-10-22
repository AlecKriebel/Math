# A negative answer to Nevo's homology-sphere decomposition question

Alec Kriebel · ORCID0009-0001-9320-500X ·17October2026 · extensively AI-assisted and unrefereed.

The research note gives a finite pure two-dimensional abstract simplicial complex K which is doubly Cohen–Macaulay over every characteristic-zero field and contains no two-dimensional homology-sphere subcomplex over any field. This negates Nevo's OWR17/2005 Problem8 (printed961) and published DCG39(2008) Problem3.7 (printed417), before any overlap or reordering requirement. The standard homology-sphere convention includes every face link. The finite geometry uses F11, whereas the CM coefficient field has characteristic zero. No all-characteristics CM, subdivision, immersion or global-homology-only claim is made.

## Files and reproduction

- `main.tex` and `output/pdf/spherefree-doubly-cm.pdf`: operative complete paper and pinned compiled PDF.
- `output/spherefree-doubly-cm-source-and-verification.zip`: paper source, labelled historical PR inputs, root reproduction, three full mathematical reviews, three priority reviews, source/version metadata and portable verification.
- `output/zenodo-upload-kit.zip`: identical PDF/source ZIP and exact metadata with portable deposit paths.

Extract the source archive and run `python3 -B verification/verify_all.py`. It uses the standard library, requires no network, and writes nothing. It authenticates the frozen authored inventory and PDF/source QA, compares both complete745-byte positive outputs in normal and optimized modes, and reproduces three actual wrong constructions in each mode: six failures. The diagnostic constructs all133 points and133 lines of PG(2,11), all17689 Gram entries and all266 single deletions; a seven-vertex torus checks rational H1 and exact weighted energy at the strict spectral boundary. These checks do not enumerate K or establish building theory or the universal proof.

Optional `python3 -B verification/optional_matrix_diagnostics.py` needs NumPy and runs only normally; it refuses optimized mode because its mathematical checks use assertions. It checks133 generators, inverse polynomial matrices and70756 neighbor-pair adjacencies. Default behavior prints only and never overwrites historical receipts. Optional output must be a new external file. The default verifier does not run this optional program or historical family programs.

Run `python3 -B build_package.py` to deterministically rebuild both archives from fixed publication members and `verification/AUDIT_MEMBERS.json`. The PDF is a frozen input, not recompiled by this rebuild. Compile `main.tex` separately with ordinary TeX; engine and time differences need not reproduce frozen PDF bytes. `SOURCE_MANIFEST.json` pins every other source-archive member; the external archive checksum/DOI supplies authenticity. The local guards reject unsafe paths, symlinks, nonregular files, duplicate JSON keys and incomplete inventories, and are not a concurrent-adversary sandbox. Optional `python3 -B verification/self_test.py` uses disposable synthetic packaging fixtures; it is separate from the mathematical proof and real PDF QA.

The original13 PR files in `inputs/` and their old audit prose are a historical edition dated10October2026. The complete paper and new verification package are operative. Historical absent programs are not represented as rerun. Third-party bodies, extracts, renders and raw service returns are excluded. Public custody receipts may pin private evidence: complete source-custody checks require obtaining those sources and are outside offline verification.

## Prior credit and review boundary

The LSV affine building/lattice/faithful polynomial representation is an essential imported theorem. Degree-versus-congruence displacement already appears in Lubotzky–Meshulam Proposition3.3; the note proves its own matrix reduction modulo the nonreduced ideal (t^9). Garland-type normalized link vanishing and the curvature/Euler obstruction are established mechanisms, credited to Ballmann–Świątkowski and Januszkiewicz–Świątkowski. The note checks the precise deleted-link and same-dimension CM conditions needed for Nevo's question.

Root and three fresh priority approaches found no earlier recorded full answer in inspected accessible material. Their176 query inputs contain167 exact distinct strings, with conceptual/work overlaps; this is not a unique-work count. No firstness, causal-independence, exhaustive-search or continued-global-openness certificate is claimed. Material unread full-body leads include Chari1997 and Baclawski1982. Other original papers, books, theses, versions and subscription indexes remain uninspected. Exact selective reading scopes and near matches, including recent numerical/algebraic consequences, remain in the authored audit records.

Three source-first full mathematical reviews independently checked the supplied candidate across distinct mechanisms. Root's original-body/outline exposure and the supplied-source basis of the reviews are disclosed. These are internal AI reviews, not external human peer review, journal acceptance or formal verification. AI tools were extensively used in development, writing, research, computations and adversarial checks. This preprint is unrefereed.

Fresh whole-package reviews and later production receipts are separate gates outside the frozen archive, avoiding circular self-attestation. The repository production uploader is `zenodo_deposit_tool/zenodo.py`. Kit and production metadata are identical; only relative payload paths differ. Reconcile an uncertain deposit or tracker append read-only before retrying. No GitHub release is required.
