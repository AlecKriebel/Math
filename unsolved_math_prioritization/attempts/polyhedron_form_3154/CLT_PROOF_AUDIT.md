# Verification audit: fixed-edge form of convex polyhedra

Date: 21 October 2026. Target: row 1875, problem ID 3154 / OPG-36933.

## Finding and attribution boundary

The target concentration and nondegenerate rescaled-limit statements follow rigorously from the published uniform enumeration theorem of Bender–Wormald (1988). The exact-scope statement is explicitly claimed and proved in Lachlan Bridges, *Gaussian Vertex-Face Balance in Random Convex Polyhedra with Fixed Edge Count*, arXiv:2609.22402v1, 18 September 2026, Theorem 1.1(vi), through Sections 2–4 and 6.3. The inspected argument has the required global normalization, tails and moment control. This audit supplies an authored reconstruction of that implication, not a claim of a new solution.

The mathematical acceptance below means verification of this target implication using established published enumeration results as inputs. It does not mean that Bridges's preprint is peer-reviewed or journal-accepted, nor that every stronger local/deviation/endpoint assertion in that paper has been audited. The source gate reports no journal reference at its inspection. An independent adversarial review is required alongside this report before final acceptance.

## 1. Exact sampling model and centering

For each admissible edge count e, let U(e,v) count unlabelled combinatorial types of convex three-dimensional polyhedra with e edges and v vertices. Choose a type uniformly, not a labelled graph, rooted map or geometric realization. Simple 3-connected planar graphs give the same types. Let V be its vertex count and F its face count. Euler gives V+F=e+2. Minimum vertex degree and face size give

    e/3+2 <= V,F <= 2e/3.

The permissible edge counts are 6 and all integers at least 8. Pyramids give even counts; stacking on a triangular side gives odd counts at least 9. Seven is impossible by the displayed bounds. All limits are through admissible counts.

Set i=V-1, j=F-1, so i+j=e, and X=V-(e+2)/2=i-e/2. Thus X lives on Z for even e and Z+1/2 for odd e. Polarity is a bijection of the sampled types, preserving e and interchanging V,F. Consequently the law of X is exactly symmetric, E[V]=(e+2)/2, and all odd centered moments vanish. This is not an asymptotic centering assertion.

## 2. Classical input and unrooting

Write u(i,j)=U(i+j,i+1). The published 1988 theorem and the immediately following unrooted formula imply

    u(i,j) = (1+o(1)) B(i,j),
    B(i,j) = binom(2i,j+3) binom(2j,i+3) / (4 * 3^5 * i*j*(i+j)),

uniformly as max(i,j) tends to infinity. Both binomial shifts matter. The publisher PDF, printed page 100, was visually inspected to verify the constant, shifts, uniformity, and direct unrooted conclusion. Its zero-support qualification rules out a positive proxy for a zero rooted count (apart from irrelevant very small indices); together with positivity in the bulk this verifies eventual complete central lattice support. No labelled-to-unlabelled heuristic is needed.

For clarity, the older transfer theorem also validates the route followed by Bridges. Bender–Wormald (1985), Theorem 4.1, bounds the number S(v,f) of symmetric unrooted types by o(c^v q(v,f)), uniformly for 1/2<f/v<2, with c<1 and q the rooted count. Each e-edge type has exactly 4e/|Aut| rootings because fixing an incident oriented edge-side flag fixes a connected map. Hence

    0 <= U(e,v)-q(v,f)/(4e) <= S(v,f).

Every feasible fixed-edge pair satisfies 2f-v>=4 and 2v-f>=4, hence the stated open ratio restriction, including pairs approaching its endpoints. Moreover v>=e/3+2. Thus the relative unrooting error is o(e*c^v)=O(rho^e) for any fixed rho strictly between c^(1/3) and 1. Normalizing the counts preserves a uniform multiplicative O(rho^e) error and an O(rho^e) total-variation error. This stronger error is not necessary for the target CLT: the directly published uniform unrooted formula already suffices.

Uniformity is essential: a pointwise asymptotic for fixed vertex/face ratios would not alone justify a diagonal sum or boundary control. Here it is available in the actual cited source. This audit uses the classical enumeration/asymmetry theorems as published dependencies and does not claim to have independently re-proved their entire papers.

## 3. Bulk asymptotic and rate function

Let a=i/e and define, with 0 log 0 interpreted as zero,

    I(a)=(3a-1)log(3a-1)+(2-3a)log(2-3a)
         -a log a-(1-a)log(1-a),
    G(a)=((3a-1)(2-3a))^(5/2)/(a^4(1-a)^4),
    h(a)=G(a)/(4*3^5*pi).

These functions are needed on 1/3<a<2/3. For any fixed compact subset of that interval, Stirling's formula applied uniformly gives

    u(i,e-i) = 4^e e^(-4) h(a) exp(-e I(a)) (1+o(1)).

To verify the prefactor rather than guess it, the unshifted product has prefactor

    [pi*e*sqrt((3a-1)(2-3a))]^(-1).

The two shifts multiply it asymptotically by

    ((3a-1)/(1-a))^3 * ((2-3a)/a)^3.

Finally division by 4*3^5*a*(1-a)*e^3 gives h(a)e^(-4). Thus h(1/2)=2/(3^5*pi).

Direct differentiation gives

    I''(a)=2/[a(1-a)(3a-1)(2-3a)] > 0.

Symmetry and evaluation give the unique minimum I(1/2)=0 and I'(1/2)=0. In particular,

    I(1/2+d)=16d^2+(320/3)d^4+O(d^6).

The quadratic coefficient, and not an arbitrary choice of scaling, therefore fixes the variance e/32. Symbolic checks independently verify the derivative identity and the sixth-order coefficient 23296/15.

