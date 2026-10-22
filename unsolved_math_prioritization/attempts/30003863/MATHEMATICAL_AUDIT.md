# Independent mathematical audit: del Pezzo complement extension

Public proof-only edition. Recorded audit date: 10 October 2026. This AI-assisted audit is unrefereed; acceptance does not mean external human peer review or journal acceptance.

## Verdict

**ACCEPT_SCOPED_PARTIAL_RESULTS. The full conjecture remains unproved.**

This edition binds the distributed [PROOF.md](PROOF.md): 23,737 bytes, SHA-256 `bc5e0d4920cf8f943fce3ab65c19cbdc657608afc2e77e627a3a79421d3798ae`. The accepted proof's complete mathematical argument and explicit control formulas are preserved. Editorial changes remove private coordination, clarify historical computational evidence, reconcile the summary with Corollary 3.3, and state public review limits. No mathematical correction was required. The original proof package was read without modification; edition preparation independently checked its frozen byte identities.

The packet supplies valid elementary restrictions, complete results for explicitly specified pointwise projection kernels, and finite certificates for individual proposed nonambient maps. It supplies neither a proof nor a counterexample to problem 30003863 / OWR-16169-010. No novelty certification is made.

No blocking mathematical error was found. The explanations below expand several compressed steps, particularly the weighted local argument and the inverse-degree bound. No candidate patch is required for scoped acceptance.

## 1. Exact target and prior credit

The original question is Park's Conjecture 5 in the contribution on printed pp.1728–1730 of Oberwolfach Report 28/2018. Its ambient space is fixed. It includes polynomial degrees one, two, and three in P³, as well as a quartic in P(1,1,1,2) and a sextic in P(1,1,2,3), with integral normal Du Val boundary. The proposed equivalence concerns absence of an anticanonically polar cylinder and extension of **every** complement automorphism. The plane and quadric cases cannot be silently dropped merely because their anticanonical degrees exceed three. Their anticanonical degrees are nine and eight, respectively.

