# Additional source audit: uniform time envelope

This additive verification preserves the pre-code mathematical seal. After the independent metric reviewer identified additional source printing problems, the root read Kahn's complete Theorem 3.1 proof on PDF pages 10–14 and visually inspected pages 12–13 from the root's freshly fetched, pinned bytes. The reversed lower-bound signs, inconsistent speed-threshold constant, depth-dependent printed epsilon_max, and incorrectly powered exponential-moment constant are visible in the supplied version. These are not candidate errors. The source's qualitative no-forbidden-set common time bound, which the candidate credits, can be recovered without those constants as follows.

Write q=gamma-1, a=gamma-d>0. Choose alpha>2^(q/a); in particular alpha>2. Put r_n=alpha^(-n). Each radius-r_n parent ball admits an internal radius-r_(n+1) net with at most K=(2alpha+1)^d members. There are at most K^n parent balls and K^(n+2) relevant sibling pairs at level n. These are deterministic finite nets.

For any sibling pair, the centers are at most 2r_n apart and each child radius is s=r_n/alpha. Lines whose directions lie within a fixed positive cone of half-angle at most 1/(8alpha) about the center-displacement direction, and whose perpendicular offsets lie within s/4 of the first center's projection, hit both balls: the second center's projection differs by at most 2r_n/(8alpha)=s/4. A positive orientation measure times an offset (d-1)-volume supplies a lower bound c_alpha r_n^(d-1), uniformly for every pair and n. Coincident centers only improve this bound, using any reference cone. This proves the needed positive lower line measure directly, without the source's printed cone normalization or inequality direction. Only the case with no forbidden lines is needed here.

Let b>log K and x>=0, and choose the deterministic speed threshold

    v_n(x)=[c_alpha r_n^(d-1)/(b(n+1)+x)]^(1/q).

The Poisson probability that one sibling pair lacks a line this fast is at most exp[-b(n+1)-x]. Summing over all levels and pairs gives failure probability at most

    C exp(-x), C=K^2 exp(-b)/(1-K exp(-b)).

The sum is over one countable deterministic collection, so the resulting event is common to every endpoint pair in the parent unit ball. On it, the source's recursive connection construction has at most 2^n connectors at level n, each with length at most 2r_n+2r_(n+1) and speed at least v_n(x). Its time is therefore at most

    C' sum_n [2 alpha^(-a/q)]^n [b(n+1)+x]^(1/q)
      <= C''(1+x)^(1/q).

The ratio is strictly below one by the chosen alpha. The bound follows, for example, from b(n+1)+x<=(b+1)(n+1)(1+x) and summability of the geometrically weighted (n+1)^(1/q). The connector lengths also sum since 2/alpha<1, and the residual subproblems shrink to their prescribed endpoints. Thus this construction yields feasible finite-time paths; removing loops cannot increase travel time. Existence and interpretation of minimizing paths are credited source model facts, rather than inferred from numerical checks.

A common measurable environmental envelope can be obtained from the countable collection of sibling maximal speeds: take X to be the positive part of the supremum of c_alpha r_n^(d-1)/v_max(pair)^q-b(n+1). The preceding union bound gives P(X>x)<=C exp(-x), and X is finite almost surely. Then C''(1+X)^(1/q) bounds every constructed pair's time. This proves the qualitative common stretched-exponential tail used in TURN 1 and provides deterministic T_n proportional to (n+1)^(1/q) with failure at most 2^(-n-1), after increasing its constant. No printed exact exponential-moment constant is needed.

Consequently the candidate's credited common-envelope premise survives the source-printing audit, as does its correctly unconditional record-speed argument. This reconstruction verifies a cited dependency; it is not a sixth author proof-search turn or a novelty claim. The ordinary-axiom SIRSN gap remains unchanged.

The separately checked Blanc–Curien–Kahn primary arXiv abstract (2407.07887, submitted July 10, 2024) and publisher record (Proceedings of the London Mathematical Society 131 (2025), e70070, DOI10.1112/plms.70070) support the candidate's bibliographic/model-scope description. Their local geodesic structure results are not used as a general maximum theorem or as a present-day openness certificate.
