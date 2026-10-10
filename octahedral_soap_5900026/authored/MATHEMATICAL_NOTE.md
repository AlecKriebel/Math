# An exact partial audit of the octahedral soap-film problem

Problem 5900026 / AMR-058-0026, rank 955. Authored 7 October 2026.

**Disposition: UNSOLVED.** Five substantive approaches are recorded below. They establish a restricted minimization theorem, explicit global lower and upper bounds, an exact affine-dual optimum, and a central-continuity obstruction. None determines the unrestricted ordinary or real-coefficient minimum. Independent review is pending. No novelty claim is made.

## 0. Scope, normalization, and the comparison identity

Let Ω = {x in R³ : |x₁|+|x₂|+|x₃| < 1}. Its frame has vertices ±e₁, ±e₂, ±e₃ and edge length √2. Index its eight triangular faces F_s by s in S={−1,1}³, where F_s lies in s·x=1 and the coordinate signs are s. Each face has area √3/2 and outward normal s/√3. Let P={s: s₁s₂s₃=1} and N=S\P.

We use the compact paired-region formulation: an eight-set finite-perimeter partition (E_s) of Ω, with trace 1 for E_s on the relative interior of F_s and trace 0 on the other faces. No chamber volumes are prescribed. The energy A is the sum of the areas of internal reduced interfaces, each counted once. This is the eight-region separation requirement; merely touching all twelve wires is insufficient. Statements below concern this explicitly fixed model. We do not assert equivalence to every other Plateau spanning convention.

Write n_{st} for the unit normal on an interface pointing from E_t into E_s. For bounded divergence-free fields v_s having the required normal traces, the divergence theorem gives

    L(v) := Σ_s ∫_{F_s} v_s·n_Ω = Σ_{s<t} ∫_{H_st} (v_s−v_t)·n_st.

Consequently, if |v_s−v_t|≤1 throughout Ω for every pair, then L(v)≤A. If only pairs in a graph G are allowed to have positive-area interfaces, it suffices to impose this norm bound on G. Equality holds for a candidate whenever v_s−v_t=n_st on each of its sheets. Smooth fields and constant fields satisfy the needed trace conditions. The same inequality holds for the real-current relaxation with the corresponding linear boundary constraints, by the mass/comass inequality. The choice of orientation is fixed by the displayed identity.

For specificity, the real paired-current relaxation used in Approach 4 has real 3-currents V_s and antisymmetric real 2-currents T_st=−T_ts, with Σ_s V_s=[[Ω]], finite pair masses, no T_st mass on the relative interiors of the boundary faces, and incidence equations

    Σ_t T_st = S_s − ∂V_s,

where S_s is the outward-oriented face current. Its energy is Σ_{s<t} M(T_st). Ordinary partitions give V_s=[[E_s]] and interfaces oriented by n_st. Pairing the incidence equations with divergence-free fields gives exactly the same comparison inequality. Convex averaging preserves these equations. The mixture used below additionally has nonnegative chamber densities, summing to one. No attainment or strong-duality theorem is needed for the bounds in this note.

The source's fractional question uses real-coefficient flat-chain/covering-space ideas. The explicit linear relaxation above is the setting for our fractional calculations; we do not claim equivalence to every possible fractional formulation, and in particular no equivalence with an arbitrary mod-v problem is assumed or proved.

## Approach 1. A primal geometric family and its exact optimum

For each s in N put J_s(a)=a s, where 0<a<1/3. The outer chamber of label s is the tetrahedron with vertices s₁e₁,s₂e₂,s₃e₃,J_s(a). Remove these four disjoint open tetrahedra. Partition the remainder by the four cones

    C_t={x : t·x≥u·x for every u in P},  t in P.

The inner chamber with label t is C_t minus the outer tetrahedra. The face trace is the required label everywhere except the edges, a set of boundary area zero. In an octant s in N, the winning inner label is obtained by flipping a coordinate having smallest absolute value. Thus an outer chamber meets exactly its three Hamming-distance-one neighbors in P. At a=1/6 all eight chambers have positive volume: each outer chamber has volume 1/12 and, by tetrahedral symmetry, each inner chamber has volume 1/4. Their sum is 4/3=|Ω|.

