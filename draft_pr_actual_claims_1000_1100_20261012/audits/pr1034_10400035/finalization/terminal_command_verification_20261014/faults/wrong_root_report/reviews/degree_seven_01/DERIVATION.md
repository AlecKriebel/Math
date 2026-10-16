# Independent derivation of the degree-seven mechanism

Written before reading `AUDIT_KERNEL_ORDER_SEVEN.md`, acceptance, or priority files. The only candidate mathematical inputs read for this derivation were `PROOF_KERNEL_ORDER_SEVEN.md` and `MARKED_FREE_REVERSAL_LEMMA.md`. Fresh primary bodies were retrieved independently. No other new review family was read.

## Claim, category, and success criteria

Let C be an oriented smooth ball represented by a corner-rounded D²×[0,1], with two distinct labeled endpoints p₁,p₂ on the real disk diameter. Strands are upward-oriented smooth proper arcs, standard in endpoint collars. Equivalence is an ambient smooth isotopy fixing the boundary and, after collar straightening, a smaller boundary collar. No strand framing is specified.

Let F₂ consist of links whose actual exterior π₁ is abstractly the free group of rank two; the bottom meridians need not be a chosen free basis. Let Vₙ(2) be Q-valued ordinary finite-type invariants of order at most n, and Nₙ(2) their subspace vanishing on every member of F₂. The target is an element v∈N₇(2) with a nonzero degree-seven symbol. It would establish exact order seven and Nₙ(2)≠0 for all n≥7, without proving minimality or a higher-strand result.

The proof has three independent obligations: (G) all actual free exteriors satisfy the exact labeled reversal, (D) a reversal-odd rational degree-seven symbol survives ordinary deframing, and (I) that symbol integrates in the ordinary rational category. A finite sample of links cannot substitute for G. A framed symbol cannot substitute for D. A numerical Lie-weight certificate alone cannot substitute for I.

## G1. Recover the handlebody from actual freeness

Delete open regular neighborhoods of the two arcs to obtain H. Its boundary is the four-holed outer sphere P and two joining annuli Aᵢ. Since χ(P)=−2 and each annulus has χ=0, the closed connected boundary has genus two. The open complement retracts onto H.

For a sphere Σ in int H, smooth Schoenflies in the ambient ball supplies the bounded-side ball B. Each connected tube Nᵢ meets ∂C and is disjoint from Σ, so it lies on the other side of Σ. Consequently B⊂H. This proves irreducibility without a conclusion about the knots obtained by closing the arcs.

Every positive-genus closed boundary surface has nonfree fundamental group. An injection of that group into a free π₁ would contradict the fact that subgroups of a free group are free. Noninjectivity and the Loop Theorem give a compressing disk. Cutting on it preserves irreducibility: a sphere disjoint from the disk bounds an interior ball in the uncut manifold, and a connected disk with its boundary on the manifold boundary cannot enter that ball while avoiding the sphere. Van Kampen after reattaching the one-handle expresses component groups as free factors, so they remain free. Repeat. The positive-boundary complexity Σ(3g−2) strictly decreases under every essential compression, including torus and separating-disk cases. Final components have spherical boundary and are irreducible, hence balls: a pushed-in boundary sphere bounds a ball on the side away from its boundary collar. Reverse the cuts to reconstruct H from balls and one-handles. It is a genus-two handlebody.

This step fails if one replaces actual π₁ by nilpotent quotient data: that would not supply the subgroup contradiction. It also does not require meridians to generate π₁.

## G2. Construct the exact marked map on the closed boundary

Put r(z,t)=(conjugate(z),1−t). Its three-dimensional determinant is +1. Its fixed endpoint coordinates are pᵢ, so it preserves labels. For an upward parameterization γᵢ, define (ργ)ᵢ(s)=r(γᵢ(1−s)).

Choose orientation-preserving tube charts qᵢ:D²ε×[0,1]→Nᵢ, satisfying qᵢ(0,s)=γᵢ(s) and qᵢ(z,s)=(pᵢ+z,s) near both ends. The normal bundle over the interval is trivial; both endpoint frames lie in the same component of the oriented frame space, so they extend. Integer twists produce different allowed charts, not an endpoint obstruction.

