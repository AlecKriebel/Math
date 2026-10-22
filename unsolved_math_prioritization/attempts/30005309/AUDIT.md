# Independent mathematical audit: unrestricted correlation-model partial bounds

Date: 11 October 2026 UTC. Target: 30005309 / OWR-11695865-008.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. Novelty and priority are unestablished; no exhaustive current-openness claim is made.

## Verdict and exact accepted scope

ACCEPTED as rigorous partial mathematics, with the explicit SSL finite-degree qualification in the reviewed theorem. No mathematical correction is required to the pinned theorem. This is not acceptance of an exact all-n recurrence for any of the three requested sequences, nor of resolution of the bundled problem, novelty, or exhaustive literature/history coverage.

The accepted claims are:

* The all-n ML lower-bound recurrence with block weights 1, 2, and 2^k for k >= 3, its exponential generating function, and its displayed values.
* The all-n intrinsic SSL theorem producing at least B_n persistent simple invertible critical points, with block weights 1, 0, and 2^(k-1) for k >= 3; the stated SSL-degree inequality only under the finite-generic-degree convention.
* The scheme-exact dual determinant reduction, n! upper bound, supermultiplicativity, resulting elementary lower bounds, and exact dual degree 5 at n=3.
* The ML total-degree and multihomogeneous upper bounds; the SSL isolated-scheme-length upper bound and its conditional degree interpretation.
* The generic-diagonal positive-dimensional obstructions: ML at n=4 and SSL at n=5.
* The generic n=1 degrees 1,1,1 and n=2 degrees 3,2,4, with losses kept distinct.

The creator inventory's pending-acceptance field is historical metadata of the sealed submission; this separate report records the independent internal AI acceptance of the partial theorem.

## Exact input authentication

The complete theorem and source/scope report, all three authored Python checkers, README, retained check results, and input-manifest records were read. The externally supplied inventory was authenticated before mathematical execution, with exact closed membership:

* Creator closed inventory: 2801 bytes; SHA-256 c31ddcb6051a1289becfa2cdc033f3732b22c92bc8ac36e69eedd46ad1dae6e4.
* Original complete theorem: 19022 bytes; SHA-256 b1ac5288a7d082e862b185fa83b999fbc29256fcb135b046d59bad5e83b50ccb.
* Original source/scope report: 5910 bytes; SHA-256 5762f759e40e81f1f1796d9138715e98bff578d9be3aa56bf78eb5e93edbba34.
* Creator finite mathematical checker: 8692 bytes; SHA-256 82816b47a6327f0ba4e507c85d46d239bc387a21e14b1874430d10aa5e2e51b5.
* Creator integrity checker: 4181 bytes; SHA-256 4f1a171d2f6a40a784d928faef2555a56110080473cafc879d9bd3cea98ded54.
* Creator closed-inventory checker: 1880 bytes; SHA-256 5e59937fc3279749c9cebfe5c4559670562cd5909a89e35ebc36a7bc2bc33773.

All 16 creator members match, and only the inventory itself is self-excluded. Independently, the scoped source-evidence inventory SHA-256 f3b99fee790752f87f9487b4d9a134f75c1a870ac8fcdc18833f05123970193e and all 43 declared member byte counts and hashes match. The exact complete original problem statement was read. Counts alone are not authentication evidence.

No reviewed input was modified. The audit's own closed inventory binds this report, its independent checker, execution outputs, and retained source-status receipt.

## 1. Model, schemes, and multiplicity

The model is the full affine space of symmetric matrices with unit diagonal, restricted to nonzero determinant, over C. Its off-diagonal dimension is m=n(n-1)/2. The three systems are respectively offdiag(K-KSK), offdiag(K-W), and offdiag(KSK-W), with K=Sigma^(-1) and W=S^(-1). Multiplying either equation list by an everywhere-invertible common denominator does not change its localized ideal. Thus the three displayed numerator ideals, saturated by Delta, are scheme-correct and preserve multiplicity. W is never independently varied from S in the SSL argument.

