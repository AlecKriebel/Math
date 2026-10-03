# An even-strand Markov calculus for classical and virtual links

Alec Kriebel · ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

This is an unpublished, unrefereed research-note preparation. It gives an explicit elementary formulation for the ordinary oriented, unframed closure interpretation of Problem 42 in the 2014 Fenn–Ilyutko–Kauffman–Manturov survey: four reversible classical schemes and eight virtual schemes, together with defining braid relations, use only even-strand states. The proof converts every edge of the established unrestricted Markov theorems by positive padding. It does not claim first discovery, current openness, minimality, uniform geometric locality, a certificate-search algorithm, or a welded/plat/framed/transverse classification.

AI tools were used extensively in construction, drafting, adversarial review and computational verification. No human peer review or formal proof certification is claimed. This author preparation still requires native LaTeX compilation, visual inspection, and a new independent adversarial review before publication. No DOI has been assigned to this preparation.

## Contents

- `even_strand_markov.tex`: standalone manuscript, including its bibliography; no external input or images are needed.
- `verify_even_calculus.py`: compact Python standard-library diagnostics, with exact integer calculations and no network or file writes.
- `run_diagnostics.py`: optional runner retaining the checker and runner as they were before execution, full separate streams, actual command, clocks, interpreter and process IDs.
- `verification_run/`: one genuinely completed author-preparation diagnostic run, including full stdout and empty stderr.
- `metadata.json`: publication metadata draft and explicit pending workflow flags. It is not a Zenodo deposition or approval record.
- `SOURCE_PRECISION_QUALIFICATIONS.md` and `SOURCE_READ_NOTES.md`: mathematical scope, source access and priority qualifications.
- `INPUT_BINDINGS.json`: a small inventory of the first-party original/proof/priority materials read during authoring; these external audit paths are historical context, not dependencies of the proof or checker.
- `PREPARATION_REPORT.md` and `RESEARCH_LOG.md`: what was prepared, genuinely checked and still remains.
- `LICENSE-TEXT.md` and `LICENSE-CODE.txt`: CC BY 4.0 for new text and MIT for new code.
- `PACKAGE_MANIFEST.json`: author handoff inventory. It is not an immutable closure or publication gate.

## Reproduce the bounded diagnostics

Use Python 3.9 or later. No installation or third-party module is required. From this directory run:

```sh
python3 -B verify_even_calculus.py
```

The expected result is `PASS_BOUNDED_DIAGNOSTICS`, with 7,106 checks, 316 lifted edge cases and 1,716 relation-context cases. The fixed local seed is 10600042. The printed JSON is deterministic and can be compared byte for byte with `verification_run/stdout.bin`; its SHA-256 is `729d2e4d5532db6420fb9248d4b4a3aad909e0c8603e548848eccf35351d8fff`.

For a fresh captured run, use `run_diagnostics.py` in a new copy of this package **without its existing `verification_run/` directory**. The runner refuses to overwrite that directory. Running the checker directly does not modify the archived evidence.

The retained actual run used Python 3.9.6 and exited successfully. The capture records the actual interpreter path and child PID 95899; it does not substitute a generic command for the command that ran. Its source and operator remained unchanged. The stdout is 1,056 bytes; stderr is empty.

## What the diagnostics establish

The checker constructs unrestricted edges independently from the displayed even patterns, applies positive padding, and compares both exact tagged endpoints. It includes both classical signs, virtual stabilization, right and left exchanges, their reversals, empty blocks, one-strand padding, every defining relation family in bounded whole-word contexts, and the supplied-certificate height formula. It exercises all four classical and eight virtual families. The code enforces syntactic support bounds and the buffered minimum of four strands; it never asks whether a word could be rewritten into an admissible block.

Countercontrols show why the restrictions matter. An illicit two-strand T replacement could identify closures of `sigma1^3` and `sigma1`, whose Fox 3-coloring counts are 9 and 3. An illicit R replacement could identify `sigma1^2` and `sigma1 v1 sigma1 v1`; their ordered intercomponent signed crossing matrices differ despite equal component counts. The checker also rejects a buffered BR block reaching the forbidden index, checks the corresponding ordered-crossing obstruction, rejects BL at two strands, and shows that adding an idle strand fails to preserve the component count. The manuscript gives the invariance reasoning behind the witnesses.

These finite diagnostics support the written universal edge-lifting proof. They do not prove the unrestricted Markov theorems, decide link equivalence, solve the braid word problem, certify historical novelty, or replace independent review. Component counts alone are only diagnostics, not an equivalence criterion.

## Source and prior-work precision

The new operative bibliography uses *Banach Center Publications* 103 (2014), **9–61**, with Problem 42 on published page 37 / arXiv:1409.2823v1 page 34. Fiedler's 2003 negative conjugation-plus-double-move result is explicitly compared: D followed by T gives all four classical double-sign choices, while BC and T are additional permitted schemes whose generation by conjugation and double moves is not asserted. The full Fiedler counterexample proof has not been independently certified here. The bounded priority review did not verify an exact earlier answer, but it establishes neither absence of one nor present openness.

Earlier archived source records remain historical evidence. Their bibliographic or priority wording is superseded for this package by `SOURCE_PRECISION_QUALIFICATIONS.md`; they were not edited. No new research turn or discovery attempt was created by this preparation.
