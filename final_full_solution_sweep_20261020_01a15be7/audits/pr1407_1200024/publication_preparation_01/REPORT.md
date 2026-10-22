# PR1407 / 1200024 — scientific publication preparation

**Disposition: prepared for two NEW independent whole-package reviews; publication_ready=false and root_authority=false.**
Assigned preparation 100%; overall sweep checkpoint 80%.
This is a scientific handoff, not permission, an independent final acceptance, a service action or a publication record.

## Exact claim and original coverage

The seven-page note, *Free spanning-forest degree can decrease under squaring*, proves a counterexample for infinite connected locally finite simple unweighted vertex-transitive graphs. For the binary grandparent graph G of degree8, its full automorphism group is nonunimodular, and its simple square has degree40. The proof gives

    Edeg_FUSF(G) = (24-sqrt(2))/7 > 161/50,
    Edeg_FUSF(G²) <= 3208526010913748780/10^18 < 321/100.

With the paper's explicit convention b_F(X)=Edeg_FUSF(X)/2-1, the difference exceeds1/200. No equality for another nonunimodular Betti invariant is asserted.

Abért's actual 2November2010 seven-page source, printed4 Question24, says arbitrary vertex-transitive and gives the Cayley comment. The page was independently visually inspected. There is no implicit global unimodularity assumption. Its normalization formula is not printed, so that qualification remains explicit in the abstract, theorem interpretation, source notes and proposed metadata. The known Cayley case is not refuted, and no negative result for the unimodular subclass is claimed.

## Complete mathematical materials

The note contains two genuine free-exhaustion calculations of the original graph, not an extrapolation from numerical data:

1. Two-terminal descendant branches yield kappa_0=1/2 and kappa_(m+1)=(1+2kappa_m)/(2+2kappa_m). Explicit L_(m,n) subgraphs form an increasing free edge-exhaustion on the diagonal. Uniform contraction of the upper triangular suffix justifies the diagonal conductance limit. The resulting parent/grandparent free resistances are (3sqrt(2)-2)/7 and (6-2sqrt(2))/7.
2. An actual nested induced exhaustion by descendants of the nth ancestor through depth2n yields c_m=1+2c_(m-1)/(1+c_(m-1)) and inhomogeneous suffix coefficients. Uniform derivative bounds1/2 and1/4 prove the required triangular convergence independently, retaining the finite top boundary.

The full automorphism group is recovered intrinsically from triangle counts and the unique center among the recovered tree-neighbors, rather than inferred from a nonunimodular subgroup. The complete40-neighbor square count, distinction of free/wired resistance, finite Kirchhoff marginal and exact passage to infinite free marginals are stated and justified.

The finite square J=(G[tree ball10])² contains every infinite-square root edge. All40 finite unit flows are carried unchanged into sufficiently large finite FREE exhaustions. Finite Thomson/Rayleigh plus exhaustion gives the required upper bound. Minimizing arbitrary infinite square-summable flows, which would give a wired quantity, is not used.

The immutable original current data is distributed in full. Its gzip SHA256 is
6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f
(165241 compressed bytes;4460799 decoded JSON bytes).

The newly authored independent indexed-tree checker regenerates the whole3070-vertex19931-edge graph and all40 infinite root neighbors. It verifies every one of797240 genuine integer current entries, all122800 divergence equations, every one of40 exact energies and the total3208526010913748780/10^18. It rejects four actual-row corruptions: changed current, wrong source, boolean current and missing entry. Normal and optimized Python outputs agree exactly. These are four distinct corruption mechanisms; optimized replay does not create additional distinct tests.

A separate new binary-word/global-Fraction star-mesh script checks four branch depths and the actual induced n=2,3 networks (maximum127vertices). At n=2 it finds triangle(7/3,17/10,1) and resistances27/80,121/240; at n=3 it finds(12/5,6236/2669,1). These finite diagnostics support indexing and do not replace the written all-depth proofs.

No original claimant verification program or floating solver was executed for these independent replays. The certificate is treated as inert data. No proof-assistant certification is claimed.

## Actual priority challenge and limitations

The original graph family, Kirchhoff/Thomson/Rayleigh principles, and forest/exhaustion framework are credited. This paper proposes a specific expected-degree comparison, not a new general electrical or forest mechanism.

The corrected actual BLPS author body was read for the finite principles and free/wired/exhaustion identities actually imported. Tang's actual arXiv v2 Section5.2, including its finite-ball path/resistance bounds and complete connectivity/branching proofs, was read in full. It does not give the complete expected-degree square comparison found here. Pete–Timár's actual v2 introduction/theorems explicitly distinguish component-count changes under generating-set changes from the Cayley expected-degree invariant; the component-count theorem is not misrepresented as this full result. Gaboriau's actual Section2.4 retains a transitive-unimodular hypothesis.

