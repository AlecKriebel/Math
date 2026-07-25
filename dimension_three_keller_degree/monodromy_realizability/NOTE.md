# Regular monodromy is impossible, and the degree \(2\)-\(10\) action ledger

**Synthesis timestamp (UTC):** 2026-07-25T21:02:56Z

**Scope:** Keller counterexamples
\(\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\).
**Status:** attributed synthesis; no novelty is claimed for the regular-action
obstruction or the low-degree transitive-group census.

> **Review and assistance notice.** This note is not peer reviewed. It was
> prepared with substantial AI assistance. Exact computations verify the
> encoded group data and status ledger; they are evidence, not peer review or
> a proof of the cited geometric theorems.

## 1. The classical theorem used

Let \(k\) be a field of characteristic zero,
\[
B=k[X_1,\ldots,X_n],
\qquad
F=(f_1,\ldots,f_n)\in B^n,
\]
and suppose
\[
\det\left(\frac{\partial f_i}{\partial X_j}\right)\in k^\times.
\]
Put
\[
A=k[f_1,\ldots,f_n],\qquad K=\operatorname{Frac}(A),\qquad
L=\operatorname{Frac}(B).
\]
Wright's Theorem 3.7, under these section-wide hypotheses, states:

> If \(L/K\) is Galois, then \(A=B\).

Thus \(F\) has a polynomial inverse. Wright labels this as Campbell's theorem
for \(k=\mathbb C\), proves the algebraic characteristic-zero statement, and
includes it as condition (2) of the summary theorem on the following page.
Campbell proved the complex case in 1973; Razar gave an independent algebraic
treatment in 1979.

The theorem assumes that the original extension \(L/K\) is Galois. It is not
enough that \(L/K\) has a Galois closure: every finite separable extension has
one.

## 2. Galois extension if and only if regular natural monodromy

Now take \(k=\mathbb C\), let \(d=[L:K]\), let \(N/K\) be the normal closure,
and set
\[
G=\operatorname{Gal}(N/K),\qquad H=\operatorname{Gal}(N/L).
\]
The geometric monodromy is the faithful transitive action of \(G\) on the
\(d\) embeddings
\[
\operatorname{Hom}_K(L,N)\simeq G/H.
\]
The stabilizer of the embedding \(L\hookrightarrow N\) is \(H\). Faithfulness
follows because the kernel is
\(\operatorname{core}_G(H)=\bigcap_{g\in G}gHg^{-1}\), whose fixed field is
the compositum of all conjugates of \(L\), namely \(N\).

Since the action is transitive,
\[
\begin{aligned}
G\curvearrowright G/H\text{ is regular}
&\Longleftrightarrow H=1\\
&\Longleftrightarrow N=L\\
&\Longleftrightarrow L/K\text{ is Galois}.
\end{aligned}
\tag{1}
\]
This is a statement about the **natural permutation action**, not merely the
abstract isomorphism type of \(G\).

Combining (1) with the classical Galois-case theorem gives:

### Regular-action obstruction

For a Keller map over \(\mathbb C\),
\[
F\text{ is a polynomial automorphism}
\quad\Longleftrightarrow\quad
\operatorname{Mon}_{\mathrm{geom}}(F)
\text{ is regular on the generic fibre}.
\tag{2}
\]
Consequently, the natural geometric monodromy of every Keller counterexample
is nonregular. It is also nonabelian: a faithful transitive action of an
abelian group is regular, because all point stabilizers coincide and
faithfulness makes their common value trivial.

The map \(F\) need not be finite or a covering over the whole target. One
restricts to a dense open set on which it is a connected finite etale cover;
its permutation monodromy is the group in (1).

### Arithmetic/geometric warning

Over a non-algebraically-closed field, \(L/K\) is Galois exactly when the
**arithmetic** monodromy is regular. Geometric monodromy instead tests the
extension after base change to an algebraic closure. Since this program works
over \(\mathbb C\), arithmetic and geometric monodromy coincide here. We do
not silently replace one by the other over a general field.

## 3. Certified realizations used in the ledger

Two existing artifacts supply the realized entries.

1. The [weighted-lift symmetric-monodromy
   theorem](weighted_lift_symmetric/NOTE.md) gives, for every \(d\ge3\), an
   explicit dimension-three Keller counterexample of generic degree \(d\)
   with natural geometric monodromy \(S_d\). For \(3\le d\le10\), these are
   \(3T2,4T5,5T5,6T16,7T7,8T50,9T34,10T45\).
