# A counterexample to deterministic transport under mutual multiphase domination

## Conclusion and attribution

Mutual domination by probability kernels does not imply the existence of deterministic componentwise transports in both directions. The counterexample below uses two atomless probability measures on each of two compact standard Borel spaces. A deterministic reverse transport exists, but a deterministic forward transport does not.

This is an independently checked presentation of the interval and square obstruction in Theorem 3.1(1), pp. 4-5, of Alper Ferudun's unrefereed note, *A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces*, dated 2 October 2026. His component densities (x,1-x) are equivalent to the probability-component normalization (1,2x) below: send a pair of measures (alpha,beta) to (alpha+beta,2alpha), with inverse alpha = sigma_2/2 and beta = sigma_1-sigma_2/2. The same change on both spaces preserves the simultaneous transport conditions. No novelty or peer-reviewed publication claim is made. The mathematical argument below is self-contained.

The question is Gershon Wolansky's question in *Multiphase Optimal Transport*, Oberwolfach Report 7/2017, printed p. 388, in *Applications of Optimal Transportation in the Natural Sciences*, DOI [10.4171/OWR/2017/7](https://doi.org/10.4171/OWR/2017/7). The [published PDF](https://ems.press/content/serial-article-files/46673) places that page at physical PDF page 50. It asks whether mutual componentwise domination entails maps in both directions; it does not require those maps to be inverses. The final space in its printed reverse-domination expression is an evident repeated-space typo, and its component index uses N where the preceding definition uses k. We address the coherent mutual-domination question for k = 2.

## Definitions and measures

For measurable spaces X and Y, a probability kernel P from X to Y assigns to each x a countably additive probability measure P_x on Y, with x -> P_x(B) measurable for every measurable B in Y. It transports a finite measure sigma to eta when

    eta(B) = integral_X P_x(B) d sigma(x)

