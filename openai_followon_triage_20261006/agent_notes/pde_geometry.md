# PDE, geometry and Banach triage (families 322–377)

Checkpoint: 2026-10-06 America/Los_Angeles. Triage completion estimate 90%; candidate proofs not attempted. Claims below are conditional on the supplied main theorems. Read catalogue, selected TeX introductions/proof mechanisms, Lean scope docs 362/370/374, and primary literature. No external communication.

## 1. Complete the all-dimensional Lane–Emden a priori theory (#370)

**Exact immediately defensible target.** For n>=3, p,q>1, and 1/(p+1)+1/(q+1)>(n-2)/n, every nonnegative classical solution of -Delta u=v^p, -Delta v=u^q in any proper domain Omega satisfies u(x)<=C dist(x,boundary Omega)^(-alpha), v(x)<=C dist(x,boundary Omega)^(-beta), where alpha=2(p+1)/(pq-1), beta=2(q+1)/(pq-1), and C depends only on n,p,q. Obtain corresponding gradient estimates, exterior-domain decay, nonexistence on a Dirichlet half-space, and bounded-domain Dirichlet a priori compactness. First release should package the full subcritical range with explicit theorem hypotheses; extensions to nonlinearities asymptotic to the powers and uniformly positive smooth coefficients are a useful second theorem.

**Route and remaining gap.** Apply #370 (A=B=0), strong maximum principle to nontrivial nonnegative blow-up limits, then Polacik–Quittner–Souplet (2007), Theorems 4.2 and 4.3. Those theorems explicitly assume only bounded entire Liouville nonexistence and p,q>1. This is a direct established transfer, not a speculative proof mechanism. For bounded-domain uniform Dirichlet bounds check boundary blow-up using their half-space theorem. Variable coefficients/lower-order perturbations need a compactness normalization argument. Do not claim p or q<=1, critical hyperbola, or parabolic bounds automatically.

**Impact/tractability.** High tractability; medium-high PDE impact; very high risk someone immediately observes the same corollaries. Better publication value in full perturbation/boundary/singularity package than restating one known conditional theorem. Exact universal-bound range is sharp because at/on above the hyperbola positive radial entire solutions can be rescaled on a fixed ball.

**Evidence.** Local: `preprints/The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026/build/sections/01-introduction.tex` (Theorem main and Corollary lane-emden), `lean/docs/370.md`. The paper mentions bounds as motivation but does not state the proposed full local/boundary estimate suite. Primary: https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf , Theorems 4.2–4.3 and 7.3. Its conditional estimates already exist; novelty is the newly unconditional all-dimensional scope.

## 2. Large-data global smooth electron–ion plasmas (#362)

**Exact target.** Finitely many species f_a>=0 with fixed masses m_a>0, charges e_a of either sign, compactly supported smooth initial densities, compatible C_b^infinity finite-energy Maxwell fields on R^3: unique global classical relativistic Vlasov–Maxwell solution, compact phase support on every finite interval. Start with two equal-mass species with charges +/-1, then arbitrary fixed mass/charge ratios.

**Route.** Set normalized momentum v=p/m_a, so speed is u(v)=v/sqrt(1+|v|^2) for every species, while acceleration gets constant e_a/m_a. Maxwell source terms are species sums with signed charge weights; total kinetic energy is the positive sum sum_a m_a integral sqrt(1+|v|^2) f_a. Retarded source/receiver kernel terms gain fixed species-pair charge factors. In `cancellation.tex` the exact signed-force identity is geometric: it uses |u|^2=1-q^-2 and |a|^2=1-q_X^-2, not positivity of electric charge. Thus opposite signs should multiply the complete source identity, leaving the integration-by-parts cancellation intact. Sum absolute estimates with finite charge/mass-dependent constants and close one bootstrap over the maximum momentum among all species.

**Exact unverified gap.** Reprove the signed impulse estimate (Proposition increment in setup.tex) for every source/receiver species pair, then check the angular occupation and selected-range coefficient estimates remain uniform when accelerations have different charge/mass factors. The paper's theorem and Lean comparator are strictly one-species. This is not already a formal corollary: class as medium-risk adaptation, potentially very high impact, not promised straightforward. Neutrality, noncompact momentum tails, collision terms and curved spacetime are outside this target.

**Evidence.** Local: `preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/sections/introduction.tex`, `setup.tex` (Prop signed momentum increments), `cancellation.tex` lines 1–109 (signed force identity), `lean/docs/362.md`. Primary continuation/multispecies formulation: Glassey, *The Cauchy Problem in Kinetic Theory*, chapters 5–6, https://epubs.siam.org/doi/10.1137/1.9781611971477.ch5 and https://epubs.siam.org/doi/10.1137/1.9781611971477 .

