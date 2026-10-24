# Independent construction family — Kourovka 21.135

Target: finite groups G,H with identical **multisets** of complex irreducible character degrees, R(G)=1 and R(H)>1. No such pair has been constructed. All exclusions below concern specified mechanisms; they do not settle the target or establish originality.

## 1. Direct products and cancellation

For a finite group X put

    D_X(s) = sum_{chi in Irr(X)} chi(1)^(-s).

This is a finite Dirichlet polynomial. The irreducibles of X x Y are the tensor products, so D_(X x Y)=D_X D_Y. Equality for all real s is equivalent to equality of the multisets: a nonzero finite difference has a least integer degree d with nonzero coefficient, and multiplication by d^s followed by s -> +infinity recovers that coefficient.

**Cancellation.** If the degree multisets of A x K and B x K are equal, those of A and B are equal. Indeed D_K(s)>0 for every real s, so cancel it pointwise and apply the preceding uniqueness argument. Equivalently, identify an integer degree with its unique prime factorization and use the integral domain Z[x_p : p prime].

Moreover R(X x Y)=R(X) x R(Y). One inclusion follows because the product on the right is a solvable normal subgroup; the reverse follows by projecting any solvable normal subgroup to the two factors. Thus adjoining a common factor to a known mismatching pair cannot repair the mismatch or manufacture a radical-free/radical-nontrivial pair from a pair without the same distinction. This route is blocked unless a genuinely new polynomial identity between different factors is found.

## 2. Regular prime cyclic wreath products do not erase a mismatch

Let p be prime and W_p(X)=X^p semidirect C_p, where C_p cyclically permutes all p coordinates. Its irreducible degrees can be obtained directly from Clifford theory.

- A constant tuple (chi,...,chi) of base characters is invariant. Its tensor representation extends to the wreath product by cyclically permuting tensor factors. It has p extensions, all of degree chi(1)^p.
- Every nonconstant tuple has a free orbit of size p. Induction gives one irreducible for each such orbit, of degree p times the product of the p tuple degrees. There are no other irreducibles.

Consequently, for z=p^(-s),

    D_(W_p(X))(s) = p D_X(ps) + (z/p) [D_X(s)^p - D_X(ps)].       (1)

**Injectivity.** For any two finite groups X,Y, equality of degree multisets of W_p(X),W_p(Y) implies equality for X,Y.

Write F(s)=D_X(s)-D_Y(s). If nonzero, F(s) and F(ps) have the same fixed nonzero sign for all sufficiently large positive s, by the least-degree coefficient argument. Subtracting (1), multiplying by p, and factoring a difference of pth powers gives

    0 = z Q(s) F(s) + (p^2-z) F(ps),
    Q(s) = sum_{i=0}^{p-1} D_X(s)^(p-1-i) D_Y(s)^i > 0.

Both coefficients zQ(s) and p^2-z are strictly positive for positive s, so the two terms have the same nonzero sign. Contradiction.

This proof includes groups with arbitrary numbers of linear characters, the trivial group, and p=2, where coincident contributions at degree 4 must not be separated incorrectly.

**Radical behavior.** For a nontrivial finite X and any faithful permutation group P on a nonempty finite set Omega,

    R(X wr_Omega P)=1 if and only if R(X)=1.

If R(X)>1, the coordinate product R(X)^Omega is nontrivial solvable normal. Conversely suppose R(X)=1. Then S=Soc(X) is a direct product of nonabelian simple groups and C_X(S)=1: a nontrivial centralizer, being normal, would contain a minimal normal subgroup of X, which lies in S but also in Z(S)=1. The coordinate subgroup T=S^Omega is normal in the wreath product. A solvable normal subgroup A intersects T trivially, since A intersect T is solvable normal in a direct product of nonabelian simple groups. Therefore [A,T] is trivial. An element centralizing T must fix every coordinate, by faithfulness of the permutation action, and each of its base coordinates belongs to C_X(S)=1. Thus A=1.

The qualification X!=1 is necessary: the wreath product of the trivial group is P itself.

Combining injectivity with radical behavior shows that applying the same regular prime cyclic wreath construction on both sides cannot provide a counterexample unless one already had a counterexample among the bases. Iterating such operations has the same limitation. This is an exact mechanism exclusion, not a solution of 21.135.

## 3. Abelian replacement in a fixed permutation wreath construction

Assume Omega is nonempty. The number k(X wr_Omega P) depends on the number k(X) of irreducible characters of X, and on the action of P on Omega, but not on the degrees of those characters. For each P-orbit of labelings f:Omega -> Irr(X), its stabilizer P_f acts by permuting equal tensor factors; the representation extends by those tensor permutations. The irreducibles above that orbit correspond to Irr(P_f). Thus

    k(X wr_Omega P) = sum_{f modulo P} k(P_f).                    (2)

If k(X)<k(Y), identify Irr(X) with a proper subset of Irr(Y). The old labeling orbits and their contributions persist unchanged, and at least one constant labeling by a new color supplies a new orbit. Therefore (2) strictly increases with k(X).

