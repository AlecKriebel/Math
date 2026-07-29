# Theorem dependency map

**Paper:** *Low-Schmidt Rigidity and Tensor-Local Constraints in the
Exceptional Unitary Hecke Yang--Baxter Class*

**Audit date:** 2026-07-29

**Purpose:** record the logical dependencies and the exact scope of the
structural-frontier theorem package. Claim identifiers refer to
[`CLAIMS.md`](../CLAIMS.md). This map is not a substitute for the proofs in
the manuscript and cited notes.

## 1. Starting hypotheses and notation

Throughout, \(V\cong\mathbb C^d\), \(q=e^{i\pi/3}\), and
\[
 P=P^*=P^2\in\operatorname{End}(V\otimes V),\qquad
 \operatorname{rank}P=\frac{d^2}{2}.
\]
Set
\[
 R=qI-(1+q)P,\qquad H=I-2P.
\]
The exceptional hypothesis is that the two spatial shifts of \(R\), or
equivalently of \(P\) or \(H\), satisfy the braid-form Yang--Baxter
relation. No scalar-partial-trace, irreducibility, faithfulness, or
localization assumption is added.

The two established existence inputs are:

- **C2:** the local-dimension-two class is empty;
- **C0--C1:** an exact solution exists at \(d=4\), and identity
  stabilization gives solutions for every \(d\in4\mathbb N\).

## 2. Global dependency graph

```text
exceptional projection P
  |
  +-- no-opposite-spectrum theorem (Lechner Props. 2.3--2.4)
  |     |
  |     +-- C4: Tr_1(P)=Tr_2(P)=(d/2)I
  |             |
  |             +-- C5: eta=1/2 Markov trace at every tensor level
  |             |      |
  |             |      +-- C9: faithful representation of the
  |             |      |       trace quotient H_n(3,6)
  |             |      |
  |             |      +-- Wenzl/Rowell simple data
  |             |              |
  |             |              +-- C6: m_(lambda,n)
  |             |                       = D_lambda (d/2)^n
  |             |                       and only 2 | d is forced
  |             |
  |             +-- zero partial traces of H
  |             |
  |             +-- two-projection blocks + spatial restriction
  |                    |
  |                    +-- C17: 8 | r d^2 for every rank-r
  |                         one-leg commutant projection
  |                         |
  |                         +-- C55: OSR(H) <= 3 iff 4 | d
  |                         |
  |                         +-- C63: injective OSR-four sandwich map
  |                         |          implies 4 | d
  |                         |
  |                         +-- C33: at d=6,
  |                                  C_L(P) intersect C_R(P) = CI
  |
  +-- C9 + four-strand one-dimensional trace idempotents
  |     |
  |     +-- C38: square-invariant subspaces inherit balanced
  |              exceptional solutions
  |              |
  |              +-- restrictable descent
  |              +-- no restrictable d=6 solution
  |
  +-- primitive Weyl covariance + Bell diagonal form
  |     |
  |     +-- C60: 4 | d in that complete symmetry class
  |
  +-- four pairwise-anticommuting product involutions
        |
        +-- complementary local Clifford graphs
               |
               +-- C61: 4 | d in that precisely defined class
```

The branches ending in C60 and C61 are model-class theorems. They are not
inputs to C4--C55 or C63 and do not apply to an arbitrary exceptional
matrix.

## 3. Automatic tower structure

### 3.1 Automatic standardness (C4)

**Input:** the exceptional \(R\)-matrix hypotheses above.

**External input:** Lechner's no-opposite-spectrum result supplies the
shifted-subfactor irreducibility used in his Markov-character theorem.

**Output:**
\[
 \operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_d.
\]

The proof does not *assume* irreducibility, but the cited proof does *use*
irreducibility after deriving it. Rank half identifies the scalar as
\(d/2\); it is not what proves scalarity.

Primary local proof:
[`notes/track_structural_projection.md`](../notes/track_structural_projection.md).

### 3.2 Markov propagation and quotient faithfulness (C5, C9)

