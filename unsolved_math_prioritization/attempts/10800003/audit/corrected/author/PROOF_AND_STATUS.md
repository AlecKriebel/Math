# Critical-value collisions: five approaches and the remaining gap

Problem 10800003 / AMR-107-0003, queue rank 1011. Author status: **unsolved, 5/5 substantive approaches**. No target proof or target counterexample is claimed. This is an AI-assisted mathematical research packet, not human peer review, formal verification, or a novelty claim.

## 1. Controlling question and scope

V. A. Vassiliev, *A Few Problems on Monodromy and Discriminants*, Arnold Mathematical Journal 1 (2015), 201–209, §1.1, Problem 1C (printed p.203), DOI https://doi.org/10.1007/s40598-015-0011-9; official text https://amj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/.

The datum is an isolated holomorphic function germ, a miniversal deformation with Milnor number μ, a small parameter neighborhood, and a morsification with μ distinct nearby critical values. A distinguished path system determines the cycles. The question asks whether intersection 0 or ±1 suffices to lift a prescribed two-value collision into that small neighborhood. The preceding paragraph supplies the interpretation that the other critical values stay fixed and the collision follows the chosen paths. The ambient germ, starting lift, paths, and neighborhood cannot be silently changed. The known simple-singularity covering and the obstruction at intersection ±2 are credited to the source and its references.

The public primary statement was inspected both as official HTML and in the published PDF, p.203. This is a small-neighborhood continuation problem, not just an existence statement for some deformation or a test on an abstract integral matrix.

## 2. Approach 1: local-algebra completion, and why it is only local

**Strategy.** Classify a possible endpoint and attempt to invert its local critical-value map. This gives complete local models but leaves access to their neighborhood unproved.

Work in a Milnor representative for which the critical locus over a sufficiently small parameter base is finite, with total local Milnor number μ. Assume a collision lift has an endpoint in this representative; only its chosen two critical values coalesce, and the remaining μ−2 values stay distinct from each other and the collision value. Conservation of the local Milnor number assigns total multiplicity two to the collision cluster. Every other critical value has multiplicity one.

A length-two cluster therefore consists either of two Morse points, or of one critical point with Milnor number two. In the latter case the Hessian has corank one: if its corank were at least two, the maximal ideal of the local Jacobian algebra would have cotangent dimension at least two, making the algebra's length at least three. The holomorphic splitting lemma reduces corank one to a univariate germ h(z) plus a nondegenerate quadratic form. Since dim C{z}/(h')=2, h has leading degree three and is right equivalent to z³. Thus the only endpoints are a Maxwell coincidence of two A1 points or one A2 point.

This argument uses the usual splitting lemma and conservation of Milnor number; it does not derive those foundational singularity-theoretic facts from finite calculations. Near such an endpoint, versality supplies independent deformation coordinates for the local critical germs and the other Morse points. Equivalently, the Kodaira–Spencer map to the direct sum of their Jacobian algebras is an isomorphism in a sufficiently small miniversal representative. Its dimension is μ, and its basis property persists from the original base point in the finite flat critical algebra.

For the Maxwell case the two germ coordinates are their independent values u,v. Their coincidence is u=v. With c=(u+v)/2 and d=(u−v)/2, the unordered pair is determined by c and d². Setting d→0 while the other μ−2 value coordinates stay fixed realizes every sufficiently local collision of this type.

For A2 use

    H(z; a,b) = z³ − 3az + b.

Writing a=s², the critical points are z=±s and the critical values are b∓2s³. The squared difference is 16a³. A chosen branch of the cube root along a collision path therefore gives a continuous local lift a→0; the mean b and other value coordinates can be prescribed independently. A2's two standard vanishing cycles have intersection ±1; two cycles localized in distinct Morse balls at a Maxwell endpoint are disjoint and have intersection zero. These statements can also be read directly from the quadratic and cubic local models and their suspensions.

**Result.** Every endpoint of the specified kind has the expected A1+A1 or A2 local model, and those models permit the requisite local collision. **Gap.** Starting with an arbitrary specified morsification and an allowed intersection number does not give a path to either local chart inside the prescribed parameter neighborhood. Assuming that access would assume the central issue.

## 3. Approach 2: the complete rank-two reflection test

**Strategy.** Search for a sharper obstruction in the two-cycle intersection lattice and its Picard–Lefschetz transformations.

