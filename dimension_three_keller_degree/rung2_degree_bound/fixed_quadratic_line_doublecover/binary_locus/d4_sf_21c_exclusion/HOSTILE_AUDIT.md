# Clean-room hostile audit of `D4-SF-21C`

**Clean-room reconstruction recorded (UTC):** 2026-07-26T04:35:00Z
**Primary `NOTE.md` first consulted:** not yet at the time this section was
written.
**Scope:** the normal form
\[
s^2=-5,\qquad
h=(p-sq)(sp-q),\qquad
R=(p-sq)^2(sp-q)
\]
and the full homogeneous determinant
\[
\det\!\left(L+zJH_2+z^2JH_3+z^3JH_4\right),
\quad H_4=(hp^2,hq^2,0).
\]
No primary proof formula or verifier was imported into the clean-room
script.

## 1. Pre-comparison reconstruction

Put \(P=hp^2,Q=hq^2\), and
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
Their exact gcd is a nonzero scalar multiple of \(pR\).  Dividing by
\(pR\) gives
\[
\bar\alpha=-6sq,\qquad
\bar\beta=-6(4p+sq),\qquad
\bar\gamma=8q(sp-q).
\]
Consequently the full \(E_7\) contact equation is
\[
\bar\alpha\,U_r+\bar\beta\,V_r+\bar\gamma\,T_r=0.
\]
Solving this equation in the complete homogeneous coefficient spaces
\[
\deg U_r=\deg V_r=2,\qquad \deg T_r=1
\]
gives rank \(9\) in \(15\) coefficients, hence a complete
six-dimensional contact space.  In clean-room coordinates
\((v_1,v_3,v_4,t_0,t_1,t_2)\),
\[
\begin{aligned}
V_r={}&v_1pq+v_3q^2+v_4qr,\\
T_r={}&t_0p+t_1q+t_2r,\\
U_r={}&\frac43\left(t_0+\frac{3s}{5}v_1\right)p^2\\
&+\frac4{15}\left(st_0+5t_1-\frac{15}{4}v_1+3sv_3\right)pq\\
&+\frac43\left(t_2+\frac{3s}{5}v_4\right)pr
  +\frac4{15}\left(st_1-\frac{15}{4}v_3\right)q^2\\
&+\frac4{15}\left(st_2-\frac{15}{4}v_4\right)qr .
\end{aligned}
\]
Integration in \(r\) retains arbitrary binary integration constants in
\((H_3)_1,(H_3)_2,(H_2)_3\); all remaining quadratic and linear
coefficients were also retained.

The resulting \(E_6\) system has \(22\) nonzero homogeneous coefficient
equations and is linear in the \(18\) lower variables that actually occur.
A complete projective scan over \(\mathbf F_7\), with \(s=3\), found exactly
the eight points of one projective line and no other consistent contact:
\[
v_4=t_2=0,\qquad
t_0=\frac34v_3,\qquad
t_1=-\frac{3s}{4}v_3.
\]
An independent slice scan over \(\mathbf F_{23}\), with \(s=8\), selected
the same lifted direction.  Exact characteristic-zero rank checks confirm
that the other three rank-seven candidates in the normalized \(v_3=1\)
slice,
\[
(t_0,t_1)=(1,-s),\quad
\left(\frac94,-\frac{3s}{4}\right),\quad
(2,-2s),
\]
all have augmented rank \(8\), whereas
\[
\left(t_0,t_1\right)
=\left(\frac34,-\frac{3s}{4}\right)
\]
has matrix and augmented rank \(7\).

Write the surviving plane as
\[
(v_1,v_3,v_4,t_0,t_1,t_2)
=\left(m,n,0,\frac34n,-\frac{3s}{4}n,0\right).
\]
The generic \(E_6\) matrix has rank \(7\) on this plane.  The gcd of a
complete family of independently reconstructed \(7\times7\) minors is
\[
32m^2+4smn+5n^2
=32\left(m-\frac{s}{8}n\right)
       \left(m+\frac{s}{4}n\right).
\]
Thus the two and only two nonzero rank-drop directions are
\[
m=\frac{s}{8}n,\qquad m=-\frac{s}{4}n.
\]
The origin \(m=n=0\) is a separate zero-contact chart, where the \(E_6\)
rank drops to \(5\).

These calculations were persisted in `audit_reconstruct_sympy.py` before
opening the primary note.  They establish the clean-room contact/rank chart
against which the primary exclusion is compared below.

## 2. Comparison and final verdict

**Verdict: PASS, with one bibliographic correction and no mathematical
qualification.**  I found no lost orbit, contact component, rank-drop
direction, boundary solution, or misuse of the plane Jacobian Conjecture.
The candidate theorem can be promoted from “hostile audit pending” to
“hostile audit passed.”  Its scope remains exactly one of the 26 canonical
high-incidence families; it is not a closure of the parent row or a new
universal degree bound.

### 2.1 Normalization and orbit checks

The modulus recomputes as
\[
(s+s^{-1})^2=-\frac{16}{5}.
\]
The two choices of the root of \(s^2=-5\) do not produce different
families.  The source involution \(q\mapsto-q\) sends
\[
h_s\longmapsto-h_{-s},\qquad R_s\longmapsto-R_{-s},
\]
and the signs are absorbed by invertible target scalings.  Interchanging
\(p\) and \(q\), together with the corresponding interchange of the first
two target coordinates, sends the doubled-factor presentation \(X^2Y\)
to \(XY^2\) up to a nonzero scalar.  A nonzero scalar multiplying \(R\)
is likewise removed by an invertible scaling of the third target
coordinate.

