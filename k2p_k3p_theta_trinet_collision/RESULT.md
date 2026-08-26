# Exact K2P and K3P tree-theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial 3-blob shares an exact three-leaf distribution with a three-star tree under both K2P and K3P.

## K2P

The simple K2P witness lies over `Q(sqrt(71))`, has equal inheritance weights, strictly positive transition probabilities, and exact minimum site-pattern probability `1188799 / 79626240`. It is a counterexample to Lemma 5.6 and the K2P branch of Corollary 5.8 in arXiv:2607.12919v2. Version 3 removes those statements and leaves the high-level K2P question open; this collision answers it negatively. A separate edgewise strictly continuous-time witness is checked independently by direct Markov pruning.

The fixed K2P theta map has full rank 9 at both witnesses. Near the simple collision, the collision locus is smooth of dimension 17 and codimension 3. An eight-parameter symmetric ansatz contains an exact local six-dimensional collision family.

## K3P

The K3P witness lies over `Q(5^(-1/4))`, has strictly positive transition probabilities, and gives a negative answer to the high-level K3P trinet question posed in arXiv:2607.12919v3. The fixed theta map has rank 15, its local collision locus has dimension 23 and codimension 6, and a real-analytic implicit-function argument moves the collision into the edgewise strictly continuous-time K3P rate cone. Edgewise embeddability does not assert a common generator or clock.

## Replay

Run the current clarification package:

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_displayed_trees.py
python3 verify.py
```

Successful output ends with `ALL DISPLAYED-TREE CHECKS PASSED` and `ALL EXACT CHECKS PASSED`, respectively.
