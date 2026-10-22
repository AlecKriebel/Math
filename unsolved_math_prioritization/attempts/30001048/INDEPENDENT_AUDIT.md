# Independent audit: one-handle compression-body core geodesics

Problem 30001048 / OWR-2089-004. Audit date: 2026-10-10 UTC.

## 1. Verdict and exact candidate

**ACCEPTED AS A CORRECT PARTIAL REDUCTION. THE CONJECTURE REMAINS UNRESOLVED.**

The normalized collision criterion, the one-handle-letter exclusions, and the cyclic-power exclusion are correct under the stated discrete faithful compression-body hypotheses. No false proposition was found in the accepted candidate. This audit supplies explicit background and precision arguments for cusp rank, cusp maximality, properness, orientation, and accidentally parabolic generators. None of these supplies the missing arbitrary-word or isotopy argument.

This AI-assisted, unrefereed audit accepts only the mathematical partial reduction in [PROOF_ATTEMPT.md](PROOF_ATTEMPT.md), read with the precisions below and in [CORRECTION_PRECISION_LEDGER.md](CORRECTION_PRECISION_LEDGER.md). No claim of novelty is certified. The public edition identities are recorded in [MANIFEST.json](MANIFEST.json).

## 2. Scope and hypotheses

Let C be the compression body obtained by adding one 1-handle to T² × [0,1]. Its specified core tunnel τ is the handle core continued to the negative boundary by the two product arcs. Work with its marked group

G = P * ⟨γ⟩,  P ≅ Z²,

and a discrete faithful representation ρ giving the complete hyperbolic structure in question. Write Γ = ρ(G) and N = H³/Γ. The group is torsion-free because G is torsion-free and ρ is faithful. Consequently its action on H³ is free. Discreteness excludes infinite-order elliptic elements; torsion-freeness excludes nonidentity finite-order elliptic elements.

The original question concerns isotopy of this specific proper core arc, with endpoints allowed to move on the torus when the cusp is truncated. It is not the assertion that every representative of the same element or double coset is a core tunnel, nor is it a problem about arbitrary pointwise-fixed finite endpoints.

The geometric finiteness assumption is part of the target conjecture. The accepted algebraic and cusp arguments below actually require only the relevant discrete faithful representation and rank-two peripheral cusp. They do not assume that γ is loxodromic and do not assume minimal parabolicity.

### 2.1 Why the peripheral image is a rank-two parabolic lattice

A discrete torsion-free abelian subgroup of PSL(2,C) containing a loxodromic element is cyclic: all its elements preserve the loxodromic axis, their axial displacements form a discrete subgroup of R, and the rotational kernel is a discrete subgroup of the compact circle group, hence finite and therefore trivial. Discreteness of the axial displacement image follows by compactness of the rotational factor: infinitely many elements with bounded displacements would accumulate after taking a subsequence and differences.

Since ρ(P) is isomorphic to Z², this loxodromic case is impossible. Nonidentity elliptics are also impossible. Thus its nonidentity elements are parabolic and have a common fixed point. After sending that point to ∞, they are translations T_λ(z)=z+λ. Their parameters form a discrete rank-two additive subgroup Λ of C, hence a real two-dimensional lattice. In particular every nonzero lattice element has nonzero Euclidean length and the shortest such length is positive.

### 2.2 Why the full stabilizer is exactly the marked P

The final candidate now proves this rather than assuming it. Here are all of the dependencies.

An element of Γ fixing ∞ acts as z ↦ Az+B. If |A|≠1, conjugating any fixed nonidentity T_λ by suitable powers of that element produces nonidentity translations with parameters converging to zero, contradicting discreteness. If |A|=1 but A≠1, the affine map has a finite fixed point and is a nonidentity elliptic, which is impossible. Therefore A=1 and the element is a translation. It commutes with ρ(P).

The free-product normal-form theorem implies C_G(P)=P. More specifically, a nontrivial element of a free factor cannot be conjugated back into that factor by an element outside the factor; equivalently P is malnormal in P * ⟨γ⟩. Faithfulness transfers the centralizer conclusion to Γ. Thus Γ_∞=ρ(P), including the possibility one might otherwise worry about of a larger translation superlattice.

This also proves c_γ≠0. A marked handle generator cannot fix ∞ because it does not belong to P. The group is non-elementary: it has the rank-two parabolic fixed point and γ moves that point. No elementary exception was silently included.

## 3. Normalization, marking, and geodesic ends

Start with a determinant-one matrix A=[[a,b],[c,d]] representing ρ(γ), where c≠0. Direct conjugation gives

