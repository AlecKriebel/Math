# Independent zero-energy check of the printed private coding criterion

Timestamp: 2026-10-07 UTC (2026-10-06 America/Los_Angeles). This is a materially distinct adversarial check from the family-273 entropy audit. Source inspected directly and independently: Wilde–Hsieh, *Public and private resource trade-offs for a quantum channel*, arXiv:1005.3818v3, https://arxiv.org/pdf/1005.3818v3, Section 5, printed p. 7, equation immediately before (14), together with (12)–(13). No other agent's proposed repair was used.

## Finding

The literal predecoding criterion is incompatible with the paper's own stated unit-resource conversions. It requires the **joint** register U=M T_A J S_B to be maximally mixed and independent of K L E^n. Here M and T_A represent generated private resources, whereas J and S_B represent consumed private communication and consumed secret key. The statement cannot literally mean only generated resources: it explicitly includes both consumed registers, and the following mutual-information condition uses the same joint U.

This is more than a failure of the obvious one-time-pad construction. Under the printed criterion, at N=0 **no protocol in the stated encoder/channel/decoder normal form can generate even a single reliable private bit or secret-key bit once its two errors are sufficiently small**, regardless of the quantities of consumed/catalytic public communication, private communication and secret key. The proof below is dimension-independent in the consumed resources and remains valid for arbitrary local encoding/decoding maps.

It follows that positive net private rate is impossible under the literal criterion: P=P_generated-P_consumed<=0. In particular, the unit-resource point (-1,1,-1), admitted by the claimed region and expressly identified with the one-time pad in Section 2, is excluded. The printed region and the literal Section 5 criterion therefore cannot both describe the same operational task at the mandatory zero-energy boundary.

## Precise general converse

Use trace norm without its customary factor 1/2, as in the source. Let d_M and d_T be the dimensions of the generated classical message M and generated key share T_A. Let epsilon_sec be the error in the printed predecoding condition and epsilon_rel the error in (13). Let U=M T_A J S_B and V=K L E^n. The criterion reads

`||omega_{UV} - pi_U tensor sigma_V||_1 <= epsilon_sec`,

where pi_U is the maximally mixed state on the entire tensor-product space, hence

`pi_U = pi_M tensor pi_T tensor pi_J tensor pi_{S_B}`.

At an exact average input photon budget N=0, positivity of total number implies that the average input state is the n-mode vacuum projector. That projector has rank one, so the full input together with any classical labels, quantum references, consumed secret shares, encoder ancillas, or other registers is a tensor product with the vacuum. Equivalently, a positive state whose number expectation is zero is supported on ker(N_total), which is one-dimensional. There is no nonzero-energy exceptional branch: nonnegative conditional energies with zero average vanish almost surely. Pure loss therefore supplies Bob with a fixed vacuum state B^n independent of every other register. This holds at every transmissivity, including eta=1/2 and eta=1, and allows arbitrary entanglement across channel uses beforehand.

Tracing the security condition down to M T_A L J S_B gives

`||omega_{M T_A L J S_B} - pi_M tensor pi_T tensor pi_J tensor pi_{S_B} tensor sigma_L||_1 <= epsilon_sec`.

Appending Bob's fixed vacuum and any independent local ancilla does not change this inequality. Apply the actual decoder D^{B^n S_B L J -> T_B Mhat Khat} and trace out Khat. Trace distance contracts. Under the ideal comparison state, the generated pair (M,T_A) remains uniformly distributed and independent of every decoder output. Thus the probability of the event

`G={Mhat=M and T_B=T_A}`

is exactly 1/(d_M d_T), whatever the decoder's output distribution. An event probability changes by at most half the trace norm, giving

`Pr_omega(G) <= 1/(d_M d_T) + epsilon_sec/2`.

Equation (13) compares the final state to perfect uniform correlated message and key states. Marginalization and the same event bound give

`Pr_omega(G) >= 1 - epsilon_rel/2`.

Consequently every such protocol satisfies the checkable inequality

`1 <= 1/(d_M d_T) + (epsilon_sec+epsilon_rel)/2`.

If d_M d_T>=2 and epsilon_sec+epsilon_rel<1, the right side is strictly below 1, a contradiction. Any sequence with both errors vanishing must therefore have d_M=d_T=1 for all sufficiently late blocks. In particular, generated private and generated secret-key rates are zero. There is no continuity bound with an unbounded catalyst dimension in this proof, no gross-rate boundedness assumption, and no Fano asymptotic loophole.

