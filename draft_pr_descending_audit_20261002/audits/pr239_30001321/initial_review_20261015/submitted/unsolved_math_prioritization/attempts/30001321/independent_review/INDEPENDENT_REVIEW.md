# Independent adversarial review: 30001321

## Binding disposition

**PASS_COMPLETE_SOURCE_TARGET.** The frozen candidate proves the positive one-transverse-dimensional analogue of the displayed theorem in Berger's OWR 38/2009 contribution. Consequently the negative Conjecture 1 printed immediately after it is false for the stated iid, elliptic, nearest-neighbor, space-time model. This verdict applies to the exact fixed-law, deterministic-partition quantifiers in the candidate. It does not certify novelty, priority, a result for static environments, or estimates uniform as the environment law approaches a deterministic-arrow law.

Reviewed candidate:

- `PROOF.md`: SHA-256 `036e5a1585fb4e15f888337a5433482f86db8990232fe3a42ea199eb057713f7`
- `FROZEN_MANIFEST.json`: SHA-256 `fef68ea7c25e9be16d277fdf9bbbcc121a9b9cd8660a1e499aac63266ec2ac99`
- Complete dependencies `TURN_1.md` and `TURN_2.md`, with hashes bound in that manifest

All 24 bound author files and four primary PDFs match their recorded hashes. All three author receipts replay byte-for-byte. No mandatory mathematical or source-scope correction was found. The author used three substantive turns; this is a complete candidate rather than a final unresolved disposition.

The reviewer did not supply an ingredient of this proof before its freeze. The review checker was written independently and imports no author checker. Finite computations supplement the analytic audit below; they are not the justification of the asymptotic theorem.

## 1. Exact theorem and source

For a fixed law with `0<p<1` almost surely, iid over space-time sites, let `mu_N` be the quenched endpoint distribution starting at zero and `alpha_N=E mu_N`. For every deterministic positive integer sequence `M_N` tending to infinity, every deterministic alignment of consecutive `M_N`-site intervals, every fixed epsilon>0 and every K>0, the probability of coarse endpoint L1 discrepancy exceeding epsilon is `O(N^(-K))`. The threshold in N may depend on the chosen diverging sequence. The estimates are uniform in the deterministic alignment. The extension to consecutive real half-open intervals of a common real length tending to infinity also passes.

I read the original report and visually inspected printed p.2151. It expressly defines resampling the environment after every step, states iid nearest-neighbor ellipticity, and quantifies over every diverging box scale. Its negative d=1 conjecture follows the displayed probability assertion. The source does not impose an explicit uniform ellipticity constant. The candidate covers its merely elliptic reading and therefore also its uniformly elliptic subcase. The source's notation Z in a d-dimensional sentence is immaterial at d=1. The usual deterministic reading of the specified partitions is retained; no random environment-adapted partition theorem is asserted.

A deterministic elliptic law has zero discrepancy, but the proof does not use that observation to evade a universal negative conjecture: it proves the estimate for every admissible fixed law, including nondegenerate laws. A pure random-arrow law has delta=E[p(1-p)]=0, falls outside ellipticity, and invalidates a necessary return-probability estimate. This boundary is not silently included.

## 2. Replica chain and conditional occupation control

Set q=E p, a=q(1-q), delta=E[p(1-p)]. Then `0<delta<=a<=1/4`. Two independent quenched replicas, averaged over the common fresh environment, have half-difference transitions a to either neighbor off zero and delta to either neighbor at zero. At a coincident site the four pair probabilities are `q-delta`, `1-q-delta`, delta, delta; at different sites they are products of q and 1-q. This verifies the chain for an arbitrary same-parity starting pair, not only two walks initially at zero.

The first-return calculation gives

`G(z)^(-1)=(1-delta/a)(1-z)+(delta/a)sqrt((1-z)(1-(1-4a)z))`.

The denominator bound is valid because both displayed terms are nonnegative on [0,1). Reversible weights are pi(0)=a/delta and pi(d)=1 elsewhere. All holding probabilities are at least one half, so P and 2P-I are self-adjoint Markov contractions and the spectrum of P is nonnegative. The return spectral measure is positive, hence g_n is decreasing. Combining this monotonicity with the generating-function bound at z=n/(n+1) gives the required pointwise `g_n<=C/sqrt(n+1)`. An averaged generating-function estimate alone would not suffice; the spectral monotonicity closes that point.

The backward profile u_n(d)=P_d(D_n=0) is radially decreasing. Its difference recurrence has coefficient `1-2delta-a>=1-3a>=1/4` at the exceptional origin and the usual nonnegative coefficients elsewhere. This verifies the maximum at zero rather than assuming translation invariance of the sticky chain.

Given the old environment F_s, the replica starting distribution is exactly `mu_s tensor mu_s`. Fresh time layers are independent of F_s, so

`E[I_(s+t)|F_s]=sum_(x,y) mu_s(x)mu_s(y)u_t((x-y)/2)<=g_t`.

