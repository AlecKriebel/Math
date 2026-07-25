# Independent audit: the regular-monodromy obstruction

**Date:** 2026-07-25
**Scope:** characteristic-zero Keller maps, with the monodromy statement made
over \(\mathbb C\).
**Independence:** this audit was prepared without inspecting any local draft by
another researcher.

## Verdict

The proposed translation is correct, provided that:

1. “monodromy” means the **faithful image in the natural action on the
   \(d=[L:K]\) geometric sheets**, not merely an abstract group isomorphic to
   that image;
2. the action is formed after restricting the generically finite map to a
   connected finite étale cover of a dense open subset of the target; and
3. “geometric monodromy” is used over \(\mathbb C\) (or another algebraically
   closed field).  Over a non-algebraically-closed field, the corresponding
   statement about the original extension uses **arithmetic** monodromy.

For a Keller map over \(\mathbb C\), the resulting equivalence is

\[
L/K\text{ is Galois}
\quad\Longleftrightarrow\quad
M_{\rm geom}\leq S_d\text{ is regular in its natural degree-}d\text{ action}.
\]

Combining this with the Campbell--Razar--Wright Galois-case theorem gives the
exact statement

\[
F\text{ is a polynomial automorphism}
\quad\Longleftrightarrow\quad
M_{\rm geom}\curvearrowright\{1,\ldots,d\}\text{ is regular}.
\]

Consequently, a nonautomorphic Keller map has nonregular, hence nonabelian,
geometric monodromy.  This is a necessary and, **conditional on already having
a Keller map**, equivalent test for being a counterexample; it is not a
realizability theorem for arbitrary nonregular transitive groups.

The field-to-monodromy equivalence is classical Galois theory.  Its combination
with the classical Galois-case theorem is an immediate reformulation, not a new
mathematical obstruction.

## 1. Setup and finiteness

Let

\[
F=(f_1,\ldots,f_n):\mathbb A^n_{\mathbb C}\longrightarrow
\mathbb A^n_{\mathbb C}
\]

be a Keller map, so
\(\det(\partial f_i/\partial x_j)\in\mathbb C^\times\).  Put

\[
A=\mathbb C[f_1,\ldots,f_n],\qquad
B=\mathbb C[x_1,\ldots,x_n],\qquad
K=\operatorname{Frac}(A),\qquad L=\operatorname{Frac}(B).
\]

The Jacobian rank is \(n\), so the \(f_i\) are algebraically independent.
Thus \(A\cong\mathbb C[u_1,\ldots,u_n]\), \(K\subset L\) is algebraic, and,
because \(L=K(x_1,\ldots,x_n)\) is finitely generated over \(K\), it is finite.
Write

\[
d=[L:K].
\]

The extension is separable because the characteristic is zero.

## 2. The field-theoretic proof

Fix an algebraic closure \(\Omega\) of \(K\), let \(N\subset\Omega\) be the
normal closure of \(L/K\), and set

\[
G=\operatorname{Gal}(N/K),\qquad H=\operatorname{Gal}(N/L).
\]

Consider

\[
\Sigma=\operatorname{Hom}_K(L,N).
\]

Separability gives \(|\Sigma|=d\).  The group \(G\) acts transitively on
\(\Sigma\) by postcomposition.  If
\(\iota:L\hookrightarrow N\) is the chosen inclusion, then

\[
\operatorname{Stab}_G(\iota)
=\{g\in G:g|_L=\mathrm{id}_L\}
=H,
\]

and the \(G\)-set \(\Sigma\) is \(G/H\).

This action is faithful.  Indeed, its kernel is

\[
\operatorname{core}_G(H)=\bigcap_{g\in G}gHg^{-1}.
\]

The fixed field of this core is the compositum of all \(K\)-conjugates of
\(L\), which is \(N\) by the definition of normal closure.  Hence the core is
trivial.

Because the action is already transitive, it is regular (equivalently, simply
transitive) exactly when its point stabilizer is trivial.  Therefore

\[
\begin{aligned}
G\curvearrowright\Sigma\text{ is regular}
&\Longleftrightarrow H=1\\
&\Longleftrightarrow N=L\\
&\Longleftrightarrow L/K\text{ is normal}\\
&\Longleftrightarrow L/K\text{ is Galois},
\end{aligned}
\]

where the last step uses separability.

Two cautions prevent common misstatements:

- If one embeds \(L\) in an arbitrary larger Galois extension rather than its
  normal closure, “\(H\) is normal” is the relevant condition before passing to
  the faithful image.  In the faithful monodromy image, the stabilizer is
  \(H/\operatorname{core}_G(H)\), and regularity is again equivalent to
  normality of \(L/K\).
- The group of \(K\)-automorphisms of the nonnormal field \(L\) is

  \[
  \operatorname{Aut}_K(L)\cong N_G(H)/H,
  \]

  not \(H\).  Thus a nontrivial monodromy point stabilizer does **not** by
  itself imply a nontrivial automorphism of \(L/K\).

## 3. Why this is geometric monodromy over \(\mathbb C\)

