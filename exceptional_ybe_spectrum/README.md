# Exceptional unitary Hecke dimension spectrum

This package accompanies the unrefereed paper

> Alec Kriebel, *Low-Schmidt Rigidity and Tensor-Local Constraints in the
> Exceptional Unitary Hecke Yang--Baxter Class*, version 1.0.1,
> 29 July 2026.

The complete spectrum of the exceptional family
\[
\left[e^{i\pi/3},\frac12,d\right]
\]
remains open. The paper establishes exact structural constraints:
abstract
Jones--Wenzl multiplicities permit every even \(d\), while any
hypothetical \(d=6\) solution must have operator-Schmidt rank at least
four, be nonrestrictable, have scalar intersection of its two leg
commutants, and avoid the two broad construction classes isolated in the
paper. For any candidate with \(d\equiv2\pmod4\) and
\(\operatorname{OSR}(H)=4\), both intrinsic joint-sandwich maps must be
singular.

## Read and verify

- Typeset paper:
  [`output/pdf/exceptional_ybe_constraints.pdf`](output/pdf/exceptional_ybe_constraints.pdf)
- TeX source: [`manuscript/main.tex`](manuscript/main.tex)
- Theorem dependency map:
  [`manuscript/THEOREM_DEPENDENCIES.md`](manuscript/THEOREM_DEPENDENCIES.md)
- Verifier manifest:
  [`manuscript/VERIFIER_MANIFEST.md`](manuscript/VERIFIER_MANIFEST.md)
- Supplement:
  [`manuscript/SUPPLEMENT.md`](manuscript/SUPPLEMENT.md)
- Priority audit: [`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md)
- Final hostile audit:
  [`reviews/manuscript_final_hostile_audit.md`](reviews/manuscript_final_hostile_audit.md)

Run the central deterministic exact suite from this directory:

```bash
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/run_frontier_paper_verifiers.py
```

The release run passes all 10 programs. Its retained output is
[`results/frontier_paper_verifier_suite_exact.txt`](results/frontier_paper_verifier_suite_exact.txt).
SymPy 1.14.0 is the only third-party dependency used by the central
suite; several component verifiers use the Python standard library only.

## Status

This is AI-assisted, unrefereed work. Exact programs verify the encoded
finite identities but are not peer review. The original numerical search
that discovered the earlier \(d=4\) witness was not preserved; no claim
in this paper relies on that search. Every new experiment in this package
has retained source, commands, seeds when applicable, and raw output.

No external researcher was contacted during this project.
