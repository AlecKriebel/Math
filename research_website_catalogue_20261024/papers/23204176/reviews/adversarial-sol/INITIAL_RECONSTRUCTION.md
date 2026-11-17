# Original-only adversarial reconstruction — record 23204176

INITIAL phase only. This is an independent claim reconstruction, hand derivation and falsification record, not an unconditional verification of the theorem or a promotion decision. Before this record, no README, packaged mathematical opinion/audit, support proof, program body, upstream primary mathematical source, root scientific review or peer review was semantically read. Only the complete controlling original TeX, complete outer-PDF text, four fresh individually viewed native page images, native API/HTML metadata and source-custody controls were read. Hashing all payloads and inspecting names/topology did not constitute semantic reading of their scientific contents.

Authorized INITIAL completion at seal: 100%. Best estimate toward a complete scientific assessment: 35%, because both substantive imported interfaces remain unexamined. No mathematical mechanism or assessment has been sent in messages to root before its own original gate.

## Exact target, quantifiers and exposed author assertions

The original asserts rational Hodge in **every codimension**, with **rational coefficients**, on each finite product X=product_i M_i. Each base S_i is a **complex projective K3 surface**; bases may be different or repeated. Each alpha_i belongs to Br(S_i). Each M_i is an actual **smooth projective stable** moduli space, either Gieseker-stable alpha_i-twisted sheaves with fixed numerical/sheaf data and polarization, or sigma_i-stable objects of Db(S_i,alpha_i) with a generic Bridgeland stability condition relative to the fixed numerical data, **as in the exact scope of Bülles' cited Theorem 0.1**. The original explicitly does not add a primitivity or fine-moduli hypothesis to that imported statement. Whether that scope match is correct is a target of later validation, not an established premise of this INITIAL review.

The conclusion includes every finite mixed product S_i^[n_i] with n_i>=0. The original treats an empty factor, zero-dimensional smooth projective factors, the product of no factors, and p outside [0,dim X]. It does not assert results for singular/semistable moduli, arbitrary deformations of K3^[n] type, arbitrary abelian-surface moduli, nonprojective bases, integral or generalized Hodge, or finite-dimensionality of Chow motives. Those exclusions must not be silently enlarged during review.

Hdg^p(X) is defined as H^(2p)(X,Q) intersect H^(p,p)(X,C), using the ordinary embedding of rational Betti cohomology into its complexification. The asserted conclusion is the surjectivity CH^p(X)_Q -> Hdg^p(X). All cycle correspondences and compositions are rational algebraic Chow correspondences. No integral lattice conclusion follows.

The original exposes these inherited assertions before any support reading:

- OpenAI's cited Theorem 1.1 at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a proves rational Hodge for **arbitrary finite mixed products** of projective complex K3 surfaces, with arbitrary distinct or repeated factors.
- Bülles supplies a rational **Chow-motive** splitting, with finite index sets J_i, 1<=k_ij<=dim M_i for positive-dimensional nonempty factors, and integer Tate twists. The actual splitting includes the full class of twisted/stable-object moduli used in the theorem, including the non-fine case.
- Arapura's conditional transfers and the earlier OpenAI quadratic-locus/self-power applications are antecedents; the author claims only an assembled mixed-moduli consequence, with no first-proof or substantial independent novelty claim.
- The original describes the geometric base input as unformalized and says the upstream Lean module checks Clifford/tensor algebra rather than algebraic cycles, universal Kuga--Satake algebraicity or this note's Hodge theorem. Finite supporting checks are not full geometric certificates. These are original author statements, not separately checked facts here.

The native Description repeats this scope, attribution, quantifiers and formal/finite-check limits. This favorable-looking assertion exposure is unavoidable when reading the actual original; it is not blindness to the author's claims. No underlying supporting verdict was opened.

## Independent degree and categorical reconstruction

Let V,W be smooth projective of dimensions d_V,d_W. For A in CH^a(V x W)_Q, flat pullback of z in CH^p(V), intersection with A and proper pushforward along the V-fiber gives

    A_*: CH^p(V)_Q -> CH^(p+a-d_V)(W)_Q.

