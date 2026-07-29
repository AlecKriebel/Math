# Exact exclusion of the binary-tetrahedral \(d=6\) branch

**Status:** `PROVED` and `INDEPENDENTLY_REPRODUCIBLE` by exact symbolic
arithmetic.

**Scope:** This note excludes the complete balanced diagonal-\(2T\)-invariant
heterogeneous ansatz described below. It does **not** exclude an arbitrary
\(d=6\) exceptional Yang--Baxter matrix.

## 1. The ansatz and its exact decomposition

Let \(A=\mathbb C^2\) be the defining representation of the binary
tetrahedral group \(2T\subset SU(2)\), and let \(B=\mathbb C^3\) be the
induced tetrahedral rotation representation. We seek a Hermitian balanced
involution

\[
K\in\operatorname{End}(A\otimes B\otimes A)
\]

that commutes with the diagonal \(2T\)-action. It is inserted with shift
\(\dim(A\otimes B)=6\):

\[
K_1=K\otimes I_6,\qquad K_2=I_6\otimes K.
\]

A solution of

\[
K_1K_2K_1-K_2K_1K_2=\frac13(K_1-K_2)
\]

would block, after the usual spectator/regrouping step, into an ordinary
local \(d=6\) solution.

Reorder the two \(A\)-factors only for the representation-theoretic
calculation. Since

\[
A\otimes A\cong 1\oplus 3,
\qquad
3\otimes 3\cong1\oplus1'\oplus1''\oplus3\oplus3,
\]

one obtains

\[
\boxed{A\otimes B\otimes A\cong1\oplus1'\oplus1''\oplus3\oplus3\oplus3.}
\]

The exact verifier constructs the 24 Hurwitz units, their defining and
rotation matrices, and explicit orthonormal intertwiners for all six
summands. It verifies all intertwining identities for all 24 group elements
and computes the commutant dimension

\[
1^2+1^2+1^2+3^2=12.
\]

If an equivariant projection has rank six, let \(s\in\{0,1,2,3\}\) be the
number of one-dimensional summands it contains and let
\(r\in\{0,1,2,3\}\) be its rank on the multiplicity space of the three
copies of \(3\). Then

\[
s+3r=6,
\]

whose only solutions are

\[
(s,r)=(3,1),\qquad(0,2).
\]

The two branches are complements. Because the cubic relation is invariant
under \(K\mapsto-K\), it is enough to study \((s,r)=(3,1)\).

## 2. Complete \(\mathbb{CP}^2\) parameterization

Choose orthonormal intertwiners

\[
U_0,U_1,U_2:\mathbb C^3\longrightarrow A\otimes B\otimes A
\]

for the three copies of the tetrahedral \(3\), and let \(P_{\rm diag}\) be
the sum of the three distinct one-dimensional summands. For a unit vector
\(z=(z_0,z_1,z_2)\in\mathbb C^3\), put

\[
W(z)=z_0U_0+z_1U_1+z_2U_2,
\]

\[
P(z)=P_{\rm diag}+W(z)W(z)^*,
\qquad
K(z)=2P(z)-I_{12}.
\]

The phase of \(z\) is immaterial, so this is exactly \(\mathbb{CP}^2\).
There are no omitted equivariant balanced signatures or mixing parameters.

## 3. Three-entry exact obstruction

Write, after fixing the projective phase,

\[
z=(a,b+ic,d+ie),
\qquad a,b,c,d,e\in\mathbb R,
\]

with

\[
a^2+b^2+c^2+d^2+e^2=1.
\]

Let

\[
F=K_1K_2K_1-K_2K_1K_2-\frac13(K_1-K_2).
\]

In the explicit tensor basis used by the verifier (with zero-based matrix
indices), exact reduction modulo the normalization equation gives

\[
F_{2,2}=-\frac43(bd+ce),
\]

and

\[
F_{5,5}
=b^2+c^2+d^2+e^2-\frac23(bd+ce)-\frac23.
\]

Thus \(F=0\) would force

\[
bd+ce=0,
\qquad
b^2+c^2+d^2+e^2=\frac23,
\qquad
a^2=\frac13.
\]

The projective phase may therefore be chosen so that
\(a=1/\sqrt3\). The two real vectors \((b,c)\) and \((d,e)\) are
orthogonal, so for some real \(r,s,x,y\) and
\(\varepsilon\in\{+1,-1\}\),

\[
(b,c)=r(x,y),\qquad
(d,e)=\varepsilon s(-y,x),
\]

\[
r^2+s^2=\frac23,\qquad x^2+y^2=1.
\]

Under these forced conditions, a third exact residual entry is

\[
F_{57,20}
=-\frac{2\sqrt6\,i}{27}(x-iy)
\left[
r(6s^2-1)+\varepsilon i\,s(6s^2-3)
\right].
\]

Consequently,

\[
\begin{aligned}
|F_{57,20}|^2
&=\frac{8}{243}(x^2+y^2)
\left[
r^2(6s^2-1)^2+s^2(6s^2-3)^2
\right]\\
&=\frac{8}{243}
\left[
\left(\frac23-s^2\right)(6s^2-1)^2
+s^2(6s^2-3)^2
\right]\\
&=\boxed{\frac{16}{729}},
\end{aligned}
\]

because the bracket on the second line is identically \(2/3\). This
contradicts \(F=0\).

Therefore:

> **Proposition.** No balanced diagonal-\(2T\)-equivariant involution on
> \(A\otimes B\otimes A\) satisfies the shifted exceptional cubic relation.

The proof covers the complementary signature by \(K\mapsto-K\).

## 4. Numerical falsifier and provenance

Before evaluating the objective, the complete seed interval, stopping rule,
and candidate threshold were recorded in
`results/d6_binary_tetrahedral_cp2_seed_manifest.json`. The search used a
four-real-coordinate chart covering the full complex \(\mathbb{CP}^2\),
not merely its real locus.

An analytic-gradient check at seed `26074000` had relative error
\(1.1647\times10^{-9}\). All 64 predeclared production seeds
`26074001`--`26074064` were run. No candidate event occurred. The smallest
observed normalized squared residual was numerically \(16/9\), with
Frobenius residual \(8\sqrt2\). This numerical floor is not asserted as a
proved global minimum and is not used in the exact exclusion.

### Reproduction commands

From the project root:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_binary_tetrahedral_cp2_ansatz.py

/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_binary_tetrahedral_cp2_no_go.py

/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_binary_tetrahedral_cp2_search.py \
  --gradient-check --seed 26074000

/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_binary_tetrahedral_cp2_search.py \
  --seed-start 26074001 --seed-end 26074064 \
  --max-iterations 1000
```

The exact verifiers use SymPy `1.14.0`. The numerical search used Python
`3.9.6`, NumPy `2.0.2`, and SciPy `1.13.1` on
`macOS-26.5.2-arm64-arm-64bit`. Source and raw-output SHA-256 hashes are
recorded in `results/d6_binary_tetrahedral_cp2_search_summary.json`.
