# Algebraic stringy Euler numbers under divisorial contractions

## 0. Target, notation, and status

Work over C. The question is whether a divisorial Mori contraction f:X→X′ between normal projective Q-Gorenstein log-terminal varieties always satisfies

    e_alg^str(X) > e_alg^str(X′).

Here f is proper birational, contracts a divisor, and −K_X is f-ample. This is Conjecture 4 in Batyrev's contribution to OWR 46/2016, pp. 2684–2686, and Conjecture 1.5 in Batyrev–Gagliardi, arXiv:1610.03842v2. The short dataset row does not repeat the domain of the invariant. We retain the primary domain rather than manufacture a nonproper counterexample.

For smooth projective V, write e_alg(V)=Σ_p dim H_alg^{2p}(V,Q), where H_alg is the span of cycle classes. Its additive extension to varieties is used below. A nonempty smooth projective V has e_alg(V)>0; hyperplane powers show e_alg(V)≥dim(V)+1. This additive extension is not generally multiplicative for arbitrary products. Projective bundles do have the expected projective-space factor.

On a log resolution π:Y→X, write K_Y=π*K_X+Σ_i(A_i−1)D_i, where A_i>0 are log discrepancies and the D_i have simple normal crossings. The same invariant can be computed as

    e_alg^str(X)=Σ_J e_alg(D_J°) ∏_{j∈J}1/A_j,

or

    e_alg^str(X)=Σ_J e_alg(D_J) ∏_{j∈J}(1/A_j−1).

The empty closed intersection is Y; the empty open stratum is the complement of all D_i. The two expressions agree by finite inclusion–exclusion. Divisors not exceptional for one of two maps may be added to the common support with log discrepancy 1.

The general conjecture is not proved or disproved in this packet. No novelty or exhaustive current-openness claim is made.

## Route 1. Smooth centers and smooth exceptional divisors

### Proposition 1A: smooth blowups

Let Z be a nonempty smooth connected subvariety of codimension c≥2 in a smooth projective V. Let X=Bl_Z V and f:X→V. Then

    e_alg^str(X)−e_alg^str(V)=(c−1)e_alg(Z)>0.

Proof. X and V are smooth, so their stringy invariants equal their ordinary algebraic Euler invariants. Let E=P(N_{Z/V}). The cohomology blowup decomposition is

    H^{2p}(X,Q) = f*H^{2p}(V,Q)
                  ⊕ ⊕_{j=1}^{c−1} i_*(ξ^{j−1}π_E*H^{2p−2j}(Z,Q)).

The forward maps preserve algebraic classes because they are pullback, multiplication by the algebraic tautological class, and pushforward. The inverse projections are also algebraic correspondences: projective bundle integration and Chern-class corrections extract the summands. Consequently this direct decomposition restricts to the algebraic cycle-class subspaces, giving

    b_alg^{2p}(X)=b_alg^{2p}(V)+Σ_{j=1}^{c−1}b_alg^{2p−2j}(Z).

Sum over p. Finally K_X=f*K_V+(c−1)E and O_X(−E) is f-ample, so this is genuinely a Mori contraction. Codimension 1 is deliberately excluded: blowing up an invertible ideal is an isomorphism. For disconnected smooth centers, add the same positive expression over components. □

### Proposition 1B: one smooth exceptional divisor

Suppose f:X→X′ is a divisorial Mori contraction with X smooth and its whole exceptional locus a single smooth irreducible divisor E. Then, writing K_X=f*K_X′+aE,

    e_alg^str(X)−e_alg^str(X′)=a/(a+1) · e_alg(E)>0.

Proof. Since X is a log resolution of X′ with just E, the closed-stratum formula gives e_alg^str(X′)=e_alg(X)−a e_alg(E)/(a+1). To check the sign rather than assume it, a=0 would make K_X trivial on contracted curves. If a<0, f-ampleness of −K_X would make E f-ample, hence f-nef. The negativity lemma says an f-exceptional f-nef divisor has nonpositive coefficients, contradicting E effective and nonzero. Hence a>0. The claimed formula follows. □

This second proof works for arbitrary smooth E, not merely rational or homogeneous E. It stops when X is singular or E is not a smooth log-resolution divisor. Resolving those singularities introduces intersecting strata whose algebraic Euler numbers can be negative.

### Wrong-invariant check

For a smooth projective curve C of genus g, e_alg(C)=2, whereas e_top(C)=2−2g. Blowing up a smooth threefold along C changes the algebraic invariant by +2, but changes the topological Euler number by 2−2g. For g≥2 the latter is negative. This refutes only a topological replacement of the conjecture, not its actual algebraic version.

## Route 2. Toric star subdivisions and exact determinants

For a complete simplicial Q-Gorenstein toric n-fold with fan Σ, the toric stringy-volume formula gives

    e_alg^str(X_Σ)=Σ_{σ maximal} |det(v_1,…,v_n)|,

where the v_i are primitive ray generators, measured in the ambient lattice. This is the normalized volume of the fan's shed. Algebraic and topological stringy invariants agree in this toric setting; this equality is not assumed for arbitrary varieties.

