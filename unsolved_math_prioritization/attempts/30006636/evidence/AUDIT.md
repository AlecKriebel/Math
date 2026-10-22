# Independent audit of the trisection normalization obstruction

Problem 30006636 / OWR-14299913-005. Audit completed 8 October 2026.

## Verdict

**Accept the mathematical results at their stated, restricted scope.** The reviewed proof gives an admissible finite-group instance of the MMT construction whose unchanged closed-manifold values cannot extend to an ordinary complex oriented four-dimensional TQFT. All allowed cube roots are excluded. Its explicit constant-rescaled Euler TQFT is also correct.

No mathematical correction to the reviewed proof is required. In particular, the proof correctly uses **16**, not 4, as the stabilization constant for the group of order two. The number 4 is both the raw evaluation of the genus-one product diagram and the cube of its normalized invariant, which are different statements.

The broad, normalization-unspecified workshop question should not be marked fully solved. A literal extension of the specified numbers to the usual complex vector-space bordism functor is refuted in general. A construction after permissible renormalization, a general treatment of boundary state spaces and gluing, and realization by fusion 2-categories remain outside this proof. **One substantive mathematical approach** is an accurate count.

The final reviewed version is the 14,820-byte authored proof with SHA-256 `ea1692e3304a67d1051192bfaba974a8aaead3821bd2f38b7826cbfc00d29cf3`. The initially reviewed version had 14,830 bytes and SHA-256 `bd6cf8f186b47e223cf7478578f49e8fe684c9bd98d123ca83d2423c48d82cee`; reversing exactly two page-locator corrections in the final version reproduces that initial hash, verifying that its mathematical content is unchanged. The auditor made no changes to the proof. This audit contains authored mathematical discussion and public bibliographic references; no copied source documents or source passages accompany it.

## Source identity and normalization

The source question was checked on printed page 768, PDF page 32, of Oberwolfach Report 12/2026. It concerns extension of the trisection invariants to a four-dimensional TQFT, and also raises boundary-gluing and fusion-2-category issues. It does not specify a target category or say whether changing the closed-manifold normalization is allowed. The report identifies the MMT preprint in its references.

In the supplied arXiv v1 PDF, Definition 4.26 and Theorem 4.28 are on page 32. The former requires the punctured stabilizing evaluation to be `C_st dim(m)` for every simple boundary label; the latter fixes `I(T)=xi^(-g) av(T)` with `xi^3=C_st`. Neither statement supplies an additional arbitrary connected-manifold constant. Thus a proof concerning these exact values must not silently replace them by a more convenient normalization.

The finite-group calculation in Proposition 6.13 on page 58 gives the number of admissible labelings times one factor `|B||C|` for each red curve. Corollary 6.14 on page 59 gives an independent consistency check: in the specialization used here the resulting expression is `N^k N^(-g/3)` for the positive real normalization root. Its proof gives `C_st=N^4`. The argument under review correctly returns to Theorem 4.28 to retain every complex cube-root choice, rather than reading the positive-root shorthand as excluding the others.

The source pages 32 and 59 and the stabilizing figure on page 6 were visually inspected in addition to text extraction. The OWR page and its complete first open-question bullet were visually inspected. No claim about current literature priority or a later manuscript version is certified by this audit.

## Categorical admissibility

Set `C=Vec_G`, `B=Vec`, and `M=Vec`, using trivial cocycles and the standard spherical structures. The action of `Vec_G` forgets grading and tensors with the resulting vector space; the right `Vec` action is ordinary tensor product. These actions have the ordinary associativity and interchange maps. They satisfy the bimodule axioms because they are inherited from tensor products of vector spaces.

There is one simple object of `M`. Therefore it is finite semisimple and indecomposable. Its ordinary trace is cyclic and nondegenerate, and the two module-trace requirements reduce to the usual partial-trace identities. The simple object has trace dimension one. No freeness or faithfulness of the group action on the one-point set is required in MMT: transitivity is sufficient, and the one-point action is transitive. The trivial cochains meet the compatibility condition in the source's finite-group construction.

A `Vec_G`-module endofunctor of `Vec` is tensoring by a vector space with a coherent `G`-action. Bimodule natural transformations are intertwiners. Composition gives the usual tensor product representation, so its endofunctor category is equivalent to `Rep(G)`. With the ordinary module trace the induced spherical dimension is the ordinary representation dimension. Alternatively, taking `A` literally to be that endofunctor category makes `Phi=id` pivotal without choosing any equivalence. These facts agree with MMT Proposition 4.13 and Section 6.2.1.