From C4, normalized tensor traces obey the Markov rule at every level:
\[
 \tau_{n+1}\!\left(\rho_{n+1}(x)P_n\right)
 =\frac12\tau_n(\rho_n(x)).
\]
This is an all-level partial-trace calculation, not an inference from the
two-strand number \(\tau_2(P)=1/2\).

If \(\operatorname{Ann}_n\) is the annihilator of the resulting Markov
trace on the specialized Hecke algebra, faithfulness of the ordinary
matrix trace gives
\[
 \ker\rho_n=\operatorname{Ann}_n.
\]
Thus C9 is precisely the injective representation
\[
 H_n(q)/\operatorname{Ann}_n
 \cong H_n(3,6)\hookrightarrow\operatorname{End}(V^{\otimes n}).
\]
It is not faithfulness of the raw specialized Hecke algebra, braid group,
or braid-group algebra.

Primary local proofs:
[`notes/track_structural_projection.md`](../notes/track_structural_projection.md)
and
[`notes/track_hecke_multiplicity.md`](../notes/track_hecke_multiplicity.md).

### 3.3 Complete abstract multiplicities and their limitation (C6)

For every admissible Jones--Wenzl label \(\lambda\),
\[
 m_{\lambda,n}=D_\lambda\left(\frac d2\right)^n,
\]
where \(D_\lambda\in\{1,2,3\}\) is the categorical dimension, not the
ordinary simple-module dimension. The formula satisfies all Bratteli
restriction recurrences and is integral exactly when \(d\) is even.

This proves that Markov weights, simple-block multiplicities, central
ranks, and their branching recurrences cannot force \(4\mid d\). It does
not construct a common two-site matrix at odd \(d/2\), and it does not
exhaust same-\(P\) tensor locality.

Proof and independent replays:
[`notes/track_hecke_multiplicity.md`](../notes/track_hecke_multiplicity.md),
[`scripts/hecke_multiplicity_spectrum.py`](../scripts/hecke_multiplicity_spectrum.py),
and
[`verifiers/verify_fusion_arithmetic_independent.py`](../verifiers/verify_fusion_arithmetic_independent.py).

## 4. Tensor-local divisibility chain

### 4.1 One-leg projection arithmetic (C17)

C4 supplies the ranks and overlap trace on the invariant spectator sector.
The abstract two-projection block theorem then gives common-one and
common-zero multiplicities \(rd^2/8\). Hence a rank-\(r\) projection in
either one-leg commutant forces
\[
 8\mid rd^2.
\]
In particular, when \(d\equiv2\pmod4\), neither leg commutant contains an
odd-rank projection.

Proof and replay:
[`notes/controlled_leg_divisibility.md`](../notes/controlled_leg_divisibility.md)
and
[`verifiers/verify_controlled_leg_divisibility.py`](../verifiers/verify_controlled_leg_divisibility.py).

### 4.2 Complete low-Schmidt spectrum (C55)

The dependency chain is:

```text
OSR(H)=2 or 3
  |
  +-- Cohen--Yu / Chen--Yu:
  |      four-local equivalence to a controlled unitary
  |
  +-- one legitimate same-site conjugacy
  |      (the four-local equivalence itself is not a YBE equivalence)
  |
  +-- Hermiticity support graph
         |
         +-- nonbipartite component -> true rank-one leg projection
         |
         +-- all bipartite -> cubic equates a unitary with
                              (1/3) times a unitary, impossible
  |
  +-- C17 -> 4 | d
```

Rank one is immediate. The known \(d=4\) OSR-three witness and identity
stabilization prove the converse. Therefore
\[
 \exists H\text{ exceptional with }\operatorname{OSR}(H)\le3
 \quad\Longleftrightarrow\quad4\mid d.
\]

Proof, source audit, and replay:
[`notes/low_schmidt_control_obstruction.md`](../notes/low_schmidt_control_obstruction.md),
[`reviews/final_groups_III_IV_audit.md`](../reviews/final_groups_III_IV_audit.md),
and
[`verifiers/verify_low_schmidt_control_obstruction.py`](../verifiers/verify_low_schmidt_control_obstruction.py).

### 4.3 Unrestricted OSR four (C63)

