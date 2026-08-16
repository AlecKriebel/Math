# Exceptional four-dimensional Hecke Yang–Baxter operator

Submission package version 1.1.1 · 16 August 2026

## Result

This package gives an exact representative of the exceptional class

\[
\left[e^{i\pi/3},\frac12,4\right].
\]

Let \(V=\mathbb C^2\otimes\mathbb C^2\), and put

\[
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\quad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

If a four-letter word denotes a Kronecker product, define

\[
\begin{aligned}
H={}&-\frac{ZIZZ+ZIJJ+JIZJ-JIJZ}{\sqrt6}
      -\frac{XIXX}{\sqrt3},\\
q={}&e^{i\pi/3},\\
R={}&\frac{q-1}{2}I_{16}+\frac{q+1}{2}H.
\end{aligned}
\]

Exact checks and the printed proof establish

\[
H^*=H,\qquad H^2=I,\qquad \operatorname{Tr}H=0,
\]

\[
H_1H_2H_1-H_2H_1H_2=\frac13(H_1-H_2),
\]

and therefore

\[
R_1R_2R_1=R_2R_1R_2,\qquad
(R+I)(R-qI)=0,\qquad R^*R=I.
\]

The \((-1)\)-spectral projection \(P=(I-H)/2\) has rank eight and

\[
\operatorname{Tr}_{1}(P)=\operatorname{Tr}_{2}(P)=2I_4.
\]

The partial-trace identity identifies the normalized tensor-space trace with
the \(\eta=1/2\) Markov trace. Its trace radical is exactly the kernel of the
unital \(*\)-representation, and the maps are compatible with the standard
tower inclusions. Thus the construction gives faithful embeddings

\[
H_n(3,6)\hookrightarrow
\operatorname{End}\!\left((\mathbb C^4)^{\otimes n}\right)
\]

for all \(n\). Thus it is an ordinary unitary localization of the
\(\mathcal C(\mathfrak{sl}_3,6)\) Jones--Wenzl representation sequence.
The paper also proves that four is the minimum possible local dimension.
In dimension three, the Temperley--Lieb and complementary
Temperley--Lieb obstructions both have nonzero exceptional trace norm
\(1/18\).

## Simplified structure

With

\[
A=ZIZZ,\quad B=ZIJJ,\quad C=JIZJ,\quad D=JIJZ,\quad E=XIXX,
\]

the first four terms form one reflection

\[
M=\frac{-A-B-C+D}{2}.
\]

Here \(A,B,C\) commute, \(D=ABC\), and \(E\) anticommutes with all four.
Hence every

\[
H(\alpha,\beta)=\alpha M+\beta E,\qquad
\alpha^2+\beta^2=1,
\]

is a Hermitian involution. A complete 18-word certificate proves that the
cubic Yang--Baxter identity holds on this circle exactly at

\[
\alpha^2=\frac23,\qquad\beta^2=\frac13.
\]

After swapping the two qubits inside each four-dimensional site, the
\(16\times16\) operator has one spectator qubit and an active
\(8\times8\) \((3,2)\)-generalized Yang--Baxter operator. This is a structural
normal form. The global sitewise swap proves that its generalized braid
representation has the same kernel as the ordinary one, so it is also a
faithful \((3,2)\)-localization. This is not a claimed equivalence with the
known quaternionic \((3,1)\) construction.

## Reproduce the checks

Create a clean Python 3.14.6 environment, install the hash-locked wheels, and
run the complete suite:

```text
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: \
  -r requirements.txt
YBE_PYTHON=.venv/bin/python ./run_all.sh
.venv/bin/python test_failure_modes.py
.venv/bin/python verify_checksums.py
```

Or run the routes separately:

```text
.venv/bin/python verify_exact.py
.venv/bin/python verify_tensor_words.py
.venv/bin/python verify_supplied.py
```

- `verify_exact.py` uses only the Python standard library and directly
  multiplies sparse exact matrices over
  \(\mathbb Q(\sqrt2,\sqrt3,i)\), including the two dimension-three
  obstructions, both partial traces, the literal active operator and its Hecke
  relation, the explicit sitewise-swap factorization, the generalized
  Yang--Baxter equation, and far commutativity.
- `verify_tensor_words.py` never constructs a matrix. It verifies the
  involution relations and all 18 coefficients of the generic cubic
  residual in the abstract Pauli algebra.
- `verify_supplied.py` is the supported, optimization-safe SymPy route and
  requires exactly SymPy 1.14.0 and mpmath 1.3.0.
- `verify_supplied_original.py` is the byte-for-byte original attachment. It
  uses Python assertions and is retained only for provenance, not execution.
- `test_failure_modes.py` rejects optimized execution and deliberately mutates
  each supported route to confirm that scientific failures cannot pass.
- `verify_checksums.py` validates the package-local manifest without allowing
  absolute or parent-directory paths.
- `verification_output.txt` is the frozen successful reference run.

All supported checks use explicit failures and reject optimized Python. The
finite programs check the stated matrix, word, trace, obstruction, and
generalized-operator identities. Tower faithfulness, the dimension-three
classification reduction, and priority remain printed mathematical or
literature arguments.

The [typeset paper](output/pdf/exceptional_ybe_d4.pdf), [priority
audit](PRIORITY_AUDIT.md), [revision audit](REVISION_AUDIT.md), [source
snapshot](SOURCE_SNAPSHOT.md), and [research log](RESEARCH_LOG.md) are
included.

With [Tectonic](https://tectonic-typesetting.github.io/) installed, rebuild
the PDF with:

```text
./build_paper.sh
```

The build requires Tectonic 0.16.9 and uses the explicit default bundle v33.
See [VERIFICATION_ENVIRONMENT.md](VERIFICATION_ENVIRONMENT.md) for the fixed
environment. Generate deterministic manual-upload artifacts with:

```text
.venv/bin/python package_submission.py
```

The source ZIP contains exactly the verified `SHA256SUMS` allowlist plus the
manifest itself. The builder refuses unexpected files in `submission/`, so a
local virtual environment, cache, note, or unrelated file cannot be archived
silently.

The exact Zenodo, arXiv, and journal handoff fields are in
[ZENODO_DEPOSIT.md](ZENODO_DEPOSIT.md), [ARXIV_METADATA.md](ARXIV_METADATA.md),
and [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md). The licenses are CC BY
4.0 for the manuscript/documentation and MIT for verifier/runner code.

## Scope and status

A fresh audit through 16 August 2026 found no prior public ordinary
four-dimensional localization or equivalent five-word formula. The
construction therefore appears to answer the existence question in
[arXiv:2603.20158v1](https://arxiv.org/abs/2603.20158v1), but absolute
priority cannot be certified. It gives examples in all base dimensions
\(4m\) after tensoring with identities; the dimensions
\(6,10,14,\ldots\) remain open. No claim of
absolute priority, uniqueness, a classification in every even dimension, or
equivalence with the older quaternionic \((3,1)\) model is made. Substantive
generative-AI use is disclosed in the paper; the human author determines the
released scope and claims and assumes responsibility for the manuscript and
verification package.
