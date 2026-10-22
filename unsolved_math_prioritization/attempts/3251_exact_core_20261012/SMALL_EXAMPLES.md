# Small explicit examples

These hand-sized examples are mathematical illustrations. They are not a redistributed exhaustive dataset.

## The k equals three family

Let A={0,1}, P={2,3}, L={4,5}, M={6,7} and (u,b,c,d,e)=(8,9,10,11,12). Join two vertices exactly when they belong to one of these eight triples:

{0,1,8}, {0,1,9}, {0,1,10}, {2,3,8}, {2,3,11}, {2,3,12}, {4,5,9}, {6,7,9}.

The 13-vertex graph has 20 edges and exactly these eight maximum cliques. Its core is X={0,1,2,3,9}, inducing K3 on {0,1,9} disjoint K2 on {2,3}. A perfect elimination order is (4,5,6,7,11,12,10,2,3,9,8,0,1).

Prescribe A color 0 and P+b color 1. This is a division of G[X], but {0,1,8} forces u=1 and {2,3,8} forces u=0. The color complement also fails. Among 32 core colorings, 24 divide the core, 22 extend and two do not. The full graph has 1,458 labelled divisions. An explicit full division is (0,1,0,1,0,1,0,1,0,0,0,0,0), in vertex order 0 through 12.

The two conflicting cliques form a signed X-tree: the only outside-X vertex is u, contained in both nodes; the prescribed A and P are monochromatic on opposite bipartition sides. The core maximum-clique constraint alone misses this tree constraint.

## A three-node abstract tree

Take rank-three sets Q0={0,1,4}, Q1={4,5,2}, Q2={5,3,6}, and prescribed set P={0,1,2,3,6}. The free vertices 4 and 5 each occur in two sets, giving the path Q0,Q1,Q2. Prescribe (alpha(0),alpha(1),alpha(2),alpha(3),alpha(6))=(0,0,1,0,0). The leaves force vertices 4 and 5 both to 1, making Q1 monochromatic. This is a matching signed tree with labels (0,1,0).

Flipping alpha(0) to 1 repairs this example: the full coloring (1,0,1,0,0,1,0) satisfies all three sets. This is an abstract set-family example and is not asserted to be an exact graph maximum-clique family. Same-side leaves here have the same color; the general theorem does not require their prescribed boundary cliques to be disjoint.

## Necessary-bound arithmetic

At k=4, 3k-4=8. The alternative r=k-1 would give 3k-3=9, but the external four-color theorem excludes r=3 altogether for an odd-hole-free indivisible k=4 graph. Thus the core must contain a K4 and have at least eight vertices. This does not construct an indivisible graph. At k=5 the two arithmetic bounds are 11 and 12; no sharpness or existence claim is made.