The auxiliary diagonal matrix D in S=Sigma-Sigma D Sigma is unique: D=K-KSK. Consequently this incidence formulation and the ML scheme are isomorphic on the invertible locus, including infinitesimal structure. The same observation applies to the diagonal T_0=KSK in the diagonal-data SSL argument. There is no reliance on real positive definiteness or on counting local/global optimizers.

The rational coordinate examples used below employ a diagonal congruence R with R^2=diag(B). They correspond to actual complex correlation matrices Sigma=R^(-1)BR^(-1). Every diagonal entry of B is nonzero. This is an invertible change of off-diagonal tangent coordinates and output scalings, so ranks in these coordinates are exactly ranks in the unrestricted correlation tangent space. It is not an equicorrelation restriction.

## 2. Upper bounds and generic finiteness

Adjugate entries have total degree at most n-1. The ML numerator degrees are at most 2n-1, dual at most n, and SSL at most 2n. Affine Bezout therefore gives the stated product bounds for isolated local scheme lengths. Positive-dimensional components do not invalidate a bound on the sum over isolated points; they do prevent identifying that sum with an unqualified finite total length.

For the ML alternative, the N=n(n+1)/2 entries of S-Sigma+Sigma D Sigma have bidegree at most (2,1) in m off-diagonal Sigma coordinates and n diagonal D coordinates. After bihomogenization, the ambient dimension is m+n=N, and the coefficient of H^m E^n in (2H+E)^N is 2^m binom(N,n). Since the localized incidence and critical schemes are isomorphic, this is the stated ML bound. Boundary components of a chosen compactification cannot increase the isolated affine contribution beyond this intersection bound.

The ML map from X_n times C^n to Sym_n is a morphism from an irreducible N-dimensional smooth variety to an N-dimensional space. At (I,0) its derivative is (H,E) -> H-E; the zero-diagonal and diagonal subspaces are complementary. Dominance, finite generic extension, and characteristic-zero separability give a finite reduced fiber on a nonempty Zariski open of data. For a finite-type affine model, generic finiteness can be promoted to finiteness after localizing the base, so no properness assumption is hidden here.

For dual ML the rational map Sigma -> offdiag(Sigma^(-1)) has derivative -H at I, giving its analogous generic finiteness and reducedness. These proofs do not establish global generic finiteness for SSL. The reviewed artifact explicitly does not make that inference. Its SSL lower bound retains an intrinsic simple-branch formulation and its upper bound retains an isolated-length formulation. Those qualifications must remain in any reuse.

## 3. Dual determinant reduction and n=3 certificate

Set M=A+diag(z) with A_ij=W_ij for i != j and f=det(M). The maps Sigma -> K=M and M -> M^(-1)=Sigma are inverse regular maps after inverting determinants. The conditions diag(Sigma)=1 become partial_i(f)/f=1. Therefore the determinant ideal localized at f, and equivalently its saturation in affine z-space, is scheme-exact. The diagonal of W does not enter; inversion is birational on symmetric matrices, so generic invertible S supplies generic off-diagonal W.

Each partial_i f-f is multiaffine. Its class in (P^1)^n is H_1+...+H_n, and the top coefficient is n!. This counts an upper bound, not an equality, because unsaturated base points and infinity may consume intersection degree.

For symmetric M of rank n-1, its nonzero symmetric rank-one adjugate is c vv^T. Vanishing of every diagonal cofactor would give v_i^2=0 for every i, impossible for v != 0 over C. Thus f and all diagonal cofactors vanish exactly at rank <= n-2. The dimension argument is valid: after choosing an invertible principal (n-3)-block, the residual symmetric 3x3 Schur complement with generic off-diagonals a,b,c has unique rank-one diagonal completion (ab/c,ac/b,bc/a). This establishes dominance of the corank-two locus over off-diagonal data. Its codimension is 3, so the generic diagonal fiber dimension is n-3. At n=3 it is a unique point.

The n=3 calculation was independently reconstructed from the actual matrix with off-diagonals (1,2,3), not by running a source-author program. The supplied lex Groebner basis generates exactly the saturated ideal after adjoining tf-1. Its univariate polynomial has degree 5 and gcd with its derivative equal to 1. The other coordinates, including t, are linear expressions in z_3. Hence the localized scheme consists of five simple invertible points.

