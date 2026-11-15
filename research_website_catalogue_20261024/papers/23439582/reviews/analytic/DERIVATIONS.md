# Analytic closure of the full published claim

This is a mathematical derivation, not a computational certificate of topology. It uses the actual target and the precise classical interfaces listed in `PRIMARY_EVIDENCE.md`. The initial reconstruction remains immutable and records what was and was not established before primary reading.

## A. Finite ideals and the complete graded reduction

For an ordinary Hopf algebra B and a finite-dimensional nonzero right ideal I, form the coefficient closure J=(id tensor B^*)Delta(I). Finite tensor expansions of a finite basis of I show dim J<infinity; the counit shows I subset J. To check the coideal direction explicitly, choose an expansion Delta(i)=sum j_alpha tensor b_alpha with the b_alpha independent. Coefficient functionals show each j_alpha lies in J. Coassociativity then gives

Delta((id tensor f)Delta(i))
=sum j_alpha tensor (id tensor f)Delta(b_alpha),

so Delta(J) subset J tensor B. For b in B, the equality

((id tensor f)Delta(i))b
=sum (id tensor f_{b_(2)})Delta(i b_(1)),

where f_c(z)=f(zS(c)), follows from sum b_(1) tensor b_(2)S(b_(3))=b tensor 1. Hence J is a right ideal. If epsilon vanished on J, applying epsilon tensor id to Delta(J) would force J=0. Choose j in J with epsilon(j)=1. Then 1=sum j_(1)S(j_(2)) belongs to J, so J=B. Consequently B must be finite-dimensional. B^(op,cop), whose antipode is the same S, yields the corresponding left-ideal statement. No inverse antipode, finite-dimensional dual, commutativity or cocommutativity is used.