The candidate states this scope correctly. It does not confuse the already established cylinder equivalence with the all-automorphism assertion. The original source was read on pp.1728–1730; its ambient list and conjecture were independently visually checked on physical pages 45–46. [Original report](https://ems.press/content/serial-article-files/46750).

The credited prior results were checked in the locally hash-verified primary files:

- Cheltsov–Dubouloz–Park, Theorem C / Theorem 4.4 and Corollary 4.10: the polar-cylinder direction; Theorem 4.1: full extension for smooth anticanonical degree one, and absence of positive-dimensional connected algebraic groups for smooth degrees two and three; Theorem 4.3: the stated singularity classification of cylinder-free surfaces. The inspected local version is arXiv:1712.09148v1. [Primary arXiv record](https://arxiv.org/abs/1712.09148).
- Park, Theorem 1.5 and Corollary 3.2: the classification and cylinder equivalence. The latter is not the full extension conjecture. The live web-tool request failed, but the independently read local primary PDF matched its accepted byte count and hash. [Institutional manuscript](https://cgp.ibs.re.kr/files/preprints/CGP18017_JHP_Ga-Actions%20on%20the%20complements%20of%20hypersurfaces.pdf).
- Cheltsov–Park–Prokhorov–Zaidenberg, §4.2, especially Theorem 4.20, Corollary 4.22, Theorem 4.23 and Conjecture 4.24: the same essential distinction is preserved in the published 2021 survey. Its actual §4.2 setup concerns anticanonical degrees at most three; the original question additionally names ordinary planes and quadrics, which the candidate separately handles. Printed p.83 was visually checked. [Published survey](https://ems.press/content/serial-article-files/37019).
- Blanc–Poloni–Van Santen, *Complements of hypersurfaces in projective spaces*, JEP 11 (2024), 733–768: p.734 explicitly distinguishes the unresolved smooth-cubic extension question from singular-cubic negative results. Proposition 2.1 and Remarks 2.2–2.3 provide the homogeneous lift and composition background. Proposition 5.22 establishes nonextension for singular irreducible cubics and does not settle smooth cubics. The PDF was opened through the web tool and the local copy was independently read and hash-checked; p.734 was visually checked. [Published paper](https://www.numdam.org/item/10.5802/jep.264.pdf).

These are dated, bounded source checks. They do not establish worldwide current openness or originality of the candidate's elementary lemmas. Some cited arguments are presented over C; the stated characteristic-zero application is compatible with the usual finite-type descent/spreading argument. No characteristic-positive extension is accepted here.

## 2. Cylinder direction and additive actions

The candidate correctly credits the geometric implication from a polar cylinder on S to a cylinder and additive action on U. For a principal cylinder open set of an affine variety, differentiation along its A¹ coordinate gives a locally nilpotent derivation on the localization. The inverted function is a unit on the cylinder and hence independent of the A¹ coordinate. Multiplication by a sufficiently large power clears denominators and gives an LND on the original affine ring. For nonprincipal open cylinders the relevant finite divisor-class argument is part of the cited results, rather than a consequence for arbitrary affine varieties.

The independent LND argument in §2 is sound. In a three-dimensional domain, the kernel of a nonzero LND has transcendence degree two. Choose arbitrarily many linearly independent invariant functions. Their multiples of the LND commute, and their exponentials define a regular Ga^N action. Faithfulness is especially transparent by choosing an element b with δb nonzero and δ²b=0: a nonzero invariant multiplier f sends b to b+fδb. Thus the action kernel is trivial.

The dimension comparison is understood in the algebraic-action sense, not as a statement about abstract groups. The stabilizer Aut(P,S) is a finite-type algebraic group: the weighted projective ambient has a preserved ample polarization, and the ordinary ambient is PGL₄. A regular family of automorphisms whose members all extend lies in that algebraic subgroup of the automorphism ind-group. It cannot contain faithful Ga^N actions for unbounded N. This validates the nonextension conclusion. Conversely, absence of Ga actions, or even absence of every positive-dimensional connected algebraic subgroup, does not control arbitrary discrete automorphisms. The candidate never makes that invalid converse inference.

## 3. Cubic degree, Jacobian, and contraction restrictions

### 3.1 Reduced tuple and homogeneous Jacobian

For a reduced homogeneous tuple G representing a rational map on smooth P³, regularity at a point implies that the tuple is a local scalar times a tuple with a unit coordinate. If that scalar vanished at the point, factoriality of the regular local ring would give a codimension-one divisor common to every G_i. Its closure would be a common global homogeneous factor. Thus a primitive tuple has no removable base point on the regularity domain. In particular it has no common zero above U.

On the affine cone open F≠0, F(G) is nowhere zero. The units of k[x₀,x₁,x₂,x₃,F⁻¹] are cF^r because F is irreducible. Comparing degree gives F(G)=aF^m.

The map G on this cone is not claimed to be an isomorphism. Its differential is nevertheless invertible there: it induces the isomorphism dφ on the quotient by the radial tangent direction, and maps the radial vector x to mG(x). Here m is nonzero because the field has characteristic zero. Therefore det(DG) is nowhere zero off F, so it equals bF^e with 3e=4(m−1). This yields m≡1 mod 3. The same reasoning applies to the reduced inverse tuple, independently.

If a birational map maps a prime divisor dominantly to a divisor, the generic local DVRs are identified: in the common function field, one DVR dominating another DVR must be the same DVR. If S were not contracted, its target would be S. Since a reduced tuple has some G_j nonzero generically along S, pulling back the local target equation gives aF^m/G_j³, with valuation m. Equality of the generic DVRs forces valuation one. Hence m>1 contracts S. Every other divisor intersects U and cannot be contracted. Degree one gives an invertible linear tuple. The theorem is valid without requiring the cubic itself to be smooth or Du Val; irreducibility suffices for this paragraph.

### 3.2 Radial-to-projective conversion and valuation inequality

On x_i=1 and target coordinate G_j≠0, the projective Jacobian is det(DG)/(mG_j⁴), up to sign. One way to verify the factor m is to differentiate the four-vector G in one radial and three affine directions, use Euler's identity, and then pass to three ratios G_a/G_j. Both denominator exponent four and the scalar m are required. The selected G_j is a unit at the generic point of S. Coordinate changes to regular target parameters have unit Jacobian and do not alter this valuation. Thus the projective Jacobian has valuation 4q for m=1+3q.

For h_i=t^{a_i}u_i near the generic point of a smooth source divisor, expanding their differentials shows that a nonzero term in dh₁∧dh₂∧dh₃ has at most one contribution involving dt. Its order is at least a₁+a₂+a₃−1. The determinant therefore has at least this order, even when cancellation increases it. This explains the correct direction of the inequality in the proof.

For a smooth target cubic and a point center, a₁=m and a₂,a₃≥1, so 4q≥m+a₂+a₃−1 implies q≥a₂+a₃≥2. For a curve center, choose a transverse local equation inside S, and a rational parameter along the curve with order zero. Separability in characteristic zero provides an independent third differential generically. The same estimate gives q≥a₂≥1. Hence degree four cannot contract the smooth cubic to a point, and a curve center in degree four has transverse order one. Smoothness is essential to these parameter choices. No assertion is made that curve centers are impossible.

### 3.3 Inverse-degree bound

The added Corollary 3.3 is correct for reduced birational maps of P³. The inverse base locus has codimension at least two. A general line misses that locus and meets the common isomorphism open set. Restricting the inverse degree-n tuple to this line gives a basepoint-free degree-n linear system on P¹ and a morphism birational to its image. Consequently that image curve has degree n, with no division by a covering degree.

The curve is contained in the two degree-m equations obtained by pulling back the planes defining the line. General pairs of members of a primitive dominant linear system have no common divisorial component: after choosing the first member, a general second member avoids its finitely many irreducible factors, since none is fixed by the entire system. The image curve is a component of this proper complete intersection, whose total degree is m². Bézout gives n≤m². Exchanging forward and inverse maps gives m≤n².

For m=4, n cannot equal one because the inverse of a linear automorphism is linear. Combining n≤16 with n≡1 mod 3 gives exactly {4,7,10,13,16}. This is a finite inverse-degree list conditional on forward degree four, not a global bound on automorphism degrees.

## 4. Smooth-cubic pointwise projection kernels

The theorem assumes π_p∘φ=π_p, with the base fixed pointwise. Preservation of a pencil up to any nontrivial base action is a different assertion and is not proved.

If p∈S, smoothness ensures that the t² coefficient L is nonzero; if p∉S the t³ coefficient is nonzero. Dehomogenizing a base coordinate preserves irreducibility of F, and Gauss's lemma gives an irreducible polynomial of degree two or three in t over K=k(P²). It is separable in characteristic zero.

The generic line with p removed is A¹_K; the cubic removes the closed degree-two or degree-three point. Its P¹ completion has one more boundary point, infinity. Infinity is the only K-rational missing point because the polynomial is irreducible of degree at least two. Every automorphism of the open smooth rational curve extends to its smooth projective completion and must preserve the boundary and residue-field degrees. It therefore fixes infinity and is affine t↦at+b.

If p∈U, the rational projection is undefined at p, but deleting p and φ⁻¹(p) removes no point dominating the base. This still gives inverse maps of the generic fiber. Alternatively, linewise preservation forces φ(p) to lie on every line through p and hence to equal p. There is no missing generic-fiber obstruction in this case.

For degree two, the only possibilities are identity and reflection −t−Q/L. If L does not divide Q, the homogeneous tuple [Lu₀:Lu₁:Lu₂:−Lt−Q] is defined on a dense open set of L=0 and sends it to p∈S. That dense open set meets U; it contradicts an automorphism of U. If Q=LM, cancellation produces a projective linear involution preserving F. It is genuinely nontrivial in characteristic zero. This establishes the claimed trivial/order-two alternative without needing an external Eckardt-point classification. In the smooth setting the divisibility condition is the familiar Eckardt situation.

For degree three, centering removes the quadratic term. An affine permutation of the three roots must have zero translation, since their sum is zero. Comparing v³+Av+B with its transform gives (a−a³)A=0 and (1−a³)B=0. Irreducibility forces B≠0. Therefore a³=1; if A≠0 then a²=1 also, so a=1. If A=0, the three constant cube roots of unity give the cyclic kernel. The coordinate change v=t+L/3 and every resulting transformation are globally linear. Equality on the generic fiber determines the rational map, and hence determines the automorphism on dense U. Globalization is justified.

Nothing in this reasoning proves that an arbitrary complement automorphism preserves one of these projections, even up to a base action.

## 5. Weighted local lemma and double-cover kernels

### 5.1 Nonzero square coefficient

This is the most delicate local step, and it is valid under the stated normal Du Val hypotheses.

If the w² coefficient vanished, the w-vertex would lie on S. The index chart is A³/μ₂ with weights (1,1,1) for the quartic, and A³/μ₃ with weights (1,1,2) for the sextic. All nonzero weights are coprime to the group order, so each action is free off the origin. The local defining equation f after setting w=1 is invariant, because its weighted degree is 2r.

The inverse image T=V(f) is a hypersurface. Its quotient is the local S: invariants commute with quotient by invariant f in characteristic zero, by the Reynolds operator. Off the origin this is the étale pullback of a normal surface, hence is normal there. In particular it is generically reduced. A hypersurface is Cohen–Macaulay and S₂. Every codimension-one point lies away from the isolated origin, so R₁ holds. Serre's criterion gives normality of T. This reasoning also rules out problematic multiple components through the origin; it is not an unjustified assumption that a finite pullback is automatically normal at the branch point.

Adjunction gives a free dualizing module for T. The residue of the ambient three-form divided by f transforms with character equal to the sum of the three weights minus the character of f. The latter is zero; the former is 3≡1 mod 2 or 4≡1 mod 3. Thus the residue generator has nontrivial character in both cases.

If S were Gorenstein at the vertex, pull back a local canonical generator. Étaleness identifies it with an invariant generator of ω_T on the punctured local surface. Relative to the residue generator its multiplier, and the reciprocal multiplier, are regular on that punctured surface. Normality and codimension two extend both over the origin. They still multiply to one, so the multiplier is a unit, not merely a nonzero function that might vanish at the origin. Invariance would require this unit to transform by the inverse nontrivial character. Evaluating at the fixed origin contradicts its nonzero residue in k. Since Du Val singularities are Gorenstein, the w² coefficient cannot vanish.

Completing the square uses a weighted-degree-r polynomial and defines a triangular graded automorphism of the **same** weighted projective ambient. It does not change the problem's ambient space.

### 5.2 Fiberwise double-cover theorem

Over the dense base chart x≠0, W=w/x^r is an ordinary affine coordinate. The generic quadratic is irreducible because S is integral. The rational missing-point argument from §4 again forces affine transformations, and an affine permutation of two distinct roots is identity or the deck reflection. In completed-square form it is W↦−W; in the original coordinates it is w↦−w−A. These formulas are weighted homogeneous ambient automorphisms. Equality generically determines the original automorphism throughout U.

The w-vertex is outside S after the square-coefficient lemma, but it is omitted in forming the rational projection; it cannot dominate the base, so its presence in U does not change the generic-fiber argument. Singularities elsewhere in the base or surface likewise do not alter this dense function-field computation. The accepted result concerns the pointwise kernel only, not preservation of the projection by the full automorphism group.

## 6. Polynomial certificates and explicit controls

The certificate proposition is correct. F(G)=aF^m and F(H)=bF^n ensure neither tuple vanishes simultaneously on F≠0, and both maps preserve that open set. The two composition identities give mutually inverse projective maps. A primitive degree-m tuple with m>1 cannot represent a projective linear map, since two primitive tuples for the same projective map differ by a scalar.

Conversely a polynomial tuple representing identity has components Kx_i with polynomial K. For example, pairwise relations x_jP_i=x_iP_j and coprimeness of the coordinates show divisibility by every corresponding x_i and equality of the quotients. K is nowhere zero off F because both maps are defined there. Thus K is a scalar power of F. Homogeneity determines s=(mn−1)/3. The same argument applies to the reverse composition. The proposition does not require H to be separately primitive for sufficiency; primitivity of G suffices to establish nonambientness. Conversely both tuples can be chosen reduced.

The original candidate's recorded verifier checked its listed fixtures, with all scalar constants specialized to one except the Jacobian constants. It is not advertised as a general parser for arbitrary coefficient certificates, an infeasibility solver, or an exhaustive search. An actual counterexample to the original conjecture would additionally require a cylinder-free boundary. The E6 fixture does not meet that condition.

Independent exact arithmetic reproduced all five fixtures without importing the author's code or SymPy. The independent implementation uses sparse rational-coefficient polynomial dictionaries, full simultaneous substitutions in both directions, and a permutation expansion of the Jacobian determinant.

### Primitivity and geometric status of the controls

- Plane: the gcd of the last three coordinates is x₃, and the first coordinate reduces to x₁² modulo x₃. The whole tuple is primitive. The degree-two triangular map is nonambient. The complement is A³, and on S=P², three times a line is anticanonical with A² complement.
- Rank-four quadric: the first and fourth coordinates have gcd F, and the third reduces to x₀³ modulo F. Irreducibility of F and F∤x₀ give primitivity. The exact forward and inverse identities hold.
- Rank-three quadric: the first three coordinates have gcd F, and the fourth reduces to x₀³ modulo F, again giving primitivity. Rank three gives a normal A1 cone. On both quadrics the x₀≠0 chart of S is A², and twice the hyperplane divisor is anticanonical. Both sides of the conjectured equivalence are false in all these cases.
- E6 cubic: as a polynomial linear in x₀, it is primitive and irreducible because gcd(x₁²,x₁x₂²+x₃³)=1. Its partial derivatives force the unique projective singularity [1:0:0:0]. It is normal by R₁ and the hypersurface S₂ property. The local change y↦Y−z²/2 gives Y²+w³−z⁴/4. Its Jacobian ideal is generated by Y,z³,w² and has a six-dimensional quotient, consistent with the E6 normal form. The x₁=1 chart is A² and gives the stated polar cylinder.
- E6 tuple primitivity follows from the second and fourth coordinates having gcd F², whereas the first reduces to −x₁⁷ modulo F. The invariant derivation and exponential construction are correct; its second-order term retains the same sign in the inverse. Both complete compositions are xF¹⁶ and both determinants are 7F⁸.
- Fermat: coordinate transposition is a primitive linear involution, with determinant −1. Smoothness follows from the four cubic partial derivatives. It is ambient and supplies no nonlinear counterexample.

The independent negative controls show why each certificate condition matters. The inflated tuple x_iF actually passes the relevant one-sided and composition identities but is visibly nonprimitive. A changed E6 forward coefficient fails the boundary identity. Reversing the second-order inverse sign fails composition. Pairing the E6 map with itself satisfies both one-sided boundary identities while failing inverse composition. A wrong Jacobian scalar is also rejected. These checks remain active under optimized Python.

## 7. Verification, provenance, and limits

The frozen manifest pin and all 14 allowlisted files were checked. The original author's checker was run normally and with `-O`; both result files exactly match the frozen recorded results. Its seal verifier passed in both modes. Its negative seal tests rejected altered, unlisted, and missing files in temporary copies.

The independent checker passed normally and with `-O`, with identical JSON output. It verifies 40 fixture checks, five negative controls, and eleven generic/local/arithmetic checks. These finite polynomial checks support the displayed constructions, not the universal geometric theorems; those were audited separately above.

All five relevant source PDF byte counts and hashes were independently recomputed during the audit. [SOURCE_METADATA.json](SOURCE_METADATA.json) records their public identity and historical inspection scope. No source body is reproduced in this report. The audit used an external manifest pin; independent integrity controls rejected a resealed altered candidate against that original pin. A final whole-input comparison verified that every original candidate file was unchanged.

Edition preparation rechecked frozen byte identities and publication integrity but did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection, or literature search. The recorded exact computations are supplementary historical evidence. The complete mathematical arguments, polynomial certificate criterion, and explicit controls are included here and in the proof; no analytic claim depends on an omitted executable or raw output. Programs, raw outputs, datasets, copied source documents/text/images and private coordination material are excluded.

Remaining mathematical gaps are exactly substantial: arbitrary smooth-cubic automorphisms; arbitrary cylinder-free weighted cases beyond the credited smooth degree-one theorem; preservation of any useful projection by an arbitrary automorphism; and exclusion or construction of nonlinear certificate solutions in unbounded degree. No combination of the accepted kernel results removes these gaps.

No source copies are redistributed in this edition. The original audit made no repository or queue modification.
