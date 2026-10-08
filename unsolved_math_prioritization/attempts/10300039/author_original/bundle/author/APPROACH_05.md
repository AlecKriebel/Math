# 5. Attempted counterexamples by covers, isotopies, and product blow-ups

## Attempt

Begin with the full-sphere leaves of a hyperbolic surface-bundle foliation and try to create two-sided branching while retaining those limit sets. The following obstructions delimit a natural construction family.

## Lemma 5a: covering and isotopy invariance

For a finite cover p:M' -> M, the universal pullback of p^*F is the same foliation of the same universal cover as the universal pullback of F. With the lifted hyperbolic metric, the individual lifted leaves, leaf space, and ideal limit sets are literally unchanged. Thus a finite cover of the specified foliation cannot turn an R-covered leaf space into a branched one.

If h:M -> M is an ambient homeomorphism, a lift maps lifted leaves to lifted leaves and induces a homeomorphism of leaf spaces. Hence it preserves the R-covered property. If h is isotopic to the identity on compact M, choose the isotopy lift beginning at the identity. Its displacement is uniformly bounded: the lifted isotopy commutes with deck transformations, and displacement attains a bound on a compact fundamental set times [0,1]. Sets moved a bounded hyperbolic distance have unchanged visual limit sets, by Lemma 2's bounded-distance argument. In particular this preserves the full-sphere condition leaf by leaf. The compactness and chosen lift are essential to this bounded-displacement assertion.

## Lemma 5b: countable ordered interval insertions remain a line

Let S={s_i} be a countable set of distinct real numbers. Replace each s_i in R by the closed interval [0,w_i] with w_i>0 and sum_i w_i<infinity, and give the result X its natural lexicographic order topology; at points outside S retain a singleton. Then X is order-homeomorphic to R.

Proof. Define A(t)=sum_{s_i<t} w_i. Send a singleton t outside S to t+A(t), and a point (s_i,u) in the inserted interval to s_i+A(s_i)+u. This map is strictly increasing: for t<t', the increase includes t'-t>0 in addition to nonnegative inserted weights, including the unused part of any endpoint interval. It is onto. Indeed the monotone function t -> t+sum_{s_i<=t}w_i is unbounded in each direction; its only jumps are the intervals filled by the displayed rule. To verify absence of other gaps, local limits of the sum follow from summability by first discarding a tail of total weight <epsilon and then taking one-sided limits in a finite sum. Thus the image omits no real number. A strictly increasing bijection between linearly ordered spaces with their order topologies is a homeomorphism.

A standard product blow-up whose sole leaf-space effect is to replace countably many leaves of an R-covered foliation by ordered intervals has exactly this order type. The weights are coordinates, not an invariant metric, and may be chosen summably because the blown-up leaf set is countable. The conclusion does not cover arbitrary surgeries, branching replacements, or non-product regluings.

## Outcome

The specified construction family cannot furnish a counterexample: covers, conjugacies, and these product blow-ups retain R-covered leaf spaces. The desired two-sided branching has not been produced. Allowing more general surgery may create branching, but then neither tautness, the hyperbolic ambient topology, nor preservation of all full-sphere leaf limit sets is proved here. Those requirements cannot be dropped merely because a local leaf-space picture branches.

This is a construction obstruction, not an impossibility theorem for all counterexamples.