for every measurable B. A single kernel must transport every component in a multiphase transport. For a measurable map T, the pushforward is (T#sigma)(B) = sigma(T^{-1}(B)).

Let X = [0,1] and Y = [0,1]^2, both with their Borel sigma-algebras. Write lambda for Lebesgue probability measure restricted to the Borel subsets of [0,1], and lambda^2 = lambda tensor lambda. Define

    sigma_1(dx) = dx,                 sigma_2(dx) = 2x dx,
    eta_1(du,dv) = du dv,             eta_2(du,dv) = 2u du dv.

All four measures are nonnegative, nonzero probabilities: integral_0^1 1 dx = integral_0^1 2x dx = 1. The vector masses are both (1,1).

Each scalar component is atomless. For example, for a measurable A, the functions t -> sigma_i(A intersect [0,t]) and t -> eta_i(A intersect ([0,t] x [0,1])) are continuous, start at zero, and end at the measure of A. An intermediate value splits every positive-measure A into two positive-measure pieces. This also proves atomlessness directly, rather than relying merely on the absence of point atoms.

The vector measures are atomless in the usual no-vector-atoms sense. If a set A has nonzero vector measure, then its first-component measure is positive, since the second component is absolutely continuous with respect to the first. Split A into B and A\B with positive first-component measure. Then both vector measures of those pieces are nonzero. Thus A is not a vector atom.

## Mutual domination by one kernel in each direction

For x in X, define

    P_x(B) = integral_0^1 1_B(x,v) dv,       B Borel in Y.

This is the probability measure delta_x tensor lambda. Its total mass is one. For each Borel B, its vertical sections are Borel and the displayed integral is Borel measurable as a function of x. The latter follows first for measurable rectangles and then for every Borel B by the monotone class theorem. Thus P is a probability kernel, not merely a collection of conditional formulas defined separately almost everywhere.

For i = 1,2 let f_1(x) = 1 and f_2(x) = 2x. Tonelli's theorem gives, for every Borel B in Y,

    integral_X P_x(B) d sigma_i(x)
      = integral_0^1 integral_0^1 1_B(x,v) f_i(x) dv dx
      = eta_i(B).

Hence the same kernel P transports both source components to their target components.

The projection S:Y -> X, S(u,v) = u, is continuous and satisfies S#eta_i = sigma_i for both components, again by integrating over v. Equivalently,

    Q_(u,v)(A) = 1_A(u)

is a probability kernel from Y to X, and integral_Y Q_y(A) d eta_i(y) = sigma_i(A) for every Borel A. Mutual domination therefore holds, with a deterministic transport in the reverse direction.

## No deterministic forward transport

Suppose, for contradiction, that a Borel map T:X -> Y transports both components:

    T#sigma_1 = eta_1,       T#sigma_2 = eta_2.

Write T(x) = (a(x), b(x)). The coordinates are Borel measurable and take values in [0,1], so all integrals below are finite. Testing the first pushforward identity against the bounded Borel function (u,v) -> u^2 yields

    integral_0^1 a(x)^2 dx = integral_[0,1]^2 u^2 du dv = 1/3.

Testing the second identity against (u,v) -> u yields

    2 integral_0^1 x a(x) dx = integral_[0,1]^2 2u^2 du dv = 2/3.

Together with integral_0^1 x^2 dx = 1/3, these identities imply

    integral_0^1 (x-a(x))^2 dx = 1/3 - 2(1/3) + 1/3 = 0.

Since the integrand is nonnegative, a(x) = x for lambda-almost every x.

Now form the graph

    G_b = { (u,v) in [0,1]^2 : v = b(u) }.

This is a Borel set: (u,v) -> v-b(u) is Borel measurable, and G_b is its inverse image of the closed set {0}. For every u, the vertical section (G_b)_u is the singleton {b(u)}, which has lambda measure zero. Tonelli's theorem therefore gives lambda^2(G_b) = 0.

But outside a lambda-null set, T(x) = (x,b(x)) belongs to G_b. Thus

    (T#lambda)(G_b) = lambda(T^{-1}(G_b)) = 1,

contradicting T#lambda = lambda^2 and lambda^2(G_b) = 0. There is no deterministic forward map. In particular, the pair of deterministic maps asked for in the question does not exist. QED.

This is not a topological dimension argument: measurable maps can send interval Lebesgue measure to square Lebesgue measure. The second component is essential because it forces the first output coordinate to equal the input almost everywhere.

## Common dominating measures and normalization

Nothing in the proof depends on an unstated scalar normalization. The explicit kernels have mass one at every point, and each component is a probability. If a common scalar reference measure is desired for the vector Radon-Nikodym derivatives, take

    rho_X = sigma_1 + sigma_2 = (1+2x) dx,
    rho_Y = eta_1 + eta_2 = (1+2u) du dv.

Both have mass two, and P transports rho_X to rho_Y while Q transports rho_Y to rho_X. The respective vector densities are

    (1/(1+2x), 2x/(1+2x)),
    (1/(1+2u), 2u/(1+2u)).

They have nonnegative entries summing to one. The laws of these density vectors under rho_X and rho_Y agree, by integrating out v. Consequently the convex-integral expressions in the report agree as well under this reference convention. If probability reference measures are preferred, use rho_X/2 and rho_Y/2, and double the displayed vector densities. The transport identities remain unchanged. The counterexample itself was proved directly using the kernels, so it does not require any comparison-of-experiments theorem or an interpretation of the report's scalar norm notation.

## Measurable maps and completion

The Borel formulation is already a counterexample within the stated question. The obstruction to deterministic maps is also valid if the source sigma-algebra is completed and T is only Lebesgue measurable as a map to Borel Y. Each coordinate then agrees almost everywhere with a Borel function. Choose Borel versions a_0,b_0 with values in [0,1], and set T_0 = (a_0,b_0). Because both source components are absolutely continuous with respect to lambda, replacing T by T_0 on a lambda-null set preserves both pushforward identities on every Borel target set. The preceding Borel proof applies to T_0.

In particular, allowing maps into a fully completed planar target cannot restore a deterministic transport: such maps would in particular be measurable into the Borel target and would satisfy the same Borel pushforward identities.

There is a separate issue for probability kernels on completed target sigma-algebras. The formula P_x = delta_x tensor lambda is asserted here on Borel Y. We do not assert, or need, a simultaneous extension of every P_x to every set in the completed planar sigma-algebra. Completing the planar measure admits subsets of null vertical fibers whose sections need not be Lebesgue measurable. The completed-measurability robustness claim above concerns nonexistence of deterministic maps; mutual domination has been established on the stated Borel spaces.

## Optional everywhere positive densities

If strict positivity of densities at every point is desired, replace only the second components by

    sigma'_2(dx) = (2/3)(1+x) dx,
    eta'_2(du,dv) = (2/3)(1+u) du dv.

These are probabilities with continuous densities in [2/3,4/3]. The same kernels transport the corresponding components. A putative deterministic forward map still satisfies integral a dx = 1/2 and integral a^2 dx = 1/3 by its first-component pushforward. Its second-component pushforward, tested against u, gives

    integral_0^1 (1+x)a(x) dx = integral_0^1 (1+u)u du = 5/6.

Hence integral xa dx = 5/6 - 1/2 = 1/3. The same zero-square-integral and Borel-graph contradiction follows. Thus even continuous, bounded, everywhere strictly positive component densities do not rescue the asserted implication.

## References and scope

1. Gershon Wolansky, *Multiphase Optimal Transport*, in *Applications of Optimal Transportation in the Natural Sciences*, Oberwolfach Report 7/2017, pp. 388-390, question on p. 388. DOI: https://doi.org/10.4171/OWR/2017/7. Published PDF: https://ems.press/content/serial-article-files/46673.
2. Alper Ferudun, *A Negative Answer to Wolansky's Question on Mutually Dominating Multiphase Measure Spaces*, EulerSolve Research Papers, OWR-15212-005, manuscript and online release dated 2 October 2026; publicly marked unrefereed preprint. Landing page: https://eulersolve.org/papers/owr-15212-005/. DOI: https://doi.org/10.5281/zenodo.23107180. Theorem 3.1(1), pp. 4-5, is the prior interval/square example. The canonical PDF was retrieved from the linked Zenodo record and inspected; its first page also marks the note unrefereed.

The conclusion is the negative answer to the mutual-domination question as posed. It does not classify every pair of multiphase spaces, and it does not assert that deterministic maps fail in both directions in this example. It neither establishes priority for this presentation nor upgrades the cited preprint to a peer-reviewed result.
