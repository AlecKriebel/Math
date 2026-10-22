# First fresh whole-preprint adversarial review: PR765 / 30005613

**Disposition: REPAIRS REQUIRED for the frozen complete package. The mathematical theorem and its bounded attribution/framing review pass; four reproducible rebuild-preservation defects remain unresolved.** This review is complete. It is an internal AI adversarial review, not external human peer review, a formal proof certificate, a historical-first certificate, or publication approval. The final closure timestamp and full authored-file hashes are in MANIFEST.json.

The exact reviewed package is identified in CHECKED_INPUTS.json: paper.tex 17,334 bytes, the 78,509-byte six-page PDF, the 335,220-byte source ZIP, both Zenodo JSON files and the 389,281-byte upload kit. Each supplied SHA256 matched before review and again after all work. None of those six frozen inputs was changed. Only this review directory was written; no Git index/branch/remote mutation, external correspondence, staging, publishing or release occurred.

## Required software repairs

### PP01-001: a symlink in an output ancestor can mutate the closed source tree

Location: build_package.py lines 269-275, especially creating destination parents before checking only dest.is_symlink(). The extracted builder checks that the top-level output directory resolves outside the closed source, but it does not validate descendants' existing ancestors or resolved destinations.

Physical reproduction in a disposable extracted input copy S and external output directory O: create O/output/pdf as a directory symlink to S. Run the extracted builder under -O with --output-dir O and the original bound PDF. It exits 0, follows that symlink and writes S/paper.pdf, changing S's exact closed inventory. The closed input passed its initial integrity check. OUTPUT_SYMLINK_ATTACK.json records the command, exit and added path. symlink_attacks.py reproduces it without touching the frozen input.

Required fix: preflight all seven output destinations, including the inventory receipt, and every existing ancestor before any write. Reject symlinks/nonregular objects and require every resolved target to remain in the intended output tree and outside the closed input tree. Check the complete closed input inventory/bytes again after a successful rebuild. A postcheck alone is insufficient because it detects corruption only after it has occurred.

### PP01-002: the final inventory receipt follows a direct symlink and overwrites input

Location: build_package.py line 280. PACKAGE_INVENTORY.json bypasses even the direct symlink test used for the six main outputs.

Physical reproduction: symlink O/PACKAGE_INVENTORY.json to S/paper.tex, then run the same valid external rebuild under -O. It exits 0 and replaces the contents of S/paper.tex with the 1,115-byte inventory JSON. The resulting inputs are damaged even though the rebuild reports success. The second case in OUTPUT_SYMLINK_ATTACK.json records this independently of PP01-001.

Required fix: treat the receipt as an ordinary protected output in the complete preflight and safe-write path. Do not append an unchecked write after the protected output loop. The rejection must occur before any output or input changes.

### PP01-003: hardlink aliases evade path and symlink checks

Location: build_package.py lines 274-275 and 280, which write directly into an existing regular-file inode.

Physical reproduction: hardlink O/zenodo-metadata.json to S/paper.tex. The builder exits 0 and overwrites S/paper.tex with the 4,080-byte metadata JSON; its resulting hash is e8c6ad1672752360fd14e6294d8859ae4a2a95a1cf64c42caaacaafbf027d20a. Separately, hardlinking O/PACKAGE_INVENTORY.json to S/paper.tex overwrites it with the 1,115-byte receipt. Both are regular files with external pathnames; resolved-path tests and is_symlink() cannot detect inode aliasing. OUTPUT_HARDLINK_ATTACK.json and hardlink_attacks.py supply the actual commands and before/after hashes.

Required fix: reject existing destination hardlink/inode aliases to closed input files during preflight; rejecting multi-link output files is a simple conservative option. Write every output, including the receipt, through a fresh same-directory temporary regular file followed by atomic replacement, instead of truncating an existing inode. Retain the ancestor/resolved-path checks and final input-preservation comparison. Symlink-only fixes or a preservation check after direct writes do not resolve this defect.

### PP01-005: the supplied external PDF can be overwritten by an output-path overlap

