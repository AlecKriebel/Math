# Verification report — version 1.0.0

**Mathematical verdict: PASS.** The supplied construction completely refutes
Knudson's Conjecture 2 as printed on p. 1629 of OWR 29/2008.

## Exact success criterion

A finite, valid simplex-wise filtration over F2 must produce a nonincident
persistence pair whose path count in the *fixed* matching of incident
persistence pairs differs from one. The witness has count zero. No geometric,
positive-dimensional, or closed-manifold restrictions appear in the source.

## Distinct checks

| Approach | Mechanism and evidence | Status / remaining gap |
|---|---|---|
| Source audit | Entire Knudson contribution pp. 1628–1630 read; p. 1629 visually checked from original PDF | PASS for original conjecture; live catalogue inaccessible |
| Mathematical reconstruction | Elder-rule component mergers; direct enumeration of six incidence arrows | PASS; no unresolved proof gap |
| Supplied verifier | Exact F2 reduction, separate union-find, acyclicity and complete path enumeration | PASS; exact output matches supplied file |
| Independent implementation | Reconstruct H0 inclusion ranks, mixed differences for barcode, rational and prime-field reductions | PASS; no dependency on supplied pairing algorithm |
| Boundary/interpretation checks | Essential class, critical endpoints, face-before-coface order, field signs, fixed versus modified matching | PASS; no minimality claim |
| Adversarial review | Separate AI agent challenges source interpretation and reconstructs proof | PASS; not external human peer review |
| Priority | 39 recorded targeted queries and primary-source comparisons | Scoped PASS; unpublished/unindexed work and unavailable full texts remain possible |

The independent verifier's field runs cover Q and primes 2, 3, 5, 7, 101.
They do not establish the all-field statement by exhaustion: the displayed
signed identities with pivot coefficients 1 prove it. Its relabeling check
covers all 24 permutations of the four vertices. Both programs were executed
normally and with optimization enabled, with byte-identical outputs.

## Strongest verified result

The filtration `a,b,c,d,cd,bd,ac` gives `P={(d,cd),(c,bd),(b,ac)}`,
`V_P={(d,cd)}`, and no path from `ac` to `b`. The phenomenon persists over any
field. The earlier pair `(c,bd)` has a unique path; cancelling it creates a
path for `(b,ac)` in a different matching. The latter fact cannot rescue the
fixed-field conjecture. This directly explains why algebraic elimination
and the original geometric matching need not agree.

## Artifact provenance and limitations

Original input SHA-256 values:

```text
aed912e2ba41f1ce6ed400a65d9c0cc6dc7cdd6361b7e87eb924d303607f1df6  inputs/gradient_path_counterexample.py
21982a0e73a6327e1b93573d7b4504157f1e489ca00aee9b149f12c70ba407bc  inputs/gradient_path_counterexample_output.txt
```

The new checker was written separately from the supplied reduction and
union-find code. The separate agent's rational calculation provides another
implementation check. Correctness is established by the elementary proof,
with code as reproducible supporting evidence. There is no proof-assistant
certificate or external human referee report. The catalogue mapping is
user-supplied; this package does not certify that website's present status.
See `priority_independent.md` for explicit coverage limits.