For the symmetric surface convention, choose self-intersections −2 and mutual intersection m. The rank-two Gram matrix and reflections, in the ordered cycle basis, are

    G = [[−2,m],[m,−2]],
    Ra = [[−1,m],[0,1]],    Rb = [[1,0],[m,−1]],
    P = Ra Rb = [[m²−1,−m],[m,−1]].

These follow directly from Rδ(v)=v+(v,δ)δ. Direct multiplication gives Ra²=Rb²=I, det P=1, tr P=m²−2, and det G=4−m². For m=0, P=−I and has order two. For m=±1, P²+P+I=0 and P has order three. For m=±2, P=I+N with N≠0 and N²=0, hence P^k=I+kN and infinite order. For |m|≥3, tr P>2; its real eigenvalues are reciprocal and one is >1, so P again has infinite order. Thus P has finite order exactly for |m|≤1.

This is a complete algebraic calculation for this normalized symmetric rank-two model. It does not assume that an arbitrary matrix is geometrically realizable. For a plane-curve odd-dimensional homology pairing the ordinary intersection form is alternating, and one must instead use transvections; the displayed reflection matrices must not be reused in that parity. Our geometric argument in the next section works directly on the surface and makes no parity conversion claim.

**Result.** In the symmetric convention the allowed pairs are precisely the negative-definite rank-two cases A1+A1 and A2; every invariant of this displayed matrix pair has already been accounted for. **Gap.** This matrix computation cannot distinguish two actual lifts having the same rank-two data. It proves neither their accessibility nor a new obstruction among m=0,±1. In particular, infinite order alone is not a general substitute for the endpoint argument: a nonsemisimple quasi-unipotent matrix need not be forbidden by a general monodromy theorem.

## 4. Approach 3: geometric vanishing cycles on a plane-curve fiber

**Strategy.** Seek a genuine obstruction invisible to algebraic intersection by retaining the isotopy classes of vanishing curves, rather than only their homology classes.

Restrict to a plane-curve germ, so a smooth Milnor fiber is an oriented surface. Suppose the specified collision along the chosen two vanishing paths, with all other critical values fixed, has an endpoint in the fixed Milnor representative. The vanishing paths must be continued compatibly with that collision: near the endpoint, their pieces in a small collision disk are the two local vanishing paths, and their continuation to a common regular reference fiber uses a common tail. Transporting this local pair back identifies it with the original specified pair by the same fiber diffeomorphism. Separate Hurwitz changes involving other critical values are not permitted in this identification. Transport the two vanishing curves along the lifted path with this path-system convention. Near a Maxwell endpoint they are supported in disjoint Morse neighborhoods, and hence have geometric intersection number zero. Near an A2 endpoint the standard two curves in the local once-punctured torus intersect once. A common transport diffeomorphism preserves geometric intersection number. Therefore a necessary condition is

    i_geom(a,b)=0 in the algebraic-intersection-zero case;
    i_geom(a,b)=1 in the algebraic-intersection-±1 case.

In particular, an actual distinguished pair with algebraic intersection zero but positive geometric intersection would obstruct the required collision. The same conclusion holds for algebraic intersection ±1 and geometric intersection >1. This is a conditional, geometrically finer test, not an exhibited counterexample.

We tried to produce the requisite pair by Torelli twisting. If c is a separating essential curve and a is a nonseparating curve with i_geom(a,c)>0, then b=T_c(a) has [b]=[a], since a separating Dehn twist acts trivially on H1. On a surface with boundary, [c] need not be zero, but it has zero algebraic intersection with every homology class; the transvection formula therefore still gives [T_c(a)]=[a]. Thus the algebraic intersection of a,b is zero. The standard annulus/bigon calculation gives

    i_geom(a,T_c(a)) = i_geom(a,c)² > 0.

For completeness, put a and c in minimal position, cut an annular neighborhood of c into a rectangle, and compare a's crossing arcs to their once-twisted copies. Each original crossing arc and each twisted crossing arc contribute one crossing. There are i_geom(a,c)² such pairs; the bigon criterion for minimal a,c removes no resulting pair. This gives the displayed formula. The curve a crossing a separating curve twice can be drawn as an essential arc in each side joined across the separator; hence the construction is nonempty on a surface of genus at least two.

**Rejected candidate.** This does not produce a pair in a distinguished basis: [a]=[b] makes the homology classes dependent, whereas a distinguished set of μ vanishing cycles is a basis of the Milnor homology. Therefore the easy Torelli-twist example is expressly discarded. One could instead twist only one of two independent classes, but the pair still needs simultaneous realization by the specified distinguished path system of an actual isolated singularity. No such realization is supplied here.

