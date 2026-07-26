# Full contact exclusion for `D4-DN-1CC`

**First banked:** `2026-07-26T03:58:02Z`
**Status:** certified family-level exclusion.  Two exact implementations
and an independent hostile reconstruction pass; not peer reviewed.

## Statement

Let \(k\) be an algebraically closed field of characteristic zero.  In the
fixed-quadratic line-double-cover row, take the frozen delta-four
doubled-nonbranch representative
\[
 h=(p+q)^2,\qquad
 P=hp^2,\qquad Q=hq^2,\qquad
 R=(p+q)(2p^2+pq+2q^2).
\]
There is no Keller counterexample having these top forms.

More precisely, the complete \(E_7\)-contact space has dimension six.
The \(E_6\) equations cut it set-theoretically to the single affine line
\[
 U=U_0-\frac23\kappa p(p+q)r,\qquad
 V=V_0+\frac23\kappa q(p+q)r,\qquad
 T=T_0+\kappa(-p+q)r,
\]
where \(U_0,V_0\) are arbitrary binary cubics and \(T_0\) is an arbitrary
binary quadratic.  The chart \(\kappa\ne0\) is inconsistent at \(E_4\).
On the boundary \(\kappa=0\), \(E_4\) removes every nonlinear
\(r\)-dependent term, so the map exits to a plane Keller map with a
triangular third coordinate and is an automorphism.

This closes one of the 26 frozen high-incidence canonical families.  It
does not by itself close the global quartic row or improve the universal
degree floor.

## Complete \(E_7\) parameterization

Put
\[
 \alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad \gamma=J(P,Q).
\]
Directly,
\[
\begin{aligned}
\alpha&=-6pq(p+q)^2(2p+3q),\\
\beta&=-6pq(p+q)^2(3p+2q),\\
\gamma&=8pq(p+q)^4.
\end{aligned}
\]
Write
\[
\begin{aligned}
U&=U_0+rU_1+r^2U_2+u_3r^3,\\
V&=V_0+rV_1+r^2V_2+v_3r^3,\\
T&=T_0+rT_1+r^2T_2 .
\end{aligned}
\]
The identity
\[
E_7=\alpha U_r+\beta V_r+\gamma T_r=0
\]
splits by powers of \(r\).  Its three coefficient matrices have ranks
\(2,3,4\) on spaces of dimensions \(2,5,8\), respectively.  Thus
\(u_3=v_3=0\), and the remaining six parameters may be named
\((d,z,x,y,a,b)\), with
\[
\begin{aligned}
U_2={}&\left(\frac8{15}z-d\right)p
       \left(\frac49z-\frac23d\right)q,\\
V_2={}&\left(\frac4{45}z+\frac23d\right)p+dq,\qquad T_2=z,\\
U_1={}&\frac{24a+4b-45x+30y}{45}p^2\\
 &+\frac{12a+16b-18x-15y}{27}pq
 +\frac{2(2b-3y)}9q^2,\\
V_1={}&\frac{2(6a-4b+45x-30y)}{135}p^2+xpq+yq^2,\\
T_1={}&ap+bq.
\end{aligned}
\]
Because these ranks and the displayed substitution are checked, this is a
parameterization of the full contact space, not an ansatz.

## \(E_6\) leaves one line

The \(r^3\)-coefficient of \(E_6\) is
\[
\begin{aligned}
&\frac{20}{27}(3d-2z)^2q^3
+\frac23(15d^2-16dz+8z^2)pq^2\\
&\quad+\frac2{45}(225d^2+56z^2)p^2q
+\frac4{135}(15d+2z)^2p^3.
\end{aligned}
\]
Its two extreme coefficients give
\[
3d-2z=15d+2z=0,
\]
and hence \(d=z=0\).  There is no missing nonzero-\((d,z)\) pivot chart.

Let \(A_{r^2}=a_r r^2\) and \(B_{r^2}=b_r r^2\).  The two extreme
coefficients of the remaining \(r^1\)-part of \(E_6\) are
\[
\frac{10}{27}(-2b+3y)^2,\qquad
\frac{2}{1215}(6a-4b+45x-30y)^2.
\]
They imply
\[
b=\frac32y,\qquad a=\frac{12y-15x}{2}.
\]
After this substitution, any three of the four middle equations form an
augmented \(3\times3\) determinant
\[
32400(x-y)^2.
\]
Consequently \(x=y\), \(a=-3y/2\), and \(b=3y/2\).  Setting
\(y=2\kappa/3\) gives exactly the affine line in the statement.  Conversely,
the complete \(E_6\) system is consistent on that line and forces
\[
A_{r^2}=B_{r^2}=\frac{\kappa^2}{45}r^2.
\]