This recovers the classical finite-ideal result in [Lomp, section 2.4](https://arxiv.org/pdf/math/0307046v1), actual physical 4–5. Lomp's field case is a specialization of its free-over-a-ring statement; the target supplies its own direct field proof above, so no extension to arbitrary coefficient rings is needed.

For a Koszul graded Hopf algebra H in odd characteristic, use B=H#kC_2 with the target's formulas. Write a=|h| and, in a homogeneous coproduct term, b=|h_(1)| and c=|h_(2)|, so b+c=a modulo2. Expanding the target antipode gives

S_B(h#g^i)=(-1)^((i+a)a) S_H(h)#g^(i+a).

Both antipode equations can be checked without a general bosonization citation:

- For m_B(S_B tensor id)Delta_B(h#g^i), the sign is (i+a)b+(i+a)c=(i+a)a and the remaining group power is g^a. The H sum is sum S_H(h_(1))h_(2)=epsilon_H(h). If epsilon_H(h) is nonzero, a=0, so the group power and sign both become the unit. If a=1, the counit is zero and the H sum vanishes.
- For m_B(id tensor S_B)Delta_B(h#g^i), the antipode contributes (i+c)c and multiplication contributes (i+c)c again. They cancel; the group powers also cancel. The result is sum h_(1)S_H(h_(2))#1=epsilon_H(h)#1.

Associativity has sign i|a|+(i+j)|b|=j|b|+i(|a|+|b|). Both iterated coproducts yield the same triple

h_(1)#g^(|h_(2)|+|h_(3)|+i) tensor h_(2)#g^(|h_(3)|+i) tensor h_(3)#g^i.

For coproduct multiplicativity, the ordinary B tensor B product sign is (|h_(2)|+i)|a_(1)|+i|a_(2)|, exactly the H Koszul sign plus the smash-product sign. Counitality follows from the H counit and its vanishing on odd degree. Thus all ordinary Hopf axioms hold. A graded one-sided ideal I of H gives a corresponding ideal I#kC_2 of dimension 2 dim I. Infinite H gives infinite B, so the ordinary finite-ideal result applies. In characteristic 2, signs are all +1 and forgetting the grading on H directly gives an ordinary Hopf algebra. Negative integer gradings, if present, still have a well-defined parity. The main loop-chain application is connective but the algebraic lemma does not need connectedness of H_0.

## B. Why each cellular class has a finite-total-homology source

Let A be an augmented DG algebra and let K be a compact proxy for k: K is in thick_A(A) and thick_A(k), while k belongs to Loc_A(K). Then Loc_A(K)=Loc_A(k). [DGI Theorem4.9](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf), actual physical 20 / printed 376, applies to the **compact K**, not to the possibly noncompact k. With E=REnd_A(K), its exact right-module convention gives an equivalence D(E^op) -> Loc_A(K) by N tensor_E K, with inverse RHom_A(K,-).

Choose a semi-free E resolution of the corresponding N. Its generators are well-ordered with each differential involving finitely many earlier generators. The dependency closure of a finite set is finite: otherwise a finite-branching dependency tree from those roots has an infinite branch, contradicting strict descent in the well-order. Every finite dependency-closed submodule is finite semi-free; the stages are filtered and their union is the resolution. Inclusions and exact filtered unions of module complexes compute the derived filtered colimit. Applying derived tensor with K gives a filtered homotopy colimit of P in thick_A(K). Homology commutes with this filtered colimit, so every x in H_n(M) lifts from some H_n(P).

Since K is finitely built from k, its total k-homology is finite-dimensional. Long exact sequences, finite sums/shifts and retracts show the same for every P in thick_A(K). Only the class's source P is finite in this sense. The entire M need not be finite, and k need not be compact. This also agrees with the perfect-module approximation in the proof of [BIS Lemma4.1](https://nyjm.albany.edu/j/2025/31-26v.pdf), physical 9 / printed 709. The additional hypotheses of that lemma are not silently imposed on noncompact k; the direct argument uses compact K and DGI's equivalence.

For any derived A-linear f:M -> A, the image of H_*(P -> M -> A) is a graded **left** H_*(A)-ideal of finite total dimension. Section A forces that image to vanish if H_*(A) is an infinite-dimensional graded Hopf algebra. Every lifted x is killed, so H_n(f)=0 for all integers n. This proves Proposition4 of the target and is stronger than applying it only to the canonical cellular map. It proves a homology ghost, not that f is a null morphism.

## C. Compact Lie proxy and the exact completed target

Let F=F_p and X=(BG)^wedge_p. To avoid confusing cochains with chains, write C=C^*(X;F) and B=C_*(Omega X;F). The actual [DGI section 5.7](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf), physical26 / printed 382, explicitly states proxy-smallness for both C -> F and B -> F for **every compact Lie group G**, and states that (X,F) is of Eilenberg–Moore type. This is the precise interface required by the target. Its proof was read together with its local supporting propositions, rather than inferred from a title or an inventory opinion.

Here is the load-bearing transfer in detail. A faithful unitary representation of a compact Lie group can be made special unitary by adjoining det(rho)^(-1); no component-action condition is needed. The quotient M=SU(n)/G is a compact smooth manifold with a finite CW structure. It is connected because SU(n) is connected. Put S=C^*(BSU(n);F) and Q=C^*(M;F). Eilenberg–Moore over the simply connected BSU(n) identifies Q=C tensor_S F. The augmentation F is small over S; Q has finite total homology and H_0(Q)=F in the cochain convention, so it is cosmall over Q. DGI 3.16, 5.3 and 5.5 give these facts, and 4.18 constructs a compact C proxy (in this instance Q can be used).

DGI 5.7 then states F-goodness of BG, finite p-group fundamental group of its completion, and the finite-type Eilenberg–Moore conclusion. DGI 4.22 identifies B with REnd_C(F) and makes (C,F) double-centralizer complete. Proposition 4.17 transfers the proxy across that duality. Explicitly, if Q is a C proxy, L=RHom_C(Q,F) is finitely built both from F and from B: apply RHom_C(-,F) to the two finite constructions of Q. Compact-generator evaluation L tensor_End_C(Q) Q -> F is an equivalence by 4.10, and it is B-linear. Since End_C(Q) builds Q as its module, L builds F as a B-module. Thus L satisfies all three proxy conditions over completed loop chains.

No untwisted Gorenstein identification of Gamma is used. Neither adjoint orientability nor nilpotence of the pi_0 G action on G_0 is required by this proxy construction. Replacing Omega X by G, or applying cochain smallness alone without this transfer, would not establish the result; the actual primary supplies the missing transfer in full stated scope.

## D. Infinitude and arbitrary fields

[Ishiguro, printed 198](https://msp.org/gtm/2007/10/gtm-2007-10-011s.pdf) explicitly identifies p-compactness of BG with finite total F_p homology of Omega((BG)^wedge_p). Proposition 1.3(a), printed 199 / physical 5, states the necessary implication

BG p-compact => pi_0 G p-nilpotent.

Taking precisely this contrapositive gives infinite total F homology of B under the published hypothesis. There is no use of the generally false converse for arbitrary compact Lie groups. Ishiguro 1.4 on the same page even warns that the necessary condition is insufficient. The 2007 authored primary attributes the proposition to its 2001 Proposition 3.1; that older proof has not been retrieved or represented as independently re-proved. The reviewed interface is the actual cited published Proposition 1.3(a).

For any field k of characteristic p, chains on the **same space X** give R=B tensor_F k as augmented DG algebras. This is an exact extension functor. Extending L carries its finite B construction to a finite R construction, its finite F construction to a finite k construction, and its localizing construction of F to a localizing construction of k. Therefore k has a compact proxy over R. Homology also commutes with this flat extension. An infinite F basis of H_*(B) becomes a basis over k, so dim_k H_*(R) is still infinite. This remains true for arbitrary infinite or nonperfect extension fields; no infinite cochain dual is interchanged with tensor.

Pontryagin product, diagonal and inversion in a loop-group model give H_*(R) its graded Hopf structure; field Kunneth gives the required tensor-product identification. Disconnected Omega X is allowed, since loops have component multiplication and inversion. Section B applies to the canonical R-linear nu:Gamma_k R -> R and yields H_n(nu)=0 for every integer n. This proves the entire original quantified statement. Negative n also have connective target zero, but degrees0 and higher require the genuine ideal argument.

## E. Falsification boundaries and exact finite evidence

The criterion fails without infinite Hopf dimension: A=k has identity cellularization, nonzero on H_0. It fails if “Hopf” is replaced by “augmented infinite-dimensional algebra”: for A=k x k[t], augmentation to the first factor, e=(1,0) gives the compact proxy Ae=k and Gamma_k A=Ae -> A is the nonzero inclusion. The finite ideal k x0 explains the failure. These are exact counterexamples to weakened statements, not counterexamples under the published hypotheses. No converse to the non-p-nilpotence condition, arbitrary coefficient-ring claim or nullhomotopy claim is inferred.

The independent child checker in `sign-check/` uses subset-unshuffle coproducts in the infinite noncommutative free algebra k<e,o>, with full, untruncated output words. It passed 131095 exact equality comparisons across F2/F3/F5, including nine comparisons to predicted mutant residuals. The finite test domains and shared-model limits are explicit in its sealed report. Its omitted group-parity coproduct control has multiplicativity residual -2(o#1) tensor(o#1), detected in F3/F5; the particular residual vanishes in F2, while both mutated antipode convolutions still fail there. This is appropriate characteristic-sensitive evidence, not a sampled proof of the infinite theorem.

Separately, after inspecting both supplied programme bodies and their three-line optimization-guard difference, the canonical verification programme was executed once in an isolated, byte-identical copy with Python -I -B and assertions enabled. Its complete parsed output equals the published expected object; the second archived recorded-result object is byte-identical to that expected object. The two programme ASTs agree after removing precisely the added guard. Native tests use a three-letter free algebra and smaller domains. Neither run calculates a cellularization, proves a topological import, certifies arbitrary Hopf algebras, or establishes world priority. The theorem rests on sections A–D and the accepted cited topological theorem, not on finite test counts.
