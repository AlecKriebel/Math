# Turn 5: determinant formulation and an exact stability obstruction

Final author turn. The original conjecture remains unresolved after5/5 turns. The strongest structural partial is the all-cactus theorem in Turn2, conditional only on its explicitly credited published cycle theorem. This turn examines an independent algebraic route.

## 1. A cancellation-free coefficient formulation

Give each arc in color i weight z_i. Define the incoming Laplacian L(z) by L_vv=Σ_{u→v}z_color(u→v) and L_vu=−Σ_{u→v}z_color(u→v) for u≠v. Parallel colored arcs each contribute. For a root r, delete row and column r to obtain L^(r). Then

P(z)=Σ_{r∈V}det L^(r)(z)

is the spanning out-arborescence generating polynomial, counting all roots. This is the standard directed matrix-tree identity; the following argument fixes orientation and gives the needed self-contained justification.

Expand a minor multilinearly in its rows. For each v≠r, choose one entering arc u→v, contributing its weight and row e_v−e_u, with e_r interpreted as zero after deletion. If the chosen parent function contains a directed cycle, the corresponding rows along that cycle sum to zero, so the determinant vanishes. Otherwise every parent chain ends at r. Ordering vertices by distance from r makes the row matrix triangular with diagonal1, so its determinant is1. Exactly the rooted spanning out-trees survive. Thus P has nonnegative integer coefficients and homogeneous degree q=n-1.

The coefficient [z_1⋯z_q]P is exactly the number of rainbow spanning out-arborescences. The original conjecture is equivalent to positivity of this coefficient on every promised instance. This is a reformulation, not a proof of positivity.

There is an exact finite inclusion-exclusion formula:

[z_1⋯z_q]P = Σ_{S⊆[q]}(-1)^(q-|S|) P(1_S).

For a monomial with support T, the inner alternating sum vanishes unless T=[q]. A degree-q monomial supported on all q variables must have exponent1 in every variable. This proves the identity. It yields an exponential coefficient test; it does not produce a sign argument for the alternating sum.

## 2. Small valid instance where real stability fails

Take V={0,1,2} and two color trees

A_1={a:0→1, b:1→2}, A_2={c:2→1, d:1→0}.

The union's underlying simple graph is just a path. Its spanning out-arborescences are exactly {a,b}, {b,d}, {c,d}, with roots0,1,2. The individual-arc polynomial is

F(a,b,c,d)=ab+bd+cd.

A real polynomial is real stable if it is nonzero whenever every variable has strictly positive imaginary part. At

a=2+i, b=1+i, c=−2+i, d=−1+i,

we have ab=1+3i, cd=1−3i and bd=−2, so F=0, although all four imaginary parts are1. Hence F is not real stable.

After identifying each color's arc variables, P(x,y)=x²+xy+y² is also not real stable: take x=√3+i and y=−√3+i. Then x+y=2i and xy=−4, so P=(x+y)²−xy=0. The rainbow coefficient is nevertheless1, realized by {b,d}. This is a counterexample to a proposed stability premise, not to the rainbow conjecture.

## 3. The associated matroid shortcut also fails

The same two spanning arborescences B_1={a,b}, B_2={c,d} violate the basis-exchange axiom for the family of all spanning out-arborescences. Remove b from B_1. Adding c gives two arcs entering vertex1; adding d gives a directed2-cycle on0,1 and leaves2 isolated. Neither is an arborescence. Since B_1,B_2 are valid bases of the putative rank2 family, this disproves the matroid premise needed to apply a single-matroid independent-transversal theorem directly. This elementary obstruction is not claimed novel; arborescences are already treated via matroid intersections in the primary literature.

One could still seek another polynomial, another representation, or a specialized inequality not requiring stability. The obstruction only rules out real stability of the natural all-root generating polynomial and the single-matroid interpretation of its supports.

## 4. Final remaining gap

Determinant minors give exact counting, but their alternating subset sum has no established positive lower bound for the general promised instance. Positivity of all evaluations on the positive orthant and the presence of each monochromatic monomial do not suffice as abstract coefficient conditions: Σ_i z_i^q has those properties and no full rainbow monomial when q≥2. That abstract polynomial is not asserted realizable by an input graph.

Combining the turns: source components and articulations can be removed, and all cactus graphs are covered using credited cycle theory. Exact core quotas tell when repeated projected roots are controllable. At a two-vertex separator the missing issue is colorful state compatibility. For irreducible strongly connected, biconnected instances, neither that compatibility nor the determinant coefficient's positivity is proved. These are the final gaps; no sixth author search is included.

## 5. Reproducibility

`python verify_turn5.py` implements integer Laplacian minors and inclusion-exclusion, compares their coefficient with direct rainbow counting on exact finite instances, and checks the stability and basis-exchange counterexamples. No floating-point evidence is used for the displayed zero. These finite controls do not extend the previously published small-order search or certify novelty.
