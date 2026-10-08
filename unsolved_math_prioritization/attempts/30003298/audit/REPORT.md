# Independent mathematical audit: problem 30003298

## Verdict

**Accepted as a correct partial result, without a mathematical correction patch.**

The frozen proof establishes infinite rational rank of

    H^(4g-5)(Gamma; H_(2g-2)(C_g; Z))

for every g >= 2 and every torsion-free finite-index subgroup Gamma of the orientation-preserving mapping class group of the closed oriented surface. It answers the original degree 2g-1 precisely at g=2. The disposition remains **unsolved, five approach families** for the general-genus problem. Nothing reviewed here establishes infinite generation in the requested degree for any g>=3.

This is an independent AI-assisted mathematical audit, not conventional human peer review or formal proof-assistant verification. Acceptance concerns the stated corollary and the accuracy of its limitations. It does not certify novelty or worldwide open status. The imported Harer/Bieri–Eckmann and Fullarton–Putman theorems remain deep external dependencies.

The audited author MANIFEST.json has 1,349 bytes and SHA-256

    63f3be3527b07b3cef5b5bc509f3bcd93e78fec442a62f1f59bab0ca9ab3e554

All ten original packet files were preserved byte-for-byte. Their original `independent_review: pending` field is an accurate historical freeze; this separate acceptance report does not rewrite that history.

## 1. Exact target and source qualification