## Why catalytic gross rates do not fix it

The source starts with M independent of S_B and allows an arbitrary encoder to produce L, J and T_A. Sending M through a consumed private channel by choosing J=M creates precisely the M–J correlation that the maximally mixed pi_{M T_A J S_B} forbids. Adding more private-channel uses, larger shared keys, local randomness, or returned catalytic resources cannot change the general decoding bound above: all inputs Bob can use, except the fixed vacuum and independent local ancillas, are included in the ideal state that is independent of M T_A.

If a sequential protocol gives Bob an extra message-dependent memory before the security check and keeps that memory out of J S_B B^n, it no longer fits the normal form actually asserted in Section 5. If that memory is allowed, the quoted condition has ceased to be a general predecoding criterion. Such a re-timing or relabeling is a change of the stated operational model, not a catalytic escape within it.

Local bins accessible to Eve only add possible side information to Eve. They do not give Bob a correlated input outside the decoder registers or create a correlation absent from the ideal state. If consumed J or S_B is discarded only after decoding, the literal predecoding criterion still concerns the earlier state. Replacing those consumed registers by fresh randomness before decoding erases their useful information unless it is retained in an additional decoder memory, again outside the source normal form. Thus permitted private disposal does not invalidate this converse.

## Explicit one-time-pad calculation

For d=2^k, take independent uniform M,S in a group of d elements, retain the initial key share S_B=S, and transmit L=M+S. Bob recovers M=L-S. The actual distribution on (M,S_B,L) is uniform on d^2 triples satisfying L=M+S_B. For every comparison distribution of the printed form pi_{M S_B} tensor sigma_L, its total-variation distance from the actual distribution is at least 1-1/d (test the event L=M+S_B, whose actual probability is 1 and comparison probability is 1/d). A uniform sigma_L attains this bound, so the minimum trace norm is

`2(1-1/d)`.

It equals 1 for one private bit and tends to 2 at large block length. Generated-message secrecy alone is perfect: M is independent of L. Consumed-key secrecy alone is also perfect: S_B is independent of L. What fails is the unjustified demand that their **joint** (M,S_B) be independent of L. This illustrates the criterion error but is not needed for the general impossibility proof.

## Intended resource conventions and a possible repair boundary

The same primary paper explicitly admits the one-time-pad resource vector (-1,1,-1), secret-key distribution (0,-1,1), and private-to-public conversion (1,-1,0). Section 4 generates its unit-resource cone from those three vectors. Thus its stated intended net-resource model is the ordinary model in which the consumed key can be correlated with the public ciphertext jointly with the generated message. The Section 5 condition is inconsistent with that intended model; it is not an extra security feature that ordinary OTP satisfies.

A physically composable secrecy criterion for the **generated** private outputs would instead protect M T_A from Eve's final side information including the entire public transcript, while permitting correlations involving consumed J or S_B. For example, a relevant marginal condition is `omega_{M T_A K L E} close to pi_{M T_A} tensor sigma_{K L E}`. This statement alone is not a proof that the source's converse continues to hold: equation (14) protects the larger Y=M J S_B T_A and is used subsequently. Removing consumed registers from the criterion requires a genuinely corrected converse or another proved coding theorem. It must not be described as a verbatim application of the printed proof.

The source's intended resource conversions are therefore unambiguous, while its explicit catalytic security condition is too strong. The exact literal target cannot be proved as written. A follow-on claiming the standard region may be possible under a rigorously repaired, explicitly stated convention, but this audit does not silently weaken the requested security model or certify such a repair.

## What was actually checked

Directly inspected the primary PDF's resource definitions, Theorem 1 inequalities, Section 4 unit-resource cone, Section 5 state (12), decoder inputs, final criterion (13), and the criterion immediately before (14). The converse above is an independent proof using rank-one vacuum support, contractivity of trace distance and a classical success event. It does not rely on any upstream entropy inequality. No external individuals were contacted and no repository git operations were performed.

Mathematical check completion estimate: 100% for this boundary audit. Publication-package completion estimate: 100% for this note, 0% toward an independently proved full repaired private coding theorem. These percentages are progress estimates, not evidence.