Fresh primary publisher-deposited bibliographic records authenticate the final Tang and Pete–Timár DOIs. Actual final journal PDF requests returned HTML challenges, not scholarly PDFs. Their final bodies were not read, and no assertion about unchanged final content is made. The full Lyons–Peres book, unindexed materials, theses and alternative terminology remain coverage limits. SOURCE_READ_SCOPE.json, DEPENDENCIES.md and PRIORITY.md state exact versions and actual read scopes.

Bounded primary searches and inspected bodies authenticated no earlier full counterexample publication. That does not certify worldwide firstness, exhaustive novelty or continuing openness. The result and data were already public in PR1407 before this dated note. No prior dependency DOI, claimant PR or internal acceptance is offered as existing publication coverage. No existing-publication spreadsheet row is proposed.

## Duplicate checks

Before substantive preparation, the GWS CLI read numeric gid1254632077 with all43 columns requested, full raw metadata before/after and both typed UNFORMATTED_VALUE and FORMULA raw views. The final refresh did the same and found209 populated rows with no changes. All245 local publication-state files were re-inventoried; their hashes are unchanged. Every actual keyword lead was read; the two sheet and two local leads concern distinct mathematical subjects.

Public Zenodo identifier and mathematical-term queries were read in full. The apparent identifier/word matches were unrelated medical, biological or model records, not graph-forest results. No equivalent published record or unfinished target upload was authenticated. Full operational captures remain private and outside the scientific release. This is a preparation-time deduplication result, not authority to publish later; root must repeat live status/DOI/spreadsheet checks.

## Paper, archives and reproduction

A dedicated LaTeX project was created with the built-in project tool, and the final source compiles successfully with the built-in compiler. The exported PDF was compiled with the already pinned cached Tectonic0.17.0 under a profile denying network and all writes outside this preparation folder. No installation, package download or shared-cache write was used. The sole cache-font issue was resolved by selecting a cached small math size; a breakable certificate filename and intact main theorem avoid layout defects. Every one of the final seven PDF pages was visually inspected; RENDER_RECEIPT.json records the final pages.

The SIX release files are in release/. The16-member source ZIP includes editable main.tex, frozen identical PDF, entire certificate, both independent standard-library scripts and exact outcomes, scientific reproduction/dependency/priority notes, provenance, licenses, metadata and a deterministic offline builder. Every source member is read back and hashed by source-manifest.json, which excludes only itself.

The five-member upload kit contains the PDF, source ZIP, metadata, two-file deposit manifest and upload README. The scientific deposit is PDF+source ZIP ONLY. No third-party scholarly body, private operational capture, credentials or upload driver is distributed.

Every source member was physically reconstructed from the completed source ZIP into a fresh own scratch folder. Both scientific checkers, including a fresh optimized full current replay, pass there. The fresh builder produces all SIX release files byte-identically. This packaging replay copies the frozen PDF; it does not recompile TeX or independently prove mathematics or novelty. Archive CRCs, member modes/timestamps, exact membership, nested kit bytes, metadata and deposit files were read back. PACKAGE_REPLAY_RECEIPT.json records the result.

The existing top-level Zenodo client's local check accepts the exact two-file manifest. Its code returns before token/client/state loading for that command, and the invocation additionally denied network and outside-folder writes. No stage, inspect, upload, reserve or publish action was taken.

## Disclosure, preservation and next step

Alec Kriebel is the named author with ORCID0009-0001-9320-500X. Extensive AI involvement across research, proof, computation, literature, writing and adversarial auditing is disclosed. This is an unrefereed preprint without formal independent human peer review or journal acceptance. Authored prose/certificate data are CC BY4.0; authored verification/packaging code is MIT.

The adopted predecessor seal d9fd06768c2480003b547a84f66b33d8290e766c746375fa7d993fd390edb543 was independently checked again after preparation: all48payload files and6directories retain exact bytes, modes, nanosecond mtimes and membership. The original certificate bytes are unchanged. All new work stays in this dedicated folder and uses no hardlinks. Resource receipts cover the14MiB new-allocation cap and150MiB reserve.

Known material mathematical objections: none found in this preparation. Priority/source-edition coverage remains bounded as disclosed. Two NEW independent adversarial reviews of the ENTIRE final paper, code, data, metadata and archives are still required, followed by root adoption and live duplicate/concurrency checks. No independent final acceptance or root authority is conferred here.

No Git, STATE, QUEUE, PR, service, DOI or spreadsheet/ledger write was performed. No outside person was contacted, no outreach was prepared, and unrelated agents were not messaged.
