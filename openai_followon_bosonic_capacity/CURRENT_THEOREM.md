# Exact theorem and operational status

Theorem scope and validation limits. Current complete-package review and publication status are maintained separately in publication/ and reviews/; the source archive is a fixed mathematical snapshot.

For the pure-loss channel L_eta, eta in [1/2,1], n uses have independent vacuum environments. Arbitrary signal entanglement across uses is permitted. Constraint: total mean photon number of the message/key/randomness-averaged input <= nN, with finite N>=0. No peak/per-codeword constraint. Logarithms base2. Forward signed net resource rates have finite gross generation/consumption rates and exponentially finite registers; no superlinear catalysts or free feedback.

## Quantum theorem
The exact C/Q/E region is the closed union lambda in [0,1] of
C+2Q <= g(lambda N)+g(eta N)-g((1-eta)lambda N),
Q+E <= g(eta lambda N)-g((1-eta)lambda N),
C+Q+E <= g(eta N)-g((1-eta)lambda N).
Basis: externally attributed OpenAI finite-energy multimode EPnI, analytically audited; original regularized quantum coding theorem; explicit photon-cost approximation and closure. The original formulas and conditional reduction are WHG's, not new inventions.

## Literal private target: refuted
WH arxiv1005.3818v3 Sec5 before Eq14 protects U=(M,T_A,J,S_B) jointly from (K,L,E^n), with pi^U a mutually independent uniform product. At N=0, all bosonic inputs/outputs are vacuum. Reliability and that predecoding condition imply
1 <= 1/(d_M d_T_A)+(epsilon_sec+epsilon_rel)/2.
Vanishing errors force both generated private/key dimensions to1 regardless consumed gross resources. The nominal region contains OTP(-1,1,-1), hence cannot be the literal source's capacity region. This is a counterexample to the unchanged requested positive assertion, not full success for it.

## Explicit repaired private theorem (GEN)
Fresh uniform communication messages K,M are initially independent of consumed key S_B; public communication is not unrestricted common-randomness generation. Protect generated W=(M,T_A) by ||omega^(W X E)-pi^W tensor omega^(X E)||_1 ->0, X=(K,L). Consumed V=(J,S_B) is traced out and may become correlated. Eve has all public transcript and complement output, not an extra revelation of consumed key. This is uniform-message trace secrecy, not semantic security.
The exact region in this explicitly different model is the closed union of
R+P <= g(eta N),
P+S <= g(eta lambda N)-g((1-eta)lambda N),
R+P+S <= g(eta N)-g((1-eta)lambda N).
Corrected converse and direct packing/covering achievability are supplied, with energy selection. Standard finite gross resource composition is explicit. The original private theorem with its printed stronger condition is not used as a valid black box.

## Validation limits and exclusions
No completed Lean build, axiom report or formal verification of follow-on capacities. Source semantic audit found full Fock states and actual channel/entropy, no visible proof placeholders in the26-module closure. Analytical proof is the decisive upstream validation basis.
N=0, lambda endpoints and eta=1/2,1 are included. No thermal quantum capacity, amplifier, two-way-assisted, semantic-security, confidential-broadcast or stronger cost claim. Optional additive-noise extension withheld from this package.
