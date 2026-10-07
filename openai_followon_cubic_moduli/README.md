# Cubic compactification consequence and priority audit

This is a research audit, not a new-solution preprint package. Owned audit findings are published in public repository checkpoints under the user's research protocol. The requested higher-dimensional comparison is already publicly stated in stronger form by Kong–Shen–Zhao–Zhao. Our gap-based consequence uses OpenAI's upstream theorem and Li–Liu/Spotti–Sun's established transfer. No genuinely new in-scope contribution has been established. No Zenodo deposit, DOI, or tracker row was created.

- `main.tex`: self-contained consequence/audit note; author Alec Kriebel, ORCID 0009-0001-9320-500X. Built-in LaTeX compiler verified successfully.
- `paper.pdf`: exported readable audit PDF, created using Tectonic; not a submitted preprint.
- `CURRENT_THEOREM.md`, `DEPENDENCY_LEDGER.md`, `APPROACH_TABLE.md`: exact scope, dependencies, limitations and route status.
- `agent_notes/`: five distinct scoped mathematical and priority audits, source hashes, exact arithmetic check.
- `reviews/`: adversarial priority verdict and subsequent full audit-package review evidence.
- `RESEARCH_LOG.md`: timestamped decisions and separate completion estimates.
- `sources/PINNED_MANIFEST.json`: exact upstream source pin and hashes. The clone `/Users/alec/Desktop/math` was read-only; builds used project-local copies.
- `receipts/`: nonsecret build, review/hash and owned-main publication receipts.

The complex structure is retained in the GH object. The K-side object is the cubic Q-Gorenstein smoothing closure; equal dimension and volume alone do not suffice. Only closed polystable-point topology is claimed. No schemes/stacks/nonclosed-semistable upgrades or full Lean verification is asserted.

## Reproduction

Open `main.tex` in Codex's built-in LaTeX editor and compile. To export a standalone PDF with the installed Tectonic 0.16.9: `tectonic --keep-logs main.tex`, then copy `main.pdf` to `paper.pdf`. Compilation is not mathematical proof. The built-in compiler and the exported PDF are separately checked.

Run `python3 reproducibility/verify_constants.py` with Python 3 (standard library only). It reproduces exact rational tail and fourfold constants; it does not verify the full gap theorem. To rebuild upstream sources, obtain public openai/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a and copy the two family037 manuscript directories into a temporary/project-local directory. Run `tectonic --keep-logs paper.tex` inside each `build` directory. Do not build in the source clone. Upstream build instructions and inputs remain the original authors'.

Third-party PDFs, publisher previews and HTML/text reading caches under `sources/` and `references/` are retained locally as evidence and excluded from repository/deposit payloads absent a redistribution license. The original notes and source are the owned findings. Internal AI reviews are not conventional human peer review. No external individuals were contacted.

## Priority source

[Primary author page](https://sites.google.com/uic.edu/jzhao/research), [public KSZZ manuscript](https://drive.google.com/file/d/1eB16wLGE2G5QrbV-pUDmw_ieLMiLlOcO/view). PDF dated September30 2026, downloaded October6 2026 PDT; earliest actual public posting not established. SHA256 6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e. Its proof is distinct from the gap route. Current public exact-result overlap and the inherited reduction preclude our new-resolution claim, without a blanket ban on genuinely new alternative proofs.