For `G=C_2`, all simple objects involved in the curve labels have dimension one; there are two red representations, two green labels and one blue label. All data are admissible within the semisimple framework of the original construction. The final additional condition, nonzero stabilization, follows from the explicit value 16. No assumption that the prospective TQFT is itself semisimple or unitary is used in the obstruction.

## Label counts and topology

For a balanced `(g,k)` trisection, the red-green pair is a genus-`g` Heegaard diagram for the connected sum of `k` copies of `S^1 x S^2`. Its standard presentation has `g` generators and `g` relators and presents the free group of rank `k`.

When `B` is trivial and the region-label set has one element, the sole nontrivial admissibility conditions are the signed green-crossing words around the red curves. These are the Heegaard relators. Assignments satisfying them therefore count homomorphisms from that free group to `G`, not conjugacy classes of homomorphisms. The answer is `N^k` for a group of order `N`. Changing a relator's initial point conjugates its word; changing the relevant orientation convention inverts the relator or a generator. These operations preserve the solution count. There is no extra division by `N` or the order of a centralizer.

The regular-character identity supplies `N` for each red identity-word constraint. There are `g` red curves, giving

    av(T) = N^(g+k).

This counts only the red-green Heegaard group; it is not an assertion that the invariant is counting representations of the four-manifold's fundamental group. That distinction explains why the entire specialization collapses to an Euler-characteristic function.

Three parallel, disjoint, essential curves on a torus give a balanced `(1,1)` trisection. Each two-color pair is the genus-one diagram of `S^1 x S^2`. Gay--Kirby Remark 5(2) identifies a `(g,g)` trisection with the corresponding connected sum of `S^1 x S^3`, so this example is `S^1 x S^3`. It is not an unbalanced genus-one stabilization of the four-sphere.

