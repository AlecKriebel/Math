# Sharp JC identifiability boundary - exact release package

This package certifies:

> Binary standard semi-directed `S_TC` level-2 networks with at most one
> triangle per blob are generically identifiable under the four-state
> Jukes-Cantor model modulo ordinary triangle redirection `T`.

It also certifies sharpness: the larger class `W_TC \ S_TC` contains the
all-`n` non-`T` Theta ambiguity.

The class names are locked as follows:

- `R_TC`: the supplied rooted DAG is tree-child;
- `W_TC`: the standard semi-directed topology has at least one tree-child
  rooted partner;
- `S_TC`: every admissible rooted partner is tree-child.

## Reproduce

```bash
python3 verify_release.py
```

Expected final status:

```text
"status": "ALL EXACT CHECKS PASSED"
```

The fail-closed verifier checks the SHA-256 manifest before and after all
computations. Generated console transcripts are deliberately outside the
manifest; all source, machine-readable certificate, reviewer, and report bytes
are hash-locked. It regenerates the 192-record seven-port classification; runs a
separately implemented seven-port replay; independently replays the root
reduction; validates the hash-locked independent audit of all 547 pointwise-cut
Bernstein factor certificates; verifies the frozen bounded nonroot atlas,
positive gluing, ordinary triangle redirection, Theta sharpness, and the final
dependency-closure review; and rejects any missing, changed, or unresolved
theorem dependency.

To recompute the complete independent pointwise-cut audit as well, run:

```bash
python3 verify_release.py --full-adversarial
```

The manuscript-ready proof is in
`report/FINAL_SHARP_BOUNDARY_THEOREM.md`.

A typeset seven-page version is available at
`report/FINAL_SHARP_BOUNDARY_THEOREM.pdf`.
