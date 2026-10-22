# Turn 4: the higher-two-primary correction is a real presentation problem

**Original unrestricted target remains unresolved.** This turn attacks the missing higher-two-primary structures through characteristic surgery data. It derives exact correction laws and a concrete failure on one fixed lens-space Spin^c structure. No assumption of connected-sum additivity is used in these calculations.

## 1. Characteristic vectors and the rational signature defect

Let L be an oriented framed surgery link with nonsingular integral symmetric linking matrix B. A characteristic vector c has c_i≡B_ii modulo2, and its class modulo2B Z^n specifies a Spin^c structure on the rational homology boundary, by Deloup–Massuyeau's Spin^c Kirby theorem. In the positive discriminant convention put

    q_(B,c)([x])=(xᵀBx-cᵀx)/2 modulo1,
    D(B,c)=signature(B)-cᵀ B^(-1)c,

where x ranges over B^(-1)Z^n/Z^n. Boundary conventions may negate q and D together, as explained in Turn2.

**Lemma 4.1.** The Gauss–Brown invariant of q_(B,c) equals D(B,c) modulo8.

**Proof.** Choose an integral Wu vector w with Bw≡diag(B) modulo2. Such w exists: over F2, a vector y in ker(B) satisfies diag(B)·y=yᵀBy=0, so diag(B) is orthogonal to the kernel and hence lies in the image of the symmetric matrix B. Write c=Bw+2z with z integral and put t=B^(-1)z.

The homogeneous discriminant function q_(B,Bw) has Brown invariant signature(B)-wᵀBw by the classical van der Blij formula, stated as formula(18) in Massuyeau's spin paper. The affine change of c shifts q by the character -b(t,-). Completing the square as in Turn2 changes the Brown invariant by -8q_(B,Bw)(t). Therefore it becomes

    signature(B)-wᵀBw-4zᵀB^(-1)z+4wᵀz.

Its difference from D(B,c) is8wᵀz, an integer multiple of8. This proves the lemma. ∎

This calculation supplies a rational lift modulo8. It does not prove that the same signature defect is an invariant modulo16.

## 2. Exact representative-change parity

Replacing c by c+2Bz leaves the Spin^c boundary structure unchanged. Direct expansion gives

    D(B,c+2Bz)-D(B,c)=-4(cᵀz+zᵀBz).             (1)

The parenthesis is even because c is characteristic. Define

    rho_(B,c)(z)=(cᵀz+zᵀBz)/2 modulo2.           (2)

Then the change in (1) is -8rho modulo16. The parity is not always zero.

**Lemma 4.2.** The representative-change function satisfies the exact cocycle identity

    rho_(B,c)(z+w)
      =rho_(B,c)(z)+rho_(B,c+2Bz)(w) modulo2.     (3)

**Proof.** Before reduction modulo2, the cross term in the left side is zᵀBw. The same cross term appears when c+2Bz replaces c in the final term on the right. The two integer expressions are equal. ∎

Thus the ambiguity is controlled, but a correction is needed. A proposed formula

    F(L,c)=D(B,c)+8 e(L,c) modulo16

with e∈Z/2 must obey

    e(L,c+2Bz)-e(L,c)=rho_(B,c)(z).               (4)

A correction depending only on the boundary quadratic isometry class cannot obey (4) whenever rho is nonzero, because that class is unchanged by the representative change. A numerical choice reducing D to a fixed interval can obey it, but simply recovers a branch of the degree-zero Brown invariant; it does not generate new topology.

## 3. A fixed higher-two-primary example

Let M be the boundary of +4 surgery on an unknot, and use the characteristic vector c=2. Its Chern class is2 in Z/4, so this is one of the structures excluded from the odd-Chern theorem. The representative c'=10 gives the same Spin^c structure because c'-c=2B.

Yet

    D([4],2)=0,
    D([4],10)=-24=8 modulo16.

The finite quadratic function is unchanged. Indeed

    q_(4,2)(j)=(j²-2j)/8 modulo1

has values0,-1/8,0,3/8 for j=0,1,2,3, and its Gauss sum is exactly2. The terms with exponents -1/8 and3/8 cancel. Its Brown value is0 modulo8, so both proposed defects reduce correctly while disagreeing by8 modulo16. The parity rho_(4,2)(1)=3 is odd. This is a failure on the same manifold, same Spin^c structure and same surgery link, not merely on two unrelated lattice models.

