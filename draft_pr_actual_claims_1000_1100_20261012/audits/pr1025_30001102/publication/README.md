# Polynomial-time optimization and exact separation for rational mixed-integer bipartite covers

Alec Kriebel, independent researcher; ORCID
[0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).
Draft version 1.0, 12 October 2026.

The note proves exact rational optimization, strong separation and membership
in the actual convex hull of arbitrary bipartite mixed-integer covers, with
free-sign coordinates, arbitrary rational edge demands and any selected
integer coordinates. Total binary input size includes graph, numerators,
denominators, objective and rational query. Dimensions and denominators vary.
The hull is proved closed, including boundary membership.

Classical mixed proximity (Cook et al.1986), hybrid partial minimization
(Takamatsu–Hara–Murota2004), ring/scaling lineage (Murota2002/2003), exact
submodular minimization and GLS optimization/separation are credited. The
contribution is an explicit assembled rational application with localization,
exact LP completion and hull/encoding accounting. The bounded priority search
does not certify exhaustive originality. No separate subtree-hull conjecture,
compact extended formulation, strongly polynomial total algorithm or
arbitrary-real oracle model is claimed.

[The TeX source](research_note.tex), [PDF](research_note.pdf),
[supplement](SUPPLEMENT.md), [exact metadata](metadata.json) and
[evidence index](evidence/INDEX.md) form a draft preprint package. All six PDF
pages compiled without warnings and were rendered/visually inspected. Fresh
whole-package review 1 found two P3 presentation/boundary repairs; both were
applied. A NEW independent review 2 verified both repairs and the entire
package, finding zero actionable issues. The preprint is ready for immutable
publication; [final acceptance](evidence/FINAL_ACCEPTANCE.json) and
[current review state](evidence/CURRENT_REVIEW_STATE.json) record the gate.
The polynomial LP, submodular
and GLS algorithms are dependencies of the proof; diagnostic small-case
enumeration is not a full implementation or complexity proof.

With Python3.10+ and standard library only, from this directory run:

```text
python3 run_checks.py
python3 run_checks.py --output verification_receipt.json
```

The runner reproduces nine baselines and fifteen actual defective-source cases
in normal/-O/-OO modes, with exact complete output/exit comparison. The three
arithmetic sources are unchanged, and source faults are applied only in child
memory. No credentials, network, UID1000 account or external solver is needed.
Recorded execution used Python3.14.6 on macOS; other operating systems are not
tested here. The historical permission harness is preserved as history and not
replayed or simulated. Isolated Python flags are not a general security sandbox.

AI tools were used extensively in solving, verifying, source auditing and
preparation. This is unrefereed. Independent adversarial reviews are AI
reviews; conventional human peer review, journal acceptance and formal
proof-assistant certification are not claimed.