On cohomology, the three operations respectively preserve degree/type, add (a,a), and subtract (d_V,d_V). Thus a rational (p,p) class maps to a rational (q,q) class with q=p+a-d_V. Smoothness makes intersection theory available; projectivity supplies proper pushforwards and pure Hodge structures. The argument would not automatically extend to open stable loci or singular coarse compactifications.

For B in CH^b(W x V)_Q, composition is obtained on V x W x V by multiplying the two pullbacks and pushing along W. Its codimension is a+b-d_W. Therefore an identity endomorphism of h(V) requires a+b=d_V+d_W, exactly the relation printed in the note. This is independent of whether a named Tate convention writes its morphisms with +t or -t: the actual codimensions determine both degree shifts.

If h(X) splits into a finite sum of Tate-twisted h(K_j), component maps can be represented by homogeneous rational algebraic correspondences A_j and B_j with

    A_j in CH^(a_j)(X x K_j)_Q,
    B_j in CH^(b_j)(K_j x X)_Q,
    a_j+b_j=d_X+d_(K_j),
    sum_j B_j composed A_j = Delta_X.

Projectors on any intermediary summands can be absorbed into these component maps; they must themselves be algebraic Chow projectors. For arbitrary z in Hdg^p(X), define q_j=p+a_j-d_X. If Hodge holds in every codimension on K_j, choose a cycle Z_j of codimension q_j realizing A_j*z. If q_j<0 or q_j>d_(K_j), the target cohomology is zero and Z_j=0 in that degree. Then

    Z=sum_j B_j*Z_j,
    codim(B_j*Z_j)=q_j+b_j-d_(K_j)=p,
    cl(Z)=sum_j B_j*A_j*z=z.

The last equality follows from the actual diagonal correspondence. This verifies the local conditional transfer without assuming that z is decomposable, that the individual motives are finite-dimensional, or that the Chow group has a basis of algebraic Hodge tensors. It does not produce the required maps for the asserted moduli class and does not prove the mixed-K3 input.

The exact category matters. A splitting only in a numerical or abstract tensor category cannot simply be used as a rational algebraic cycle identity without an appropriate realization/representative bridge. A homological identity represented by actual algebraic correspondences would already suffice for the cohomological conclusion, but that weaker sufficient condition is not a replacement for checking the original claim that Bülles supplies the stated Chow splitting.

### Checkable Tate and boundary controls

For X=Spec C, K=P^1, one may take A=[P^1] of codimension 0 and B=[point] of codimension 1, giving the unit summand and q=0. Alternatively take A=[point] and B=[P^1], yielding q=1 and the Tate-shifted summand. Both have a+b=1 and recover the point class. This tests both shifts without choosing a Tate-sign notation.

For X=P^1 and K=Spec C, the top-degree summand has A=[P^1] of codimension 0 and B=[point] of codimension 1. It sends p=1 to q=0 and back to p=1; for p=0 that component has q=-1 and contributes zero. The separate unit summand recovers degree zero. Thus out-of-range q_j is harmless, but the input must cover all relevant codimensions rather than a single arbitrarily selected degree.

For X=K=S a K3 and A=B=Delta_S, a=b=2 and q=p. The printed composition equation gives codimension 2, not 4, after pushing through the middle surface. These controls expose the common dimensional error of forgetting to subtract the middle dimension.

## Tensor assembly and mixed-Hodge stress test

For factor i let d_i=dim M_i and e_ij=dim S_i^k_ij=2k_ij. If the asserted splitting is available, a_ij+b_ij=d_i+e_ij. For a multi-index J=(j_1,...,j_r), the exterior-product correspondences on X and K_J have

    a_J=sum_i a_ij_i, b_J=sum_i b_ij_i,
    d_X=sum_i d_i, d_(K_J)=sum_i e_ij_i,
    a_J+b_J=d_X+d_(K_J).

