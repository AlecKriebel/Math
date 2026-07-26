# Full-lower \(E_6\) rebuild for `D4-DN-3`

**First banked:** `2026-07-26T04:19:22Z`
**Status:** certified exact contact-locus theorem with dual exact
implementations and an independent hostile reconstruction; not a Keller
exclusion and not peer reviewed.

## Result

For
\[
h=(p+q)^2,\qquad P=hp^2,\qquad Q=hq^2,\qquad R=(p+q)^3,
\]
the set-theoretic projection of the complete \(E_7,E_6\) system to contact
space is exactly
\[
\boxed{
a=b,\qquad
8a^2+24a(x-y)+9(x-y)^2=0.
}
\]
Over \(\mathbb C\), this is the union of two affine planes:
\[
\begin{aligned}
\Pi_+:\quad&
(a,b,x,y)=
\left(k,k,s+\frac{-4+2\sqrt2}{3}k,s\right),\\
\Pi_-:\quad&
(a,b,x,y)=
\left(k,k,s+\frac{-4-2\sqrt2}{3}k,s\right).
\end{aligned}
\]
They meet along \(k=0\), namely
\[
a=b=0,\qquad x=y=s.
\]

Crucially, this calculation retains and eliminates all 18 lower variables:
the six nonbinary quadratic coefficients of \(A,B\), \(L_{33}\), and all
11 binary coefficients of \(U_0,V_0,T_0\).  No conclusion is inferred from
the zero-binary slice.

This result does **not** exclude `D4-DN-3`.  It gives the complete,
specialization-safe denominator for the next \(E_5,E_4\) descent.

## Complete \(E_7\) space

As usual,
\[
\alpha=J(Q,R),\quad\beta=-J(P,R),\quad\gamma=J(P,Q),
\]
and here
\[
\alpha=-6q(p+q)^4,\qquad
\beta=-6p(p+q)^4,\qquad
\gamma=8pq(p+q)^4.
\]
Writing the \(r^2\)-contact parameters as \(d,z\) and the \(r\)-contact
parameters as \(a,b,x,y\), the full solution of \(E_7=0\) is
\[
\begin{aligned}
U_2&=\frac{4z-3d}{3}p,&V_2&=dq,&T_2&=z,\\
U_1&=\frac{4a-3x}{3}p^2+\frac{4b-3y}{3}pq,&
V_1&=xpq+yq^2,&T_1&=ap+bq.
\end{aligned}
\]
The three \(r\)-blocks have nullities \(0,2,4\), so these six parameters
are exhaustive.

The \(r^3\)-part of \(E_6\) is
\[
\begin{aligned}
&\frac23(-3d+4z)^2q^3
+2(9d^2-16dz+8z^2)pq^2\\
&\quad+\frac23(27d^2-24dz+8z^2)p^2q
+6d^2p^3.
\end{aligned}
\]
The two extreme coefficients force \(d=z=0\).

## Exact elimination ideal

At \(r\)-degree one, only two of the 18 lower variables occur: the
\(r^2\)-coefficients \(a_r,b_r\) of \(A,B\).  Eliminating them from the
six coefficient equations gives an ideal \(J\subset
\mathbb Q[a,b,x,y]\).

The exact Groebner certificate proves
\[
J\subset I=(a-b,f),\qquad
(a-b)^2\in J,\qquad f^2\in J,
\]
where
\[
f=8a^2+24a(x-y)+9(x-y)^2.
\]
Therefore \(\sqrt J=I\).  Moreover,
\[
f=
\bigl(3(x-y)+(4+2\sqrt2)a\bigr)
\cdot\bigl(3(x-y)+(4-2\sqrt2)a\bigr).
\]
The two displayed factors are distinct, so \(I\) is radical and has exactly
the two stated geometric components.

The script checks ideal membership by exact Groebner reduction; it does not
infer the radical from numerical solutions.

## Full 18-variable consistency atlas

Restoring all lower coefficients, \(E_6\) has 13 coefficient equations
linear in the following 18 variables:
\[
(a_{pr},a_{qr},a_{rr},b_{pr},b_{qr},b_{rr},L_{33},
u_0,\ldots,u_3,v_0,\ldots,v_3,t_0,t_1,t_2).
\]

On \(\Pi_+\), the following exact \(7\times7\) pivot is valid for every
\(s\) whenever \(k\ne0\):
\[
373248(7-5\sqrt2)k^2.
\]
The coefficient and augmented matrices both have rank seven.  Galois
conjugation gives
\[
373248(7+5\sqrt2)k^2
\]
on \(\Pi_-\).  Thus there is no hidden exceptional line in either plane.

The common boundary is recomputed:

| Stable chart | condition | rank \(M\) | rank \((M\mid b)\) | pivot |
|---|---:|---:|---:|---:|
| `DN3-P+-KNZ` | \(k\ne0\) | 7 | 7 | \(373248(7-5\sqrt2)k^2\) |
| `DN3-P--KNZ` | \(k\ne0\) | 7 | 7 | \(373248(7+5\sqrt2)k^2\) |
| `DN3-INTERSECTION-SNZ` | \(k=0,s\ne0\) | 6 | 6 | \(-279936s\) |
| `DN3-ORIGIN` | \(k=s=0\) | 5 | 5 | \(31104\) |

These four charts cover both planes, their intersection, and the origin.
This is a pivot atlas, not a generic-rank assertion.

## What the rebuild corrects

A generic symbolic solve can introduce the apparent denominator
\[
s+\left(-\frac{10}{3}+2\sqrt2\right)k.
\]
That line is not a geometric component or a consistency boundary.  The
displayed seven-pivot is independent of \(s\), so it remains nonzero there
for \(k\ne0\).  Any taxonomy that split or deleted this line solely because
of that solver denominator was an artifact of the chosen pivot.

Likewise, setting \(U_0=V_0=T_0=0\) before projection is not
specialization-safe.  The present matrices retain those 11 variables in
every chart.

## Reproduction

Run:

```sh
./verify_strict.sh
```

The terminal markers are:

```text
D4_DN3_FULL_E6_ELIMINATION_PASS_TWO_PLANES_18_LOWER
D4_DN3_PARI_FULL_18_LOWER_ATLAS_PASS
D4_DN3_FULL_REBUILD_STRICT_PASS
```

The SymPy check derives the elimination ideal, radical certificate, and
full pivot atlas.  The PARI/GP check independently reconstructs the
weighted determinant and all 18 lower columns, then checks the ranks and
pivots over \(\mathbb Q(\sqrt2)\).

## Scope and disclosure

This package proves the complete \(E_6\) contact locus only for frozen
family `D4-DN-3`.  It does not close the family, the fixed-quadratic row, or
the quartic frontier.  The derivation and code were produced with AI
assistance.  Exact checks are evidence about the encoded algebra, not peer
review.
