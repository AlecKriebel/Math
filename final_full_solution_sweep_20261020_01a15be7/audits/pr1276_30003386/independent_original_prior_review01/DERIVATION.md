# Independent mathematical derivation: the exact mutual-domination question

## Quantifiers and category

The original question asks whether, for positive atomless vector measures on measurable spaces X and Y, common componentwise transport kernels in both directions imply the existence of deterministic componentwise maps T:X->Y and S:Y->X. Both maps need to exist; they need not be inverses. The inspected question imposes neither a common dimension, a continuity requirement, an independent-component condition nor completeness of the sigma-algebras. A counterexample among compact standard Borel spaces therefore suffices for its full universal implication.

Fix Borel X=[0,1], Y=[0,1]^2. Write L for the Borel Lebesgue probability and L2=L tensor L. Set

    sigma_1=L, sigma_2=2x L;
    eta_1=L2, eta_2=2u L2.

All four components have mass1. They are atomless: for a measurable A the mass of A cut by x<=t, or u<=t, is a continuous function of t, since each component density is bounded by2 and the mass between cuts s,t is at most2|t-s|. This splits every positive-measure A. The total positive measures sigma_1+sigma_2 and eta_1+eta_2 are also atomless by the same argument with bound3. In particular neither vector has a vector atom. This is stronger than checking singleton masses alone.

## One genuine common kernel in either direction

For every x define P_x=delta_x tensor L on the Borel square. It is a countably additive probability measure. For any Borel rectangle UxV, P_x(UxV)=1_U(x)L(V), a Borel function. A monotone-class argument gives Borel measurability in x for every Borel B in Y. Thus the formula defines one kernel simultaneously on the whole target Borel sigma-algebra, including x=0 and1; it is not a separately selected almost-everywhere formula for each component.

For f_1=1 and f_2=2x, Tonelli gives

    integral P_x(B) f_i(x) dx
      = integral integral 1_B(x,v) f_i(x) dv dx
      = eta_i(B).

The same P works for both components. In reverse, S(u,v)=u is continuous and Q_(u,v)=delta_u is a probability kernel. Integrating out v proves S#eta_i=sigma_i for both i. Thus mutual domination is satisfied exactly, and a reverse deterministic map actually exists.

## Adversarially test the forward map

Suppose T(x)=(a(x),b(x)) is Borel and T#sigma_i=eta_i for i=1,2. From the first identity tested against u^2,

    integral a(x)^2 dx=1/3.

From the second tested against u,

    integral x a(x) dx=1/3.

Together with integral x^2 dx=1/3 this gives integral(a-x)^2 dx=0. All tests are bounded Borel functions. Nonnegativity therefore forces a=x almost everywhere; there is no unsupported pointwise conclusion.

The graph G={(u,v):v=b(u)} is Borel as the zero set of the Borel function v-b(u). Its vertical sections are singletons, so Tonelli yields L2(G)=0. Nevertheless T(x)=(x,b(x)) lies in G outside the one null set already identified. Hence T#L(G)=1, contradicting T#L=L2. This proves that no forward deterministic transport exists. Failure of this one map is sufficient to negate the existence of the requested pair; no claim that the reverse map fails is needed.

This is not a dimension argument: without the second component a measurable map can transport interval Lebesgue measure to square Lebesgue measure. Coordinate rigidity is the essential obstruction. The proof uses neither a numerical approximation nor any general comparison-of-experiments theorem.

## Exact relation to the older published construction

Ferudun's Theorem3.1(1), printedpp4-5 in version1.0, uses alpha=x dx, beta=(1-x)dx and their square analogues. Apply the same invertible linear operation to both vector measures:

    [sigma_1] = [1 1] [alpha],       [alpha] = [0   1/2] [sigma_1],
    [sigma_2]   [2 0] [beta ]        [beta ]   [1  -1/2] [sigma_2].

Both products of these matrices are the identity. A common map or kernel transports the original pair if and only if it transports the new pair, by linearity of pushforward/integration of finite measures. Negative entries in the inverse do not invalidate the statement: both named original pairs are already positive measures, and the inverse is used only to recover equalities. It is not being used to construct arbitrary new positive measures.

The normalized weights therefore introduce neither a different mathematical result nor new priority. The same fiber kernel and projection occur in the existing paper. Its rigidity lemma implies the first-coordinate identity; the direct second-moment calculation above independently verifies the particular theorem without depending on that lemma's general formulation. The actual Borel-version graph argument is printed in the prior paper. Other examples, finite classifications and positive theorems in that paper are outside this audit.

## Completion boundary

If T is measurable from the Lebesgue-completed source into Borel Y, its coordinates have Borel versions a_0,b_0 agreeing almost everywhere, with values adjusted on a null set to stay in[0,1]. Both source components are absolutely continuous with respect to L, so the single Borel replacement T_0 preserves both pushforward identities on every Borel target set. The contradiction applies to T_0. A map into a fully completed planar target would also be measurable into the Borel target, so it cannot restore a deterministic transport.

This robustness statement does not claim that P extends simultaneously to all sets in the fully completed planar target sigma-algebra. Such a completion contains arbitrary subsets of area-zero vertical fibers, whose sections can fail to be Lebesgue measurable. No measurability or countable-additivity extension for all such target sets has been constructed here. Nor is nonexistence of every possible extension being claimed. The original measurable-space question admits the Borel spaces used above, so this separate extension issue does not weaken the negative answer.

## Endpoint positivity and normalization stress tests

For any hidden concern about the density2x vanishing at0, replace the second density by h(x)=(2/3)(1+x), and the target analogue by h(u). These densities are continuous, between2/3 and4/3, and integrate to1. The same P and Q work. The first-component identity gives integral a=1/2 and integral a^2=1/3. The second identity tested against u gives integral(1+x)a=5/6. Subtraction yields integral xa=1/3, followed by the same zero-square and graph contradiction. Alternatively the positive-density pair is the invertible reweighting (sigma_1,(2/3)sigma_1+(1/3)sigma_2) of the normalized pair. This is an elementary deduction, not an additional novel theorem.

A common reference is rho_X=(1+2x)dx and rho_Y=(1+2u)du dv. Both have mass2 and their normalized vector densities sum to1. The kernels transport these references as well. Dividing by2 gives probability references without changing the component identities. Thus neither the unspecified scalar norm in the report nor the use of probabilities rather than total mass two obstructs the example.

## Outcome and computational limits

The pinned PR proof establishes the full original negative implication on its specified Borel spaces, and accurately records the completed-source and completed-target boundary. The existing prior theorem has the same hypotheses, construction and result after the invertible component change. No mathematical repair or new publication is needed.

The independent finite diagnostics verify exact rational masses/moments, generator-rectangle identities via the original and normalized densities, matrix inverses, strict-positive reweighting, two deliberately wrong kernels and simple graph-line contradictions. These finite controls do not prove atomlessness, all-Borel kernel measurability, almost-everywhere replacements or the universal graph argument; those are the written deductions above. Historical computations and other theorems in the prior source are not claimed as reexecuted or reaudited.

This independent review and exposition extensively use AI and have no external human peer review or formal proof-assistant certification.
