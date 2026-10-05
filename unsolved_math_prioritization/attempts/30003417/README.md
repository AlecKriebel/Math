# Meager-ideal equalities: supporting proofs, no resolution

Problem **30003417 / OWR-15216-023**, rank **735**. Queue status **unsolved**, **5/5** approaches. **Zero original-solution credit.** The independent audit gives a scoped **PASS** for the supporting mathematics and provenance, with no mandatory corrections.

Work in **ZFC**. The target asks whether add(Mκ)=bκ and cof(Mκ)=dκ hold for every regular uncountable κ with 2^{<κ}=κ, using the bounded topology on 2^κ and unions of at most κ nowhere dense sets. Neither universal equality is proved here; no countermodel or independence result is obtained.

The retained proofs establish the known formulas add(Mκ)=min(bκ,cov(Mκ)) and cof(Mκ)=max(dκ,non(Mκ)), topological transfer, elementary special cases and a filter-union obstruction. The missing inequalities remain bκ≤cov(Mκ) and non(Mκ)≤dκ. These supporting results are not claimed as new resolutions.

- [Exact report and remaining gaps](author/safe_output/REPORT.md)
- [Retained supporting proofs](author/safe_output/RETAINED_PROOFS.md)
- [Independent proof-by-proof audit](audit/AUDIT_REPORT.md)
- [Current classification](release_status.json)

The dissertation's Question 2.6.1 concerns **inaccessible κ only**. Its dated discussion cannot certify openness for every regular successor. Bounded literature checks do not certify worldwide openness. Imported forcing constructions were not fully independently audited.

Both frozen archives and all their files are preserved byte-for-byte. Their pending-audit/no-remote-write fields record historical preparation, while the separate audit and this wrapper record the later disposition. Frozen references to exhausted describe the used five-turn budget; the actual queue cell is literally unsolved.

## Reproduce

Run `python3 verify_release.py` from any working directory. Only the standard library is required; no network, scholarly PDF or corpus is needed. The wrapper verifies publication inventory/hashes, frozen ZIPs and manifest members, classification, and both portable verifiers. It also supports `python3 -O verify_release.py`; the assertion-based author checker is always launched separately with assertions enabled and Python environment overrides ignored.

The 371 author and 1,086 independent finite order assignments are abstract order-logic regression checks, not models of set theory or proofs about infinite cardinals. The independent checker rejects 16 negative controls. Source-byte checks are **NOT_RUN** in portable replay; the separately recorded full-input audit is historical evidence, not a fresh source verification. The direct mathematical audit is not a formal proof-assistant certification.

The publication manifest binds every packet file except itself. Its external hash is recorded with publication verification. This unrefereed, AI-assisted research packet contains only authored work and public verification metadata. No source PDF, extract, raw dataset or private coordination is redistributed.
