# A published negative answer to OWR-3388-006

## Disposition and exact target

The answer to problem 30001148 is **no**. This is a recovery and verification of published counterexamples, not a new mathematical discovery. The unrestricted question was already answered negatively by Colliot-Thélène, Parimala and Suresh, *Lois de réciprocité supérieures et points rationnels*, Transactions of the AMS 368 (2016), 4219–4255, DOI [10.1090/tran/6519](https://doi.org/10.1090/tran/6519), Corollary 5.3 and Example 5.6(a) in [arXiv:1302.2377v3](https://arxiv.org/abs/1302.2377).

The original contribution by Colliot-Thélène in [OWR 05/2009](https://doi.org/10.4171/OWR/2009/05), printed pp. 317–318, asks about arbitrary connected linear groups, arbitrary homogeneous spaces, and **all nontrivial rank-one discrete valuations of F**, not necessarily trivial on the complete discretely valued base field K. It imposes neither projectivity on the homogeneous space nor finiteness on the residue field. Its title mentions p-adic curves, but the question itself is broader.

Below are two credited ways to see the negative answer. The second includes elementary hypothesis checks for fully specified fields and a torus. Both use established theorems for the arithmetic obstruction. These inputs are explicitly identified rather than silently re-proved or claimed as original.

## 1. Direct application of the 2016 counterexample

Set A = C[[t]], K = C((t)), and let C/K be the smooth projective elliptic curve whose affine equation is

    y² = x³ + x² + t³.

Let F = K(C). Its regular minimal model over A has special fiber of type I₃: three projective lines forming a triangle. This is CTPS Lemma 5.5 and Example 5.6(a). The cubic discriminant is -t³(4 + 27t³), which is nonzero in K, so its generic smoothness also follows directly.

CTPS Corollary 5.3 supplies a torus torsor E/F with E(F) empty and E(F_v^h) nonempty for **every** rank-one discrete valuation v, where F_v^h denotes the henselization. Concretely its equation has the form

    (X₁² - aY₁²)(X₂² - bY₂²)(X₃² - abY₃²) = c,

where a = π₂π₃, b = π₃π₁, c = π₁π₂π₃, and the nonzero functions π_i are chosen with the divisor-avoidance conditions in CTPS §5.2. These are existence choices supplied by the theorem; no unverified explicit π_i is substituted here.

To check that this is within the target's group class, take the product of the three Weil restrictions of G_m from the quadratic étale algebras defined by a, b, ab, and take the kernel G of the product of their norms to G_m. After a separable closure, this map is multiplication of six coordinates. Its kernel is G_m^5. Thus G is a smooth connected linear F-torus and the nonzero norm fiber E is a G-torsor. It is geometrically integral, has trivial geometric stabilizer, and is a homogeneous F-variety.

Every henselization embeds over F in the corresponding completion: a complete discrete valuation field is henselian. Hence E(F_v^h) nonempty implies E(F_v) nonempty. The theorem therefore gives precisely

    E(F) = ∅,     E(F_v) ≠ ∅ for every nontrivial rank-one discrete v of F.

The use of all valuations, rather than just the horizontal places of C, is part of the cited corollary. This alone resolves the stated question.

## 2. A constant-torus example with elementary parameter checks

Here the supporting arithmetic theorem is from Colliot-Thélène, Harbater, Hartmann, Krashen, Parimala and Suresh, *Local-global principles for tori over arithmetic curves*, Algebraic Geometry 7 (2020), 607–633, DOI [10.14231/AG-2020-022](https://doi.org/10.14231/AG-2020-022), [publisher PDF](https://content.algebraicgeometry.nl/2020-5/2020-5-022.pdf). Write CHHKPS for this paper.

Choose

    k = C((u))((v)),     R = k[[t]],     K = k((t)),
    L = k(√u, √v),      T = R¹_{L/k} G_m,
    X = Proj R[x,y,z] / (xyz - t(x+y+z)³),
    F = K(X_K).

Thus both K and its residue field k have characteristic zero; K carries its t-adic complete discrete valuation. The symbols u,v,t are independent. The torus T is extended from k to R, X, and F as required. It has dimension three.

### 2.1 The base and the model

The classes of u and v are independent in k×/k×². Indeed, if u^ε v^δ is a square, with ε,δ in {0,1}, then the v-adic valuation forces δ=0. The residue of a square of v-valuation zero is a square in C((u)); its u-adic valuation then forces ε=0. Consequently [L:k]=4, with Galois group C₂×C₂, and T is a connected torus.

The generic plane cubic H=xyz-t(x+y+z)³ is geometrically smooth. At a hypothetical projective singular point put s=x+y+z. The equations H_x=H_y=H_z=0 say yz=xz=xy=3ts². If s=0, at most one coordinate is nonzero, contradicting s=0. Otherwise all three coordinates are nonzero, x=y=z, and the equations force 27t=1, impossible in k((t)). A smooth plane cubic is geometrically integral: distinct positive-degree components of a plane curve over an algebraically closed field intersect, making their union singular. Thus F is a one-variable regular extension of K; in particular K is algebraically closed in F.

The displayed projective R-model is flat because its defining equation has nonzero reduction xyz modulo t, so its quotient coordinate rings have no t-torsion. Its generic fiber is integral, so flatness also gives integrality of the total model. The closed fiber is the union of x=0, y=0, z=0, three copies of P¹_k, meeting at the three distinct k-rational coordinate vertices. Off those vertices the fiber is smooth, and the total scheme is regular there. At a vertex, for example [0:0:1], the local equation is xy-t(x+y+1)³; the coefficient of t in its linear term is -1. Its local hypersurface ring is therefore regular, and the two fiber branches meet normally. Hence X is a regular normal-crossings model.

The dual graph is a triangle. The patching reduction graph in CHHKPS §6.1 is its barycentric subdivision, a six-cycle; both have H₁(Γ,Z)=Z. Distinguishing the graphs avoids a harmless shorthand in their Example 8.7.

### 2.2 A nonzero residual obstruction

First, q=⟨1,u,-v⟩ is anisotropic over k. The binary form x²+u y² is anisotropic over C((u)): if both entries are nonzero their u-valuations have opposite parity, so cancellation is impossible. Over k, for (x,y) not both zero, its v-valuation is therefore 2 min(ν_v(x),ν_v(y)); equal leading valuations cannot cancel because the residual binary form is anisotropic. This is even, whereas ν_v(vz²) is odd when z is nonzero. Thus x²+uy²=vz² has only the zero solution.

For clarity one can verify the obstruction used in CHHKPS Example 8.1 algebraically. Let σ negate √u and fix √v, and τ negate √v and fix √u. Set

    N = ker(N_{L/k}:L× → k×),
    I_G L× = subgroup generated by g(w)/w, g∈G, w∈L×.

The element i=√(-1) in C has norm i⁴=1 and belongs to N. If i belonged to I_G L×, commutativity and the two generators would give

    i = (σ(r)/r)(τ(s)/s),   r,s∈L×.

Then θ=σ(r)/r has N_{L/k(√v)}(θ)=1 and N_{L/k(√u)}(θ)=-1. Write

    θ = A+B√u+C√v+D√(uv),  A,B,C,D∈k.

The constant terms of these two norm equations are

    A²+vC²-uB²-uvD² = 1,
    A²+uB²-vC²-uvD² = -1.

Their sum yields A²=uvD². Since uv is not a square, A=D=0. The first equation becomes 1+uB²-vC²=0, contradicting anisotropy of q. Therefore the class of i is nonzero in N/I_G L× = Ĥ⁻¹(G,L×).

We now invoke, rather than re-prove, the standard flasque-resolution identification stated in CHHKPS §8.1 (credit there to Colliot-Thélène–Sansuc 1977, Proposition 15): for a flasque resolution

    1 → S → Q → T → 1

of this norm-one torus, H¹(k,S) ≅ Ĥ⁻¹(G,L×). In particular H¹(k,S)≠0. The preceding calculation is a parameter verification of their published Example 8.1, not a novelty claim.

### 2.3 All valuations and the homogeneous space

For any F-torus define

    Sha(F,T) = ker[ H¹(F,T) → ∏_w H¹(F_w,T) ],

where w ranges over **all** nontrivial discrete valuations of F. This is CHHKPS §1.2's definition, not a restriction to a chosen model's codimension-one points or to valuations trivial on K.

CHHKPS Theorem 6.4(c), applied to the R-torus T and the model just checked, gives

    Sha(F,T) ≅ H¹(k,S),

since every component is P¹_k, every intersection is k-rational, and the graph has one cycle. Theorem 4.4 is the comparison that identifies the patching obstruction with this all-valuations Sha for a torus extending over the model. It applies here because T is already defined over R. Thus Sha(F,T)≠0.

Choose a nonzero class ξ in Sha(F,T) and let Y be its T_F-torsor. The usual torsor/cohomology correspondence says Y(F)≠∅ if and only if ξ=0, and Y(F_w)≠∅ if and only if ξ restricts to zero in H¹(F_w,T). By construction,

    Y(F)=∅,    Y(F_w)≠∅ for every w.

Over a separable closure, Y becomes G_m³. In particular it is a smooth geometrically integral affine homogeneous space of the connected linear group T_F, with trivial geometric stabilizer. This is a complete existence counterexample with specified F and T. An explicit equation or chosen cocycle for Y is not provided or needed for the existential negation; its existence follows from the nonzero cohomology class and the cited arithmetic theorem.

## Scope and limitations

- The 2016 route already works with algebraically closed residue field C. The more elementary parameter audit of the constant-torus route uses the larger residue field C((u))((v)). Neither field K is a finite extension of Q_p.
- The constructed Y is affine and positive-dimensional. It is not a projective homogeneous space. A compactification would not automatically remain homogeneous. No negative answer to a projective-homogeneous or p-adic-specific conjecture is asserted.
- Trivial stabilizer is in particular smooth and connected, so adding only connectedness of the stabilizer would not repair the unrestricted statement.
- The original report's rational-group positive case included a reductive group extending over the valuation ring and a principal homogeneous space. It cannot be applied after dropping its rationality hypothesis.
- Linh's 2024 paper, DOI [10.1112/jlms.12842](https://doi.org/10.1112/jlms.12842), treats a different refined obstruction and class of stabilizers; its standard places are closed points on the generic p-adic curve. It does not establish the unrestricted assertion or invalidate these earlier counterexamples.
- The finite/symbolic checker supports algebra and graph bookkeeping. It does not enumerate valuations, construct the global torsor, prove the cited patching theorem, or replace the mathematical argument.

One substantive reconstruction turn suffices because the exact original yes/no question has a known negative answer. Further speculative attempts are unnecessary. Independent adversarial review of this packet is still required before publication.
