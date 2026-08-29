# Lost-bridge global-transfer audit

## Verdict

`PASS`.

Let `N,N′` be binary standard semi-directed strongly tree-child level-2
networks on the same labelled leaf set. Assume source-relative regular
full-dimensional K3P containment on the strict principal domain:

```text
Φ_N(θ) = Φ_N′(σ(θ))   for every θ in a nonempty source-open regular set U.
```

Then `Cut(N) = Cut(N′)`.

The reverse inclusion that was previously missing follows from the completed
204-direction pointwise K3P obstruction. The reduction uses only the already
proved direction `Cut(N′) ⊆ Cut(N)`, the networks' reduced bridge trees
separately, the strong-tree-child primitive/compression theorem, direct
four-leaf marginalization, and the pointwise 204-direction certificate. It
assumes neither a common bridge tree nor bridge-tree equality and imports no
fourteen-orbit relation.

## 1. Exact hypotheses and the previously proved direction

The containment convention supplies a regular source point, a connected
Euclidean-open source parameter set `U`, and a physical analytic target
section. It does not supply target regularity or a target-open image.

For any labelled split `R` that is a target bridge split, every target 5 by 5
flattening minor for `R` vanishes identically. After composition with `σ`, all
corresponding source pullbacks vanish on `U`. If `R` were a source noncut, the
displayed-tree boundary specialization and explicit quartet minor in the
article make at least one pullback a nonzero source polynomial. A nonzero real
polynomial cannot vanish on `U`. Therefore

```text
R in Cut(N′)  implies  R in Cut(N).
```

The active machine handoff for this paragraph is
`K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json`. It binds the displayed-tree
boundary lemma, the literal two-term wrong-quartet minor, all 808,642 balanced
words, and all 379,742 reduced-palette presentations (zero survivors). Its
proof DAG has nine implication steps and explicitly records that neither the
legacy `CUT_GLOBAL_LOGIC_REPORT.json` nor a JC cut theorem is load-bearing.
The direct verifier checks the full 15-node transfer DAG and rejects 39/39
targeted mutations, including coherent premise substitution and deletion.

Only this direction is used below. The argument does not smuggle in the
reverse inclusion being proved.

## 2. A lost source split is nontrivial

Assume for contradiction that `S = A | B` is in `Cut(N)` but not in
`Cut(N′)`. If either side were a singleton, its pendant leaf edge would
realize `S` in every standard network on the label set. Thus `|A| ≥ 2` and
`|B| ≥ 2`. This disposes of all trivial splits before the crossing argument.

## 3. Target bridge-tree dichotomy without a common tree

Use only the target reduced bridge tree `T′`. Color every labelled leaf by
membership in `A` or `B`, and let `H_A,H_B` be the minimal subtrees of `T′`
spanning the two color classes.

The hulls cannot be disjoint: an edge on the path between disjoint hulls would
realize `A | B` as a target bridge split. Hence their intersection is
nonempty. There are two possibilities.

1. The intersection contains an edge. That target bridge has at least one
   `A`-leaf and one `B`-leaf on each side.
2. The intersection is one component vertex `v`. Every branch of `T′−v` is
   monochromatic, and at least two branches have each color.

For the second assertion, if a branch at `v` contained both colors, its
incident edge would have both colors on that side. Since `v` lies in both
color hulls, each color also occurs outside the branch, producing the first
case. Membership of `v` in each hull forces at least two incident branches of
each color. Thus `v` has at least four relevant branches; in a binary standard
network it is a nontrivial bridge component rather than an ordinary trivalent
component.

This is the one-active/two-active crossing-quartet dichotomy, stated without
identifying `T′` with the source bridge tree.

## 4. The two-active target alternative is impossible

Suppose the first case occurs, and write the intervening target bridge split
as `R = C | D`. It has witnesses in all four intersections:

```text
A∩C, A∩D, B∩C, B∩D.
```

Hence `R` crosses `S`: two splits are compatible exactly when at least one of
these intersections is empty.

