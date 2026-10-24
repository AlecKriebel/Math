# Fresh independent adversarial audit: independent zero-weight directions

## Verdict and exact claim

**PASS for the stated derived partial theorem.** Suppose the finite RAAG graph has vertex partition S disjoint-union D, D has no internal edges, the live flag complex on S is simply connected, every dead vertex has a nonempty connected induced live-neighbor graph, and the height map is nonzero on every live generator and zero on every dead generator. Then its kernel is finitely presented and has an intrinsic Dehn upper bound n^9, up to the standard coarse comparison.

This is an upper bound for an explicit subclass. It supplies no superexponential or superpolynomial-subexponential example and does not resolve either branch of Kourovka 21.126. No originality, sharp exponent, arbitrary dead-edge configuration, or arbitrary subgroup upper bound is verified. This is an independent AI adversarial audit, not human peer review.

## Distinct mechanisms checked

### Connected nonzero weighted kernels have quadratic distortion

The earlier rectangular height-pushing construction requires only connectedness of the positive/negative link to extend over the deleted balls' radial 1-skeleta. Extending over radial edges asks only for paths, not disk fillings. The same coordinate compatibility and linear height-strip local Lipschitz estimate therefore apply on Y union X^(1). This domain contains the connected original 1-skeleton and its other pieces attach to it, so its retraction image Z is path connected.

The height-zero kernel acts freely and properly on Z, with finitely many cell orbits by the bounded-height cube argument. Z is a connected locally finite finite-shape polyhedral length space. Its intrinsic metric is proper and geodesic (equivalently, one may use uniform finite-shape paths), so the standard geometric-action comparison gives a finite generating set and comparison of intrinsic distance with kernel word length. No finite presentation is inferred here.

A length-n ambient word path between kernel vertices stays in height O(n) and has rectangular length O(n). Its pushed image has length O(n^2) and the same endpoints. This proves the distortion upper bound. It does not use simple connectivity of this live-neighbor flag complex.

### Identity HNN filling estimate

Let u be an X-word representing an element of an associated finitely generated subgroup K_i. If v is a word in its chosen subgroup generators representing u, the relation t_i^epsilon u t_i^(-epsilon)=u has a certificate consisting of two base diagrams for u=v and a corridor of |v| commutation cells. This works for epsilon=+1 and -1: inverses of stable-letter commutation relations have the same area cost. If subgroup generator X-lengths are at most C, the two base boundaries have length at most |u|+C|v|.

For a null boundary word of length at most n, Britton supplies a pinch whenever stable letters remain. Delete the two pinch stable letters and retain exactly the same base word u. This preserves the represented element because the associated map is the identity. Therefore the number of base letters on every subsequent boundary is at most n; there is no substitution-length recurrence. At most n/2 such steps occur. Using a distortion upper bound f for |v| yields O(n delta_G(n+C f(n))+n f(n)) area, followed by one final base filling of length at most n. This is the displayed coarse estimate. The argument specifically uses identity associated maps and would not justify the same bound for arbitrary HNN monodromy.

### Kernel presentation and residues

The absence of edges within D makes the ambient RAAG exactly the simultaneous identity HNN extension of A(S) along its induced neighbor parabolics. After scaling the global height image to Z, choose t of height one. For each z, d_z is positive because the live neighbor set is nonempty, and phi(A(Lambda_z))=d_z Z.

An independent Bass–Serre orbit calculation reproduces the author's presentation: the kernel action on the ambient Bass–Serre tree has one vertex orbit because phi(A(S))=Z, and d_z edge orbits for the z-loop because phi(A(Lambda_z))=d_z Z. The edge groups are t^i K_z t^(-i), and both edge injections are identical because z centralizes its neighbor parabolic. Thus each residue gives one identity HNN stable letter.