All old support points have the same parity. For moments of an occupation sum, the proof orders the time indices and conditions at the penultimate index. Every earlier product, including repeated factors at that index, is measurable there. The conditional sum over the final index is at most A_L=sum_(j<L)g_j. Iteration bounds the ordered sum by A_L^k; expansion costs at most k!. Equal indices are correctly included because I_s<=1. Thus the factorial moment bound is valid without temporal independence of I_s. Selecting a fixed sufficiently large moment order for each desired K gives the stated superpolynomial bad-event estimates.

## 3. Turn 1: coarse expectation, with parity

The layer-exposure martingale is exact. Conditional on F_s, the environmental variables within the next layer are independent and centered after subtracting q. Its quadratic variation is the sum of the squared semigroup gradients weighted by `sigma^2 mu_s(x)^2`.

The binomial kernel estimates used in the proof can also be derived directly by Fourier inversion. For the binomial characteristic function, squared modulus is `1-4a sin^2(theta/2)`. Its modulus is bounded by `exp(-c_q t theta^2)` on [-pi,pi]. Integrating either this bound or this bound times `|exp(i theta)-1|` gives respectively `C/sqrt(t+1)` and `C/(t+1)` for the point mass and adjacent parity-lattice difference. Unimodality gives total variation of the adjacent difference equal to twice the peak mass.

For one interval, summing that difference telescopes to two endpoints; alternatively it is bounded by the number of contributing points times the peak gradient. Across disjoint partition intervals, the sum of absolute gradients is bounded by the full kernel variation. These facts give the claimed sum of squared gradients and then the convolution estimate for the sum of interval variances. The central-window Cauchy-Schwarz argument and annealed tail bound give the written expectation bound. First fixing R and then sending n,M to infinity proves rho(n,M)->0 even when M grows arbitrarily slowly. No rate is extracted from this qualitative limit.

## 4. Turn 2: polynomial auxiliary scale

This dependency is essential, and I checked the complete argument rather than replacing it with a quenched CLT.

The scalar Bernstein-Freedman estimate is applied to the joint event that the martingale is large and its predictable quadratic variation is small. The exponential supermartingale has expectation at most one; Markov's inequality on that joint event is valid. There is no illicit conditioning on a future good event.

For the final averaged segment of length ell, arbitrary bounded terminal tests have gradient at most C/sqrt(N-s). The deterministic dyadic time blocks have length at most h_j and reciprocal variance weight at most 1/h_j. The occupation moment estimates provide one good event controlling every test simultaneously. The bad-event probability is charged only once, outside the union over sign tests.

Writing gamma=1/4+d, the chosen parameters are beta=1/4+d/2 and eta=d/4. The exact margins are

- `beta-eta-(1/2-gamma)=5d/4>0`, so the concentration exponent dominates the sign-test entropy
- `2beta-1/2-eta=3d/4>0`, so the boundary-strip mass concentrates
- `gamma-beta=d/2>0`, so the smoothing strip is small compared with the cells

The tail window is deterministic. Its annealed probability is `exp(-c log^2 N)`, and Markov's inequality converts the environmental tail mass to the same superpolynomial order for any fixed positive threshold.

For the actual last segment, the centered displacement bound must be combined with the old mass near shifted cell boundaries. The periodic Lipschitz majorant has support in O(r) residue classes. On the parity lattice, a residue modulo M is bounded by `2/M+2*peak`, which is sufficient for the displayed bound. This handles both even and odd M. The Lipschitz property is preserved by the averaged semigroup, so the common occupation event controls its quadratic variation. The two endpoint-cell couplings then compare the true law with the averaged-last-segment law. Thus the auxiliary theorem indeed has a superpolynomial tail at every fixed gamma>1/4. It is not itself asserted for a subpolynomial target scale.

## 5. Old-law soft interval estimate

For ell=N^(3/4) and m=N-ell, the prescribed intervals have size O(N^(3/8)log N). Their tapered majorants have expectation `O(N^(-1/8)log N)`, below the threshold `N^(-1/32)`. Their predictable variance on one common occupation event is `O(N^(-7/32))`, and their increments are `O(N^(-3/8))`. At deviation of order N^(-1/32), the variance contribution gives the exponent N^(5/32); the increment contribution gives a still larger exponent. Union over O(N) prescribed intervals preserves superpolynomial decay. No environment-dependent interval is used here.

The proof requires a small incoming mass per macroscopic strip, not a high-moment estimate of the instantaneous overlap I_m. The latter would be a stronger and unsupported shortcut, which the candidate avoids.

## 6. Fresh-kernel coupling and conditional mean

For a fixed environment, the two paths use independent coins until meeting and common coins afterward. Each marginal is the correct quenched chain. Same-parity nearest-neighbor paths cannot cross without meeting. Before meeting, their current sites are distinct, and the environment of that new time layer has not yet been exposed. Only at this averaging step are the environmental variables independent. The annealed gap is therefore the symmetric lazy walk, regardless of q's drift.

