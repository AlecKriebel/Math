# Geometric Chern operations in the arithmetic homotopy fibre: partial results

Problem: OWR 16158, Quick (joint with Hopkins), pp. 1074–1075, queue ID 30003773. Status: not solved here. This note concerns the fibre of the motivic regulator, not Rodriguez's weak arithmetic cobordism or Hodge-filtered cobordism alone.

## Setup and scope of assertions

Write E = MGL_S, B = eta_* MU_D, r:E -> B and A = fib(r). The OWR report and 2016 Paris slides supply this schematic triangle; they do not in the inspected excerpts specify every enhancement, realization, grading, or multiplicative coherence. Statements using the triangle alone are unconditional formal consequences of that setup. Statements using an E-module enhancement explicitly assume r is an E-module map, with B an E-module via a compatible multiplicative regulator. Such enhancement is not constructed by this note.

For a pointed motivic space T and bidegree (p,q), E^{p,q}(T) means [Sigma^infty T, Sigma^{p,q}E], and similarly for A,B. The ordinary unpointed X is used with X_+. The triangulated exact sequence has segment
B^{p-1,q}(T) -> A^{p,q}(T) -> E^{p,q}(T) -> B^{p,q}(T).
All new results below are elementary formal deductions; none is claimed as a new general theorem in the literature.

## Avenue 1: literal fibre-valued Chern classes and the obstruction

Proposition 1. An E-class x admits a lift to A if and only if r(x)=0. When a lift exists, its set of lifts is a torsor under coker(E^{p-1,q}(T) -> B^{p-1,q}(T)).

Proof. Exactness identifies the image of A -> E with ker(r). The inverse image of x is a coset of ker(A -> E), and that kernel is the image of B^{p-1,q}; the kernel of the latter map is the image of E^{p-1,q}. This proves both statements. The assertion concerns homotopy classes; higher coherences retain further information.

Consequently a general Chern class cannot simply be lifted merely by calling it arithmetic. Under the usual orientation-compatible complex realization, c_1^E(O(1)) on P^1_S maps to a class whose image in ordinary complex cohomology is the generator of H^2(P^1(C);Z); it is nonzero. Thus that class has no fibre lift. This example is conditional on the stated orientation/realization compatibility, not an independently established property of the incompletely specified regulator in the report.

The same issue already occurs for the unit. If r(1)=1_B and 1_B is nonzero, 1_E has no lift. Therefore no unit on A can make A -> E unit-preserving. This does not prove that the underlying spectrum A admits no abstract unital multiplication whatsoever. A fibre can naturally be a nonunital algebra or an E-module; absence of a compatible unit does not forbid Chern operators on that module.

Outcome: rules out a naive interpretation, not the stated open problem. In particular this is not a counterexample to the existence of geometric Chern operators.

## Avenue 2: oriented module operations

Assume the fibre triangle is formed in E-modules and E is oriented. For a rank-r algebraic vector bundle V on X define
c_i(V): A^{p,q}(X) -> A^{p+2i,q+i}(X), a |-> c_i^E(V) . a.
These operations exist algebraically in the enhanced category, without any lift of c_i^E(V) to A. They commute with forgetful maps to E, and satisfy naturality and the Whitney identity because those identities hold for E-Chern classes and the E-action is associative. For line bundles the formal group law identity is inherited as an identity of module operations wherever the usual evaluation of the formal group law is defined (for example on finite-dimensional smooth schemes in the standard oriented setting). No convergence claim for arbitrary infinite spaces is made.

Proof: apply the module action to each equality of E-classes. For naturality require the usual pullback compatibility of the module cohomology action. If compatible pushforwards and their projection formula have been established for A, projection formulas for these operations follow as well; this note does not construct those pushforwards.

A useful conditional strengthening is the projective bundle formula for the fibre. Suppose the Chern class actions give compatible natural maps on the whole fibre triangle, and both E and B satisfy the projective bundle formula for pi:P(V) -> X, rank(V)=r. Then the map
sum_{i=0}^{r-1} A^{p-2i,q-i}(X) -> A^{p,q}(P(V)), (a_i) |-> sum xi^i pi^*(a_i),
is an isomorphism. Proof: apply the indicated finite direct sums and shifts to the fibre triangle over X; compare it with the triangle over P(V). The E and B comparison maps are equivalences at mapping-spectrum level if the projective bundle decompositions hold in all degrees. The induced map on fibres is then an equivalence. Equivalently, the long exact sequences and five lemma prove the group statement. This requires coherent compatibility, not just unrelated abstract group decompositions. It does not supply geometric representatives of elements of A.

