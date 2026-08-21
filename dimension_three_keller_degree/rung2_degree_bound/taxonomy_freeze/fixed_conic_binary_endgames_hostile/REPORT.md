# Hostile PARI audit of the complete binary fixed-conic endgames

## Verdict

\[
\boxed{\textbf{PASS}}
\]

Starting from the retained complete \(E_7\) fibres, the exact calculation
recovers every later family (13)--(36) in
`WORKING_FIXED_CONIC_ROW.md` as the complete solution fibre on its stated
branch.  No omitted rank-jump or zero specialization was found.

This package closes the lower-endgame scope explicitly left open by
`fixed_conic_binary_repair_pari/REPORT.md`.  Together, the two independent
PARI packages cover the binary part of the frozen row
`Q2-E2-A1-B2-D2-N1`.

## 1. Information boundary and method

The derivation first read only the frozen-row hostile report, its Phase A
normal-form derivation, and the completed independent PARI \(E_7\to E_6\)
repair.  It derived the seven tangent obligations before opening the legacy
working note and exact scripts.  It did not inspect any file under
`fixed_conic_binary_endgames_sympy/`.

The retained checker uses PARI/GP exact rational coefficient matrices.
For every endgame it starts with:

- all 12 coefficients of the binary cubic \(V\), subject only to the
  already-certified \(E_7\) compatibility equations;
- the complete affine \(E_7\) fibre with its 11 free \(H_2\) coefficients;
- all nine entries of the linear part \(L\).

Every linear solve quoted below has a displayed constant rational minor,
except the explicitly stated nilpotent \(K\ne0\) \(E_4\) solve, whose minor
is nonzero exactly under that branch hypothesis.  The scalar \(E_4\)
rank-drop is handled from raw equations by squares, not by a
parameter-dependent generic solve.

The checker uses one-based \(v_i,w_i,\ell_i\).  The legacy note uses
zero-based indices.

## 2. Starting ranks and branch count

The imported top certificate gives, for each of \(h=pq,p^2\),
\[
\operatorname {rank}E_8=12,\qquad \dim\ker E_8=18,
\]
and
\[
\operatorname {rank}_{H_2}E_7=7,\qquad
\dim(E_7\text{-fibre in }H_2)=11.
\]
The common \(E_7\) pivot determinant is \(-2^{19}\).

The exhaustive tangent list has seven strata:

| leading divisor | tangent strata |
|---|---:|
| \(pq\) | opposite weight, scalar, zero |
| \(p^2\) | scalar, semisimple, nilpotent, zero |

The two zero-tangent strata each split into three support orbits.  The
nilpotent stratum splits at \(K=0\).  Thus the retained terminal ledger has
12 branches: 10 contradiction branches and 2 binary
plane-plus-shear automorphism exits.

## 3. Split roots

### 3.1 Opposite weights

Normalize the tangent to \(pA_p-qA_q\).  From the full \(E_7\) fibre, the
\(E_6\) matrix in the nine entries of \(L\) has rank \(3\), pivot columns
\((3,6,9)\), six free entries, and constant minor
\[
-128.
\]
Its eight nonzero left-null compatibilities have radical
\[
\begin{gathered}
v_8=v_3=v_5=v_{10}=w_3=w_{13}=0,\\
v_2=6v_7-9v_{12}+4w_{11},\qquad
3v_1=2v_6-3v_{11}-2w_{17}.
\end{gathered}
\]
After translating indices through the certified \(E_7\) pivot formulas,
these are exactly the eight conditions in (11).  They leave a
13-parameter \((V,H_2)\)-fibre.

On the whole fibre, \(E_5\) has rank \(4\) in the remaining six entries of
\(L\).  Its left-null vector has inhomogeneous pairing
\[
64.
\]
This proves (11)--(12) exhaustively.

### 3.2 Scalar tangent

Normalize the tangent to \(2A\).  The successive data are:

