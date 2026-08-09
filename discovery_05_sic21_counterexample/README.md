# Discovery 05: an explicit counterexample to SIC(21)

> **Technical precursor.** Discovery 07 is the canonical consequence paper.
> It incorporates the inverse-series lemma developed here and replaces this
> 21-dimensional, infinitely-many-exponents result with an explicit
> 14-dimensional obstruction at every positive exponent. This directory and
> its release timestamp remain public for provenance.

> **External supersession, 28 July 2026.** Roy van Rijn subsequently
> published a four-term counterexample to `SIC(3)`. That later result is not
> prior art against this 22 July release, but it supersedes the dimension-21
> benchmark. The historical content here is the explicit certificate and the
> scalar-parameter inversion lemma. See `PRIORITY_AUDIT.md`.

Status: **public branch draft; not peer reviewed**.

First public branch draft: **22 July 2026, 02:59:33 UTC**.

This directory gives an explicit characteristic-zero counterexample to the
Special Image Conjecture in dimension 21. In 42 polynomial indeterminates,

```text
A(xi,Z) = -sum xi_j g_j(Z),   b=Z_1,
```

has 72 monomials and total degree four. Every positive power of `A` belongs
to `ker(E_21)`, while `b*A^m` does not belong to `ker(E_21)` for infinitely
many `m`. The narrow quantitative novelty is one dimension: Exploration 03's
22-variable cubic model already implies an SIC(22) witness by Zhao's
homogeneous theorem. The present construction removes its homogenizing
variable and proves the scalar-parameter lemma needed for the resulting
nonhomogeneous linear block.

Start with [`NOTE.md`](NOTE.md). The source-specific novelty investigation is
in [`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md), the derivation chronology is in
[`RESEARCH_LOG.md`](RESEARCH_LOG.md), and the file inventory is in
[`MANIFEST.md`](MANIFEST.md). The rendered paper is
[`output/pdf/sic21_counterexample.pdf`](output/pdf/sic21_counterexample.pdf).

## Verification

The primary exact verifier uses SymPy 1.14:

```console
python3 -m pip install -r requirements.txt
python3 verify_symbolic.py
```

The exported certificate is generated deterministically and checked with only
the Python standard library:

```console
python3 export_certificate.py
python3 verify_exported_stdlib.py
```

A separate Node.js/BigInt implementation checks the collision and determinant
pencil without Python or a CAS:

```console
node verify_exported_node.mjs
```

The expected certificate SHA-256 is

```text
ed5a5a2069da28905403d2dd5b709951a22b863455608b5b4f8a5c9bdb784286
```

## Authorship and warning

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI).

Alec Kriebel is a complete amateur exploring the limits of AI-assisted
mathematics and cannot independently verify the claims. Nothing here should
be treated as established until experts in polynomial inversion and
Mathieu--Zhao subspaces have reviewed it. The priority audit is necessarily
provisional.
