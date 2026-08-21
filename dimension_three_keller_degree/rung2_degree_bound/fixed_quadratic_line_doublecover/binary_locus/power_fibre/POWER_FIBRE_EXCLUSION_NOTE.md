# The exceptional power fibre contains no Keller counterexample

**Exact candidate checkpoint:** 2026-07-25T12:29:43Z  
**Status:** complete primary proof; pending independent hostile audit; not peer
reviewed.

## 1. Statement and scope

Translate a degree-four polynomial map so that its constant term is zero and
write
\[
F=L(p,q,r)^T+H_2+H_3+H_4,\qquad L\in\operatorname{GL}_3(\mathbb C),
\]
with \(H_i\) homogeneous of degree \(i\).  This note treats exactly the
constant-dependent Hilbert--Burch exception in the binary fixed-quadratic
line-double-cover row:
\[
H_4=(p^4,p^2q^2,0),\qquad (H_3)_3=p^3.              \tag{1}
\]

**Candidate theorem.**  Every Keller map on (1) is a polynomial
automorphism.  Equivalently, the exceptional power fibre contains no Keller
counterexample.

Most branches are stronger: no Keller map exists on them.  The only
surviving top branch exits through an unconditional low-degree plane theorem
and the classical birational Keller theorem.

## 2. Full top-identity parameterization

Put
\[
\det\!\left(L+zJH_2+z^2JH_3+z^3JH_4\right)
  =\sum_{j=0}^8E_jz^j.                              \tag{2}
\]
The Keller condition is \(E_j=0\) for \(j>0\).

Write
\[
\begin{aligned}
T_0&=c_0p^2+c_1pq+c_2q^2,&
U_0&=u_0p^3+u_1p^2q+u_2pq^2+u_3q^3,\\
A_0&=x_0p^2+x_1pq+x_2q^2,&
B_0&=y_0p^2+y_1pq+y_2q^2.
\end{aligned}
\]
The complete \(E_7=0\) solution is
\[
\begin{aligned}
(H_2)_3&=T_0+r(t_p p+t_q q)+t_tr^2,\\
(H_3)_1&=U_0+\frac43rp(t_p p+t_q q)+\frac43t_tpr^2.  \tag{3}
\end{aligned}
\]
The remaining entries are general:
\[
\begin{aligned}
(H_3)_2={}&V_0+r(v_4p^2+v_5pq+v_6q^2)
 +r^2(v_7p+v_8q)+v_9r^3,\\
(H_2)_1={}&A_0+r(a_p p+a_q q)+a_ar^2,\\
(H_2)_2={}&B_0+r(b_p p+b_q q)+b_br^2.               \tag{4}
\end{aligned}
\]

## 3. The branch \(v_9\ne0\)

The full calculation is recorded in `V9_EXCLUSION_NOTE.md`.  Its three
terminal obstructions are:
\[
\begin{array}{c|c}
\text{branch}&\text{necessary nonzero coefficient}\\ \hline
t_p\ne0 &[r^3]E_4=-\dfrac8{27}qt_p^4,\\[2mm]
t_p=0,\ c_1\ne0 &[q^2r^2]E_4=\dfrac43c_1^3v_9,\\[2mm]
t_p=c_1=0&
[r^2]E_3=-\dfrac23\ell_{32}v_9
(8c_0^2p-9c_0u_0p-6\ell_{31}p+6\ell_{32}q+9x_0p).
\end{array}                                         \tag{5}
\]
In the last row, \(\ell_{32}\ne0\) makes the displayed linear factor
nonzero, while \(\ell_{32}=0\) makes the first and third rows of \(L\)
collinear.  Thus no Keller map has \(v_9\ne0\).

## 4. The \(v_9=0\) orbit split

Set
\[
\ell=v_7p+v_8q.
\]
The diagonal stabilizer of (1), together with the induced diagonal target
changes, reduces \(\ell\) to exactly one of
\[
0,\qquad p,\qquad q,\qquad p+q.                    \tag{6}
\]
Indeed the two nonzero coefficients can be scaled independently; their
zero pattern is unchanged.  No equivalence between \(p\) and \(q\) is
assumed, and both are checked.

