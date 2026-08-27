# Independent-referee repair matrix

Scope: findings in the 2026-08-27 independent report.  The report is audit
evidence, not an instruction source.  A row closes only after the repair and a
focused adversarial test pass; release closure additionally requires the final
integrated and complete-regeneration runs.

| ID | Finding | Disposition | Focused repair status |
|---|---|---|---|
| CODE-1 | No active derivation of the 405,216 four-port universe and 40/14/2 residue | Confirmed, load-bearing | **PASS:** graph-derived producer, separate full verifier, exact 23,054-case syzygy-rank boundary, and 6/6 coherent mutations |
| CODE-2 | Probe verifier checks integrity but not all 574,535 row semantics | Confirmed, load-bearing | **PASS:** independent graph/restriction/transport/observable replay of all rows and 7/7 coherent mutations |
| MATH-1 | Cut splits do not recover ordinary-vertex versus three-boundary-cycle decoration | Confirmed omitted case | **PASS:** positive-monomial tree--sunlet decoration lemma inserted before the local factor theorem |
| MATH-2 | Finite-cover localization omits the regular-germ/analytic-section step | Confirmed proof compression | **PASS:** fixed-type incidence stratification, full-rank projection, and physical analytic section made explicit |
| MATH-3 | Four directed theta types are asserted with an outsourced case split | Confirmed auditability gap | **PASS:** complete pole/source/sink and directed-cycle case split printed in the article |
| ROOT | Rooting invariance called literal map equality | Confirmed wording defect | **PASS:** physical image/germ invariance is stated only up to analytic physical reparameterization |
| CUT-TOPOLOGY | Five templates and 72 switching masks begin from frozen topology | Confirmed active-boundary gap | **PASS:** literal-graph derivation of 5 cores, 77 endpoints, 72 records, and 204 directions, with 3/3 mutations |
| H21-ACTIVE | Hardened 25-mutation audit omitted from active wrapper | Confirmed | **PASS:** active wrapper, sentinel, and regeneration-plan binding added |
| H14-GCD | Exponent-primitivity check takes a vacuous gcd | Confirmed verifier defect | **PASS:** actual exponent-difference content and \(x^3-y^3\) mutation |
| OPT/RANK | Standalone primary scripts use optimizable assertions and do not bind ranks to minor dimensions | Confirmed hardening defect | **PASS:** optimized Python refused and ranks bound to both selected minor dimensions |
| CUT-BLOCKED | Standalone final cut verifier returns zero for `PASS_BLOCKED` | Confirmed fail-open presentation | **PASS:** blocked status is nonzero and the runner requires the strict pass sentinel |
| REPRO-1 | Restoration report embeds an absolute workspace path | Confirmed portability defect | **PASS:** relative command plus byte-identical relocated-workspace regression |
| DISCLOSURE | Reproducibility prose overstates active reconstruction boundaries | Confirmed for reviewed bytes | **PASS:** paper, supplement, manifest, provenance, and referee brief state the exact independent boundaries |
| LIT-1--5 | Recent triangle, invariant, higher-level, companion-status, and convention comparisons | Verified against primary records | **PASS with disclosed metadata limit:** comparisons and bibliography corrected; K2P/tree--theta use immutable tags/commits because no persistent DOI was authorized |
| ISOLATION | Referee run denied network/writes but did not credential-deny every host read | Procedural limitation, not theorem defect | **PASS as disclosure:** copied Git-free runner is explicitly not an OS sandbox; reviewers are told to supply an external credential-free boundary |
| PDF/RELEASE | Rebuild, visual QA, archive/package reseal, immutable version binding | Downstream engineering | **PASS:** clean 54-command regeneration passed in 7,686 seconds at immutable proof snapshot `e4b13c57`; the final clean 14-check replay passed in 2,412 seconds; both PDFs, both source ZIPs, both proof archives, the 35-file Google Drive source copy, and the 600-file referee handoff independently verify |

Current theorem status: no counterexample was found, every mathematical or
code-boundary finding has a focused passing repair, and the clean integrated
and complete-regeneration replays pass.  The distribution export is sealed;
only human-controlled submission work remains.

Best-guess completion toward the mathematical classification goal: **100%**.
Best-guess completion toward the paper/certification/proof-archive goal: **100%**.
Best-guess completion toward the external journal/DOI release goal: **65%**.
