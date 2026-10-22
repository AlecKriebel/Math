# Research log: KP-4.64

Date: 2026-10-03, UTC. Five distinct mathematical approach families were developed. The count records substantive construction/obstruction attempts; source identification and repository checks do not count as an attempt.

## Source and scope checkpoint, 20:38 UTC

The live catalogue request returned HTTP 403. The pinned catalogue was used only to identify Problem 4.64 and its primary source. The complete 2026 K3 preliminary author PDF was fetched successfully and the exact question and remark were read on p. 242. No prior target-specific repository attempt or PR was located after identifier/name searches and direct directory checks; a queued row alone was not used as evidence of no prior work. Current-source searches did not locate a later resolution. Discovery completion estimate: 0%; no valid irreducible example.

## Attempt 1: multiply known monopole classes

Mechanism: Bauer's connected-sum product, using the K3 spin class and Hopf powers. Work: computed χ, σ, b±, index and expected dimension for #ᵐK3; checked the two-/three-factor nonequivariant detection and the distinct four-factor equivariant criterion. Outcome: m=2,3,4 give the desired separation but each is visibly reducible. The fifth factor does not improve this route. Gap: no irreducible replacement and no right to cancel a displayed neck by comparing only forms. Detailed proof: §2.

## Attempt 2: force a torsion-valued invariant

Mechanism: the Hurewicz kernel rather than the underlying integral SW invariant. Work: matched the original BF-I kernel calculation with Bauer's later primary-component description, recovered k=0/four injectivity, and derived the r-even and b⁺ congruence restrictions for k=1/two. Outcome: exact necessary conditions within b₁=0,b⁺>1,r≥2. Gap: a nonzero stable cohomotopy group does not imply realization by a monopole map, much less irreducibility. Detailed proof: §3.

## Attempt 3: glue along −2 spheres

Mechanism: replace the connected-sum S³ neck by the RP³ boundary of a −2 disk bundle. Work: checked the full gluing statement and its 0/2 evaluation compatibility, proved the BF-support obstruction, reconstructed the positive-semidefinite support/reflection argument, and computed the resulting two-K3 topology. Outcome: χ=44,σ=−30,b⁺=6,b⁻=36; SW vanishes by parity, but all BF classes vanish too. Gap: this specific construction is excluded; a new gluing mechanism must escape its support obstruction. Detailed proof: §4.

## Attempt 4: spin rational-cohomology realization

Mechanism: replace invariant computations by the Furuta–Kametani–Minami nonvanishing theorem. Work: read the proof chain from the stabilized δ construction through the explicit two-Hopf model and Pin(2)-equivariant representative comparison to Theorem 19; verified that δ lives on the ordinary S¹ invariant. Combined it with a proof that every ordinary SW invariant vanishes when b₁=0,b⁺ is even. Also checked Theorem 20 and δ-bijectivity: the larger n≥3 family has zero spin-structure BF class despite the same abstract Z/2 target. Outcome: a rigorous sufficient realization criterion. Gap: no irreducible spin rational-cohomology K3#K3 is constructed; the larger-family vanishing is only for spin structures. Detailed proof: §5.

## Attempt 5: finite quotient of a reducible model

Mechanism: a free group action could potentially produce a quotient without the visible separating neck. Work: combined finite-cover signature/Euler multiplicativity and Betti parity to prove |G| divides gcd(16,3m+1). Outcome: no nontrivial free oriented quotient of an even K3 connected sum; among m=2,3,4 only the triple-K3 double-quotient case survives arithmetically. Gap: no suitable action, quotient irreducibility proof, or ordinary BF descent/computation for that survivor. Detailed proof: §6.

## Author synthesis checkpoint

All five routes have either a proved scoped obstruction or a precise unsatisfied realization condition. The proof is frozen with reproducible arithmetic controls and source attribution. Discovery completion estimate remains 0%: the target example and any universal obstruction remain absent. No probability of eventual solvability is inferred from that estimate. Separate adversarial review remains required before promotion.
