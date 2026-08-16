# Milestone 3B: the JC root-collapsed Psi move and its exact lifting obstruction

## Scope and convention

This note classifies the four-model orbit found in the root-spanning,
four-leaf theta census.  It uses the semi-directed convention from Milestone
3A: suppress only the degree-two artifact created by the global root, forget
tree-edge directions, and retain arrowheads entering reticulations.

The four root models are

| name | census index | leaf labels in port order |
|---|---:|---|
| `A` | 18 | `(1,2,3,4)` |
| `A_reflected` | 18 | `(3,2,1,4)` |
| `B` | 19 | `(2,1,3,4)` |
| `B_reflected` | 19 | `(2,3,1,4)` |

For the nonroot audit, change the old root `S` into a tree vertex, add a new
root `RHO`, add a new leaf `LIN` labelled `5`, and add arcs

```text
RHO -> S,   RHO -> LIN.
```

This exposes the incoming state port by a positive outgroup edge.  Marginalizing
leaf `5` recovers the original four-leaf model.

## Primary theorem

**PROVED.** Under JC, the four root models are pairwise distinct
semi-directed topologies and possess one common seven-dimensional regular
relatively open stochastic region.  Call the resulting root-adjacent move
`Psi`.

**PROVED.** After restoring the incoming port, the `Psi` orbit splits exactly
as

\[
\{A,B_{\rm reflected}\}
\quad\sqcup\quad
\{A_{\rm reflected},B\}.
\]

Within each two-element class, the two networks:

1. are related by ordinary redirection of the triangle `S-U-V`;
2. have equal ten-dimensional irreducible JC model closures;
3. possess a common ten-dimensional regular relatively open stochastic
   region.

Between the two classes, the complete open stochastic images are disjoint:
an ordered-quartet invariant is zero on every point of the first class and
strictly positive on every point of the second.

Consequently, `Psi` is a genuine extra semi-directed ambiguity only where the
global-root suppression destroys the triangle that supports it.  Its only
surviving nonroot lift in this four-model orbit is the already permitted
triangle-redirection move `T`.  It therefore supplies no independently
stackable non-triangle bit.

## The four topologies at the root

The two unlabelled directed cores have arcs

```text
A (census 18):
U->V, S->U, S->V, U->P3, P3->X,
V->P40, P40->P41, P41->X,
P3->L0, P40->L1, P41->L2, X->L3.

B (census 19):
U->V, S->U, S->V, U->P30, P30->P31, P31->X,
V->P4, P4->X,
P30->L0, P31->L1, P4->L2, X->L3.
```

Vertices `V,X` are reticulations.  The complete encodings and port labels are
in `certificates/jc_psi_lifting_certificate.json` and are regenerated from
the exact census.

**EXACTLY COMPUTED.** After suppressing `S`, all four root models have no
three-vertex triangle, and exhaustive colour-preserving graph isomorphism
finds four rooted and four semi-directed isomorphism classes.

**EXACTLY COMPUTED.** On the explicit seven-variable source box

\[
0<u,x,z,p,q,r<1,\qquad 1/32<y<5/32,
\]

the following maps preserve all 64 zero-sum four-leaf Fourier coordinates:

\[
\begin{array}{c|ccccccc}
 &u&x&y&z&p&q&r\\ \hline
A_{\rm reflected}&8y-1/4&z&(4u+1)/32&x&r&q&p\\
B&(8y-1/4)&(4u+1)/32&x&z&q&p&r\\
B_{\rm reflected}&u&y&z&x&q&r&p.
\end{array}
\]

The complete symbolic identity and rank-seven certificates are replayed by
`src/verify_jc_psi_move.py`.

**PROVED.** The gauge determinant is nonzero throughout that source box, and
the full symbolic Jacobian rank of each unlabelled parameterization is seven.
The inverse-function theorem therefore gives a common regular relative open
region, rather than an isolated coincidence.

## What changes when the incoming port is restored

**EXACTLY COMPUTED.** Every augmented network is binary, strongly tree-child,
and level 2.  Its unique nontrivial blob contains the two reticulations and
has simple-cycle lengths

