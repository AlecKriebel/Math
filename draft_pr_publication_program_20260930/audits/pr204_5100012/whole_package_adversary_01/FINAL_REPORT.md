# Whole-package adversarial review 01

UTC completion: 2026-10-16T10:58Z. Review completion estimate:100% of the assigned bounded audit. This does not assign a probability of universal correctness or publication novelty.

## Result and issue disposition

**No substantive issue found in the frozen current publication package.** No P0/P1/P2/P3 correction request is raised. This is a fresh source-first adversarial audit, not acceptance of earlier favorable reports. It is not publication authorization, a readiness gate, human peer review, a proof-assistant certificate, or a novelty/priority/independence certification. Root must make any subsequent disposition.

The strongest checked result is the qualified theorem stated in the current paper: proper strictly nested confocal elliptical caustic, noncircular boundary, physical least N>=3 odd or divisible4, all admitted coprime windings and both orientations, signed ordered shoelace areas and center feet on complete original sidelines. The analytic reasoning closes that claim without using finite checks as a universal proof. No exact remaining mathematical gap was identified in that scoped argument.

## Independence and sequence

SOURCE_FIRST_PLAN.md was frozen at2026-10-16T10:47:28.426323Z before opening the candidate manuscript/proof or favorable reports. Its SHA256 is968704a35504eb87721af5b8e234a51a4ebb11a0a148b9d1599c793d5545dd4b. I next read the original arXiv/journal table definitions and Stachel theorem, recorded SOURCE_FIRST_ASSESSMENT.md and froze445 immutable input records, then read the candidate. I did not import prior audit conclusions as authority. Candidate exposure after the source assessment is disclosed; this is independent verification, not independent discovery.

I wrote only authored review artifacts in this assigned folder. I used no Git/index/ref/branch/checkout commands, changed no package/native/main/QUEUE files, made no editor/UI changes, installed/copied no dependencies, cleaned no shared caches and communicated with no outside individual. Internal coordination was limited to Root. New Root operational files that appeared outside the sealed package during review are enumerated separately in IMMUTABLE_INPUTS_AFTER.json and were not treated as review authority.

## Source problem, mathematical proof and falsification

The arXiv v11 Table3 p6 and journal Table3 p346 specify k203,b as signed A A_m, M=O, N not2 modulo4, with proof/value unknown there. The table does not literally specify physical least period. The current paper explicitly presents the least-period qualification rather than silently attributing it to the table.