For \(\operatorname{OSR}(H)=4\), let \(\mathcal A,\mathcal B\) be the
intrinsic Schmidt supports. Projecting an outer leg of the full cubic
modulo \(\mathbb CI+\mathcal A\), and symmetrically modulo
\(\mathbb CI+\mathcal B\), gives the all-input quotient identities. If a
joint-sandwich map is injective, the corresponding five-dimensional
operator system is a \(C^*\)-algebra. Such an algebra has a rank-one
projection in its commutant, and C17 forces \(4\mid d\).

Thus a hypothetical OSR-four solution with \(d\equiv2\pmod4\) must have
nonzero Hermitian traceless common sandwich annihilators on **both** legs.
C63 does not prove that every OSR-four solution has \(4\mid d\).

Proof, hostile audit, and replay:
[`notes/osr4_joint_sandwich_degeneracy.md`](../notes/osr4_joint_sandwich_degeneracy.md)
and
[`verifiers/verify_osr4_joint_sandwich_degeneracy.py`](../verifiers/verify_osr4_joint_sandwich_degeneracy.py).

## 5. Square restrictions and leg intersections

### 5.1 Square-invariant inheritance (C38)

C9 kills both one-dimensional four-strand Jones--Wenzl idempotents.
Their trace polynomials at a restricted Markov parameter \(\eta\) have the
unique common zero \(1/2\). Therefore every nonzero square-invariant local
subspace inherits a non-scalar balanced exceptional solution and has even
dimension.

Consequences:

- a two-dimensional square-invariant subspace is impossible in \(d=6\);
- if both \(W^{\otimes2}\) and \((W^\perp)^{\otimes2}\) are invariant,
  a \(d\equiv2\pmod4\) solution descends to a smaller solution in the same
  congruence class;
- no \(d=6\) solution is restrictable.

A four-dimensional **one-sided** square-invariant subspace in \(d=6\)
remains open; its two-dimensional orthogonal complement would necessarily
leak.

Proof and replay:
[`notes/restrictable_four_strand_obstruction.md`](../notes/restrictable_four_strand_obstruction.md)
and
[`verifiers/verify_restrictable_four_strand_obstruction.py`](../verifiers/verify_restrictable_four_strand_obstruction.py).

### 5.2 Scalar common-leg intersection at \(d=6\) (C33)

C17 reduces a nontrivial projection in
\(\mathcal C_L(P)\cap\mathcal C_R(P)\) to rank two. Its \(2\times2\) cell
is scalar by the determinant gap and C2; the cubic propagates that scalar
to \(W\otimes V\), contradicting C4. Hence
\[
 \mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6.
\]

This statement concerns only the intersection after identifying the two
local matrix algebras. It does not prove that either
\(\mathcal C_L(P)\) or \(\mathcal C_R(P)\) is scalar separately.

Proof and replay:
[`notes/d6_two_block_leg_types.md`](../notes/d6_two_block_leg_types.md)
and
[`verifiers/verify_d6_two_block_leg_types.py`](../verifiers/verify_d6_two_block_leg_types.py).

## 6. Main model-class theorems

### 6.1 Primitive-Weyl Bell diagonal (C60)

The hypotheses are a **primitive** \(d\)-dimensional Weyl pair and
diagonality in its fixed generalized Bell basis. The common Weyl
\(M_d\)-action makes every eigenvalue multiplicity of
\(H_{12}H_{23}\) divisible by \(d\). The exceptional cubic and balance
give multiplicities
\[
 \frac{d^3}{4},\qquad\frac{3d^3}{8},\qquad\frac{3d^3}{8},
\]
so \(4\mid d\). This proves the complete primitive-Weyl Bell-diagonal
\(d=6\) branch empty, but says nothing about arbitrary Bell bases or
arbitrary exceptional solutions.

Proof, audit, and replays:
[`notes/weyl_bell_diagonal_divisibility.md`](../notes/weyl_bell_diagonal_divisibility.md),
[`reviews/final_groups_III_IV_audit.md`](../reviews/final_groups_III_IV_audit.md),
[`verifiers/verify_weyl_bell_diagonal_divisibility.py`](../verifiers/verify_weyl_bell_diagonal_divisibility.py),
and
[`verifiers/verify_d4_bell_diagonal_exhaustive.py`](../verifiers/verify_d4_bell_diagonal_exhaustive.py).