\[
3,6,7.
\]

The sole triangle is `S-U-V`; every other cycle has length at least four.

**EXACTLY COMPUTED.** For each of the pairs

\[
(A,B_{\rm reflected}),\qquad(A_{\rm reflected},B),
\]

there is exactly one leaf-colour-preserving isomorphism of the underlying
root-suppressed undirected graph.  It swaps `U` and `V`, preserves the
directions entering `X`, and sends the source triangle reticulation `V` to the
target tree vertex `U`.  The target triangle reticulation remains `V`.

**PROVED.** This is precisely triangle redirection: the underlying labelled
graph and every reticulation arrowhead outside `S-U-V` agree, while only the
reticulation designation inside that triangle changes.

This graph check is the key correction to the initial discovery impression.
The same pair is non-triangle-equivalent at the global root because
suppressing `S` removes the three-vertex triangle; below the root, it is an
ordinary `T` move.

## Exact ten-dimensional tensor correspondence

Number source edges of `A` by

```text
0 U->V          1 S->U          2 S->V          3 U->P3
4 P3->X         5 V->P40        6 P40->P41      7 P41->X
8 P3->L1        9 P40->L2      10 P41->L3     11 X->L4
12 RHO->S      13 RHO->L5.
```

Number target edges of `B_reflected` in its census order:

```text
0 U->V          1 S->U          2 S->V          3 U->P30
4 P30->P31      5 P31->X        6 V->P4         7 P4->X
8 P30->L2       9 P31->L3      10 P4->L1       11 X->L4
12 RHO->S      13 RHO->L5.
```

Write the source multipliers as `a_i`, the target multipliers as `b_i`, and
put

\[
d=a_0a_1+a_2.
\]

Fix the source and target inheritance probabilities to `1/2`, and fix
`a_5=b_6=1/2`.  Define

\[
\begin{aligned}
b_0&=\frac{4a_0a_1a_3}{d}, & b_1&=a_1,
&b_2&=\frac{4a_1a_2a_3}{d}, & b_3&=\frac d{4a_1},\\
b_4&=a_6, &b_5&=a_7, &b_7&=a_4,\\
(b_8,b_9,b_{10},b_{11})&=(a_9,a_{10},a_8,a_{11}),\\
(b_{12},b_{13})&=(a_{12},a_{13}).
\end{aligned}
\]

**EXACTLY COMPUTED.** Direct displayed-tree contraction and rational-function
simplification prove equality of all 256 zero-sum five-leaf Fourier
coordinates under this map.  Applying the same leaf permutation `(1 3)` to
both sides proves the identical correspondence for
`A_reflected` versus `B`.

**PROVED.** The correspondence is stochastic on a nonempty explicit box.  It
suffices to take

\[
89/100<a_0<91/100,
\qquad
99/200<a_i<101/200\quad(i=1,2,3),
\]

with every other free multiplier in `(0,1)`.  Positivity is immediate.  The
endpoint bounds

\[
4a_0a_1a_3<d,qquad
4a_1a_2a_3<d,qquad
d<4a_1
\]

hold throughout this box and imply `b_0,b_2,b_3<1`; every other target
multiplier is copied from the source or equals `1/2`.

## Dimension, regularity, and openness

Use the ten source columns

```text
0,1,2,3,4,6,7,8,9,10
```

and the ten target columns

```text
0,1,2,3,4,5,7,8,9,10.
```

Fix every omitted multiplier and both inheritance probabilities to `1/2`.
For the ten output rows `0,1,2,3,4,5,6,7,14,15`, counted after the constant
five-leaf JC orbit coordinate, the common source-gauge determinant is

\[
-\frac{
a_0a_1^2a_{10}^3a_3^3a_4^3a_6^2a_7a_8a_9^3
(a_1-1)^2(a_6-1)^2(a_0a_1+a_2)^2
}{2^{32}}.
\]

**EXACTLY COMPUTED.** This determinant is nonzero throughout the stated
source box.  Exact polynomial-matrix reduction gives generic rank ten for
both complete sixteen-parameter augmented models.

At the rational source point