ANALYTIC_REVIEW.md contains the independently checked chain:
- Stachel journal Theorem4.3 gives the full canonical scope, coprime star winding and real physical least period.
- Substitution proves the actual contact line and center foot; no boundary tangent or clipped-segment substitution is used. Real projection denominators are positive.
- A=C_A S has the correct shoelace1/2 and endpoint-count factors.
- The reduced real lattice has m=N or N/2 and multiplicity N/m. Equal residues cannot cancel. S has exactly the two stated simple poles; symmetry and divisor degree give exactly the two stated simple zeros.
- Adjacent pedal-area terms cancel the apparent double pole. The N3 and N4 cases and antipodal even-N multiplicities are included, without overlapping incident-edge grouping.
- The quarter-shift/Laurent calculation gives C_T=alpha² sn(delta)(dn(delta)+k'²)/(1+dn(delta))²>0, with correct sign and units.
- The parity shift is a half-period precisely in the target classes. For excluded primitive N=2 mod4 it is a full period, yielding the genuinely nonconstant C_A C_T S².
- Reversal negates both signed areas. Positivity justifies absolute values of those shoelace areas, while no unweighted star-face claim follows.
- Circle, collapsed-caustic, hyperbolic, nonconfocal, arbitrary-point and clipped-foot extensions are outside the theorem. Circle limiting behavior is consistent.

Own exact script independent_checks.py verifies the two displayed H/J six-orbits from their coordinates, including outer membership, tangent discriminants, interior caustic contacts, forward normalized reflection, six distinct vertices, complete-line perpendicular feet and signed shoelace sums. It reproduces A B=14000/729 and14336/729. Double traversal scales each area by2 and the product by4, so the twelve-entry products differ by448/243 while least period stays six. Thus the repair/qualification has a concrete physical counterexample.

Additional own checks cover38,057 coprime arithmetic configurations through N500 and24 modulus/period/star configurations with k=1e-6,0.63,0.9999, complex phases and near-pole residues. They passed. These are finite exact arithmetic and noninterval numerical diagnostics, explicitly separate from the analytic proof.

## Attribution, overlap and chronology

I freshly read the complete centered Ferudun primary PDF in memory, SHA2568ba41a5466bc289a9f714b57527f596fbe39b3422bc6bcf0a95d39bbde50c40c, from the primary publication URL. Its Theorem1 is the same qualified theorem, with stars, signed areas, least-period convention and the repeated-six/twelve obstruction. Its Lemma3 reflection telescope produces the dn/W trace. The current paper's standard addition identity converts this to the shifted S trace, so its explicit normalization/coefficient follows from that source plus Jacobi identities. The current abstract, Section1, Section7, README and exact Zenodo metadata prominently acknowledge the overlap and disclaim theorem/formula/method novelty, priority and independence. I found no unsupported novelty or open-problem-resolution claim in those governing documents.

The later arbitrary-point primary paper's introduction and Lemma4.3 with adjacent context were checked in memory. Its adjacent-foot pole cancellation supports the cited method overlap; no full verification of that separate17-page theorem or supplement is claimed. AST arXiv v2 Section4 and Chavez-Caliz journal Section5 Theorem6 independently support the prior meromorphic cancellation/compactness credit. DLMF22.4,22.8 and22.13 were checked as primary formula sources. The source-access records are appropriately limited rather than claims of comprehensive reading.

Fresh primary Zenodo metadata gives centered-record creation2026-10-01T15:39:54.821511+00:00. Fresh DataCite gives registration2026-10-01T15:39:55.000Z. The preserved GitHub server metadata gives PR204 creation2026-10-01T05:28:14Z and preserved HEAD551a524e2db65fec90684485ef676d0b4179378d. I independently reconstructed native tree/blob identities from frozen custody evidence, but did not reacquire GitHub live evidence because the shared API quota was exhausted. These are distinct server record times. They do not establish discovery time, earliest historical visibility, priority, dependence, independence or literal simultaneity; the current paper makes exactly that limitation explicit. No exhaustive worldwide novelty search was performed.

Primary links checked: [centered paper](https://eulersolve.org/papers/amr-050-0012/paper.pdf?v=8ba41a5466bc), [centered Zenodo](https://zenodo.org/api/records/23085904), [DataCite](https://api.datacite.org/dois/10.5281/zenodo.23085904), [arbitrary-point paper](https://zenodo.org/api/records/23400541/files/AMR-050-0011-paper.pdf/content), [AST v2](https://arxiv.org/html/2001.02934v2), [DLMF22.4](https://dlmf.nist.gov/22.4).

## Fresh reproducibility and code/data enforcement

I actually executed the sealed portable entrypoint with parent Python -B -O, PYTHONDONTWRITEBYTECODE=1, the specified existing read-only SymPy1.14.0/mpmath1.3.0 runtime, jobs2, and work/output paths inside this review folder. It completed all28 expected outcomes:14 valid ordinary/optimized child runs and14 intended false-identity/NaN rejections. Seven valid mode pairs matched; all142 scientific input pins passed; material hashes/sizes/mtime/ctime and dependency cache inventories were unchanged.

Fresh receipt SHA256409c91fa35260623e0317563b7a3762203b884f5eb559497e0f4653da86b5b3e; raw companion SHA2561313fa325be0417713de8b258853b18c727a9f06238ca0c05528c97cee7be8b3. FRESH_PORTABLE_RUN.json and its raw gzip preserve exact execution/code/flag/output bindings. The current driver source hash is1ac4733a4a383702dae18d68cd65042e531b406326e16e23f292a3f8f9c2c774.

I inspected all seven live program families and the original author/reviewer scripts and false-identity mechanisms. Independent AST comparison shows the valid historical derivatives change only Assert statements to explicit conditional exceptions. Their successful outputs remain byte-identical to archived original JSON. False author contact identities, reviewer product-plus-one, exact low-period and physical product-plus-one identities fail at their intended mathematical checks in both modes. The complex guard derivatives additionally reject a false numerical formula and an injected NaN residual.

EXECUTION_BINDINGS_CHECK.json independently rechecks every fresh28-case raw stream against receipt length/hash/source/flag bindings, the archived successful28-case run, the preserved failed13-case ENOSPC run, and24 historical physical execution receipts. It additionally challenges five actual driver guards under -O: false require, JSON NaN, numeric inf, numeric NaN and string inf; all reject. Archived binding consistency is not independent authentication that a historical execution occurred, which is why the fresh execution matters.

The historical bare-assert -O deficiency is real but already explicitly disclosed and replaced in the live entrypoint. It is not an unresolved defect in the current verification package. The documented first portable attempt is honestly FAIL with13 completed cases and15 ENOSPC setup failures; the later complete run and this fresh run are distinct. High precision remains noninterval and finite; neither PASS counts nor floating-point agreement proves the universal theorem.

A transient shared-storage ENOSPC also prevented two attempted shell preview/notes operations during this review. No scientific run failed or was hidden; subsequent stdout-only in-memory renders and direct file writes succeeded. No cleanup of shared data was performed. Fresh work scratch was automatically removed by the driver's per-case cleanup.

## Archive, provenance, metadata and presentation

Independent check_archive.py and ARCHIVE_CHECK.json verify:
- 181 outer regular files including the seal, with every other file matching the seal's exact byte count and SHA256.
- 177 unique ZIP entries, exact authoritative PUBLIC_MATERIALS_MANIFEST file set, all CRCs and member bytes matching both manifest and outer files; safe relative paths and no symlinks.
- All20 original submission files (59,343 bytes) equal the immutable originals; their SHA256/size/native blob identities match. All8 preserved native tree identities reconstruct, and every original file's path binds to the archived HEAD tree.
- The three intended upload pins and exact Zenodo metadata pin agree. Author name, affiliation, ORCID, date, title, abstract/scope, references, license and disclosure agree across paper/README/metadata.
- Third-party primary PDFs, dependency installations, bytecode/cache files, credentials and UI data are not package members. The explicitly excluded private512,477-byte direct-audit runtime inventory is absent. Historical manifests describing that larger local collection are preserved provenance, not falsely substituted for the authoritative public archive manifest.
- The sealed flags remain package_prepared=true, publication_ready=false, whole_package_reviews_complete=false and release_authorized_by_this_seal=false. Historical acceptance ledgers are dated stage records; this review does not rewrite them.

I inspected all six compiled manuscript pages using in-memory JPEG previews, without writing raster files or changing the editor. Equations, tables, theorem scope, references and pagination were legible and consistent with the source, with no clipping or substantive presentation defect found. No fresh LaTeX recompilation was attempted; the sealed PDF was read and visually checked.

Seal SHA2568808d37f4f0ed5a7cac015d9ef989aa07afca65498f450324d0128d1dd26d8fb.
TeX SHA256353813028694c4d995be16c69c205750a993754fa1e650cdc587a324a2aaffc2.
PDF SHA256e6ce64d99c1f3af9eb3a675594b29948d66a54e38e2b0bedeb03d2519d287b07.
ZIP SHA25605ea647a9f46afbdf1f0b47400ced35e69d81133b58d3cee8e070152beda8456.
Exact metadata SHA25672edabdae3623562bed1120f29d2db1ef95ff026bcc300586f403741ba5d57f0.

## Immutability and final limitations

IMMUTABLE_INPUTS_AFTER.json rehashes all445 frozen records: no content differences or missing frozen inputs. Newly added Root operational paths outside the sealed package are enumerated separately and are outside this package review. The fresh driver's142 scientific snapshots additionally include unchanged mtime/ctime and dependency cache inventories.

Authored-file inventory and exact pins are in AUTHORED_ALLOWLIST.json, with a stated self-exclusion convention. All authored files are confined to whole_package_adversary_01. Primary PDF bytes were not persisted or redistributed.

No bounded adversarial audit proves absence of every conceivable error. No formal proof verification, exhaustive novelty search, live GitHub reacquisition, complete later arbitrary-point-paper audit, or supplement reproduction is claimed. Within the assigned scope, no substantive mathematical, attribution, chronology, reproducibility, metadata or archive-integrity issue remains identified. This report is delivered for Root's decision; it does not release or approve publication.