An additional independent check of the unsaturated quotient gives exactly six standard monomials. Zero-dimensionality and pure-power leading-monomial bounds are checked before enumeration. The excluded point is (2/3,3/2,6); its matrix has rank 1 and the Jacobian determinant of the three unsaturated equations is 12. In the general nonzero-(a,b,c) case this determinant is 2z_1z_2z_3=2abc, so the base point contributes exactly one to the multiaffine upper bound 6. The upper bound of five generic invertible roots plus persistence of the five specialized simple roots proves dualMLdeg(3)=5. This is a reproof of an already reported primary-source value, not a new numerical prediction.

For supermultiplicativity, the full cross-block derivative at block-diagonal Sigma is H -> -K_a H K_b, an invertible map on all a by b cross entries. The within-block derivatives are nonsingular on generic simple fibers. Thus each pair yields a simple full-model root; perturbation gives the generic lower bound. Iterating blocks of size 2 gives 2^floor(n/2), and size-3 blocks plus the remainder gives the stated 5^floor(n/3) factor with a factor 2 for remainder 2. Remainders 0 and 1 have factor 1.

## 4. ML diagonal classification, enumeration, and simplicity

For diagonal S, D Sigma commutes with DS because DS=D Sigma-(D Sigma)^2. If d_i != 0, d_j=0 and Sigma_ij != 0, the (i,j) commutator entry forces s_i d_i=0. This contradicts invertibility of diagonal S. Thus D is either invertible throughout a connected block or vanishes throughout it. The latter would imply Sigma=S and hence only an excluded s_i=1 singleton. Generic diagonal data avoid this.

Once D is invertible, the same commutator forces s_i d_i=c on every support edge and hence the whole block. The congruence B=D^(1/2) Sigma D^(1/2) satisfies B^2-B+cI=0 and diag(B)=c/s_i. Except at c=1/4 it is diagonalizable with distinct eigenvalues lambda and 1-lambda. This exclusion is proper even beyond the rank-one branch: if c=1/4, B-I/2 is nilpotent, so trace(B)=k/2 and T=2k. A generic diagonal S avoids that hyperplane in reciprocal coordinates.

A symmetric idempotent of rank 1 is uu^T with u^T u=1. The trace relation gives T lambda^2-(T+k-2)lambda+k-1=0. Its generic two roots are distinct, and the prescribed u_i^2 sum to 1. Excluding coordinate zeros and lambda values 0,1,1/2 removes proper algebraic conditions. Each admissible square vector gives 2^(k-1) projectors, since simultaneous sign reversal is the only identification. Their complete support ensures connectedness.

For k>=3 the two quadratic roots do not have equal c=lambda(1-lambda): if they did, their sum would be 1, whereas it is 1+(k-2)/T. Distinct c give distinct recovered D, hence distinct Sigma. The total is 2^k. For k=2 the roots are complementary and describe the same two points; the direct equation rho^2=1-s_1-s_2 confirms the weight 2. A singleton contributes 1. These are lower-bound families; the text does not claim all ranks have been exhausted.

To audit simplicity, allow arbitrary zero-diagonal H, rather than only support-preserving or equicorrelation variations. The uniquely recovered delta D is diagonal for a critical Jacobian kernel vector. Differentiating the commutator at DS=cI gives that diag(s_i delta d_i) commutes with D Sigma. Complete support forces it to be scalar, delta c I. Differentiating the trace identity then gives

(T-(k-2r)/(2lambda-1)) delta c=0.

At r=1 this factor is nonzero exactly away from the quadratic discriminant. Thus delta c=delta D=0. The remaining congruence tangent X satisfies BX+XB=X. The only eigenspace pair whose eigenvalues sum to 1 is the lambda/1-lambda pair, so at rank 1 the symmetric solutions are uv^T+vu^T with u^T v=0. The zero diagonal gives u_i v_i=0; every u_i is nonzero, hence v=0 and H=0. The exceptional small cases are already covered directly.

