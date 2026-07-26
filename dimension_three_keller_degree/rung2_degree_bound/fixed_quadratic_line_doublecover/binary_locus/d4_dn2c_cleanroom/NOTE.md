# D4-DN-2C: complete \(E_7\) kernel and full-lower \(E_6\) projection

**Status:** exact clean-room candidate, checked by the scripts in this
directory.  It is intentionally independent of
`d4_dn2c_full_rebuild`.  It is not yet a two-method certification and it
is not a family exclusion.

The subsequent lower-order clean-room audit is recorded in
`LOWER_AUDIT.md`.  It closes the two plane interiors and the origin, and
independently closes the claimed \(F=G\) punctured overlap at \(E_3\).
It deliberately leaves one \(F\)-only \(E_4\) implication as an explicit
gap, so the scope remains short of a solo family exclusion.

**First exact run:** 2026-07-26T05:57:51Z.

Work over a characteristic-zero field.  For the component statement,
extend the field to contain a square root \(s\) of \(-2\).  Put
\[
 h=(p+q)^2,\qquad
 P=hp^2,\qquad Q=hq^2,\qquad R=h(p-2q).
\]
Write
\[
 H_4=(P,Q,0),\qquad H_3=(U,V,R),\qquad H_2=(A,B,T).
\]
The coefficients \(E_j\) are those of
\[
 \det\!\left(L+wJH_2+w^2JH_3+w^3JH_4\right).
\]

## Result

The complete \(E_7\) contact kernel is six-dimensional.  It has
coordinates \(a,b,c,d,e,f\) in which
\[
\begin{aligned}
 U&=U_0+rU_1+r^2U_2,&
 V&=V_0+rV_1+r^2V_2,&
 T&=T_0+rT_1+r^2T_2,\\
 U_2&=a(p+2q)+4b(p+q),&
 V_2&=aq,&
 T_2&=3b,\\
 U_1&=c(p^2+2pq)+d(pq+2q^2)
      +4ep(p+q)+4fq(p+q),\\
 V_1&=cpq+dq^2,&
 T_1&=3ep+3fq.
\end{aligned}
\]
Here \(U_0,V_0\) are arbitrary binary cubics and \(T_0\) is an
arbitrary binary quadratic at the \(E_7\) stage.

Restore all 18 variables which can enter \(E_6\):

- the \(4+4+3\) coefficients of \(U_0,V_0,T_0\);
- the three coefficients of each of \(A_r,B_r\); and
- \(L_{33}\).

Then the reduced projection of the full system \(E_6=E_7=0\) to the
six contact coordinates is
\[
 a=b=0,\qquad d=-2f,\qquad
 H(c,e,f)=3c^2+8ce+4cf+8e^2+4f^2=0.                 \tag{1}
\]
Over a field containing \(s^2=-2\), this is exactly the union of two
planes
\[
\begin{aligned}
 \Pi_+:\quad &a=b=0,\ d=-2f,\
 3c+(4+2s)e+(2-2s)f=0,\\
 \Pi_-:\quad &a=b=0,\ d=-2f,\
 3c+(4-2s)e+(2+2s)f=0.                              \tag{2}
\end{aligned}
\]
Their intersection is the line
\[
 a=b=0,\qquad c=d=-2k,\qquad e=f=k.                 \tag{3}
\]
The full-lower \(r^0\) block remains consistent both on the punctured
intersection and at the origin.  Thus no point of the two planes is an
artifact of a generic denominator.

## Exact \(E_7\) calculation

Set
\[
 \alpha=J(Q,R),\quad\beta=-J(P,R),\quad\gamma=J(P,Q).
\]
Direct coefficient calculation gives
\[
\alpha=-6pq(p+q)^3,\qquad
\beta=6p(p+q)^3(p+2q),\qquad
\gamma=8pq(p+q)^4.
\]
The three coefficient matrices in the \(r^2,r^1,r^0\) blocks of
\(\alpha U_r+\beta V_r+\gamma T_r\) have respectively
\[
\begin{array}{c|c|c|c}
\text{block}&\text{matrix size}&\text{rank}&\text{nullity}\\ \hline
r^2&6\times2&2&0\\
r^1&7\times5&3&2\\
r^0&8\times8&4&4.
\end{array}
\]
Primitive integer bases of their kernels are recorded by
`derive_e7_matrix.py`; substituting those bases gives the displayed
parameterization.

## Exact \(E_6\) projection

The coefficient vector of \(E_6\) is affine-linear in the 18 lower
variables.  Its two coefficients
\[
 [p^3r^3]E_6=-6a^2,\qquad
 [p^2qr^3]E_6=48b(a+b)
\]
force \(a=b=0\).

After this substitution the \(r^1\) block uses only the two lower
variables \((A_r)_{r},(B_r)_{r}\).  Its \(6\times2\) coefficient matrix
has constant rank two; the first two rows give the constant pivot \(36\).
The ideal of its \(3\times3\) augmented minors has Gröbner basis
\[
\left\{
\begin{aligned}
G={}&3c^2-6cd+8ce-8cf-8de-4df\\
   &\quad +8e^2-16ef-4f^2,\\
&(d+2f)^2
\end{aligned}
\right\}.                                           \tag{4}
\]
Its radical is \((d+2f,H)\).  The exact factorization
\[
 3H=
 \bigl(3c+(4+2s)e+(2-2s)f\bigr)
 \bigl(3c+(4-2s)e+(2+2s)f\bigr)
\]
gives (2).

For the \(r^0\) block, the five columns belonging to
\[
(A_r)_p,(A_r)_q,(B_r)_p,(B_r)_q,L_{33}
\]
have constant rank three; a \(3\times3\) pivot is \(216\).
Quotienting the seven-dimensional coefficient space by this fixed
image leaves a \(4\times11\) matrix \(B\) for the binary coefficients of
\(U_0,V_0,T_0\).

On \(\Pi_+\) the following is a specialization-safe atlas:
\[
\begin{array}{c|c|c|c|c}
\text{chart}&\operatorname{rank}B&
\operatorname{rank}A_0&
\operatorname{rank}[A_0\mid b_0]&\text{pivot}\\ \hline
e\ne f&2&5&5&108(s-1)(e-f)^2\\
e=f=k\ne0&1&4&4&18k\\
k=0&0&3&3&216.
\end{array}
\]
All \(3\times3\) augmented quotient minors vanish identically on the
first chart.  All \(2\times2\) augmented quotient minors vanish
identically on the second.  At the origin the quotient right-hand side
is zero.  Conjugation gives the identical atlas on \(\Pi_-\).
This proves sufficiency on every boundary, rather than only after
inverting \(e-f\).

## Scope and disclosure

This note determines the \(E_7/E_6\) contact projection for the single
frozen family D4-DN-2C.  It does **not** impose \(E_5,E_4,\ldots\), does
not exclude this family, and does not change the global quartic count or
the certified degree floor.

The derivation was produced with AI assistance.  The scripts encode
exact rational and algebraic-number calculations and are evidence about
that encoded algebra, not peer review.  This note has not been peer
reviewed.
