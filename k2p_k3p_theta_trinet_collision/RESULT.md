# Exact K2P and K3P tree--theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial
3-blob shares an exact three-leaf distribution with a three-star tree under
K2P. Since K2P is a K3P submodel, this collision alone answers both high-level
Kimura trinet-disjointness questions in arXiv:2607.12919v3 negatively.

## K2P

The compact witness lies over `Q(sqrt(71))`, has equal inheritance weights,
strictly positive transition probabilities, and exact minimum site-pattern
probability `1188799 / 79626240`. It is a counterexample to Lemma 5.6 and the
K2P branch of Corollary 5.8 in arXiv:2607.12919v2. A separate edgewise strictly
continuous-time witness is checked independently by direct Markov pruning.

The fixed K2P theta map has full rank 9 at both witnesses. Near the simple
collision, the collision locus is smooth of dimension 17 and codimension 3,
fibers submersively over nearby tree distributions, and has 11-dimensional
fixed-output network fibers. Its complexified image is Zariski dense in the
effective affine K2P three-leaf Fourier space.

## K3P

The exact quartic theta parameter lies over `Q(5^(-1/4))`, has strictly
positive transition probabilities, and lies outside every character-relabeled
K2P parameter specialization. Its shared comparison-tree distribution is
openly identified as relabeled K2P. The fixed theta map has rank 15, its local
collision locus has dimension 23 and codimension 6, and its fixed-output fibers
have dimension 14. Removing the three relabeled-K2P tree strata gives a
relatively open dense set of nearby genuinely K3P shared distributions. The
same conclusion holds in the edgewise strictly continuous-time rate cone.
The complexified theta image is Zariski dense in the effective affine K3P
three-leaf Fourier space.

## All leaf counts

For every labelled unrooted binary tree topology on `n >= 3` leaves and every
chosen internal vertex, strict-interior K2P and K3P parameters give an exact
collision with the network obtained by replacing that vertex by one theta
3-blob. Edgewise strictly continuous-time and genuinely K3P variants also
exist. This is a one-blob common-subtree theorem, not a multi-blob
composability claim.

## Replay

Run the current clarification package:

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_displayed_trees.py
python3 src/verify_k2p_four_leaf_graft.py
python3 verify.py
```

Successful output ends with `ALL DISPLAYED-TREE CHECKS PASSED`,
`ALL FOUR-LEAF GRAFT CHECKS PASSED`, and `ALL EXACT CHECKS PASSED`,
respectively.
