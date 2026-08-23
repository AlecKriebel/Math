# Independent referee audit research log

## 2026-08-22T21:59:04-07:00 — Evidence freeze

- Scope: independent audit of release packet `full_referee_validation_packet_v1.0.7` for *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*.
- Source packet preserved at `source_snapshot/`; all executions are confined to `working_packet/` or further disposable copies.
- Supplied outer manifest verified before execution: 263/263 entries matched, exit status 0.
- Supplied inner repository manifest verified before execution: 198/198 entries matched, exit status 0.
- Original git state: branch `main`, one commit ahead of `origin/main`, with unrelated pre-existing modified/untracked paths outside this audit folder. Those paths will not be altered.
- Three independent review families started: core algebraic claims, nonlinear/PDE claims, and software/reproducibility semantics.
- Best-guess completion: **5%**. The evidence is preserved, but no mathematical conclusion or replay outcome has yet been accepted.

## 2026-08-22T22:07:00-07:00 — Full document read and independent dependency reconstruction

- Read all 1,217 lines of `main.tex` and all 971 lines of `supplement.tex`, rather than relying on the author-provided review maps.
- Rendered and visually inspected all 18 manuscript pages and all 18 supplement pages. Fonts are embedded; no clipping, overlap, missing page, or unreadable figure/table defect was apparent in the six full-document contact sheets. The dense supplement coefficient tables remain legible at page resolution.
- Confirmed that the packet reading PDFs and repository manuscript PDFs are byte-identical.
- Constructed `THEOREM_DEPENDENCY_MAP.md`, recording exact domains, conclusion types, direct dependencies, evidence types, and source-line locations.
- Static wrapper inspection found two host preflight gaps before execution: no `pdflatex` command, and the default `python` lacks required `pypdf`. The exact advertised wrapper will therefore be run and recorded as a non-pass; non-document stages will be pursued separately if the full environment cannot be made available transparently.
- No central contradiction has been found at this checkpoint. This is not a validity finding: certificate identities, verifier semantics, nonlinear reductions, boundary cases, and replays are still under audit.
- Best-guess completion: **24%**.
