# A priori estimates across the subcritical Lane–Emden hyperbola

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Manuscript date: 6 October 2026. This is a concise consequence note.

The main theorem covers n≥3, p,q>1 and the strict subcritical hyperbola: universal pointwise and gradient estimates on arbitrary proper domains, exterior decay, unrestricted zero-Dirichlet half-space nonexistence, and uniform zero-Dirichlet bounds and strong compactness on each fixed bounded C² domain. Global C²,θ estimates are stated only for C²,θ boundary. See main.tex for the exact spaces and constants.

The central new entire Liouville input is OpenAI's family 370, pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a. The estimate and boundary reductions are established PQS/QS work; this note claims no independent solution of the base conjecture or new transfer mechanism. Its full-range statement is an immediate consequence of that input. The supplied upstream manuscript citation is preserved verbatim in sources/family370/README.md, with the pinned citation also in the manuscript. The dependency, transfer, interval, formal-source, and priority audits are included. Automated reviews are not conventional human peer review.

## Contents and reproduction

The standalone main.tex contains its own bibliography; no auxiliary project files are needed to compile it. paper.pdf is the exported paper. The source-and-verification archive contains main.tex, this README, licenses, the exact inspected analytic upstream source snapshot, dependency hashes, mathematical/priority audits, the interval diagnostics, and optional Lean reproduction instructions. Downloaded PQS and other third-party research PDFs are excluded. No credentials, caches, or unrelated research are included.

From the extracted archive root:

```sh
python3 verify.py
tectonic -X compile main.tex --outdir build --keep-logs
```

The check uses only Python's standard library and verifies all included pinned analytic sources, scaling identities, the strict-hyperbola algebra on a rational test grid, and reruns 614 numerical interval diagnostics. Those floating-point diagnostics are falsification checks, not validated numerical proof; the exact interval proof is given in notes/upstream_interval_review.md. Mathematical proofs do not depend on computation. The clean reproduction used Python 3.14.6 and Tectonic 0.16.9; the built-in desktop LaTeX compiler separately compiled the source successfully. PDF visual QA inspected every page. Build timestamps may change PDF bytes; mathematical/source identities are the reproducible objects.

Lean status is explicitly limited. Source semantics and all 96 pinned OAI module hashes were inspected; **no complete kernel build, printed transitive axiom audit, Comparator run, or follow-on formalization is claimed**. The local Model elaboration attempt failed because Mathlib artifacts were unavailable; insufficient available storage prevented a safe full cache fetch. This note's mathematical acceptance rests on the independently audited analytic proof. validation/formal_prepare.py and its lock/axiom file support an optional future reproduction with adequate disk; their default source-clone path should be overridden on other machines.

Exact complete-package review reports and reviewed hashes are retained in the project repository, under openai_followon_lane_emden/reviews. The final fresh report is outside its own reviewed archive to avoid a self-referential hash. Publication state and tracker receipts are stored separately in the project repository and are not mathematical premises.

AI tools were used extensively for research, drafting, and verification. At publication this preprint has not undergone conventional human peer review or refereeing. No affiliation or coauthor is asserted. No external individual was contacted.