In particular, replacing a nonabelian base X by an abelian group A of the **same order**, while keeping the same faithful permutation group/action, cannot preserve both order and the degree multiset: k(A)=|X|>k(X), so the number of irreducibles strictly increases. The same reasoning rules out replacing just some invariant collections of base coordinates by equal-order abelian bases whenever the stabilizer formula remains the stated ordinary permutation action.

The general group extension problem has arbitrary actions and character obstructions; neither (1) nor (2) has been applied to those without proof.

## 4. Candidate families and actual gaps

- Products of simple groups are potentially viable sources, but simple-group recognition does not tensorize automatically. Distinct-factor polynomial identities are being tested; common-factor stabilization is excluded by Section 1.
- A nontrivial central cover of a simple group is not radical-free and has different degree data from the simple group. For SL_2(5), the central-character contributions create degrees 2 and 6. For the equal-order comparison between A_5 wr C_2 and the central product SL_2(5) circle SL_2(5), the former has two linear characters and the latter is perfect with one; this mismatch already rules it out.
- In affine groups V semidirect K with V abelian, characters are controlled by K-orbits on Irr(V) and characters of the stabilizers. Making V normal solvable is easy; matching all orbit indices and stabilizer degree multiplicities to a radical-free group is the unresolved step. An equality of degree sets or of a few moments would be inadequate.
- For permutation extensions of S^n, replacing the base by an equal-order abelian group fails by Section 3. Moving a solvable permutation-top factor into a normal radical changes the orbit/stabilizer data; no identity equating the two spectra was found.

## 5. Finite computational scope

The accompanying GAP library scan and exact Python product scan test ordinary character tables from CTblLib 1.3.11 and unordered products of two listed factors. Their exact scope, input hash, count, and results are in artifacts/product_scan_results.json. The library is not a classification of all finite groups up to the order bound; its failure to contain a collision cannot prove the target. The direct product radical computation is justified in Section 1, and each individual table's radical order is computed from its full class-value information by GAP's ClassPositionsOfSolvableRadical, not inferred from the degrees.

All results remain partial research evidence. The complete statement of 21.135 is unresolved here.

## 6. A tempting multiplicity-content invariant is false

A radical-free finite group need not have gcd of its degree multiplicities equal to one. An explicit counterexample to that proposed invariant is

    E = {(a,b) in S_5 x S_5 : sign(a)=sign(b)}.

It has order 7200 and trivial radical: both coordinate projections onto S_5 are surjective, and the image of a solvable normal subgroup under either projection is solvable normal in S_5, hence trivial.

View E=(A_5 x A_5) semidirect C_2, with the outer involution simultaneously interchanging the two degree-three characters of each A_5. The invariant character labels have degrees 1,4,5. Tuples of two invariant labels have two extensions each. Tuples with precisely one degree-three label have one induced character per two-element orbit. The four tuples of two degree-three labels form two orbits. This gives the full exact degree data

    1:2, 4:4, 5:4, 6:2, 16:2, 18:2,
    20:4, 24:2, 25:2, 30:2.

All multiplicities are even, and their gcd is exactly two. The squares sum to 7200. This agrees with the library table labelled (A5xA5):2. The separate check_diagonal_outer.g constructs E as an actual permutation group on ten points, computes its degrees and solvable radical without a CTblLib lookup, and confirms the same data (artifacts/diagonal_outer_check.json). Dividing this polynomial by two produces an integral positive polynomial, but that alone does not make the quotient the degree data of any finite group. No such realization is asserted.

Three other catalog pairs match order, linear count, and degree SET but differ in multiplicities. They are preserved by set_near_misses.py. For q=25, the radical-free table L2(25).2^2 and the radical-order-two table Isoclinic(L2(25).2_3x2) have common degree set {1,25,26,48,52}; their multiplicities at 26 are respectively 6 and 14 and at 52 respectively 4 and 2. They therefore do **not** solve the problem. The q=49 and q=81 analogues fail in the same way.

## 7. Exploratory unbounded-product factor screen: verification gap retained

For 1716 distinct catalog spectra, Sympy 1.14.0 produced factorizations of the associated polynomials in variables indexed by primes. Every factorization was exactly reconstructed using ordinary integer sparse convolution. There are 208 distinct proposed primitive factors among the 217 radical-free spectra. Of the 1499 other spectra, 1400 have at least one proposed factor absent from the radical-free list. The remaining 99 have only old factors, but have an integer scalar penalty greater than one relative to the consistent radical-free contents. Details are in artifacts/exploratory_factor_report.json.

If every proposed factor is irreducible over Q, unique factorization would exclude equality between arbitrary products of catalog radical-free spectra and products containing at least one catalog nontrivial-radical spectrum. However, exact reconstruction by itself does not certify irreducibility. Independent irreducibility certificates were not supplied, so this stronger arbitrary-product exclusion is **not promoted as a verified result**. The independently reproduced bounded two-factor search in Section 5 remains the verified computational statement.

The finite catalog is in any event not a classification of all finite groups, so even a completed unbounded-product screen would leave arbitrary semidirect extensions and other groups outside the input unresolved.