But `R` is a target bridge split. The already proved directional inclusion
makes `R` a source bridge split. Now both `S` and `R` would be edge splits of
the source reduced bridge tree. Any two edge splits of one tree are
compatible: after deleting the first edge, the second edge lies wholly in one
of its two components, leaving one of the four intersections empty. This
contradicts the four nonempty intersections above.

Therefore a lost source bridge can never lead to the target's two-active
central-bridge case. This compatibility step is the missing link that lets
the pointwise one-active calculation close the directed global problem.

## 5. Why the remaining target restriction is one-active

Only the single-component case `H_A ∩ H_B = {v}` remains. Choose actual labels
from two `A`-branches and two `B`-branches at `v`. Every component strictly
between `v` and one chosen label has only two selected boundaries. Ordinary
serial paths and noncentral two-boundary blobs therefore compress to effective
arms. The unique central active component is `v`.

For a level-2 strongly tree-child component, the frozen primitive theorem and
noncut word compression retain:

- the cycle or one of four directed theta cores;
- one complete minimum strong repair;
- every path-sink child role;
- at least two actual labels of each color; and
- any other required role as a zero-character completion port.

The model-independent switching-compression replay has zero survivors: a
balanced noncut coloring cannot be displayed by every switching. Choose a
switching that fails the color split. The ordinary tree quartet criterion
then chooses two actual labels of each color whose quartet remains wrong.
Zero-character completion ports keep the physical strong core intact without
becoming selected tensor boundaries.

Consequently the target marginal is one of the graph-derived four-active-port
directions in the frozen one-active universe. Independent reconstruction
checks:

- 5 primitive core templates;
- 72 active-labelled records;
- 216 labelled 2 by 2 split entries;
- 12 entries displayed by every switching and removed;
- 204 normalized wrong-split directions; and
- 204 distinct labelled direction keys.

For every split entry, displayed-by-all status is independently recomputed
from every switching descendant mask. No graph automorphism or transported
representative is used. The resulting 204 normalized signature hashes agree
entrywise with the independently verified K3P pointwise package.

## 6. Every compressed target arm remains strictly physical

Let a nonempty serial class have strict K3P transition distributions
`p_1,…,p_m` on `Z₂ × Z₂`. Each distribution has four strictly positive
entries. Serial composition is group convolution, so every entry of
`p_1 ∗ … ∗ p_m` is a sum of strictly positive products. Fourier transformation
converts convolution to coordinatewise multiplication, giving effective
spectra `(product c_i, product g_i, product t_i)` in `(0,1)^3`.

The positive inverse-Fourier entries are exactly the strict `D₃,+`
inequalities. Thus every nonempty serial edge class remains strict; an empty
path is suppressed rather than introduced as an identity-boundary parameter.

A noncentral side blob needs one additional observation. With only two
retained boundaries, each displayed switching contributes a K3P path matrix
between those boundaries. Its switching weight is a product of factors
`λ_r` and `1−λ_r`, hence is strictly positive, and the complete weights sum
to one. Marginalizing the blob gives

```text
M_eff = sum_s w_s M_s,   with w_s > 0 and sum_s w_s = 1,
```

a convex mixture of strict displayed-path K3P matrices. K3P matrices form a
linear family, so the mixture is again K3P. In probability coordinates,
every entry is a positive convex combination of strictly positive entries.
In Fourier coordinates, each nontrivial spectrum is a convex combination of
numbers in `(0,1)`, and therefore also lies in `(0,1)`. Thus a marginalized
two-boundary side blob is a strict `D₃,+` effective edge. A chain of such
edges and ordinary paths remains strict by convolution.

Each inheritance probability is retained as `λ`, becomes `1−λ` after a
parent-role flip, or disappears after summing both switches. Retained or
complemented probabilities remain in `(0,1)`.

Hence the target quartet tensor is evaluated at a strict physical point of
the exact 204-direction theorem. This is pointwise; no target regularity or
target-open marginal is needed.

## 7. Marginal identity and the rank contradiction

Let `I = {a_1,a_2,b_1,b_2}` be the selected labels. Applying the same linear
marginal map to the containment identity gives, for every `θ in U`,

```text
Marg_I Φ_N(θ) = Marg_I Φ_N′(σ(θ)).
```

