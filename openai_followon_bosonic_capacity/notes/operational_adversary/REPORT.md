# Independent operational adversarial audit

Timestamp: 2026-10-07T04:17:38.932312+00:00
Scope: exact forward net-resource conventions; eta in [1/2,1]; finite mean energy; arbitrary permitted block entanglement. This is a conditional reduction audit, not certification of EPnI or an unconditional capacity theorem.

## Strongest verified finding

Assuming the finite-energy multimode vacuum entropy inequality for every n and t in [0,1], the entropy portion of both WHG converses reduces rigorously to the displayed one-parameter regions, without product or Gaussian restrictions on input states. The basic signed unit-resource cones agree with all zero-energy and endpoint tests. An operational defect in the private catalytic converse must be repaired explicitly if the full signed region is claimed under conventional consumption of secret key: the printed secrecy criterion includes consumed key in the secrets required to remain jointly hidden. The one-time pad violates that criterion. The necessary repair below preserves the claimed inequalities.

Completion estimate for this audit: mathematical/operational resolution 75%; publication-package readiness 5%. Remaining audit work: full energy-controlled father-code achievability reconstruction; independently inspect full erratum text, beyond latest arXiv revisions.

## Primary statements read

1. Wilde--Hayden--Guha, PRA 86, 062306 (2012), Sections II, III.A, III.E, III.G--H: https://www.markwilde.com/publications/PhysRevA.86.062306.pdf . Eq.(1) gives the C/Q/E formula and Eq.(2), Theorem 7 gives the R/P/S formula:
   R+P <= g(eta N),
   P+S <= g(eta lambda N)-g((1-eta)lambda N),
   R+P+S <= g(eta N)-g((1-eta)lambda N).
   All logarithms for these rates are base two. A stray natural-log notation in Proposition 1 is not compatible with their rates; use one convention consistently.
2. Wilde--Hsieh, Quantum Information Processing 11, 1431--1463 (2012), https://www.markwilde.com/publications/QINP-quantum-dynamic.pdf ; also latest arXiv:1004.0458v3 (25 June 2012). Section 3 fixes finite gross generated and consumed resource rates: dimensions 2^(n barC), 2^(n tildeC), etc. The definition is closure of achievable signed rates, and Theorem 1 is closure of union of regularized one-state regions. Section 6 proves all three inequalities with finite resource-reference registers, data processing, and continuity only on finite generated-resource systems. Section 6.1 spectral refinement adds a classical label, improving all three information quantities while leaving the average physical channel input unchanged.
3. Wilde--Hsieh, QIP 11, 1465--1501 (2012), https://markwilde.com/publications/10.1007_s11128-011-0317-z.pdf ; latest arXiv:1005.3818v3 (25 June 2012). Theorem 1 is the full signed R/P/S region. Section 5 is the catalytic converse. Lemma 6 refines inputs to pure states for a degradable channel. Eve receives channel environment and designated publicly discarded registers. Forward noiseless public/private channels are supplied/charged as side resources.
4. The joint erratum DOI is 10.1007/s11128-012-0451-2, published online 7 August 2012. Primary LSU metadata located at https://repository.lsu.edu/physics_astronomy_pubs/5730/ ; its PDF endpoint returned 403. Latest primary arXiv versions explicitly replace Theorem 2's convex-optimization claim by single-channel-use optimization. Neither claims arbitrary state-space optimization convex. The full erratum PDF was not yet obtained, so no claim of full-text review is made.

## Operational model restrictions needed in the theorem

- The C,Q,E and R,P,S coordinates are signed net rates. A point is generated-minus-consumed resource rates; C,Q,R,P are not restricted to nonnegative octants. The corresponding side channels are forward Alice-to-Bob, finite-dimensional noiseless resources. Preshared ebits and secret key are ideal standard resources. No free backward/public feedback is supplied.
- The only physical energy charged is the bosonic channel input. Abstract side-resource channels and local registers have no bosonic photon cost in the cited resource model. Claiming a total optical energy budget including side channels would be a different theorem.
- Use a fixed finite tuple of gross resource rates as in the cited code definition, or otherwise prove a reduction to it. Net rates alone do not make original continuity error terms o(n) when gross dimensions are allowed to grow superexponentially with n. This audit does not assert a counterexample for superlinear ideal catalysts; it identifies that extension as unsupported by the cited proof.
- Channel uses are block coded with arbitrary entanglement across uses. There is one encoder before the noisy block, forward auxiliary transmissions, and one decoder. Uncharged adaptive feedback and two-way-assisted capacities are outside scope.
- Input energy is averaged over the prescribed uniform classical messages, maximally mixed quantum source and supplied ideal resources. A conditional component need not satisfy energy <=nN, but has finite energy almost surely and average energy <=nN. This is distinct from an every-codeword or high-probability photon-number occupation constraint.
- Reliability is the cited joint trace-norm/entanglement fidelity condition, with a finite-dimensional reference for each finite code. Strong secrecy and security for arbitrary message priors must not be conflated. Uniform-message secrecy alone is not a proof of semantic security.