## 3. Sharp Brenier stability for nonuniform log-concave sources (#374)

**Exact target.** Compact convex K with nonempty interior; rho=r(x)dx a probability with log-concave density bounded above and below by positive constants on K; arbitrary targets in fixed compact Y. Establish ||T_mu-T_nu||_L2(rho)<=C(K,Y,r) W2(mu,nu)^(1/3). Uniform sharpness over this source class follows from its uniform-density subclass. Ideally make C depend only on elementary geometry and density bounds.

**Route.** The new paper's central finite-cell moment inequality arises by coupling the two source restrictions and dominating their midpoint pushforward by the source on the intermediate convex cell. For log-concave r, r((x+y)/2)>=sqrt(r(x)r(y)); combine this with the same triangular-map determinant inequality. Then reproduce the graph-Laplacian potential estimate and weighted coordinate-slice gradient interpolation, using density bounds. This is a concrete mechanism, not just guessing that all bounded densities behave alike.

**Gap/risks.** Must verify the midpoint domination gives exactly the needed normalized cell-mass inequality and that differentiation of weighted masses/moments is legitimate. General merely bounded non-log-concave densities are NOT supplied by the midpoint proof: a fixed density-ratio loss before taking the second variation is insufficient. Gaussian/unbounded supports also require new tail estimates. Medium tractability and moderate-high optimal-transport relevance; less compelling than major conjectures elsewhere in the corpus.

**Evidence.** `preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/introduction.tex` states only uniform convex source and describes exact midpoint mechanism; `lean/docs/374.md` has same scope. Existing 1/3 finite-target estimates have nondegeneracy-dependent constants; proposed theorem must keep target-uniformity.

## Explicitly screened out

- #337 model-ball Faber–Krahn and Saint–Venant comparisons are already Corollary model-ball-spectral of the paper. Do not relaunch.
- #335 Yamabe/simplicial-volume bound essentially appears in the proof's conformal reduction; weak novelty.
- #343 ball-packing numerical consequences/packing stability mostly look immediate and likely covered in applications; not a leading stream.
- #368 strong W1p diffeomorphic approximation does not by itself prove no Lavrentiev gap for physical elastic energies singular as determinant tends to zero. Such a claim transfers the difficulty to uncontrolled determinant/inverse energy.
- #375 general double-well potentials and #377 sharp infinity-harmonic exponent 1/3 require new analytic estimates; not characterized as easy.
- #372 uniqueness-to-logarithmic stability or arbitrary partial-data elasticity needs quantitative complex geometrical optics/Runge estimates, not automatic from qualitative uniqueness.

## Independent adversarial review of computation agent's targets

Checkpoint: 2026-10-06; triage completion estimate 100%. These are mathematical reduction checks, not proofs of source papers.

**#129 binary alphabet conversion: passes.** Encode each relation R on h points by its h^2 adjacency bits. A binary 1NFA can remember source/guessed target/block position in O(h^4) states (O(h^3) appears possible) and check the selected bit, implementing nondeterministic path propagation across complete blocks. A binary s-state 2DFA or 2NFA is simulated over relation symbols by retaining virtual position in the h^2-bit block, using O(s h^2) states. Each relation symbol permits its indexed bit to be read in the finite transition table. The exponential-in-h lower bound therefore becomes a stretched exponential in the polynomial-size binary source and remains superpolynomial. Malformed binary strings do not weaken the reduction: only valid encodings occur in the pullback; the source can explicitly reject nonmultiple block lengths. Required formal details: virtual endmarkers, stay moves, and correspondence of infinite nonaccepting computations. This does not prove L!=NL.

**#142 factoring over explicitly represented finite extensions: passes.** For squarefree f over F_q, q=p^m, compute B={b in F_q[x]/f:b^q=b}, a product of r copies of F_q, by F_q-linear algebra. For each basis element b_i of B and each F_p-basis element alpha_j of F_q, form tau_ij=Tr_Fq/Fp(alpha_j b_i). Its component values lie in F_p; its minimal polynomial can be computed by F_p-linear algebra and factored with #142. Gcds with tau_ij-c split f. The nondegenerate trace pairing guarantees that two distinct components differ on some tau_ij. All dimensions and exponent lengths are polynomial in deg(f),m,log p. Standard squarefree decomposition and inverse Frobenius address multiplicities. Require a valid explicit field presentation; constructing such a presentation is a separate target. No hidden primitive-root or integer-factorization oracle is needed.