The Jacobian condition makes \(F\) étale, hence quasi-finite.  The morphism
need not be finite or a global topological covering.  By Zariski's Main
Theorem, and then by removing the image of the complement in the finite
normalization, one can choose a nonempty Zariski-open
\(U\subset\mathbb A^n_{\mathbb C}\) such that

\[
V=F^{-1}(U)\longrightarrow U
\]

is a connected finite étale cover of degree \(d\).  Its function-field
extension is still \(L/K\).

For a geometric base point \(\bar u\), the fiber \(V_{\bar u}\) is the
degree-\(d\) set corresponding to \(\Sigma\).  The image of
\(\pi_1^{\mathrm{\acute et}}(U,\bar u)\) in
\(\operatorname{Sym}(V_{\bar u})\) is, up to conjugating the labeling of the
fiber, \(\operatorname{Gal}(N/K)\) in the action above.  Over \(\mathbb C\),
Riemann existence identifies the same finite image with the image of the
topological monodromy representation

\[
\pi_1^{\mathrm{top}}(U(\mathbb C),u)\longrightarrow S_d.
\]

Since \(\mathbb C\) is algebraically closed, there is no nontrivial constant
field quotient: arithmetic and geometric monodromy coincide here.

This also explains why an everywhere-étale Keller map can have nontrivial
monodromy: for a nonproper map one first removes the nonproperness/branch locus
of the normal closure.  Étaleness of \(F\) does not say that
\(F(\mathbb C)\) is a global covering of all of \(\mathbb C^n\).

### Base-field warning

Over a non-algebraically-closed field \(k\), the universally valid statement is

\[
L/K\text{ is Galois}
\quad\Longleftrightarrow\quad
M_{\rm arith}\text{ is regular in its natural action}.
\]

Geometric monodromy instead tests the base-changed extension
\(L\bar k/K\bar k\).  The distinction is real.  For example,

\[
K=\mathbb R(t^3)\subset L=\mathbb R(t)
\]

is not Galois.  Its arithmetic monodromy in degree \(3\) is \(S_3\), but after
base change to \(\mathbb C\), the extension
\(\mathbb C(t)/\mathbb C(t^3)\) is cyclic Galois and its geometric monodromy
\(C_3\) is regular.  This example is only a field-theoretic warning, not a
Keller map.

## 4. Exact Keller-map consequence

Campbell proved the Galois case over \(\mathbb C\).  Razar and independently
Wright gave algebraic/general characteristic-zero treatments.  In particular,
Wright's Theorem 3.7 states that if \(L/K\) is Galois then \(A=B\); his summary
theorem states the result over every characteristic-zero field.

For a Keller map over \(\mathbb C\), therefore,

\[
\begin{array}{c}
F\text{ is a polynomial automorphism}\\
\Updownarrow\\
d=1\\
\Updownarrow\\
L/K\text{ is Galois}\\
\Updownarrow\\
M_{\rm geom}\text{ is regular in degree }d.
\end{array}
\]

The middle equivalence uses the Galois-case theorem in the nontrivial
direction; a nontrivial Galois extension cannot occur for a Keller map.

Thus any Keller counterexample satisfies all of the following:

1. \(d\geq 3\).  Degree \(1\) is the birational case and every separable
   quadratic extension is Galois.
2. If \(H\) is a point stabilizer in \(M_{\rm geom}\), then \(H\neq 1\).
3. \(|M_{\rm geom}|=d|H|>d\).
4. \(M_{\rm geom}\) is nonabelian.  A faithful transitive action of an abelian
   group is regular: all point stabilizers coincide, so faithfulness forces
   them to be trivial.

In degree \(3\), the conclusion is exact:

\[
M_{\rm geom}\cong S_3,\qquad H\cong C_2,\qquad
\operatorname{Aut}_K(L)\cong N_{S_3}(C_2)/C_2=1.
\]

Indeed, the only transitive degree-\(3\) actions are the regular \(C_3\) action
and the natural \(S_3\) action.  Consequently, once a nonautomorphic degree-\(3\)
Keller map and its field degree are established, \(S_3\) monodromy follows
without a separate discriminant calculation.  An explicit primitive element,
discriminant, or branch divisor would still contain additional information not
provided by this obstruction.

Conversely, “\(M\) is a nonregular transitive subgroup of \(S_d\)” does not
produce a Keller map.  The table below is only a filter on possible natural
actions.

## 5. Complete degrees \(2\) through \(10\) audit

The GAP TransGrp identifiers \(dTj=\texttt{TransitiveGroup(d,j)}\) classify
**permutation actions up to conjugacy in \(S_d\)**, not merely abstract groups.
This distinction is essential: for example, \(S_3\) occurs regularly as \(6T2\)
and nonregularly as \(3T2\).

The complete 165-row output, including group order, point-stabilizer order, GAP
name, and abstract structure description, is in
[transitive_actions_2_10.tsv](transitive_actions_2_10.tsv).  The following
table enumerates all actions compactly by giving the full GAP-ID ranges and
identifies every regular one.