## Explicit source defect and repaired private converse

On printed p.1475 (arXiv v3 p.8), Section 5 requires
||omega^(M K E^n T_A L J S_B) - pi^(M T_A J S_B) tensor sigma^(K L E^n)||_1 <= eps,
with pi described as maximally mixed. It then asserts I(M J S_B T_A; E^n K L)<=eps. Both issues are real:

1. Trace norm eps gives a dimension-dependent information bound, not literally eps. At fixed gross finite resource rates, Alicki--Fannes/Winter continuity on the finite secret register gives O(eps n)+O(h_2(eps))=o(n), even with infinite-dimensional Eve. This is sufficient for a weak capacity converse. Strong secrecy achievability needs a sufficiently fast decaying error, which the finite alphabet privacy-amplification coding proof must supply separately.
2. Requiring consumed key S_B jointly hidden with generated message M excludes the one-time pad. For independent uniform n-bit M and K=S_B and public L=M xor K, one has I(M;L)=0 but I(MK;L)=n. The protocol consumes key; no secrecy of that consumed key jointly with the generated message is required afterward. Likewise J may be a copy of M sent through a charged private side channel, so private registers need not be mutually independent uniform registers. The paper's own unit cone contains the one-time pad, so its literal displayed security criterion is stronger than its operational resource accounting.

A repair for the standard consumption model is direct. Write W=(M,T_A), V=(J,S_B), X=(K,L), and Y=(W,V). Require generated secrets W to be uniform and jointly independent of Eve and the public transcript, up to the stated error. Then I(W;E^n X)=o(n); consumed V need not stay private jointly with W. Reliability and data processing give, suppressing o(n),

n(barP+barS) <= I(W;B^n V|X) - I(W;E^n|X).

The exact chain-rule identity is
I(W;BV|X)-I(W;E|X)
= I(WV;B|X)-I(WV;E|X)
  +I(W;V|X)+I(V;E|WX)-I(B;V|X).

Since V is classical,
I(W;V|X)+I(V;E|WX)=I(V;WE|X)<=H(V|X)<=log|V|.
Consequently,
n(P+S)<=I(Y;B^n|X)-I(Y;E^n|X)+o(n),
after subtracting tildeP+tildeS. There is only one side-resource cost, not two.

For the third inequality, reliability gives
n(barR+barP+barS)<=I(KW;B^n V L)-I(W;E^n|KL)+o(n).
Its chain-rule expansion is
I(XY;B)-I(Y;E|X)+I(VL;KW)-I(VL;B)+I(V;E|WX).
The last positive correction satisfies
I(VL;KW)+I(V;E|WKL)
= I(L;KW)+I(V;K|L)+I(V;WE|KL)
<= H(L)+H(V|L)
<= log|L|+log|V|.
Subtract all consumed rates to obtain the original third private inequality. The first inequality uses no secrecy and is unchanged. This repair requires neither joint secrecy of consumed key nor a finite-dimensional Eve system.

## Conditional entropy reduction, valid for arbitrary entangled block inputs

Let g use base two, F_t(s)=g(t g^(-1)(s)), with F_0=0. F_t is continuous and increasing. It is convex for 0<=t<=1, concave for t>=1. A checkable calculus proof uses x=g^(-1)(s) and
sign F_t''(s) = sign[(t x+1)ln(1+1/(t x))-(x+1)ln(1+1/x)].
The function h(x)=(x+1)ln(1+1/x) strictly decreases because h'(x)=ln(1+1/x)-1/x<0. Limits at s=0 give the boundary cases. Base conversion is a positive rescaling.

For any n-mode average-energy ensemble {p_x,rho_x}, define b=(1/n)sum_x p_x S(L_eta^tensor n(rho_x)). Maximum entropy and subadditivity give 0<=b<=g(eta N), so choose lambda by b=g(eta lambda N). Conditional component energies are finite almost surely, because their nonnegative average is finite; all needed average entropies are finite by the Gibbs entropy bound and concavity.

Assumed vacuum entropy inequality and Jensen give
b>=sum_x p_x F_eta(S(rho_x)/n)>=F_eta(sum_x p_x S(rho_x)/n),
so sum_x p_x S(rho_x)<=n g(lambda N).
For eta>=1/2, Eve is L_kappa(B), kappa=(1-eta)/eta in [0,1]. A second application and Jensen give
sum_x p_x S(E rho_x)>=n F_kappa(b)=n g((1-eta)lambda N).
The averaged Bob output satisfies S(B rho_average)<=n g(eta N). Inserting these three bounds and the definition of b gives the exact quantum inequalities for each regularization block. Countable spectral refinements preserve average energy, and Jensen applies by finite integrability; no Gaussian/product premise occurs.

