# Accepted construction and publication guide

Problem **30005079 / OWR-10252925-004**, queue rank 947.

## Mathematical disposition

The complete construction in [PROOF.md](PROOF.md) has been accepted by two independent AI mathematical reviews: [audit A](audits/INDEPENDENT_ACCEPTANCE_A.md) and [audit B](audits/INDEPENDENT_ACCEPTANCE_B.md). Both accept the exact proof SHA-256 `657f458cf3eece42eef9c8dfd46a7c20aaaf363e3a6744f396af3c7389fa43a3`.

It constructs the smooth Fano fivefold X=V×F₁ and a quasi-monomial valuation with rational rank two and exact irrational weight ratio. Its canonical first special real degeneration has singular central fiber Z×F₁. The proof establishes the graded anticanonical Segre ring, canonical discrepancy shift, weak product soliton, and applicability of the global Han–Li minimization criterion. The original problem permits products and dimension five. The central pair is already weighted polystable, so the second canonical step preserves its underlying variety.

This is recorded as **claimed_solved, 1/5 substantive author turns**. Numerical and citation corrections, exact checks, and independent reviews are not additional author attempts. Acceptance uses the cited theorems; it does not independently reprove them. No research-novelty, priority, human-peer-review, journal-acceptance, or formal-proof claim is made.

## Preserved originals

All twelve files of the author's public candidate package are preserved byte-for-byte, including its original README, manifest, candidate language, proof, public bibliographic metadata, checks, edition history, and three correction patches. `PACKAGE_MANIFEST.json` retains its original SHA-256 `4ae078843413493dc3548e1390218ce437abd2a2dfa49049c52629432a36652c`. The two full acceptance reports and the independent reviewer's script/results are also preserved exactly. Their statements about no publication describe the time of those reviews.

The original v1→v2 numerical correction, v2→v4 citation correction, and v3→v4 polystability correction are real unified diffs. The portable driver reconstructs all four original editions using reverse patches, checks every edition hash and byte count, and replays all three patches forward. The complete current proof remains unchanged.

Only authored mathematical work, checks, acceptance reports, and public verification metadata are included. Bibliographic metadata can identify inspected public source PDFs without distributing those PDFs. No copied scholarly source documents, extracted source files, screenshots, dataset contents, private sources, personal data, or private coordination files are included.

## Reproduce the checks

Use Python 3.10 or later, with SymPy installed. The publication replay was tested with Python 3.12.14 and SymPy 1.14.0; these are tested versions, not a claim that other versions fail. Run from any working directory:

```sh
python /path/to/30005079/verify_publication.py
```

For standard-library-only integrity and correction-history checks:

```sh
python /path/to/30005079/verify_publication.py --integrity-only
```

Assertions must be enabled. The driver rejects optimized Python, unexpected files or directories, symlinks, modified or missing files, and changed frozen pins. It runs both original scripts unchanged inside a temporary layout, supplies the exact accepted proof where the independent script originally expected it, and compares both regenerated JSON outputs byte-for-byte against their frozen originals. It never rewrites the packet.

The algebra checks cover the moment identities, density masses and first moments, exact-rational root brackets, fan determinants, polynomial coprimality, and the independent toric barycenter reduction. The author's finite resultant samples are auxiliary spot checks. The all-denominators irrationality theorem, algebraic geometry, real filtration, singular product soliton, and global optimality are mathematical arguments accepted in the audits, not conclusions certified by running Python.

`PUBLICATION_MANIFEST.json` binds every published packet file except itself. Its external SHA-256 is reported in the draft PR. This is an integrity manifest, not a digital signature or a substitute for mathematical review. Repository-hosted CI status is reported separately in the PR; a successful local replay does not imply a hosted CI pass.