| \(d\) | all transitive actions | regular actions (abstract group) | nonregular actions |
|---:|---:|---|---|
| 2 | 1 | \(2T1\) (\(C_2\)) | none |
| 3 | 2 | \(3T1\) (\(C_3\)) | \(3T2\) |
| 4 | 5 | \(4T1\) (\(C_4\)); \(4T2\) (\(C_2^2\)) | \(4T3\)--\(4T5\) |
| 5 | 5 | \(5T1\) (\(C_5\)) | \(5T2\)--\(5T5\) |
| 6 | 16 | \(6T1\) (\(C_6\)); \(6T2\) (\(S_3\)) | \(6T3\)--\(6T16\) |
| 7 | 7 | \(7T1\) (\(C_7\)) | \(7T2\)--\(7T7\) |
| 8 | 50 | \(8T1\) (\(C_8\)); \(8T2\) (\(C_4\times C_2\)); \(8T3\) (\(C_2^3\)); \(8T4\) (\(D_8\)); \(8T5\) (\(Q_8\)) | \(8T6\)--\(8T50\) |
| 9 | 34 | \(9T1\) (\(C_9\)); \(9T2\) (\(C_3^2\)) | \(9T3\)--\(9T34\) |
| 10 | 45 | \(10T1\) (\(C_{10}\)); \(10T2\) (\(D_{10}\)) | \(10T3\)--\(10T45\) |
| **total** | **165** | **17** | **148** |

Here \(D_m\) follows GAP's `StructureDescription` convention and has order
\(m\).  The table has a conceptual cross-check: a regular permutation group of
degree \(d\) has order \(d\), and each abstract group of order \(d\) supplies,
up to permutation equivalence, one regular action.  Thus the regular counts
\(1,1,2,1,2,1,5,2,2\) agree with the numbers of abstract groups of orders
\(2,\ldots,10\).

For Keller counterexamples, delete the regular column.  In particular:

- degree \(2\): no candidate;
- degree \(3\): only \(3T2=S_3\);
- degree \(4\): only \(4T3=D_8\), \(4T4=A_4\), or \(4T5=S_4\);
- in each later degree, precisely the listed nonregular GAP actions survive
  this obstruction.

They survive only this obstruction, not every geometric or Keller-specific
constraint.

### Reproducibility

The script
[enumerate_regular_actions_independent.g](enumerate_regular_actions_independent.g)
was run with GAP 4.16.0 and TransGrp 3.6.5.  This GAP 4.16.0 build was made
independently of the root audit's separate GAP 4.15.1 build.

```sh
gap -A -q enumerate_regular_actions_independent.g > transitive_actions_2_10.tsv
```

For every action the script independently checks

\[
\texttt{IsRegular(G,[1..d])}
\quad\Longleftrightarrow\quad
|\operatorname{Stab}_G(1)|=1
\quad\Longleftrightarrow\quad
|G|=d.
\]

The audited TSV has 167 lines (a version line, a header, and 165 records) and
SHA-256

```text
21373021fe85115a27141360626edab1abb83209ec5808b2456ef94609d166f7
```

## 6. Prior-art assessment

There are two distinct inputs, and both are classical.

1. **The Keller Galois case.**  The original sources are:
   [Campbell (1973)](https://doi.org/10.1007/BF01349234),
   [Razar (1979)](https://doi.org/10.1007/BF02764906), and
   [Wright (1981)](https://doi.org/10.1215/ijm/1256047158).
   Wright explicitly presents Theorem 3.7 as Campbell's theorem over
   \(\mathbb C\), proves it algebraically, and states the characteristic-zero
   version.
2. **Galois cover versus regular action.**  This is the coset-action form of
   elementary Galois theory and the standard Galois correspondence for
   connected covers.  The [Stacks Project, Tag
   03SF](https://stacks.math.columbia.edu/tag/03SF) lists, for a connected
   finite étale cover, equivalence with the automorphism group acting simply
   transitively on a geometric fiber.  An explicit older monodromy statement
   appears in [Kuiken (1981), pp.
   1143--1144](https://doi.org/10.4153/CJM-1981-086-4): a cover is Galois iff
   the monodromy group has order equal to the number of sheets, hence is in the
   regular representation; the same discussion gives the core-free coset
   action and notes that a faithful transitive abelian action is regular.

The [official TransGrp
manual](https://docs.gap-system.org/pkg/transgrp/doc/manual.pdf) states that
the library gives representatives up to conjugacy in the relevant symmetric
group and that the degree-\(\leq 11\) list was already published by Butler and
McKay.  The low-degree table above is therefore a routine extraction from a
standard classification.

**Prior-art conclusion:** the sentence “Campbell--Razar--Wright excludes
Galois \(L/K\), equivalently it excludes regular natural monodromy” is a
correct and useful reformulation, but it is merely classical.  Likewise,
“counterexample monodromy is nonabelian” and the degree-\(2\)/degree-\(3\)
consequences are immediate group-theoretic corollaries.  Novelty would have to
come from additional Keller-specific restrictions, a new realizability or
nonrealizability theorem for nonregular actions, or explicit structural data
for a particular map—not from this translation itself.
