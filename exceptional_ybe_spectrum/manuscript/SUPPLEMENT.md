# Supplementary exact constructions, exclusions, and bounded searches

**Paper:** *Tensor-Local Constraints in the Exceptional Unitary Hecke
Yang--Baxter Class*

**Cutoff:** 2026-07-29

**Scope:** supporting results not needed for the main theorem package

## 1. How to read this supplement

This file separates three logically different kinds of evidence:

1. **Exact ansatz theorem:** a human-readable proof excludes every member
   of a precisely defined construction class.
2. **Exact limitation model:** an exact object shows that a proposed set of
   necessary conditions is insufficient, but is not itself an exceptional
   \(R\)-matrix.
3. **Numerical search:** a reproducible falsifier found no candidate in a
   declared search, but proves no nonexistence statement.

Only the first category is an ansatz-level nonexistence result. None of
the results below excludes an arbitrary \(d=6\) exceptional matrix unless
that scope is explicitly stated. The authoritative status ledger is
[`CLAIMS.md`](../CLAIMS.md).

The main paper retains only the broad primitive-Weyl Bell-diagonal and
four-product Clifford-frame theorems. The narrower exact branches are
collected here so the paper does not become a catalogue of failed
searches.

## 2. Exact general construction obstructions

### 2.1 Tensor products preserve the class only by spectators (C28)

If \(R\) has exceptional spectrum
\(\Sigma=\{-1,e^{i\pi/3}\}\) and the regrouped tensor product
\(R\boxtimes S\) with a unitary \(S\) again has spectrum contained in
\(\Sigma\), then \(S=I\). The multiplicative stabilizer of \(\Sigma\) is
trivial.

Thus the usual tensor-product construction gives exactly identity
stabilization. It explains the known passage \(d=4\mapsto4m\), but cannot
create \(d=6\).

- Proof:
  [`notes/tensor_product_extension_no_go.md`](../notes/tensor_product_extension_no_go.md)
- Exact replay:
  [`verifiers/verify_tensor_product_extension_no_go.py`](../verifiers/verify_tensor_product_extension_no_go.py)
- Limitation: this does not exclude colored gluing, off-diagonal coupling,
  or an unrelated solution.

### 2.2 Non-scalar monomial unitary Hecke matrices (C11)

No non-scalar monomial unitary matrix can simultaneously have the required
two-root Hecke polynomial and satisfy the ordinary Yang--Baxter equation.
Cycle structure reduces the problem to a diagonal Yang--Baxter equation.

- Proof:
  [`notes/track_additive_constructions.md`](../notes/track_additive_constructions.md)
- Limitation: “monomial” is a basis-dependent ansatz and is not forced by
  the exceptional relations.

### 2.3 Majid--Markl associative Hecke gluing (C58)

At the exceptional phase, the canonical mixed two-dimensional block in
the Majid--Markl associative gluing is not unitary for any positive
tensor-square local metric. More generally, in their full operator-valued
mixed-block form on a nontrivial **orthogonal** Hilbert direct sum, the
quadratic relation forces
\[
 T=(\lambda+\mu)I,
\]
whereas unitarity forces \(T=0\) for non-opposite roots.

- Proof:
  [`notes/majid_markl_gluing_unitarity_no_go.md`](../notes/majid_markl_gluing_unitarity_no_go.md)
- Exact replay:
  [`verifiers/verify_majid_markl_gluing_no_go.py`](../verifiers/verify_majid_markl_gluing_no_go.py)
- Limitation: the theorem does not cover arbitrary colored mixed blocks
  outside that gluing geometry or a nonorthogonal algebraic color
  splitting in the full operator-valued case.

### 2.4 Standard Manin \(GL(s|s)\) super-Hecke symmetry (C45)

The balanced one-parameter Manin super-Hecke symmetry has the ordinary
braid and Hecke relations and equal eigenvalue multiplicities after the
required normalization. At \(q=e^{i\pi/3}\), however, its two eigenspaces
cannot be orthogonal for any positive tensor-square local metric. It is
therefore not locally unitarizable. This excludes its local-basis
conjugates as well.

- Proof:
  [`notes/manin_super_hecke_unitarity_no_go.md`](../notes/manin_super_hecke_unitarity_no_go.md)
