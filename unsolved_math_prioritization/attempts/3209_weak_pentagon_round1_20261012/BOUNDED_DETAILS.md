# Additional bounded counts and explicit examples

These figures preserve useful exact outcomes of the accepted first-round audits. They corroborate the symbolic proofs and do not extend the finite catalog range or settle either universal target. They are not raw input records or a redistributed certificate stream.

## Clebsch walks

The independent theory audit used the even-subset model of the Clebsch graph: a vertex is an even-cardinality subset of {1,2,3,4,5}, encoded here by its five-bit mask; adjacency means symmetric difference has size four. These masks are not the four-bit Cayley labels used in the fixed-cut proof. There are 16 vertices in either model.

For each length, the audit computed the entire integer walk matrix. The number of reachable ordered endpoint pairs, the smallest positive entry and the sum of all entries are:

| Length | Reachable ordered pairs | Smallest positive walk count | Total walks |
| ---: | ---: | ---: | ---: |
| 1 | 80 | 1 | 80 |
| 2 | 176 | 2 | 400 |
| 3 | 240 | 6 | 2,000 |
| 4 | 256 | 24 | 10,000 |
| 5 | 256 | 120 | 50,000 |
| 6 | 256 | 840 | 250,000 |
| 7 | 256 | 4,200 | 1,250,000 |

An explicit pentagon in this even-subset model has cyclic vertex sequence (0,15,17,6,27). For each even cycle of length 4 through 12, alternating 0 and 15 gives a witness. For each odd cycle of length 5 through 11, take the displayed pentagon and insert the required number of initial two-edge returns 0,15,0. This gives exactly the accepted examples at those lengths. A triangle is impossible by the unique generator relation.

The ten two-element subsets, encoded by (3,5,6,9,10,12,17,18,20,24), give the standard Petersen embedding: two such subsets are adjacent precisely when disjoint. The audit checked this graph's 12 pentagons and edge coverage; it did not claim to audit the whole earlier screen.

For the restored square, take the cycle v0-v1-v2-v3-v0, four edges vi-ti, and the exterior edges t0-t1 and t2-t3. List the square vertices first in cyclic order, then terminals t0,t1,t2,t3. The even-subset sequence (0,15,0,15,15,0,15,0) gives an unrestricted homomorphism. By contrast, the prescribed terminal sequence (0,30,30,0) cannot extend although both proposed reconnection edges have valid images. This is a boundary obstruction only. Of 4,096 normalized square boundaries, 961 fail; among the 400 boundaries satisfying both reconnection edges, 45 fail.

## Empty cross relations and extension counts

For each k, the audit enumerated every k-element subset A of the Clebsch vertex set and found the largest possible cardinality of a set B having no edge to A. A and B may overlap. For k from 0 through 16, the respective maxima are

(16,11,8,6,5,5,3,2,2,1,1,1,0,0,0,0,0).

This contains the supplemental fact that a six-set has open-neighborhood union of size at least 13. Among the 8,008 six-sets, the union sizes 13,14,15,16 occur 160,1,800,3,312,2,736 times, respectively. The symbolic proof of the six-by-six cross-edge lemma uses only the weaker bound needed there.

The claw extension passed all 256 normalized terminal triples. The double claw passed all 4,096 normalized quadruples. Its seven cross-matching patterns comprise the empty matching (4,096 cases), four individual cross edges (16 normalized boundary cases each), and two perfect cross matchings (one boundary-free case each), for 4,162 cross-pattern cases in total. The full ordered single-vertex boundary criterion passed all 4,096 triples, including repeated images.

For C5, all 3,125 edge-color assignments were checked: 120 are original weak-pentagon witnesses and none changes under the deterministic normalization. For C7, all 78,125 assignments were checked: 16,800 are valid and 14,616 change under that normalization. All preserve singleton colors on the odd cycle and acquire explicit exact-cut complements. This samples one deterministic bipartition choice per witness; the proof, rather than the test, establishes every allowed choice. The density arithmetic was checked on 28,840 bounded integer cases and also proved symbolically.

## Cut histogram of the authored 14-vertex graph

Independent direct summation checked all 8,192 normalized cuts, fixing vertex 0 outside the selected side. The numbers of cuts at each attained size are:

| Cut size | Number |
| ---: | ---: |
| 0 | 1 |
| 3 | 14 |
| 4 | 22 |
| 5 | 56 |
| 6 | 218 |
| 7 | 462 |
| 8 | 764 |
| 9 | 1,176 |
| 10 | 1,438 |
| 11 | 1,354 |
| 12 | 1,106 |
| 13 | 792 |
| 14 | 454 |
| 15 | 218 |
| 16 | 91 |
| 17 | 24 |
| 18 | 2 |

Unlisted sizes occur zero times. The two size-18 cuts are exactly masks 2650 and 7794, whose witnesses are displayed in the full proof. The nonextendible local cut has mask 10698 and size 15. The independent symmetry reconstruction examined 384 initial pentagon assignments and 1,536 candidate value pairs at the next two constrained vertices; none completes the local-cut assignment. The original separate search took 522 calls, but the hand contradiction is the negative certificate and no timeout inference is used.
