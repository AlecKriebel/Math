# Attempt 3: uniformize a metric and lift at fixed height

This attempt tests two tempting constructions. Both fail for reasons that do
not refute the original question.

## Lemma 3.1: uniformly equicontinuous boundary actions cannot work here

Let an infinite group act as a convergence group on a compact metrizable Z with
at least three points. No compatible metric makes the entire group uniformly
equicontinuous. In particular it cannot make all elements L-bi-Lipschitz for
one finite L, or all elements isometries.

Proof. Take distinct g_n. The convergence property gives a subsequence and a,b
such that g_n tends locally uniformly to b outside a. Choose distinct u,v
outside a. Then both g_n u and g_n v tend to b. Uniform equicontinuity applied
to the inverse maps g_n^{-1}, which are in the same group, would imply that
u and v have zero distance. This is a contradiction. The equivalence of triple
properness and this subsequence formulation is credited to [B99, Section 1].

This lemma does not obstruct uniform quasi-Moebius actions. Those need not be
equicontinuous at a fixed boundary scale. In an isometric hyperbolic action
the base point can move arbitrarily far.

## An exact fixed-height counterexample on a hyperbolic model

Let F=F(a,b), let T be its unit-edge Cayley tree, and let C be the space of
infinite reduced words. For xi,eta in C let ell(xi,eta) be their common-prefix
length, with ell(xi,xi)=infinity. On X=C times N_0 define

q((xi,n),(eta,m)) = n+m-2 min(n,m,ell(xi,eta)),
D(x,y) = q(x,y) + 1 if x!=y, and D(x,x)=0.

Map pi(xi,n) to the prefix of xi of length n, a vertex of T. Then q is the
pullback of the tree distance, so it is a pseudometric. Adding the discrete
metric gives the genuine metric D. Furthermore

0 <= D(x,y)-d_T(pi(x),pi(y)) <= 1.

Thus every four-point sum for D differs by at most 2 from the corresponding
tree sum. The largest two four-point sums differ by at most 2: this follows
by selecting the two equal maximal tree sums, whose D sums are each at least
that common value and at most two more, while every other sum has the same
upper bound. Consequently X is Gromov-hyperbolic (with four-point constant
at most 2). Its boundary is C: the Gromov products differ by a bounded amount
from those of prefix vertices, and Gromov sequences of prefixes are exactly
sequences whose common initial words tend to infinite length. Every infinite
word is represented by its successive prefixes. This also proves that the
boundary topology is the common-prefix topology.

There is an exact action by bijections

L_g(xi,n)=(g xi,n).

For any fixed g, tree base-point change gives
|ell(g xi,g eta)-ell(xi,eta)|<=|g|, first for finite prefixes and then by a
limit. Indeed changing a base point by |g| changes each Gromov product by at
most |g|, by the triangle inequality. Hence L_g is a surjective rough isometry
with additive error 2|g|. It induces the desired action on C.

Nevertheless the family is not uniformly quasi-isometric. For n>=1 set

xi_n=a^n b b b ...,
eta_n=a^n b^{-1} b^{-1} b^{-1} ...,
g_n=a^{-n}.

At height n the two labeled points have q-distance zero and D-distance 1.
Their L_{g_n} images have distinct first letters, q-distance 2n and D-distance
2n+1. No constants lambda,C independent of n can satisfy the upper
quasi-isometry bound 2n+1<=lambda+C.

X was deliberately defined as a metric model without a geodesicity claim.
Its explicit comparison to a geodesic tree suffices for all assertions above.
This is an obstruction to the fixed-height ansatz, not to the original
problem: left translations already give F an exact isometric action on T
with this same boundary action. A successful lift must be allowed to move
height and base point.

Checkpoint: approximately 12% toward the universal target. Two overly strong
uniformizations have been ruled out; neither is asserted to be necessary.
