# Exact closure theorem for the primitive theta2 five-port gate

## Claim

On the principal positive K2P domain

\[
\mathcal D_+=\{0<s<1,\ 0<g<1,\ g>2s-1\},
\]

every directed presentation from one of the four minimum-repaired primitive
five-port `theta2` source supports into the primitive target-completion
grammar is one of the following:

1. pointwise disjoint by a displayed-quartet or tree--sunlet sign;
2. generically noncontained because the exact target rank is smaller than the
   exact source rank;
3. generically noncontained by an explicit target invariant with nonzero
   source pullback; or
4. an exact labelled semi-directed isomorphism.

For an isomorphic selected presentation with one or two target dummy roles,
every physical fixed-full restoration path to six or seven ports is likewise
pointwise separated or exactly isomorphic.  Thus the dummy presentations are
restoration roots, not silently accepted selected terminals.

This is a local primitive gate.  It does not alone prove the global strongly
tree-child level-2 theorem.

## Primitive universe and raw partition

The graph grammar produces four `theta2` source repairs, 1,983
selected-incoming target completions, 4,155 marginalized-incoming target
completions, and 120 port permutations.  Hence

\[
4(1983+4155)120=2,946,240
\]

raw directed presentations.  Independently recomputing every switching-tree
displayed set and every three-leaf type gives, for each source repair,

| category | raw presentations |
|---|---:|
| displayed-quartet mismatch | 735,648 |
| tree--sunlet strict sign | 632 |
| topology survivors | 280 |

The 280 survivors form 120 exact polynomial-map descriptor classes.  Their
rank histogram is `14:8, 16:80, 18:32`.  Every source has exact rank 18.  Per
source, the 120 classes and 280 raw survivors partition as

| proof | classes | raw presentations |
|---|---:|---:|
| target rank below 18 | 88 | 200 |
| exact quadratic separator | 24 | 60 |
| exact labelled isomorphism | 8 | 20 |

There is no unresolved class.

## Directional topology proof

For unequal displayed-quartet sets, the ledger records the first mismatching
four-set, both displayed sets, and the appropriate `I_singleton` or
`J_membership` Fourier invariant.  Propositions 2.9--2.10 and Theorem 2.11 of
Englander et al., version 4, prove zero-versus-strict-positive separation for
strict positive K2P mixtures.  The reviewed PDF has SHA-256
`3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5`.
Because marginalization preserves equality, a four-leaf pointwise separator
rules out containment in either direction, even when source and target have
different dimensions.

For a tree--sunlet three-leaf marginal, put

\[
\mathcal T_3=V^2X_g-X_s^2Y_gZ_g.
\]

It vanishes on every K2P tree.  On the relevant sunlet its pullback is

\[
-a_s^2b_s^2a_gb_gc_g^2f_s^2\delta(1-\delta)d_ge_g(1-f_g)^2<0.
\]

Every factor is strict on `D_plus`.  The verifier independently expands the
underlying symbolic identity.

## Exact rank proof

For each regenerated descriptor the lower certificate is a nonzero rational
Jacobian minor at the deterministic strict rational point.  The upper
certificate is not a sampled rank.  With edge-sector variables `x_i` and
inheritance variables `l_j`, use

\[
V(x_i)=x_iA_i(l),\qquad
V(l_j)=l_j(1-l_j)C_j(l_0,\ldots,\widehat{l_j},\ldots).
\]

The `A_i` and `C_j` are multilinear.  Expanding `J_f V=0`
coefficientwise gives an integer matrix `A`.  If `E` evaluates these fields at
an interior rational point, then

\[
\dim E(\ker A)=\operatorname{rank}\binom{A}{E}-\operatorname{rank}(A).
\]

The exact integer ranks certify enough independent generic fibre fields to
match every lower minor.  Upper equals lower for all 120 descriptors, with no
exception orbit.  Since a rank-18 source variety cannot be generically
contained in a rank-14 or rank-16 target variety, all 88 rank exclusions per
source are directional certificates.

## Quadratic and isomorphism terminals

Each of the 96 source-indexed quadratic certificates records a
multihomogeneous polynomial in observable Fourier coordinates.  Exact sparse
substitution gives zero on the target map and a stored nonzero source
pullback.  Therefore the generic source image is not contained in the target.

The corrected graph relation is applied to
`selected_graph_from_completion(record)`, not to the completion graph with
dummy leaves.  This distinction is load-bearing.  Each of the 32 canonical
isomorphism classes stores the explicit mixed-vertex bijection induced by a
full labelled semi-directed incidence-graph isomorphism.  Auxiliary
incidence-edge indices are deliberately omitted because they depend on graph
insertion order.  The associated class rows expose all 80 raw transports.

## Fixed-full restoration of dummy anchors

Among the 80 raw isomorphism transports, 24 have no dummy, 40 have one dummy,
and 16 have two.  A dummy-bearing selected isomorphism is not declared a full
terminal.

Fix an actual full source-to-target relation first.  Retain one actual omitted
label on both sides and marginalize that same relation.  The paired `(s,g)`
serial-product section makes the source restriction map physically open.
Thus the actual child is one of the graph-enumerated source subdivisions and
target dummy promotions.  No abstract selected relation is lifted and no
target marginal openness is used.

There are eight first source insertion segments.  The 72 role requests yield
576 six-port children:

| remaining dummy roles | quartet-separated | isomorphic |
|---:|---:|---:|
| 0 | 280 | 40 |
| 1 | 224 | 32 |

The 32 isomorphic rows with one role remaining are continuation nodes.  A
first subdivision creates nine possible second insertion segments.  Their
288 seven-port children comprise 256 quartet separations and 32 exact full
isomorphisms.  Consequently every fixed-full path either contradicts the
assumed containment by a pointwise marginal separator or reaches the same
labelled semi-directed network.  There are zero unresolved paths.

The artifact retains all 864 path rows, 72 final physical isomorphism maps,
all raw transports, and exact canonical relation classes.  It binds the
paired marginal proof and replayer by SHA-256.

## Replay and falsification

The default verifier regenerates the complete primitive universe.  The frozen
rank and restoration artifacts retain their exact legacy compiler/canonicalizer
provenance.  Replay first requires those legacy values, then reconstructs the
current rank and restoration gzip bytes by replacing only the provenance
fields.  It correspondingly updates only the summary provenance, the two
derived artifact metadata records, and the summary payload seal.  Those three
reconstructed outputs and every other unchanged artifact are compared
byte-for-byte with the fresh run.  The quick verifier checks the contiguous raw-ID
census, hashes, rank/class bindings, topology witness semantics, anchor and
restoration grammar, all continuation parents, and every certificate
reference.  The mutation suite also rejects wrong legacy compiler or
canonicalizer bindings, as well as omissions, duplications, false
rank exclusions, class reassignments, topology or polynomial corruption,
isomorphism-map corruption, restoration-role drift, missing roots/children,
and optimized Python mode.
