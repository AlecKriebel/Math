# Clean-room lower audit for D4-DN-2C

**Status:** exact, independently derived partial audit.  This directory
does not by itself prove the full family exclusion: the remaining local
gap is the \(F\)-only part of the punctured intersection at \(E_4\).

**UTC timestamp:** 2026-07-26.

This audit was derived without reading `d4_dn2c_full_rebuild`.

## Chart ledger

| frozen contact chart | clean-room status | exact mechanism |
|---|---:|---|
| \(\Pi_+\setminus\ell\) | closed | three lower-free \(E_5\) coefficients |
| \(\Pi_-\setminus\ell\) | closed | Galois conjugate of the preceding calculation |
| \(\ell\setminus\{0\}\) | partial | the \(F=G\) overlap is closed at \(E_3\); the \(F\)-only \(E_4\) implication remains outside this audit |
| origin | closed | all six \(r\)-dependent coefficients of \(A,B\) collapse |

Here \(\Pi_\pm\) and \(\ell\) are the planes and their intersection from
`NOTE.md`.

## Plane interiors

On \(\Pi_+\), solve the constant-rank \(E_6\), \(r^1\) block with pivot
\(36\).  The three coefficients
\[
 [p^3r^2]E_5,\qquad[p^2qr^2]E_5,\qquad[pq^2r^2]E_5
\]
are \((e-f)\) times three binary quadratics in \(e,f\).  The coefficient
matrix of those quadratics in the basis \(e^2,ef,f^2\) has determinant
\[
 -768(-22+\sqrt{-2})\ne0.
\]
Thus \(E_5=0\) on the chart \(e-f\ne0\) would force
\(e^2=ef=f^2=0\), a contradiction.  Conjugation closes
\(\Pi_-\setminus\ell\).

The calculation restores all \(E_5\)-only binary coefficients of
\(A,B\) and all entries of the linear part before extracting the three
coefficients.  See `verify_plane_interiors_e5.py`.

## Punctured intersection

Write the nonzero intersection parameter as \(k\).  Then
\[
\begin{aligned}
U_1&=2kp(p+q),&V_1&=-2kq(p+q),&T_1&=3k(p+q),\\
(A_r)_r&=2k^2,&(B_r)_r&=2k^2.
\end{aligned}
\]
The complete \(E_6,r^0\) system has a \(4\times4\) pivot
\[
23328k^4
\]
in the variables \(u_{c0},u_{c1},u_{c2},v_{c0}\).  The \(E_5,r^1\)
system has rank two and pivot \(-72k^2\), giving
\[
\begin{aligned}
(A_r)_p&=(A_r)_q+2(B_r)_p
 k(-3v_1+4v_2-3v_3),\\
(B_r)_q&=k(v_1-v_2).
\end{aligned}
\]
The \(E_5,r^0\) new-variable matrix has rank three and pivot
\(-864k^3\).

After dimensionless normalization, put
\[
\begin{aligned}
X&=t_0-t_1+t_2,\\
Z&=6v_1-9v_2+9v_3,\\
F&=2L-2t_1+4t_2+3v_1-6v_2+9v_3,\\
G&=6A-8L-8t_2+9u-12v_1+12v_2-18v_3 .
\end{aligned}
\]
The residual \(E_5\) equations factor into
\[
 FG=0
\]
and
\[
\bigl(3B-(2+2i)X-Z\bigr)
\bigl(3B-(2-2i)X-Z\bigr)=0.
\]
At \(E_4\), two lower-free \(r^2\) coefficients force \(X=0\); the two
quadratic branches therefore coalesce to \(3B=Z\).  On the \(G\)
component,
\[
[q^3r]E_4=\frac23
\bigl(2L_{33}-2kt_1+4kt_2+3kv_1-6kv_2+9kv_3\bigr)^2,
\]
so \(F=0\).  The reverse implication on the \(F\)-only component is the
one step not certified in this directory.

### Independent \(E_3\) closure of the overlap

On \(F=G=0\), localize at \(k\ne0\) and make the invertible source
change \(r_{\rm new}=kr\).  This normalizes \(k=1\); the remaining
coefficients are reparameterized without loss.  Exact coefficient
pivots at \(E_6,E_5,E_4\) are
\[
23328,\qquad -864,\qquad 36.
\]

After the \(E_4\) pivot, all \(r\)-containing coefficients of \(E_3\)
vanish.  Its four binary coefficients have a common factor
\[
\begin{aligned}
C={}&-4\ell_6+4\ell_7
2t_1v_1-4t_1v_2+6t_1v_3
-4t_2v_1+8t_2v_2-12t_2v_3\\
&-3v_1^2+12v_1v_2-18v_1v_3
-12v_2^2+36v_2v_3-27v_3^2.
\end{aligned}
\]
The determinant of the linear part factors as
\[
\det L=-\frac{C D}{144}
\]
for the exact polynomial \(D\) encoded in
`derive_overlap_e3.py`.  If \(C=0\), the linear part is singular.
If \(C\ne0\), divide the four \(E_3\) coefficients by \(C\).
Three quotient equations solve triangularly, with constant pivots, for
\[
b_1,\qquad a_2,\qquad \ell_6.
\]
Exact substitution into the fourth quotient makes it zero and forces
\(C=0\), contradicting the localization.  Hence the overlap has no
solution with \(\det L\ne0\).

`search_punctured_representative.py` supplies a separate diagnostic:
it constructs an exact \(E_4\) survivor with
\(\det L=1265/48\), for which the binary \(E_3\) coefficients are
\[
\left(\frac{1725}{4},\frac{23}{3},
-\frac{5819}{12},-\frac{184}{3}\right).
\]
This representative is evidence about the location of the obstruction,
not the proof; the symbolic common-factor argument is the proof.

## Origin

At zero contact, \(E_6\) first kills the \(r^2\) coefficients of
\(A,B\).  Its remaining kernel is
\[
\begin{aligned}
A_r&=x(p+2q)+4y(p+q),\\
B_r&=xq,\qquad L_{33}=3y.
\end{aligned}
\]
With arbitrary binary \(U_0,V_0,T_0,A_0,B_0\) and all other linear
entries restored, four lower-free \(E_4\) coefficients are
\[
\begin{aligned}
[p^3r]E_4&=-3x^2,\\
[p^2qr]E_4&=24y(x+y),\\
[pq^2r]E_4&=3(x+4y)(3x+4y),\\
[q^3r]E_4&=6(x+2y)^2.
\end{aligned}
\]
The first two already give \(x=y=0\).  Thus all six \(r\)-dependent
coefficients of \(A,B\) vanish and every nonlinear term is binary.  The
established plane/Moh exit then makes the map an automorphism.

## Scope and disclosure

This is a structural audit of one frozen family.  It is not a global
quartic exclusion and, because of the stated \(F\)-only gap, it is not
by itself a full D4-DN-2C exclusion.

The work was produced with AI assistance.  Exact scripts verify the
encoded algebra; they are not peer review.  This note has not been peer
reviewed.