There are twelve outer triangular sheets, each joining an edge [s_i e_i,s_j e_j] of F_s to J_s(a). Their individual area is

    (1/2)√(6a²−4a+1).

There are six inner kites. For s,u in N agreeing in exactly coordinate k, such a kite has cyclic vertices

    0, J_s(a), s_k e_k, J_u(a).

Each consists of two triangles of area a√2/2, so its area is a√2. The total is

    A(a)=6√2 a+6√(6a²−4a+1).

Let Q(a)=6a²−4a+1. Direct differentiation gives

    A'(a)=6√2+6(6a−2)/√Q(a),
    A''(a)=12/Q(a)^(3/2)>0.

Hence a=1/6 is the unique minimum in this family, and A(1/6)=4√2. Reflection x↦−x, including relabeling s↦−s, gives the opposite-parity candidate with the same boundary trace and area. Each candidate has five tetrahedral points: the center and the four J_s. Calling it a film with a central tetrahedral point does not mean it has only one tetrahedral point.

At a=1/6 the inner normal directions form regular tetrahedra; Approach 2 checks the corresponding reflected-tetrahedron normals at each outer junction. This verifies the equal-angle junction geometry, but stationarity and one-parameter minimality do not imply unrestricted global minimality.

**Result:** an explicit ordinary competitor of area 4√2 and exact minimization within a specified one-parameter family. **Obstruction:** arbitrary competitors need not belong to this family.

## Approach 2. Exact minimization with a restricted adjacency graph

Define constant vectors

    p_t=t/(2√2), t in P;
    p_s=5s/(6√2), s in N.

The four vectors p_t form a regular tetrahedron of side one. For s in N, p_s is the reflection of p_{−s} in the affine plane through the other three tetrahedron vertices. Define affine scores

    f_t(x)=p_t·x, t in P;
    f_s(x)=p_s·x−1/(3√2), s in N.

Their maximum cells give the candidate of Approach 1 at a=1/6. On any face F_s the score of its own label is 1/(2√2), and every other score is at most that value; inequalities are strict in the face interior. In an N octant, writing m=min_i |x_i| and r=Σ_i |x_i|, the outer score beats all inner scores exactly when r+3m≥1. This is precisely the cap tetrahedron with apex s/6. No outer score wins strictly outside its own octant. To check this, let r=Σ|x_i|≤1 and m=min |x_i|. If the sign pattern of x belongs to P, the maximum inner score, multiplied by 6√2, is 3r, while 5s·x−2≤5r−2≤3r. If its sign pattern is a different member of N, let d be the sum of the absolute coordinates whose signs differ from s. There are two such coordinates and d≥2m. The difference between the scaled outer score and the maximum inner score is 2(r−1)−10d+6m≤0. Zero coordinates follow by continuity. Inside the s octant, r+3m≥1 is equivalent to r+3|x_k|≥1 for all k. Its intersection with the octant and r≤1 is exactly the tetrahedron with the stated vertices.

For a core sheet between t,u in P, |p_t−p_u|=1 and its inward normal is p_t−p_u. For an outer sheet between s in N and the label t obtained by flipping coordinate k, its plane is

    4s_k x_k + Σ_{i≠k}s_i x_i = 1,

and p_s−p_t is its unit normal pointing into the cap. The exact pair-distance inventory is:

- Six P–P pairs: distance 1.
- Twelve P–N pairs of Hamming distance one: distance 1.
- Six N–N pairs: distance 5/3.
- Four opposite P–N pairs: distance √(8/3).

Let G contain exactly the first eighteen pairs. The boundary flux is

    L(p)=4·3/(4√2)+4·5/(4√2)=4√2.