T_(d/c) A T_(-d/c) = [[a+d, −1/c],[c,0]].

Conjugation by the complex dilation z ↦ cz then gives

g = [[s,−1],[1,0]],  s=a+d.

The dilation is an orientation-preserving hyperbolic isometry, including when c is non-real. Its determinant-one matrix representative may use either square root of c; the induced conjugation is unambiguous. The lattice is rescaled by the same nonzero complex factor. No assumption about a unit cusp translation has been introduced.

All matrix lifts may be changed by sign: bc and ad are unchanged. Thus the forbidden-interval test is well-defined on PSL(2,C) once the geometric normalization is fixed.

Let L be the geodesic {(0,t):t>0}. It has endpoints g⁻¹∞=0 and ∞. The customary geodesic representative of the oriented double coset PγP instead has endpoints ∞ and g∞. Applying g to L gives that same endpoint pair with an appropriate orientation. The two lines have the same projected image. Reversing the orientation of an unoriented core arc is harmless; no γ versus γ⁻¹ error affects the argument.

The double-coset interpretation also works if γ is accidentally parabolic. The necessary condition is g∞≠∞, already proved from the full stabilizer. The endpoints remain distinct. Any two points at infinity determine a unique H³ geodesic, and changing γ by left or right peripheral factors changes that line only by a peripheral deck translation. Lifting a core arc, extending its two ends into the corresponding horoballs, and straightening it gives this representative. Uniqueness concerns the proper homotopy class with cusp endpoints, not the unknown isotopy class.

Lackenby–Purcell's Lemma 4.8 is phrased using a loxodromic generator. The accidentally parabolic extension just described is an elementary endpoint argument supplied here; it should not be represented as an extra conclusion of the cited lemma without this explanation.

### 3.1 Setwise stabilizer

If an element preserves L and fixes its two endpoints individually, it fixes ∞ and therefore belongs to P; a translation fixing 0 is the identity. If it swaps the endpoints, a matrix representative has a=d=0 and bc=−1, so its square is −I. It would be a nonidentity order-two element of PSL(2,C). This is excluded by torsion-freeness. Thus Stab_Γ(L) is trivial.

### 3.2 Properness, not just local injectivity

Choose a sufficiently small embedded rank-two cusp neighborhood, lifting to a horoball B_∞={t>H} for some H>0. Such an embedded horoball exists for a rank-two cusp of a discrete torsion-free Kleinian group. Increase H to exceed 1 if convenient.

For the normalized g, the upper-half-space action on L is exactly

g(0,t) = (s,1/t).

Hence q(0,t), where q:H³→N is the quotient map, goes to unbounded depth in the cusp when t→∞. Since q(g(0,t))=q(0,t), it also goes to unbounded cusp depth when t→0. In logarithmic parameter r=log t, both ends escape every compact subset of N. The middle parameter interval is compact. Thus q|_L is proper.

This fills in the useful precision behind the candidate's short properness sentence. Merely remaining inside some cusp neighborhood would not, on its own, prove properness; the depth tends to infinity here.

## 4. Exact collision criterion

The proposition is valid for every h≠1 in Γ. It must not be read as a statement for arbitrary PSL(2,C) matrices without the trivial-stabilizer hypothesis, because a diagonal matrix could preserve L.

Write h=[[a,b],[c,d]] with ad−bc=1.

### 4.1 Zero entries and ideal endpoint coincidences

All exceptional configurations are accounted for:

- If b=0 or c=0, then bc=0. The lines share 0 or ∞, respectively, unless both endpoints coincide.
- If a=0 or d=0, then ad=0 forces bc=−1. Again a pair of ideal endpoints shares a point, unless both coincide.
- If the unordered endpoint pairs coincide, h preserves L. This was excluded for h≠1.

Distinct hyperbolic geodesics sharing an endpoint at infinity have no common interior point. Therefore none of these zero-entry cases is an interior collision. The interval endpoints 0 and −1 must indeed be excluded.

### 4.2 Nonzero entries

If all four entries are nonzero, hL has distinct finite nonzero endpoints u=a/c and v=b/d. Its semicircle lies in the vertical plane over the Euclidean line through u and v. The vertical geodesic L meets it if and only if 0 lies strictly between u and v on that line. This is equivalent to u/v being negative real.

Now

u/v = ad/(bc) = 1 + 1/(bc).

For a nonzero complex number x, 1+1/x is negative real exactly when x is real and −1<x<0: taking imaginary parts first forces x to be real, and the real inequality then gives the specified interval. Thus L meets hL precisely when bc∈(−1,0). In that case the crossing height is √(|u||v|)>0.

### 4.3 Passing to the quotient

