# Lossless reconstruction of the degree-three source union bases

## Problem

The complete numerical fixed-marginal cache stores every post-Omega source
block and its branch maps, but deliberately discards the raw union basis in
the tensor product of three (S_7) Specht multiplicity spaces.  Those bases
are needed to apply the local partial-transpose crossing to a saved source
candidate.  Retaining every basis simultaneously would use about (1.17) GB
in double precision.

## Reconstruction identity

For one ordered source block, let

\[
U\in\mathbb R^{D\times r}
\]

be the discarded orthonormal post-Omega union basis.  Concatenate all raw
projected branch images into

\[
V=[V_1\ \cdots\ V_k]\in\mathbb R^{D\times q}.
\]

The cache retains their coordinates

\[
M=[U^{\mathsf T}V_1\ \cdots\ U^{\mathsf T}V_k]
  =U^{\mathsf T}V\in\mathbb R^{r\times q}.
\tag{1}
\]

By construction, the columns of (V) span the union and therefore

\[
V=UM.
\tag{2}
\]

The full marginal cache includes every reachable target block, so (M) has
full row rank.  Multiplying (2) by (M^{\mathsf T}) gives the exact recovery
formula

\[
\boxed{
U=VM^{\mathsf T}(MM^{\mathsf T})^{-1}.
}
\tag{3}
\]

This reconstructs the orientation used by the saved source variables, not
merely the same abstract subspace.  It also avoids repeating the large SVD
that originally selected (U).

## Implementation and audits

`discovery/agent_dth_level2_reconstruct_union.py` rebuilds one source block
at a time.  It uses the target bases already stored in the cache, recreates
the exact branch ordering, applies the Grassmann and Omega projectors, and
then evaluates (3).  The Omega range has dimension at most three, so its
orthonormal orientation is irrelevant to the resulting projector.

For every reconstructed block the code checks

\[
UM=V,\qquad U^{\mathsf T}V=M,\qquad U^{\mathsf T}U=I,
\]

as well as membership in the degree-three Grassmann range and annihilation
by the prolonged Omega Gram operator.

The module exposes `reconstruct_union(block, target_data)`.  A crossed
PPT/Lanczos solver can stream through the ordered source blocks, reconstruct
one (U), contract the corresponding saved density, and release it before
moving to the next block.

## Exact counterpart

Equation (3) is an identity, but the present cache and reconstruction are
floating-point discovery data.  An exact certificate should use the rational
seed-Gram basis from
`notes/agent_dth_level2_rational_seed_compression.md` and the exact rational
branch matrices from
`notes/agent_dth_level2_rational_branch_intertwiners.md`.

The reconstruction closes an implementation gap for deciding whether the
strict holomorphic extension also lies in the Γ_A cone.  It does not itself
assert PPT feasibility or infeasibility.
