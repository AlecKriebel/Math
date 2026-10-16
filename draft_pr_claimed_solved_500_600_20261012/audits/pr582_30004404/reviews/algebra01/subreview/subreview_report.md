# Independent algebra subreview: PR582 / problem30004404

Review timestamp: 2026-10-15 05:25:57 UTC. Completion estimate: 100% of the assigned independent algebra checks.

## Scope and verdict

**PASS for the algebraic obstruction and formulas proved below.** Every homomorphism from a nonabelian free group to a metabelian group has nontrivial kernel. For the filling application, only the single admissible map q0 is assumed to have metabelian target. Thus, for every nonabelian free subgroup H of the ambient group,

    {1} != H'' <= ker(q0 restricted to H)
                = H intersect ker(q0)
                <= H intersect (union over admissible r of ker(q_r)).

This suffices to disprove trivial intersection with the union. It does **not** assert that H'' is killed by any other filling q_r whose target has not been proved metabelian. No conclusion about the intersection of all filling kernels is asserted.

No candidate, older verdict, or sibling review was read. No Git mutation, remote action, or external outreach was performed. The check is an independent algebra subreview, not a claim of novelty.

## 1. Explicit nontrivial word in F(x,y)''

Use [a,b] = a b a^-1 b^-1. Let c = [x,y] and d = x c x^-1. Since the derived subgroup is normal, c and d belong to F(x,y)'. Therefore W = [c,d] belongs to F(x,y)''.

Write X = x^-1 and Y = y^-1. Direct free reduction gives

    c = x y X Y,
    d = x x y X Y X,
    W = x y X Y x x y X Y X y x x Y X X.

The displayed word has 16 letters and no adjacent inverse pair. The normal-form theorem for a free group therefore gives W != 1. The executable control independently constructs [c,d], reduces the 20-letter concatenation, and checks this exact 16-letter output.

For any homomorphism phi: F(x,y) -> G with G'' = {1}, functoriality gives phi(F(x,y)'') <= G'' = {1}. Equivalently, phi(c) and phi(d) lie in the abelian group G', so phi(W) = 1. Consequently W is a nonidentity kernel element. No assumption that the images of x and y generate G is required.

## 2. Intrinsic bases and all-H quantifiers

If H is an abstract free rank-two subgroup, choose a free basis u,v of H and substitute u,v into W. The free-group isomorphism x -> u, y -> v proves W(u,v) != 1 in H. Merely inserting ambient generators would not establish membership in H; merely choosing two arbitrary elements of H would not establish freeness.

If H has larger free rank, take any two distinct members of a free basis. They freely generate a rank-two subgroup, so the same witness is nontrivial and lies in H''. The statement is consequently valid for every nonabelian free H, regardless of its embedding in the ambient group.

Let q_r: Gamma -> G_r be the admissible filling maps, and suppose that q0 is one of them with G0 metabelian. For every such H <= Gamma, q0 restricted to H kills H'', and H'' is nontrivial by the preceding witness. Thus one admissible metabelian filling obstructs the proposed union avoidance for every H. The witness may depend on the free basis of H; it need not be an ambient generator word chosen uniformly for all H.

Logical distinction: H intersect (union_r ker q_r) = {1} is equivalent to every restriction q_r|H being injective. To refute it one needs one admissible noninjective restriction. In contrast, a statement about the intersection of the kernels has different quantifiers and is unnecessary here.

Boundary conditions: the argument requires H to be nonabelian free, q0 to be a group homomorphism, q0 to be in the allowed family, and its target to be metabelian. It does not apply to an arbitrary two-generated group in which W may already equal 1, or to cyclic H. The verification that the actual filling q0 satisfies this application interface belongs to the parent review.

## 3. Semidirect products for every A in GL(2,Z)

Use column vectors and the convention t(v,0)t^-1 = (Av,0), where t = (0,1). In Z^2 semidirect_A Z, for v,w in Z^2 and n,m in Z,

    (v,n)(w,m) = (v + A^n w, n+m),
    (v,n)^-1  = (-A^-n v, -n).

The inverse is valid on both sides because A is unimodular, so every positive or negative power preserves Z^2. Associativity follows directly from A^(n+m) = A^n A^m.

Expanding the four factors under the stated commutator convention gives

    [(v,n),(w,m)] = ((I-A^m)v + (A^n-I)w, 0).

In particular every commutator lies in the abelian subgroup Z^2 times {0}, proving that the entire group is metabelian.

More precisely, set

    S_n = sum_(j=0)^(n-1) A^j           if n > 0,
          0                             if n = 0,
          -sum_(j=1)^(-n) A^-j         if n < 0.

Then A^n-I = (A-I)S_n for all integers n. Hence each commutator vector belongs to (A-I)Z^2. Conversely,

    [t,(w,0)] = ((A-I)w,0),

so the derived subgroup is exactly (A-I)Z^2 times {0}. It is abelian, including when A-I is singular or zero.

No step divides by A-I, diagonalizes A, assumes an eigenvalue condition, or requires determinant +1. Thus identity, finite-order, unipotent, negative-unipotent, hyperbolic, and orientation-reversing matrices are all covered. A finite-order matrix does not make t finite order: the quotient in this torus-bundle group remains Z. If an alternative action convention is used, replace A by A^-1 consistently; the metabelian conclusion is unchanged. If det(A) is not +/-1, these negative-exponent formulas do not in general define a semidirect product on the lattice Z^2.

The same metabelian proof works for an abelian rational vector fiber, provided the stated action really is an automorphism and the maps in question are homomorphisms.

## 4. Fresh exact controls and limitations

Run the adjacent validate_algebra.py with Python 3; it uses only the standard library and writes controls_result.json.

Ten matrices cover identity; orders 2, 4, and 6; two orientation-reversing involutions; unipotent and negative-unipotent examples; and hyperbolic examples of determinants +1 and -1. Heights in the element tests range from -4 to +4. All arithmetic is exact integer arithmetic.

Results:

- 10 two-sided matrix-inverse checks.
- 170 Laurent-sum factorizations, for exponents -8 through +8.
- 450 two-sided group-inverse checks.
- 4,050 associativity triples.
- 20,250 direct commutator-formula checks.
- 20,250 evaluations of the explicit F'' witness, all equal to the identity.

All checks passed. These finite checks supplement the universal proofs; they do not substitute for them. The strongest verified result is the unconditional free-group/metabelian theorem together with the universal semidirect formulas. The exact remaining application check is that the particular admissible q0 is a homomorphism into the advertised metabelian torus-bundle target. Other filling targets have not been assumed or checked to be metabelian.