For cross-block variations the Sylvester map is H -> H-(Sigma_a D_a)H-H(D_b Sigma_b). Its possible zero eigenvalues correspond to eigenvalues mu_a+mu_b=1. This forces mu_a(1-mu_a)=mu_b(1-mu_b), namely equal block constants. Singleton eigenvalues are 1-s_i with c_i=s_i(1-s_i), so they fit the same argument. Every block constant is nonconstant in that block's independent parameters, and finitely many branch choices and partitions occur at a fixed n. All forbidden equalities can therefore be avoided simultaneously on a nonempty Zariski open. This is a full-model simplicity argument.

Counting the block containing label 1 yields exactly the displayed weighted-partition recurrence. The block exponential generating series is e^(2x)-1-x-x^2, so exponentiation gives the stated A_n series. The n=0 combinatorial initialization is 1; it is not a claim about a statistical model with data size zero.

## 5. SSL diagonal classification, enumeration, and simplicity

At diagonal S, W is diagonal, so T_0=KSK is diagonal and invertible. The equivalent relation Sigma T_0 Sigma=S gives B^2=ST_0 for B=T_0^(1/2) Sigma T_0^(1/2). Commutation with its square and connectedness force s_i (T_0)_ii=c != 0. With beta^2=c, B=beta(2P-I), and trace(B)=cT=beta(2r-k) gives beta=(2r-k)/T. Therefore balanced r=k/2 is impossible when T != 0. The diagonal prescription P_ii=(1+beta/s_i)/2 has trace r.

At rank 1 and k>=3 there are exactly 2^(k-1) sign projectors with generic nonzero entries. Replacing (r,beta,P) by (k-r,-beta,I-P) gives the identical B and does not double the count. A connected size-2 block would require r=1, the forbidden balanced case; r=0 or 2 is scalar and disconnected. Thus b_2=0, while singletons have weight 1.

A full zero-diagonal kernel variation again forces s_i delta(T_0)_ii=delta c by the differentiated commutator. Differentiating trace(B)=Tc and B^2=cI gives T delta c=(T/2) delta c. Because T != 0, delta c=delta T_0=0. The remaining equation BX+XB=0 has exactly the cross-eigenspace symmetric solutions uv^T+vu^T at rank 1. Their zero diagonal forces X=0. This verifies simplicity in the entire tangent space.

Cross-block zero modes would require opposite eigenvalues. All nonsingleton eigenvalues are +/- beta and singleton eigenvalues are s_i. Opposite eigenvalues require equal c, with c=(k-2)^2/T^2 on the constructed nonsingletons and c_i=s_i^2 on singletons. These nonconstant functions depend on disjoint data sets, so all collisions can be simultaneously avoided as in ML. The counting recurrence follows. The block series is (e^(2x)-1)/2-x^2; exponentiating gives the displayed B_n series.

No ML dominance argument is transferred to SSL. The actual result proved here is that finitely many distinct simple SSL roots persist after general perturbation; translating that into total finite critical degree uses the stated convention, not an unproved theorem inside the package.

## 6. Prescribed projector diagonals and positive-dimensional strata

The variety of symmetric rank-r idempotents is the open set of nondegenerate r-subspaces in Gr(r,k), with the projector onto the orthogonal complement kernel uniquely determined. It is irreducible and has dimension r(k-r). For each pair of coordinates, one can choose a subspace containing e_i+e_j and r-1 other coordinate vectors to get P_ij != 0. Thus each off-diagonal nonvanishing condition is nonempty open, and their intersection is nonempty by irreducibility.

Tangent vectors [A,P] with A skew-symmetric have diagonal variations spanning the vectors P_ij(e_i-e_j). Connected support therefore gives diagonal-map differential rank k-1. The map to trace-r diagonal space is dominant and generically smooth, with generic fiber dimension r(k-r)-(k-1)=(r-1)(k-r-1).

It remains necessary that the prescribed diagonals from data actually be generic in that target; dimension counting alone would be insufficient. The artifact supplies this missing step. In ML, choosing generic (lambda,p) of trace r and setting s_i=lambda(1-lambda)/((1-lambda)+(2lambda-1)p_i) gives a generically finite map from a k-dimensional space to diagonal data, since lambda satisfies the quadratic trace equation and then p is uniquely recovered. This proves dominance. In SSL, choosing (beta,p) and setting s_i=beta/(2p_i-1) is birationally recovered by beta=(2r-k)/T when 2r != k, proving the analogous dominance.