**Result.** The geometric-intersection necessary condition is proved under the endpoint hypotheses; the simplest apparent counterexample fails a mandatory basis condition. **Gap.** Construct and verify a genuine distinguished pair violating the condition, or prove this violation impossible. No arbitrary-surface example is promoted to a singularity counterexample.

## 5. Approach 4: inverse critical-value flow and an integrable continuation bound

**Strategy.** Turn collision lifting into an explicit differential equation and look for an a priori bound that excludes parameter escape.

Let p_i(λ) be the labelled Morse critical points along a prospective lift and v_i(λ)=F(p_i(λ),λ). Differentiation gives

    A_ik(λ) = ∂v_i/∂λ_k = (∂F/∂λ_k)(p_i(λ),λ),

because the x-gradient of F vanishes at p_i. Miniversality identifies tangent parameter vectors with the Jacobian algebra; at a Morse fiber that algebra is the direct sum of μ copies of C, evaluated at p_i. Hence A is invertible. For prescribed value motion v(t), the unique lift while it exists satisfies

    λ'(t) = A(λ(t))^(-1) v'(t).

Here labels are continued along the path; an ordering of the unordered configuration is a harmless local choice, not an extra global covering hypothesis.

**Conditional continuation theorem.** Let K be a closed Euclidean ball of radius r>0 centered at an initial Morse parameter λ0, compactly contained in a chosen valid miniversal representative. Let the labelled prescribed value path v:[0,1]→C^μ be continuous, with v(0) equal to the labelled critical values of λ0, and continuously differentiable on [0,T] for every T<1. Suppose the prescribed values are distinct for t<1 and only the designated pair collides at t=1; for the target problem the other μ−2 labelled values are constant. Suppose there is a nonnegative Lebesgue-integrable function g on [0,1] such that, wherever the maximal lift remains in K,

    ||A(λ(t))^(-1) v'(t)|| ≤ g(t),    g≥0,    integral_0^1 g(t) dt < r.

Then the lift exists for all t<1, never leaves K, and has an endpoint in its interior realizing the collision.

**Proof.** Until any first exit its distance from its initial point is bounded by the integral of g, strictly less than r, so no first exit occurs. If maximal time T<1, integrability makes λ(t) Cauchy as t→T; its limit is interior to K. The limiting critical values are distinct, so A is invertible and the inverse-function theorem extends the lift beyond T, a contradiction. If T=1 the same Cauchy argument supplies an interior endpoint, and continuity of the critical-value map gives exactly the desired limiting values. This establishes the claim. A sufficient explicit hypothesis is g(t)≤C(1−t)^(-α), 0≤α<1, with C/(1−α)<r.

The local models explain why a blow-up in A^(-1) need not itself obstruct completion. In the A2 model, with fixed mean and value difference d=v_−−v_+=4s³, one has a=(d/4)^(2/3), and |da/dd| is a constant times |d|^(−1/3). For a linear approach d(t)=d0(1−t), this is integrable. Maxwell coordinates have bounded ordered inverse differential.

**Result.** A precise sufficient analytic bound reduces escape to an inverse-Jacobian estimate, with the A2 exponent correctly integrable. **Gap.** The integer m alone supplies no such bound on A^(-1) in this work. The hypothesis is not inferred from m=0 or ±1.

## 6. Approach 5: a nonsimple separable test and its full miniversal repair

**Strategy.** Search for an explicit obstruction in separable deformations of the X9 germ x⁴+y⁴, then test whether it survives the missing miniversal directions.

For p(x)+q(y), with p',q' each having three distinct roots α_i,β_j, its nine critical values form an additive grid

    V_ij = P_i + Q_j,    P_i=p(α_i),    Q_j=q(β_j).

Consequently every rectangle obeys V_ij−V_il−V_kj+V_kl=0. Suppose two entries alone are allowed to change while the other seven are fixed. The change matrix W also has additive form W_ij=u_i+w_j and support at most two. Such a matrix must vanish: among the three rows there is a zero row, which forces all w_j equal; each nonzero row would then have all three entries nonzero, impossible. Thus no nontrivial two-value motion with seven fixed values is possible in the separable slice. This is an exact all-path restriction as long as the roots are labelled continuously and remain distinct.