On P prescribe τ=r pointwise. On Aᵢ prescribe τ(qᵢ(z,s))=qᵢ(conjugate(z),1−s). The maps agree in full product neighborhoods of the seams because the charts are standard near the ends. Disk reflection and interval reversal each have determinant −1, giving determinant +1 together. The boundary map is an orientation-preserving involution. It has two fixed points on P and two on each Aᵢ. These are six isolated fixed points, not fixed circles. The branched Euler formula gives −2=2χ(∂H/τ)−6, hence quotient sphere.

There is an especially useful exact conjugation description. For the trivial exterior H₀ with identical outer endpoint disks, define φ:∂H₀→∂H as identity on the literal P and by tube charts on annuli. Then τ=φ(r|∂H₀)φ⁻¹. This is a boundary diffeomorphism only. Assuming that φ extends would beg the tangle problem; the proof does not do so.

## G3. Extend the map, then restore exact values and germs

Let f:H→H₀ be any orientation-preserving handlebody diffeomorphism. Then fτf⁻¹ on ∂H₀ is conjugate to the standard hyperelliptic map by fφ. Centrality of that map in the closed genus-two surface mapping class group gives [fτf⁻¹]=[r|∂H₀]. Hence F₀=f⁻¹rf is a handlebody diffeomorphism whose boundary σ is isotopic to τ. This is where genus two is essential.

Choose δₜ with δ₀=id and δ₁=τσ⁻¹. In a collar c(x,u), the map K(c(x,u))=c(δλ(u)(x),u), with λ=1 near the boundary and λ=0 at the inner edge, is a diffeomorphism. The u coordinate is unchanged, so injectivity and nonsingularity do not depend on how the intermediate δₜ moves the annuli. K∘F₀ has boundary value τ exactly. The isotopy is allowed to move P at intermediate times because no tubes are glued then. Its endpoint restores P pointwise to the prescribed r.

For smooth gluing, equality of boundary values is not itself sufficient; normal derivatives must also match. Let Jᵢ=qᵢ◦((z,s)↦(conjugate(z),1−s))◦qᵢ⁻¹ on a tube. Together with r near P, this gives a compatible local diffeomorphism germ across the boundary pattern, because the qᵢ charts are standard at the seams. Uniqueness of smooth collars relative to their boundary permits the exterior extension to be adjusted to this local germ. Equivalently, use a collar pulled back by the prescribed germ and straighten the extension to the resulting product map. The positive normal derivative condition eliminates a component obstruction. This adjustment changes only the exterior side and leaves τ on the boundary. Equivariant corner rounding is possible for the explicit finite-order local maps. There is no use of a PL Alexander trick as a smooth isotopy theorem.

Now glue Jᵢ to the corrected extension. The result h:C→C is smooth and orientation preserving, equals r on a small boundary collar, and satisfies h(γᵢ(s))=γᵢ(1−s). It need not have order two. Set g=r∘h. Then g=id on that collar and g(γᵢ(s))=(ργ)ᵢ(s). These are literal equalities, so no pure-braid factor, label exchange, or four-holed-sphere map remains.

The relative-ball diffeomorphism theorem supplies a smooth isotopy from g to id. The version fixing a small collar follows from parametric collar straightening (or the usual neighborhood-relative convention for Diff rel∂). Extending the isotopy by identity gives the corresponding long-link equivalence. Thus every L∈F₂ satisfies L=ρL in the required marked ordinary category.

## G4. Identify the orientation operation rather than an ambient mirror

For standard long lines (i,0,t), component-parameter reversal turns their ends downward. The rigid map R(x,y,z)=(x,−y,−z) restores them to the original upward labeled lines. After translation and rescaling in z this is exactly r. It has determinant +1 and fixes the component coordinate i. Simultaneously reversing both tangent orientations does not change a crossing sign; orientation-preserving ambient motion also preserves the local positive/negative resolution convention. Thus pullback by ρ preserves finite-type order and acts on symbols by the support-order reversal without a component permutation. A half-turn exchanging left and right labels, or a mirror of oriented space, would fail this test.

## D. Fresh algebraic nonzero and deframing checks

Inspecting the complete heptapus drawing gives seven cycle vertices and seven legs, with counterclockwise cyclic colors 1121222 (up to cyclic rotation). Its degree is (7+7)/2=7. Reversal is odd because there are seven legs. The blackboard vertex convention can reverse a global sign of the weight calculation but cannot change nonzeroness or the odd eigenspace.

An independent exact identity uses adX=LX−RX on Mat_N. For a length-seven word w, expansion yields all 128 choices of left and right factors. The left factors keep their order and the right factors reverse order; right-factor count supplies the sign. Because Tr_End(Mat_N)(L_A R_B)=Tr(A)Tr(B), cyclically grouping those choices gives

