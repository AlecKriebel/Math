# Exact directional topology theorem on the principal K2P domain

## 1. Claim and parameter convention

Let `N1,N2` be binary semi-directed networks on the same labelled leaves.
All inheritance probabilities are in `(0,1)`, and every K2P edge has Fourier
vector `(1,s,g,s)` in

\[
\mathcal D_+=\{0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

If some four-leaf marginal of `N1` and `N2` has a different set of displayed
quartet trees, then their complete physical K2P images are disjoint.  This is
pointwise disjointness, not merely generic distinction, and therefore rules
out containment in both directions.

The character names in Englander et al. use the equal K2P pair `G,T`; this
project uses the equal pair `C,T`.  A Klein-four-group automorphism carries
one convention to the other.  The proof below is invariant under that
renaming.  The cited paper assumes every nontrivial Fourier edge parameter is
in `(0,1)`; `D_plus` is a subset of that domain.

## 2. Quartet inequalities

Write the three quartet splits as `12|34`, `13|24`, and `14|23`.  After a
permutation of characters and leaves, the linear Fourier expression

\[
I_{12}=q_{GGGG}-q_{GGTT}
\]

is zero on the K2P tree with split `12|34` and strictly positive on either
other split.  Indeed, the pendant factors agree because the repeated K2P
characters have the same eigenvalue, while on a crossing split the difference
has the form

\[
(\hbox{positive pendant monomial})(1-a),
\]

where the relevant effective internal eigenvalue satisfies `0<a<1`.

Likewise

\[
J_{13}=q_{GGGG}-q_{GGTT}-q_{GTTG}+q_{GTGT}
\]

is zero on the `12|34` and `14|23` trees and strictly positive on the
`13|24` tree.  Leaf permutations give `I_t` and `J_t` for every split `t`.

A strict network distribution is a convex mixture of its switching-tree
distributions.  Every switching weight is positive because every inheritance
probability is strictly between zero and one.  Consequently:

- if one displayed set is the singleton `{t}` and the other contains a
  different tree, `I_t` is zero on the first image and positive on the second;
- if neither set is a singleton, choose `t` in one set but not the other;
  `J_t` is positive on the image containing `t` and zero on the other.

These cases exhaust the seven nonempty subsets of the three quartet trees.
Thus unequal displayed sets give disjoint physical images.

Marginalization is linear.  If two full distributions were equal, all their
four-leaf marginals would be equal.  Disjoint quartet marginal images
therefore imply disjoint full images.

This is Proposition 2.9, Proposition 2.10, and Theorem 2.11 of Englander et
al., *Identifiability of Phylogenetic Level-2 Networks under the Jukes-Cantor
Model*, bioRxiv 2025.04.18.649493, version posted 2026-07-04.  The locally
reviewed PDF has SHA-256
`3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5`.

## 3. Binding to the graph compiler

The compiler's `quartet_splits` operation has exactly the displayed-set
meaning used above:

1. choose one incoming edge at every reticulation;
2. delete every other incoming reticulation edge;
3. restrict the resulting switching tree to the selected four labels;
4. prune unlabelled dead ends and suppress unlabelled degree-two vertices;
5. record its unique balanced split.

An independent implementation replays all six source supports and all 2,814
four-port target completions.  It agrees with the compiler on all 2,820
displayed sets, produces no star record, and verifies that deleting target
dummy leaves before or during switching gives the same displayed set in all
2,814 cases.  Relabelling transports these base checks to all 24 port
permutations.

The same theorem therefore validates the 360,408 raw `quartet` exclusions in
the 405,216-row raw ledger and the 35,758 first-child
`displayed_quartet_mismatch` certificates in the restoration forest.  These
are exact directional noncontainment certificates, not topology heuristics.

## 4. Tree--sunlet rows

The remaining topology exclusions use a different pointwise sign theorem.
For a three-leaf marginal put

\[
X_h=q_{hh0},\quad Y_h=q_{h0h},\quad Z_h=q_{0hh},\quad V=q_{CTG}.
\]

Every K2P tree has

\[
\mathcal T_3=V^2X_g-X_s^2Y_gZ_g=0.
\]

For a three-sunlet, after the appropriate leaf permutation, its exact
pullback is

\[
-a_s^2b_s^2a_gb_gc_g^2f_s^2\,
 \delta(1-\delta)d_ge_g(1-f_g)^2<0.
\]

Every factor is strict on `D_plus`.  Tree and sunlet physical images are
therefore disjoint in both directions.  This validates the 16,974 raw
`tree_sunlet` exclusions and the 646 restoration children carrying that
certificate.  The archived exact factor replay is independently rerunnable.

Together the displayed-set and tree--sunlet theorems validate all 377,382 raw
topology exclusions and all 36,404 topology-terminal restoration children.

## 5. Strongest valid bridge-tree consequence

Different trees of blobs force a four-leaf restriction with different
displayed quartet sets.  Hence the theorem above gives

\[
\operatorname{TreeOfBlobs}(N_1)\ne
\operatorname{TreeOfBlobs}(N_2)
\quad\Longrightarrow\quad
\mathcal M_{K2P}(N_1)\cap\mathcal M_{K2P}(N_2)=\varnothing.
\]

Therefore any nonempty directed containment on `D_plus` forces equality of
the labelled reduced trees of blobs.  This is the correct K2P bridge-tree
recovery route.  It is stronger than generic cut recovery and avoids an
invalid reuse of the JC pointwise flattening-rank dichotomy.

Generic cut minors alone give only the following safe statement: a target cut
must also be a source cut under source-to-target containment.  They do not
rule out a source cut mapping into an exceptional cut-like locus of a target
noncut model.  Strict K2P tree--theta collisions outside the strong class show
that this logical issue is real.  Thus the final theorem should cite the
displayed-quartet disjointness theorem (and its exact compiler binding), not
silently transplant the JC endpoint proof.

After the tree of blobs is recovered, the strict tree--sunlet sign separates
an ordinary trivalent component from a three-sunlet.  Strong level-2 theta
components have at least four boundary incidences, so this supplies the
ordinary/nontrivial decoration used before projective bridge localization.