Take a simplicial maximal cone σ=cone(v_1,…,v_n) and a primitive lattice vector

    v=Σ_i c_i v_i,  c_i>0.

Subdivide σ by the ray through v. The new maximal cones replace each v_i by v. Multilinearity of determinant gives

    |det(v_1,…,v_{i−1},v,v_{i+1},…,v_n)|
       =c_i |det(v_1,…,v_n)|.

All other maximal cones are unchanged. Thus the exact local change is

    Δ=(Σ_i c_i−1)|det(v_1,…,v_n)|.

The relative canonical coefficient of the inserted divisor is a=Σ_i c_i−1, since the target support function takes value 1 on every v_i. When this projective star subdivision is a Mori extraction, a>0 and Δ>0. There is no need to approximate a volume numerically.

A fully geometric infinite family is the toric weighted blowup of a fixed point of P^n with primitive positive integer weights w_1,…,w_n, n≥2. The original cone is unimodular, the subdivision is projective, and its exceptional divisor is relatively antiample. Here a=Σw_i−1>0 and

    e_alg^str(X)=n+Σ_i w_i,  e_alg^str(P^n)=n+1.

The verifier checks these determinant identities for an explicitly bounded family of primitive weights. It also checks two prohibited extrapolations: c-sum 1 gives a crepant subdivision with equality; c-sum below 1 reverses the sign and is not K-negative. General toric and spherical affirmative results were already known; this route is a reproducible special-case proof, not a new solution.

## Route 3. Canonical projective surfaces

### Proposition 3

Let f:X→X′ be a divisorial Mori contraction between projective canonical surfaces. Let μ:S→X and μ′:S′→X′ be their minimal resolutions. Then

    e_alg^str(X)−e_alg^str(X′)=k,

where k≥1 is the number of point blowups in the induced birational morphism h:S→S′.

Proof. The standard surface-resolution facts used here are: (i) canonical surface singularities are rational double points and their minimal resolutions are crepant; (ii) every resolution of a normal surface dominates its minimal resolution; and (iii) a proper birational morphism between smooth surfaces factors into point blowups. Fact (i) is recalled in Carvajal-Rojas–Yasuda, Example 2.17; fact (iii) is Stacks Project, Tag 0C5Q. The universal minimal-resolution property in (ii) is a standard surface-resolution input, not a claim checked by the numeric verifier.

The composite fμ:S→X′ is a resolution, so (ii) gives h:S→S′ with μ′h=fμ. By crepancy and resolution independence,

    e_alg^str(X)=e_alg(S),  e_alg^str(X′)=e_alg(S′).

Each point blowup adds exactly 1 to e_alg by Proposition 1A, so the difference is k. If k=0, identify S=S′. Crepancy would then imply

    μ*K_X=K_S=μ′*K_X′=μ*f*K_X′.

Pullback of Q-Cartier divisors under a birational morphism is injective, hence K_X=f*K_X′. Its degree on every contracted curve would be zero, contradicting relative ampleness of −K_X. Therefore k≥1. □

This proof does not establish the claim for noncanonical klt surfaces or for higher-dimensional canonical varieties, which need not admit crepant resolutions. Weak factorization alone in higher dimensions introduces blowdowns as well as blowups and has no automatic sign.

## Route 4. Common resolutions, known equivariant positivity, and its precise obstruction

Let p:Y→X and q=f p:Y→X′ be a common log resolution with one SNC support D_i. Let A_i and B_i be the positive log discrepancies over X and X′, respectively. The standard discrepancy comparison for a K-negative birational contraction gives A_i≤B_i for all i, with at least one strict inequality. The invariant difference is exactly

    Δ=Σ_J e_alg(D_J°) [∏_{j∈J}1/A_j−∏_{j∈J}1/B_j].        (4.1)

Every bracket is nonnegative. Thus all-stratum nonnegativity, together with a positive stratum meeting a strictly changed discrepancy, proves strict decrease. This implication is elementary. Its hypotheses are not automatic: open algebraic Euler invariants can be negative.

Batyrev–Gagliardi Theorem 3.6 proves the conjecture for an equivariant divisorial contraction with a common equivariant log resolution having finitely many orbits of a connected linear algebraic group. The orbit Euler numbers are nonnegative, and a suitable closed projective orbit ensures strictness. Theorem 1.8 yields the projective spherical case. These are established special cases, not a proof in the absence of the finite-orbit-resolution hypothesis.

### An actual geometric negative stratum

Start with X=Bl_p P^2→P^2 and then blow up m distinct points on its exceptional P^1 to obtain Y. Write D_0 for its strict transform and D_1,…,D_m for the new exceptional curves. This is a genuine common log resolution. The open algebraic Euler values are

    e_alg(D_0°)=2−m;  e_alg(D_i°)=1 (i>0);
    e_alg(D_0∩D_i)=1.

For m≥3 the central open stratum is negative. The log discrepancies over X and P^2 are, respectively,

    A=(1,2,…,2),  B=(2,3,…,3).