For the private region, refine each mixed rho_xy spectrally to pure rho_xyz. Average rho_x and average input remain unchanged. The first private information quantity increases by data processing. The second and third increase because degradable coherent information of each rho_xy is nonnegative (I(Z;B|XY)>=I(Z;E|XY) for a pure refinement). Therefore pure refinement dominates all three inequalities individually, not merely a scalarized objective. Its first quantity is S(B rho_average)-sum_xyz p_xyz S(B psi_xyz)<=n g(eta N). The same b and Eve lower bound then give the two remaining displayed private inequalities.

## Closures and convexity

For fixed finite N and eta>=1/2, let u=g(eta lambda N) in the compact interval [0,g(eta N)]. Quantum right-hand sides are
A(u)=g(eta N)+F_(1/eta)(u)-F_kappa(u),
B(u)=u-F_kappa(u),
D(u)=g(eta N)-F_kappa(u).
They are concave in u. The feasible set in (C,Q,E,u) is closed and convex, and its projection onto rates is convex and closed (u ranges over a compact interval). The same argument works for private rates, with constant first face, B(u),D(u). Thus the displayed one-parameter union itself is already closed and convex; the operational definition can still state its closure. No additional unverified convex-optimization claim about arbitrary quantum-state search is used. Equal-energy time sharing is included.

## Endpoint tests

- N=0: input is vacuum exactly. Both formulas reduce to their unit-resource cones. The C/Q/E cone generators are teleportation (-2,1,-1), superdense coding (2,-1,-1), entanglement distribution (0,-1,1). Its inverse inequalities are C+2Q<=0, Q+E<=0, C+Q+E<=0. The R/P/S cone generators are secret-key distribution (0,-1,1), one-time pad (-1,1,-1), private-to-public (1,-1,0). Its inequalities are R+P<=0, P+S<=0, R+P+S<=0. These exact signed cones are a useful check that setting communication coordinates nonnegative silently changes scope.
- lambda=0: classical/public-only ensemble; conditional inputs coherent/pure; Eve conditional entropy zero. Quantum face C+2Q<=g(eta N), Q+E<=0, C+Q+E<=g(eta N); private analog follows.
- lambda=1: all modulation photons allocated to quantum/private conditional layer. This is a valid limit even when a continuous Gaussian modulation alphabet collapses to a point.
- eta=1/2: Bob and Eve channel states agree up to phase; Q+E<=0 and P+S<=0. The degrading map is identity and no conjecture is needed for this equality. Remaining faces still trade classical communication against assistance.
- eta=1: Eve is vacuum, F_0=0; lambda=1 dominates every lambda. Quantum region C+2Q<=2g(N), Q+E<=g(N), C+Q+E<=g(N). Private region R+P<=g(N), P+S<=g(N), R+P+S<=g(N).

## Infinite-dimensional achievability: concrete needed details

WHG p.062306-5 sketches Fock truncation, finite alphabet and entropy convergence. That sketch alone does not establish a theorem with an exact energy constraint:

- Use a vacuum-replacement cutoff T_K(rho)=P_K rho P_K +Tr[(I-P_K)rho]|0><0|. Unlike normalized postselection with unchanged labels, it is a CPTP map and never increases mean photon energy. Normalize purified inputs after obtaining T_K(rho_x), not by assuming the original reference remains finite-dimensional.
- First use a strict budget N_0<N. Truncate the displacement Gaussian to bounded radius, approximate it by a finite alphabet, and then cut off Fock space. Bounded displacement radius gives uniform finite energy for all conditional states; energy-constrained entropy continuity gives convergence of all four needed averaged entropies. Include energy as a functional if using Caratheodory to reduce the alphabet; preserving only four entropy functionals does not automatically preserve cost.
- For coherent private inputs, T_K can produce mixed states; for the private pure ensemble use normalized P_K|alpha>, whose energy is <=|alpha|^2 by truncating its photon-number distribution. Alternatively refine T_K outputs spectrally and use degradability/pure-refinement domination.
- The selected finite-dimensional father/publicly-enhanced-private-father codes must meet average channel-input cost <=mN, rather than merely inherit the chosen ensemble's expected cost. A reconstruction must show its code-input expectation/typicality bound or cite an input-cost version with exact hypotheses. One can use N_0<N and bounded number operator to absorb an o(m) cost error, but that error must actually be proved for the constructed codes.
- The pure-loss channel maps a finite per-mode Fock cutoff to finite Bob and Eve cutoffs, so ordinary finite-dimensional coding and security proofs can apply once the input ensemble and cost control are fixed. Let N_0 increase to N after coding; at N=0 use the unit cones directly.

This audit does not certify the finite-dimensional father-code cost step solely from the WHG truncation paragraph. It is the remaining operational proof obligation, distinct from the upstream entropy premise.
