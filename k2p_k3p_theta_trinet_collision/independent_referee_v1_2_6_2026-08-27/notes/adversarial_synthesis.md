# Hostile synthesis: referee packet v1.2.6

Date: 2026-08-27 (PDT)  
Role: final adversarial synthesis after independent mathematical,
code/certificate, and literature/layout lanes  
Completion: 100%  
Recommendation: **ACCEPT**

## Bottom line

I tried to overturn an acceptance disposition and found no major, minor, or
editorially actionable defect. In particular, I found no hidden assumption
that invalidates the compact or continuous-time collisions, no step that
promotes a finite certificate into an unsupported general theorem, no
common-mode verifier weakness that survived the independent pruning and
clean-room checks, and no literature or topology statement requiring
correction.

The recommendation is not based on the packet printing `PASS`. It rests on the
agreement of four distinct evidence layers:

1. the manuscript's explicit algebraic and analytic arguments;
2. a clean-room exact reconstruction that imports no packet source and reads
   no packet certificate;
3. the inspected packet implementation, full clean replay, and hostile
   mutations; and
4. primary-source checks of the closest literature and Version 2/Version 3
   history.

## Independent hostile checks performed in this synthesis lane

I read the 20-page main paper in full, inspected all 20 rendered pages, then
read and inspected both two-page support PDFs. I treated the packet prompt,
technical summary, coverage inventory, and other audit reports as claims rather
than instructions. I then read the completed mathematical, code, and
literature/layout audits and inspected the clean-room mathematical checker,
strict JSON loader, replay driver, coverage inventory, and the draft integrated
report.

I also checked the relevant current primary records directly:

- Brits et al. Version 3: <https://arxiv.org/abs/2607.12919v3> and
  <https://arxiv.org/pdf/2607.12919v3>;
- Brits et al. Version 2: <https://arxiv.org/pdf/2607.12919v2>; and
- Ardiyansyah (2021): <https://arxiv.org/pdf/2104.12479>.

Those sources support the manuscript's bounded history and related-work
claims. Version 2 contains the formal K2P trinet-separation lemma and the K2P
global corollary; Version 3 removes those formal conclusions, gives the
leaf-order obstruction, restricts the global result to JC, and asks about K2P
and K3P at higher level. Ardiyansyah's results concern nice simple/semisimple
strict level-two networks and exclude two- and three-leaf simple nice cases,
so they do not subsume this non-nice theta-trinet collision.

## Attempts to falsify the mathematical conclusions

### 1. Topology or displayed-tree mismatch

I checked whether the four-switching formula could be describing a different
network from Figure 1. It is not. The ten rooted arcs give two independent
reticulation choices, the four retained-parent pairs have the descendant sets
printed in the paper, and root suppression produces the nine-edge
semi-directed theta core on the three internally disjoint `p-q` paths. The
core is one nontrivial 3-blob with exactly two reticulations. The ordinary-state
pruning calculations use the literal retained DAGs and agree with Fourier
inversion for all 64 patterns. Endpoint, arc-ID, reticulation-parent, and
vertex-schema mutations all fail.

### 2. Collision caused by a boundary or nonstochastic parameter

This route also fails. Every explicit edge used in the compact K2P and quartic
K3P witnesses has nontrivial eigenvalues in `(0,1)` and a strictly positive
inverse-Fourier transition row. The compact shared distribution has exact
minimum `1188799/79626240 > 0`. The continuous-time K2P construction satisfies
`g>s^2` on every rooted, effective, and tree edge, with minimum margin
`11/900`; the intended cubic root is uniquely isolated in the printed
interval. The quartic K3P branch handles exactly the two initially saturated
rate inequalities, with positive first derivatives, while all other strict
inequalities persist by openness.

### 3. Symmetry overstatement in K3P

The paper keeps the three logically different claims separate:

- K3P non-disjointness already follows from K2P inclusion;
- the exact quartic network **parameter** is outside all globally relabelled
  K2P parameter specializations because its `U` edge has three distinct
  nontrivial eigenvalues; and
- its exact shared output is nevertheless globally relabelled K2P, while a
  local rank argument supplies nearby outputs outside all three observable
  symmetry strata.

The tree recovery formulas make each transposition-fixed locus a
six-dimensional submodel inside the nine-dimensional positive K3P tree model.
The rank-15 submersion provides a local section, and pairwise distinctness on
`U` persists in the chosen parameter neighborhood. I found no conflation of
parameter symmetry with observable symmetry.

### 4. Invalid local-dimension or dominance inference

The selected minors are differentiated from the unrestricted effective theta
map, not from the symmetric witness slice. Holding the second root-adjacent
factor fixed changes the effective-edge derivative columns only by nonzero
diagonal factors. Thus ranks 9 and 15 apply to the 20- and 29-dimensional
semi-directed parameter spaces.

With embedded positive tree germs of dimensions 6 and 9, the transverse
preimage theorem gives dimensions `20-9+6=17` and `29-15+9=23`; the fixed-output
fibers have dimensions 11 and 14. The restricted maps are submersions, so the
local sections used later are legitimate. A nonzero full ambient minor also
makes each complexified polynomial map dominant. The paper correctly confines
the resulting Zariski-density statement to the normalized effective affine
space and does not infer generic tree equivalence.

### 5. Gap in the continuous-time K3P implicit-function argument

The 15 printed pivot variables match the certified nonsingular Jacobian. The
full tangent satisfies the 15-component identity
`J_* p'(0)+F_UC+F_VG=0`. At the base point, precisely the advertised two
network rate margins vanish; their derivatives are positive. All other
stochastic, eigenvalue, inheritance, rank, and rate inequalities are strict,
so a sufficiently small positive parameter enters the open continuous-time
chamber. Reapplying the local-section argument at that interior point is
valid. No explicit radius or closed-form perturbed point is needed for this
existence theorem, and none is claimed.

