# Exact physical vacuum specialization of the supplied EPnI statement

Status: elementary mathematical deduction **conditional on the soundness of the upstream EPnI theorem**. This project has verified the upstream statement's source semantics but has not reproduced its Lean build.

Let `n≥1` be finite, let `ρ` be any positive trace-class normalized state on the full n-mode Fock space, and assume `Tr(ρ H_n)<∞`, where `H_n=∑_j a_j†a_j`. No Gaussianity or tensor-product structure between the n modes is assumed. Let `v_n=|0,…,0⟩⟨0,…,0|`. Then `v_n` has finite energy zero and von Neumann entropy zero. The product-port input `ρ⊗v_n` is exactly the independence hypothesis of EPnI; it does not impose separability between modes within `ρ`.

For `0≤τ≤1`, the reduced first output of the passive beamsplitter with amplitudes `sqrt(τ)` and `sqrt(1−τ)` is exactly the n-mode pure-loss channel `L_τ^{⊗n}(ρ)`, as a consequence of its standard vacuum Stinespring definition. The supplied Lean number-basis coefficient implements this same passive rotation, with an irrelevant sign on the discarded port. The required output state exists, is positive trace-one, and has finite energy; its photon expectation is `τ Tr(ρ H_n)` (the looser finite-energy bound in the formal source also suffices here).

Writing `g_nat(x)=(x+1)ln(x+1)−x ln x`, EPnI gives

\[
\tau g_{\rm nat}^{-1}(S_{\rm nat}(\rho)/n)\le
 g_{\rm nat}^{-1}(S_{\rm nat}(\mathcal L_\tau^{\otimes n}(\rho))/n).
\]

Both sides are nonnegative, so the strictly increasing inverse relation yields

\[
S_{\rm nat}(\mathcal L_\tau^{\otimes n}(\rho))/n\ge
 g_{\rm nat}(\tau g_{\rm nat}^{-1}(S_{\rm nat}(\rho)/n)).
\]

The already-direct upstream declaration `epni_entropy_closed` supplies the last inequality without reapplying `g`. It covers the endpoints: `τ=0` produces vacuum and the lower bound is zero; `τ=1` is equality.

For entropy in bits, set `S_bit=S_nat/ln 2` and `g_bit=g_nat/ln 2`. Then `g_bit^{-1}(s)=g_nat^{-1}(s ln 2)` and the identical physical inequality is

\[
S_{\rm bit}(\mathcal L_\tau^{\otimes n}(\rho))/n\ge
 g_{\rm bit}(\tau g_{\rm bit}^{-1}(S_{\rm bit}(\rho)/n)).
\]

This is the strong multimode vacuum minimum-output-entropy statement, at fixed input entropy, needed by the requested capacity converse. It is stronger than a single-mode or unentangled-input statement. It does not itself prove the ensemble Jensen step, the energy-constrained coding theorem/closures, or the follow-on dynamic-capacity region.

For the degradable pure-loss channel with `η∈[1/2,1]`, the vacuum inequality can also be applied to the receiver's n-mode output with transmissivity `τ=(1−η)/η`, because the complementary output is obtained by that additional pure-loss channel up to an output phase unitary. Its input is finite-energy whenever the original channel input is. This supplies the per-conditional-state receiver/environment entropy comparison. The conversion of this family of comparisons into a common ensemble parameter still requires a proved convexity/Jensen argument, not substitution of one selected state's photon parameter for the ensemble average.
