# Fixed-full hard-cover theorem

Status: **PROVED; schema-3 n3/n4 forests and their relation bindings are
independently verified**

## Statement

Let `H` and `H'` be fixed labelled standard-strong local factors on the same
finite boundary set `X`, and suppose a source-relative full-dimensional
regular germ of the projective JC model of `H` is contained in that of `H'`.
Fix admissible rooted presentations of both factors.  Let `Q` be a labelled
core-retaining rigid support of `H` containing its rooted incoming boundary.

If the restriction of `H'` to `Q` does not retain its primitive core, choose:

1. every omitted reticulation-sink boundary of `H'`;
2. one actual boundary on every still-empty segment of one minimum strong
   repair of `H'`; and
3. the rooted incoming boundary of `H'` when it is not in `Q`.

Call the resulting ordered set of distinct physical boundary labels `D`.
Then `D` is contained in `X \ Q`, every label of `D` is an ordinary segment
port in `H`, and the fixed relation determines one path in the sequential
dummy-restoration tree.  For every prefix `D_j` of `D`, the original full
containment descends directly to a source-relative containment

```text
H | (Q union D_j)  <=_JC  H' | (Q union D_j).
```

Consequently, if every graph-derived restoration path is either strictly
separated at one prefix or terminates in labelled isomorphism modulo ordinary
triangle redirection `T`, then the fixed full relation is separated or admits
a common core-retaining rigid support modulo `T`.

This theorem does **not** assert that containment of the selected marginal on
`Q` lifts to any restored marginal.

## Proof

The full factors have the same labelled boundary set because the labelled
bridge tree has already been recovered.  A full standard-strong target factor
contains every reticulation-sink child and occupies every segment required by
at least one minimum strong repair.  Hence the three listed role families can
be filled by distinct actual labels of `X \ Q`.  They are precisely the
completion grammar's `D_SINK`, `D_REPAIR`, and marginalized `INCOMING` roles.

The source support `Q` is core-retaining, so it already contains every source
reticulation-sink boundary and one complete source repair.  Any label outside
`Q` is therefore an ordinary boundary attached at a subdivision vertex of a
directed source segment.  Its segment and its order relative to the labels of
`Q` and the earlier labels of `D` are fixed by the full source graph.  Inserting
the next label in every segment position therefore enumerates the actual
prefix.  A deterministic order on `D` loses no relation: it merely names the
same finite set of labels in that order.

Let `U` be the source-open germ contained in the target model.  Marginalizing
the distributions in `U` to `Q union D_j` gives containment of the indicated
prefix models.  This is a direct image of the **original full relation**, not
an inference from the preceding prefix.  On the source side, suppressed edge
classes map to effective JC multipliers by

```text
y_C = product_{e in C} x_e.
```

The classes are disjoint, and the differential row for `C` has strictly
positive entries on `(0,1)^E`; thus each prefix restriction is a submersion
onto its effective source parameter cube.  It follows that the descended
containment is source-relative full-dimensional on a nonempty regular open
subgerm.  No continuous target parameter selection is used.

If a prefix has an invariant vanishing identically on the target but with
nonzero source pullback, its common source locus is contained in a proper
source algebraic set, contradicting the descended source-open containment.
If an invariant vanishes identically on the source and has a strictly signed
target pullback on the target open cube, the two prefix interiors are
disjoint, again a contradiction.  Therefore the actual path cannot meet a
certified separating state.  Under the stated finite hard-cover hypothesis it
terminates in a labelled `T`-quotient equality, giving a common rigid support
modulo ordinary triangle redirection.

## Artifact requirements

The promotion certificate must distinguish canonical algebra from relation
paths.  Every emitted path record must contain:

- `restoration_root_id`, identifying the fixed selected source-target
  presentation and full port matching;
- `parent_path_id`;
- the deterministic `dummy_order`;
- the complete restored role-to-physical-label map;
- the source prefix word tuple;
- a `canonical_state_id` pointing to regenerated graph-derived algebra; and
- a terminal classification.

Canonical states may be deduplicated, but path records may not be replaced by
an unbound list of state identifiers.  Additional ordinary ports after the
target core has been restored are handled by the independently audited
support-plus-one/two probe-coherence theorem.

## Exact status

- **VERIFIED:** fixed-full restoration exhaustiveness, role completeness,
  source segment placement, prefix submersion, and both separator directions.
- **FALSE:** unconditional lifting from selected marginal containment.
- **FALSE AS A RELATION CERTIFICATE:** the schema-2 `40,072`-state discovery
  census keyed states only by semi-directed mixed codes.  Distinct rooted
  presentations could merge while retaining only the first graph witness and
  child set.  The corresponding theta-2 n=4 run was rejected by exact replay.
- **EXACTLY COMPUTED:** the fixed root inventories contain `5,344` n=3 roots
  and `132` filtered theta-2 n=4 roots.
- **VERIFIED:** schema-3 regeneration binds every state to its fixed root and
  exact rooted graph pair.  Independent normalized comparisons and mutation
  audits cover all `5,344` n3 and `132` theta-2 n4 roots.  The separate
  signature gates prove that these are exactly the nonretaining relations
  surviving the necessary algebraic filter.  Common-anchor probe streams
  promote every terminal to arbitrary subdivisions.