## 4. Full-support bounds, including endpoints

Fix 0<delta<1/6. On |X|<=delta*e, continuity of h and strict convexity give constants C,c>0, independent of e and parity, such that

    u(i,e-i) <= C 4^e e^(-4) exp(-c X^2/e).

For the rest of the feasible support, use the uniform classical bound u<=C B. Each shifted binomial is at most (2e)^3 times the corresponding unshifted binomial, by the exact ratio of the three successive numerator and denominator factors. The entropy inequality binom(n,k)<=exp(n H(k/n)) applies to those unshifted binomials even at endpoints. The product of their exponential bounds is exp(e(log 4-I(a))). Discarding denominator factors if desired gives the deliberately coarse bound

    u(i,e-i) <= C e^6 4^e exp(-e I(a)).

Feasibility gives a in [1/3+1/e,2/3-1/e]. Since I extends continuously to [1/3,2/3] and is strictly positive away from 1/2, there is kappa>0 such that

    u(i,e-i) <= C e^6 4^e exp(-kappa e),  |X|>delta*e.

This handles both endpoints without applying interior Stirling there and without dividing by a vanishing prefactor. There are at most e+1 possible i. Polynomial factors therefore cannot spoil exponential negligibility.

## 5. Actual total count and lattice normalization

Choose 0<eta<1/4 and w=e^(1/2+eta). All points in the parity-dependent unit lattice with |X|<=w are eventually present: both shifted binomials are positive there and the classical theorem has the required zero-support qualification and uniform positive asymptotic. On this window, e I(1/2+X/e)=16X^2/e+O(X^4/e^3), with uniform o(1) error because 4eta-1<0. Also h(1/2+X/e)=h(1/2)(1+o(1)). Thus

    u(i,e-i)=4^e e^(-4) [2/(3^5*pi)] exp(-16X^2/e)(1+o(1)).

For either parity, the shifted Gaussian Riemann sum divided by sqrt(e) tends to the integral of exp(-16t^2), namely sqrt(pi)/4. Truncating at w does not change this limit because w/sqrt(e) tends to infinity. The central Gaussian bound controls w<|X|<=delta*e, while the exponential bound controls the remainder. Consequently the total number of sampled types is

    sum_i u(i,e-i) ~ 4^e / (486*sqrt(pi)*e^(7/2)).

This is a full diagonal sum with a proved negligible complement, not merely a saddle-point contribution asserted to be the whole answer.

## 6. Probability limit and moments

Let Z=X/sqrt(e/32), whose lattice mesh is Delta=sqrt(32/e). Dividing central counts by the total yields, uniformly on every fixed bounded z-interval,

    P(Z=z)=Delta*(2*pi)^(-1/2)*exp(-z^2/2)*(1+o(1)).

On |X|<=delta*e the probability is bounded by C*Delta*exp(-c' z^2). In the remaining region, the total probability is bounded by a polynomial in e times exp(-kappa e). These estimates prove tightness. Shifted Riemann sums of the local approximation then yield Z converging in distribution to a standard normal, without losing either parity subsequence.

For every fixed integer r>=1, the central tail sum of |z|^(2r) times that Gaussian bound tends to zero as the truncation threshold tends to infinity, uniformly in sufficiently large e. This follows by comparison with Gaussian tail integrals on meshes Delta<=1. The outer-region contribution also tends to zero: |Z| is O(sqrt(e)), so any fixed moment adds only a polynomial factor to an exponentially small bound. Hence the powers |Z|^(2r) are uniformly integrable and E[Z^(2r)] tends to (2r-1)!!. In particular Var(V)~e/32. No moment conclusion is inferred from weak convergence alone.

Finally, with beta=V/(e+2),

    sqrt(e)*(beta-1/2) = [e/(e+2)] Z/sqrt(32)
        => N(0,1/32).

It follows that beta tends in probability to 1/2, and Var(beta)~1/(32e). The exact mean of beta is 1/2. This answers both concentration and the nondegenerate rescaling question for the intended model.

## 7. Independent computation and limits of verification

The accompanying check_constants.py checks exact symbolic identities and exact rational symmetry of the shifted-binomial proxy for both parities. It also numerically normalizes that proxy at e=100,101,500,501,2000,2001,10000,10001. These are NOT exact polyhedron counts. At e=10000 its total/asymptotic ratio is approximately 0.996095, variance/e approximately 0.0312316 (target 0.03125), and standardized fourth moment approximately 2.996225 (target 3). The numerical checks detect constant/scaling mistakes but are not the proof of convergence, and give no numerical rate for the original theorem's unquantified uniform o(1).

No mathematical gap was found in the target implication. The CLT is weaker than other assertions of Bridges's Theorem 1.1; this audit does not extend acceptance automatically to moderate deviations, Mills ratios, or endpoint expansions.

## Public references

- Lachlan Bridges, *Gaussian Vertex-Face Balance in Random Convex Polyhedra with Fixed Edge Count*, arXiv:2609.22402v1 (18 September 2026): https://arxiv.org/abs/2609.22402v1
- E. A. Bender and N. C. Wormald, *The Number of Rooted Convex Polyhedra*, Canadian Mathematical Bulletin 31 (1988), 99–102: https://doi.org/10.4153/CMB-1988-015-2
- E. A. Bender and N. C. Wormald, *Almost all Convex Polyhedra are Asymmetric*, Canadian Journal of Mathematics 37 (1985), 854–871: https://doi.org/10.4153/CJM-1985-046-0
- Original problem: https://garden.irmacs.sfu.ca/op/asymptotic_distribution_of_form_of_polyhedra
- Author's parallel formulation: https://mathoverflow.net/questions/26346/limit-distribution-of-topological-form-of-polyhedra-with-large-number-of-edges