Distributing a finite tensor product over finite direct sums yields the sum of composites. Composition of exterior correspondences equals the exterior product of compositions, with the canonical factor permutations. Hence the sum is the exterior product of diagonals, which is Delta_X. Chow cycle classes have even total cohomological degree, and the categorical/exterior-product construction handles the usual graded permutation conventions; no extra unexplained global sign or scalar is licensed. The proof does not require a Künneth component of z to be individually algebraic.

Each K_J is an actual finite mixed product of the possibly different/repeated projective K3 bases. This is where the full imported mixed-base quantifier is needed. Knowing Hodge separately for each M_i and multiplying algebraic cycles is not enough to prove Hodge for arbitrary product classes.

A concrete falsification of that tempting shortcut is the diagonal on S x S. Its action is the identity on the nonzero H^(2,0)(S). If its middle Künneth component were a sum of external products of divisor classes, each such correspondence would act trivially on H^(2,0): pairing a (2,0) class with a divisor has type (3,1), outside the top (2,2) degree of a surface. The remaining H^0/H^4 product pieces cannot supply the missing H^2 action either. Thus the diagonal class is not generated merely by external products of algebraic classes from individual factors, although the diagonal itself is algebraic. This is a counterexample to the shortcut, not to the note's actual correspondence proof.

For mixed S,T, H^4(S x T) contains the middle H^2(S) tensor H^2(T) term. Its Hodge tensors can reflect relationships between transcendental structures, rather than just divisor products. No general vanishing or algebraicity of those tensors was assumed here. A theorem about each separate self-power does not, by formal product closure alone, establish the required theorem for arbitrary mixed factors.

Conversely, choosing every M_i=S_i^[1]=S_i and alpha_i=0 recovers every mixed K3 product. Therefore using the universal moduli assertion itself to discharge the mixed-K3 premise is circular. The route is blocked at an equivalent unsupported central assertion; it can be reopened only by substantive evidence for the actual imported mixed-K3 theorem. The original explicitly recognizes this equivalence, so its corollary should not be mistaken for an independent solution of that central problem.

## Normalization and moduli-scope falsification

The proof needs genuine rational algebraic correspondences with composite identity. A coarse non-fine moduli space need not carry an honest universal family, and the Brauer-twisted situation cannot be handled by assuming one exists. Those are material imported interfaces.

A checkable normalization control: replacing a family E by E direct-summed m times replaces a derived Hom class involving that family in both arguments by m^2 copies of the original class. Chern classes are nonlinear. If N=m^2, then formally

    c_2(F direct-summed N times)=N c_2(F)+binomial(N,2)c_1(F)^2.

For m=2 this is 4c_2+6c_1^2, not an unqualified unchanged diagonal formula. This does not determine the correct quasi-universal normalization; it shows why copying a raw Ext-diagonal identity to an unnormalized family is invalid. The actual Bülles/Markman construction must provide the normalized rational Chow maps. The original remark names this requirement but does not prove it.

If maps gave only sum B_j A_j=lambda Delta_X with lambda in Q nonzero, rational coefficients permit rescaling the B_j by 1/lambda. They do not permit silently doing so for lambda=0, an unknown factor, or an integral-coefficient claim. Multiplication by 2 on a rational vector space has a rational inverse; the analogous integral inverse need not exist. This isolates why the conclusion is rational and cannot be promoted to integral Hodge or a torsion statement.

The exact stable-object scope remains a falsifiable issue. Genericity must be with respect to fixed numerical data; it is not a blanket statement that all stability conditions yield smooth projective spaces. The Gieseker polarization and numerical data are fixed. Nonempty stable loci that are only quasi-projective do not meet the theorem. Singular semistable compactifications are not inserted to make them proper. If the cited Bülles theorem imposed an additional missing condition, or supplied a weaker type of motive, that would be a genuine scope gap requiring disposition, not a reason to quietly weaken the claimed theorem.

