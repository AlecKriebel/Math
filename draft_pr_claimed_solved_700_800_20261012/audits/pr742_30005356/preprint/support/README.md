# Verification materials: inverse Frobenius in generic multiplicative fields

This archive supports Alec Kriebel's unrefereed research note, version 1.0,
dated 13 October 2026. The theorem is a complete negative answer to the
unrestricted integral-polynomial equality in OWR 2023, printed pages 97-98,
and arXiv:2212.02115v4, Question 5.8. The characteristic-zero classification and
equality with the localized ring in positive characteristic remain unresolved.
Classical inverse Frobenius, d'Elbee's polynomial faithfulness and Chini's
base-language distinction are credited. No first-priority, current-open-status,
final-journal-wording, external human-review or formal-certification claim is made.

The complete proof is in paper.tex. Compile it with a standard LaTeX engine
or Tectonic. The separate paper.pdf is the rendered manuscript. The manuscript
uses no additional project files. Publication metadata is identical in the
support archive, deposit configuration and upload kit.

Extract source-and-verification.zip into a new empty directory and run:

```sh
python3 -B verify_bundle.py
python3 -O -B verify_bundle.py
```

The top-level verifier uses explicit checks that remain active with -O. It
runs assertion-based child controls in normal mode with PYTHONOPTIMIZE removed.
The frozen candidate's own wrapper deliberately rejects optimized execution;
the top-level verifier checks this rejection as a guard, rather than treating
an optimized refusal as a mathematical pass. Python3.10 or newer and the
standard library suffice; no network, account, dataset or algebra package is
needed. For integrity only use `python3 -B verify_bundle.py --integrity-only`.

The replay verifies the exact closed inventory, the original packet's 26 files
and its archives, independent historical controls, and a new independent
operator-algebra reviewer's finite negative controls. All finite fields used
are outside ACFH. In them inverse Frobenius is an integer power; these are
intentional checks against overgeneralization. Computations do not establish
the infinite-model exclusion, certify the written proof or guarantee novelty.

The historical_candidate folder preserves the exact files from PR #742 head
77be9cbd8b58358919f42c204d9dd829ccd5d60f. Dated audit reports preserve their
original conclusions. In particular, the wide priority audit's overbroad
full-problem wording is corrected in priority_scope_addendum; the original
closed report remains unchanged. PRIORITY_GATE.json records the reconciled
exact-target conclusion. References to prior absolute workstation paths are
informational provenance; replay uses paths relative to this archive.

The final journal body was inaccessible. The inspected versioned texts define
the precise claim answered here. Bounded primary-source and registry searches
found no earlier equivalent full proof, without certifying historical priority.
No third-party source PDF, extracted scholarly text, raw dataset, credentials,
private coordination material or downloaded source image is in this archive.
Whole-preprint reviews and subsequent publication receipts are maintained in
the linked repository audit folder; they are not recursively included here.

AI tools were used extensively in development, reproduction, verification,
adversarial review and preparation. This is an unrefereed preprint. Internal
AI-assisted review is not external human peer review or proof-assistant
certification. The deposit is CC BY 4.0; frozen artifacts retain their provenance.

For an independent archive rebuild, copy the extracted support materials into
a separate working directory, place the supplied paper.pdf there (or compile
paper.tex into output/pdf/paper.pdf), and run `python3 -B build_package.py`.
The new closed support copy is in support/. Fixed ZIP entry dates make the
support archive reproducible from identical inputs. Packaging generates new
outputs in that working copy; use a clean extraction for the inventory replay.