Outcome: a precise spectral meaning of Chern operators, but not a geometric model. The missing geometry cannot be inferred from formal module structure alone.

## Avenue 3: relative cycles and nullhomotopies

For every bidegree (p,q), the derived mapping space Map(T,Sigma^{p,q}A) is the homotopy fibre of Map(T,Sigma^{p,q}E) -> Map(T,Sigma^{p,q}B) over zero. This follows by applying the exact suspension equivalence and the limit-preserving mapping-space functor to the fibre triangle. Thus an A-cocycle of that degree consists of an E-cocycle of that degree together with a path from its B-image to zero, with equivalence and higher compatibility governed by that homotopy fibre. The statement is about derived mapping spaces (or mapping spectra and their infinite-loop spaces), not merely the kernel of a map of cohomology groups. A topologically null cobordism cycle does not suffice: the nullhomotopy is in Hodge-filtered cobordism, and can retain secondary information even when its underlying MU-class vanishes.

A precise elementary model exists if the relevant maps have been replaced by compatible cochain-complex models. For r:C^* -> D^*, put F^n=C^n direct-sum D^{n-1}, with d_F(a,b)=(d_C a,r(a)-d_D b). Its cocycles satisfy d_C a=0 and r(a)=d_D b; its boundaries are (d_C u,r(u)-d_D v). Direct calculation gives d_F^2=0. This model has the lift criterion and ambiguity of Proposition 1.

If an even-degree closed Chern representative c acts on C and its image acts on D, compatibly with r, then (a,b) |-> (ca,r(c)b) is a chain map of degree deg(c). Indeed d(ca)=c da and d(r(c)b)=r(c) db, and r(ca)=r(c)r(a). This supplies an explicit relative formula once a multiplicative chain model exists.

Limitation: arbitrary integral MU/MGL spectra cannot simply be replaced by ordinary cochain complexes without losing homotopy information. The formula is a rigorous conditional model, not an integral geometric solution. A complex-manifold group isomorphism alone does not provide an arithmetic spectrum-level geometric comparison with all required operations and nullhomotopies.

## Avenue 4: Green currents, metrics and Hodge-filtered geometry

Haus–Quick's geometric Hodge-filtered cycles use proper complex-oriented maps, connections, and currents, with f_*K^p(nabla)-dh a smooth filtered form; their 2023 Theorem 1.2 identifies the geometric and abstract Hodge-filtered groups for complex manifolds. Their 2024 Theorem 1.1 constructs proper holomorphic pushforwards, with canonical Bott orientations explained in Section 5. These are imported results, not results proved here.

The condition that the current differs from a filtered smooth form does not mean that the corresponding Hodge-filtered class is zero. On P^1(C), the degree-one divisor has nonzero ordinary cohomology class. For any normalized closed 2-form omega with integral 1, a prospective equation d h = delta_point - omega is consistent with integration, whereas d h = delta_point is impossible: integration of an exact current against the constant test function is zero and the right-hand side has integral 1. Thus the usual Green correction subtracts curvature rather than annihilating the degree-one cohomology class. This calculation explains concretely why a Hodge-filtered representative is not automatically a nullhomotopy in B.

Rodriguez, Definition 3.3.6, already gives geometric first Chern operators in his weak arithmetic theory. Importing that formula requires a comparison with the report's fibre, over its arithmetic base, preserving operations and equivalence relations. No such comparison is constructed here. His field-base restriction also obstructs simply identifying the theories.

Outcome: useful geometric input, but neither metric choice nor existing current cycles alone solve the relative arithmetic problem.

## Avenue 5: vertical supports give a genuine formal special case

Let j:eta -> S be the generic-point morphism in the setup B=j_*D. Let X be smooth over S, let Z be a closed subset with empty generic fibre, and put T=X/(X\Z), the pointed motivic quotient. Assume the usual derived pullback/pushforward adjunction used in defining B. Since j^*X=j^*(X\Z), j^*T is the zero pointed motivic object. Therefore
[ T, Sigma^{p,q}j_*D ] = [ j^*T, Sigma^{p,q}D ] = 0
for all p,q. Apply [T,-] to the fibre triangle. Both adjacent B-groups vanish, so
A_Z^{p,q}(X) -> E_Z^{p,q}(X)
is an isomorphism in every bidegree, canonically and naturally. Here the subscript Z means cohomology represented by the quotient T, not an unsupported use of a localization theorem for a different theory.

