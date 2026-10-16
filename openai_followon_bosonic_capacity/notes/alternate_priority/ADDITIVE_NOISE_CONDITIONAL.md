# Conditional finite-energy additive-noise consequence

This is a transfer argument contingent on sharp thermal attenuation. It does not verify that premise or independently resolve a core capacity target.

Use [q,p]=i and vacuum covariance I/2. In the complex displacement convention, define N_nu by chi_out(z)=chi_in(z) exp(-nu |z|^2); it adds nu photons per mode. Vacuum attenuation A_tau has chi_out(z)=chi_in(sqrt(tau)z) exp(-(1-tau)|z|^2/2). A thermal attenuator T_{tau,B} has noise factor exp(-(1-tau)(B+1/2)|z|^2). Consequently, for each 0<tau<1,

\[
T_{\tau,\nu/(1-\tau)}=N_\nu\circ A_\tau.
\]

For fixed n and trace-class rho, A_tau^{tensor n}(rho) tends in trace norm to rho as tau tends to 1. Its beam-splitter Stinespring unitary tends strongly to identity; finite-rank trace-class approximation and contraction extend the convergence to all trace-class inputs. Composition with N_nu is trace-norm contractive, so T outputs tend to N_nu^{tensor n}(rho).

For total finite input photon energy E, all these outputs have energy tau E+n nu <= E+n nu. The n-mode photon Hamiltonian has finite Gibbs partition function at every positive inverse temperature. Energy-constrained entropy continuity ([Winter 2016](https://doi.org/10.1007/s00220-016-2609-8)) therefore gives entropy convergence. Lower semicontinuity alone has the wrong direction and is insufficient.

If the sharp thermal-attenuator inequality holds, then for every tau<1,

\[
S(T_{\tau,\nu/(1-\tau)}^{\otimes n}(\rho))/n
\ge g(\tau g^{-1}(S(\rho)/n)+\nu).
\]

Taking the limit proves

\[
S(N_\nu^{\otimes n}(\rho))/n\ge g(g^{-1}(S(\rho)/n)+\nu).
\]

Product thermal inputs attain equality. The statement covers every finite n, finite-energy rho with arbitrary internal entanglement, and nu>0; nu=0 is identity. It does not establish finite-entropy/infinite-energy inputs. All entropy units must agree.

Priority boundary: [De Palma 1805.12469v3, Conjecture 1 and Corollary 5](https://arxiv.org/html/1805.12469v3) already state this conjecture and prove it for nu>=1. One-mode and arbitrary-n product-basis-diagonal cases are known. The meaningful removed restriction, conditional on the new input, is unrestricted finite-energy multimode rho for 0<nu<1; this must be attributed as a consequence.
