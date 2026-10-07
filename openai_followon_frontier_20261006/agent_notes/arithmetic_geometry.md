# Arithmetic and geometry frontier screen

Checkpoint: 2026-10-06 PDT. Assigned screen 100% complete; no new theorem proved. No external contact.

## Recommendation: critical-line bootstrap for RH / Dirichlet GRH

Impact 10/10; extreme risk. Exact natural target: all nontrivial zeros of all finite-order Hecke L-functions over Q(sqrt(-3)) lie on Re(s)=1/2. The source's quadratic base-change argument then gives Dirichlet GRH, including classical RH. The user-facing headline can be RH, but this mechanism must retain the full Hecke family because Poisson introduces twists even when the ultimate target is zeta alone.

Inspected actual source: `/Users/alec/Desktop/math/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex`, introduction, proof overview, continuation theorem, local Euler factor proof, compensated probe construction, and concluding exponent calculations. This September 30 manuscript is the stronger 7/8 theorem. The October 5 alternate gives only 11/12 and is not the frontier.

### Why there is a new analytic lever

The source already demonstrates a two-stage improvement 11/12 -> 7/8. Its common continuation theorem (lines400+) is explicitly valid for any sigma_0 in (1/2,1): compare the SAME normalized completed cubic-theta probe J with a Mellin integral containing H_eta/L_eta. H_eta must be holomorphic and bounded away from zero; both the direct bound and off-principal-row bound must have positive power margins independent of the target character. Such estimates contradict beta_* > sigma_0, where beta_* is the supremum of real parts of zeros across the complete primitive finite-order Hecke family.

Stage one uses C_I(s)=s-2/3. Stage two introduces selected-prime local compensation, asymmetric scales, a marked inverse-polynomial second-moment recursion and a plain-polynomial fourth-moment recursion. The detector's two witnesses have the same row character and twist height. This is a concrete zero-exclusion mechanism, not merely improved zero density.

The exact second-stage compensated probe (lines6880+) is a composition, over selected prime slots, of a marked term conjugate(eta(p)) I_{eta;p}(X,Y,Zq_p) minus a rescaled term q_p^(-3/2) I_eta(X/q_p,Y/q_p,Z). This cancels a scalar local contribution, leaving the sextic-character prime factor used by the moment estimates. Higher compensation is therefore a specific possible new construction, not an appeal to "better estimates" alone.

### What is NOT established, and the first meaningful gate

The current final geometry is h=13/16, ell=1/6, l_x=17/48, l_y=23/48, and C_II(s)=s-11/16. It assumes Delta=beta_*-7/8 in (0,1/24], with kappa=3/4+2Delta<=5/6. The high power margin is (51/64)Delta and the low margin Delta. The bin-contour/extraction lemmas explicitly assume sigma_0 in [7/8,1) (lines5808+,6021+,6174+). Existing bounds cannot simply be iterated below 7/8.

FIRST GATE: extract all actual exponent, prime-slot capacity, Euler-domain, exceptional-character, principal-residue and height constraints into a checked parametric certificate; reproduce 7/8, then find and rigorously certify any strictly smaller zero-free threshold. A numerical feasible point is not enough without proving every invoked analytic estimate on its new domain.

### A concrete deeper obstruction visible in the Euler proof

The complete local identity has one domain reaching x_r>=51/100, z_r>=17/50, w_r>=-1/100, x_r+w_r>=1+epsilon. This handles reflected nonprincipal rows. Its second domain, containing the principal residue, is x_r>=7/8, z_r>=33/200, w_r>=19/20.

In the local defect calculation (lines4139+), the good-prime error is bounded by

    Q^(4-6*x_r-6*z_r+theta) + Q^(1-x_r-w_r-6*z_r), theta=max(-w_r,0).

At the actual principal residue (w,z)=(1,1/6), the first existing upper bound is Q^(3-6*x_r). Absolute summability over primes therefore requires x_r>2/3. This does not prove an intrinsic 2/3 obstruction, but it identifies a specific bound that must change before the critical line: cancel or correctly extract its leading Euler terms, or construct a different probe. Merely optimizing the final 7/8 arithmetic cannot establish RH.

NEXT GATE: construct a higher compensation / mixed-moment family that proves the necessary local holomorphy and off-principal savings below each existing obstruction. Seek either a bootstrap valid for every beta_*>1/2 or certified thresholds sigma_j decreasing to 1/2. Constants may depend on each fixed epsilon. No uniform limit estimate is needed if zero-freeness in Re(s)>1/2+epsilon is separately proved for every epsilon>0. The functional equation then finishes.

The unproved claim is precisely the new critical-line-compatible arithmetic estimates. Treat the route as blocked if a proposal merely renames these estimates as an assumption. This screen inspected the source mechanism, not every step of the 16k-line upstream proof; that dependency needs adversarial audit.

Primary external context:

- Clay official RH description: https://www.claymath.org/millennium/Riemann-Hypothesis/
- Guth–Maynard, New large value estimates for Dirichlet polynomials: https://arxiv.org/abs/2405.20552. Its published zero-density result is a possible independent large-values approach family, not an existing zero-exclusion theorem.

## Other arithmetic/geometry routes screened

1. Full BSD / first rank-two case: source002's actual introduction exposes reusable integral character division, marked residual tests, position-cut estimates and quotient-divisor removal through extra tame variables. But its calibration is rank0 modular symbols or rank1 height/Gross–Zagier, and its pair comparison needs a(E)+a(E^D)=1. Rank2 has no supplied higher-rank height calibration or exterior-power Euler-system comparison. Density-one low-rank twists do not reduce a high-rank curve; quadratic base-change ranks add. Impact9.5–10, less concrete bootstrap than qRH.

2. Hodge for all projective K3^[n] deformations: the solved local `openai_followon_k3_moduli_hodge/CURRENT_THEOREM.md` includes products of Bülles-type smooth K3 moduli spaces, explicitly excluding arbitrary deformations. Markman's https://arxiv.org/abs/2204.00516 proves rational Hodge isometries algebraic and suggests hyperholomorphic transport. It does not establish transport/generation of all Hodge classes. Algebraicity along a Hodge locus is a central missing theorem, not automatic. Impact9, valid distinct research direction but less maximal impact.

3. Hodge for all abelian varieties: the CM source constructs balanced four-factor CM tensors via theta one-forms on arithmetic ball surfaces, identifies rational CM sources through Hecke/Frobenius slope data, and contracts auxiliary CM factors. General non-CM classes have no supplied torus/embedding-line reduction. CM specialization plus lifting cycles assumes a variational Hodge statement. Markman's independent secant strategy https://arxiv.org/abs/2509.23403 is relevant, but this source does not solve its higher-dimensional deformation obstruction. Impact9.5; do not infer all-abelian Hodge from dense CM points.

4. Full Tate for abelian varieties over all finite fields is ALREADY an explicit consequence in source032 via CM-Hodge and Milne. Source001 supplies algebraic specialization in all realizations. Not a new candidate.

5. Sources033–036 already claim characteristic-zero log abundance, generalized minimal model existence, and uniform Iitaka statements. Source014 already includes all-place generic Ramanujan for split adjoint exceptional function-field groups and its stated Arthur enhancement. Those broad labels alone would duplicate the release; arbitrary number-field Langlands has no comparably specific bridge established in this screen.