- Exact \(d=6\) replay:
  [`verifiers/verify_manin_super_hecke_d6.py`](../verifiers/verify_manin_super_hecke_d6.py)
- Limitation: this is the standard one-parameter Manin family, not every
  multiparameter super-Hecke symmetry.

## 3. Exact controlled, factor, and color exclusions

These results are now conceptually subsumed in part by the complete
low-operator-Schmidt theorem, but they remain useful independent checks of
specific construction mechanisms.

| Claim | Precisely excluded class | Exact proof / replay | Scope guard |
|---|---|---|---|
| C18 | The complete diagonal-regular group-relative ansatz \(H=\sum_x|x\rangle\langle x|\otimes L_xhL_x^*\) whenever \(d\equiv2\pmod4\), including \(C_6\) and \(S_3\). | [`notes/group_relative_ansatz_exact.md`](../notes/group_relative_ansatz_exact.md), [`verifiers/verify_group_relative_exact.py`](../verifiers/verify_group_relative_exact.py) | The proof uses its true rank-one control; it is not a theorem about arbitrary group-covariant matrices. |
| C26 | The full crossed-factor face ansatz for both \(6=3\cdot2\) and \(6=2\cdot3\), with arbitrary signature-\((3,3)\) face blocks. | [`notes/track_color_face_search.md`](../notes/track_color_face_search.md), C17 and [`verifiers/verify_controlled_leg_divisibility.py`](../verifiers/verify_controlled_leg_divisibility.py) | One leg contains a rank-three control projection. Equal-size three-color blocks are not covered. |
| C23 | Every exceptional solution on \(\mathbb C^2\otimes\mathbb C^m\), \(m\) odd, equivariant for the specified diagonal \(U(m)\) color action. | [`notes/track_weyl_h0_deformation.md`](../notes/track_weyl_h0_deformation.md), [`verifiers/verify_weyl_h0_and_swap_block_no_go.py`](../verifiers/verify_weyl_h0_and_swap_block_no_go.py) | The diagonal \(U(m)\) covariance is load-bearing. |
| C22 | The explicitly defined cyclic three-color mixed low-Schmidt family and its pure-product boundary at \(d=6\). | [`notes/track_color_low_schmidt_exact.md`](../notes/track_color_low_schmidt_exact.md), [`verifiers/verify_color_low_schmidt_no_go.py`](../verifiers/verify_color_low_schmidt_no_go.py) | Higher-Schmidt or differently coupled color blocks remain outside the theorem. |
| C16 | Rank-one Bloch-controlled reflections on \(\mathbb C^2\otimes\mathbb C^3\). | [`notes/face_rank_one_control_no_go_d6.md`](../notes/face_rank_one_control_no_go_d6.md), [`verifiers/verify_face_rank_one_control_no_go.py`](../verifiers/verify_face_rank_one_control_no_go.py) | This is a particular face/control form, not unrestricted OSR four. |

The heterogeneous blocking lemma in
[`notes/track_additive_constructions.md`](../notes/track_additive_constructions.md)
explains why the next symmetry branches are relevant: a suitable
\(12\times12\) operator on
\(\mathbb C^2\otimes\mathbb C^3\otimes\mathbb C^2\), shifted by
\(\mathbb C^2\otimes\mathbb C^3\), would block into an ordinary
\(d=6\) solution. The lemma is an equivalence only within that spectator
form; it does not say every ordinary \(d=6\) solution admits such a
factorization.

## 4. Exact finite-symmetry heterogeneous branches

### 4.1 Diagonal \(S_4\) on \(V_2\otimes V_3\otimes V_2\) (C46)

The full equivariant commutant is \(M_2(\mathbb C)\oplus M_2(\mathbb C)\).
The central balanced choices and the complete noncentral
\(S^2\times S^2\) branch are empty. The noncentral proof has both a real
case split and an exact unit-ideal certificate.

- Proof:
  [`notes/s4_equivariant_exact_no_go.md`](../notes/s4_equivariant_exact_no_go.md)
- Exact central replay:
  [`scripts/verify_track_additive_s4_central.py`](../scripts/verify_track_additive_s4_central.py)
- Exact noncentral replay:
  [`verifiers/verify_s4_equivariant_noncentral_no_go.py`](../verifiers/verify_s4_equivariant_noncentral_no_go.py)

