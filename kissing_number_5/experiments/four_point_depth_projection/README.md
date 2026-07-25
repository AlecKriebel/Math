# Four-point depth/projection audit

This isolated research folder studies whether the exact robust slab theorem
\[
\#\{x:\langle e,x\rangle<-1/300\}\ge 7,\qquad
\#\{x:\langle e,x\rangle>1/300\}\ge 7
\]
for every unit direction \(e\) can be combined with common-pair projection
capacities to exclude a 41-point kissing code.

The scope is classification-free.  Discovery computations are kept here and
must not be confused with the exact certificates elsewhere in the repository.

Current status: the direct synthesis is blocked by an exact countermodel.
The certified 41-point subset of the rank-six \(E_6\) root system satisfies
the robust depth theorem, every **code-base** numerical common-pair
capacity (including the positive contact-base cap seven), every resulting
nonnegative weighted inequality, and all local Gram conditions through
four points.  It fails global rank five, the degree-two \(S^4\) harmonic
inequality, and a stronger common-pair family using arbitrary auxiliary
axes.  See
`e6_rank6_shadow_countermodel.md` and run the independent exact verifier
listed there.

The centered all-degree quarter-grid pair/triple witness also survives the
full continuum of exact base-stratified depth rows coming from every
direction \(\lambda y+\mu z\).  The exact algebraic-boundary verifier and
proof are in `centered_quarter_pair_depth/`.

The first extension not represented by that witness is the exact
edge-conditioned product \(\sum_eH_e\Gamma_e\).  Its universal linear
four-point inequality and boundary audit are in
`edge_conditioned_depth_capacity_product.md`.

The first stored local Gram-PSD `K5` extension violates two exact product
rows.  This is not a marginal obstruction: an alternative exact 64-atom
local `K5` extension satisfies all 560 direction/capacity product rows.
The certificates, exact verifiers, and the distinction from global
Lasserre consistency are in `k5_product_audit/`.
