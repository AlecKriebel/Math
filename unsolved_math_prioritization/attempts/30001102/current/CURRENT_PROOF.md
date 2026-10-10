# Polynomial bit complexity for the rational mixed-integer bipartite system

**Status: accepted complete polynomial-bit solution for the stated rational binary-input target, following independent mathematical audit. No novelty or journal-acceptance certificate.**

Target: 30001102 / OWR-2489-008, Conforti, *Combinatorial Mixed-Integer Programming*, OWR 51/2008, pp. 2904–2905, Problem 1. This packet uses one substantive approach. Its two main ingredients are a signed-threshold proximity argument and submodular minimization on a finite ring family. Neither enumeration of denominator residues nor a fixed-dimensional assumption is used.

## 1. Exact claim and input

Let a finite bipartite graph have specified disjoint vertex classes U,V, n=|U|+|V|, and edge set E. Let I be any subset of its vertices. Every demand b_e is a rational number, encoded by signed binary numerator and positive binary denominator. Define

S = {x in R^n : x_u+x_v >= b_uv for uv in E; x_i in Z for i in I}.

There are no sign restrictions on x. For a rational objective c, also encoded in binary, the minimization task is to return either (a) the statement that the infimum is -infinity, together with a feasible point and an improving integral recession direction, or (b) an exact rational minimizer in S and its value. Maximization is handled by replacing c with -c. The membership task takes a rational query point q and decides q in conv(S). Arbitrary real oracle data are not claimed to be a finite bit-complexity instance.

**Theorem.** Both tasks are solvable in time polynomial in the total binary input size. Strong separation for conv(S) is polynomial as well. Dimension, the number of integer coordinates, and all denominators vary with the input.

The cases n=0, E empty, and I empty are allowed. The zero-dimensional case is immediate; below assume n>=1. E empty can either be handled directly or by the same LP boundedness check.

## 2. Sign change and unboundedness

Put y_u=x_u for u in U and y_v=-x_v for v in V. This invertible diagonal integer map preserves exactly which coordinates must be integral. Write a_u=c_u, a_v=-c_v. The continuous relaxation is

P = {y : y_u-y_v >= b_uv for uv in E},

and the mixed set is T=P intersect {y_i integer for i in I}. We minimize a^T y.

S and T are always nonempty: for example all original x-coordinates can equal the integer M=max(0,max_e ceil(b_e)). The continuous LP is polynomial-time solvable in the rational bit model. If it is unbounded below, rational LP recession theory supplies a rational r with r_u-r_v>=0 and a^T r<0. Clearing denominators makes r integral, without changing these properties. Thus y^0+t r is in T for every nonnegative integer t, and the mixed problem is also unbounded below. A polynomial-bit rational ray can be found by the rational feasibility system r_u-r_v>=0, a^T r<=-1, and clearing its denominators still has polynomial bit length. The converse is immediate from T subset P.

Henceforth the LP has a finite optimum, and y* is a rational LP minimizer of polynomial bit length. No vertex of P is assumed; P generally has lineality.

## 3. An elementary proximity lemma

We prove that the mixed problem has a minimizer z with ||z-y*||_infinity<n. More generally, the argument works for a system of difference inequalities with any subset of integer coordinates, provided its mixed feasible set is nonempty and its continuous relaxation has a finite optimum; here only the specified P is needed.

### 3.1 Signed threshold decomposition

For any d in R^n, list its distinct positive coordinate values as 0<t_1<...<t_s and set t_0=0. For each h, let r^h be the 0/1 indicator of {i:d_i>=t_h}, with coefficient lambda_h=t_h-t_(h-1). Apply the same construction to the magnitudes of its negative coordinates: for their distinct positive magnitudes 0<q_1<...<q_t, use r^h=-1 on {i:d_i<=-q_h} and 0 elsewhere, with coefficient q_h-q_(h-1).

This yields d=sum_h lambda_h r^h, with at most n terms, each lambda_h>0 and each nonzero r^h in {0,1}^n or {0,-1}^n. Every coordinate r_i^h has the sign of d_i or is zero. Every difference r_i^h-r_j^h has the sign of d_i-d_j or is zero. In particular, since the decomposition is conformal on each coordinate and each difference,

|lambda_h r_i^h| <= |d_i|,
|lambda_h(r_i^h-r_j^h)| <= |d_i-d_j|.

These properties follow directly from the nesting of the threshold sets; they also follow by summing nonnegative terms after orienting each difference according to its sign.

### 3.2 Removing a large layer

Take any z in T and d=z-y*. For every layer (lambda,r), the point y*+lambda r belongs to P: on every row its left-hand side lies between the corresponding values at y* and z. LP optimality therefore implies a^T r>=0.

