# Robust polynomial interpolation: accepted prior-proof audit

Problem **2508 / EP-1133**, rank **1037**. Repository disposition: **already_solved, 0/5 new substantive approaches**, relative to the declared Bernstein interpolation strict-density theorem and standard analytic imports.

Start with [ACCEPTANCE.md](ACCEPTANCE.md), the complete [authored proof verification](author/public/REPORT.md), and the complete [independent mathematical audit](independent_audit/INDEPENDENT_AUDIT.md). The accepted reports and archives are preserved byte for byte.

The prior argument is the April 29, 2026 draft *A Bernstein-density proof of Erdős’s robust interpolation obstruction*, publicly attributed through Przemek Chojecki's posting with GPT-5.5 Pro assistance. Its PDF title page names no author. This publication records an AI-assisted verification of that prior argument, not a novelty or priority claim. Journal acceptance, current tracker acceptance, community consensus, human expert certification, and proof-assistant formalization are not established.

## Source-free contents and trust

The author archive contains exactly 16 regular members; the independent supplement contains exactly eight. Both original final receipts are retained separately. Third-party source PDFs, copied extracts, datasets, and private coordination material are omitted. Public source URLs, hashes, sizes, and historical inspection records remain in the frozen metadata.

Use an independent trusted receipt, such as the exact-commit PR record, to authenticate BOOTSTRAP.py before executing it. A freshly computed hash of unknown files is not a trust anchor. The authenticated bootstrap pins the publication verifier and manifest; the verifier enforces the exact recursive inventory, original accepted bytes, strict JSON parsing, archive inventories, and archive-to-file byte comparisons.

Python 3, standard library only, under an ordinary nonroot account:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

For the outer publication controls, supply the trusted publication manifest, bootstrap, and verifier digests in that order:

    python -I -S -B mutation_tests.py . MANIFEST_SHA256 BOOTSTRAP_SHA256 VERIFIER_SHA256

The wrapper does not change the packet. Only temporary copies are writable; accepted originals are never thawed. The author harness uses its original 28 source-free mutation categories and its own genuinely nonroot read-only replay. The publication wrapper also reruns the source-free subset of the independent controls and a separate genuinely nonroot read-only baseline. Outer controls cover normal, -O, -OO, hostile Python environments, real denied-write probes, malformed metadata, altered archives, and path/type substitutions.

## Fresh versus historical verification

Fresh default replay reports source PDFs and corpora as **NOT_RUN**. It reruns 84 author bundle rejections and 51 independent portable rejections. The historical author total of 90 includes six optional-source rejections omitted from this replay. The historical independent total of 75 includes 24 source-dependent rejections omitted here. These categories can overlap and must not be summed as independent mathematical evidence. The original independent full-source harness requires all five external files and is **NOT_RUN** by the publication wrapper; its historical exact receipt is preserved.

The finite checks cover 80 parameter choices, 400 exact arithmetic cases, and 15,192 finite node/block patterns. They check arithmetic and indexing, including repeated nodes. They do not prove compactness, the density theorem, or the infinite analytic argument.

For an optional full-source rerun of the accepted author verifier, follow [its original README](author/public/README.md). Obtain all five external files independently and match their published pins. The publication wrapper itself has no optional-source interface and makes no fresh source-inspection claim.

No merge, release, DOI deposit, or external outreach is part of this draft. Absence of GitHub checks means CI **NOT_RUN**, not a passing CI result.
