# Hostile independent audit: full-lower D4-DN-3 contact locus

UTC audit timestamp: **2026-07-26T04:41:40Z**

## Verdict

**PASS, with deliberately narrow scope.**  The encoded theorem may be
promoted as an exact contact-locus theorem for the frozen D4-DN-3 normal
form.  It is **not** an exclusion of D4-DN-3, is not a quartic degree bound,
and does not by itself produce or rule out a Keller counterexample.

Set-theoretically, the full \(E_6\) contact projection is exactly

\[
V\!\left(
 x_0,\ x_1,\ y_2-y_3,\
 9(y_0-y_1)^2+24(y_0-y_1)y_3+8y_3^2
\right).
\]

Over \(\mathbb C\), this is exactly two planes meeting in one line.

## Independence protocol

I reconstructed the result before reading the primary note, atlas, or
verification code.  The hostile verifier:

1. starts from
   \[
   h=(p+q)^2,\qquad P=hp^2,\qquad Q=hq^2,\qquad R=(p+q)^3;
   \]
2. independently computes the \(E_7\) coefficient syzygies and chooses a
   different contact-coordinate presentation;
3. rebuilds the weighted Jacobian determinant;
4. retains all 18 lower unknowns in a \(28\times18\) coefficient system,
   including zero monomial rows;
5. derives the contact radical and rank atlas from that reconstruction; and
6. imports no primary module or data file.

Only after those calculations agreed internally did I compare them with
`NOTE.md`, `ATLAS.json`, and the two primary verifiers.

## Exhaustive \(E_7\) reconstruction

The binary Jacobian minors independently simplify to

\[
\alpha=-6q(p+q)^4,\qquad
\beta=-6p(p+q)^4,\qquad
\gamma=8pq(p+q)^4.
\]

The three successive \(r\)-blocks have nullities \(0,2,4\).  A complete
basis used in the hostile calculation is

\[
\begin{aligned}
(U_2,V_2,T_2)
 &=x_0(-p,q,0)+x_1(4p/3,0,1),\\
(U_1,V_1,T_1)
 &=y_0(-p^2,pq,0)+y_1(-pq,q^2,0)\\
 &\quad+y_2(4p^2/3,0,p)+y_3(4pq/3,0,q).
\end{aligned}
\]

Thus all six contact parameters are present; no \(E_7\) branch is removed
by the parametrization.

## Radical certificate

The unspecialized \(E_6\) system has a constant \(5\times5\) pivot

\[
31104
\]

in the lower variables.  Consequently the first elimination step divides by
no polynomial in the contact parameters.  Lower-variable-free residuals
contain constant associates of

\[
x_0^2,\qquad 27x_0^2-24x_0x_1+8x_1^2.
\]

They force \(x_0=x_1=0\) set-theoretically.  After this substitution, the
four remaining pure-contact quadrics generate an ideal \(I_y\).  With

\[
d=y_2-y_3,\qquad
g=9(y_0-y_1)^2+24(y_0-y_1)y_3+8y_3^2,
\]

the exact Gröbner certificates are:

- every generator of \(I_y\) reduces to zero modulo \((d,g)\);
- \(d^2\) reduces to zero modulo \(I_y\); and
- \(g^2\) reduces to zero modulo \(I_y\).

The quadratic \(9z^2+24z+8\) is squarefree.  Hence \((d,g)\) is radical and
\(\sqrt{I_y}=(d,g)\).  This is a symbolic radical certificate, not a
floating-point factorization.

Writing

\[
c_\pm=\frac{-4\pm2\sqrt2}{3},
\]

the exact factorization is

\[
g=9\bigl((y_0-y_1)-c_+y_3\bigr)
     \bigl((y_0-y_1)-c_-y_3\bigr).
\]

Since \(c_+\ne c_-\), there are exactly two geometric planes over
\(\mathbb Q(\sqrt2)\), hence over \(\mathbb C\):

\[
(x_0,x_1,y_0,y_1,y_2,y_3)
 =(0,0,s+c_\pm k,s,k,k).
\]

They intersect on \(k=0\), namely
\((0,0,s,s,0,0)\).

## Full 18-variable atlas

The lower variables retained are:

- the six nonbinary quadratic coefficients of \(A,B\);
- the \(L_{33}\) coefficient;
- four binary cubic coefficients of \(U_0\);
- four binary cubic coefficients of \(V_0\); and
- three binary quadratic coefficients of \(T_0\).

The other binary \(A,B\) coefficients and the other entries of the linear
matrix remain symbolic in the reconstructed determinant.  They are not
silently set to zero.

The coefficient and augmented ranks, together with nonvanishing pivots, are:

| Chart | Conditions | coefficient/augmented rank | certified pivot |
|---|---:|---:|---:|
| \(P_+\) transverse | \(k\ne0\) | \(7/7\) | \(373248(7-5\sqrt2)k^2\) |
| \(P_-\) transverse | \(k\ne0\) | \(7/7\) | \(373248(7+5\sqrt2)k^2\) |
| plane intersection | \(k=0,\ s\ne0\) | \(6/6\) | \(-279936s\) |
| origin | \(k=s=0\) | \(5/5\) | \(31104\) |

These four charts cover the complete radical locus.  In particular, the
rank equalities provide a lower-variable lift at every contact point, so the
result is the actual set-theoretic projection and not merely the closure of a
necessary locus.  The intersection and origin systems were rebuilt directly,
not obtained by specializing a solution that had divided by \(k\).

## Earlier solver denominator

An earlier solved formula used the denominator

\[
D=s+\left(-\frac{10}{3}+2\sqrt2\right)k
\]

on the plus plane.  This is not a rank boundary.  The transverse safe pivot
above is independent of \(s\), and the hostile verifier additionally
specializes to

\[
k=1,\qquad s=\frac{10}{3}-2\sqrt2,
\]

where \(D=0\), and recomputes ranks \(7/7\).  Thus the missed line was an
artifact of that solver choice.

## Scope and loss audit

- The theorem concerns only the frozen D4-DN-3 normal form.
- The complete \(E_7\) nullity calculation rules out loss of a contact
  parameter within that normal form.
- The \(28\times18\) \(E_6\) system retains every stated lower unknown.
- The constant initial pivot introduces no exceptional contact divisor.
- The four rank charts cover both planes and their entire intersection.
- The conclusion is only that all and only these contacts lift through
  \(E_6\).  Lower weighted equations remain to be analyzed.  Therefore no
  Keller-map exclusion is claimed.

## Executed checks

Primary strict verification, invoked from its directory:

```text
D4_DN3_FULL_E6_ELIMINATION_PASS_TWO_PLANES_18_LOWER
D4_DN3_PARI_FULL_18_LOWER_ATLAS_PASS
D4_DN3_FULL_REBUILD_STRICT_PASS
```

Independent hostile strict verification:

```text
D4_DN3_HOSTILE_FULL_E6_CONTACT_ATLAS_PASS
D4_DN3_HOSTILE_AUDIT_STRICT_PASS
```

The primary wrapper has now been amended to resolve its own directory, as
the hostile wrapper already did.  Both are working-directory independent.

## Disclosure

This audit and its verification code were produced with AI assistance.  The
work is not peer reviewed.  Exact computer-algebra checks are evidence about
the algebra encoded in the scripts; they are not a substitute for independent
mathematical review of the normal-form reduction or the surrounding research
program.
