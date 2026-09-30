# 30000304: exceptional regenerative composition structures

**Unsolved, 3/5 approaches; partial results awaiting separate review.**

The [mathematical note](PARTIAL_RESULT.md) contains:

- A necessary identity showing that a genuinely simultaneous coalescent has at most one possible positive mutation rate admitting a regenerative ordering
- An exact, valid two-atom coalescent that passes the four-sample test and fails at five, demonstrating the remaining difficulty
- An all-sample exclusion for bounded-parent full-replacement coalescents with no Kingman component

The original unrestricted conjecture remains open in this package. The known non-simultaneous theorem, classical regenerative representation and coalescent recursion are credited. No novelty is asserted.

Reproduce 1,328 exact diagnostic assertions using Python 3's standard library:

```sh
python3 unsolved_math_prioritization/attempts/30000304/verify.py
```

See `verification.json` for hashes and exact fractions. The verifier uses labeled paintbox merger events and a freezing recursion, rather than substituting the desired identity as its implementation. Finite diagnostics do not prove the general mathematical claims.

`SOURCES.md`, `sources.json` and `source_record.json` preserve source scope and access qualifications. `readiness.json` and `RESEARCH_LOG.md` record the gates and attempt accounting.
