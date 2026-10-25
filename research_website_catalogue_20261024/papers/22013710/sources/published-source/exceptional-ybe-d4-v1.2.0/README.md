# An exceptional four-dimensional unitary Hecke Yang–Baxter operator: a five-word Pauli–Clifford normal form

Submission package version 1.2.0 · 19 August 2026

Status: **DOI-bearing archival release; arXiv and journal submission pending**

The version-specific Zenodo DOI for this edition is
[10.5281/zenodo.22013710](https://doi.org/10.5281/zenodo.22013710). The
preceding version 1.1.3 remains archived at
[10.5281/zenodo.21971507](https://doi.org/10.5281/zenodo.21971507).

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

Thus \(J=XZ=-iY\), and \(\{I,X,Z,J\}\) is the real Pauli--Clifford basis.

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
the \(\eta=1/2\) Markov trace. Both inclusions between its trace radical and
the representation kernel follow from matrix-trace faithfulness, and the
quotient maps commute with the standard tower inclusions. Since GHR identify
the entire categorical endomorphism algebra with the braid image and
\(H_n(3,6)\), the construction gives precisely the faithful embeddings

\[
H_n(3,6)\hookrightarrow
\operatorname{End}\!\left((\mathbb C^4)^{\otimes n}\right)
\]

for all \(n\). Thus it is an ordinary unitary localization of the simple
tensor generator \(X\) of \(\mathcal C(\mathfrak{sl}_3,6)\), with
\(\operatorname{FPdim}(X)=2\). In particular, the Rowell--Wang localization
conjecture, as restated in GHR Conjecture 1.5, holds in the case the GHR paper
singled out as a possible counterexample.
The paper also proves that four is the minimum possible local dimension.
In dimension three, the Temperley--Lieb and complementary
Temperley--Lieb obstructions both have squared \(L^2\)-norm \(1/18\) with
respect to the exceptional trace.

Galindo and Rowell independently obtained the same existence and strict
localization conclusion, with dimension four smallest in Lechner's exceptional
family, through a quaternionic twisted-group-algebra construction in
[arXiv:2608.16865v1](https://arxiv.org/abs/2608.16865v1). Version 1.1.0 of
this package publicly disclosed the complete explicit solution on 28 July
2026; Galindo and Rowell report earlier private work and circulation. Version
1.2.0 treats the papers as independent concurrent work, makes no claim about
private discovery priority, and adds an exact comparison of the two local
formulas.

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
faithful \((3,2)\)-localization. An exact comparison with the displayed
generalized operator \(K_{\mathrm{GHR}}^{\mathrm{gen}}\) gives unnormalized squared Frobenius residuals
\((0,48)\) at shifts \((1,2)\), while the present active operator gives
\((24,0)\). This distinguishes their displayed \((3,1)\) and \((3,2)\)
tensor structures, not the matrices after tensor structure is forgotten.

There is also an intrinsic quaternionic form. With

\[
\mathsf A=-i\sqrt2 M,\qquad \mathsf B=iE,
\]

\[
U_{\mathrm K}=\frac{\mathsf A+\mathsf A\mathsf B}{2},\qquad
V_{\mathrm K}=\frac{\mathsf A-\mathsf A\mathsf B}{2},
\]

one has

\[
U_{\mathrm K}^2=V_{\mathrm K}^2=-I,\quad
U_{\mathrm K}V_{\mathrm K}=-V_{\mathrm K}U_{\mathrm K}=\mathsf B,
\quad
U_{\mathrm K}+V_{\mathrm K}+U_{\mathrm K}V_{\mathrm K}=-i\sqrt3 H.
\]

The paper displays a unitary \(S\) and proves exactly that

\[
R_{\mathrm K}=(S^\dagger\otimes S^\dagger)\Sigma R_{\mathrm{GR}}\Sigma
(S\otimes S),
\]

where \(R_{\mathrm{GR}}\) is independently encoded from Galindo–Rowell
Section 13 and \(\Sigma\) reverses the two four-dimensional local sites. Thus
the comparison is
with the opposite operator; it is not presented as plain local equivalence to
\(R_{\mathrm{GR}}\) under a convention that excludes site reversal.

## Global braid and link consequences

Put

\[
\kappa=q-1=q^2=e^{2\pi i/3}.
\]

The exact partial traces of \(R\) and \(R^{-1}\) prove that
\((R,I_4,\kappa,2)\) is a Turaev enhancement. Its ordinary-trace invariant is

\[
\mathcal J_R(\widehat\xi)
=\kappa^{-\operatorname{wr}(\xi)}2^{-n}\operatorname{Tr}(\rho_n(\xi)).
\]

The Hecke relation gives \(R-qR^{-1}=\kappa I\), hence

\[
\mathcal J_R(L_+)+\mathcal J_R(L_-)=\mathcal J_R(L_0),
\qquad
\mathcal J_R(L)=2P_{\mathrm H}(L;i,i).
\]

The original Lickorish–Millett normalization was checked line by line, giving

\[
\mathcal J_R(L)
=2(-1)^{c(L)-1}(-2)^{d_2(L)/2},
\]

where \(d_2(L)\) is the mod-2 first-homology dimension of the oriented triple
cyclic cover branched over \(L\). Also \(R^3=-I\) and \(R^6=I\), so a local
three-twist change negates the invariant and a six-twist change preserves it.

The local opposite comparison extends to every strand number. A tensor-site
reversal first sends generator \(i\) to generator \(n-i\); conjugation by the
Garside half twist removes that index reflection. Thus the five-word and
Galindo–Rowell representations are unitarily equivalent on the same braid
word. Through this equivalence, the cited Family III results transfer finite
images and Clifford structure in a fixed conjugated Pauli frame; the
Galindo–Rowell metric-family algorithm gives exact deterministic
polynomial-time evaluation of the enhanced invariant. The scalar enhancement
and HOMFLYPT specialization above are direct calculations from the five-word
matrix. The full quaternionic tower has dimension
\(4^{n-1}\); \(H_n(3,6)\) is its braid-generated subalgebra, not asserted to be
the entire tower.

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
.venv/bin/python verify_concurrent_equivalence.py
.venv/bin/python verify_braid_link.py
```

- `verify_exact.py` uses only the Python standard library and directly
  multiplies sparse exact matrices over
  \(\mathbb Q(\sqrt2,\sqrt3,i)\), including the two dimension-three
  obstructions, both partial traces, the literal active and GHR operators,
  their Hecke relations and exact generalized residual table, the
  six-dimensional three-strand Hecke image, the explicit sitewise-swap
  factorization, and far commutativity.
- `verify_tensor_words.py` never constructs a matrix. It verifies the
  involution relations and all 18 coefficients of the generic cubic
  residual in the abstract Pauli algebra.
- `verify_supplied.py` is the supported, optimization-safe SymPy route and
  requires exactly SymPy 1.14.0 and mpmath 1.3.0.
- `verify_concurrent_equivalence.py` separately encodes the five-word
  operator, literal Galindo–Rowell tensor placements, site swap, displayed
  unitary, and intrinsic Family III factorization over
  \(\mathbb Q(\sqrt2,\sqrt3,i)\).
- `verify_braid_link.py` rechecks the intrinsic factorization, `S`-unitarity,
  and exact two-site comparison, then checks the enhancement partial traces,
  matrix skein relation, local order, the two-strand examples, the figure-eight
  and Borromean closures, the standard-frame non-Clifford witness, Pauli
  quarter-turns, Clifford normalization, and the site-reversal and Garside
  conjugacies for every generator at \(n=3,4\), all in exact arithmetic.
- `verify_supplied_original.py` is the byte-for-byte original discovery-era
  checker. It uses Python assertions and is retained only for provenance, not
  execution.
- `test_failure_modes.py` rejects optimized execution and includes selected
  deliberate mutations of each supported route to confirm that those
  mutations are detected.
- `verify_checksums.py` validates the package-local manifest without allowing
  absolute or parent-directory paths.
- `verification_output.txt` is the frozen successful reference run.

All supported checks use explicit failures and reject optimized Python. The
finite programs check the stated matrix, word, trace, obstruction, and
generalized-operator identities. Tower faithfulness, all-strand conjugacy, the
dimension-three classification reduction, and source-based topological and
concurrent-work interpretations remain printed mathematical or literature
arguments.

The [typeset paper](output/pdf/exceptional_ybe_d4.pdf), [concurrent-work and
chronology record](CONCURRENT_WORK_AND_CHRONOLOGY_v1.2.0.md),
[global-braid source audit](GLOBAL_BRAID_SOURCE_AUDIT_v1.2.0.md),
[topological normalization audit](TOPOLOGICAL_NORMALIZATION_AUDIT_v1.2.0.md),
[global-strengthening adjudication](GLOBAL_STRENGTHENING_ADJUDICATION_v1.2.0.md),
[Section 9 hardening adjudication](SECTION9_HARDENING_ADJUDICATION_v1.2.0.md),
[historical priority audit](PRIORITY_AUDIT.md), [v1.1.3 correction
audit](CORRECTION_AUDIT_v1.1.3.md), [historical frontier-review
adjudication](REVIEW_ADJUDICATION_v1.1.2.md), [historical revision
audit](REVISION_AUDIT.md), [source snapshot](SOURCE_SNAPSHOT.md), and
[research log](RESEARCH_LOG.md) are included.

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

Operational Zenodo, arXiv, and journal handoff documents are retained only in
the private workspace and deliberately excluded from the public source ZIP.
The licenses are CC BY 4.0 for the manuscript/documentation and MIT for
verifier/runner code.

## Scope and status

The complete construction was publicly released in version 1.1.0 at
2026-07-28T04:10:58Z. Galindo–Rowell arXiv v1 was submitted at
2026-08-17T17:47:15Z, and its independent Family III construction gives the
same existence and strict-localization conclusion, with dimension four
smallest in Lechner's exceptional family. The public chronology establishes earlier
documented public disclosure by Kriebel; it does not adjudicate reported
earlier private work. The result gives examples in every base dimension
\(4m\) after tensoring with identities; dimensions \(6,10,14,\ldots\) remain
open. No claim of private discovery priority, uniqueness, or classification in
every even dimension is made. Substantive generative-AI use is disclosed in
the paper; the human author determines the released scope and claims and
assumes responsibility for the manuscript and verification package.