```text
(a0,...,a13; lambdaV,lambdaX)
=(9/10,1/2,1/2,1/2,2/5,1/2,1/10,1/3,
  3/5,2/3,3/4,1/2,1/2,1/2; 1/2,1/2)
```

the corresponding target is

```text
(b0,...,b13; muV,muX)
=(18/19,1/2,10/19,19/40,1/10,1/3,1/2,2/5,
  2/3,3/4,3/5,1/2,1/2,1/2; 1/2,1/2).
```

**EXACTLY COMPUTED.** All parameters are strictly interior, all 256 Fourier
coordinates agree, and the selected source and target rank-ten minors are

\[
-\frac{263169}{13743895347200000000000},
\qquad
\frac{5000211}{274877906944000000000000}.
\]

**PROVED.** The common ten-variable gauge maps with rank ten into each
ten-dimensional model.  Its image therefore contains a relative
neighborhood of the common point in each stochastic image.  Both pairs have
full-dimensional regular stochastic overlap, and their irreducible Zariski
closures agree pairwise.

## Strict separation of the two nonroot classes

Take the marginal on the ordered leaf tuple `(5,1,2,3)`, write its fourteen
nonconstant JC orbit coordinates as

\[
(A,B,C,D,E,F,G,H,J,K,L,M,N,O),
\]

and define

\[
I=J-K-M+N.
\]

**EXACTLY COMPUTED.** The complete parameterizations of `A` and
`B_reflected` satisfy `I=0`.  On `A_reflected`,

\[
I=-2a_1a_{10}a_{12}a_{13}a_3a_6a_8a_9
\left[a_5\{\lambda a_0+(1-\lambda)a_2\}-1\right].
\]

On `B`, put

\[
u=\lambda b_0+(1-\lambda)b_2,
\qquad
v=\lambda b_0b_1+(1-\lambda)b_2.
\]

Then

\[
I=-2b_{10}b_{12}b_{13}b_4b_6b_8b_9(b_1b_3u-v).
\]

**PROVED.** Every outside factor is positive in the open JC cube.  On
`A_reflected`, `a_5{lambda a_0+(1-lambda)a_2}<1`.  On `B`,

\[
b_1b_3u<b_1u
<\lambda b_0b_1+(1-\lambda)b_2=v.
\]

Both bracketed factors are strictly negative, hence `I>0` throughout the
complete open parameter spaces of `A_reflected` and `B`.  Therefore no model
in the zero class has even one open stochastic distribution in common with a
model in the positive class.

## Consequence for the global program

**PROVED.** Milestone 5F subsequently shows that `Psi` is not primitive.
Every network in this orbit is obtained by inserting the two-port root-cycle
move `C_root` above a four-port root cycle; collapsing that local tensor
recovers the cycle.  The `Psi` equality is therefore generated by contextual
`C_root` and reversible root placement, and the explanation persists under
K2P and K3P.

**PROVED.** The root `Psi` move can alter the leaf-labelled semi-directed
topology in a way not represented by a visible triangle redirection.  Because
a rooted network has only one global root artifact, copies of this exact move
cannot be made into independent non-triangle bits merely by putting the same
gadget in lower blobs: the incoming-port atlas reduces every surviving copy
to ordinary `T`, while the other copy choices are strictly separated.

**UNRESOLVED.** This is not yet a root-locality theorem for every strongly
tree-child level-2 generator.  A different generator could still support a
stackable non-triangle ambiguity.  The complete four-leaf atlas and the
remaining ported-generator cases must be classified before alternatives S2
or S3 can be claimed.

## Independent replay

**EXACTLY COMPUTED.** `src/verify_jc_psi_lifting.py` independently regenerates
the four census networks, checks the graph classification, factors the strict
quartet invariant, proves both 256-coordinate rational identities, computes
the exact generic ranks, and verifies the rational rank minors.

**EXACTLY COMPUTED.** `src/verify_jc_psi_lifting_stdlib.py` imports neither
SymPy nor python-flint.  Its sparse rational-function engine independently
checks both complete 256-coordinate identities; direct exact contraction at
the rational common point and multilinear finite differences replay the two
rank-ten determinants.