Consequently rank 2 in ML k=4 has generic projector-fiber dimension 1 and rank 2 in SSL k=5 has dimension 2. Congruence changes are invertible, eigenvalues and scale factors are nonzero generically, and complete support is an open condition, so these are connected critical loci inside the invertible model. They are not denominator artifacts. Their existence defeats naive diagonal-fiber exhaustion and permits further branches after perturbation. No number of those additional branches is asserted.

## 7. Persistence and the word generic

At each constructed point the square Jacobian in correlation coordinates is invertible. The analytic implicit function theorem produces one simple branch over a common neighborhood of the chosen data; disjoint neighborhoods preserve distinctness of the finitely many roots. Algebraically, these points lie in components locally etale over data, hence in dominating generically finite components. After shrinking a nonempty Zariski open, their degrees contribute at least the constructed number of simple roots. For ML and dual ML, this intersects the finite reduced generic locus established above. For SSL it proves the intrinsic simple-branch statement even without ruling out other dominating components. This addresses the distinction between an analytic neighborhood and the theorem's generic algebraic statement.

The examples need not be positive definite: the degree concerns generic complex data. A nonempty Zariski-open condition can be interpreted against the Zariski-dense real positive-definite data set when relevant; no local neighborhood of a negative example is claimed to contain positive-definite matrices.

## 8. Small cases and independent computation

At n=1 the model has one point and no off-diagonal equations; all three lengths are 1. At n=2 the three symbolic numerators in the artifact were independently derived from the original matrix equations for arbitrary a,b,c,rho, with W computed as S^(-1). Specializing S=[[2,1],[1,3]] gives degrees 3,2,4, squarefree polynomials, and no common factor with 1-rho^2. Their leading-coefficient, discriminant, and determinant-resultant conditions are open, proving the generic small degrees. The SSL numerator's degeneration at diagonal b=0 explains why the diagonal lower bound B_2=1 does not equal generic SSL degree 4.

The new independent checker does not import any creator module. It verifies six nonuniform rational projector/congruence examples: rank-one ML at k=3,4; rank-one SSL at k=3,4; rank-two ML at k=4; rank-two SSL at k=5. It calculates all unrestricted Jacobian columns exactly over Q, verifies three selected columns by direct symbolic directional differentiation in each case, and proves exact nullities 0,0,0,0,1,2. It also checks full diagonal-map ranks 2,3,2,3,3,4.

An explicit original-coordinate nonuniform ML point is Sigma=[[1,-1,-1],[-1,1,-4],[-1,-4,1]], S=diag(-5,-20,-20). Its exact full Jacobian determinant is 2176/15625. Independently assembled full rectangular cross-block maps have determinants -2744 for ML blocks 3+2 and -626913312768 for SSL blocks 3+4. Equal block-constant controls are singular and rejected. These checks corroborate, but do not replace, the all-n spectral proof.

The independent check also enumerates weighted set partitions directly through n=6 and compares them with the recurrence, rather than relying solely on an exponential-series calculation. The displayed sequences through n=8 agree. The creator separately checks the exponential series through n=8.

The reviewed creator checker constructs original-coordinate rational points through single-block size 7 and block products of total sizes 6 and 8. Its matrix derivative formulas have the correct signs and multiplication orders for the three losses. Its larger nonsingularity certificates perform exact Gaussian elimination modulo 1000003. Primality is checked before use, every rational-entry denominator is checked to be nonzero modulo the prime, and each pivot is required to exist. Thus all entries lie in the localization Z_(p), and invertible reduction implies a nonzero determinant over Q. These are sound exact nonsingularity certificates, not numerical conditioning tests. This audit also verifies primality independently by trial division and checks rejection of denominator 1000003. A modular zero determinant would not prove rational singularity, but the checker never makes that inference.

## 9. Execution history and negative controls

All three creator checkers were read before execution, then run unchanged in normal, -O, and -OO modes. Their outputs are retained separately; only report identities and prose findings are distributed in this edition. All nine runs pass. The independent checker likewise passes unchanged in normal, -O, and -OO; it uses explicit exception guards and checks that its AST contains no assert statements.