In Fourier coordinates, marginalizing sets omitted leaf characters to zero.
Thus the quartet flattening is the corresponding submatrix of the full
flattening.

The source bridge realizing `A | B` survives because `I` contains two labels
on each side. Conditioning on its bridge character writes each of the four
K3P character blocks as a rank-one outer product. Therefore the source
quartet flattening has rank at most four at every source point.

The identical target quartet belongs to one of the 204 normalized one-active
wrong-split directions. The final exact package partitions those directions
as `180 + 12 + 10 + 1 + 1 = 204` and certifies each pointwise. If the full
flattening had rank at most four, its four nonzero Fourier blocks would all
have rank one, forcing the selected minor equations to vanish. The
single-minor, signed-pair, cyclic, record-43, and record-60 certificates
respectively contradict those equations. Hence the target quartet flattening
has rank greater than four at every strict physical point.

The two sides are the same tensor, so their flattening ranks cannot be both at
most four and greater than four. This contradiction proves
`Cut(N) ⊆ Cut(N′)`. Together with the previously established opposite
inclusion, the cut sets and therefore the labelled reduced bridge trees agree.

## 8. Dependency and circularity audit

The load-bearing chain is:

```text
source-relative containment
  -> target-cut implies source-cut
  -> eliminate a crossing target bridge by source-tree compatibility
  -> one central target component
  -> compress serial paths and two-boundary side blobs to strict K3P arms
  -> frozen strong-core/switching compression
  -> one of 204 normalized wrong-split directions
  -> direct four-leaf marginal identity
  -> source bridge rank <= 4 versus pointwise target rank > 4
  -> contradiction and equality of cut sets
```

Not used:

- a common bridge tree;
- bridge-tree equality;
- corresponding source/target factors;
- the fourteen-orbit collision classification;
- restoration or probe reconstruction;
- target-generic nonvanishing;
- equality of source and target image dimensions; or
- target openness/regularity along the analytic section.

The local 204 theorem is invoked only after the topology argument has produced
one physical target component. It does not presuppose common factors or a
common bridge tree, so there is no localization loop.

An independently written adversarial package in `adversarial/` byte-binds the
stable producer and verifier, rebuilds the 204 directions, checks 19,270
noncut two-colorings of labelled trees through seven vertices, and rederives
the side-blob mixture closure from exact rational K3P arithmetic. It reports
zero tree counterexamples and rejects 35/35 targeted proof mutations. A
separate release verifier sits above both sealed layers, avoiding a circular
hash dependency while making the theorem manifest fail closed against a
change to either layer.

## 9. Replay

From the project root:

```bash
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/build_k3p_cut_inclusion_evidence.py
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/build_global_transfer.py
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py --mutations
.venv/bin/python -O cut_recovery/strong_crossbridge/global_transfer/verify_global_transfer.py --mutations --report cut_recovery/strong_crossbridge/global_transfer/OPTIMIZED_VERIFICATION_REPORT.json
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/adversarial/verify_global_transfer_adversarial.py --check-manifest --no-write-report
.venv/bin/python -O cut_recovery/strong_crossbridge/global_transfer/adversarial/verify_global_transfer_adversarial.py --check-manifest --no-write-report
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/adversarial/test_global_transfer_adversarial_mutations.py
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/verify_release.py
.venv/bin/python -O cut_recovery/strong_crossbridge/global_transfer/verify_release.py --report cut_recovery/strong_crossbridge/global_transfer/RELEASE_OPTIMIZED_VERIFICATION_REPORT.json
.venv/bin/python cut_recovery/strong_crossbridge/global_transfer/build_manifest.py
cd cut_recovery/strong_crossbridge/global_transfer
shasum -a 256 -c MANIFEST.sha256
```

The independent verifier does not import the producer. It reconstructs all
204 topology directions, rechecks the proof dependency DAG, verifies split
incompatibility, replays the `Z₂ × Z₂` character/convolution identities and
all zero-, one-, and two-reticulation switching-weight sums, crosswalks the
local universe entrywise, and binds the local independent verification and
all 34 of its rejected mutations.
