# Exceptional four-dimensional Hecke Yang--Baxter operator

## Status

This folder is an exact-verification checkpoint for a proposed representative
of the exceptional class

\[
\left[e^{i\pi/3},\frac12,4\right].
\]

The matrix identities have been independently verified.  The literature and
equivalence audit is still in progress at this checkpoint, so this file makes
no unconditional priority claim.

The construction writes \(V=\mathbb C^2\otimes\mathbb C^2\), lets

\[
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\quad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\]

and defines

\[
\begin{aligned}
H={}&-\frac{ZIZZ+ZIJJ+JIZJ-JIJZ}{\sqrt6}
      -\frac{XIXX}{\sqrt3},\\
q={}&e^{i\pi/3},\\
R={}&\frac{q-1}{2}I_{16}+\frac{q+1}{2}H.
\end{aligned}
\]

Here a four-letter word denotes a Kronecker product.  Exact checks establish

\[
H^*=H,\quad H^2=I,\quad \operatorname{Tr}H=0,
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

The partial-trace identity is the extra input needed to identify the normalized
matrix trace with the \(\eta=1/2\) Markov trace throughout the Hecke tower.

## Verification

The two new checkers are deliberately independent of the discovery process:

```text
python3 verify_exact.py
python3 verify_tensor_words.py
```

`verify_exact.py` uses only the Python standard library and directly multiplies
the exact matrices over \(\mathbb Q(\sqrt2,\sqrt3,i)\).
`verify_tensor_words.py` never constructs a matrix; it checks a finite
18-word certificate in the abstract Pauli algebra.  `verify_supplied.py` is the
byte-for-byte source attachment and requires SymPy.

## Research warning

Alec Kriebel is a complete amateur and cannot independently certify the
mathematics.  This is an AI-assisted research artifact requiring expert review,
not an established result.  No outside researcher was contacted during this
independent audit.

