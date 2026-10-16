# NP-completeness of three-terminal shortest-path blocking

Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X.
Research note version 1.0, 12 October 2026.

The four-page note proves NP-completeness of the exact undirected triangle BSP
question posed by Krause, even with unit deletion costs, unit traversal lengths
and initial terminal distances 3. It also proves the finite-terminal-distance
and exact 3-to-4 variants. Extensive AI tools were used for construction,
verification, adversarial review and writing. The preprint is unrefereed and
has not undergone independent human or journal peer review. Historical first
priority is not asserted. The earlier tripartite attachment mechanism is credited
to Khachiyan and coauthors (2008), and the two-subdivision cover identity is
credited to Poljak (1974). Both ingredients are proved explicitly here.

The published supporting archive contains the LaTeX manuscript, an unchanged
original proof/verification packet, fresh independent audit reports and checkers,
the current priority audit and a source-free reproduction entrypoint. It contains
no copied primary-source PDFs, source images, raw catalogue statement/report,
credentials or private account data. Primary references are linked and their
retrieval hashes recorded. Original pre-audit/prepublication language is preserved
as historical evidence and is superseded by this note and its publication record.

## Reproduction after extracting the supporting archive

Requires Python 3.10 or later and its standard library. From the extracted root:

```
python3 verify_package.py
python3 -O verify_package.py
python3 verify_package.py --pdf ../three-terminal-shortest-path-blocking-v1.0.pdf
```

The supported entrypoint verifies exact payload membership, byte counts and
SHA-256 hashes, original frozen anchors and manuscript identity; runs the original
three mathematical suites; checks all 100 original mutations; and runs both fresh
independent mathematical checkers plus supplementary optimization/integrity
controls. Replays occur in disposable copies and preserve the distributed files.
The child command uses `-I` without `-O`, ensuring mathematical assertions remain
active even when the outer entrypoint runs under optimization. Direct optimized
execution of historical raw checkers is not a supported reproduction command.

Use `--integrity-only` for a quick byte-consistency check. Supply `--pdf PATH` to
verify the separately distributed PDF against the recorded digest. The archive
does not need network access, source PDFs, credentials or an original workspace.
Hashes establish consistency against trusted manifests/verifiers; replacing the
entire verifier and its trust anchors can defeat that boundary. Finite checks
supplement the universal written proof and are not proof-assistant certification.

The source `note.tex` is standalone. A PDF can be regenerated with Tectonic:

```
tectonic note.tex
```

Compilation can require Tectonic's package bundle to be cached or available online.
PDF generation timestamps can change its byte digest, so a rebuilt PDF need not
match the released PDF byte-for-byte. The released manuscript is the mathematical
reference; the original proof packet remains independently checkable.

## License and references

Authored manuscript, proofs, code and audits in this deposit are licensed under
Creative Commons Attribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/ . External references retain their
own terms and are not redistributed in this package.

Primary historical question: Krause, Oberwolfach Report 50/2005, pp. 2856–2858,
DOI https://doi.org/10.4171/OWR/2005/50 .
Original research proposal: https://github.com/AlecKriebel/Math/pull/904 .