The rendered official report, printed page 3190, was independently inspected. Question 11 uses outer cohomology in degree 2g-1 and coefficient homology in degree 2g-2. The coefficient is not curve-complex cohomology, and the curve complex is not a universal curve. The finite-index subgroup is fixed; varying congruence level cannot silently vary the requested group. The local question omits an explicit genus range, and the packet transparently adopts the closed-surface g>=2 setting. The official repository identifies the workshop/report as 2016. [Official Surface Bundles report](https://publications.mfo.de/handle/mfo/3560).

The two complete dataset byte counts and hashes in PROVENANCE.json were independently recalculated. The problems dataset contains exactly one record with the target ID, equal to the retained exact-record JSON. Its 3,444-byte serialization and hash match. The research dataset contains 6,701 records, no OWR-prefixed keys, and no occurrence of the target ID or code in the checked records. All four local source PDFs match their recorded hashes and byte counts. No dataset or source-document contents are included in this audit deliverable.

The author ledger's chronology and repository-wide duplicate-search history are process reports, rather than mathematical premises. This audit does not claim independently to have reconstructed every historical search or timestamp. Its exact-target source and dataset checks do not establish exhaustive literature or repository absence.

## 2. Imported quotient theorem

The Fullarton–Putman author version was checked in its definitions, the equivariance paragraph on page 9, Propositions 3.10–3.11, the surjectivity proof, and the dimension calculation. Pages 9 and 11 were also visually inspected. The source defines the Steinberg module and target over Q. The map is equivariant for the entire Mod_g, the target action factors through Sp_(2g)(F_p), and choosing the level parameter ell=p supplies a surjection for every prime. The target is the quotient of the special-linear Steinberg module by separated apartments, not the symplectic Steinberg representation. Its dimension is |Sp_(2g)(F_p)|/[g(p^(2g)-1)]. The arXiv page identifies the inspected version as 29 November 2017 and records publication in JEMS 22 (2020), 1261–1287. No final-typeset-PDF inspection is claimed. [Author PDF](https://academicweb.nd.edu/~andyp/papers/HighLevel.pdf), [publication/version metadata](https://arxiv.org/abs/1610.03768).

The simplification of this dimension to

    (1/g) p^(g^2) product_(i=1,...,g-1)(p^(2i)-1)

is correct: the exponent sum 1+3+...+(2g-1) is g^2, and cancellation removes exactly the final product factor. For fixed g this positive polynomial has degree 2g^2-g and positive leading coefficient 1/g, so its values are unbounded along the primes. No finite table is being substituted for that argument.

The packet correctly avoids the inconsistent numerical examples in the source's introductory remark. Direct evaluation gives 324 for (g,p)=(2,3) and 7680 for (3,2). The displayed introductory values differ. A claimed cohomology lower bound need not be an exact quotient dimension; the retained argument imports the precise proposition and needs only unboundedness. Neither the author packet nor this audit purports to resolve the introductory numerical discrepancy or prove the introductory sample bounds separately.

## 3. Duality, actions, orientation, and finite classifying space

The Church–Farb–Putman paper was read, with page 2 visually checked. It states the general-coefficient rational duality formula and identifies the Steinberg module with the homology of the ordinary curve complex. Its geometric account supplies a contractible thick Teichmüller manifold with corners, finite stabilizers, compact quotient, and boundary modeled by the curve complex. It explicitly attributes the deep duality statements to Harer and Bieri–Eckmann. [Author PDF, section 2](https://academicweb.nd.edu/~andyp/papers/TopCohomologyMod.pdf).

The following checks justify the packet's use of that account for the specified Gamma.

1. A torsion-free subgroup has trivial intersection with each finite stabilizer. Hence its action on the thick space is free. A finite-index quotient remains compact. The compact smooth manifold-with-corners quotient has finite CW type, giving a finite BGamma. The cell dimension may be 6g-6; the rationalization argument does not require a free cellular resolution of length 4g-5.
2. The mapping classes under consideration preserve the complex orientation of Teichmüller space. Restriction to its thick part preserves the induced orientation. There is therefore no extra orientation character to insert for this group. This justification would need revision for the extended mapping class group.
3. The dimension shift is consistent at the geometric level: with n=6g-6 and d=4g-5, the boundary degree n-d-1 is 2g-2. The compactly supported cohomology description of the dualizing right module, followed by inversion to a left module, gives the natural curve-homology action. It does not replace that module by its algebraic dual.
4. The integral curve homology is free abelian because the curve complex has the homotopy type of a wedge of spheres in this range. The integral duality statement for the torsion-free subgroup therefore has the ordinary tensor coefficient D_Z tensor A. Under the left-module convention the action is diagonal. For A=D_Z tensor Q, associativity of tensor products identifies this coefficient with D tensor_Q D.

Consequently, the precise top-degree identification used in the proof is

    H^d(Gamma;D) = (D tensor_Q D)_Gamma.

No Hom module, contragredient coefficient, completion, or finite-dimensionality assumption is hidden in that expression.

## 4. Independent check of the finite-image criterion

Every algebraic step in PROOF.md, sections 3–4, is valid.

For a finite rational representation, averaging a rational dot product over the finite image gives an invariant rational symmetric form. Positivity can be checked after embedding Q in R, so the averaged form is nondegenerate. Finite image, not semisimplicity, irreducibility, faithfulness, or finite-group simplicity, is the required property.

For a surjection pi:M->V, the map of a pulled-back form is pi* composed with the isomorphism V->V* and then pi. Surjectivity of pi makes pi* injective, so its rank is exactly dim(V). This factorization is valid for arbitrary M, including infinite-dimensional M, and uses the full algebraic dual.

A finite linear combination of finite-rank operators has image contained in the sum of their finite-dimensional images. Thus a finite-dimensional subspace spanned by finite-rank forms has a uniform finite rank bound: select a finite basis from the generating forms and sum its ranks. Unbounded ranks contradict that bound. This step would be false if one merely knew there were infinitely many forms, but the proof uses the stronger and sufficient rank information.

An invariant bilinear form is a linear functional on the diagonal tensor square and annihilates each coinvariant relation. Restricting invariance from G to any subgroup L is legitimate; no property of a congruence subgroup enters. The association from coinvariant functionals back to forms is injective because elementary tensors span and the quotient map is surjective. Independent forms therefore give independent functionals on the coinvariants.

The final dual argument uses only the elementary contrapositive that a finite-dimensional vector space has finite-dimensional dual. It does not infer equality of infinite cardinal dimensions, identify M with M*, or require a basis of the full infinite dual. The greedy finite-witness version separately proves every desired finite lower bound.

This verifies the central implication from unbounded finite-image quotients to infinite-dimensional coinvariants for every fixed Gamma.

## 5. Integral conclusion and exact genus boundary

Let P_* be the finite-rank free cellular resolution from a finite BGamma. In every degree, Hom_(ZGamma)(P_j,D_Z) is a finite direct sum of copies of D_Z. Tensoring with Q commutes with this finite direct sum and with the differential. Exactness of localization then identifies the cohomology of the rationalized complex with the rationalization of integral cohomology.

The finiteness condition is on the resolution modules, not on D_Z. There is no use of a generally invalid interchange between tensoring and an infinite product. Hence

    H^j(Gamma;D_Z) tensor_Z Q = H^j(Gamma;D)

is justified, and infinite rational dimension in degree d implies infinite rational rank of the integral group, in particular failure of finite generation.

Solving 4g-5=2g-1 gives g=2. For g>=3, the original degree instead corresponds to homological degree 2g-4>0. Neither finite-index transfer nor a quotient argument removes that positive degree. The published-dependency corollary settles genus two without settling the general question.

## 6. Audit of all five approaches

### Approach 1: boundary kernel

The calculation n-q=d and the Poincaré–Lefschetz coefficient convention are correct. With H_d(B;D_Z)=0 imposed, the pair sequence starts with an injection of H_d(M;D_Z)=H^0(Gamma;Z)=Z. Taking the image of the next arrow produces exactly the stated kernel K and short exact sequence. An extension of a finitely generated abelian group by Z is finitely generated, while its quotient K must be finitely generated if the extension is. Thus the equivalence of finite generation is correct. Compactness of B alone does not give finite generation with an infinite-rank local coefficient system.

The Avramidi manuscript's relevant boundary-vanishing and obstruction passages were inspected. Section 6 explicitly uses F_p coefficients, which is another reason not to treat its displayed boundary equation alone as a newly verified integral theorem. Section 9 discusses the primary obstruction, and section 10 poses the broader dualizing-module question. The packet retains the integral boundary condition as a hypothesis rather than depending on a fresh proof of the specialized small-model argument. That is adequate. The author's current publication page still labels this manuscript under revision, and arXiv lists the 2017 version. [Manuscript](https://arxiv.org/abs/1701.00309), [author publication list](https://sites.google.com/site/gavramidi/papers).

### Approach 2: transgression

For g>=2 the fiber is simply connected, with nonzero rational homology only in degrees 0 and m=2g-2. The pulled-back local system is constant on the fiber. The coefficient universal coefficient theorem therefore gives D on the bottom row and the full Hom_Q(D,D) on the upper row, with the stated conjugation action. The Borel boundary model is compatible with the equivariant curve-complex model; it does not require the ordinary quotient of the curve complex to be B.

In this first-quadrant two-row spectral sequence, d_(m+1) is the only possible inter-row differential. There is no entering differential at (0,m), and no outgoing one from (q,0). The edge image at the former is its kernel; the latter's cokernel is the last nonzero filtration subspace in total degree q and injects into H^q(E;D). This establishes the exact segment as written. The identity transgression agrees with the primary section obstruction up to sign by the cellular attaching-sphere construction.

The endomorphism quotient remains uncomputed. The successful invariant bilinear forms are maps to D*, so they cannot be inserted here as endomorphisms without an additional argument. The packet correctly stops at this gap.

### Approach 3: positive-degree coefficient homology

The duality shift and the coefficient long exact sequence are correct. In positive homological degree, a coefficient surjection need not induce a surjection in homology; the displayed connecting map is exactly the obstruction.

The countermodel also checks out. Under the diagonal Z action on Q[Z] tensor Q[Z], the difference b-a indexes orbits and the coordinate a is a regular-module coordinate. Hence the module is a direct sum of regular modules. Multiplication by t-1 is injective on each Laurent-polynomial module and their direct sum, but the coinvariants have one Q for every difference. The standard length-one resolution gives zero homology in every positive degree. This refutes the formal degree-zero-to-positive-degree inference, not the mapping-class question itself.

### Approach 4: finite-index transfer

For a rational Gamma-module, corestriction after restriction is the subgroup index times the identity, with coefficient transport included. Restriction is therefore split injective. If the subgroup is normal, averaging makes invariants exact for the finite quotient even for infinite-dimensional rational representations, so the stated Lyndon–Hochschild–Serre collapse is valid.

For the sign-action countermodel, t-1=-2 on A is invertible, while t^2-1=0. Thus H^1(Z;A)=0 and H^1(2Z;A)=A. This explicitly defeats unrestricted upward propagation. The example is correctly presented as a general coefficient countermodel, not as a model for D.

### Approach 5: finite-image forms

This route is the fully established argument audited in sections 2–5 above. It keeps Gamma fixed while changing p. The resulting forms are already invariant under the full mapping class group, so restriction is immediate. Its exact success and its remaining positive-degree gap are both stated accurately.

## 7. Executable and adversarial verification

The author's verifier is an integrity/scope check and finite diagnostic suite. It is not a mathematical proof checker, and the packet explicitly says so. A self-contained manifest can be recomputed after changing prose; therefore its own hash checks alone cannot authenticate the author freeze. This is a normal scope limitation, not a proof defect.

The independent verifier pins all ten author file hashes, including MANIFEST.json, outside that packet. It imports none of the author's implementation. It independently checks symplectic-order arithmetic, the degree boundary, an averaged non-orthogonal rational order-three representation, a non-coordinate surjective pullback, exhaustive 2-by-3 binary-matrix rank subadditivity, and finite Laurent-differential controls. These are diagnostics of the elementary mechanisms, never finite substitutes for the general proof.

Observed results:

- Independent verifier: PASS, 4,398 checks in each of normal, -O, and -OO.
- Independent hostile suite: 40 rejected mutations per mode, 120 total. Cases include altered mathematical scope, malformed/duplicate/nonfinite JSON, wrong data types, missing/extra files, symlinks, directory substitution, unsafe manifest paths, and changed proof/verifier/metadata with a recomputed self-manifest.
- Read-only relocation: PASS in all three modes; an actual write probe failed; before/after file hashes were identical.
- Author verifier: PASS, 13,830 checks per mode, identical outputs.
- Author hostile harness: PASS, 20 rejected mutations per mode, 60 total, including its own read-only checks.
- Original frozen packet: unchanged after all tests.

The independent pinning rejects rebound mutations at the integrity boundary. It does not claim to exercise semantic parsing of every malformed document after that boundary; the author's separate harness supplies additional parser/schema controls. Assertions are not used to enforce either verifier's acceptance criteria, so optimization does not disable those checks.

## 8. Disposition and residual limits

No mathematical correction patch is required. Preserve the frozen author packet and retain this audit alongside it. Acceptance is for the top-degree theorem, the genus-two answer, and the five-route account as a partial investigation. Keep the original general problem marked unsolved with five approaches.

A bounded current-source check found no reason to change that disposition. The checked later papers concern different groups, coefficients, or ordinary cohomology, rather than resolving this exact twisted target. That comparison is not an exhaustive negative literature theorem. [Punctures and boundary continuation](https://arxiv.org/abs/2003.10913), [handlebody duality paper](https://jep.centre-mersenne.org/articles/10.5802/jep.341/).

This audit contains authored analysis, source titles/links, and verification metadata only. It performs no publication, remote writes, or changes to the author packet.
