# Independent review: KP 3.61 mutation-rank partial

## Verdict

**PASS_SCOPED_TOPOLOGY_AND_SOURCE_HOLD.** No mandatory mathematical correction is required. The original balanced-sutured Floer-dimension question remains **unsolved, 2/5**. The accepted deductions are a data-preserving extension criterion and separating integral-homology invariance, with a correct nonseparating caution. Neither is a general Floer-rank theorem.

The frozen `PARTIAL_RESULT.md` has SHA-256

`c064e0d83d682f206098835741553c946bd9f62efaddc4c6ebe5aee42a186522`.

This is an independent adversarial AI review, not human peer review or a novelty assessment.

## 1. Exact original scope and prior announcements

I read the complete [K3 Problem 3.61](https://aimath.org/pastworkshops/kirbylistrep.pdf), printed pp.174–175, and visually inspected p.174. The operation is cutting along an embedded **closed genus-two surface** and regluing by its hyperelliptic involution. The broad question is total balanced-sutured Floer dimension over F2, with closed hat-HF and knot hat-HFK as special cases. Its wording does not require the mutation surface to separate. The source itself distinguishes failures of finer gradings from the total-dimension question. All these qualifications are retained.

Both institutional seminar sources were independently retrieved. The [2022 Nantes–Orsay abstract](https://www.imo.universite-paris-saclay.fr/~frederic.bourgeois/seminar/NO12-22.html) announces a rank-invariance application of a compact-Fukaya/bordered-Floer construction. The [2023 Uppsala abstract](https://www.uu.se/en/department/mathematics/research/geometry-and-physics/seminar-series-in-geometry-and-topology-/archive/2023-02-16-gt-seminar-with-paolo-ghiggini-institut-fourier-grenoble) identifies the joint project with Ina Petkova as work in progress and discusses hat Heegaard Floer homology. Neither page supplies a complete proof or a precise statement of the whole balanced-sutured/nonseparating scope. A targeted current search also located a Durham conference abstract repeating the work-in-progress qualification, but no complete manuscript was located. This is a retrieval limitation, not evidence of withdrawal or a false announcement.

The accessible full [Moore–Starkston paper](https://arxiv.org/abs/1204.2524), including Theorem 1, Section 2 and its conclusions, was checked. Its examples have equal total knot-Floer dimension while finer graded groups differ. Its handlebody mutations contain the distinguished knot inside the handlebody. The author's use of these examples and the distinction from data-free handlebody mutations are accurate. This audit does not reconstruct their Floer computations.

The primary PDF hashes agree with the submitted manifest: K3 `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`; Moore–Starkston `ed2ac65a70f4b686239530b4e7f1382b09038e3ffb8b74f69eff80b2b1b55b7c`.

## 2. Extension criterion

The quotient-map verification is correct. In the mutant, the boundary point y is identified with `f(h(y))` on X. Under the piecewise map `(id_X,H)`, its Y-image is `H(y)=h(y)`, which is identified with that same point in the original gluing. The inverse is induced by `(id_X,H^{-1})`. Collar straightening makes the maps product-like at the seam, so the resulting oriented map is a diffeomorphism in the stated smooth category.

Every item of distinguished data must be preserved by this map. For sutured manifolds, the stipulated fixed remaining boundary and sutures provide that condition. For a marked-knot formulation, one must either require the extension to preserve the knot or work in its sutured exterior and preserve the corresponding boundary data. The artifact explicitly excludes the incorrect inference when a knot inside the handlebody is moved by the extension.

The genus-two handlebody example is sound. The double branched cover of a ball over three disjoint boundary-parallel arcs is a genus-two handlebody; the boundary cover of a sphere over six points is its genus-two boundary. The deck transformation is orientation-preserving and restricts to the hyperelliptic mapping class. The unique hyperelliptic mapping class in genus two and a boundary-collar isotopy allow any isotopic boundary representative. This gives an extension when the handlebody contains no distinguished knot or other data requiring preservation. Ordinary Floer invariance under the resulting data-preserving diffeomorphism then applies. No general mutation theorem is hidden in this argument.

## 3. Separating integral homology, including torsion

The hyperelliptic action on `H1(Sigma_2;Z)` is `-I`. Besides the standard symplectic-basis description, the six fixed points provide a check: each has Lefschetz index +1, so the trace on the four-dimensional first homology is `2-6=-4`. An involution over characteristic zero is diagonalizable with eigenvalues ±1, forcing all four eigenvalues to be -1. The integral endomorphism is therefore exactly `-I`.

For connected separating sides, the Mayer–Vietoris H0 map takes the generator to `(1,-1)` and is injective. Hence H1 is exactly the cokernel of the stated inclusion map. Composing one inclusion with `-I` is intertwined by multiplication by -1 on the corresponding target homology summand. This is an automorphism of an arbitrary abelian group, including its torsion subgroup. Thus the integral cokernels are isomorphic without a freeness assumption.

In presentation form, internal relations can be retained as separate columns. Negating the relevant target rows and the corresponding internal-relation columns gives unimodular equivalence of the two presentations. The independent checker includes both free and torsion summands to verify this point. The proof concerns ordinary H1 and says nothing about a Floer differential.

## 4. Nonseparating example

Cutting `Sigma_2 x S1` along a fiber and regluing by h really does produce the mapping torus of h. The Wang sequence gives a short exact sequence from `coker(f_*-I)` to H1 of the mapping torus and then to the invariant H0 group Z. It splits as a sequence of abelian groups because the quotient is free, without requiring a canonical splitting.

For f=id the cokernel is Z4. For f=h it is the cokernel of `-2I_4`, namely `(Z/2)^4`. After the Z summand is added, the claimed groups `Z5` and `Z + (Z/2)^4` follow. Over F2 the two fiber actions coincide, and the first-homology dimensions are both 5. The example therefore correctly disproves an unrestricted integral-H1 preservation claim, while not providing a Floer-rank counterexample. If desired it also fits the sutured setting after removing a ball disjoint from the mutation surface; that observation is not needed for the submitted claim.

## 5. Independent checks

All **13,125** submitted presentation controls reproduce with a byte-identical receipt in an isolated copy. The verifier hash is `d56b119c6dc61b7d2a21a5cdfd2b8022b7c4eeeea3577cfa5eec755682705e9c`.

The separate checker passes **3,185** exact assertions. It includes 72 independent integer presentations with internal torsion and free summands, their explicit unimodular intertwiners and Smith factors, 12 finite-group quotient examples on a 120-element target, and the mapping-torus and H0 action matrices. No submitted code is imported. The finite presentations are algebraic controls; they are not asserted to be a census of realized three-manifolds.

Run from the review directory:

```sh
python independent_checks.py
(cd author_replay && python verify.py)
```

The independent script requires SymPy. The author's script uses the standard library. Neither computes Floer homology or supplies executable geometry. The extension and homological arguments have been reviewed separately in prose.

## 6. Disposition

Preserve the original unresolved status, the full F2 balanced-sutured scope, and the Ghiggini–Petkova announcement credit and access limitation. The remaining problem requires a genuine Floer comparison for nontrivial mutations, or an actual geometric mutant pair with unequal total Floer dimension. The submitted work does not claim either, and no correction is required.
