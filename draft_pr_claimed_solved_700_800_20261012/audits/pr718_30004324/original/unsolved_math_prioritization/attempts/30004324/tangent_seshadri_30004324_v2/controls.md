# Exact controls and limits

These checks guard against common invalid shortcuts. They are independent of any novelty claim.

## Projective space

For n=1, T(P^1)=O(2), giving epsilon=2. For n>=2, the Euler sequence gives a surjection O(1)^{n+1}->T(P^n). On the normalization of any curve C, all quotient slopes of the target are at least deg C, so epsilon>=1 because deg C>=mult_x C. A line has splitting O(2) direct_sum O(1)^{n-1}, giving epsilon<=1. Thus epsilon=1. Any proposed universal lower bound epsilon>1 in dimension at least two fails this control.

## Positive determinant is weaker than positive minimum slope

On P^1, E=O(3) direct_sum O(-1) has determinant degree 2 but epsilon(E;x)=-1. It cannot replace T_X in the positive-point argument. For the tangent bundle, its special geometry and the actual minimum-slope hypothesis are essential.

## Product and smooth-fiber obstruction

If f:X->Y is smooth, dim Y>0, and the fibers have positive dimension, choose a complete integral curve C in the fiber through x. The restriction of df yields a surjection nu^*T_X -> O_{Ctilde}^{dim Y}. Its minimal normalized quotient slope is at most zero, so epsilon(T_X;x)<=0. In particular P^a times P^b, a,b>=1, fails the hypothesis. This obstruction uses a quotient, not an arbitrary subbundle.

A slightly broader elementary version applies whenever a complete curve C through x is contracted by a morphism f to a smooth Y and df|C is not identically zero: its positive-rank image is a subsheaf of a trivial bundle, has nonpositive degree, and is a quotient of nu^*T_X. This gives the same nonpositivity. A zero differential, notably in positive characteristic, must not be discarded.

## Blow-up exceptional locus

For pi:Xtilde=Bl_Z X->X with a nonempty smooth center of codimension r>=2, the exceptional divisor E is smooth and its normal bundle restricts to O(-1) on a line ell in a fiber E->Z. The normal quotient T_Xtilde|ell -> O(-1) gives epsilon(T_Xtilde;x)<=-1 for each x in E by choosing a fiber line through x. Thus a positive point is outside E. Outside E, FM21 Lemma 4.10 gives epsilon(T_Xtilde;x)<=epsilon(T_X;pi(x)). This does not by itself justify passage through arbitrary singular contractions or flips.

For Bl_Z P^n, no point outside E is positive either. A line through its image and a point of Z has a rational strict transform elltilde through x with E.elltilde>=1. The blow-up canonical formula gives -K_Xtilde.elltilde=n+1-(r-1)E.elltilde<=n, contradicting Lemma 1's n+1 bound if x were positive. No generic-position assumption on a transverse single intersection is needed.

## Stable-tree controls

With one nonconstant component and at most one marking, a nonempty contracted subtree cannot be stable: its special-point count is at most 2t, versus the required 3t. The program enumerates labeled trees up to seven vertices and checks this obstruction for every location of the marking and nonconstant vertex.

The number of markings matters. A contracted vertex attached to one nonconstant vertex and carrying two markings is stable (three special points). That negative control is explicitly accepted by the program. The candidate must therefore use the one-pointed universal curve, not claim the two-pointed stable-map space has no boundary.

Similarly, merely being degree-minimal within an arbitrarily chosen family would not exclude a lower-degree boundary component in a different family. The proof minimizes across all rational images through x.

## What the computation does not do

The code does not verify stable-map properness, deformation theory, base change, the global geometry of X, the Fano characterization, or historical novelty. It only checks finite splitting-degree identities, elementary graph stability, and numerical sample controls. The proofs of the universally quantified geometric claims are in the authored text and cited dependencies.
