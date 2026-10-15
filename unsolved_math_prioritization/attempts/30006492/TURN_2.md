# Author turn 2: Fourier equivalence after guitar locality fails

**Partial; both general source questions remain unresolved.** 2026-10-01.

This turn tests whether a failed guitar conjugator or a nonisomorphic set action provides a counterexample to the source's *linear representation* question. An explicit family shows that neither test is sufficient: a Fourier transform supplies a genuine all-strand complex linear equivalence even when no relevant set-action bijection exists in the three-color case.

## 1. A linear welded pair and its actual derived rack

On X=F_p for an odd prime p, define

    r(x,y)=(2x+y,−x),     s(x,y)=(−y,−x).

Both are bijective and nondegenerate; r is the Alexander solution with parameters 1 and −1. They satisfy the virtual relation and welded relation (1) of TURN_1. These statements can be verified as identities of integral matrices on triples, so are valid after reduction modulo any p. The pair is also Reidemeister-I compatible: each x has the unique fixed mate y=−x.

The left-action guitar convention at n=2 is J_2(x,y)=(x,2x+y). Direct conjugation gives

    J_2 r J_2^(-1)(x,y)=(y,−x+2y)=r′(x,y).

Thus r′ is precisely the dihedral rack-derived solution, not the violin-derived first component. The pair (r′,s) is itself welded in the same convention, again by integral triple-matrix identities. The conjugator used below leaves the second component q=s.

## 2. All-n complex linear equivalence

Write the two-coordinate matrices as

    M = [[2,1],[-1,0]],       M′ = [[0,1],[-1,2]],
    S = [[0,-1],[-1,0]].

Then M′=M^(-T) and S=S^(-T). Their adjacent-coordinate embeddings in GL_n(F_p) have exactly the same identities. Let omega be a primitive pth root of unity in C. On C[F_p^n], define the unnormalized finite Fourier map

    F e_x = sum_(y in F_p^n) omega^(x dot y) e_y.

It is invertible by character orthogonality (its inverse has coefficients p^(-n)omega^(−x dot y)). For any A in GL_n(F_p), direct relabeling of the summation gives

    F P_A = P_(A^(-T)) F,

where P_A e_x=e_(Ax). Applying this to every adjacent M and S shows that F intertwines all generators of the two welded-braid representations. Hence the source Q2 has an affirmative answer for this family for every n over C. The same proof works over any coefficient field of characteristic different from p containing the required pth roots, and more generally after a suitable scalar extension. No characteristic-p conclusion is inferred.

This is a representation-theoretic isomorphism, generally not a basis permutation, a diagonal gauge, or a local two-color relabeling. The mechanism is the standard finite Fourier duality, credited here rather than claimed as new.

## 3. Three-color set-action obstruction

At p=3 the original pair is

    r(x,y)=(y−x,−x),   s(x,y)=(−y,−x),
    r′(x,y)=(y,−x−y).

An exhaustive own-code enumeration of all permutations of X² first checks bijectivity, nondegeneracy, involutivity and the YBE; it then checks both compatibility identities. The only nondegenerate involutive partners q making (r′,q) welded in this convention are

    q_c(x,y)=(c−y,c−x),   c in F_3.

This finite classification is reported only for |X|=3 with those explicit axioms. It is not a general classification of welded pairs and uses no external census or downloaded program.

The original WB_3-action has exactly three points fixed by every generator: (a,−a,a), a in F_3. For the target (r′,q_c), the two r′ generators force all coordinates to be equal, and q_c then forces 2a=c. Thus precisely one basis point is fixed by every generator. Consequently no equivariant *set bijection* to any of these three local target pairs exists. This does not contradict Section 2: the complex linearizations are equivalent.

For q_0=s the original set-action orbit sizes are 1,24,1,1, whereas the target orbit sizes are 1,9,9,8. Both have four orbits, consistent with equal dimensions of invariant vectors in their complex permutation modules. The failure to preserve the number of globally fixed basis points is not an invariant of abstract complex representations.

## 4. The chosen guitar map is genuinely nonlocal

For the standard left-action guitar map on triples,

    J_3(x,y,z)=(x,2x+y,2x+2y+z),

transporting s_1 changes even the third coordinate: on a direct calculation the new third coordinate differs by −4x−4y in the original input variables. Equivalently, in the target coordinates (u,v,w), J_3 s_1 J_3^(-1) changes w to w+4u−4v. At p=3 this can be nonzero. Such an operator cannot be q_1 for any local q, which must leave the third coordinate unchanged.

For example target input (u,v,w)=(0,1,0) changes its third coordinate to 2. This is a real locality failure, not merely a slot-dependent weight. Nevertheless the Fourier operator gives a different, nonmonomial intertwiner for all n. Therefore this locality failure must not be promoted to a negative answer to Q2.

## 5. Exact diagnostic scope

The own finite enumeration finds 4 nondegenerate YBE solutions and 2 involutive ones on two colors, and 66 and 12 respectively on three colors. It finds 228 welded pairs on three colors for each of the two forbidden-move orientations; in each orientation 222 have a local chosen guitar transport and 6 do not. These figures are computation results within the declared finite axioms, not imported catalog claims.

For the displayed three-color example, enumerating the 432 elements of the joint permutation image gives equal integer characters for the source and all three compatible target partners. This is an exact finite check; Section 2's explicit Fourier formula, rather than a search cutoff, supplies the all-n theorem for q_0. The other forbidden-move orientation was used as a convention control and is not silently mixed into the theorem.

The full source Q1 concerns 2-cocycle enrichments; none of the unweighted Fourier argument shows that a weighted operator is Fourier conjugate to a *local monomial* weighted pair. Fourier conjugation usually destroys monomial form. Q2 remains unresolved for general pairs. The next mechanism should inspect coefficient-field and weighted-locality obstructions with invariant tests valid for the actual stated representation category.

Substantive author turns: 2/5. Completion estimate20% toward the full two-question target. No full counterexample, no novelty claim, and no substitution of set actions for linear representations.