2. The [certified square of the announced cubic
   map](../../discovery_04_wreath_monodromy/NOTE.md) has generic degree \(9\)
   and geometric monodromy
   \[
   S_3\wr S_3=9T31,
   \qquad |9T31|=1296,\qquad
   |\operatorname{Stab}_{9T31}(1)|=144.
   \]

Here \(dTj\) means GAP's `TransitiveGroup(d,j)`, hence an action up to
conjugacy in \(S_d\). “Realized” means that one of the cited, locally
certified dimension-three counterexamples realizes that action. “Open” means
only that the action survives (2) and is not realized by either cited
artifact. It is not a claim of worldwide nonrealization.

## 4. Compact degree \(2\)-\(10\) ledger

The full 165-action GAP output, with orders and point-stabilizer orders, is
[transitive_actions_2_10.tsv](regular_obstruction/transitive_actions_2_10.tsv).
The status partition is:

| \(d\) | all | excluded: regular | realized | open in this ledger | E/R/O |
|---:|---:|---|---|---|---:|
| 2 | 1 | `2T1` | `-` | `-` | 1/0/0 |
| 3 | 2 | `3T1` | `3T2` | `-` | 1/1/0 |
| 4 | 5 | `4T1,4T2` | `4T5` | `4T3-4T4` | 2/1/2 |
| 5 | 5 | `5T1` | `5T5` | `5T2-5T4` | 1/1/3 |
| 6 | 16 | `6T1,6T2` | `6T16` | `6T3-6T15` | 2/1/13 |
| 7 | 7 | `7T1` | `7T7` | `7T2-7T6` | 1/1/5 |
| 8 | 50 | `8T1-8T5` | `8T50` | `8T6-8T49` | 5/1/44 |
| 9 | 34 | `9T1,9T2` | `9T31,9T34` | `9T3-9T30,9T32-9T33` | 2/2/30 |
| 10 | 45 | `10T1,10T2` | `10T45` | `10T3-10T44` | 2/1/42 |
| **total** | **165** | **17** | **9** | **139** | **17/9/139** |

Every row is a disjoint exhaustive partition of the TransGrp actions in that
degree.

### Degree four

The excluded actions are
\[
4T1=C_4,\qquad 4T2=V_4.
\]
Both are regular. The three nonregular actions left by the obstruction are
\[
4T3\simeq D_4,\qquad 4T4=A_4,\qquad 4T5=S_4.
\]
Here \(D_4\) denotes the order-eight symmetry group of a square; GAP's
`StructureDescription` writes it as `D8`. The weighted-lift family realizes
\(4T5=S_4\); \(4T3\) and \(4T4\) remain open in this ledger.

### Degree six

The two excluded actions are
\[
6T1=C_6,\qquad 6T2\simeq S_3.
\]
They are the two regular actions associated with the two abstract groups of
order six. In particular, \(6T2\) is \(S_3\) acting regularly on itself; it is
not the natural three-point action \(3T2\), which is nonregular and realized.
All \(6T3,\ldots,6T16\) are nonregular. The weighted-lift family realizes
\(6T16=S_6\), leaving the other thirteen actions open in this ledger.

## 5. What this does and does not prove

The obstruction proves that regular actions, and hence all abelian natural
monodromy groups, are impossible for counterexamples. In degree three it is
complete: \(3T1=C_3\) is excluded and \(3T2=S_3\) is forced.

For \(d\ge4\), nonregularity is only a first filter. No action in the open
column is asserted to occur, and no additional action is excluded here. In
particular, this note contains no new Keller-specific nonrealizability theorem
beyond the classical Galois case.

## References

1. L. A. Campbell, *A condition for a polynomial map to be invertible*,
   Math. Ann. **205** (1973), 243-248,
   [doi:10.1007/BF01349234](https://doi.org/10.1007/BF01349234).
2. M. Razar, *Polynomial maps with constant Jacobian*, Israel J. Math.
   **32** (1979), 97-106,
   [doi:10.1007/BF02764906](https://doi.org/10.1007/BF02764906).
3. D. Wright, *On the Jacobian conjecture*, Illinois J. Math. **25** (1981),
   423-440, Theorem 3.7,
   [doi:10.1215/ijm/1256047158](https://doi.org/10.1215/ijm/1256047158).
4. E. Kuiken, *Coverings with singularities*, Canad. J. Math. **33** (1981),
   1141-1150,
   [doi:10.4153/CJM-1981-086-4](https://doi.org/10.4153/CJM-1981-086-4).
5. A. Hulpke, *The Transitive Groups Library*, GAP package TransGrp,
   [official manual](https://docs.gap-system.org/pkg/transgrp/doc/manual.pdf).