Reflection at the first hit of zero also works for holding steps. The survival mass starting at d is exactly `sum_(j=1-d)^d p_ell(j)`, bounded by 2d times the maximal lazy-walk mass. The coupling inequality then gives the required averaged quenched-kernel L1 estimate. Opposite parity would invalidate this coupling conclusion; the candidate explicitly excludes it and never needs it.

Within each H-cell the replacement law has the same cell mass as the actual old law and the conditional distribution of alpha_m. All possible old starting sites share parity; both laws are supported where alpha_m is positive. An independent coupling within the cell is enough: its distance is at most H. Integrating the kernel coupling over it gives the first error `CH/sqrt(ell)`. The replacement-versus-alpha L1 identity is exact, and Markov kernels contract it.

The remaining alpha_m mixture is compared with its annealed law by convexity and the uniform-in-alignment Turn-1 expectation bound. Translation of each starting point only changes the deterministic target alignment. This proves the conditional mean estimate for every fixed old environment. With H=N^(5/16), the coupling error is N^(-1/16), while Turn 2 applies at gamma=5/16. The slow target M_N occurs only in rho(ell,M_N), not in a concentration exponent.

## 7. Moving-strip dependence and concentration

The killed kernel uses a deterministic tube centered at the individual starting point plus vt. At each time the transition variable is read at the current site before a step; that site is in the tube whenever the path is alive. A step that exits the tube is killed without consulting any transition variable at its destination. Consequently the entire killed row from x is a function only of the environmental variables inside its specified tube.

The strips partition space-time by the deterministic coordinate y-vt. Their input vectors are disjoint, mutually independent, finite after restriction to reachable sites, and independent of F_m. Irrational drift does not affect any of these facts. Changing one input can affect a row only for starting points in its fixed enlarged influence interval J_k. Overlapping cones do not need to be independent.

Every starting point is counted by at most six influence intervals. Thus `sum w_k<=6` and `sum w_k^2<=6 max w_k`. Two subprobability row outputs have L1 distance at most two, so changing one strip moves the mixture by at most 2w_k. The reverse triangle inequality gives the same oscillation for the nonlinear norm F-dagger. Conditional bounded differences therefore yields `exp(-c t^2/max w_k)`. The previously proved old-law bound makes this `exp(-c_t N^(1/32))` off a superpolynomial exceptional event. Conditioning on F_m here is legitimate: the future product distribution is still unchanged, while its influence weights become deterministic.

The lost mass is controlled by a maximal, not merely endpoint, annealed bound. For a walk starting anywhere, the centered annealed increments are independent bounded mean-zero variables. The exponential maximal inequality gives `d_N<=C exp(-c R^2/ell)=C exp(-c log^2 N)`. This estimate holds for every starting point and thus every old mixture. The killed kernel is pointwise dominated by the unrestricted kernel; their L1 distance is exactly the lost mass. Markov's inequality at a fixed loss threshold is therefore sufficient, and retains superpolynomial order. No quenched maximal inequality is assumed.

## 8. Completion, quantifiers and boundary tests

For fixed epsilon, the conditional mean becomes at most epsilon/4 once the qualitative rho term is small and the auxiliary coarse discrepancy is small. On the old-mass good event, a large actual discrepancy with small lost mass forces a fixed positive upper deviation of the killed norm. Combining bounded differences, the two old-environment bad events, and the lost-mass estimate proves the stated bound for every K.

The argument is acyclic: Turn 1 establishes expectation convergence; Turn 2 proves only a fixed polynomial auxiliary scale; the final segment converts these two distinct facts into all diverging target scales. It never selects a vanishing gamma or presumes a polynomial lower growth of M_N. Constants may depend on the fixed law, epsilon and K; the eventual threshold may depend on the sequence. The real-length extension changes only the interval site count in the expectation input, and leaves that qualitative convergence valid.

Nonuniform ellipticity creates no hidden inverse moments: all input constants depend on fixed q and delta, which are strictly positive in the required places. Biased drift, nearest-neighbor parity, deterministic environments, very slowly diverging scales and cells larger than the diffusive window are all covered. Static RWRE, degenerate delta=0 laws and environment-selected partitions are outside this verdict.

## 9. Reproducibility and limits

The three author scripts pass with 486, 50,324 and 17,148 exact controls, and their output bytes agree with the frozen receipts. The independently authored `independent_check.py` passes **31,888 exact assertions**, including a different polynomial resolvent check, arbitrary-old-law replica propagation, three-valued environment conditional moments with repeated time indices, direct coalescing-pair propagation, path-sum killed kernels, moving strips at nonzero rational drifts, real partition lengths, parity residue bounds and exact exponent margins.

The analytic arguments above establish the theorem; finite tests only guard against algebraic, indexing and dependency mistakes. Relevant replica, quenched-mean, exposure and coupling methods are classical and credited. The checked primary sources do not certify novelty or the absence of a later equivalent result. Publication remains under the parent's separate authorization gate, with the original conjecture's negative direction and the candidate's affirmative direction stated explicitly.