The frozen denominator independently records
\[
\gcd\bigl(J(Q,R),-J(P,R),J(P,Q)\bigr)\doteq pX^2Y
\]
for `D4-SF-21C`.  Within the source and target normalizations of that
denominator, I found neither a second orbit hidden by the choice of \(s\)
nor an omitted doubled-factor presentation.  This is an audit of this
canonical family, not an independent certification that the global
26-family denominator is complete.

### 2.2 Contact completeness

After the clean-room chart above was frozen, the primary coordinates
were found to agree through
\[
v_1=m,\qquad v_3=\frac{4s}{15}n,\qquad
t_0=\frac{s}{5}n,\qquad t_1=n,\qquad v_4=t_2=0.
\]
Thus the two clean-room rank-drop directions
\[
v_1=\frac{s}{8}v_3,\qquad v_1=-\frac{s}{4}v_3
\]
are exactly the primary directions
\[
(m,n)\sim(-1,6),\qquad (m,n)\sim(1,3),
\]
respectively.

The primary proof does not infer contact completeness from a generic
rank computation.  Its highest-\(r\) equations first force both
degree-one contact coordinates to vanish.  Four global left-kernel
identities for the remaining full coefficient matrix then force the two
relations defining the plane.  These are polynomial identities, with no
division by a minor, so they remain valid on every rank-drop locus.  On
that plane, the pivot substitution retains arbitrary free lower
coefficients and is substituted back into every \(E_6\) equation.
Consequently:

- the four left-kernel conditions give necessary equations everywhere;
- the all-equation back-substitution gives sufficiency on the plane;
- the factor
  \[
  \Delta=(m-n/3)(m+n/6)
  \]
lists both and only the nonzero rank-six directions; and
- the origin is separately solved at rank five.

This closes the possible “generic chart only” and “one rank-drop
direction omitted” failure modes.

### 2.3 Independent lower-degree replay

The clean-room determinant was descended independently on the contact
plane, choosing its pivots dynamically rather than importing the
primary pivot lists.  It reproduced:

1. rank seven generically, rank six at both nonzero boundary directions,
   and rank five at the origin;
2. two generic \(E_5\) obstructions whose resultants, up to nonzero
   normalization, are pure ninth powers of \(n\) and \(m\);
3. the exact obstruction
   \[
   [p^3r^2]E_5=-\frac{108}{5}
   \]
   from a fresh six-pivot solve at each of
   \((m,n)=(1,3)\) and \((-1,6)\); and
4. at the origin, the two successive exact squares
   \[
   12b^2,\qquad \frac{8s}{3}\lambda^2,
   \]
   followed by the vanishing of every remaining nonbinary quadratic
   coefficient.

The terminal clean-room markers are

```text
D4_SF_21C_CLEANROOM_LOWER_PASS
D4_SF_21C_CLEANROOM_TOP_PASS
```

The exhaustive \(\mathbf F_7\) projective contact scan and the separate
\(\mathbf F_{23}\) slice scan are independent falsification checks of
the characteristic-zero chart.  They are not used as a proof over
\(\mathbb C\).

### 2.4 Zero-contact exit and Moh's hypothesis

Once the zero-contact chart makes every nonlinear term binary,
postcomposition by the inverse linear part gives
\[
(p,q,r)\longmapsto
\bigl(p+A(p,q),q+B(p,q),r+C(p,q)\bigr).
\]
The Keller determinant of this map is the Jacobian determinant of its
first two coordinates.  Their degrees are at most four, so Moh's proved,
unconditional plane result for degree strictly less than \(100\) applies.
This step
does not assume the open plane Jacobian Conjecture.  If \(\phi\) denotes
the resulting plane automorphism, the displayed lift has the explicit
polynomial inverse
\[
(P,Q,R)\longmapsto
\left(\phi^{-1}(P,Q),
R-C\!\left(\phi^{-1}(P,Q)\right)\right).
\]

The theorem is stated over \(\mathbb C\), exactly within the hypothesis
needed here; no extension to an arbitrary characteristic-zero base field
is silently asserted.

### 2.5 Primary certificate and mutation guard

The unmodified strict wrapper was rerun after the clean-room comparison.
Its final output was

```text
D4_SF_21C_INCIDENCE_PASS
D4_SF_21C_CONTACT_PLANE_PASS
D4_SF_21C_E5_E4_DESCENT_PASS
D4_SF_21C_SYMPY_STRICT_PASS
D4_SF_21C_PARI_DETERMINANT_BUILT
D4_SF_21C_PARI_CONTACT_PASS
D4_SF_21C_PARI_GENERIC_PASS
D4_SF_21C_PARI_BOUNDARY_PASS
D4_SF_21C_PARI_ZERO_PASS
D4_SF_21C_PARI_STRICT_PASS
D4_SF_21C_FULL_STRICT_PASS
```

The SymPy and PARI/GP programs separately reconstruct the determinant
and all three lower-rank charts.  The wrapper also changes the boundary
constant from \(-108/5\) to \(-107/5\) and confirms that this mutation is
rejected.

### 2.6 Editorial correction applied

The DOI metadata supplied by the publisher lists R. Biggers, T. T. Moh,
and M. Fried as authors of “On the Jacobian conjecture and the
configurations of roots,” and gives pages 140--213.  The primary note
originally listed T.-T. Moh alone and pages 140--212.  The primary note
now follows the publisher metadata.  This discrepancy did not affect the
theorem or the use of Moh's degree bound.