Discovery credit: the parent root reported this additional edge. This reviewer then independently physically reproduced it; it is not counted as this reviewer's independent discovery. EXTERNAL_PDF_ALIAS_ATTACK.json records that distinction.

Place the exact bound original PDF bytes at the external output path O/zenodo-metadata.json and supply that path as --pdf, with the same O as --output-dir. The current builder exits 0 and replaces that supplied PDF with the 4,080-byte metadata JSON. No symlink or hardlink is involved. Its closed source tree remains intact, but its external PDF input is destroyed. The PDF was valid and matched the expected 78,509-byte binding before the build.

Required fix: include the actual external PDF path/inode among protected inputs during all-output preflight, and reject any destination alias to that input. Recheck its bytes after successful output writing, as well as the complete closed-source inventory. Atomic replacement alone still overwrites an input pathname when it is itself an output destination, so explicit alias rejection is needed.

All five damaging attack invocations used only copies inside this review's own scratch. The original six publication outputs remained intact. The parent acknowledged the three independently discovered defects, reported the fourth and plans a global repair only after this review is closed; no unreviewed future fix is counted as resolved here.

## Minor standalone exposition repair

PP01-004, paper.tex line 197 / Section 3: explicitly state O_1=Q_1(1) when setting a_1=x_1=1. The intended initial single cube is clear from the geometry and explicit in the original preserved proof, so this is a small missing definition rather than a central mathematical gap. The parent independently noticed it as well. It should be included in the forthcoming revision.

## Mathematical finding

For every d>=2 the proof chooses both growing cube widths and positive shrinking zero-thickness windows to obtain a connected open quasi-conical Dirichlet domain with a complete orthonormal eigenbasis, full essential spectrum [0,infinity), dense positive eigenvalues and no zero, AC or SC subspace. I found no unproved central implication or counterexample within that exact scope.

INITIAL_POSITION.md records an independent first reading before inherited verdicts. MATHEMATICAL_REVIEW.md supplies the detailed checkable reconstruction and attacks. In particular:

- The capacity argument uses the necessary logarithmic cutoff in d=2, ordinary radial scaling in d>=3, bounded real/imaginary truncations for arbitrary Sobolev functions, and closed H0^1 subspaces. It survives arbitrary fixed earlier irregular screens without a boundary regularity theorem.
- A compactness contradiction in a fixed bounded box supplies norm convergence of the shrinking-window resolvents. The final infinite exhaustion is separately proved by form Galerkin projections and is only strong. In fact its resolvent norm discrepancy is one, which confirms why the distinction matters.
- Finite nonresonance selection precedes aperture selection. Whole disjoint spectral clusters handle degeneracy and splitting, preserve nesting and ranks, and impose only finitely many constraints at each stage. No uniform gap, simple spectrum or future spectral information is assumed.
- Norm limits of protected finite-rank projections commute with the independently identified genuine resolvent. Its injectivity excludes infinite-energy escape. Repeated complete cube-basis probes and the explicit birth-plus-tail bound 3*2^(-n-1) prove completeness and eliminate SC, rather than merely producing dense eigenvalues.
- Compact plane-wave cutoffs in disjoint growing cube interiors give singular Weyl sequences at every nonnegative energy. The zero-mode energy identity, connectedness and infinite volume exclude a zero eigenvector. The d=1 failure and all claim boundaries are correctly retained.

Fresh exact finite controls use a different rational rotation and a d=3 forbidden-width example, together with exact tails and cutoff-profile arithmetic. They illustrate the analytic checks and certify no PDE or infinite-dimensional theorem. Analytic counterexamples to branch selection, strong-only projection limits, missing dense probes, noninjective limiting resolvents and false norm exhaustion are written out in MATHEMATICAL_REVIEW.md.

## Primary sources, credit and bounded priority

SOURCES_AND_PRIORITY.md details the independent primary-source comparison. The official OWR contribution at printed pp.2077-2078 and KL Sections 2.2, 3, 5 support this existential question with future-width freedom. HSS1991 Proposition 1.4, directly read with its proof at printed pp.458-460, already uses spectral families for degeneracies. These antecedents are substantively credited. The accepted increment is the exhaustive geometric transport/completeness construction; no abstract-method novelty is claimed.

