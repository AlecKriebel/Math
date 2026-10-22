# A concrete higher-rank local-system family crosses the Alexander-one barrier

PASS2, 14 October 2026. This construction is classical twisted Alexander theory. Its explicit Kinoshita–Terasaka calculation is replayed from Wada's primary 1994 example; no novelty or Jones reconstruction is claimed.

## Result

A canonical finite family of genuine rank-two local systems distinguishes the Kinoshita–Terasaka knot from the unknot even though their ordinary Alexander modules and Blanchfield forms vanish. This is an explicit way past the limitation established in the companion pairing report.

The family uses all parabolic `SL₂(F₇)` representations of the knot group, rather than choosing one arbitrarily. We verify one nonabelian member and its local-system homology-order ratio exactly. Its result is a degree-six polynomial, while every member of the corresponding unknot family has a pole of order two at `u=1`. No full-knot-data theorem or extraction of Jones from this family is provided.

## 1. Intrinsic family

Let `E` be the oriented compact exterior, `G=π₁(E)`, and `ℓ:G→Z` its positive meridional character. Put

`Λ₇=F₇[u,u⁻¹]`, `Q₇=F₇(u)`.

Let `P₇(K)` be the finite groupoid of representations

`ρ:G→SL₂(F₇)` with `tr ρ(m)=2`,

where `m` is any positive meridian, and arrows are simultaneous conjugations. The condition is independent of which meridian is chosen, since positive meridians are conjugate. This includes the trivial and unipotent abelian representations. There are finitely many homomorphisms because `G` is finitely generated and the target group is finite.

Each representation defines a rank-two local system over Λ₇ with monodromy

`g ↦ u^{ℓ(g)}ρ(g)`.

Its chain complex and homology are intrinsic to `(E,ℓ,ρ)`. An orientation-preserving diffeomorphism of oriented knot pairs induces an equivalence of representation groupoids by pullback and compatible homology isomorphisms. Conjugate representations give isomorphic coefficient systems. Thus retaining the entire indexed family removes the need to select a distinguished representation.

For each representation whose Q₇-coefficient homology is zero, define

`τ_ρ(K)=ord_Λ₇ H₁(E;Λ₇²_ρ) / ord_Λ₇ H₀(E;Λ₇²_ρ)`

as a class in `Q₇× / {c u^j : c∈F₇×, j∈Z}`. Here the order of a torsion module over the PID Λ₇ is the product of its nonzero Smith factors. For a finite two-dimensional exterior model, Q₇-acyclicity makes `H₂` vanish over Λ₇ as well: it is a torsion submodule of a free module, hence zero. Consequently the displayed ratio agrees with the usual twisted torsion convention. For nonacyclic representations, retain their homology and a nonacyclic flag instead of pretending the same ratio is defined.

One may take the set or multiset of these classes together with the nonacyclic records. The argument below works for either choice. This is an actual homology extraction, not a scalar assigned from Jones.

## 2. One verified nonabelian member

Use Wada's four-generator presentation for the Kinoshita–Terasaka complement. The source states that it is strongly Tietze equivalent to the displayed Wirtinger presentation; it is not an arbitrary deficiency-one presentation whose relation complex is being silently identified with the exterior. All generators represent positive meridians. The source-derived presentation and four representation matrices are an external replay fixture, not redistributed in this authored packet. It is identified by SHA-256

`d441e8606b116f7994fd9b5e6f166ff656fe9c2bfe2b0d56c7ae2c40148acd24`.

The fixture records equation (6.1) and the first parabolic representation on printed pages 254–255. The public checker accepts its JSON path through `--input`; this input is required for a full numerical replay. The proof and source reference specify the object without claiming that the publication packet bundles all source material.

Every determinant is one and every trace is two. Exact multiplication verifies all three relations in the external input. The commutator of the first two matrices is `[[1,1],[1,2]]`, so the image is nonabelian.

