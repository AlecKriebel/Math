# Research log: unmarked finite resonance \(c^2=9\)

## 2026-07-25T07:22Z — orbit opened

Opened the exceptional finite resonance represented by
\[
H_4=((p-q)^2,(p+q)^2,0),\qquad R=x(p-3q).
\]
The residual source change \(q\mapsto-q\), followed by the first-two-target
swap, identifies \(c=3\) with \(c=-3\).

## 2026-07-25T07:28Z — complete raw kernel

Reconstructed raw \(E_7\) rank \(14\), nullity \(12\), fixed maximal minor
\(-1039973956284579840\), twelve exact kernel directions, independence minor
\(49152\), and a four-coordinate gauge determinant \(-36\). This produced
the eight-parameter normal form in `NOTE.md`.

## 2026-07-25T07:35Z — staged \(E_6\) compatibility

Found four division-free square certificates. In sequence they force
\[
g=0,\quad f=0,\quad D=-2e,\quad C=0.
\]
The certificates were first obtained from cleared polynomial left-kernel
pairings and then reduced to sparse literal coefficient combinations.

## 2026-07-25T07:41Z — lower solve and exit

The surviving \(E_6\) system has constant rank-eight minor \(5159780352\).
At \(E_5\), the column determinant splits off the sole remaining resonance
\(-6A+3B+48e+16w=0\). The resonant \(E_5\) system has constant rank-four
minor \(20736\). Two \(E_4\) coefficients then force first
\(\ell_{33}=3e^2\) and then \(\ell_{32}=0\), contradicting the only branch
on which \(\det L\) could be nonzero.

## 2026-07-25T07:49:45Z — independent reconstruction closed

SymPy and PARI/GP exact reconstructions passed. Added strict transcript
checking and fail-closed mutation tests. The finite \(c^2=9\) resonance is
excluded as an exact working theorem, subject to expert review.

## 2026-07-25T09:55:40Z — hostile audit passed

An independently written PARI/GP verifier reconstructed the raw orbit,
gauge legality, every staged \(E_6\) compatibility rank, the complete
\(E_5\) resonance split, both \(E_4\) exits, and the \(c=\pm3\)
conjugacy. The same coefficient minor stays nonzero through all
specializations, and all cleared left-kernel denominators were checked
polynomially. Strict and mutation-based fail-closed tests pass. Verdict:
PASS for this exact joint orbit.