If lambda>=1, then z-r also belongs to P, by the same between-endpoints argument. It remains mixed-integer because r is integral. Moreover,

a^T(z-r)<=a^T z,
||z-r-y*||_1<||z-y*||_1.

The strict inequality holds because r is nonzero, sign-conformal to d, and |r_i|<=|d_i|.

### 3.3 Attainment without circularity

Do not assume that a mixed optimum already exists. For any z^0 in T, consider the closed set

A={z in T : a^T z<=a^T z^0}.

It is nonempty. The distance ||z-y*||_1 attains its minimum on A: restrict to the closed ball with radius ||z^0-y*||_1, which is compact. Let z minimize that distance. Section 3.2 rules out every layer coefficient lambda>=1. Thus all its at most n coefficients are strictly below 1, so ||z-y*||_infinity<n.

It follows that every feasible mixed point has a no-more-expensive mixed point in the fixed compact box y*+[-n,n]^n. Therefore minimizing the objective on the closed mixed subset of this box attains the global mixed optimum. This proves the proximity assertion and finite attainment.

## 4. Only O(n) labels per integer coordinate

For i in I put

l_i=ceil(y*_i-n),    h_i=floor(y*_i+n).

Every global mixed optimum needed above has its integer coordinates in these intervals. Each interval has h_i-l_i<=2n, independently of b's magnitude or denominators. Its endpoints have polynomial binary length because y* does.

Let D be the set of integer vectors p indexed by I satisfying these bounds and

p_u-p_v >= ceil(b_uv)  whenever u,v are both in I and uv in E.

This is exactly the set of feasible integer-coordinate assignments in the chosen intervals. Necessity is immediate. For sufficiency, convert the fixed integer y-values to the corresponding fixed original x-values and assign a sufficiently large common integer M to every remaining original x-coordinate. All edges incident with a continuous coordinate are then satisfied; edges between two integer coordinates already are satisfied. This uses the free-sign original model, and introduces no permanent nonnegativity constraint.

In particular, D is nonempty by Section 3. It is closed under componentwise minimum and maximum, since difference inequalities and coordinate bounds have this property.

For p in D define

f(p)=min {a^T y : y in P, y_i=p_i for i in I}.

Each value is finite and attained: the slice is nonempty, and its objective is bounded below by the optimum on P. It is computable exactly by a rational LP of polynomial size. The output value and an optimizing completion have polynomial bit length, uniformly for all such p. The integer endpoints and all p have polynomial bit length. The bit complexity of an exact rational LP supplies the required oracle guarantee; an unbounded continuous slice in directions of zero cost causes no difficulty.

## 5. Submodularity of the LP value function

For p,q in D choose minimizing completions y,z in their respective slices. The points y meet z and y join z belong to P. Indeed if y_u-y_v>=b and z_u-z_v>=b, then

min(y_u,z_u)>=min(y_v,z_v)+b,
max(y_u,z_u)>=max(y_v,z_v)+b.

Their fixed-coordinate vectors are p meet q and p join q. A linear functional is modular under coordinatewise meet and join, so

f(p)+f(q)=a^T y+a^T z
          =a^T(y meet z)+a^T(y join z)
          >= f(p meet q)+f(p join q).

Thus f is submodular on the finite distributive lattice D. This step is on sign-changed difference variables. The original covering feasible set is not closed under coordinatewise minimum.

## 6. Explicit polynomial-size ring-family interface

Make a ground element (i,t) for each i in I and integer l_i<t<=h_i. Its meaning is p_i>=t. The ground set W has size at most 2n|I|<=2n^2. Encode p by

A(p)={(i,t): l_i<t<=p_i}.

Union and intersection correspond exactly to coordinatewise maximum and minimum.

The family C={A(p):p in D} has the following explicit implication representation.

1. Add (i,t) implies (i,t-1) whenever t>l_i+1.
2. For every integer-integer edge, put d=ceil(b_uv). The inequality p_u>=p_v+d requires the base condition p_u>=l_v+d. If this threshold is at most l_u it is automatic, if between l_u+1 and h_u it is forced, and if larger than h_u the family is empty.
3. For each threshold (v,t), require (v,t) implies (u,t+d). A target at most l_u is automatic. A target above h_u makes (v,t) forbidden. All other targets are ordinary implication arcs.

Including the base condition in step 2 is essential. There are polynomially many nodes and arcs, at most O(n^2+n|E|). Arc arithmetic has polynomial bit length; no large numerical interval is enumerated.