Another diagnostic of the claimed splitting is that K3 powers have no odd rational cohomology, and Tate twists shift by an even cohomological degree. A genuine splitting of the stated kind forces odd cohomology of each eligible M_i to vanish. A proposed example within the claimed moduli scope with nonzero odd cohomology would therefore falsify the splitting/scope application. No external example was fetched or asserted here; this is a precise check for the imported interface.

## Remaining boundary cases

- A finite product with an empty factor has empty underlying variety and zero Hodge targets. The product with no factors is instead Spec C; its codimension-zero class is represented by the point and its other targets vanish. These two uses of “empty” must be kept separate.
- A smooth zero-dimensional projective complex scheme is a finite disjoint union of reduced points. Products decompose into finitely many copies of the remaining factors; the transfer applies componentwise. Smoothness rules out hidden nonreduced zero-dimensional pieces.
- Codimensions p<0 or p>dim X have zero cohomological target. Degree zero and top degree reduce to components and points, respectively; they do not exercise the difficult mixed middle-degree input.
- For Hilbert schemes n>=1, ch(I_Z)=(1,0,-n) and sqrt(td(S))=(1,0,1), giving Mukai vector (1,0,1-n), as printed. The n=0 scheme is a point. The n=1 case is a K3 itself, and mixed n_i=1 factors implement the central-equivalence test above.
- Products and index sets must be finite. Infinite products/direct sums would not inherit this finite correspondence sum or even remain the stated smooth projective finite-dimensional varieties.
- A disconnected positive-dimensional space of varying component dimensions would require componentwise treatment of dimension and motive conventions. The fixed-numerical-data moduli theorem must be checked in its exact intended class; it is not a license to apply a single dim X formula to arbitrary disconnected nonpure schemes.
- Being deformation equivalent to a K3 Hilbert scheme, or having a similar Hodge structure, is not the same as possessing the asserted algebraic Chow correspondences. Such extensions were explicitly excluded.

## Exact deferred interfaces and evidence limit

The strongest original-only deduction here is the conditional rational correspondence-transfer proof, including its degree/type arithmetic, tensor assembly, boundary cases and normalization failure controls. No unconditional assertion that every rational Hodge class on the stated moduli products is algebraic has been independently established in INITIAL.

The exact remaining interfaces are:

1. The actual full proof of the pinned OpenAI mixed-K3 Theorem 1.1, with its projective-complex, arbitrary distinct/repeated finite mixed-product quantifiers and every-codimension rational conclusion. A self-power, restricted-locus, motivated-cycle or Clifford/tensor statement alone is insufficient. The geometric Kuga--Satake/algebraicity interfaces underlying that proof must be checked substantively after authorization.
2. The actual full Bülles theorem and construction for this exact twisted stable-sheaf/generic stable-object scope, including smoothness/projectivity, numerical data, quasi-universal normalization and genuine rational algebraic Chow splitting. The asserted absence of new primitivity/fine-moduli conditions must be checked, not inferred from this note's wording.
3. Standard cycle-class, intersection/pushforward and Chow-motive realization facts used in the local reduction. Their types are consistent in the hand reconstruction, but this record is not a full foundational formalization.
4. Historical antecedent and scope assertions about Arapura, Markman, the quadratic-locus companion and universal Kuga--Satake companion. These concern attribution and exact inherited geometry, not a priority conclusion from search absence. No such sources were fetched or opened in this phase.

No native scientific script, imported mathematical program, AST/compiler, test or build was executed. Poppler only extracted/rendered the controlling PDF. The only executed saved readers performed passive byte/topology/metadata custody. The initial custody comparison omitted the manifest's derived hidden_component field; all 49 payload-row differences were exactly that field, with all bytes/modes/hash values equal. Its failure record and reader are preserved; a separately saved, fully read schema-faithful passive reader recorded exact custody. No source repair or scientific-support reading occurred.

After the finite INITIAL manifest/seal, the entire INITIAL namespace is frozen. Further scientific work requires the root checkpoint and explicit RESUME in a separate sibling continuation. No external individual was contacted, no outreach prepared, and no Git/native/config/index/website/spreadsheet/deploy/release/Zenodo action occurred.