The elementary proof was also checked directly. Write any integer q=i+ell d_z with 0<=i<d_z, allowing negative ell. A word v_z in the neighbor parabolic of height d_z exists by Bezout; it commutes with z, even if that parabolic is nonabelian. Then h=t^q v_z^(-ell) t^(-i) has height zero and h z_i h^(-1)=t^q z t^(-q). This proves generation for positive and negative height indices. Rewriting an ambient height-zero word supplies precisely these conjugates and elements of the base kernel.

For injectivity, expand a reduced word in the proposed stable letters. An ambient Britton pinch must have the same dead-letter label z, opposite stable signs, and middle base element t^(-i) g t^j in A(Lambda_z). Its height j-i belongs to d_z Z, forcing i=j because both representatives lie in [0,d_z-1]. The remaining membership says exactly g in t^i K_z t^(-i). This would be a forbidden pinch of the proposed word, for either choice of its first stable sign. Different dead labels cannot create a Britton pinch; multiple dead vertices therefore introduce no missing cancellation case. A word with no stable letters uses the embedded base kernel. The presentation is injective.

### Distortion comparison and finite presentability

For an induced RAAG parabolic, the standard generator-killing retraction is 1-Lipschitz, and inclusion is also 1-Lipschitz. It is therefore isometric in standard word metrics. If k_i=t^i k t^(-i) and k_i is measured in the finitely generated base kernel G, each G-generator has uniformly bounded ambient length. Conjugating by one of the finitely many fixed t^i adds a constant. Hence |k| in its neighbor parabolic is at most C|k_i|_G+C. Applying the quadratic distortion lemma there, then conjugating the subgroup generating set, gives the common quadratic bound in G. No reverse undistortion of G or of K_i is assumed.

The simply connected live flag complex gives G finite presentation and quartic Dehn upper bound via the previously reviewed nonzero-weight note. The neighbor kernels need only be finitely generated. There are finitely many dead labels, finitely many residue indices, and finitely many subgroup commutator generators. Thus the simultaneous HNN presentation is finite. The filling estimate with delta_G(n)=O(n^4) and f(n)=O(n^2) gives n*(n+n^2)^4+O(n^3)+O(n^4)=O(n^9).

## Adversarial cases and exact computation

The claim handles D empty by reducing to the quartic live-kernel bound. A singleton neighbor graph has trivial associated kernel; this creates a free stable letter and no missing relation. Unequal weights and d_z>1 are accounted for by the residue list, not by assuming the restricted map is onto. Mixed live signs can be inverted at the outset. No argument uses an edge between two dead generators, and the final note explicitly leaves that case outside scope.

I independently checked a nontrivial model with two dead letters and modulus two. Let the ambient group be Z(a) times Z(b) times F(c,z,w), so the live graph on {a,b,c} is a clique and both dead vertices have neighbor edge {a,b}. Give weights (2,4,3,0,0). Put k=a^(-2)b and l=a^(-3)c^2. Direct projection to F(c,z,w) identifies the kernel with Z(k) times the index-two subgroup in which the c exponent is even. Its free factor has the Schreier basis c^2,z,c z c^(-1),w,c w c^(-1). Thus the kernel is Z times F_5, exactly the proposed centralizer presentation with both moduli equal to two.

The standard-library exact checker `verify_zero_directions.py` maps 73,811 freely reduced words of length at most five in the predicted five-generator free factor into the ambient free group, independently decodes them by Schreier rewriting, and recovers every word exactly. For each it checks five central coordinates and exact height zero. It also checks 162 residue-conjugation identities for both dead labels and all q from -40 through 40. Arbitrary inverse stable letters occur in the word census. The finite test is a consistency check of this explicit model, not a proof for every graph or an isoperimetric lower bound.

## Outcome

No substantive mathematical objection was found in the exact stated scope, and no repair was required for this note. All three mechanisms are independently justified: connected-kernel quadratic distortion, nonexpanding identity-HNN pinch reduction, and the residue-indexed kernel decomposition. The remaining dead-edge case requires new work; it does not follow from this PASS.