The MMT stabilizing figure is balanced `(3,1)` and represents `S^4`. Its red-green pair has two transverse pairs and one parallel pair. For `C_2`, the two constrained green labels are identities and the third is arbitrary. The three red character sums each contribute two. Puncturing leaves exactly one possible boundary label, of dimension one; no label-choice or boundary-dimension factor is missing. Hence

    av(T_product) = 4,
    av_m(T_stabilizer') = C_st = 16.

Independently summing all four product-diagram terms gives 4. Summing all 64 stabilizer terms `(-1)^(r1*c1+r3*c3)` gives 40 positive and 24 negative terms, hence 16. The signs of the two individual crossings cannot affect this calculation for `C_2`.

## Root-independent algebra

For any allowed root `xi^3=N^4`, set `a=xi/N`; then `a^3=N`. The trisection handle count gives `chi(X)=2+g-3k`. Consequently

    xi^(-g) N^(g+k) = N^k a^(-g)
                        = a^(3k-g)
                        = a^(2-chi(X)).

This argument uses integer exponents and works for every root, with no branch convention or approximate cube root. Stabilization increases `(g,k)` by `(3,1)` and leaves the displayed value unchanged. The four-sphere value is one using the permitted `(3,1)` diagram; the argument does not depend on allowing a genus-zero diagram in MMT's definition.

For the group of order two, the product value `x` satisfies

    x^3 = (4/xi)^3 = 64/16 = 4.

This also agrees with `x=a^2`. Selecting another root simply multiplies the value by a cube root of unity and cannot make it an integer. The exact polynomial obstruction treats all choices simultaneously.

## TQFT trace obstruction

For an ordinary oriented four-dimensional bordism functor into finite-dimensional complex vector spaces, the closed bordism `Y x S^1` is the categorical trace of the identity cylinder of `Y`. A strong symmetric monoidal functor preserves dualities and their traces. The target trace is `dim_C Z(Y)`, independently of bases and independently of the chosen isomorphism identifying the monoidal unit with `C`.

This independence matters: rescaling evaluation and coevaluation compatibly does not rescale the trace. The zigzag identities make the two rescalings cancel. Changing a basis in `Z(empty)` conjugates an endomorphism of a one-dimensional space and also leaves its scalar unchanged.

Taking `Y=S^3` therefore requires a nonnegative integer `d` with `d^3=4`. There is no such integer: cubes of 0 and 1 are at most 1, while cubes of integers at least 2 are at least 8. The argument excludes zero state spaces as well as positive-dimensional ones. It uses no semisimplicity, positivity, unitarity or extension-to-corners assumption on the proposed TQFT.

Allowing all algebraic complex vector spaces does not repair the issue: their dualizable objects are finite-dimensional. A coevaluation is a finite tensor sum, and the zigzag identity forces its finitely many factors to span the state space. A theory with a genuinely different target category, nonstandard trace, anomalous composition law or extra bordism structure requires a separate analysis; it has not been ruled out by an ordinary vector-space dimension argument.

## Audit of the rescaled Euler theory

For any nonzero complex `a`, assign `C` to every closed oriented three-manifold, including the empty manifold. A compact oriented four-dimensional bordism `W` acts by multiplication by `a^(-chi(W))`. Use ordinary multiplication as the tensorator `C tensor C -> C` and the identity as the unit map.

Every closed oriented three-manifold, disconnected or otherwise, has Euler characteristic zero. Therefore its cylinder acts by one. For gluing along any such `Y`, Euler characteristic obeys

    chi(W' composed W) = chi(W') + chi(W) - chi(Y)
                       = chi(W') + chi(W).

This makes composition exact. Additivity under disjoint union proves compatibility with the tensorator, including closed components and empty bordisms. Ordinary multiplication satisfies associativity, unit and symmetry coherence. The symmetry bordism is a cylinder and acts by one, matching the ordinary swap under the tensorator. Diffeomorphism invariance follows directly from Euler characteristic.

The cup and cap bordisms for an object are products with an interval and have Euler characteristic zero, so they supply the standard duality of the line. Thus the trace of each identity is one, exactly as it must be. Two four-balls glued along `S^3` give the four-sphere scalar `a^(-1)a^(-1)=a^(-2)`, while `S^3 x S^1` gives one. These checks explicitly verify the potentially delicate vacuum and unit normalizations.

On connected closed manifolds this functor gives

    E_a(X) = a^(-chi(X)) = a^(-2) I_a(X).

On disconnected closed manifolds the correct comparison factor is `a^(-2 b0(X))`, with the empty manifold sent to one. A single constant independent of the number of components would not express this multiplicative extension. The reviewed proof already phrases this correctly.

A pure factor `q^chi(X)` cannot change the product value because its Euler characteristic is zero. Compatible rescaling of the Hopf integrals likewise cancels against the genus normalization, as in MMT Remark 3.15. Rescaling the module trace changes the specified input and is a separate operation. The repair above genuinely changes closed-manifold values; it is not a state-space basis choice or a freedom in the monoidal unit.

## Scope and accounting recommendation

The result negates the following precise universal assertion: every admissible MMT invariant, with its stated normalization, is the closed partition function of an ordinary complex oriented four-dimensional TQFT. One explicit counterexample is sufficient, and the proof provides one.

Because the workshop wording leaves normalization equivalence and target conventions unstated, this should be reported as a negative answer to the unchanged ordinary-TQFT reading, with the broader formulation still unresolved here. The explicit Euler repair shows that dropping the unchanged-normalization qualifier would materially overstate the obstruction. This family cannot serve as a counterexample to extension after arbitrary connected-component rescaling.

The natural approach count is one: test the trace axiom on `S^3 x S^1`, using a concrete admissible specialization. The general family computation, exact finite checks, source verification and independent audit support that approach. The Euler construction describes its limitation. They should not be counted as five separate solution attempts. Any requirement for additional approaches to the broader normalization-flexible problem remains unsatisfied by this particular note.

Recommended concise status: **Accepted normalization obstruction; broader TQFT extension question remains open in this work.** No assertion of priority, full problem resolution, or general nonextension after renormalization should accompany it.

## Independent executable checks

The accompanying source-free script `check_normalization.py` uses integer and rational arithmetic only. It enumerates the two concrete `C_2` character sums, checks standard Heegaard-label counts for cyclic groups of orders 1 through 7 and the nonabelian group `S_3`, and checks the Laurent identities modulo `a^3=N` for finitely many integer parameters. It also checks Euler gluing exponents. The output records all check counts and the limitations of such finite verification.

The topology, categorical trace theorem and arbitrary-bordism functoriality are established by the arguments above, not by finite testing. The MMT invariant theorem and its general finite-group evaluation remain declared external mathematical dependencies.

## Public references

- Catherine Meusburger, contribution with Vincentas Mulevicius and Fiona Torzewska, *Trisection invariants of four-manifolds*, Oberwolfach Report 12/2026, printed pages 767--768. [DOI](https://doi.org/10.4171/OWR/2026/12), [MFO record](https://publications.mfo.de/handle/mfo/4446).
- Catherine Meusburger, Vincentas Mulevicius and Fiona Torzewska, *Categorical 4-manifold invariants from trisection diagrams*, arXiv:2511.19384v1. [Versioned record](https://arxiv.org/abs/2511.19384v1). Relevant pages: 5--6, 14--19, 32, 53--59.
- David T. Gay and Robion Kirby, *Trisecting 4-manifolds*, Geometry & Topology 20 (2016), 3097--3132, Theorem 4 and Remark 5(2). [Publisher PDF](https://msp.org/gt/2016/20-6/gt-v20-n6-p02-s.pdf).
