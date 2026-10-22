# Turn 1 candidate: adjoint exclusion of nonlinear components

2026-10-02. Status: complete scoped candidate over the complex numbers, awaiting independent adversarial review. ORIGINAL SOURCE remains unresolved: Janssen works in arbitrary characteristic; a characteristic-zero result alone is partial. This is the first recovered substantive turn; no prior saved assignment or author turn was found. It must not be counted as a verified solution yet.

## Exact claim
Let L be a nonempty reduced finite union of projective lines in P^3_C, I its homogeneous radical ideal, and alpha its initial degree. If alpha(I^(2))=alpha(I)+1, then L is coplanar or a pseudostar (all pairwise intersections of distinct planes, no three containing a line). In particular L is arithmetically Cohen–Macaulay, answering the source existence question negatively in characteristic zero.

## Adjoint lemma
If S⊂P^3_C is an integral surface of degree d≥2, there exists a nonzero polynomial of degree d−2 vanishing along every one-dimensional irreducible component of Sing(S).

Proof. Let ν:Y→S be normalization and π:X→Y a projective resolution. Put H=(νπ)^*O_S(1). This is nef and big, H²=d, and its complete linear system has a basepoint-free subsystem given by ambient hyperplanes. A general member C of that subsystem is smooth and integral (Bertini for a birational map onto an integral surface; the hyperplane avoids the finitely many singular points of Y). Adjunction gives
0→ω_X(H)→ω_X(2H)→ω_C(H|C)→0.
Kawamata–Viehweg vanishing on the smooth complex projective surface gives H¹(X,ω_X(H))=0. Since deg(H|C)=d>0, Riemann–Roch and Serre duality on C give h⁰(C,ω_C(H|C))=d+g(C)−1≥1. Hence H⁰(X,ω_X(2H)) is nonzero.

The normal surface Y is Cohen–Macaulay and its dualizing sheaf ω_Y is reflexive. A canonical form on X determines a section of ω_Y on the smooth locus of Y, which extends across its finitely many singular points by reflexivity. This yields an injection π_*ω_X→ω_Y. Projection formula and finite duality for ν identify
ν_*ω_Y = Hom_S(ν_*O_Y,ω_S) = c⊗ω_S,
where c=Hom_S(ν_*O_Y,O_S) is the conductor ideal, identified inside the common rational function field, and ω_S=O_S(d−4). Thus a nonzero section above yields a nonzero section of c(d−2)⊂O_S(d−2). It lifts to a homogeneous polynomial of degree d−2 because H¹(P³,O(-2))=0 in the hypersurface exact sequence. Its restriction is nonzero, so the polynomial is nonzero.

Every singular curve of S is nonnormal at its generic point: a one-dimensional normal Noetherian local domain is regular, while the generic point of a singular curve is a singular codimension-one point. The conductor is a proper ideal there. Consequently its sections vanish on that curve. This proves the lemma. All cited geometric inputs and the extension/lifting must be checked independently before promotion.

## Minimal symbolic-square witness
Set a=alpha(I), e=a+1 and choose 0≠F∈I^(2)_e. For a union of distinct lines with homogeneous primes P_l, I^(2)=∩_l P_l². Thus F has order≥2 along each target line. Every line lies in at least one irreducible factor of F.

### Repetitions
If the squarefree radical of F has degree≤e−2, it is already a nonzero element of I of degree below a, impossible. The only remaining repeated-factor case is F=H²G where H is a linear form, G is squarefree and coprime to H. If G is nonconstant, choose a nonzero partial derivative ∂G. For a target line not contained in H, localizing at its prime shows G has order≥2 along the line, hence ∂G vanishes on it. On a target line contained in H, H vanishes. Therefore H∂G is a nonzero polynomial of degree e−2 in I, contradiction. (Membership in the prime follows from generic vanishing; equivalently use the differential criterion for linear primes.) If G is constant, F=H² and all target lines are coplanar. Thus outside this already-ACM exception F is squarefree.

### Nonlinear components
Suppose a squarefree F has irreducible factor Q of degree d≥2. By the adjoint lemma choose nonzero A of degree d−2 vanishing on all singular curves of V(Q). Then A(F/Q) has degree e−2. Any target line lying in another component of F is contained in V(F/Q). Any remaining target line lies solely in V(Q); since F vanishes doubly and other factors are units at its generic point, Q vanishes doubly there. That line is a singular curve of V(Q), so A vanishes on it. Again A(F/Q)∈I contradicts alpha(I)=e−1. Hence F is a product H_1⋯H_e of distinct linear forms.

### Plane arrangement
Every target line is an intersection of at least two of these planes. Fix i≠j and write l=V(H_i,H_j). If l is absent from L, or if some third H_k contains l, then F/(H_iH_j) vanishes on every target line: a different target line cannot be contained in both H_i and H_j and therefore lies in a remaining factor; if l itself belongs to L in the latter case it lies in H_k. This gives degree e−2 in I, impossible. Thus every pairwise line is in L and no three planes contain a line. Conversely there can be no additional target line because every target line lies in at least two factors. L is exactly their pseudostar.

## ACM verification
Let J=(F/H_1,…,F/H_e). An e×(e−1) Hilbert–Burch matrix has H_i in row i of column i (1≤i<e), −H_e in its last row in every column, and zero elsewhere. Its maximal minors, up to sign, are exactly these generators. Their ideal has height two: its zero set is the union of pairwise plane intersections. Hilbert–Burch makes R/J Cohen–Macaulay with no embedded associated primes. At the generic prime (H_i,H_j) no other H_k vanishes, because there are no triple-containing lines; J localizes to (H_i,H_j). Thus J is generically reduced and unmixed, hence radical, and J=I(L). Therefore R/I(L) is Cohen–Macaulay. Coplanar reduced line unions are complete intersections (plane equation plus product of the distinct line equations in that plane), also ACM.

## Scope and caveats
This proof is characteristic zero and depends essentially on resolution and Kawamata–Viehweg vanishing. It does not establish a positive-characteristic version. The published ACM classification and its pseudostar terminology must be credited. No novelty or priority claim is made. Independent source, proof and edge-case review is required, especially the adjoint/conductor lemma.
