# Independent analytic review — Zenodo 22089551, version 1.2.4

Completed: 2026-10-25 UTC. Review scope: mathematical claims and proofs, their published-document binding, exact imported hypotheses, and independent finite falsification controls. No prior review, historical audit verdict, sibling opinion, or released verification report was consulted before this verdict. No publication, repository, website, spreadsheet, or outreach action was taken.

**Verdict: no blocking mathematical defect found in the stated theorem.** The full proof reconstructs, including the boundary-availability lemma, finite expected return rather than merely finite-set hitting, and construction of a nonexplosive continuous-time chain. This is an independent analytic review, not formal verification or a claim that finite tests establish the theorem.

## Published objects and coverage

Title: *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*. Author: Alec Kriebel. Published version: 1.2.4, dated 22 August 2026. Record: [Zenodo 22089551](https://zenodo.org/records/22089551).

| Published object | Coverage | SHA-256 |
|---|---|---|
| `paper-v1.2.4.pdf` | All 16 pages | `1df7ec1e4596680e229c0316fad20d46b276fead4cf642ac40e47182e14cd7f4` |
| `supplementary-note-v1.2.4.pdf` | All 2 pages | `8838eefbb4233f0cbaba988544c060efd483b94f6ab69781b2f7023134733d98` |
| `bimolecular-positive-recurrence-v1.2.4.zip` | Current manuscript sources and build support used; historical opinions excluded | `1f5983ebe6251a87fa5b1657d1934e2d7d6e13b1fad7bb5e53201c1a9ceecbbb` |

Read all 1,212 lines of current `manuscript/paper_content.tex`, the complete current arXiv wrapper, supplementary-note source, bibliography, and reproducibility environment. Rebuilt both current documents from those sources using cached Tectonic with the declared source-date epoch. **The extracted text is identical on every one of the 18 published pages. The rebuilt PDFs are not byte-identical.** `source_binding.json` records both sets of hashes and the page-by-page text comparison. Rebuilt binary PDFs were removed; source, compiler logs, extracted published text and binding evidence remain in this review folder.

Coverage map: main pp. 1–3 motivation and model; p. 4 main theorem, lifted state-return lemma and stationary corollary; pp. 5–7 marked chain, exact factorial identity, entropy rewrite and examples; pp. 7–8 episode recursion and scalar envelope; pp. 8–10 logarithmic compactification, top-complex alternative and exceptional set; pp. 10–11 quantitative limitations; pp. 12–13 sampled-chain drift, finite trace return and physical-time conversion; pp. 14–16 scope, declarations and references. Both supplement pages were checked, including marking, positive-return conventions, occupation balance, nonexplosion and the boundary between computation and proof.

The package's own verification suite, interpreter matrix and release-report byte-reproducibility claims were not independently rerun in this analytic track. The controls below are separately written and import no manuscript verification code. This is an explicit coverage boundary, not a discovered defect in those package claims.

## Exact claim and assumptions

Theorem 2.1 assumes a finite species set and finite set of labelled reaction channels, positive fixed rate constants, stochastic mass action with falling factorial propensities, weak reversibility, one linkage class, and molecularity at most two for **every complex**, including targets. One linkage class plus weak reversibility means that the complex graph is strongly connected. Parallel channels are allowed. Self-channels can be removed without changing the population generator; channels with the same population displacement but different source/target complexes must remain distinct.

For every initial population, its reachable set is a closed communicating class. On each nonabsorbing class the minimal continuous-time chain is nonexplosive and positive recurrent; each absorbing singleton has its point-mass law. Corollary 2.3 gives one unique stationary probability **per reachable class**. It does not claim uniqueness across distinct classes, convergence rates, useful bounds on stationary tails or unbounded moments, product form, or the full chemical recurrence conjecture with arbitrary linkage structure or molecularity.

These are mathematical deductions within a specified stochastic model. The paper does not empirically establish well-mixed chemistry, mass-action validity, or any physical rate parameter. Finite and absorbing classes are handled before the infinite-class drift proof. Common molecularity implies finite population shells; absent species remain invariant. None of these cases requires an interior-state assumption.

## Reconstruction of the proof

### Population reachability and actual channel marks

For an enabled reaction y→y′ at x, write x=ρ+y with ρ≥0. A directed complex return path from y′ to y lifts to the population path ρ+z along the same edges: its next source is present at each step. Thus every enabled population transition has a finite return path, and accessibility is symmetric. The argument respects zero complexes, zero coordinates, lattice/parity restrictions and parallel channels. This step needs weak reversibility, but neither a single linkage class nor bimolecularity. It is combinatorial accessibility, not probabilistic positive recurrence.

Construct the embedded population chain first. The augmented chain records the target t of the actual last channel, so x≥t. Its reachable augmented state set is irreducible: a desired post-jump pair has a predecessor in the population class, and a population path to that predecessor followed by the defining channel reaches that marked pair. Its projection has the original population transition law, independent of the current mark. This prevents a hidden replacement of channel labels by net increments.

Set V(x,t)=Σᵢ log((xᵢ−tᵢ)!). It is nonnegative and has finite sublevel sets despite log(0!)=log(1!)=0. If the next channel has source s and target u, the new residual is x−s; cancellation gives the exact identity

`V(x−s+u,u)−V(x,t) = log((x)_t/(x)_s)`.

Both factorials are positive where the identity is used. Source=t therefore gives exactly zero reward, rather than a large unaccounted error from Stirling approximation. This is a useful change of state and potential, not an assumption about the chain's asymptotic distribution.

### One-step drift and rare-terminal propagation

Let κ̄_y be the sum of outgoing constants from source y, and p_x(y)=κ̄_y(x)_y/Λ(x). Every complex has positive κ̄_y after removal of self-channels in the nontrivial strongly connected graph. Direct substitution into the exact identity gives

`δ(x,t) = log p_x(t) − Σ_s p_x(s) log p_x(s) + Σ_s p_x(s) log κ̄_s − log κ̄_t`.

Thus δ≤log p_x(t)+C₀, where C₀=log|C|+log(κ̄_max/κ̄_min). The zero complex has falling factorial one and creates no singularity. The entropy estimate includes disabled sources by the standard zero-probability convention.

Fix a simple directed complex path from the current target to any chosen terminal c. The episode follows exactly its designated channels; a different channel stops it immediately. Once c is reached, one ordinary jump terminates the episode. It lasts between one and |C| jumps. During designated steps the residual remains fixed and the immediate potential change is zero.

Conditioning on the next channel gives `J_k=δ_k+q_k p_k J_(k+1)` with fixed q_k>0. A central danger would be multiplying a large negative terminal drift by a path probability tending to zero. The manuscript handles it through the exact scalar optimization

`F_q(M)=sup_(0<p≤1)[log p+C₀+qpM]`.

Its two branches are C₀+qM for M≥−1/q and C₀−1−log(−qM) otherwise. F_q is increasing and tends to −∞ when M does. Backward composition along the finite path therefore sends terminal drift tending to −∞ to initial episode drift tending to −∞, even when intermediate source probabilities decay on different scales. No uniform lower bound on the full path probability is assumed.

### The bimolecular boundary step, independently reconstructed

From a divergent sequence with a fixed target, extract a subsequence in which each residual coordinate is either a fixed integer or tends to infinity. Let I contain **all** divergent coordinates, including those with zero normalized logarithmic weight. Normalize their logarithms by their sum to obtain w≥0, Σw=1. For any fixed enabled complex y, `log((ρ+c)_y)=R w·y+o(R)`. Bounded-coordinate factorials contribute only bounded terms; slow divergence is correctly kept in the availability set I.

I checked the key availability lemma by a contrapositive mechanism. Suppose there is no strict-weight pair s,c with s enabled over ρ+c. If all complexes have equal w-weight, w·x is a reaction-wise invariant diverging on the sequence, impossible within one class. Otherwise a top complex cannot contain two I-particles: such a binary source has no bounded companion and would be enabled above every lower complex. A unary top complex is excluded for the same reason.

Consequently every top complex must be Sᵢ+D, with i divergent and D bounded. All represented divergent indices J have wᵢ equal to the positive maximal weight. A complex containing a J-particle is top; no complex can contain two J-particles. If a lower complex contained any top companion D, it would enable the corresponding top source, again contradicting the supposition. Therefore all complexes have zero value under

`ℓ(x)=Σ_(i∈J)x_i − Σ_(D in companion set)x_D`.

This is a reaction-wise signed invariant. Its positive coordinates diverge, while its negative coordinates are fixed along the extracted sequence, so it diverges on a single communicating class—also impossible. This exhausts binary complexes. The signed coefficients cannot cancel divergent positive coordinates because companions are outside I; slow divergent coordinates are not mistakenly treated as bounded companions.

Hence a fixed enabled s,c with w·s>w·c exists. Their factorial ratio tends to infinity, so p_(ρ+c)(c)→0. The entropy estimate and episode envelope supply an episode drift tending to −∞. The molecularity bound is used essentially here; this proof does not silently establish the same availability alternative for higher-order complexes.

### From subsequences to finite expected positive return

For each terminal c, let D_c(z) be its exact expected episode drift. Define K by min_c D_c(z)>−1. If K were infinite, finite sublevel sets would supply a sequence with V→∞. The preceding compactification yields either an impossible invariant or one fixed terminal with D_c→−∞, contradicting membership in K. K is also nonempty: at a global minimum of V, every episode endpoint has at least the initial potential. The global minimum exists by finite sublevel sets on the nonempty state space.

Outside K, select a minimizing terminal deterministically with a fixed tie-breaking rule before the episode begins. This is an adapted choice on a countable state space. The drift is at most −1. Each episode has at most |C| jumps and a coordinate can increase by at most two per jump. Thus for each deterministic number of episodes the potential is integrable. The nonnegative stopped supermartingale gives Eσ_K≤V(z) by bounded-time expectation followed by monotone convergence. No unjustified optional stopping at an unbounded time occurs. Hitting K midway through an episode can only make the original-chain hitting time smaller than the endpoint bound.

Finite expected hitting is not by itself positive recurrence; the paper supplies the necessary further step. From each k∈K take one ordinary jump, then use the finite expected hitting bound from its finitely many successors. This proves finite expected **positive** return to K. Its finite trace chain is irreducible. A finite-block positive-probability path to a selected k* gives finite expected trace return count M. If B is the maximum expected trace-excursion length over K, conditioning at each excursion start and Tonelli give expected original return count ≤B·EM. This does not presume independence between the random number of excursions and their lengths. Projecting away the mark gives finite positive return to its population coordinate.

### Physical time and stationary probability

The embedded chain is established as positive recurrent before nonexplosion is asserted. It visits a fixed state infinitely often. In the standard independent holding-time construction, the holding times on those visits are independent exponentials at one finite positive rate; their sum diverges almost surely. Therefore physical jump times cannot accumulate. Quadratically growing rates elsewhere cause no circularity in this argument.

On a nonabsorbing class every state enables a genuine channel. A positive falling factorial is an integer at least one, giving Λ(x)≥κ_min>0. Conditional expectation along a finite-mean embedded return cycle then bounds expected physical return by expected jump return divided by κ_min. It is the rate **lower** bound that controls finite physical return; recurrence of a fixed embedded state controls nonexplosion. A global upper bound on Λ is neither stated nor needed.

The normalized expected occupation of a complete return cycle is finite and sums to one. The supplement's arrival/departure balance is valid because the cycle has finite expected jump count. An independent check is to take the embedded invariant probability α and set π(x) proportional to α(x)/Λ(x): its normalizer is positive and at most 1/κ_min. Combined with the already proved nonexplosion and irreducibility, this gives the same unique stationary law. Periodicity of the discrete chain is not an obstacle. Absorbing singletons use their point masses separately.

## Imported results and novelty boundary

- [Anderson–Cappelletti–Kim, author-hosted paper](https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf): Theorem 4.1 has the additional pure-species complex condition `{S,2S}∩C≠∅` for every species. Its §6.1 explains the relevant boundary-source availability issue. The current paper's comparison and removal of that assumption are correctly scoped. Their Theorem 3.1 and Lemma 3.2 already contain the embedded-chain conversion and mass-action rate-lower-bound ingredients; these are not new general Markov-chain results. Example 4.1 matches the example analyzed here.
- [Norris, *Markov Chains*, authored book text](https://cape.fcfm.buap.mx/jdzf/cursos/procesos/libros/norris.pdf): checked Theorem 2.7.1 on recurrent jump chains and nonexplosion, Theorems 3.5.1–3.5.3 on embedded invariant measures and positive recurrence, and Theorem 3.5.5's stationary characterization. The irreducibility and nonexplosion hypotheses fit the proof's order. The warning that a finite generator-invariant measure alone need not exclude explosion is relevant; the manuscript does not make that invalid inference.
- [Paulevé–Craciun–Koeppl, primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3835780/): Lemmas 4.5–4.6 concern reversibility of accessibility in a discrete reaction network. The manuscript properly distinguishes this earlier combinatorial terminology from Markov-chain positive recurrence.
- [Xu, current primary preprint](https://arxiv.org/html/2409.05340v2): checked the scope of the broader second-order nonexplosion result and the discussion around Theorem 4.13. Nonexplosion alone does not settle stationary existence. It is contextual support, not a missing premise needed for this paper's self-contained physical-time argument.
- [ConStRAINeD project publication page](https://constrained.polito.it/publications/): the announced two-species result is explicitly listed as “in preparation.” Its stated two-dimensional scope is complementary to arbitrary species with one linkage class and binary complexes. No unpublished proof was treated as an established dependency.

The sampled-chain Foster argument is proved in the manuscript rather than delegated to a generic Meyn–Tweedie theorem. Likewise, I reconstructed the return-cycle occupation argument and checked an equivalent route in Norris; I did not read the entire Asmussen volume or infer its hypotheses solely from the citation. This review does not establish exhaustive bibliographic priority. The credible added mathematical content is the target-shift/episode mechanism combined with the binary availability-or-invariant lemma, removing the earlier pure-species condition in the stated single-linkage setting.

## Independent falsification controls

Reproducer: `independent_checks.py`; results: `independent_checks.json`. Uses the Python standard library, exact integers and rational coefficients of logarithms of primes where applicable. It imports no paper code.

1. **153,976 graph-free availability scenarios.** Enumerated all nontrivial subsets of three-species binary complexes, all nonempty divergent-index sets, small nonnegative weights including zero-weight divergent indices, and bounded residual coordinates in {0,1,2}. Searched directly for a higher-weight enabled pair; if absent, independently searched an integer linear invariant with a diverging positive part. Found 146,882 enabled-pair witnesses and 7,094 invariant certificates; no failure. The certificate search does not implement the manuscript's case classifier.
2. **400 exact episode cases.** Compared full branching enumeration of episode endpoints with the drift recursion using exact symbolic logarithmic rewards. Included zero, unary, mixed and doubled complexes, parallel channels, and equal population increments with different sources and targets. Verified endpoint probability one and the exact target/source identity throughout; all passed.
3. **108 scalar-envelope comparisons.** Checked both branches, their common boundary, interior maximizers and very small continuation probabilities; all passed.
4. **Unit-rate attenuation family.** For d=2,…,5 and N=10⁶, direct evaluation agrees with the claimed coefficient −2/dᵈ after division by log N to within 3×10⁻⁶. This checks the quantitative warning rather than implying a uniform useful drift bound.

I also reconstructed by hand the initial boundary stress example, the Anderson–Cappelletti–Kim example's displayed phase drifts, and the fixed-m limit as the indicated rate tends to zero. Their signs and asymptotics are consistent. These controls do not exhaust arbitrary dimension, prove universal recurrence, enumerate K, or validate stationary tail/mixing claims. The analytic reconstruction is the basis for the verdict.

## Strongest checked claim and remaining gap

The strongest checked claim is Theorem 2.1 together with Corollary 2.3: **every finite weakly reversible single-linkage bimolecular stochastic mass-action network with positive constants has a nonexplosive positive recurrent minimal process on each nonabsorbing reachable class and a unique stationary probability there; absorbing classes have their point masses.** The proof includes arbitrary species count, boundary populations, zero complexes, multiple rate scales, parallel channels and conserved lattice restrictions.

**No unresolved analytic gap or substantive mathematical defect was identified in that claim.** Remaining review limitations are formal machine verification, exhaustive prior-art search, and the package's own cross-interpreter/release reproducibility assertions, which were outside this independent analytic track. No repair or extension was attempted. In particular, this verdict should not be promoted into a claim about multiple linkage classes, higher-order complexes, computable Foster-set size, mixing rates, or stationary moments.