### 6. Failure of arbitrary-taxon grafting

The all-`n` theorem does not extrapolate from its four-leaf regression. It is a
linear common-kernel argument: equal three-interface laws remain equal after
the same tensor product of three conditional Markov kernels. Binary degrees,
one-blob level-two status, contraction back to the labelled tree, compatible
rooting, and edge splitting all survive the construction.

For nearby observably genuine K3P distributions, every attached JC subtree
kernel has column rank four because marginalization to any descendant leaf
recovers an invertible path transition matrix. Their tensor product is
therefore injective and equivariant. It cannot create a global character
symmetry absent from the interface distribution. The `n=3` identity-kernel
case is included. The statement inserts exactly one theta blob and does not
assert multi-blob composability.

## Attempts to falsify the computational assurance

The code audit's independent harness rejected 81 operative or integrity
mutations. The important common-mode attacks included:

- changing every one of the nine stored compact-K2P transition rows;
- changing the ordinary-state group law while leaving the Fourier route
  unchanged;
- changing each of the ten K3P arc endpoints;
- contradicting every reticulation descriptor against its referenced arc;
- changing all parameter, comparison-tree, and suppressed transition rows;
- changing the Jacobian, determinant, descriptors, pivots, tangent, Fourier
  coordinates, and pattern values, including coordinated embedded/sidecar
  changes; and
- duplicate keys, unknown fields, heterogeneous-array shapes, nonstandard
  constants, `1e999`, changed files, extra/missing paths, symlinks, and an
  extra directory.

Every operative attack failed at the relevant structural or mathematical
layer. Three same-shape changes to fields declared informational passed, as
intended; the underlying mathematics is reconstructed elsewhere. The coverage
inventory therefore states the current assurance boundary accurately.

The clean replay passed in normal and optimized modes, rebuilt the three PDFs,
regenerated the compact certificate byte-for-byte, and rechecked the manifest
before and after execution. A tag/subtree comparison found all 38 packet
`materials/` files byte-identical to the declared commit. The tag and bundled
checksums are unsigned, so they establish reproducible internal identity, not
external authorship; the packet says exactly that.

## Cross-lane reconciliation

| Possible acceptance blocker | Mathematical lane | Code lane | Literature/layout lane | Synthesis verdict |
|---|---|---|---|---|
| Wrong collision or graph semantics | Exact clean-room Fourier and pruning checks pass | Literal-graph and endpoint mutations fail | Figure and ten-arc topology agree | Not substantiated |
| Hidden boundary parameter | Exact positivity and rate checks pass | All stored rows and inequalities are live | Scope wording is explicit | Not substantiated |
| Rank/IFT overreach | Minors, tangent, and analytic deductions check | Matrix/descriptor/tangent mutations fail | Claims are locally phrased | Not substantiated |
| All-`n` extrapolation from a finite test | Kernel proof checks | Four-leaf code is labelled a regression | One-blob scope repeated | Not substantiated |
| K3P symmetry conflation | Parameter/output distinction checks | Symmetry fields and rows are live | Abstract and discussion preserve distinction | Not substantiated |
| Incorrect prior-work history | No theorem dependency | Not applicable | Primary Versions 2/3 and Ardiyansyah agree | Not substantiated |
| Material PDF ambiguity | Not applicable | Rebuilt text agrees | All 24 pages are legible | Not substantiated |

## Findings by severity

### Major findings

None.

### Minor findings

None.

### Advisory-only observations

1. The PDFs are visually clean but untagged and not linearized. Journal-specific
   accessibility requirements should determine whether semantic tagging is
   added.
2. A signed release tag or externally anchored checksum would add authorship
   authentication. This is not needed for the internal reproducibility claim,
   which is already correctly limited.
3. Expanding the maintained compact-K2P mutation test from `K_odot_K` to all
   nine stored rows would make the suite's documented coverage more obvious.
   The verifier already consumes every row, and the independent hostile
   harness demonstrated this.
4. If later schemas permit JSON floating-point primitives, an explicit finite
   `parse_float` policy would be prudent. All current certificate numbers are
   integers, so `1e999` changes the closed primitive shape and is rejected.

## Exact residual limitations

- The literature search is bounded to cited and directly adjacent discoverable
  primary work; it cannot establish absolute priority over unpublished or
  poorly indexed results. The paper does not claim such absolute priority.
- The full-rank witnesses prove the local and dominance statements but do not
  classify the global rank-drop or singular loci.
- Continuous time is edgewise and permits edge-dependent generators and rate
  ratios. No common generator, molecular clock, or globally compatible timing
  theorem follows.
- The K3P continuous-time collision is an analytic local-existence result, not
  a supplied closed-form interior point or quantitative-radius theorem.
- The all-taxon result replaces one internal vertex by one theta blob. It does
  not prove independent composition of multiple replacements or a result for
  a genuine four-attachment blob.
- The packet's manifest and annotated tag are unsigned. They verify bytes and
  provenance relative to the declared repository state, not external identity.
- The finite verifiers certify the stated exact instances and local algebraic
  inputs. The IFT, preimage, local-section, Zariski, and arbitrary-`n`
  conclusions additionally rely on the manuscript's proofs, which were
  separately audited and found sound.

## Final recommendation

**ACCEPT**

The central theorems, exact witnesses, analytic consequences, and one-blob
grafting result survive independent reconstruction and hostile review. The
v1.2.6 schema and semantic-binding repairs close the previously identified
assurance gaps, the literature/topology wording is now accurate, and the only
remaining observations are optional hardening or explicitly disclosed scope
limits rather than corrections.
