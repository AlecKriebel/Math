# Additional period-deletion interface check

This note follows the initial independent derivation and the source reads; it is not relabeled as a pre-source derivation. The candidate membership proof already needs only least action and f-pi, so it does not depend on an unsupported period-deletion assertion.

For completeness, let pi be a positive period and delete the first pi_v occurrences of each v from any legal word (or every occurrence when fewer exist). At a surviving occurrence of v, the deleted prefix count gamma has gamma_v=pi_v and 0<=gamma_u<=pi_u. Under the candidate column-Laplacian convention, (Delta gamma)_v=d_v pi_v-sum_{u->v}gamma_u>=d_v pi_v-sum_{u->v}pi_u=0. The new prefix state is the old one plus Delta gamma, so the surviving firing remains legal. If the original word dominates pi, its deleted vector is exactly pi and the final state is unchanged. The sign and kernel orientation are explicit.

The additional fresh controls replay 50 actually generated legal words on five/six-vertex graphs after this deletion, testing legality at each of 8,397 surviving firings and final-state equality when a complete period was removed. This is finite evidence and not a replacement for the proof above.
