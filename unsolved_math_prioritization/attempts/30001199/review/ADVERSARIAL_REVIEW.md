# Independent full proof review: 30001199

2026-10-02. **PASS for the complete source-model circular LTI rule after3/5 author turns.** No mandatory mathematical correction. Recommended disposition already_solved3/5 with Kerber–van der Schaft2010 Theorem4 credited and this packet described as a complete alternative proof. No discovery/priority claim; AI-assisted audit is not human peer review or formal certification.

## Source scope and earlier dependency

The full source gate and all three proofs were read. Original OWR closed-feedback pages657–658 were visually inspected; the surrounding LTI/free-disturbance scope agrees with the theorem. The2010 indexed primary theorem and Lemma1/AppendixA were independently opened. Its displayed instantaneous-kernel enlargement fails in the recorded double-integrator identity example: the added signed hidden state has unequal derivative outputs. Both premises can be identities and all external-input matrices vanish. This is a failure of that auxiliary enlargement under the retrieved formula, not of the main rule. Binary/visual2010 PDF access remains unverified, and the packet correctly qualifies that limitation. The complete proof reviewed here does not rely on that enlargement.

## Quotient and graph reduction

A controlled-invariant N inside kerC admits a linear compensating disturbance feedback K. Quotienting A+LK is well-defined and the substitutions dbar=d−Kx and d=dbar+Kx prove both trajectory directions for arbitrary related initial lifts with unchanged interconnection input. Free, unrestricted disturbances are essential. Linear ODE existence and locally integrable signals suffice; no bounded-input result is claimed. Output-preserving product bisimulations and transitivity transfer both circular premises and the conclusion. Maximality of N* forces the reduced model's output-nulling subspace to vanish, including zero-dimensional quotients.

Every identically zero-output trajectory lies in each stage of the stated descending subspace iteration: derivatives stay in its current subspace almost everywhere, and continuity/closedness extend the needed algebraic condition to every time. Thus in a reduced specification such a state trajectory is zero. Output equality makes repeated context copies have equal inputs; their difference is precisely such a trajectory. Linearity plus the zero source trajectory also forces uniqueness of the remaining target state. Fullness therefore gives the two graph maps with no missing fiber.

## Algebra and nilpotence

Direct differentiation in the first negative-feedback premise gives EA2−A1E+(B1−F BP1)C2 with image in V1; the second gives HA1−A2H+(J BP2−B2)C1 with image in V2. Context-disturbance variations give EV2⊂V1 and HV1⊂V2. These signs and inclusions yield CK=0, KV1⊂V1 and [K,A1]−DC1 with image in V1 for K=EH, D=E(B2−J BP2).

The stable-image lemma is correct. At stabilization every y in imK^m can be written K^m x with x in imK. In the commutator sum all DC terms vanish, either by CK^r=0 or by Cx=0, and error terms remain in V by K-invariance. Hence the stabilized image is controlled invariant and output-nulling. It is zero after quotienting, proving nilpotence. This uses finite dimension only, not spectral stability or a contraction assumption. The finite inverse I+K+...+K^(m−1) preserves V1.

## Fullness and disturbances

The inverse explicitly solves the two simultaneous graph equations for every implementation state pair, independently of future disturbances. Its graph is linear/full and preserves both outputs. Each residual r_i is in the correct target disturbance image by using one premise with zero context disturbance at the related state. The stated finite inverse solves v1−Ev2=r1 and v2−Hv1=r2 while keeping v_i in V_i. Fixed right inverses of L_i on their images select admissible signals even when L_i is rank-deficient or zero. The target trajectory defined by the graph has exactly those derivatives, preserving the relation and output for every implementation disturbance. Lifting through the earlier bisimulations handles arbitrary original related initial lifts. All required quantifiers of full simulation are met.

The historical one-injective-specification and controlled-invariant-kernel partials are consistent with the final argument. They do not impose extra assumptions on the final theorem. Nonlinear systems, algebraic constraints, restricted disturbances and different semantics remain outside scope.

## Verification and integrity

All29 final-manifest entries and the author manifest c2d4f99220438261828f8f48723fb1718f5729e61cb17832d2e910d3c73b0b89 were checked as raw bytes. All three exact rational proof-check receipts and the dependency receipt replay byte-identically:7,375 assertions. The exploratory finite-field search is retained as bounded proposal evidence, not a universal proof and not independently rerun here.

Separately written integer controls exhaust5,500 eligible2x2 stable-image fixtures, verify the nilpotence consequence whenever the controlled output-null space vanishes, and check1,000 strictly-upper-triangular Neumann disturbance systems. Total8,428 independent assertions. These supplement the universal proof rather than establish it. Primary-source theory credit and the indexed-2010-access qualification must remain prominent. No additional author turn is needed for a complete source-model answer.