There is also a concrete failure of the naive spin-origin extension. The two spin-induced structures have characteristic representatives0 and4. The classical characteristic-sublink formula gives their Rochlin values1 and-3, respectively: the relevant sublinks are empty or an unknot, both of Arf invariant0. This formula is reviewed in Kirby–Melvin, *Local surgery formulas*, printed pp.214–215.

For the target c=2, completion relative to the c=0 spin origin uses a=-1 in Z/4 and the correction q_0(a)=1/8. Relative to the c=4 spin origin it uses a=1 and q_1(a)=5/8 modulo1. If these scalars are lifted by their representatives in [0,1), the proposed values are

    1-8(1/8)=0,
    -3-8(5/8)=-8=8 modulo16.

Both reduce to the same Brown value, but the answer depends on the chosen spin origin. Negating the global quadratic convention still leaves the difference8. Thus the successful odd-primary construction does not extend by simply applying the same principal scalar rule to an arbitrary spin origin.

## 4. All Kirby requirements for a correction

The correction e may depend on the actual framed link, not only on B. The Spin^c Kirby theorem makes the following requirements explicit:

- Representative changes must obey (4).
- For a handle slide or an integral basis change, B'=PᵀBP and c'=Pᵀc. The signature defect is unchanged, so e must be unchanged under the corresponding link move and relabelling. Component reversals and reorderings are included.
- A standard stabilization by an e0-framed unknot, e0∈{+1,-1}, with characteristic label±1 changes D by zero, so the correction must remain unchanged.
- If the new characteristic label is any odd k, its change of D is e0(1-k²). The required change of the correction is e0(k²-1)/8 modulo2. This is compatible with representative changes, since all odd labels represent the unique Spin^c structure on that S3 factor.
- Link isotopy must leave e unchanged.

These laws are necessary and, together, sufficient for D+8e to descend to a Spin^c diffeomorphism invariant on rational homology spheres, by the cited Kirby theorem. They do not construct e. The presentation correction problem is therefore stated precisely, rather than presumed solved by a bounding four-manifold.

On the spin-induced part, the classical formula provides the correction. If c=Bw with w integral, let s be its coordinatewise reduction to0 or1 and let C_s be the characteristic sublink. Then

    R(M,s)=signature(B)-sᵀBs+8 Arf(C_s) modulo16,

so the correction for the possibly nonbinary representative w is

    e(L,Bw)=Arf(C_s)+(wᵀBw-sᵀBs)/8 modulo2.      (5)

The quotient is an integer because w=s+2z and Bs is characteristic. Omitting this additional quotient is another representative error: for the +1-framed unknot, c=1 and c=3 have the same spin boundary, while their uncorrected defects are0 and-8. The second term in (5) precisely repairs it. For c not in BZ^n, no integral characteristic sublink represents that Spin^c structure, so the spin Arf formula cannot simply be reused.

## 5. The degree-one test after descent

Consider any two-disjoint-Y-surgery cube of torsion-Chern Spin^c manifolds for which nonsingular surgery presentations are chosen at its four vertices. Write D_v for their rational defects and e_v for the corrections. Since the Brown invariant is degree zero, the alternating sum

    Delta2 D=D_empty-D_1-D_2+D_12

lies in8Z. The descended invariant is degree at most one on this cube exactly when

    e_empty-e_1-e_2+e_12 = -Delta2 D/8 modulo2.   (6)

This is an exact necessary-and-sufficient equation, independent of the chosen presentations once the Kirby laws hold. In a cube with coherent unchanged B,c it reduces to the ordinary zero second difference for e. No unproved assertion that every cube has such a simultaneous presentation is used.

Equations(4)–(6), supplemented by whichever normalization is actually required, isolate the missing parity data. The existing odd-Chern formula supplies a solution on its stated domain. A trivial Brown branch supplies a solution without the intended geometric normalization, as Turn3 warned. I have not constructed a natural extension of the odd-Chern/spin normalization across the remaining higher-two-primary structures, nor found a contradiction to all such extensions.

## 6. Status

This turn rules out two concrete shortcuts: the raw rational signature defect modulo16, and an arbitrary spin origin followed by the principal scalar half-phase. It also derives a checkable correction cocycle and the full descent/finite-type conditions. These are scoped results and a precise residual system, not a resolution of that system. The non-torsion domain issue remains separate. One substantive author turn remains; no complete original-target claim is made.
