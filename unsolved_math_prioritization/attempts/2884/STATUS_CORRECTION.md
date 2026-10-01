# 2884 / KP-4.8: credited correction for the literal arbitrary-ambient question

**Disposition proposed for independent review:** `already_solved`, 0/5 fresh proof turns. The literal universally quantified implication is false by a known stabilization observation. This is a source validation and reconstruction of an already public consequence, not a new discovery. The separate unstabilized K3 question in Remark (2) is not settled here.

## 1. Exact target and source scope

The full primary source is Baykur–Kirby–Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, Problem 4.8, printed/PDF p.197, in the permissioned author preliminary PDF linked in SOURCES.md. Its ambient is an arbitrary closed simply connected smooth four-manifold X containing a square-zero smooth torus T with simply connected complement. It asks whether diffeomorphic knot surgeries for two prime knots force equality up to mirror. No irreducibility, minimality, nonzero Seiberg–Witten invariant, or restriction to the K3 surface appears in this question. Remark (2) separately specializes to K3. The imported statement matches these quantifiers; its cited four-page AIM workshop report is not the full problem-list source.

The distinction matters: the stabilization is made part of the **one fixed ambient manifold before either surgery**, rather than added afterward to a proposed counterexample with ambient K3.

## 2. Established input, with gluing convention

Write H=S²×S². Baykur, *Dissolving knot surgered 4-manifolds by classical cobordism arguments*, Theorem 1, asserts

    Y_K # H ≅ Y # H

for compact simply connected smooth Y and a square-zero torus with simply connected complement. The full three-page arXiv v3 proof, including Remark 2, was inspected. This published theorem is the substantial four-dimensional input. Earlier cusp/nucleus versions are credited there to Akbulut and Auckly. We do not supply a new proof of the stabilization theorem.

Use ordinary Fintushel–Stern knot surgery. On the incoming boundary S¹×∂E(K), let s be the S¹ factor, μ_K the meridian and λ_K the zero longitude. Fix a framing (a,b,μ_T) of ∂νT once. Choose the standard orientation-compatible gluing sending s and μ_K to a and b, and λ_K to μ_T, up to the single sign required for boundary orientation. Use that same framed pattern for every knot. This is the zero-surgery model in Baykur Remark 2 and in Fintushel–Stern's original construction. The earlier S¹×S³ fiber-sum paragraph in Baykur uses different named peripheral circles; it is not a license to silently interchange the knot meridian and longitude in the standard surgery.

As a primary cross-check, Choi–Park–Yun's published paper specifies the zero-longitude condition on p.738 and proves a CP²-stabilization theorem in Theorem 1.1 for a double-node torus with meridian matched to the vanishing cycle. Its proof of Corollary 1.3 applies this to the ordinary regular fiber of E(n). This is corroboration for the standard knot-surgery convention, not an assumption that every torus has a double-node neighborhood.

## 3. One admissible fixed ambient

Let Y=E(2), and choose a regular fiber F in its standard elliptic Lefschetz fibration. This is a closed smooth K3 surface. A regular-fiber neighborhood is F×D², so F has square zero.

For completeness, the complement fundamental group can be read directly from the fibration. Remove a small disk around a regular value of the base sphere. The remaining fibration over a disk is built from F×D² by attaching Lefschetz two-handles along its vanishing cycles. Its fundamental group is therefore π₁(F) modulo their normal closure. The standard factorization is (αβ)^12; α and β are the two generating primitive curves of the torus, intersecting once. Both are killed, so π₁(Y\int νF)=1. The factorization and its use for regular elliptic fibers are recalled in Choi–Park–Yun's proof of Corollary 1.3, pp.741–742. The handle description is also the elementary van Kampen proof of the asserted complement statement; simple connectivity of Y alone would not suffice.

Choose a smooth four-ball B in Y\νF and form the oriented connected sum

    X = Y # H