### 4.2 Reversed diagonal \(S_4\) on \(V_3\otimes V_2\otimes V_3\) (C54)

The reversed ordering has a different commutant,
\[
 \mathbb C^2\oplus M_2(\mathbb C)^{\oplus3}.
\]
All balanced signatures, paired under complementation, are excluded by
exact real-rational coordinate ideals.

- Proof:
  [`notes/s4_reversed_equivariant_no_go.md`](../notes/s4_reversed_equivariant_no_go.md)
- Exact replay:
  [`verifiers/verify_s4_reversed_equivariant_no_go.py`](../verifiers/verify_s4_reversed_equivariant_no_go.py)

### 4.3 Binary tetrahedral symmetry (C47)

For the defining binary-tetrahedral module \(A=\mathbb C^2\) and its
rotation module \(B=\mathbb C^3\),
\[
 A\otimes B\otimes A
 \cong1\oplus1'\oplus1''\oplus3^{\oplus3}.
\]
Up to complement, the complete balanced equivariant branch is
\(\mathbb{CP}^2\). Three exact residual entries exclude every point of
that projective parameter space.

- Proof:
  [`notes/binary_tetrahedral_cp2_no_go.md`](../notes/binary_tetrahedral_cp2_no_go.md)
- Independent exact replays:
  [`scripts/verify_binary_tetrahedral_cp2_ansatz.py`](../scripts/verify_binary_tetrahedral_cp2_ansatz.py)
  and
  [`scripts/verify_binary_tetrahedral_cp2_no_go.py`](../scripts/verify_binary_tetrahedral_cp2_no_go.py)

All three theorems require the displayed finite-group covariance. They
are not evidence that a hypothetical \(d=6\) solution must have no finite
symmetry.

## 5. Exact Weyl-functional and fixed-pairing exclusions

The main paper proves the complete primitive-Weyl Bell-diagonal theorem.
Two narrower exact calculations are retained as independent checks:

- **Cyclic Gaussian-functional branch (C13).** For the standard
  six-dimensional Gaussian Weyl generator \(U\), every balanced
  Hermitian involution \(H=f(U)\) is one of
  \(\binom63=20\) sign functions. Exact twisted-group-algebra expansion
  excludes all twenty.
  Proof:
  [`notes/root_gaussian_functional_no_go.md`](../notes/root_gaussian_functional_no_go.md);
  replay:
  [`scripts/search_gaussian_functional_d6.py`](../scripts/search_gaussian_functional_d6.py).

- **Fixed Weyl cubic pairings (C24).** Pairings which preserve the two
  specified nine-dimensional Weyl coefficient blocks, or interchange the
  two whole blocks, fail involutivity exactly.
  Proof:
  [`notes/track_weyl_h0_deformation.md`](../notes/track_weyl_h0_deformation.md);
  replay:
  [`verifiers/verify_weyl_h0_and_swap_block_no_go.py`](../verifiers/verify_weyl_h0_and_swap_block_no_go.py).

The latter does not cover arbitrary mixing between the two blocks or the
additional coefficient direction.

## 6. Exact amplification-and-cut obstructions

### 6.1 Published five-Pauli witness (C40)

For every \(m\ge2\), the identity amplification of the published
\(d=4\) witness to local dimension \(4m\) has no square-invariant local
subspace of dimension \(4m-2\). In particular, the known \(d=8\)
amplification cannot be cut to \(d=6\).

- Proof:
  [`notes/no_rank_six_subspace_of_d8_amplification.md`](../notes/no_rank_six_subspace_of_d8_amplification.md)
- Independent audit:
  [`notes/no_rank_six_subspace_of_d8_amplification_audit.md`](../notes/no_rank_six_subspace_of_d8_amplification_audit.md)
- Independent exact replays:
  [`verifiers/verify_no_rank_six_subspace_of_d8.py`](../verifiers/verify_no_rank_six_subspace_of_d8.py)
  and
  [`verifiers/verify_no_rank_six_subspace_of_d8_independent.py`](../verifiers/verify_no_rank_six_subspace_of_d8_independent.py)

### 6.2 Color/face \(d=4\) family (C53)

The same no-codimension-two-cut theorem holds for every identity
amplification of the exact color/face circle described below.

