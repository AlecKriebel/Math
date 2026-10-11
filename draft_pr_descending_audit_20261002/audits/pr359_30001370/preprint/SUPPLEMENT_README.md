# Verification supplement: common L1 basin boundaries

This package accompanies Alec Kriebel's version 1.0 research note dated 3 October 2026.
It resolves OWR-4132-003 (repository problem 30001370) for exactly 0<A<=2/5,
6<B<=16, on all probability densities in the relative L1 topology.

The theorem is proved analytically in the paper. Existing global convergence,
open stable basins, the seed at 1, integral representations, and the original
inverse-expansion mechanism are credited to Bardet–Keller–Zweimüller. The new
full-density backward transport and closure give the original common boundary.
The mathematical note does not rely on the separate linear clarification in
the preserved historical candidate's turn 2.

Extract the ZIP into a fresh directory. With Python 3.10 or later run:

```
python3 -B verify_supplement.py
```

This default requires only the standard library. It checks the exact recursive
file inventory and all payload bytes, reproduces a separate continuous Bernstein
certificate, tests rough/zero-fiber constructions, and checks the sharper
rank-one/polynomial controls. Every exact field must match exactly. Two clearly
labeled floating numerical maxima may differ by absolute 1e-12, with their
experimental bounds checked separately; they never supply the analytical proof.

For the original three author programs, prior independent program, original
wrapper, and additional symbolic identities, use an environment with
SymPy 1.14.0 and run:

```
python3 -B verify_supplement.py --full
```

No verifier installs anything, downloads sources, sends messages, or writes
files. Original four saved outputs are compared in their entirety. The old
wrapper's public-only mode honestly reports that external source hashes are
not checked. The default new supplement has no dependency on SymPy.

`candidate/` preserves all 37 submitted problem files from PR359 head
6be98eac0ba508368218179ecf80020c037dbece, including early unresolved states and
review history. Those dated records are history, not the final preprint status.
`controls/` holds fresh independent calculations. `audits/` holds dated analytic
reports, source-first reconstructions, and the bounded priority dossier. Its
private native/source receipts remain with the research repository; they are
not redistributed as copyrighted PDFs or private tool captures. The priority
dossier can check its distributable layer with
`python3 -B audits/priority/verify_namespace.py --public-only`.

The current literature audit found no exact earlier equivalent theorem in its
inspected primary corpus; it does not prove exhaustive novelty. The foundational
final journal PDF was unavailable. The original post-publication OWR report,
author-hosted manuscript, arXiv version and ESI scan are distinguished. All 3
original source-manifest payloads were freshly byte-verified in the audit; the
source-enabled original wrapper was run successfully against those retained
private copies. They are not represented as the final journal PDF.

`paper/` contains the exact manuscript source and deposit manifest reviewed with
this package. Its metadata are descriptive; upload paths refer to the separate
PDF and this ZIP in the deposit kit, not to files inside `paper/`.
`FILE_MANIFEST.json` is the sole self-exclusion from the supplement inventory;
the reviewed external ZIP checksum binds it. Finite assertion counts are
reproduction evidence, not a proof of the infinite-dimensional theorem.

AI tools were used extensively in solving, verifying, literature research,
writing and adversarial review. This is unrefereed and has no independent
external human peer review. Paper and supplement: CC-BY-4.0, Alec Kriebel 2026;
ORCID 0009-0001-9320-500X. Third-party primary papers are cited, not included.