| stage | rank in current \(L\) entries | constant minor | complete \((V,H_2)\) dimension after compatibility |
|---|---:|---:|---:|
| \(E_6\) | \(3/9\) | \(-128\) | 13 |
| \(E_5\) | \(4/6\) | \(32\) | 10 |

The \(E_6\) radical and the three linear \(E_5\) compatibilities
reparametrize uniquely as the displayed families (13)--(14), before the
\(E_4\) conditions.

Put
\[
U=v_6,\quad V=v_7,\quad X=v_{11}-v_6,\quad
Y=v_{12}-v_7,\quad B_1=w_8.
\]
Two raw \(E_4\) coefficients are
\[
-12(2v_7-2v_{12}-w_{11})^2,\qquad
-3(4v_6-4v_{11}+w_{17})^2.
\]
They force \(w_{11}=-2Y\) and \(w_{17}=4X\), including \(X=0\) and
\(Y=0\).  Successive raw residual squares then force
\[
\begin{aligned}
w_9&=-VY-Y^2,\\
w_{14}&=2UX-X^2,\\
w_{15}&=B_1+UY+VX+XY.
\end{aligned}
\]
These are exactly (15)--(16).  After them \(E_4=E_3=0\) identically and
the free linear entries are \(\ell_5,\ell_8\), corresponding to legacy
\(\ell_4,\ell_7\).

Writing
\[
\begin{aligned}
Q&=B_1Y+UY^2+\ell_5,\\
R&=-2B_1X-2UXY+VX^2+X^2Y+\ell_8,\\
P&=VX^2Y+X^2Y^2+2X\ell_5+Y\ell_8,
\end{aligned}
\]
the exact remainder is
\[
E_2=(Rp-2Qq)^2,\qquad \det L=P^2,\qquad
P=2XQ+YR.
\]
Thus (17)--(19) are complete without division by \(X\) or \(Y\).

### 3.3 Zero tangent

The complete \(E_7\) fibre is
\[
H_3=V(p,q),\qquad H_2=B(p,q)+r(\alpha A_p+\beta A_q).
\]
The split stabilizer has the three support orbits claimed in (21).  Exact
data for the two nonzero orbits are:

| support orbit | \(E_6\) rank in \(L\) | \(E_6\) compatibility count | \(E_5\) constant certificates |
|---|---:|---:|---|
| \((1,0)\) | 3 | 3 | \(8\) |
| \((1,1)\) | 3 | 4 | \(8,-16,8\) |

Both \(E_6\) minors are \(-128\).  The zero support orbit is precisely the
binary plane-plus-shear exit.  This proves (20)--(22) exhaustively.

## 4. Double root

### 4.1 Scalar tangent

The successive ranks and dimensions are:

| stage | rank in current \(L\) entries | constant minor | complete \((V,H_2)\) dimension |
|---|---:|---:|---:|
| \(E_6\) | \(3/9\) | \(-128\) | 14 |
| \(E_5\) | \(4/6\) | \(32\) | 10 |

These fibres reparametrize uniquely as (23)--(24).  Put
\[
U=v_6,\quad V=v_{12},\quad X=v_{11}-v_6,\quad
Z=v_{10},\quad B_1=w_8.
\]
The raw \(E_4\) squares and their residuals force, in order,
\[
\begin{aligned}
w_{11}&=-2X,&w_{17}&=2Z,&w_9&=-VX,\\
w_{14}&=(U+X)Z,&
w_{15}&=B_1+UX+\frac{VZ}{2}+X^2.
\end{aligned}
\]
The \(E_5\) pivot formula then gives \(B_0=UZ/2\).  These are exactly (25).
After them \(E_4=E_3=0\), again with free entries
\(\ell_5,\ell_8\).