It would be invalid to call this a counterexample to Problem 1C, because this slice is not miniversal. The full nine-dimensional tangent algebra is spanned by x^r y^s, 0≤r,s≤2. Its evaluation matrix at the nine Morse points is E=V(α)⊗V(β), a tensor product of Vandermonde matrices. Both factors are invertible. More explicitly,

    L_i(x)=product_(k≠i) (x−α_k)/(α_i−α_k),
    M_j(y)=product_(l≠j) (y−β_l)/(β_j−β_l),
    H_ij(x,y)=L_i(x)M_j(y)

belongs to this tangent space and evaluates to one at (α_i,β_j) and to zero at the other eight points. Because critical-value derivatives are evaluations, H_ij supplies an infinitesimal motion of exactly one value. Every two-entry value velocity is therefore attainable in the full miniversal deformation. The separable obstruction disappears already to first order.

The exact test fixture uses α=(−2,−1,3) and β=(−5,1,4). Their sums vanish, so their integrals give depressed quartics:

    p=x⁴/4−7x²/2−6x,
    q=y⁴/4−21y²/2+20y.

The nine values of p+q at the grid are distinct, and every Hessian is diagonal with nonzero diagonal entries. This is a nonsimple X9-type principal part; the displayed representative need not itself lie in any prescribed tiny parameter ball. Rescaling Fρ(x,y)=ρ⁴ F(x/ρ,y/ρ) makes its nonprincipal coefficients small and critical points ρ times as large, without changing these exact independence arguments. This scaling is used only for the separable fixture, not to assert completion of an unknown collision path.

**Result.** The strongest obvious additive-grid obstruction is genuine for the restricted slice and provably fails in the actual miniversal tangent space. **Gap.** Invertible evaluation matrices give only short-time flow. Their inverse may become large as critical points or moduli move; the global continuation estimate of Approach 4 remains unproved.

## 7. Current primary literature and the local/global distinction

The retained catalog's literature summary was not used as proof. The following primary texts were checked afresh:

- Vassiliev, *Isotopy classification of Morse polynomials of degree four on R²*, arXiv:2311.11113v12 (15 July 2026), Proposition 2, PDF pp.12–14: https://arxiv.org/abs/2311.11113v12. Its proof explicitly keeps seven values fixed and realizes the permitted real surgeries in a global canonical X9 family; it invokes Jaworski's 1988 result to control the modulus. It does not assert that the lift remains in an arbitrarily prescribed small ball around its initial germ.
- Vassiliev, *Complements of caustics of the real J10 singularities*, arXiv:2510.03883v5 (10 February 2026), Remark 4 and Proposition 7: https://arxiv.org/abs/2510.03883v5. These state real elementary-surgery realization in the global J10 polynomial spaces, via the corresponding parabolic theory. The proof and its references were inspected, but Jaworski's original 1988 proof was not independently inspected here; no independent proof of those global theorems is claimed.
- Vassiliev, *Complements of discriminants of real parabolic function singularities. II*, arXiv:2512.12738v6 (16 March 2026): https://arxiv.org/abs/2512.12738v6. The inspected main statements concern classification of real discriminant components and local Petrovskii lacunas. Section 1.2 transfers component realizations between small neighborhoods using scaling together with equisingularity along the modulus, credited there to Looijenga. This is not a lift of the specified critical-value path from its specified initial parameter, and does not state a solution of arbitrary complex Problem 1C.

There is also an elementary reason not to replace the missing local argument by weighted rescaling. For a weighted homogeneous family of degree d, the operation ρ^d F(ρ^(−w)x) multiplies the coefficient of a monomial of weight q by ρ^(d−q). Coefficients with q=d are unchanged. For X9's x²y² modulus, d=q=4; for J10's x y⁴ modulus with weights (2,1), d=q=6. Shrinking lower-weight coefficients therefore cannot force a path's marginal modulus back toward its original value. This observation rejects a proposed transfer argument; it does not exhibit a path that actually escapes.

## 8. Disposition

All five approaches above have a distinct mathematical mechanism. Source retrieval, duplicate checks, software tests, freeze preparation, and independent review are not counted as turns. The original general lifting assertion remains unresolved in this packet. The precise remaining choice is to prove nonescape/access to the local collision strata for every allowed actual pair, or give an actual isolated germ, starting morsification, distinguished pair, and prescribed collision whose lift fails. Neither abstract matrices, an arbitrary-surface pair, nor a nonversal slice is enough.

The executable verifier rechecks exact finite algebra and strict metadata. The arguments about local analytic geometry, continuation, and surface curves are written proofs requiring mathematical review; passing computations does not formally certify them. No exhaustive literature or global-open-status claim is made.