### 4.1. The \(q\) and \(p+q\) orbits

For either orbit, the top coefficients give
\[
t_q=0,\quad a_a=\frac29t_p^2,\quad
u_1=\frac43c_1,\quad u_2=\frac43c_2,\quad u_3=0.   \tag{7}
\]
The \(p^3q^3\)-coefficient of \(E_6\) and the \(p^2q\)-coefficient of
\([r^2]E_5\) then force \(t_p=0\).  Next,
\[
[q^4r]E_5=-\frac{16}{3}c_2^2,\qquad
[q^3r]E_4=\frac89c_1^3,                            \tag{8}
\]
so \(c_2=c_1=0\).

For \(\ell=p+q\), put
\[
A=-8c_0\ell_{32}-9\ell_{12}+9u_0\ell_{32}.
\]
Two coefficients of \([r]E_4\) are \(-2A/3\) and
\(-2(A-4\ell_{33}^2)/3\).  Hence \(\ell_{33}=0\), and then
\[
[q^2r]E_3=-\frac83\ell_{32}^2.                    \tag{9}
\]
Thus \(\ell_{32}=\ell_{33}=\ell_{12}=\ell_{13}=0\), so
\(\det L=0\).

For \(\ell=q\), \([r]E_4=0\) instead fixes
\[
\ell_{12}=\ell_{32}\!\left(u_0-\frac89c_0\right)
             -\frac49\ell_{33}^2.                 \tag{10}
\]
If \(\ell_{33}=0\), (9) again forces \(\ell_{32}=0\) and \(L\) is
singular.  If \(\ell_{33}\ne0\), successive coefficients of
\(E_4,E_3\) force
\[
v_4=v_5=v_6=\ell_{32}=0,
\quad
b_b=\frac12v_1,\quad v_2=\frac23c_0,\quad v_3=0,   \tag{11}
\]
after which
\[
[pq^2]E_3=\frac89\ell_{33}^3\ne0.                 \tag{12}
\]
Both \(q\)-containing orbits are therefore impossible.

### 4.2. The \(p\) orbit

Here \([r^3]E_5\) first gives \(t_q=0\), and \([r]E_6=0\) gives
\[
u_1=\frac43c_1,\qquad u_3=0,\qquad
u_2=a_a+\frac43c_2-\frac29t_p^2.                  \tag{13}
\]
Combining the last coefficients of \(E_6\) and \(E_5\) yields
\[
t_p(27a_a-2t_p^2)=0.                               \tag{14}
\]

If \(t_p\ne0\), a legal shear in \(r\) makes \(c_0=c_1=0\).
The complete top solution then has
\[
a_a=\frac2{27}t_p^2,\qquad
c_2=-\frac19t_p^2+\frac13t_pv_6.                  \tag{15}
\]
Two necessary coefficients are
\[
\begin{aligned}
[pq^3r]E_5
 &=-\frac{16}{81}t_p^2(t_p^2-t_pv_6+3v_6^2),\\
[r^3]E_4
 &=-\frac8{243}t_p^3(9pv_5+q(t_p+6v_6)).
\end{aligned}                                      \tag{16}
\]
The second identity forces \(v_5=0,v_6=-t_p/6\), and the first becomes
\(-20t_p^4/81\), a contradiction.

Now take \(t_p=0\).  The remaining top equations say
\[
a_av_6=0.                                          \tag{17}
\]
If \(a_a\ne0\), then \(v_6=0\); \([r^3]E_4\) forces
\(c_1=c_2=0\).  The complete lower solution successively gives
\[
\begin{aligned}
\ell_{32}&=\ell_{33}=0,\\
\ell_{12}&=a_a(y_1-b_bv_1),&
\ell_{13}&=a_a(b_p-b_bv_4),\\
\ell_{22}&=b_b(y_1-b_bv_1),&
\ell_{23}&=b_b(b_p-b_bv_4).
\end{aligned}                                      \tag{18}
\]
The last two columns of the first two rows are proportional, while the
third row is supported in the first column; hence \(\det L=0\).

