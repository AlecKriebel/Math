# Separate verification of the exact-homology supplement

Checked 3 October 2026 after the original research packet and its independent audit were frozen. The author of the original lower-bound calculation separately checked the audit's stronger calculation. **Verdict: the supplement is valid.** This is an additional AI-assisted mathematical check, not human peer review or a solution to OPG-37237.

## Checks of the new steps

1. For an injective HNN extension J with vertex group V and edge group W, exactness gives b₂(J)=b₂(V)−ρ₂+b₁(W)−ρ₁ and b₁(J)=b₁(V)−ρ₁+1. Subtracting cancels ρ₁. This verifies the supplement's formula for δ=b₂−b₁, including the final +1 from the loop in the graph of groups.
2. Replacing t by p=P⁻¹tP rewrites Γ₃ as a centralizing HNN extension along P⁻¹⟨c,d⟩P. Britton reduction gives the claimed subgroup presentation for Δ on c,e,p. Although the intersection need not be trivial or finitely generated, every added relation is a commutator. Since ⟨c,e⟩ is free, Δ has abelianization Z³. No freeness assertion about Δ is used.
3. The edge A has rational first and second Betti numbers both three. Its two abelianized power relations kill d and e over Q, leaving s,c,t. The original checked HNN calculation gives b₂(A)=3. The edge C=F₂×Z has b₁(C)=3 and b₂(C)=2.
4. The successive lower bounds on δ are therefore 0,4,5,7,6,6. Since b₁(Γ₆)=1, this proves b₂(Γ₆)≥7 without needing either unknown H₂ difference map explicitly.
5. The source's three-generator/nine-relator presentation has a presentation 2-complex with rational boundary rank two because its first Betti number is one. Therefore its second Betti number is seven. The Hopf surjection to group H₂ gives the reverse inequality, so b₂(Γ₆)=7.

The finite arithmetic was replayed independently. All old public hashes and all independent-audit hashes still match their manifests, and the author and audit verifiers reproduce their saved outputs exactly. The proof does not infer asphericity or abstract group deficiency from a chosen presentation.

## Scope

The exact value applies only to Γ₆ in Kegel–Li–Ren, arXiv:2609.10461v1. It strengthens an exclusion of one proposed input group. The existence of an undecidable smooth/locally flat PL 2-knot group in standard S⁴ remains unresolved here. No novelty claim is made.