Therefore **every finite-perimeter competitor with the fixed eight face traces and with no positive-area interfaces outside G has area at least 4√2**. The explicit candidate attains this value. The result allows nonpolyhedral interfaces and disconnected chambers; the restriction is on positive-area label adjacency, not on a chosen triangulation.

The last ten pair bounds fail. Dropping the graph hypothesis invalidates the lower-bound proof. For example, the reflected candidate uses the six N–N central adjacencies forbidden by G. Thus this theorem cannot be presented as a proof of the original unrestricted problem.

**Result:** a complete, explicitly scoped restricted minimization theorem. **Obstruction:** unrestricted competitors may create one or more of the ten forbidden pair types.

## Approach 3. Solve the entire constant and affine paired-dual classes

This approach retains every pair constraint and changes the class of vector fields.

### Constant fields

Averaging any admissible constant family over the 48 signed coordinate permutations preserves feasibility and boundary flux. The resulting family is v_s=αs. The opposite-pair bound gives |α|≤1/(2√3), while the flux is 12α. Hence the exact optimum among constant paired fields is

    L_const=2√3.

This is far below 4√2. The restricted constants of Approach 2 are not admissible points of this optimization.

### Affine fields

For real parameters α,β consider

    v_s(x)=αs+β[(s·x)s−x].

Every field has zero divergence, since div((s·x)s)=|s|²=3=div x. On F_s its outward flux density is α√3+2β/√3, so

    L(v)=12α+8β.

The norm of the difference of two affine fields is convex in x. Since the closed octahedron is the convex hull of its six vertices, it suffices to check all pair bounds at those vertices. Let s,t have Hamming distance h. At x=σ e_k, after adjusting σ for the sign of s_k, the squared difference is:

- If s_k=t_k: 4h(α±β)².
- If s_k≠t_k: 4[hα²+(3−h)β²].

Take

    α=1/(2√3),  β=1/(2√2)−1/(2√3).

For h=1, the first type is at most 1/2 and the second is 2−(2/3)√6<1. For h=2, the first is at most 1 and the second is 3/2−√6/3<1. For h=3 only the second occurs, and it equals 1. Thus these are valid unrestricted paired fields, giving the rigorous bound

    L_aff=2√2+2/√3 ≤ A.

They are optimal among all affine divergence-free paired fields, not just the displayed ansatz. Indeed, average any affine feasible family over the full octahedral group. The stabilizer of s=(1,1,1) is the coordinate-permutation group. Its invariant vector is αs and its invariant matrix is a linear combination of I and ssᵀ. Zero divergence forces that matrix to be β(ssᵀ−I), yielding exactly the ansatz. Opposite-pair constraints give |α|≤1/(2√3); distance-two pairs at a shared-sign coordinate give |α|+|β|≤1/(2√2). Therefore

    12α+8β ≤ 4|α|+8(|α|+|β|)
               ≤ 2/√3+2√2,

and the explicit parameters attain equality. The remaining constraints have already been checked.

Numerically the bound is approximately 3.98313 versus the candidate's 5.65685. This elementary exact bound is not claimed to improve Brakke's historical numerical bounds.

**Result:** exact solutions of two full-pair dual classes, with a nonconstant globally admissible certificate. **Obstruction:** even the complete affine class has a strict gap; increasing a mesh or reporting numerical convergence is not an equality proof.

## Approach 4. Fractional superposition and the relaxation gap

Encode each ordinary candidate by its oriented pair-interface currents T_st and chamber currents. Boundary conditions and the incidence equations are linear. If T⁺ and T⁻ encode the two parity candidates, then

    T^mix=(T⁺+T⁻)/2

is admissible in the corresponding real-coefficient relaxation. Equivalently, the chamber densities are the averages of the two indicator families, take values 0,1/2,1, sum to one, and have the same face traces. This constructs a fractional competitor; it is not an ordinary partition.