Formula (4.1) nevertheless gives

    Δ=(2−m)(1−1/2)+m(1/2−1/3)+m(1/2−1/6)=1.

This explicitly exhibits the cancellation that a correct general proof must control.

If one instead assigns the formal arrays A=(1,10,10,10), B=(2,10,10,10) to the three-arm SNC stratum pattern, the same weighted sum has Δ=−7/20. These are deliberately NOT asserted to be discrepancies of a Mori contraction. This numerical countermodel refutes only the inference that componentwise discrepancy growth plus positive closed-stratum Euler numbers forces (4.1) positive. Geometric compatibility imposes additional adjunction/intersection constraints.

The general remaining task is to exploit those constraints strongly enough to control every signed stratum, or to find a genuine geometric counterexample. No such step is supplied here.

## Route 5. Surface graph positivity beyond all-stratum nonnegativity

Consider a common SNC support on a smooth projective surface whose components are P^1 and whose intersections are transverse double points, with no triple points. Let d_i be the number of intersection points on D_i, counting edges with multiplicity. Outside the divisor support all contributions cancel between the two stringy expressions. For a positive log-discrepancy vector A, its remaining part is

    F(A)=Σ_i (2−d_i)/A_i + Σ_{edges ij}1/(A_i A_j).          (5.1)

The coefficient 2−d_i can be negative. Differentiation, however, gives the exact formula

    −∂F/∂A_i = [2−d_i+Σ_{j adjacent i}1/A_j]/A_i².        (5.2)

### Proposition 5A: a checked sufficient region

Let 0<A_i≤B_i for all i, with at least one strict inequality. Suppose, for every i with A_i<B_i,

    2−d_i+Σ_{j adjacent i}1/B_j >0.                       (5.3)

Then F(A)>F(B).

Proof. Along A(t)=A+t(B−A), every coordinate is ≤B_j, so the numerator in (5.2) is at least the expression in (5.3) for every changing coordinate. Thus dF(A(t))/dt is strictly negative: all changed-coordinate terms have a positive multiplier B_i−A_i and negative partial derivative. Integration from 0 to 1 proves the assertion. □

Two useful corollaries are immediate:

1. If the graph has maximum degree ≤2, condition (5.3) holds for every positive target vector B. Thus chains and cycles need no upper bound on discrepancies.
2. If every target discrepancy B_j≤1, condition (5.3) has lower bound 2. Thus even branching graphs, with genuinely negative open strata, satisfy strict monotonicity in this region.

These conclusions apply to actual contractions only after checking the stated common-resolution hypotheses and discrepancy bounds. Klt surface minimal resolutions have log discrepancies at most 1, but a common resolution dominating the source need not be that minimal resolution. For example the ordinary smooth blowup in Route 4 already has a target log discrepancy 2. Therefore the minimal-resolution bound cannot be imposed without proof on an arbitrary common resolution.

### Numerical compatibility test

For a star-shaped rational SNC graph with center self-intersection −b_0 and m one-vertex arms of self-intersections −b_i, put s=Σ_i1/b_i. Its negative intersection matrix is positive definite exactly when b_0>s (Schur complement). Adjunction for contraction of the entire graph gives

    B_0=(2−m+s)/(b_0−s),  B_i=(1+B_0)/b_i.

If only the arms are exceptional over the source, then

    A_0=1,  A_i=2/b_i.

The numerical K-negative condition at the center is

    δ=2−m−b_0+2s>0,

and B_0−1=δ/(b_0−s)>0, so every discrepancy grows. The verifier exhausts the stated finite parameter range with exact fractions and checks F(A)>F(B) for every numerically eligible star. This is only a bounded test of adjunction-compatible numerical configurations. It does not assert algebraization, a global projective realization, completeness of the graph families, or a proof for all klt surfaces.

### Contemporary adjacent results do not close the gap

Satriano–Usatine, arXiv:2607.19184v2, Theorem 1.2 concerns a seven-dimensional projective Gorenstein terminal variety with a negative off-diagonal stringy Hodge coefficient. It does not provide the algebraic cycle-class Euler invariant of a divisorial pair. That counterexample cannot simply be substituted for one in this problem. Likewise, positivity in a lexicographic motivic order under Galois quasi-étale covers in Carvajal-Rojas–Yasuda is about a different morphism and order; specialization at 1 need not preserve a strict lexicographic inequality.

## Conclusion and exact boundaries

The five routes establish explicit smooth-center and smooth-exceptional formulas, determinant proofs for toric extractions, the canonical-surface conclusion, a common-resolution criterion with its genuine negative-stratum obstruction, and a surface-graph sufficient region with exact finite tests. The already published spherical/finite-orbit cases are correctly attributed. None extends to an unrestricted divisorial Mori contraction in all dimensions.

No numerical test is used as proof of a universal geometric statement. No nonprojective example, topological replacement, formal discrepancy assignment, or neighboring conjecture is counted as a counterexample to the qualified target.