The original priority reports, comparison tables, adversarial challenge, coverage limitations and separate source-reading correction were checked after the independent first position. Fresh rendering confirms both survey formulas on PDF p.16 do have closure bars. The addendum properly supersedes the stale criticism, with all old bytes preserved. Bounded searches locate no full matching predecessor; inaccessible older/restricted bodies and unindexed/nonpublic material remain explicit limits. Neither historical firstness nor current worldwide openness is certified.

Bibliographic identities, versions, pages, ORCID, extensive AI-use/unrefereed/no-human-review/no-formal-certification disclosure, CC BY 4.0 scope and excluded stronger claims are consistent across paper/README/metadata/deposit. No private source corpus, downloaded primary full article body, credential or outreach material was found in the closed source archive. Temporary primary bodies/renderings used in this review were removed.

## Reproduction and presentation evidence

REPLAY_RECEIPT.json records fresh extracted-source replays from an unrelated working directory on Python 3.14.6 normal, outer -O, PYTHONOPTIMIZE=2 and bundled Python 3.12.14. All pass with 120 total source files, 119 manifest rows, 39 original files, 4,187 author assertions, 2,911 portable first-audit assertions, 2,923 with the author archive, and 2,304 second-audit exact tail checks. Children are explicitly launched in isolated normal assertion mode. The source tree is unchanged after each run.

REBUILD_RECEIPT.json records three independent external-output rebuilds, all six publication files byte-identical on normal/-O/3.12. Metadata copies agree, and the kit contains exactly the two deposit files, flat deposit JSON, metadata JSON and instructions. PRESERVATION_RECEIPT.json separately compares every original file to the actual frozen original directory and every original ZIP member to its extraction. These are preservation checks, not authenticity signatures or mathematical proof.

PHYSICAL_NEGATIVE_CONTROLS.json records 38 successful expected rejections across -O and environment optimization 2: changed TeX/metadata/original proof/archive, missing/extra/hidden files, empty directories, physical symlink/FIFO inputs, duplicate/unsafe/self manifest paths, repinned original/review manifests, internal rebuild output, wrong bound PDF and changed closed rebuild input. The packaged nine in-memory historical guard controls also reproduce. The five additional damaging output-path attacks are separately recorded as FAIL, not folded into a blanket guard PASS.

The diagnostic comparator uses exact types/structures/nonfloats and finite floating values with precisely 1e-12 relative and zero absolute tolerance. Eleven boundary tests additionally reject NaN/infinity, zero-versus-tiny-nonzero, type/key/length/count changes and larger floating discrepancies. No floating tolerance is applied to byte hashes or original archive payloads.

A fresh copy of TeX compiled successfully with the builtin compiler and Tectonic 0.16.9 using cached resources. All six original PDF pages and all six fresh compiled pages were individually rendered/viewed, with no clipping, overlap, broken formulas/references or illegible text. Fresh page rasters match all six original rasters byte-for-byte. The fresh PDF's different creation metadata is expected and was not mistaken for a byte-rebuild failure. COMPILE_RENDER_RECEIPT.json records these checks. An initial ENOSPC copy failure and the associated unsuccessful compiler attempt are explicitly recorded as failures; after deleting only this review's temporary source bodies, retries succeeded. A later ENOSPC here-document launch was likewise retried after cleaning only this review's already-inspected scratch. No check was dropped or falsely passed because of storage pressure.

## Final limits and closure

The whole-package review is complete; current package acceptance is withheld for PP01-001 through PP01-003 and PP01-005. The theorem review has no outstanding central gap. PP01-004 is a minor definition clarification. No future fix, second successive fresh review, external human review, formal proof or publication step is claimed as completed by this report.

All authored regular files, including hidden files, are enumerated in MANIFEST.json; only the manifest itself is excluded. No scratch directories, copied source bodies, symlinks or special objects remain. CHECKED_INPUTS.json separately records the six frozen input identities before and after review. Run python3 -B verify_closure.py for read-only review closure verification. Reproduction drivers write new receipts and must be run in a disposable review copy, not this closed record. Their original executions are preserved in the receipts above.