P=N(T₁₁₂₁₂₂₂−T₁₁₂₂₂₁₂)+3T₂(T₁₁₂₂₁₂−T₁₁₂₁₂₂).

The fresh script `artifacts/independent_wheel_check.py` verifies the grouping rather than assuming it. Using the submitted integer matrices merely as challenge data, it computes T₂=−2, T₁₁₂₁₂₂₂=38, T₁₁₂₂₂₁₂=20, T₁₁₂₂₁₂=−12, T₁₁₂₁₂₂=−23. The polynomial is 6. Two additional channels, direct evaluation of all 128 terms and direct multiplication of independently constructed 16×16 adjoint matrices, also give 6. Reversing the word gives −6. Cyclic rotations remain 6. Mutating the coefficient 3 to 2 gives −18 and fails equality. Normal and `python3 -O` outputs agree because checks are explicit exceptions, not assert statements.

The Lie construction respects AS and IHX by the alternating invariant tensor and Jacobi identity, so a nonzero value proves the rational diagram class nonzero. This fresh arithmetic avoids depending on eventual necklace independence for large N. It proves neither a nonsingular link value nor integration.

Ordinary deframing removes the two single-color struts. Connectedness alone needs the algebraic qualification: a connected nonsingle-strut class is primitive, and the framing generators are central degree-one primitives. The ordinary quotient has a complementary primitive algebra, so a degree-seven primitive is not forced into the ideal generated by the deleted degree-one struts. The cited deframing lemma identifies the symmetrized heptapus with that ordinary subalgebra; it does not assert that arbitrary framed classes automatically survive. There is no independently specified ribbon framing in G to create an unrelated framing obstruction.

## I. Rational duality, integration, and exact order

Let d be the nonzero ordinary rational degree-seven class from D, and τ_A(d)=−d. Finite-dimensional rational linear algebra gives a weight system W with W(d)=1. Define W⁻=(W−W◦τ_A)/2. Then W⁻(d)=1 and W⁻◦τ_A=−W⁻. This is dual action on functionals, not a sign assumption about scalar multiplication on invariant values.

The rational ordinary integration theorem gives f∈V₇(2) with symbol W⁻. Define v=(f−f◦ρ)/2. Naturality of the singular-resolution symbol, verified by the sign-preserving G4 operation, gives σ₇(v)=(W⁻−W⁻◦τ_A)/2=W⁻. Hence σ₇(v)(d)=1; v has exact order seven and is a nonzero function. If all nonsingular values were zero, every singular-resolution alternating sum and hence its symbol would be zero, contradicting this value.

For each free link, G gives f(L)=f(ρL), so v(L)=0. Thus v∈N₇(2), and inclusion of finite-type filtrations gives the same nonzero member in every Nₙ(2), n≥7. No all-k consequence, classification of Nₙ, or information on orders 3–6 follows from this argument.

## Primary-source interfaces used

- [Duzhin–Karev v5](https://arxiv.org/pdf/math/0507015v5), dated 25 July 2005: printed pp.1–3 establish labeled inversion and rational ordinary symbols; Lemma 4 gives odd-leg action; Proposition 2 displays the seven-wheel; Section 6/Lemma 8 supplies ordinary deframing. Full body retrieved and controlling pages visually inspected.
- [Bruno–Mecchia](https://rendiconti.dmi.units.it/volumi/46/014.pdf), printed p.272: genus-two boundary hyperelliptic extension and commutation up to isotopy. The stated fact is about the closed surface/handlebody and is not restricted to the later hyperbolic examples.
- [Hatcher, Basic 3-Manifold Topology](https://pi.math.cornell.edu/~hatcher/3M/3Mfds.pdf), printed pp.1 and 56: smooth sphere and Loop Theorem inputs. The compression and terminal-ball arguments above are independently supplied.
- [Hatcher, Smale Conjecture](https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf), printed p.604, Appendix (1): contractibility of the smooth ball diffeomorphism group relative to boundary. Visually inspected because its extracted text has defective encoding.

Haas–Susskind and Nogueira are unnecessary for this derivation; no inaccessible statement is taken as a premise. Source hashes and fetch timestamps are in `SOURCE_FETCH.json`. All copied primary bytes, extracted bodies, and source renderings are restricted to `sources/raw/`.