With
\[
\begin{aligned}
Q&=B_1X+UX^2+X^3+\ell_5,\\
R&=-4B_1Z-4UXZ+VZ^2-4X^2Z+4\ell_8,\\
P&=VXZ^2+4X\ell_8+4Z\ell_5,
\end{aligned}
\]
the exact identities are
\[
E_2=(Rp/4-2Qq)^2,\qquad
\det L=P^2/16,\qquad P=4ZQ+XR.
\]
This proves (26)--(27), including \(X=0\) and \(Z=0\).

### 4.2 Semisimple tangent

For the tangent \(pA_p\), the full successive fibre has:

| stage | rank in current \(L\) entries | minor | compatibility effect |
|---|---:|---:|---|
| \(E_6\) | \(3/9\) | \(-128\) | dimension \(21\to14\) |
| \(E_5\) | \(4/6\) | \(-32\) | dimension \(14\to10\) |
| \(E_4\) | \(2/2\) | \(-8\) | no compatibility |

The 10-parameter \((V,H_2)\)-fibre is exactly (28)--(29).  The three
constant minors give a unique \(L\), and direct exact expansion yields
\[
\det L=0.
\]
This is a constant-minor derivation of (30), so no exceptional parameter
specialization is lost.

### 4.3 Nilpotent tangent

For the tangent \(pA_q\), \(E_6\) again has rank \(3\), minor \(-128\).
Its six left-null generators have radical codimension five and leave a
17-dimensional \((V,H_2)\)-fibre.  At \(E_5\), rank \(3\) with minor
\(128\), the residual equations are exactly (31), including the product
\[
K\,w_3=0
\]
in legacy coordinates.

- If \(K\ne0\), \(E_4\) has rank \(3\) with minor
  \(-16K^3\).  Its compatibility forces exactly (32); after substitution
  there is no residual compatibility and the unique \(L\) has
  \(\det L=0\).
- If \(K=0\), the \(E_6,E_5\) ranks are \(3,3\), with minors
  \(-128,128\).  No \(E_5\) compatibility remains, and the complete solved
  linear fibre satisfies
  \[
  L_{\bullet2}=\frac{v_{11}}2L_{\bullet3},
  \]
  exactly (33) in one-based notation.  Hence \(\det L=0\).

The split at \(K=0\) is therefore exhaustive and no division crosses the
rank jump.

### 4.4 Zero tangent

The Borel stabilizer has the three orbits in (34).  For its two nonzero
orbits:

| support orbit | \(E_6\) rank in \(L\) | \(E_6\) compatibility count | \(E_5\) constant |
|---|---:|---:|---:|
| \(A_p\) | 3 | 3 | \(8\) |
| \(A_q\) | 3 | 2 | \(8\) |

The \(E_6\) generators are exactly (35) and (36), and both constant minors
are \(-128\).  The zero support orbit is the binary plane-plus-shear exit.

## 5. Exhaustiveness conclusion

Every displayed family (13)--(36) is the full solution fibre of the
preceding coefficient identities on its stated orbit.  The only genuine
lower-degree rank split is the retained nilpotent split \(K\ne0/K=0\).
The apparent scalar \(E_4\) generic rank is not used: raw square
certificates first force the rank-drop locus, where the two remaining
linear entries stay free.  Hence there is no illicit generic-rank division.

Final branch count:

| outcome | count |
|---|---:|
| constant compatibility obstruction | 5 |
| singular \(L\) from scalar/semisimple/nilpotent endgame | 5 |
| binary plane-plus-shear automorphism | 2 |
| total terminal branches | 12 |

No omitted branch was found.

## 6. Reproduction

Run:

```sh
taxonomy_freeze/fixed_conic_binary_endgames_hostile/verify_strict.sh
```

The wrapper rejects PARI parse/type/user errors and requires every decisive
rank, minor, constant obstruction, column relation, scalar-square identity,
and final pass marker.  Its terminal output is:

```text
PASS strict hostile complete binary fixed-conic endgames
```

No ledger, registry, branch, commit, or remote state was changed.
