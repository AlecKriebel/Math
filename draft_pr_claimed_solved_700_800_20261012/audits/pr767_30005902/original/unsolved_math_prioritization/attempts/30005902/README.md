# Nonvanishing Hopf cohomology bracket over an unrestricted field

Problem **30005902**, rank **802**, OWR-14298370-002. A complete negative answer to the literal unrestricted-field vanishing statement uses the 27-dimensional Hopf algebra H = F₃[x,y,z]/(x³,y³,z³), with x,y primitive and Δz = z⊗1 + 1⊗z + x⊗y. Its tensor-induction bracket satisfies **[f_x,f_y] = −f_z ≠ 0 in Ext_H¹(k,k)**. It is non-quasitriangular and has S² = id.

Independent AI-assisted audit: **ACCEPT WITH EXPLICIT SCOPE**, with no required mathematical correction. This is a draft research record, not human peer review, editorial acceptance, formal proof-assistant certification, or a novelty claim. Farinati's public 2019 explanation already describes the augmentation-derivation mechanism.

The finite-dimensional characteristic-zero variant and a variant requiring both input degrees to be at least two are **not settled here**. No assertion about their current global status is made. One of five substantive proof approaches was used; proof search stopped after the completed example.

## Read the argument

Read [the proof](author/PROOF.md), [source scope](author/SOURCE_AUDIT.md), and [the independent audit](audit/AUDIT_REPORT.md) together. The published tensor-induction orientation is R_f=(f⊗id)Δ and yields −f_z; the other translation convention has the opposite sign. Cocycles, comparison-map compatibility, nonboundaries, and power-flatness are checked explicitly. Exact finite arithmetic supplements the written argument; it cannot establish the cited general comparison theorem or editorial intent.

The original author and audit ZIPs are preserved byte for byte under frozen_archives/, with exact member copies under author/ and audit/. Their historical pending-audit and no-remote-writes statements refer to those earlier stages and remain unchanged. [RESULT.json](RESULT.json) records the later accepted disposition.

## Replay

Only Python's standard library is required. From this directory, or by absolute script path from any working directory:

    python3 -B verify_publication.py --replay --negative-controls
    python3 -O -B verify_publication.py --replay --negative-controls

Supply `--manifest-sha256 DIGEST` from the separately recorded publication receipt to authenticate the entire publication. Without an external digest, the publication manifest checks internal consistency; the two original freezes remain bound to hard-coded external pins.

The wrapper checks exact recursive inventory, hashes, byte counts, regular files, both immutable ZIPs and all 25 member-to-copy matches. It replays the author's 26,584 checks and the independent 29,708 checks, including four mathematical false alternatives each, and eight integrity controls for each frozen packet. Its own mutation controls challenge both freezes, proof and code bytes, missing/extra files, symlinks, extra directories, manifest rebinding, and assertion safety. All subprocesses force Python optimization level zero, even when the outer wrapper runs with -O or PYTHONOPTIMIZE=2.

The frozen optional identity script uses Python asserts. Do not run audit/check_identity.py directly under optimized Python. Use this optimization-safe launcher with the externally supplied input paths instead:

    python3 -O -B check_identity_safe.py --catalog /path/catalog.json --problems /path/problems.json --research-results /path/research_results.json --author-identity author/DATASET_IDENTITY.json --repository-manifest /path/repository-manifest-response.json --queue-source /path/queue-source-response.json

It recompiles the preserved script with optimization zero. The publication verifier tests that a deliberately false assertion fails through this same launcher under optimized conditions. Full corpus bytes are intentionally absent; historical identity attestations are not silently presented as a new online download.

Optional queue verification requires both full snapshots:

    python3 -B verify_publication.py --queue-base /path/base-QUEUE.md --queue-updated /path/updated-QUEUE.md

Only this target's Status=claimed_solved, Turns=1/5, and qualified Findings change. Every other queue byte, including pre-existing header contents, is preserved. Unprovided optional inputs are reported NOT_RUN.

Public source titles, URLs, manuscript status and inspection/hash metadata are in author/SOURCES.json and audit/SOURCE_RECHECK.json. The live unsolvedmath entry was inaccessible; the cached full record and original publisher report were inspected. The package contains only authored proof/code/audit and safe public metadata, with no source PDFs, copied source extracts, raw corpora, full dataset records, or private coordination material. No release, DOI, merge, or outside outreach is part of this draft.