at B, keeping F and its chosen framing untouched. Both summands are closed, smooth and simply connected. Removing a ball from a connected four-manifold leaves π₁ unchanged, and the connected-sum interface is S³. Van Kampen thus gives

    π₁(X\int νF)=π₁(Y\int νF)*π₁(H\int B⁴)=1.

The complements of F and of an open tubular neighborhood have the same homotopy type for this purpose. Hence every ambient and torus hypothesis of the literal source question is satisfied.

## 4. Surgery commutes with the disjoint connected sum

The excision and gluing for knot surgery take place inside νF, disjoint from B. The defining pieces and boundary identifications give an orientation-preserving diffeomorphism

    X_K = (Y#H)_K ≅ Y_K#H.

This does not require extending any diffeomorphism over the torus, or preserving the chosen ball under Baykur's resulting diffeomorphism: it is first an equality of the local cut-and-paste constructions, followed by an unrestricted diffeomorphism of the resulting closed manifolds. Applying the established stabilization theorem to (Y,F) gives

    X_K ≅ Y_K#H ≅ Y#H = X

for every knot K with the fixed standard gluing. In particular any two admissible prime knots give diffeomorphic surgeries on the same fixed (X,F). Existence of these permitted surgeries already disproves the unrestricted recognition implication; no assertion about every possible alternative boundary gluing is needed.

## 5. Explicit prime knots that are not mirrors

Take K₁=T(2,3) and K₂=T(2,5), the closures of the positive two-braids σ₁³ and σ₁⁵. Each is a knot because the braid permutation is the transposition. Their canonical two-disk, respectively three- or five-band Seifert surfaces have genus 1 and 2. The standard chain Seifert matrix has diagonal entries 1 and superdiagonal entries −1, of size 2 and 4 respectively. Its determinant det(tV−Vᵀ) gives

    Δ₁(t)=t²−t+1,       Δ₂(t)=t⁴−t³+t²−t+1.

Both have degree equal to twice the exhibited genus; the Alexander genus bound makes these genera minimal. The first polynomial is irreducible over Q by its negative discriminant. The second is Φ₅(−t), irreducible because Φ₅(x+1)=x⁴+5x³+10x²+10x+5 is Eisenstein at 5.

Here is a classical primeness check without assuming that irreducible Alexander polynomial alone implies primeness. Under a connected sum, Alexander polynomials multiply and the ordinary knot genus adds (Schubert). If either of these full-degree knots were a sum of two nontrivial knots, irreducibility would force one summand's Alexander polynomial to be a unit. The other summand would already have genus at least the full genus of the original knot, by the degree bound, while the unit-polynomial nontrivial summand has genus at least one. This contradicts genus additivity. Thus both knots are prime. Ozawa's introduction explicitly recalls Schubert's ordinary-genus theorem; we are not confusing it with Ozawa's separate free-genus theorem.

The degrees differ; equivalently |Δ₁(−1)|=3 and |Δ₂(−1)|=5. These quantities are unchanged under mirroring, so K₁ is neither K₂ nor its mirror. Combining this with Section 4 gives the required negative answer to the literal arbitrary-X formulation.

## 6. Credit and limits

The same specific stabilized-ambient observation and knot pair were already publicly recorded in the external Argus-AiTeam result 2884 linked in SOURCES.md. We inspected its public summary only; no external code, formalization, proof PDF, or executable was reused. Our validation rests on the primary stabilization literature and the stated source quantifiers. The external observation is credited, and no historical or mathematical novelty is claimed.

Nothing here cancels the H summand. Nothing here resolves the separate recognition question with the ambient fixed to the unstabilized K3 surface. An intended question with an additional irreducibility or nonvanishing-invariant hypothesis would be a different target requiring separate review. This correction does not silently add such an assumption or speculate about the problem editors' intentions.

The accompanying exact checker verifies finite polynomial, matrix, and genus bookkeeping only. It is not a formal proof of four-dimensional topology. Independent review must inspect all topological hypotheses, source conventions, and the logical scope above before queue promotion.