Hence every E-class WITH vertical support has a unique A-class WITH THE SAME SUPPORT mapping to it. Forgetting support gives an A-class on X. Uniqueness after forgetting support is not asserted; different supported representatives of the same underlying E-class can yield different A-classes.

With the module enhancement of Avenue 2, this supported isomorphism commutes with multiplication by E-Chern classes, since it is induced by the E-module map A -> E. Thus ordinary supported geometric descriptions, whenever available in MGL, transfer to this vertical-support special case. Existence of fundamental classes for arbitrary singular vertical subschemes is not asserted. For a regular immersion one still invokes the relevant purity/fundamental-class theorem rather than proving it by this argument.

A concrete geometric first-Chern construction in this sector does not require purity of Z. Let L be a line bundle on X, let s be an algebraic section, and suppose its zero locus Z has empty generic fibre. The section sends X\Z into L\0_X, so induces a pointed map
s_bar: X/(X\Z) -> L/(L\0_X) = Th(L).
The MGL orientation supplies the Thom class u_L in E^{2,1}(Th(L)). Pulling back gives e_Z(L,s)=s_bar^*u_L in E_Z^{2,1}(X). Its unique preimage under A_Z^{2,1}(X) -> E_Z^{2,1}(X) is a supported arithmetic lift. After forgetting support its underlying E-class is c_1^E(L): the section s and the zero section are A1-homotopic through t*s, and pullback of the Thom class by the zero section is the oriented Euler/first Chern class. No smoothness or regular-immersion hypothesis on Z is needed for this construction, beyond working with the indicated quotient and line-bundle Thom orientation.

This construction depends on the pair (L,s) and its support. It does not prove that forgetting support eliminates dependence on s; two sections of the same L may yield different A-classes with the same underlying E-class. The existence of a section with vertical zero locus is itself a restriction, not a property of all line bundles.

Outcome: a rigorously delimited sector where the archimedean target vanishes. It does not treat horizontal cycles or establish a geometric presentation of the entire arithmetic fibre.

## Remaining exact obstacle

A full solution requires an arithmetic geometric cycle/nullhomotopy model equivalent to fib(MGL_S -> eta_* MU_D), with sufficient coherent multiplicative/relative structure to identify the intended Chern operations, establish independence of auxiliary choices, and verify all relations. None of the five avenues constructs that model. The problem remains unresolved by this work; existing Hodge-filtered geometric models and Rodriguez's different theory must not be reported as its solution.

## Additional exact source check: Hopkins–Quick (2015), Section 7

Theorem 7.6 proves the projective bundle formula for logarithmic Hodge-filtered cobordism of smooth complex varieties. Proposition 7.8 establishes Chern compatibility with complex cobordism and Deligne cohomology. Theorem 7.10 constructs a morphism of oriented theories from algebraic cobordism of smooth quasi-projective complex varieties. This establishes the relevant complex-base compatibility as an imported theorem, but does not by itself identify every arithmetic realization/coherence in the report's schematic fibre. In particular it supports the conditional P1 obstruction without converting that obstruction into a refutation of the open question.

Corollary 7.12 exhibits a further exact obstruction to a shortcut: a class in the kernel of underlying topological cobordism can have nonzero Abel–Jacobi image in the Hodge-filtered theory. Therefore geometric MU-nullbordism is not enough to supply the required B-nullhomotopy. This is a structural possibility, not a claim here of a newly constructed nonzero example.

## Primary sources inspected locally

- Hopkins–Quick, Hodge filtered complex bordism, Journal of Topology 8 (2015), 147–183, Section 7, https://arxiv.org/abs/1212.2173.
- Quick, joint with Hopkins, Algebraic Cycles in Generalized Cohomology Theories, OWR 16158, pp.1074–1075.
- Quick, Paris 2016 slides, concluding Arakelov algebraic cobordism triangle.
- Haus–Quick, Geometric Hodge filtered complex cobordism (2023 local source), Definition 1.1 and Theorem 1.2.
- Haus–Quick, 2024 published pushforward article, Theorem 1.1 and Section 5.
- Rodriguez, Weak Arithmetic Cobordism, Definition 3.3.6 and base-scope warning Remark 3.2.1.

Public bibliographic URLs and current-literature status are maintained by the separate source audit, not guessed in this note.