A double point of q|_L yields x=hy for distinct x,y∈L and h≠1, hence L∩hL≠∅. Conversely an intersection gives x=hy with x,y∈L. The two points are distinct because a nonidentity element of the torsion-free discrete group cannot fix a point of H³. The line's trivial setwise stabilizer also excludes a multiple-cover/coincident-line exception.

The quotient map is a local isometry, so q|_L is an immersion. Properness was proved above. A proper injective immersion is an embedding. Consequently the exact accepted equivalence is

q(L) is a properly embedded geodesic ⇔ every h∈Γ has b_h c_h∉(−1,0).

The identity has bc=0 and does not affect the right-hand condition. All quantifiers and degenerate cases are consistent.

## 5. One-handle-letter exclusions

Burton–Purcell Lemma 4.3 supplies the needed Shimizu–Leutbecher consequence. In the normalized rank-two cusp, for T_λ∈Γ, λ≠0, and k∈Γ with c_k≠0,

|λ c_k| ≥ 1.

Indeed its radius bound is 1/|c_k|≤T, where T is the shortest nonzero peripheral translation length, and T≤|λ|. No unit translation is assumed, and the estimate is a necessary condition for discreteness, not a sufficient one. Its cited hypotheses are met.

For h=T_λ g T_μ, direct multiplication gives

h = [[s+λ, μ(s+λ)−1],[1,μ]],  bc=μ(s+λ)−1.

A collision would require μ(s+λ)∈(0,1); in particular μ≠0. Put k=T_λ g. The lower-left entry of k² is s+λ. This cannot vanish: k has lower-left entry 1 and trace s+λ, so trace zero would give k²=−I by Cayley–Hamilton, producing nontrivial order two. Applying the inequality to T_μ and k² contradicts |μ(s+λ)|<1.

For h=T_λ g⁻¹ T_μ,

h = [[−λ,1+λs−λμ],[−1,s−μ]],  bc=λ(μ−s)−1.

A collision requires λ(μ−s)∈(0,1), hence λ≠0. Put k=g⁻¹T_μ. Its square has lower-left entry μ−s, nonzero by the same order-two argument. The inequality for T_λ and k² again contradicts the required strict upper bound.

If λ or μ is zero in a way that prevents the relevant application, the collision condition itself has already excluded it. Peripheral elements have bc=0. Thus there is no missed division-by-zero or purely peripheral case.

## 6. Chebyshev lemma and powers

For P₀(x)=1, P₁(x)=x, and P_(m+1)(x)=xP_m(x)−P_(m−1)(x), the degree of P_m is m. The trigonometric identity

P_m(2 cos θ)=sin((m+1)θ)/sin θ

follows from the same recurrence and its two initial values.

For j=0,…,m, choose θ_j=(j+1/2)π/(m+1) and x_j=2 cos θ_j. These m+1 real points are distinct and lie in (−2,2), and P_m(x_j) has sign (−1)^j and magnitude at least 1. For any fixed real r∈(−1,1), subtracting r preserves each sign. There is a root of P_m−r in each of the m disjoint consecutive intervals. Since the polynomial has degree m, those are all its complex roots. This proves Lemma 3 for every m≥1, not just numerically tested degrees.

For k=T_λg=[[t,−1],[1,0]], t=s+λ, Cayley–Hamilton gives the power recurrence and therefore

(kⁿ)_12 = −P_(n−1)(t),  (kⁿ)_21 = P_(n−1)(t),  n≥1.

The product is −P_(n−1)(t)². For n=1 it equals −1. For n≥2, a product in (−1,0) implies P_(n−1)(t) is a nonzero real number of absolute value less than 1: a complex square can be positive real only if its square root is real. Lemma 3 then forces t∈(−2,2). A determinant-one matrix with that real trace is a nonidentity elliptic, impossible in Γ.

For negative n, inversion negates both off-diagonal entries and leaves their product unchanged. The result follows for all n≠0.

The accidental-parabolic trace values t=±2 are included without difficulty: P_(n−1)(2)=n and P_(n−1)(−2)=(−1)^(n−1)n, so the products are −n². This explicitly confirms that the proof does not silently omit parabolic shifted generators. Trace zero, finite-order elliptics, infinite-order elliptics, and the identity have all been treated consistently.

## 7. What the exclusions do not prove

The proved classes do not exhaust Γ=P*⟨γ⟩. Reduced words with multiple handle syllables and independent intervening peripheral elements remain. Matrix multiplication introduces cross terms; interval avoidance for selected factors has no established closure property under arbitrary products. No induction establishing the universal condition appears in the candidate or follows from these lemmas.