- Proof:
  [`notes/no_codimension_two_cut_color_face_family.md`](../notes/no_codimension_two_cut_color_face_family.md)
- Exact replay:
  [`verifiers/verify_no_codimension_two_cut_color_face_family.py`](../verifiers/verify_no_codimension_two_cut_color_face_family.py)

These results close two natural “amplify to \(4m\), then restrict to
\(4m-2\)” constructions. They do not constrain a genuinely new solution
already living in dimension \(4m-2\).

## 7. The additional \(d=4\) color/face family

The equal-sector color/face equations contain the exact circle
\[
 s^2+2t^2=1.
\]
The circle is one continuous orbit under sitewise-unitary conjugacy. Its
fourth flip moment is \(-16/3\), whereas the published five-Pauli witness
has fourth flip moment \(16\); hence the two sitewise-unitary orbits are
distinct.

This is a distinction under a finer equivalence only. Both have the same
triple \([q,\eta,d]\) and are equivalent under Lechner's all-level
braid-character equivalence. The calculation therefore does **not**
produce a second class in Lechner's classification. Literature novelty of
the color/face formula has not been established.

- Original exact family and replay:
  [`notes/track_color_face_search.md`](../notes/track_color_face_search.md),
  [`scripts/verify_color_face_d4_family.py`](../scripts/verify_color_face_d4_family.py)
- Orbit, invariant, and cut theorem:
  [`notes/no_codimension_two_cut_color_face_family.md`](../notes/no_codimension_two_cut_color_face_family.md),
  [`verifiers/verify_no_codimension_two_cut_color_face_family.py`](../verifiers/verify_no_codimension_two_cut_color_face_family.py)

For these reasons the family is supplementary rather than a central
theorem of the frontier paper.

## 8. Exact limitation models: what several invariants cannot prove

The following exact objects are deliberately **not** exceptional
\(d=6\) witnesses. Their role is to prevent invalid obstruction arguments.

| Claim | Exact limitation | Why it is not a witness |
|---|---|---|
| C19 | Evans--Pugh \(D^{(6)}\) cells give the exceptional operator on a 20-dimensional composable-path space; zero and scalar completions on the 100-dimensional edge square fail. | A path-space connection is not an ordinary operator on \((\mathbb C^6)^{\otimes2}\); a nontrivial vertex--face conversion remains open. |
| C20--C21 | The derived channel identities admit an exact Weyl-diagonal \(d=6\) model, and identical Schmidt pairing satisfies the cubic with the wrong quadratic. | The channel model is not a common projection; the paired operator is not an involution and has multiplicities \(9,27\). |
| C41--C44 | One-sided square invariance has an exact leakage variance; standardness and an inherited \(d=4\) abstract subrepresentation do not force the complementary square in nonspatial models. | The countermodels fail the ambient cubic or do not arise as \(P\otimes I,I\otimes P\) from one common \(P\). |
| C62 | Four-strand simple blocks, polar pairings, and trace closures admit an exact abstract \(d=6\) module with odd nonreal multiplicity \(81\). | It is an abstract \(H_4(3,6)\)-module, not a same-\(P\) tensor-local realization. |
| C64 | A standard trace-zero OSR-four involution in \(d=6\) has anticommuting shifts, normalized exceptional residual \(8/9\), and is stationary on the fixed-rank Schmidt search manifold. | Its cubic coefficient is \(1\), not \(1/3\). |

Replays:

- C19:
  [`scripts/audit_evans_pugh_d6_connection.py`](../scripts/audit_evans_pugh_d6_connection.py),
  [`verifiers/verify_evans_pugh_d6_from_cells.py`](../verifiers/verify_evans_pugh_d6_from_cells.py)
- C20--C21:
  [`verifiers/verify_channel_d6_abstract_model.py`](../verifiers/verify_channel_d6_abstract_model.py)
- C41--C44:
  [`verifiers/verify_one_sided_square_invariance.py`](../verifiers/verify_one_sided_square_invariance.py),
  [`verifiers/verify_one_sided_cubic_abstract_countermodel.py`](../verifiers/verify_one_sided_cubic_abstract_countermodel.py)