This proof is set-theoretic, which is what the exclusion requires.  No
squarefreeness or radical-ideal assertion is being smuggled in: over a
field, \(c^2=0\) directly implies \(c=0\).

## Lower descent and the pivot boundary

Restore arbitrary binary \(U_0,V_0,T_0\), arbitrary binary parts of
\(A,B\), all six nonbinary quadratic coefficients of \(A,B\), and a
general \(3\times3\) linear part \(L\).

On \(\kappa\ne0\), the exact \(E_6\) system has rank six and is consistent.
After its complete solution, two coefficients of \(E_4\) are
\[
[pr^3]E_4=[qr^3]E_4=\frac{16}{135}\kappa^4.
\]
Thus this chart is empty.  This is stronger than an \(E_5\)-then-\(E_4\)
descent: imposing \(E_5\) cannot repair a nonzero coefficient of \(E_4\).

The rank drops at \(\kappa=0\), so that boundary is recomputed rather than
obtained by specializing a generic-pivot formula.  The exact \(E_6\) rank
is five, and
\[
\begin{aligned}
[p^3r]E_4&=\frac2{135}(15b_{qr}+2L_{33})^2,\\
[q^3r]E_4&=\frac{10}{27}(3b_{qr}-2L_{33})^2.
\end{aligned}
\]
Hence \(b_{qr}=L_{33}=0\).  The complete \(E_6\) formulas then set
\[
a_{pr}=a_{qr}=a_{rr}=b_{pr}=b_{qr}=b_{rr}=0.
\]
All nonlinear terms are therefore binary.

For completeness, this last exit does not assume the plane Jacobian
Conjecture.  First subtract \(F(0)\).  Since a Keller map has \(L\)
invertible, postcompose by a linear map carrying its \(r\)-column to
\((0,0,1)^t\).  The map becomes
\[
(g_1(p,q),g_2(p,q),r+g_3(p,q)).
\]
Its constant Jacobian says that \((g_1,g_2)\) is a plane Keller map of
degree at most four.  Moh's unconditional theorem for plane Keller maps
of degree strictly less than \(100\) makes that plane map an
automorphism, and the displayed triangular extension is then an
automorphism.

## Completeness and boundary certificate

The stable denominator inside this representative is:

| ID | chart | outcome |
|---|---|---|
| `DN1CC-C1-NZ` | \(\kappa\ne0\) | empty by \(E_4\) |
| `DN1CC-C1-Z` | \(\kappa=0\) | binary nonlinear exit; automorphism |

The certificate checks, in order:

1. all three \(E_7\) blocks and their ranks;
2. the full six-parameter \(E_7\) substitution;
3. the contact-only \(E_6\), including the \(r^3\) block that eliminates
   both \(r^2\)-contact parameters;
4. the extreme squares and augmented minor that leave one affine line;
5. the complete arbitrary-binary \(E_6\) solve on \(\kappa\ne0\);
6. the two \(E_4\) obstructions there;
7. an independent solve on the omitted pivot \(\kappa=0\); and
8. the two boundary squares and binary exit.

There are no denominator-clearing resultants and hence no extraneous
branches.  The only pivot is \(\kappa\), and both charts are explicit.

## Reproduction

Run:

```sh
./verify_strict.sh
```

The exact terminal markers are:

```text
D4_DN1CC_FULL_CONTACT_STRICT_PASS_ONE_LINE
D4_DN1CC_PARI_INDEPENDENT_PASS_ONE_LINE
D4_DN1CC_FAIL_CLOSED_STRICT_PASS
```

The first check reconstructs the weighted determinant in SymPy and performs
exact rank, minor, and coefficient checks.  The second independently
reconstructs it in PARI/GP and checks the displayed identities.  The shell
wrapper rejects interpreter errors and missing markers.

## Disclosure

This derivation and its verification code were produced with AI assistance.
The exact checks are evidence about the algebra encoded in the scripts;
they are not peer review.  The scope is the frozen representative
`D4-DN-1CC`, not all quartic Keller maps.