Given the external source fixture, the accompanying `check_higher_rank_kt.py` independently performs these multiplications, constructs the twisted Fox matrix from the signed relator words, and checks the Fox identity before taking a determinant. It does not assume the source polynomial in that construction.

## 3. Exact homology-order calculation

Apply `Φ(g)=u^{ℓ(g)}ρ(g)` to the Fox derivatives. The relation-by-generator matrix has three rows of four `2×2` blocks. Delete the block column for `x₄`, obtaining a `6×6` matrix `N` over Λ₇. The checker obtains

`det N = 6u¹⁰+5u⁹+4u⁸+u⁷+3u⁶+u⁵+4u⁴+5u³+6u²`,

and

`det(uρ(x₄)−I)=u²+5u+1=(u−1)²` in F₇[u].

The denominator is nonzero and the deleted minor is nonzero, establishing Q₇-acyclicity. The standard deficiency-one torsion calculation gives

`τ_ρ(K)=det N / det(uρ(x₄)−I)`

`=u²·(6+3u+4u²+6u³+4u⁴+3u⁵+6u⁶)`.

The factor `u²` is a permitted Laurent unit. After removing it, this exactly matches Wada's recorded polynomial. All arithmetic in the checker is over the rational-function field F₇(u), not floating point or characteristic-zero substitution.

The unbundled knot presentation and representation are verified primary inputs from Wada, *Twisted Alexander polynomial for finitely presentable groups*, Topology 33 (1994), 241–256, §6, printed pp.254–255. [Primary paper](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/wada.pdf), [DOI](https://doi.org/10.1016/0040-9383(94)90013-2). The scanned pages were inspected directly. The source text and scans are retained privately and are not included in the authored publication packet.

## 4. Exact comparison with the unknot

The unknot exterior is homotopy equivalent to a circle. Any `ρ:Z→SL₂(F₇)` in the meridian-trace-two family is determined by a matrix `R` satisfying

`det R=1`, `tr R=2`.

The entire twisted complex is

`0 → Λ₇² --(uR−I)→ Λ₇² → 0`.

Its determinant is always `(u−1)²`, so it is Q₇-acyclic, `H₁=0`, and

`τ_ρ(U)=1/(u−1)²`

for every such representation. This has a double pole at `u=1`.

By contrast the verified knot torsion is a polynomial; its normalized value at `u=1` is

`6+3+4+6+4+3+6=32=4 mod 7`,

so it is nonzero and regular there. Multiplying by any allowed Laurent unit `c u^j` cannot change this distinction at `u=1`. Therefore the canonical finite family for the Kinoshita–Terasaka knot differs from the unknot family. An exhaustive enumeration of the knot's representations is unnecessary for this conclusion: every unknot value is fixed, and one verified knot value lies outside that set.

The source's chirality convention is immaterial to this distinction. Mirroring changes the associated Laurent-variable convention, but does not turn regularity at `u=1` into the unknot's double pole.

## 5. Relevance and remaining Jones obligation

This is a concrete, naturally indexed higher-rank local-system construction with an exact knot-sensitive homological extraction. It is not constrained by the rank-one acyclicity theorem from PASS1, and it retains information lost by the ordinary Blanchfield datum. The calculation is not merely another acyclic family: although localization is acyclic, its Laurent homology-order ratio distinguishes the explicit knot from the unknot.

This finite family is not proved to determine full knot data or Jones. Wada also distinguishes the Kinoshita–Terasaka and Conway knots by related twisted data, although their Jones polynomials agree; that fact does not rule out an extraction from richer data, but it prevents identifying these torsion collections with Jones itself.

To advance to Roberts's target, one still needs a canonically specified operation on an appropriate family of these local-system objects, and a proof that the operation produces the entire source-normalized Jones polynomial for every knot. Neither a quantum trace nor weights for summing representations are supplied by the groupoid definition. Expanding to all finite fields or ranks would give more coefficient data, but does not by itself furnish the missing operation or establish completeness. No claim is made that one fixed finite family suffices.

**Disposition: explicit higher-rank escape with verified homology extraction; full Jones bridge absent.**
