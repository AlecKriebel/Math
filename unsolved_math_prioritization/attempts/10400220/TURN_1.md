# Substantive turn1: a localized Gordian-distance reduction

## Route and exact outcome

The first author route tried to transport an optimal unknotting sequence across the mutation sphere. It proves an exact marked-pair distance identity and a useful complete u=2 subclass, but also identifies why localization is not automatic, even in known u=1 examples. The unrestricted mutation question remains unresolved. Classical mutation facts and Gordon–Luecke's theorem are credited; no novelty assertion is made for the elementary graph formulation.

## 1. Fixing the sphere makes a genuine local move graph

Fix a labeled decomposition S3=B1 union_S B2 with four marked endpoints on S, and fix one standard mutation half-turn rho on B2. Consider pairs of tangles with those endpoints whose union is a knot, up to isotopies of the marked pair. Edges are ordinary crossing changes supported in balls disjoint from S. Isotopies transport the marked sphere and its endpoint marking; they are not arbitrary forgetting of that data.

Rotating the second tangle by rho is an involutive graph automorphism. A crossing ball in B1 is unchanged; one in B2 and its crossing move are carried by rho. This is a genuine commutation of local operations, independent of any claim about a general unknotting disk intersecting S.

Let T1 be the vertices whose underlying knot has ordinary unknotting number1. Gordon–Luecke's Theorem7.1 says the graph involution preserves T1. For a nontrivial knot with this marked sphere, define

delta_S(K)=distance in the local graph from (K,S) to T1.

This distance is finite. Put the marked two-tangle decomposition in a diagram with S represented by a separating circle and no crossing on that circle. The descending-diagram procedure changes finitely many crossings, all in the two tangle interiors, to obtain the unknot. Immediately before the first resulting unknot, a nontrivial knot has unknotting number1. Stopping there gives a local path to T1; if K already has number1, the distance is zero. No assertion about optimality of this procedure is made.

Because mutation is an automorphism preserving the target set,

delta_S(K)=delta_S(K^rho).                                  (1)

Any path of length r to a number-one knot gives an ordinary unknotting sequence of length r+1. Hence

u(K)-1<=delta_S(K).                                         (2)

Define the nonnegative localization defect

D_S(K)=delta_S(K)-(u(K)-1).

For a mutant pair with this marking, subtraction of(1) gives the exact relation

u(K^rho)-u(K)=D_S(K)-D_S(K^rho).                            (3)

The identity isolates the issue: local move distance is invariant, but its excess over the unrestricted distance need not be known to be invariant. It does not itself prove or disprove the source assertion.

## 2. A complete number-two subclass

Suppose u(K)=2 and there is an ordinary crossing change in a ball disjoint from S taking K to a knot L with u(L)=1. After mutation, the transported move takes K^rho to L^rho, which has unknotting number1 by Gordon–Luecke. Thus u(K^rho)<=2. It cannot have number1, since applying the same theorem in reverse would make u(K)=1. It cannot be the unknot, since mutation preserves the unknot. Therefore

u(K^rho)=2.                                                (4)

Equivalently, if the smaller side of a potential counterexample has number2, **every** crossing change lowering it to number1 must fail this sphere-disjoint condition. The statement does not assert that one can recognize all such crossing disks from a single minimal diagram.

More generally, a sequence of m-1 sphere-disjoint crossing changes ending at a number-one knot gives the rigorous upper bound u(K^rho)<=m. To turn that into equality for m>=3 requires an additional lower bound; Theorem7.1 only settles the number-two case.

## 3. Why a blanket localization proof fails

Gordon–Luecke's Theorem8.2(2) explicitly includes EM-knots with u=1 and an essential Conway sphere S for which no unknotting arc is disjoint from S. Their mutation theorem handles these by additional geometry, not by claiming that every optimal unknotting arc localizes. Thus a proposed proof of full invariance by first moving every optimal crossing disk away from S would already rely on a false general statement. The precise theorem in Section2 uses a number-lowering local move as a hypothesis and does not suppress these exceptional cases.

For clarity, the defect in(3) is defined using the number-one target. It is zero for a number-one knot even when its actual final unknotting arc cannot be localized. The analogous local distance to the unknot can therefore have a positive defect already at u=1. These two distances must not be conflated.

An abstract finite graph demonstrates the logical gap after all known small-value constraints are retained. Take a fixed vertex U and pairs(A,A'),(B,B'),(T,T'). Local edges are A-B-T-U and A'-B'-T'-U, invariant under swapping primes. Add just one nonlocal edge A-T. In the full graph the distances to U are2 for A and3 for A', while the distance to the invariant number-one set{T,T'} in the local graph is2 for both. The defect values are1 and0, exactly as(3) predicts. This is not a knot construction; it shows that local equivariance and invariance at numbers0/1 alone do not imply full distance invariance.

## 4. Source dependence and remaining target

The only non-elementary input for(1) and(4) is the complete Gordon–Luecke mutation theorem at number1, with all exceptions retained. Unknot preservation is the classical consequence of preservation of the double branched cover and the order-two Smith theorem. The local move commutation and graph-distance arguments are proved directly above.

The unresolved step is to compare localization defects or find a certified pair where they differ. A next substantive route should test mutation-sensitive lower bounds and actual candidate diagrams with number at least2, rather than assuming the same cover, different slice genus, or an upper bound from a minimal diagram determines the ordinary unknotting number.