- C62:
  [`verifiers/verify_four_strand_nonreal_pairing_limitation.py`](../verifiers/verify_four_strand_nonreal_pairing_limitation.py)
- C64:
  [`verifiers/verify_osr4_shifted_anticommuting_trap.py`](../verifiers/verify_osr4_shifted_anticommuting_trap.py)

## 9. The bounded one-sided \(4+2\) extension audit (C65)

Fix \(V=W\oplus U\), \(\dim W=4\), \(\dim U=2\), and require only that
\(W\otimes W\) reduce to the published \(d=4\) projection. The arbitrary
rank-ten projection on
\[
 (W\otimes U)\oplus(U\otimes W)\oplus(U\otimes U)
\]
has six independent projection-block equations, six scalar-partial-trace
equations, and a master formula covering all \(64\) color blocks of the
full cubic. No off-diagonal leakage block is set to zero.

This is a complete exact reduction of that branch, but the equations have
not been proved to force the complementary square
\((U\otimes U)\) invariant.

- Reduction:
  [`notes/one_sided_fixed_h4_extension_audit.md`](../notes/one_sided_fixed_h4_extension_audit.md)
- Exact color-block replay:
  [`verifiers/verify_one_sided_fixed_h4_color_blocks.py`](../verifiers/verify_one_sided_fixed_h4_color_blocks.py)

The corrected numerical search froze the \(16\times16\) published block in
every tangent step. Fifteen predeclared runs and separate leakage-targeted
runs found no candidate; the best recorded residual was
\(6.0112\ldots\). This numerical statement is not a nonexistence theorem.
The still-open exact question is whether the mixed-sector cubic forces the
two leakage blocks into \(U\otimes U\) to vanish.

## 10. Numerical evidence, kept separate

| Claim | Declared numerical scope | Outcome | Permitted conclusion |
|---|---|---|---|
| C14 | Calibrated unrestricted Grassmann and structured shifted-operator searches at \(d=6\). | No exact candidate was recognized. | Search record only; no global or ansatz-level nonexistence. |
| C32 | One predeclared full-\(U(6)\) run in each of nine exact three-color cell-rank orbits. | Every final residual was at least \(6\). | No theorem even for the continuously parameterized orbit classes. |
| C36 | Forty predeclared runs in the complete retained 361-real-parameter traceless-Hermitian Weyl coefficient frame. | Endpoints fell near two exact nonexceptional mechanisms. | No nonexistence theorem for that frame or for arbitrary \(d=6\). |
| C49 | Sixteen Grassmann runs initialized near the orthogonalized Manin eigenspace. | Runs returned near the exact nonexceptional projection. | Basin calibration only; not a local-minimum theorem. |
| C65 | Fifteen frozen-\(H_4\) and additional leakage-targeted one-sided \(4+2\) runs. | No candidate; best residual \(6.0112\ldots\). | No theorem that one-sided invariance forces complementary invariance. |

Provenance and raw data are linked from:

- [`notes/track_d6_falsifier.md`](../notes/track_d6_falsifier.md);
- [`notes/d6_weyl_full_coefficient_search.md`](../notes/d6_weyl_full_coefficient_search.md);
- [`notes/one_sided_fixed_h4_extension_audit.md`](../notes/one_sided_fixed_h4_extension_audit.md);
- [`EXPERIMENTS.md`](../EXPERIMENTS.md);
- the corresponding machine-readable files under
  [`results/`](../results/).

No numerical residual, optimizer convergence, or failure to find a
candidate is used in the main paper's theorem proofs.

## 11. Surviving branch

After the main theorems and the exact supplementary exclusions, an
arbitrary \(d=6\) solution is still logically possible. It must at least:

- have \(\operatorname{OSR}(H)\ge4\);
- if \(\operatorname{OSR}(H)=4\), have singular intrinsic joint-sandwich
  maps on both legs;
- be nonrestrictable, while possibly retaining a four-dimensional
  one-sided square-invariant subspace;
- satisfy
  \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6\), without either
  individual leg commutant being known scalar;
- lie outside the primitive-Weyl Bell-diagonal and four-product
  Clifford-frame classes;
- avoid every narrower exact construction class catalogued above.

The complete dimension spectrum therefore remains open. This supplement
records the boundary of the proved exclusions without promoting their
union to an unrestricted nonexistence claim.
