# Question 10.21: five-turn scoped results on Spin^c phase lifts

**Original target: unsolved, 5/5 substantive author turns. Independent review pending.**

This packet concerns Deloup's Question10.21 in Ohtsuki's 2002 problem collection, printed p.526: a mod16 lift of the Spin^c quadratic Gauss–Brown phase, motivated by a degree-one invariant. The abbreviated original does not explicitly specify connected-sum additivity or complete spin-Rochlin recovery. Neither is silently imposed as an axiom of the original question. The finite Gauss phase also needs a domain qualification for non-torsion Chern classes. These points are part of the source audit, not grounds for replacing the question by an easier one.

## Exact normalization and strongest positive theorem

For a finite nonsingular quadratic function q, write gamma(q)=sum_x exp(2 pi i q(x)) and B(q)=8 arg(gamma(q))/(2 pi) in Q/8Z. The rational target for a lift is Q/16Z. Nonhomogeneous q can have nonintegral B; the Z3 example in Turn1 has B=2/3. Thus restricting every answer to Z/16Z would already misstate the phase.

Fix a convention sign epsilon so that B(q_s)=epsilon R(M,s) modulo8 for spin structures. Epsilon=+1 matches the relationship in the original problem; epsilon=-1 uses the published Deloup–Massuyeau/Massuyeau boundary-quadratic convention. Negating all quadratic functions exchanges the conventions.

**Theorem A (canonical odd-Chern lift).** Let M be a closed connected oriented rational homology three-sphere and sigma a Spin^c structure whose Chern class has odd order, including order one. There is a canonical spin structure s_sigma obtained as follows: take the unique odd-primary half a_odd of c1(sigma), subtract it from sigma, and use the unique spin structure inducing the resulting zero-Chern Spin^c structure. Put q0=q_(s_sigma), and define the unique a in H1(M;Z) by

    q_sigma(x)-q0(x)=b(a,x).

Then a has odd order. Let eta be the unique odd-order group section Q/Z→Q/2Z on the odd-order subgroup. The formula

    R_oddChern(M,sigma)=epsilon R(M,s_sigma)-8 eta(q0(a))

is a natural Q/16Z-valued lift of B. It is additive under connected sum within this class, changes sign under orientation reversal, agrees with epsilon R on spin-induced structures, and has **degree exactly one** for the source's Spin^c Y-surgery convention restricted to this class.

**Proof summary.** On a rational homology sphere H¹(M;Z)=0, so the Bockstein identifies H¹(M;Z/2) with H²(M;Z)[2]. The spin-to-Spin^c map is injective and its image is the zero-Chern set. This makes the spin origin unique after the canonical odd-primary subtraction. Affinity and nonsingularity determine a; its odd order makes q0(a) odd-primary. Completing the square gives B(q_sigma)=epsilon R-8q0(a). Eta is the unique odd-order preimage under reduction modulo1, so no branch choice is left. Y-surgery canonically transports the Chern class, spin origin, quadratic functions and a. Therefore the correction term is degree zero. The classical spin-Rochlin finite-type theorem makes the first term degree at most one. Its values on the Poincare sphere and S3 show it is not degree zero. Orthogonal-sum splitting and the homomorphism property of eta prove additivity. Full proof, conventions and primary hypotheses are in Turns2–3.

The domain includes every spin-induced structure, every structure on odd-order H1, and every structure when the 2-primary H1 summand has exponent at most two. It does **not** include a rational homology Spin^c structure with nonzero 2-primary Chern class, or arbitrary manifolds of positive first Betti number.

## Other rigorously scoped results

1. **Quadratic-data obstruction (Turn1).** No isometry-invariant, orthogonal-sum additive lift of B exists on all finite nonsingular quadratic functions, even homogeneous ones. An explicit isometry between four copies of q_+(1)=1/4 and four copies of q_-(1)=-1/4 forces contradictory lifted values4 and12. This also excludes an additive degree-zero topological lift on all rational homology Spin^c spheres. It does not exclude degree-one topology.
2. **Conditional unrestricted additive obstruction (Turn2).** No connected-sum additive Q/16Z invariant on all closed oriented Spin^c three-manifolds can reduce to B on all torsion-Chern structures. The published non-torsion absorption diffeomorphism on S2×S1#RP3 identifies the two RP3 labels after connected sum; additivity would force their unequal Brown phases to agree. The word “additive” is essential and is not supplied by the original question.
3. **Non-torsion finite-section ambiguity (Turn1).** On (Q/Z)⊕Z2, the fixed quadratic q(r,j)=j²/4-r has two quotient sections with Gauss phases±1/8. It comes from the split0/2 surgery lattice and a non-torsion Chern class. An arbitrary finite section is therefore not a canonical definition of the original phase in that domain.
4. **Higher-two-primary descent equations (Turn4).** For a nonsingular characteristic surgery pair (B,c), the defect D=signature(B)-cᵀB⁻¹c lifts Brown modulo8. The exact representative-change formula is D(c+2Bz)-D(c)=-8 rho_c(z), where rho_c(z)=(cᵀz+zᵀBz)/2 modulo2, with its proved cocycle law. Turn4 gives the full Kirby correction rules and the two-Y-surgery parity equation for D+8e. A fixed +4-unknot example gives raw lifted values0 and8 for the same Spin^c structure, and the naive principal spin-origin prescription has the same ambiguity. The correction system is derived, not solved.
5. **Floer route obstruction (Turn5).** The canonical lift -4d exists on all rational homology spheres in the positive convention, but is not degree at most one: it gives8 and0 on -Sigma(2,3,5) and Sigma(2,3,7), which have the same Rochlin value and are Y2-equivalent. The Euler-corrected lift 8(chi_red-d/2) equals Rochlin on integral homology spheres. Its general degree-one property is equivalent to an unproved evenness of the second surgery difference. The known normalized-torsion identity and augmentation-ideal finite-type bounds do not establish that parity.

The exact scalar-lift torsor in Turn3 explains why an arbitrary degree-zero phase branch, even with a piecewise homology-sphere correction added, is not being promoted to a meaningful solution of the intended refinement. The claimed affine/conjugation origin obstruction there is only a finite-torsor model under explicit extra equivariance assumptions; no diffeomorphism is inferred from an abstract torsor translation.

## Original gap

A natural geometric degree-one refinement across the higher-two-primary Chern classes has not been constructed or universally obstructed. The positive-Betti-number torsion-Chern domain is also outside Theorem A. General non-torsion structures need a precise phase definition or additional data; the short source statement does not resolve that issue. Requiring exact recovery of spin Rochlin on every three-manifold is already impossible by Deloup–Massuyeau's credited T3 example, but that stronger requirement is not the original scalar-lift problem itself.

No unrestricted solution, universal impossibility theorem, or historical novelty is asserted. A bounded current primary-source search did not verify a later complete answer; that is not a proof of current openness. Five substantive turns are exhausted. Independent review may audit or correct these claims, but no additional author search is hidden in review or packaging.

## Reproducibility and files

Read SOURCE_SCOPE.md, then SOURCE_CLAIM_MAP.md and all five turns in order. The source manifest pins ten full primary PDFs retained only as reading inputs. They are not redistributed. Each turn has an exact checker and saved JSON receipt. Run `python checks/verify_turnN.py` from this directory and compare stdout with `checks/TURN_N_CHECKS.json` for N=1,...,5. The first four scripts use installed SymPy; Turn5 uses only the Python standard library. Counts are2,376;167,961;15,401;11,644;3,098. These finite controls supplement mathematical proofs and source verification; they cannot certify the cited topological/Floer theorems or solve the remaining parity condition.