A set is in C exactly when it contains all forced nodes, avoids all forbidden nodes, and is closed under implications. The minimal member is the implication closure of the forced nodes. For each node w, the smallest member containing w, if any, is the closure of the forced nodes together with w; it does not exist precisely when that closure meets a forbidden node. These closures are computable by graph reachability. An empty-family detection would be an inconsistency with the proven nonemptiness; it is nevertheless directly checkable.

Define F(A(p))=f(p). It is a rational-valued submodular function on C. Its value oracle is Section 4's LP, and the full required domain interface is supplied by these closures.

Apply polynomial-time submodular minimization on a ring family with this interface. This is the explicit reduction in Section 6 of Alexander Schrijver, *A combinatorial algorithm minimizing submodular functions in strongly polynomial time*, JCTB 80 (2000), 346–355; author manuscript https://homepages.cwi.nl/~lex/files/minsubm6.pdf . That result requires the smallest family member and the smallest family member containing each ground element; it does not assume a value oracle alone somehow locates finite values. The interface above provides exactly those data.

The algorithm makes polynomially many arithmetic operations and value-oracle calls on O(n^2) ground elements. Each oracle call is a polynomial-bit rational LP. The oracle values have polynomial encoding length, so the complete calculation is polynomial in binary input size. This assertion is polynomial bit complexity, not a claim that the entire LP-based procedure is strongly polynomial.

A minimizing p and one final optimizing LP completion produce an exact global mixed minimizer by Section 3. Applying the inverse sign change returns the requested x.

## 7. Closed rational hull and polynomial facet complexity

This section verifies the hypotheses for using exact optimization to obtain exact separation and membership. It does not assert a general equivalence between arbitrary membership and optimization or silently replace conv(S) by its closure.

Continue in y-coordinates. Let B=max(1,max_e ceil(|b_e|)); for E empty take B=1. Let H=nB+n, an integer with polynomial bit length. Let

K=conv(T intersect [-H,H]^n),    R={r:r_u-r_v>=0 for uv in E}.

### 7.1 A uniform small optimal point for every bounded objective

For any objective a bounded below on P, a annihilates the constant-vector lineality on every connected component. Fix one coordinate to zero in each component. This produces a nonempty pointed difference-constraint polyhedron. A finite minimum is attained at a vertex there. At a vertex, the tight edge equations together with these anchors have full rank; choose a spanning tree of tight edges in each component. Coordinates are sums of at most n-1 signed demands along its tree. Thus there is an LP optimum y* with ||y*||_infinity<=nB. Isolated vertices are anchored at zero.

Section 3 yields a mixed optimum with norm <nB+n=H. Consequently, for every objective bounded below on P, its infimum over T is attained in T intersect [-H,H]^n, and equals its minimum on K.

### 7.2 Equality conv(T)=K+R

The bounded mixed set in K is a finite union of bounded rational polytopes, one for each integer assignment in [-H,H]^I. Thus K is a rational polytope. The set K+R is a closed rational polyhedron.

Every r in R has a finite decomposition into nonnegative multiples of integral vectors in {0,1}^n or {0,-1}^n that themselves lie in R, by the threshold decomposition applied to r. Here the difference inequalities are homogeneous, so every threshold layer satisfies them. If d is one such integral direction and z in T, then z+k d is in T for every nonnegative integer k. Interpolating consecutive integer k shows z+t d lies in conv(T) for every real t>=0. The same holds for any point of conv(T), and then for finite sums of such directions. Hence K+R is a subset of conv(T).

Conversely, suppose z in T were outside K+R. Strong separation of this closed convex polyhedron from z gives an objective a with

a^T z < inf {a^T w:w in K+R}.

The right side is finite, so a is nonnegative on R. Since P is a nonempty polyhedron with recession cone R, a is bounded below on P. Section 7.1 therefore identifies the minimum of a on T with its minimum on K, contradicting this strict inequality. Thus T is contained in K+R, proving the equality. In particular conv(T), and therefore conv(S), is closed and rational.

### 7.3 Explicit bit bound, with no residue enumeration

Let k be the least common multiple of the positive denominators of the input demands; for E empty take k=1. Then log k is at most the sum of their binary encoding lengths, although the numerical value of k can be exponential. We only compute/store k in binary; we never enumerate its residues.

Each polytope in the finite union defining K is described by difference constraints, integer coordinate fixings, and the integer box bounds. Its constraint matrix is totally unimodular (a transposed directed incidence matrix together with unit rows). Every vertex therefore has coordinates in (1/k)Z and absolute value at most H. This follows by choosing a nonsingular active square submatrix: its determinant is plus or minus one, and its inverse is integral. K is the convex hull of finitely many such vertices.

Together with the integral threshold generators of R, we have a finite generating description of conv(T) with points in (1/k)Z^n bounded by H and rays bounded by 1. This description is used only for a size bound, not enumerated by the algorithm.