The first independent test construction used equally spaced Vandermonde rows. Its intended complete-support guard correctly failed for a rank-two example with a zero off-diagonal projector entry. That was an unsuitable test fixture, not a theorem counterexample. The checker was changed to geometrically spaced nonuniform rows, whose exact projectors have complete support. An initial successful version was then strengthened with an explicit finite-quotient/pure-power check before standard-monomial enumeration and independent prime/denominator controls; final outputs correspond only to this strengthened final code. No unsuccessful run is counted as a pass.

Genuine negative controls cover: wrong external inventory pin, altered member bytes, unlisted files, repinned omitted and duplicate members, duplicate JSON keys, forbidden modular denominators, incorrectly declaring either positive-dimensional example simple, wrong S, singular Sigma, wrong correlation diagonal, colliding ML and SSL block constants, conflating dual and SSL equations, admitting the unsaturated rank-one dual root, an altered dual quintic certificate, double-counting complementary k=2 ML branches, and equating the ML lower bound 73 with the imported exact-source value 109. The last comparison uses that primary table as a claim-boundary control, not as a newly certified degree-109 computation.

The creator's disclosed interrupted/timed-out preliminary runs are not rerun here and are not accepted as passes. Only the sealed successful checker outputs and this audit's fresh reruns count.

## 10. Source and provenance audit; limits

The source equations and target were checked against authenticated retained extracted text:

* [Oberwolfach Report 55/2022](https://ems.press/content/serial-article-files/46992): PDF pages 17-18, printed pages 3137-3138. Its retained PDF is 600619 bytes, SHA-256 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65.
* [Amendola and Zwiernik, Likelihood Geometry of Correlation Models](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2274/1147/6553): PDF page 1; pages 3-6 including the gradients and generic complex definition; and pages 10-11 for unrestricted equations and table. Retained PDF: 375434 bytes, SHA-256 6e46808caf9da4eb37e9b6211b7c706fc38229693785e6309c6b128760a8dba5.
* [Alexandr, From Voronoi Cells to Algebraic Statistics](https://yuliaalexandr.github.io/final.pdf): retained title page and PDF page 34, printed page 25. Retained PDF: 11224611 bytes, SHA-256 bedad32eb9f78de2d60aec301488bc2e047f697e8c5f75d7348d50d241ebed57. Its title page dates the thesis Fall 2023; the cited unknown-status statement is interpreted only at that time.

The present auditor did not newly render/view PDF page pixels, re-download any PDF, inspect entire PDFs, or execute scholarly source-author code. Reading extracted text is not a new visual page inspection; authenticating full PDF bytes is not a full proof audit. The original source/scope report correctly preserves that distinction.

The three retained current-search result files were authenticated and their relevant discovery/status content checked. They are bounded result receipts, not a complete query log or an exhaustive novelty certificate. The current [arXiv landing page](https://arxiv.org/abs/2012.03903) was freshly opened by this auditor and still lists submission 7 December 2020 and latest revision v2 on 1 February 2021; the retained response identity is recorded in SOURCES.json. This verifies that specific current-revision statement, not absence of later work elsewhere. The source audit's failed fresh thesis-open disclosure is retained as a limitation; the retained authenticated thesis supplies the dated claim.

The OEIS near-match does diverge from the cited dual sequence and is not used in the proof. No exact all-three resolution or novelty conclusion follows from failure to locate one. Prior bounded repository/history checks were read and their pinned artifacts authenticated, but this mathematical auditor did not independently repeat remote history searches or claim exhaustive history coverage. The complete selected source record preserves the bundled all-three target.

No reviewed input was modified. This prose edition preserves the complete mathematical review and its limitations while excluding programs, raw outputs, copied source documents, and coordination material. Source-byte authentication, mathematical acceptance, and publication authorization are distinct.

## Final acceptance boundary

The pinned partial theorem is mathematically acceptable as written. Its SSL qualification, saturation and invertibility restrictions, dependence W=S^(-1), unrestricted tangent-space checks, multiplicity convention, source/status limits, and explicit unresolved exact-all-n target are substantive parts of this acceptance. Removing any of them would require re-review.