The mass of this specific mixture is exactly 4√2, not smaller. To see there is no positive-area cancellation, first compare sheet planes. Outer triangle planes have normals with absolute-coordinate pattern (4,1,1), whereas core planes have pattern (0,1,1); they cannot be coplanar. Parallel outer planes from opposite parity configurations are opposite faces of a slab (right side 1 with opposite normals), hence are disjoint. Core sheets from both configurations can share a plane, but then their kite interiors are on opposite sides of x_k=0, where k is the common-sign coordinate of the two central chamber labels. They intersect only on a set of area zero. All other sheet-plane intersections are at most one-dimensional. Consequently the two supports are disjoint up to area-zero sets, and multiplying both by 1/2 gives their arithmetic mean mass.

Combining this upper bound with Approach 3 gives, in the specified real-current relaxation and compact ordinary partition model,

    2√2+2/√3 ≤ inf A_real ≤ inf A_ordinary ≤ 4√2.

The ordinary inclusion in the relaxation proves the middle inequality. The mixture neither proves equality of the two infima nor produces an integrality gap. Its geometric support, if densities are discarded, has area 8√2 and is not a better ordinary film.

The 2017 covering-space examples with edge-wetting conditions do not settle the fixed eight-face separation problem. Likewise, the inherited research record's identification of fractional density with unspecified mod-v minimization has no verified justification and is not used here.

**Result:** an exact fractional competitor and a careful ordinary/real comparison. **Obstruction:** a strictly cheaper fractional competitor or a sharp all-pair dual certificate is still missing.

## Approach 5. A central-continuity obstruction for sharp paired calibration

**Theorem.** There is no full-pair calibration of boundary flux 4√2 for which all eight fields have continuous representatives at the center and the comparison identity and interface saturation apply to the two candidates above. In particular no globally continuous classical paired calibration can certify their area as the unrestricted minimum.

**Proof.** Any admissible paired family with flux 4√2 must attain equality in the comparison inequality on each of the two candidates, since both have area 4√2 and the same face traces. On every positive-area sheet, equality and the norm bound imply

    v_s−v_t=n_st

almost everywhere. Approach the origin through the interiors of the six core sheets of the P-centered candidate. Continuity at zero implies, for a vector c_P independent of t,

    v_t(0)=c_P+t/(2√2),  t in P.

Indeed every pair of the four central labels has a core sheet reaching the center, and its normal difference is (t−u)/(2√2). The N-centered candidate similarly forces

    v_s(0)=c_N+s/(2√2),  s in N.

For each t in P the full-pair constraint between t and −t gives, with d=c_P−c_N,

    |d+t/√2|≤1.

But Σ_{t in P}t=0 and |t/√2|²=3/2, whence

    Σ_{t in P}|d+t/√2|²=4|d|²+6≥6.

The four upper bounds would make this sum at most 4, a contradiction. ∎

Continuity is essential to this proof. A bounded field with direction-dependent behavior near the origin need not have a single value there compatible with all sheet limits; merely assigning a value at that point does not restore continuity. The theorem does not rule out singular or discontinuous calibrations, does not prove such a calibration exists, and does not prove a fractional integrality gap. If a full-pair calibration at the candidate value exists, at least one of its eight fields must fail this central continuity property. Brakke's symmetry/radial investigations motivate this route; the explicit finite-vector contradiction above spells out the obstruction.

**Result:** a rigorous no-go theorem for a natural sharp-certificate class. **Obstruction:** the unrestricted problem needs a genuinely noncontinuous central certificate, a different proof method, or a lower-area counterexample. No such object is supplied here.

## Final status and scaling

The five approaches leave both original minima unresolved. The strongest theorem proved here is graph-restricted, and the strongest explicitly constructed full-pair lower bound here is 2√2+2/√3. The candidate has total area 4√2 in the ±e_i normalization. For wire-edge length ℓ, multiply all areas by ℓ²/2; its area is then 2√2 ℓ².

The exact checks accompanying this note verify finite coordinates, areas squared, volumes, pair distances, affine vertex bounds, trace samples, and the algebraic obstruction. They are diagnostics supporting the written arguments, not a formal proof of geometric measure theory or global minimality.