The hull is full-dimensional: in original variables it contains the convex hull of all sufficiently large integral coordinate vectors, hence contains a translated positive orthant. Homogenize the finite generators as (v,1) and (r,0), and multiply the point generators by k. All resulting integer coordinates have magnitude at most k(H+1). Each facet of this full-dimensional hull has n independent homogeneous generators on it. A cofactor normal therefore gives an integral facet inequality whose coefficients, including its constant term, have magnitude at most

T_0 = n! [k(H+1)]^n.

A generous explicit polynomial facet-encoding bound is

phi = 10(n+1)^2 [1+ceil(log2(n+1))+ceil(log2(k+1))+ceil(log2(H+2))].

Indeed the signed binary length of each coefficient is at most 2+log2(T_0+1), and there are n+1 coefficients. The displayed bound dominates their total length. The bound is computable in polynomial bit time. Lineality does not invalidate the homogeneous generator argument; a face's spanning generators may include both signs of lineality directions.

## 8. Exact membership

The preceding algorithm is a strong rational linear-optimization oracle for conv(T): finite minima are attained at explicit rational points of T, and unboundedness is detected with an improving ray. Section 7 supplies a polynomially computable facet-complexity bound for this rational polyhedron. Hence the strong optimization/strong separation theorem for well-described rational polyhedra applies (Grötschel–Lovász–Schrijver, *Geometric Algorithms and Combinatorial Optimization*, 1988 edition, Definitions 6.2.1–6.2.2, printed pp. 162–163, and Theorem 6.4.9 with its proof, printed pp. 179–180; [inspected author-hosted book](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf)). The independent audit verified this edition directly. Its strong-optimization interface permits an exact optimizing point that need not be a vertex and improving recession directions for unbounded polyhedra; the ray above can be rescaled to the requested normalization. This is a verified edition/interface of the same established dependency, not an additional theorem assumption. Its oracle complexity is polynomial in n, phi, and the rational query encoding length. A strong separation call at the sign-changed query either confirms membership or returns a valid strict separator. This proves exact membership in polynomial time.

Only the optimization-to-separation direction is needed. No unsupported claim that an arbitrary strong-membership oracle automatically supplies strong optimization is used. The original report's informal equivalence is not a substitute for these checked hypotheses.

## 9. Boundaries and audited qualifications

- This is the original free-sign, arbitrary-rational-demand problem, with all n and |I| variable.
- Pseudopolynomial dependence on k is absent: the algorithm's finite ground set is O(n^2), from proximity, not O(nk).
- The sign change is essential; min/max closure in original cover coordinates is false.
- Only integer-integer constraints are rounded, and they are rounded upward after the sign change. LP relaxation is not asserted to equal the mixed hull.
- No NP-hardness result for two nonzeros per column is imported. The proof uses two-variable difference constraints, obtained here from bipartiteness.
- Feasibility alone does not settle optimization. Sections 3–6 supply the actual optimization reduction.
- There is no claim of a polynomial-size extended formulation, a facet characterization, the separate subtree-hull conjecture, or worldwide novelty.
- Standard dependencies are exact polynomial-time rational LP, finite submodular minimization with Schrijver's explicitly checked ring-family interface, elementary polyhedral separation/recession facts, and GLS exact optimization/separation for well-described polyhedra.
- The full independent audit checks the all-layer proximity step, preservation of integer coordinates, the finite domain's base implications, oracle bit lengths, the uniform bounded-core hull argument, and the cofactor bound.
- The overall algorithm is polynomial in binary input length, not claimed strongly polynomial. Imported rational LP, submodular minimization and GLS algorithms are not implemented by these finite checkers.

## 10. Computational support and limitations

`exact_checks.py` uses Fraction arithmetic and explicit exceptions, not Python assertions. It checks tiny instances by complete LP vertex enumeration and finite integer enumeration. It is a diagnostic checker, not a polynomial SFM or ellipsoid implementation and not a substitute for the proof.

Normal, -O, and -OO executions each passed: 24 small bipartite instances, 5,380 slice LPs, 65,014 submodular pairs, 1,723 large-layer removal checks, 1,000 exact random threshold decompositions, 1,692 ring-family equivalence checks, and nine negative/guard checks. The same deterministic seed is used in all modes. The negatives reject malformed/non-bipartite endpoints, floating-point data, invalid integer indices, and a deliberately failed check; they also distinguish ceiling from floor, sign-flipped from unflipped min-closure, missing base implications, and LP relaxation from the mixed hull.

No external solver output is used to certify the universal theorem. No numerical tolerance enters the finite checks. No source document, copied dataset, or private coordination material is part of this authored mathematical proof.
