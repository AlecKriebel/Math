# Fresh delta audit: different-character coabelian doubles

Reviewer: `/root/p21126_superexp/double_adversary`; UTC: 2026-10-24T21:30:57.183941+00:00. Exact input: `../ASYMMETRIC_CHARACTER_DOUBLE.md`, hashed in ASYMMETRIC_CHARACTER_RECEIPT.json.

**Outcome: PASS within the explicit extendable-character hypotheses.** I independently reconstructed the fiber-product equality, finite-presentation step, rational extension variant, surface-product character extension, and conditional finite iteration. No substantive objection remains. This is a route obstruction, not a solution of 21.126 or a priority certificate.

## Direct primary-theorem inspection

I read the cached primary PDF text of Claudio Llosa Isenrich, arXiv:2404.12334v2, with version header 30 October 2024. On printed p.2, Corollary 1.3 states the exponential Dehn upper bound for a finitely presented kernel of a homomorphism from a finitely presented synchronously OR asynchronously automatic group to a finitely generated abelian group. It is stated for a homomorphism and does not require surjectivity. Theorem 1.2 preceding it explains the area-radius bound behind the corollary. Thus the application is not an inference from an upper bound on δ_G(exp n), and does not assume that a finitely generated kernel N is finitely presented.

The relevant kernel for the corollary is D=ker Ψ, which IS finitely presented by the amalgam presentation. It is not the possibly non-finitely-presented N=ker χ. Distinguishing these kernels is essential, and the note does so.

## Independent image-equality reconstruction

For onto χ choose t∈G with χ(t)=1. The two maps from D are fold to G and quotient to (G/N)*(G/N)≅Z*Z=F(u,v). Their product is injective by the already independently reviewed normal-double argument. Every generator from either copy maps to an element satisfying χ(g)=ε(w), so the image is contained in that equality fiber product.

For the reverse inclusion, take (g,w) with common height k. Replace each u in a reduced word for w by t in the first copy and each v by t in the second, with inverse letters lifted inversely. The quotient image is exactly w, and the fold is t^k because every folded letter is a power of the SAME t. Left multiplication by the common element gt^{-k}∈N therefore gives (g,w). The order of multiplication is correct even if g and t do not commute. This proves actual equality of the image, not only an embedding into a potentially larger kernel.

Inside A×F2, the equation Φ(a)=0 first forces a∈G. The remaining equation χ̃(a)=ε(w) then becomes χ(a)=ε(w). Thus the equality fiber product is exactly ker Ψ. Both coordinate expressions define homomorphisms to the abelian target B×Z; no conjugation invariance outside G is silently assumed, because χ̃ is an actual homomorphism on A.

If χ̃ restricts to mχ for a positive integer m, replacing the second equation by χ̃(a)−mε(w)=0 is equivalent, on G, to m(χ(a)−ε(w))=0. Torsion-freeness of the target Z gives the required equality. Neither surjectivity of Ψ nor primitiveness of χ̃ on A is needed.

## Finite presentation and ambient geometry

Two finite presentations of G together with finitely many relations identifying a chosen finite generating set of N give a finite presentation of the double. Relations of N itself need not be enumerated or finitely presented: every N-element is already a word in the identified generators, and both copies of G impose their own relations. This is the standard finite-presentation theorem for an amalgam over a finitely generated subgroup, and the normal-form injections ensure the intended factors.

The given A is synchronously automatic under the usual meaning of 'automatic'. F2 is automatic, and finite direct products of automatic groups are automatic. A×F2 is also finitely presented, either from its automaticity or explicitly from the two finite presentations and finite cross-commutation relations. All Corollary 1.3 hypotheses hold. Its conclusion is an intrinsic Dehn upper bound for D. The parenthetical statement about asynchronous factors is conditional on an applicable product structure and is not needed for this synchronous application.

Degenerate checks: G=Z with χ=id gives D=F2; G=Z² with a coordinate character gives Z×F2; trivial B and non-surjective Φ cause no problem. A zero character is excluded from the general onto lemma and separately gives the double G*_G G=G, as stated.

## Every character in the displayed surface-product example

An arbitrary χ on (Σ1×Σ2)⋊diagφ Z is determined by λ1=χ|Σ1, λ2=χ|Σ2, and c=χ(τ). Applying χ to the two separate conjugation relations gives λi∘φ=λi for each i. There is no cancellation between the two restrictions: each relation involves only its own factor. Consequently λ̃i(s_i t_i^k)=λi(s_i) is a well-defined homomorphism on Γ_i. The proposed formula

    χ̃(g1,g2)=λ̃1(g1)+λ̃2(g2)+c h1(g1)

is a homomorphism and evaluates on (s1,s2)τ^k to λ1(s1)+λ2(s2)+ck, exactly χ. This proves integral extension, including characters genuinely nonzero on the surface factors. If χ has image dZ, all λi values and c are divisible by d, so the normalized character is still integral and has the same extension formula after division. Its kernel is unchanged.

Automaticity of the mapping-torus Γ is an EXPLICIT hypothesis. It is not asserted for every surface automorphism. A closed fibered hyperbolic3-manifold supplies the advertised automatic example, and finite presentability of the displayed G follows from the finite semidirect-product presentation. Its Dehn function need not be exponential for every φ; the note explicitly avoids that assertion.

## Iteration and limitations

At each finite stage, the previous automatic ambient A_i is replaced by A_i×F2, and the next double is a kernel to a finitely generated abelian target. If the subgroup is finitely presented, the next character has finitely generated kernel, and some positive multiple extends to A_i, the same proof applies. The exponential constant may depend on the finite stage. No uniform constant or unconditional character-extension theorem for later doubles follows.

In particular, this audit does not promote the calculation for the exact semidirect-product G to a theorem about every character of an arbitrary finite-index subgroup of G. Nor does it assert extension for every later doubled group. Such extensions would need their own argument. The note correctly confines its iteration claim to stages where extension is supplied. It also supplies no super-exponential lower bound for a nonextendable character: failure of this filter alone would not prove a successful construction.

I found no counterexample or missing hypothesis in the exact statements. No publication, solved status, full priority claim, or conclusion about all finitely presented RAAG subgroups is approved.
