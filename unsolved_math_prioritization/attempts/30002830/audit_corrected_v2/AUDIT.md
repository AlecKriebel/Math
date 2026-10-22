# Independent adversarial audit: Ueno birational modifications, 30002830

## Verdict

**SCOPED PASS. NO RESOLUTION OF RATIONALITY.** The five retained routes and their expressly limited conclusions are mathematically sound. No mandatory mathematical correction to the frozen author-safe-v1 packet was identified. In particular, the strongest positive conclusion is the existence of a rational fourfold with a generically finite dominant rational map of degree exactly three to X_{4,6}. It is not a rational inverse, and it does not settle the method question.

The two other finite-map conclusions point in the opposite direction: X has a rational quotient of degree two under the coefficient-net involution and a rational quotient of degree 24 under factor permutations. The mixed K3 fibration and Newton-width result obstruct particular relative or monomial constructions only. Neither is a total-space nonrationality argument.

This audit independently read the whole authored proof, the original method question, the cited diagonal-cubic criterion and coefficient-net discussion, and the controlling corrections to the adjacent 30002829 model. It rebuilt exact checks without importing the author's verification code. Geometric theorem dependencies remain mathematical proofs, not computer-formalized assertions.

## Frozen input and evidentiary scope

The author's manifest SHA-256 is

`d9e4ec28d3ccab08918a952bc6e448366f451d8abebaca72f292aa9e2a4e8494`.

The supplied UENO_METHODS_30002830_SAFE_V1.zip SHA-256 is

`8d3c73ef5321e5722260ee27e69ec465926cedcbff0965b52b3523b91fcd3fbf`.

The archive is bound byte-for-byte to the frozen tree, including its complete member list. The nine manifested authored files and the two manifest files are preserved unchanged. Input metadata and file bindings are recorded separately in input_bindings.json. No source PDF, extracted source text, image, raw dataset record, connector response, or private coordination file belongs to this safe output.