If \(a_a=0\), then \([pq^3r]E_5=-16c_2^2/3\), so \(c_2=0\).
For \(c_1\ne0\), lower identities give
\(\ell_{33}=\ell_{13}=0\) and
\([pq^2r]E_4=8c_1^3/9\).  For \(c_1=0\),
\[
[p^2qr]E_4=\frac83\ell_{33}^2,\qquad
[pqr]E_3=-\frac83\ell_{32}^2.                     \tag{19}
\]
Thus \(\ell_{33}=\ell_{32}=0\), again making \(L\) singular.  The
\(\ell=p\) orbit is impossible.

### 4.3. The zero orbit

When \(\ell=0\), the top identities are especially short:
\[
[r]E_6=-\frac43p^2q
\{9a_ap^2-2(t_p p+t_q q)^2\}.                      \tag{20}
\]
Thus \(t_q=0,a_a=2t_p^2/9\), and then
\[
[r^2]E_5=-\frac89p^2qt_p^3.                       \tag{21}
\]
Consequently \(t_p=t_q=t_t=a_a=0\).

The third component now has the form
\[
F_3=\ell_{33}r+G(p,q),\qquad
G=p^3+c_0p^2+c_1pq+c_2q^2+\ell_{31}p+\ell_{32}q.  \tag{22}
\]

If \(\ell_{33}\ne0\), use the triangular source coordinate
\(w=F_3\).  Substituting
\[
r=\frac{w-G(p,q)}{\ell_{33}}
\]
leaves a plane Keller map in \(p,q\) over \(\mathbb C(w)\) of degree at
most \(6\).  The possible degree-six term is \(b_br^2\); every other
substituted term has smaller degree.

Suppose \(\ell_{33}=0\).  The Keller determinant cannot be nonzero at a
critical point of \(G\), so \(G\) has no critical point.  This special
cubic is elementary to classify:

- if \(c_2\ne0\), solve \(G_q=0\) for \(q\); the resulting \(G_p=0\)
  equation is a quadratic in \(p\) with leading coefficient \(3\), so it
  has a complex root;
- if \(c_2=0,c_1\ne0\), first solve \(G_q=0\) for \(p\), then solve the
  linear equation \(G_p=0\) for \(q\);
- hence \(c_1=c_2=0\), and absence of a critical point forces
  \(\ell_{32}\ne0\).

Therefore
\[
w=G=p^3+c_0p^2+\ell_{31}p+\ell_{32}q              \tag{23}
\]
is again a triangular source coordinate.  Eliminating \(q\) leaves a
plane Keller map in \(p,r\) over \(\mathbb C(w)\) of degree at most \(9\).
The degree-nine ceiling comes from a possible binary cubic term after the
degree-three substitution for \(q\).

In both cases the unconditional plane lower bound, after base change to
\(\overline{\mathbb C(w)}\), makes the plane map birational.  This is an
application of a proved finite degree bound, not an assumption of the
plane Jacobian Conjecture.  Hence \(F\) has generic degree one.  The
classical birational Keller theorem makes \(F\) a polynomial automorphism.

This completes every orbit in (6) and proves the candidate theorem.

## 5. Verification boundary

The strict primary wrapper
`verify_power_fibre_strict.sh` runs four exact SymPy certificates:

- `verify_power_fibre_v9_sympy.py`;
- `verify_power_fibre_v9zero_q_orbits_sympy.py`;
- `verify_power_fibre_v9zero_p_orbit_sympy.py`;
- `verify_power_fibre_v9zero_ellzero_sympy.py`.

They reconstruct (2) from the full coefficient family, verify every forcing
coefficient used above, check all singular-\(L\) leaves, and symbolically
confirm the plane degree ceilings \(6\) and \(9\).  The wrapper also rejects
optimized Python, so assertions cannot be silently removed.

The scripts do not prove the cited plane lower bound or the classical
birational Keller theorem.  Those are external mathematical inputs already
audited elsewhere in this program.  A separate hostile reconstruction is
still mandatory before this note is promoted.

## 6. Disclosure

This note and its verification code were produced with AI assistance.
Exact symbolic checks are evidence about the encoded algebra, not peer
review.  The theorem is deliberately labeled a candidate until an
independent audit has checked orbit completeness, every normalization,
function-field descent, and the distinction between “no Keller map” and
“Keller maps are automorphisms.”