### 6.2 Four-product Clifford frames (C61)

The load-bearing hypothesis is that the four **product terms**
\(A_j\otimes B_j\) are pairwise anticommuting. It does not say that
either local family is itself pairwise anticommuting. Complementary local
commutation graphs and Clifford representation divisibility then force
\(4\mid d\).

This is a theorem for that precisely defined product-involution class,
not for unrestricted OSR four.

Proof, audit, and replay:
[`notes/osr4_clifford_frame_parity_audit.md`](../notes/osr4_clifford_frame_parity_audit.md),
[`reviews/final_groups_III_IV_audit.md`](../reviews/final_groups_III_IV_audit.md),
and
[`verifiers/verify_osr4_clifford_frame_parity.py`](../verifiers/verify_osr4_clifford_frame_parity.py).

## 7. The exact dimension-six frontier

Combining only the proved implications above, any hypothetical
dimension-six exceptional reflection \(H\) satisfies:

1. \(\operatorname{OSR}(H)\ge4\);
2. if \(\operatorname{OSR}(H)=4\), both intrinsic joint-sandwich maps are
   singular and carry Hermitian traceless coefficient-matrix
   annihilators;
3. it has no two-dimensional square-invariant local subspace and is not
   restrictable;
4. \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6\);
5. it is not primitive-Weyl Bell diagonal;
6. it does not belong to the four-product Clifford-frame class.

The following stronger conclusions are **not** dependencies or theorem
consequences:

- \(\operatorname{OSR}(H)\ge5\);
- scalarity of either individual leg commutant;
- absence of a four-dimensional one-sided square-invariant subspace;
- nonexistence at \(d=6\);
- the complete dimension spectrum being \(4\mathbb N\).

## 8. Additional \(d=4\) family (C53)

The exact color/face circle from C15 is one orbit under sitewise-unitary
conjugacy and is not sitewise-unitarily conjugate to the published
five-Pauli witness. The fourth flip moment proves this finer distinction.
Both families nevertheless have the same \([q,\eta,d]\) and are therefore
equivalent under Lechner's broader all-level braid-character relation.

Thus C53 does not provide a second Lechner equivalence class. Its
literature novelty has not been established. It is supplementary to the
frontier theorem package.

Proof and replay:
[`notes/no_codimension_two_cut_color_face_family.md`](../notes/no_codimension_two_cut_color_face_family.md)
and
[`verifiers/verify_no_codimension_two_cut_color_face_family.py`](../verifiers/verify_no_codimension_two_cut_color_face_family.py).

## 9. Scope guard table

| Claim | What is proved | What is not proved |
|---|---|---|
| C4 | Standardness is automatic for every exceptional matrix-class solution. | Scalar partial traces from an abstract nonspatial two-projection relation. |
| C9 | Faithfulness after quotienting by the Markov-trace annihilator. | Faithfulness of the raw Hecke or braid-group representation. |
| C6 | Complete abstract Markov/simple/central/branching arithmetic permits every even \(d\). | Existence of a same-\(P\) tensor-local model at odd \(d/2\). |
| C55 | The OSR-\(\le3\) spectrum is exactly \(4\mathbb N\). | Any classification at OSR \(\ge4\). |
| C63 | OSR-four odd-half-dimension candidates have two intrinsic sandwich degeneracies. | Four-divisibility for all OSR-four solutions. |
| C38 | Square restrictions inherit balance; two-sided restrictability is excluded at \(d=6\). | Complementary invariance from one-sided square invariance. |
| C33 | \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6\). | Scalarity of either one-sided commutant. |
| C60 | Divisibility in a fixed primitive-Weyl Bell symmetry class. | A theorem for nonprimitive or non-Weyl Bell bases. |
| C61 | Divisibility for pairwise-anticommuting product-involution frames. | A theorem for arbitrary OSR-four decompositions. |
| C53 | A finer sitewise orbit distinction at \(d=4\). | A second class under Lechner equivalence or established literature novelty. |