Fresh independent downloads of the official OWR PDF and the Catanese-Oguiso-Verra (COV) PDF matched the supplied source hashes and byte counts. OWR printed page 819 and COV pages 13 and 15 were freshly rendered and visually inspected. OWR page 819 supports the method-specific rationality target and the coefficient-net suggestion. COV Theorem 3.5 supplies the diagonal-cubic criterion used in Route 2; its Section 4 supplies prior context for the net. [OWR report](https://doi.org/10.4171/owr/2015/15), [COV paper](https://arxiv.org/abs/1506.01925).

The live target again returned HTTP 403. Its full live contents and the complete imported statement and prior AI report were not inspected. Descriptor hashes have not been independently recomputed from full imported records. The original public source establishes the scope used here; it does not remove those limits. A method-specific record is not automatically a duplicate of the adjacent general rationality record. Conversely, distinct record IDs do not establish mathematical independence or novelty. No exact duplicate/prior-attempt skip has been certified in this audit.

Mellit's supplied v3 PDF was independently rehashed and its conditional introductory theorems inspected. Its current arXiv landing page also expressly reports that the experimental conclusion is not rigorously justified. Oguiso's supplied 2024 v3 PDF was independently rehashed; Remark 1.3(3) was inspected and its current landing-page version checked. These checks do not certify global current openness. [Mellit](https://arxiv.org/abs/1705.02931), [Oguiso](https://arxiv.org/abs/2401.04386).

## 1. Shared field model and corrected open

Put a=st(s-t), b=-s(s-1), c=t(t-1), d=-(s-t)(s-1)(t-1). The projective generic fiber over K=C(s,t) has equation

`a x^3 + b y^3 + c z^3 + d v^3 = 0`.

All four coefficients are nonzero in K. Its four partial derivatives are nonzero coefficient multiples of x^2,y^2,z^2,v^2, so they have no common projective zero even after extending K to an algebraic closure. Thus the cubic is geometrically smooth. A projective hypersurface in P^3 of positive degree is connected; if this cubic had distinct geometric components, their positive-dimensional projective intersection would be singular, and a repeated component would also be singular. Consequently it is geometrically integral. Its affine v=1 chart has the same property.

The affine polynomial F=aU+bW+cV, where U=x^3-1, W=y^3-1, V=z^3-1, is primitive over C[s,t]: its coefficient content divides gcd(a,b,c)=1. Gauss's lemma therefore proves integrality of this fourfold equation itself. This is a valid strengthening for n=4; it does not repeat the false integrality claim about the unsaturated n=5 intersection found in the preceding audit. There is a unique component dominating the base, and here it is the whole affine hypersurface.

The packet explicitly retains the corrected nonempty open with q+2 inverted. Its identities imply

`q+2 = 2s(s-1)U/(s^2 U-V)` and `T-1 = U/(q(q+2)-U)`.

Thus all stipulated factors ensure T(T-1) is nonzero. The independent verifier reconstructs each elliptic relation, recovers q from original ratio data, and checks the model equation in the opposite composition. It also retains the exact bad point s=t=0, U=V=W=1: the older product is nonzero but T=0. The corrected open excludes it. A separate witness s=3,t=5,U=2,V=7,W=40/3 demonstrates nonemptiness without relying on the author's witness.

The invariant ratios generate the fixed field: adjoining the first elliptic x and y coordinates generates the full product field with degree at most six, and the faithful order-six diagonal group forces equality by Artin's theorem. Taking roots in the reconstruction supplies points upstairs; it is not a rational inverse on the covering product. The quotient-field inverse uses invariant ratios alone.

## 2. Coefficient-net involution and exact degree-two quotient

The elimination t=-Cs-A and the quadratic in s are correct. Completing the square yields e^2=-AC(A+C+1). The displayed inverse is valid on a nonempty dense open, and both compositions were independently checked after reducing modulo that relation. Vieta's formula independently reproduces the stated involution on s,t. It fixes A,C, sends e to -e, squares to the identity, and is nontrivial at a valid witness.

After eliminating C using AU+W+CV=0 and setting R=eV, the radicand is exactly

`A(AU+W)[A(V-U)+V-W]`.

Its A-adic order is one, since its coefficient of A is W(V-W), which is nonzero in C(x,y,z). Here U,V,W remain algebraically independent: adjoining their cube roots produces algebraic extensions and no relation among x,y,z is being imposed. Hence the radicand is nonsquare and the degree is exactly two. This establishes the rational subfield and identifies it with the involution's fixed field; it does not establish rationality of the quadratic extension.

The terminology “Geiser-type” is suitably qualified. The seven net base points are special; the blowup has (-2)-curves, so the proof must not rely on ample anticanonical class for a smooth del Pezzo model. The author explicitly avoids that pitfall. No global morphism is claimed for formulas with excluded denominators.

## 3. Rational covering fourfold of exact degree three

The pairing identity ab/(cd)=s^2/(t-1)^2 is correct. With u^3=s/(t-1), the extension K'=C(u,t) over K has degree three. Indeed s/(t-1) has s-adic valuation one and is not a cube; a reducible cubic Z^3-s/(t-1) would have a root in K. Since C contains the third roots of unity, this is a cyclic extension.

The pairing becomes u^6=(u^2)^3. The notation in COV Theorem 3.5 uses ac/(bd), with permission to permute the four coefficients; choosing the permutation (a,c,b,d) makes it the required ab/(cd). The base-changed cubic is still geometrically smooth and contains (1:1:1:1). Thus every hypothesis of the theorem's sufficiency direction holds. Its function field is K'(rho,sigma), hence rational over C because K'=C(u,t).

The degree assertion requires a separate argument and the author provides the correct one. Geometric integrality of the original cubic makes its function-field extension of K regular. Equivalently, base extension to K' keeps its generic fiber integral, so K' and C(X) are linearly disjoint over K. Their compositum therefore has degree exactly three over C(X). This rules out a hidden pre-existing cube root in C(X), which would otherwise collapse the covering degree.

The deck transformation u -> omega u, with the original base and fiber coordinates fixed, has fixed field C(X). An arbitrary rational coordinate system rho,sigma supplied by the theorem need not make that action linear or make its invariant field manifestly rational. The absence of explicit rho,sigma does not invalidate existence of a rational covering variety; it does prevent claiming an explicit rational parametrization from these formulas alone. The cyclic descent problem remains completely real. In particular, odd degree is not a substitute for degree one.

## 4. Symmetric-product quotient and its exact degree 24

The S4 permutation action commutes with the diagonal G-action, giving equality of the relevant fixed fields and the birational identification with Sym^4(E)/G. The Abel-Jacobi morphism Sym^4(E) -> E is a P^3-bundle: a degree-four line bundle on a genus-one curve has four independent sections and H^1=0. This is also consistent with the inspected standard symmetric-power bundle theorem. [Hu-Dauser note](https://people.math.ethz.ch/~rahul/Projective_bundle_over_Jacobian.pdf).

The degree-four divisor p+3O defines a section. The order-six elliptic automorphisms fix O and respect the group law, so both map and section are equivariant. Over the generic point of E/G, E is a G-torsor. The descended fiber is a form of P^3, and the equivariant section supplies a rational point on that form. The Brauer-Severi splitting theorem then makes it P^3. Finally, C(E)^G=C(x_1^3), a rational one-variable field. The rationality conclusion for this quotient follows without an unjustified global projective-bundle assertion over singular fibers.

For faithfulness, any permutation acting trivially on C(E^4)^G must belong to the Galois group of C(E^4) over that fixed field, namely G. The intersection of the permutation subgroup with the diagonal elliptic-automorphism subgroup is trivial: moving an independent factor cannot act as an automorphism within each factor. Therefore S4 acts faithfully on C(X), and Artin's theorem gives extension degree 24. The verifier enumerates distinct coordinate permutations only as an arithmetic check; the field-theoretic faithfulness proof is the preceding argument.

The rational quotient is a subfield, not the ordered field itself. Recovering an ordering is not a rational operation merely because the unordered parameters are rational. The packet correctly stops short of that inference.

## 5. Mixed projection, singular branch sextic, and K3 resolution

Viewing F as a quadratic in t over C(s,x,y,z) gives the stated coefficients and discriminant. Completing the square is an exact function-field operation on V-sU nonzero. Set L=C(s,x); its geometric generic surface is a double plane branched over the displayed sextic B.

The conic Q beneath the coordinatewise cube map has determinant -4U^2s^4(s-1)^4. Each coordinate-side restriction was independently checked, including the first restriction's discriminant k0^2(U+1). At the generic point of L, every listed factor is nonzero, including U+1=x^3. Thus each side intersection away from vertices is simple. The cube map is etale off the coordinate triangle, and on the interior of each side its unramified tangent direction has nonzero derivative. These facts rule out singularities away from the listed vertex.

The conic meets exactly the vertex [1:0:0], whose pullback has tangent cone k0(z^3-B0 v^3). Because B0 is nonzero, its three geometric tangent lines are distinct. There are no lower-degree local terms. This establishes an ordinary triple point and excludes any nonreduced branch component, since such a component would be singular at all of its general points. It is the only branch singularity.

There is an additional independent local check in the blowup chart z=r v. Dividing B(1,r v,v) by v^3 gives

`k0(r^3-B0) + v^3[(A0-r^3)^2-k0(r^3-B0)]`.

At v=0 the roots are simple, with derivative 3k0 r^2 nonzero at r^3=B0. Therefore the strict branch is smooth and intersects the exceptional line transversely at three distinct geometric points. Normalizing the cover replaces the local double-cover coordinate h by h/v, producing a branch factor v times the strict branch. This confirms that the exceptional line must be included, rather than treating the blown-up sextic transform alone as the branch.

The branch class is consequently (6H-3E)+E=6H-2E=2(3H-E). Since K_R=-3H+E, the double-cover canonical divisor is trivial. Its three crossings have local equation w^2=uv, hence are A1 singularities. Their resolutions are crepant. The cover is connected because its branch is reduced and nonempty; an odd valuation of the branch equation also gives nonsquareness. The finite double-cover decomposition O_R plus O_R(K_R), together with rationality of R and Serre duality, gives H^1=0; rational double points do not change H^1 upon resolution. Thus the smooth geometric resolution is indeed K3.

This conclusion is relative to L. A K3 surface in characteristic zero cannot be unirational, because a dominant rational map from a rational surface would inject its nonzero regular two-form after resolving the map. This obstructs a rational-surface parametrization over L and says nothing by itself about rationality over C. The packet supplies a valid counterexample to that erroneous leap: C(a,b,c) over C(a^4+b^4+c^4) has smooth quartic K3 generic fiber while its total field is rational.

The supporting genus-one reconstruction has correct inverse formulas and nonzero twist. It is not counted as a sixth route. An elliptic section similarly does not turn the fiber into P^1.

## 6. Minimum lattice width and field degree of torus projections

The twelve support monomials are correct and distinct. The independent certificate uses support differences 2e_s, 2e_t, 3e_x, 3e_y, 3e_z. If an integral covector has width at most one, each of these differences has pairing of absolute value at most one, so all five coordinates of the covector vanish. Thus every nonzero primitive direction has width at least two. The s and t directions each attain width two.

A GL5(Z) monomial coordinate change is an automorphism of the Laurent polynomial ring, so it preserves irreducibility. Distinct support monomials cannot collide under this change. Once the minimum chosen-variable exponent is shifted to zero, the resulting polynomial has nonzero constant coefficient and degree equal to the width. Its coefficients are primitive over the remaining Laurent ring: a nonunit content would give a Laurent factorization, contradicting irreducibility. Gauss's lemma gives irreducibility over the fraction field of those four coordinates. The latter coordinates are algebraically independent on the hypersurface, since an irreducible positive-degree relation in the fifth variable cannot divide a nonzero polynomial in the other four alone. Therefore the generic projection degree really equals the width.

This argument rules out every specified unimodular-monomial projection of degree one, not only the sampled coordinate directions and not only a bounded set of integer matrices. It does not rule out general rational substitutions, nonmonomial maps, contractions, or rational transcendence bases. Replacing x^3-1 by x-1 provides a checked width-one and rationally solvable negative control.

## 7. Reproducibility, controls, and limitations

The author checker replays unchanged with 73 checks, of which 11 are designated negative controls. The independent verifier has 120 checks, including 10 negative controls. Counts describe executable checks, not 120 formalized geometric theorems. In particular, the COV criterion, regularity implications, Artin fixed-field theorem, Brauer-Severi splitting, double-cover canonical formula, rational-double-point cohomology, and regular-form obstruction remain explicit mathematical dependencies.

The independent code never imports or executes author code to establish its own formulas. Its use of SymPy factorization over Q is explicitly auxiliary; geometric integrality over C is established by the smooth projective diagonal-cubic argument, not inferred from rational irreducibility.

Optimized and normal Python results are required to agree exactly. Both verifiers use explicit exceptions rather than Python assert statements. The retained control runner deliberately corrupts five independent formulas/certificates and four formulas/certificates in temporary copies of the author verifier. Each must fail at its intended check under Python -O. Five further tests cover changed bytes, unlisted entries, missing files, symlinks, and a locally rehashed but externally unbound author manifest. Formula controls bypass ordinary hash gating only within temporary files, so the mathematical checks themselves must detect the corruption.

The replay program checks the exact tree, external frozen author-manifest binding, optional pinned ZIP, and equality with the recorded symbolic outputs. An archive checksum alone does not substitute for comparing its complete member set and member bytes. The audit manifest enumerates safe outputs only. Results and the final operational receipt distinguish actual verification from the mathematical proof review.

## Disposition

The five routes are distinct mechanisms at the scope claimed. They reuse a shared field model openly. The elliptic reconstruction remains supporting material rather than an inflated approach count. The local mathematical disposition is five retained partial routes with the rationality goal unresolved. Any queue outcome is a separate authorized editorial action; this audit made no queue, repository, branch, PR, or remote changes.

No mandatory correction is required. The existing qualifications concerning dense opens, dominant components, exact covering degrees, relative bases, theorem dependencies, uninspected imported records, and absent novelty/global-status certification must remain attached to the results. A scoped audit pass must never be relabeled as a solution, a counterexample to rationality, or a complete classification of possible birational modifications.