The illustrative matrix h₀=[[2i,1/2],[−1,−i/4]] is correctly calculated: determinant 1, trace 7i/4, bc=−1/2, and endpoints −2i and 2i. Its eigenvalues are i(7±√113)/8, of unequal moduli, so it is loxodromic. Its image of L meets L at height 2. This refutes only the proposed shortcut that the loxodromic classification by itself forces interval avoidance. It gives no discrete faithful compression-body representation with the required marked normalization, and therefore is not a counterexample to the conjecture.

Even universal interval avoidance at a particular structure would establish proper embeddedness of the unique geodesic in the core's proper homotopy class. It would not, without an additional topological argument, establish the specified core isotopy class. Homotopic proper embedded arcs need not generally be isotopic, and inserting a local knot does not automatically preserve the property of being a core tunnel. The candidate correctly avoids both invalid implications.

A deformation argument would need a marking-compatible identification of the cusp-truncated manifolds and a family of proper embedded arcs throughout a compact parameter interval, including the endpoint. Under those conditions isotopy extension applies. Mere continuity of geodesic representatives, openness of a visibility condition, or connectedness of a deformation space does not supply those hypotheses. Neither does an assertion that some compression disk exists topologically: the cited sufficient theorem requires a disk avoiding all Ford-spine faces at each parameter.

Finally, a minimally parabolic argument does not settle all geometrically finite structures. An argument at a limiting structure with accidental parabolics needs its own control. Embeddedness can fail in a limit. The accepted partial algebraic statements themselves remain valid there; it is the suggested path-to-isotopy route whose extension is unproved.

## 8. Source and scope verification

The official Oberwolfach report was checked in context, including a visual inspection of printed p. 2436. Its question has one handle, torus negative boundary, genus-two positive boundary, geometrically finite structures, and isotopy. The EMS landing page agrees and identifies the report as volume 5 (2008), published in September 2009. [EMS report](https://ems.press/journals/owr/articles/2089)

The Lackenby–Purcell PDF was checked for the core definition, the marked group, and the homotopy construction. Visual inspection of preprint pp. 2 and 27 confirmed that Conjecture 1.1 is the target, while Theorem 5.10 requires a real-analytic minimally parabolic path starting from a one-face spine plus a disjoint compression disk at each positive parameter. Ford duality is a stronger conjecture, and the no-internal-moves path is a separate question. No universal theorem is being inferred from these conditional statements. Current arXiv metadata still identifies v2, dated 12 February 2014. [arXiv](https://arxiv.org/abs/1302.3652) [Author's institutional publication record](https://research.monash.edu/en/publications/geodesics-and-compression-bodies/)

The Burton–Purcell PDF was checked for Theorem 1.1, the generator change in Theorem 3.3, and the exact hypotheses of Lemma 4.3; preprint p. 14 was visually inspected. The counterexample construction has n≥2 handles. Its changed generators δ_k=γ_k⁻¹γ_n with k<n leave no claimed self-intersecting tunnel when n=1. It cannot be specialized to a one-handle counterexample by replacing an independent handle with a peripheral element. Current arXiv metadata identifies v2, dated 11 September 2013. [arXiv](https://arxiv.org/abs/1302.5469)

PDF identities were independently rehashed against the existing retrieval records:

- Oberwolfach report: 537,473 bytes; SHA-256 `819451936cd9990413455938b5ec318661a40fd577ed8fa75e5b03bd7ec3d856`.
- Lackenby–Purcell: 453,247 bytes; SHA-256 `b970756d1d24aa5719c885d94e2dc6d96a0d1cdb40a4d424fdeee33e856430fd`.
- Burton–Purcell: 464,320 bytes; SHA-256 `362fffde4cb62990341705eed7a51410ead2dba455d849dce1a2b94274d3ba3c`.

The audit's additional searches did not find a later primary-source resolution. This is a bounded search result, not a proof that none exists. No conclusion was taken from an inaccessible DOI response or an automated secondary summary.

## 9. Final acceptance boundary

The accepted results are exactly:

1. The normalized forbidden-interval criterion, including properness and every degeneracy exception.
2. Exclusion of peripheral elements and all witnesses pγq and pγ⁻¹q with p,q∈P.
3. Exclusion of every nonzero power of pγ for p∈P, in the given normalized marking.
4. The conditional isotopy route only under its explicitly stated entire-path embedding and marking hypotheses.

The unresolved obligations are exactly the arbitrary mixed-word condition, the core isotopy class, and the full geometrically finite endpoint scope of any future minimally parabolic path proof. **This is not an acceptance report for a proof or disproof of Problem 30001048.**
