# Transverse surgery: accepted partial results

Problem 10300034 / AMR-102-0034, rank 1005. **Unsolved, 5/5 approach families.**
The complete frozen author proof was independently audited and accepted without correction. This publication wrapper changes no author or audit byte and adds no proof-search approach.

## Mathematical scope

Read [the original proof](author_original/packet/PROOF.md), [the complete independent audit](audit/AUDIT.md), and [the scoped acceptance](audit/ACCEPTANCE.json).

The accepted results are a closed-one-form period obstruction; a common filling-group quotient in the stated epimorphism direction and its Betti lower bound; disjoint positive normally generating sections on surface products; the meridional-only extension criterion for the restricted original fiber cohomology class; an explicit contact-to-foliation knot-transfer countercontrol; and a finite circulation criterion with conditional geometric graph-to-link realization.

No fixed universal target is constructed, and no obstruction ruling out every fixed target is proved. The original question imposes no uniform bound on the number of surgery components. A necessary unbounded-component phenomenon does not answer that question. Finite graph controls do not supply the geometric realization hypotheses. Contact approximation alone does not preserve the required knot transversality.

There is no full solution, novelty certification, exhaustive current-open-status certification, formal proof, or conventional human-peer-review claim. Author and independent audit work used AI assistance.

## Frozen evidence and historical labels

All 13 author members and all seven audit members are present unchanged, together with the original author and independent-audit ZIP archives. The two external receipts are retained unchanged. Earlier `independent_audit: pending` and `remote_writes: false` labels describe historical stages; the later audit and this publication overview give the current scoped disposition. Nothing is silently relabeled.

Source records are historical retrieval/inspection evidence. Lickorish's opening theorem scope was inspected, but the full paper was unavailable: no complete-proof inspection or local PDF hash is claimed. Other frozen source pins cover three PDF/extraction pairs. Publication replay makes no new source-reading or literature-search claim.

Only authored mathematics, audits, programs and public verification metadata are included. Source PDFs, copied source extracts, dataset contents, private sources, personal information and coordination material are excluded.

## Reproduce with an external trust anchor

Authenticate the SHA-256 of BOOTSTRAP.py against the independent publication receipt or PR before execution. The launcher pins VERIFY_PUBLICATION.py and PUBLICATION_MANIFEST.json before executing payload code. The manifest binds the exact regular-file and directory inventory. The original ZIP bytes, member sets and contents, inner manifests, original proof, and scoped disposition are all checked.

    python3 -I -S -B BOOTSTRAP.py
    python3 -I -S -B -O BOOTSTRAP.py
    python3 -I -S -B -OO BOOTSTRAP.py

The default is source-free; actual source and corpus rehashes are explicitly NOT_RUN. Historical success records do not imply present access to external inputs. With authorized local inputs available, append any complete input group:

    --source-dir SOURCE_DIRECTORY
    --problems COMPLETE_PROBLEMS_JSON --research-results COMPLETE_RESEARCH_RESULTS_JSON

These inputs remain external and only hashes, sizes and match results are emitted. Both corpus files are required together. Missing, mismatched or malformed supplied inputs fail closed. `--integrity-only` authenticates the package without running finite controls and cannot be combined with optional primary inputs.

After successful authentication, the outer fail-closed controls can be run with isolated Python on TEST_MUTATIONS.py. They cover byte changes and omissions for every publication member, hostile executable replacement, malformed manifests, symlinks, nonregular files, extra directories, and altered acceptance. Genuine read-only and hostile-import controls are also included. Checks rely on a trusted interpreter/standard library/OS and a stable filesystem; they are not a defense against concurrent filesystem races.

All finite controls support artifact integrity and calculations, not general topological truth. Local and downloaded-artifact replay are distinct from GitHub CI. Zero GitHub checks does not mean CI passed. This work is a draft PR only, with no merge, release, DOI, or external outreach.
