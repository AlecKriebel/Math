# Independent PARI audit of the `D4-DN-3` boundary charts

**First banked (UTC):** `2026-07-26T05:35:49Z`  
**Status:** exact boundary-chart verification; not peer reviewed.

## Scope

This package verifies only the two boundary charts in the certified
`D4-DN-3` contact atlas:

| Stable chart | condition | result |
|---|---|---|
| `DN3-INTERSECTION-SNZ` | common contact line, scale \(k\ne0\) | impossible for a Keller map because \(\det L=0\) |
| `DN3-ORIGIN` | contact scale \(k=0\) | every nonlinear term is binary, hence the map is an automorphism |

Here
\[
H_4=((p+q)^2p^2,(p+q)^2q^2,0),\qquad R=(p+q)^3,
\]
and the punctured common line is
\[
U_1=-kp(p+q),\qquad V_1=kq(p+q),\qquad T_1=0.
\]
The certified full contact atlas identifies this \(k\) with its common-line
coordinate \(s\).  Its prior \(E_6\) calculation also forces the omitted
\(r^2\)-contact block to zero.

The verifier retains arbitrary binary \(U_0,V_0,T_0,A_0,B_0\), all six
nonbinary quadratic coefficients of the first two components, and every
entry of the linear part \(L\).  It reconstructs
\[
\det\!\left(L+wJH_2+w^2JH_3+w^3JH_4\right)
\]
directly in PARI/GP.  It does not load a SymPy eliminant, solution, or
coefficient table.

## Punctured intersection

The fixed exact pivot chain is:

| block | rank | pivot |
|---|---:|---:|
| \(E_6\) | 6 | \(-279936k\) |
| \(E_5\), \(r\)-linear | 3 | \(192k^4\) |
| \(E_5\), binary | 3 | \(108k^3\) |
| \(E_4\), \(r\)-linear | 2 | \(3k^4\) |
| \(E_4\), binary | 2 | \(9k^2\) |

Every solution denominator is checked to be a constant times a power of
\(k\).  Thus the only localization is the displayed \(k\ne0\); there is no
hidden coefficient-dependent pivot boundary.

After the two \(E_5\) rank solves, put
\[
S=v_0-v_1+v_2-v_3
\]
and
\[
D=u_1-2u_2+3u_3-v_1+2v_2-3v_3.
\]
The determinant reconstruction gives
\[
\begin{aligned}
[p^2r^2]E_4&=-\frac94k^3S,\\
[pqr^2]E_4&=-\frac92k^3S,\\
[q^2r^2]E_4&=-\frac94k^3S.
\end{aligned}
\]
Hence \(E_4=0\) and \(k\ne0\) force \(S=0\).  On \(S=0\), the six complete
binary \(E_5\) residuals are exactly
\[
\left(0,0,0,\frac34kD^2,\frac32kD^2,\frac34kD^2\right),
\]
so \(D=0\).  The two remaining constant-rank \(E_4\) solves have no
compatibilities.  Back-substitution into the entire \(E_5\) and \(E_4\)
polynomials gives zero, while back-substitution into the literal
\(\det L\) gives
\[
\det L=0.
\]
A Keller map has \(\det L\ne0\), because its constant Jacobian equals its
value at the origin.  The punctured intersection is therefore empty.

The program checks every coefficient at every stage, not just the pivot
rows.

## Origin

The origin is rebuilt from the zero-contact determinant rather than
obtained by specializing a \(1/k\)-formula.  Its complete \(E_6\) system has
coefficient and augmented rank five, with constant pivot
\[
31104.
\]
After this exact solve,
\[
[p^3r]E_4=3b_{qr}^2,\qquad
[q^3r]E_4=\frac{(3b_{qr}-4L_{33})^2}{3}.
\]
Over characteristic zero these force \(b_{qr}=L_{33}=0\).  The complete
\(E_6\) solution then sends all six nonbinary quadratic coefficients to
zero.  Since the contact is zero, every nonlinear term depends only on
\(p,q\).

This exit is unconditional.  Let \(H(p,q)\) denote the resulting nonlinear
part and let \(M=L+JH\).  The verifier constructs the literal adjugate and
checks
\[
\operatorname{adj}(L)L=(\det L)I.
\]
The first two coordinates of
\(\operatorname{adj}(L)(L(p,q,r)^t+H(p,q))\) are binary, the derivative of
the third with respect to \(r\) is \(\det L\), and the Jacobian of the first
two coordinates satisfies the exact identity
\[
\det J_{p,q}(G_1,G_2)=\det L\cdot\det M.
\]
For a Keller map, \(\det M=\det L\), so the plane map has constant
Jacobian \((\det L)^2\) and degree at most four.  Moh's proved theorem for
plane Keller maps of degree strictly less than \(100\) makes it an
automorphism; the third coordinate is then a triangular lift.  This does
not assume the open plane Jacobian Conjecture.

## Reproduction and fail-closed checks

Run:

```sh
sh verify_strict.sh
```

The exact terminal markers are:

```text
D4_DN3_PARI_PUNCTURED_INTERSECTION_PASS_DETL_ZERO
D4_DN3_PARI_ORIGIN_PASS_BINARY_COLLAPSE_PLANE_REDUCTION
D4_DN3_PARI_BOUNDARY_AUDIT_ALL_PASS
D4_DN3_PARI_BOUNDARY_STRICT_PASS
```

The wrapper rejects interpreter diagnostics and requires every marker.  It
also corrupts one \(S\)-forcing coefficient and one origin square in
temporary copies; both mutants must exit nonzero before the strict marker
is printed.

## Limits and disclosure

This package does not verify the two plane interiors \(k\ne0\) of the
`D4-DN-3` atlas, nor does it enlarge the frozen family or row scope.  It
certifies the punctured intersection and origin only.  The calculations
and prose were produced with AI assistance.  Exact checks are evidence
about the encoded algebra, not peer review.

## Reference

R. Biggers, T.-T. Moh, and M. Fried, “On the Jacobian conjecture and the
configurations of roots,” *Journal für die reine und angewandte
Mathematik* **340** (1983), 140–213,
[doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
