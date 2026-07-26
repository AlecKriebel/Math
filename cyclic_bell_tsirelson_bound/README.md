# The exact quantum value of a cyclic Bell operator

This package gives an analytic proof of Conjecture 1 in
[Perito et al., arXiv:2606.21362v3](https://arxiv.org/abs/2606.21362):

\[
\beta_{\mathrm Q}(\mathcal I_d)
=2\csc\!\left(\frac{\pi}{2d}\right)
\qquad(d\ge 2).
\]

The originating paper introduced the Bell family, conjectured the formula,
and constructed the attaining order-\(d\) strategy. The contribution claimed
here is the missing analytic upper bound. It is stronger than required: it
holds when every observable is an arbitrary unitary, without imposing its
\(d\)-th power to be the identity.

The key exact identity is

\[
\frac{|C|+|C^\dagger|}{2}\otimes I-\operatorname{Re}(C\otimes B)
=\frac12P^\dagger P,
\]

combined with the scalar extremum

\[
\max_{|z|=1}\sum_{y=0}^{d-1}|1+\omega^yz|
=2\csc\!\left(\frac{\pi}{2d}\right).
\]

The paper also includes the equality cases, a full proof that the polar-form
Bob observables have order \(d\), and the exact value
\[
\beta_{\mathrm Q}(\overline{\mathcal I}_d)
=2\csc\!\left(\frac{\pi}{2d}\right)+1
\]
for the corresponding barred functional. This value result does **not** prove
uniqueness, self-testing, or all-dimensional maximal randomness.

## Status and attribution

This is an unrefereed, AI-assisted research note. It should not be treated as
established mathematics until qualified experts have checked it independently.
The analytic proof is accompanied by symbolic and numerical verification
checks, not by a formal all-dimensional machine proof.

Authorship: **Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.**

## Package contents

- `main.tex` - complete manuscript.
- `output/pdf/cyclic_bell_tsirelson_bound.pdf` - rendered manuscript.
- `verify_certificate.py` - deterministic symbolic and numerical checks.
- `tests/` - independent regression tests.
- `certificate.json` - machine-readable theorem and dependency ledger.
- `MANIFEST.md` - claim-to-artifact map.
- `PRIORITY_AUDIT.md` - focused public-prior-art audit.
- `RESEARCH_LOG.md` - timestamped research record.
- `SOURCE_SNAPSHOT.md` - hashes of the supplied candidate package.
- `SHA256SUMS` - release hashes.

## Reproduce

Create an environment with Python 3.11 or newer, then run:

```text
python -m pip install -r requirements.txt
python verify_certificate.py
python -m unittest discover -s tests -v
tectonic main.tex --outdir build
```

The verification scripts use modest memory and are suitable for a laptop.
The all-\(d\) conclusion rests on the analytic functional-calculus argument in
the paper.
