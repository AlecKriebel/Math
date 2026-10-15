# Independent classical-coverage priority audit: PR234 / 30002291

Audit date: 2026-10-15 UTC. This is the isolated classical theorem/proof-coverage lane. The frozen proof was read before inherited scope notes; no root or sibling review conclusions were consulted. Mathematical validity is an assigned premise, not a conclusion established anew here.

## Finding

**The retrieved classical theorem statements do not literally cover the entire submitted arbitrary-predictable-compensator class. That is not a novelty certificate. The candidate is a close, comparatively elementary quadratic specialization and extension of an established truncation proof.** Two exact scope witnesses below identify remaining theorem-level differences. The result should not be described as the first semimartingale-driver response to the open-ended OWR question: adapted scalar-volatility drivers were already treated in the 2016 preprint, with a stronger functional conclusion.

The frozen literature notes should add two priority facts: a marked-jump Lévy result was publicly announced in May 2014, and the 2018/2019 general-functionals theorem formally covers nonsymmetric Lévy drivers. Full original-field stability, joint fixed-time convergence, phase conventions, and arbitrary deterministic mesh sequences are not convincing novelty distinctions.

**Qualification:** the controlling full preprints and selected extensions were retrieved and read; final AOP and Bernoulli publisher PDFs could not be independently retrieved in this lane because publisher and institution endpoints were blocked. The local cache called lma2017.pdf is the 2015 preprint. Thus this report does not certify a line-by-line comparison against both final publisher versions. Their final PDFs remain a specific unresolved source-verification task, not evidence for novelty.

## 1. Frozen target and implication standard

The target is the theorem in PROOF.md, SHA256 `508f71b81ee669d4934ef1cc9e061c129e47d36359896ad7b3e20574dbfbc539`:

- A real-line simple pure-jump Itô driver has characteristics `b_s ds` and `nu_s(dz) ds`, with deterministic global bounds `|b_s|<=B`, `integral z^2 nu_s(dz)<=K`; all jumps are compensated in L2. Time diffuseness is required, not diffuseness in the mark variable.
- `g(x)=x_+^alpha f(x)`, `0<alpha<1/2`, `f in C^1`, `f(0)!=0`, and both `f,f'` decay exponentially.
- The real-line convolution has controlled prehistory. For every deterministic `Delta_n -> 0`, normalized quadratic increment sums converge jointly at finitely many fixed positive times, stably relative to the entire original sigma field, to squared actual jumps carrying independent uniform phase weights.
- No scalar-volatility representation, symmetry, stationary increments, independent increments, or activity index strictly below 2 is assumed.

The audit distinguishes (A) substitution in a stated theorem; (B) a consequence after a routine ancillary argument, such as removal of a smooth drift; and (C) an extension requiring new hypotheses to be inserted and parts of a proof to be replaced. An available method for proving a claim does not by itself establish that the claim was already stated or proved. Conversely, a correct extension of a known method does not establish a publishable novelty contribution.

Primary-source capsules, each under 200 words, are in SOURCE_CAPSULES.md. Source IDs below refer to those capsules and to SOURCE_LEDGER.md.

## 2. Exact overlap with the scalar Lévy and LSS results

This section records the audit's substitutions and logical deductions.

For the classical power theorem take `k=1`, `p=2`, `c0=f(0)`. The singularity restriction becomes exactly `alpha<1/2`. Let

`h1(x)=x_+^alpha-(x-1)_+^alpha`.

The classical weight `sum_(l>=0) h1(l+U)^2` equals the candidate weight at `1-U`, by setting `j=l+1` in `sum_(j>=1)h1(j-u)^2`. Independent uniforms remain independent uniforms after this transformation. There is no distributional or stable-convergence difference.

For `dY_s=sigma_(s-)dL_s`, the actual jump is `J_s=sigma_(s-) Delta L_s`, so the classical coefficient is precisely `J_s^2`. Dependence of sigma on the past of L and on other adapted randomness is allowed in LSS16. It is incorrect to distinguish the candidate by saying classical volatility must be independent, stationary, Markovian, deterministic, or free of feedback.

LSS16 Theorem 1.2(i) implies joint fixed-time convergence at deterministic horizons because its limiting increasing jump process has no jump at any fixed deterministic time. M1 convergence is more than the requested finite-dimensional conclusion on this overlap. The v1 J1 assertion and v2 correction do not remove priority for the finite-dimensional result.

The classical (A) tail condition can use `theta=2` for a driver with a finite second moment: `r^2 nu(|z|>=r)<=integral_(|z|>=r)z^2 nu(dz)`. Exponential kernel decay gives every positive tail integrability exponent. For a globally bounded scalar volatility, (B1) is immediate for any permissible positive rho and finite beta-prime at least 2. The candidate's globally bounded quadratic rate, however, does not in general identify any underlying scalar L and sigma. One must not invoke (B1) before proving that representation.

The classes are not ordered globally. The classical theorems allow infinite-variance Lévy tails and broader parameters; the candidate imposes a global finite second-moment rate, quadratic power, first-order increments, and a restricted singularity interval. The candidate extends particular driver directions while restricting other directions.

## 3. Nonsymmetry was already formally covered in 2018

FUN18 model (1.1) assumes a two-sided Lévy process without a Gaussian part, with no symmetry condition in the general first-order jump regime. Here is the exact specialization, using `phi` for its test function to avoid confusing it with the candidate's kernel factor.

Choose `phi(x)=x^2`. If `beta<2` and `alpha<1/2`, then

`q0=max(beta,1/(1-alpha)) < 2`.

Take an auxiliary regularity exponent `q` strictly between `q0` and 2. Then `1<q<2`, `phi` belongs to the source's local `C^q` class, and `phi(0)=phi'(0)=0`, which are exactly the derivatives up to integer part q. Thus Theorem 2.1(i) applies. Proposition 2.3(i) gives finite-dimensional stability; `phi>=0` also satisfies (FC) and hence gives M1 convergence. The normalization is `sum phi(n^alpha Delta X)=n^(2alpha)sum(Delta X)^2`.

This is a literal theorem specialization for Lévy drivers meeting (A), not an inferred extension of the 2017 symmetry remark. The earlier LMA15 Remark 2.3 already anticipated removal of symmetry, but the formal later theorem is the stronger priority reference. FUN18 still has `beta<2`, deterministic Lévy characteristics and the convolution model; it does not state the submitted arbitrary predictable-kernel theorem. Its proof uses the same finite-jump/truncation machinery and cites earlier power-variation estimates; it does not supply a hidden arbitrary-semimartingale theorem.

## 4. Two exact driver-scope witnesses

### 4.1 A symmetric kernel that is not one scalar dilation

Write `m_a=(delta_a+delta_(-a))/2`. Let the compensator kernel be

`nu_s=m_1+m_2` for `s<1`, and `nu_s=2m_1+m_2` for `s>=1`.

Construct the independent-increment jump measure with this deterministic, locally finite intensity on the entire real line, compensate all jumps, and put b=0. Its quadratic rate is 5 before the switch and 6 after it, so H holds with K=6. This is a symmetric finite-activity candidate driver with time-diffuse compensator.

Suppose it were a scalar integral against one fixed Lévy measure, so `nu_s(A)=nu_L({z:sigma_s z in A})` for nonzero marks. At both sides of the switch the support must be the same four-point set `{-2,-1,1,2}`. Two nonzero dilation scales giving this support can differ only by sign: a finite nonzero set cannot be invariant under any dilation of absolute value other than 1, by its smallest and largest absolute elements. Reflection leaves this symmetric kernel unchanged. Thus the relative masses at absolute sizes 1 and 2 cannot change. They do change from 1:1 to 2:1. Contradiction.

This excludes the scalar LSS representation; it does not exclude all finite-dimensional representations. Indeed extra switched compound-Poisson components can produce this example. The distinction matters: a finite vector theorem could cover some such examples, but cannot be silently substituted into the scalar theorem.

### 4.2 The integrable activity-2 boundary

Take a symmetric Lévy measure supported on `0<|z|<exp(-1)` with density

`1 / (|z|^3 log(1/|z|)^2)`.

Direct substitution `|z|=exp(-u)` gives

`integral z^2 nu(dz)=2 integral_1^infinity u^(-2)du=2`.

For every `r<2`, its r-moment near zero is

`2 integral_1^infinity exp((2-r)u)u^(-2)du=infinity`.

Its activity index is exactly 2 even though its quadratic rate is finite. With b=0 and the compensated L2 interpretation, this is already a stationary symmetric Lévy member of the candidate class. Every retrieved classical jump-regime theorem imposing `p>beta`, `beta<2` fails at quadratic power for this witness. Setting the source's tail exponent theta to 2 does not alter its small-jump index beta. FIELD20's Gaussian beta=2 remark is a different regime.

For `epsilon=exp(-m)`, the small-jump quadratic mass is exactly `2/m`, tending to zero. Hence the candidate's isometry estimate remains available at the boundary. This also shows why `p>beta` is a convenient sufficient hypothesis rather than a necessary condition for all quadratic marked-jump limits. The witness supplies an exact boundary distinction, not proof that nobody previously treated that boundary.

Finite sums of locally bounded scalar integrals against a finite collection of noises with indices all below 2 do not remove this witness: choose r strictly between their maximum index and 2. Their jump r-sums are locally finite after localization, and `|sum_j a_j|^r <= d^(r-1) sum_j|a_j|^r` preserves that property. The activity-2 witness has no such r. Infinite-dimensional or mark-dependent representations require a separate theorem and cannot be rejected by this finite-dimensional argument.

## 5. Why general Poisson embeddings do not produce a literal LSS corollary

JAC06 (H) and (2.11) provide the relevant established representation, on an extension if needed:

`dY_s=b_s ds + integral delta_s(u)(N(ds,du)-ds du)`.

The image of Lebesgue measure under `u -> delta_s(u)` is the predictable jump kernel. This is not new. But the scalar LSS theorem would require the special factorization

`delta_s(u)=sigma_(s-) kappa(u)`

for one deterministic mark map kappa, or an equivalent common scalar-dilation property. An arbitrary predictable kernel does not have it, as the four-atom witness shows. Relabeling the pair `(s,u)` as noise space does not change the theorem's allowed integrands.

Conditioning on the whole predictable coefficient field is not a valid shortcut: a field depending on earlier jumps carries information about N and may change its conditional law. A time change of intensities similarly changes both the observation mesh and the difference kernel; the physical-time convolution does not become the same stationary convolution merely by changing clocks.

LSS16's introductory spatial ambit formula permits a spatially varying volatility field, but Theorem 1.2 treats its one-dimensional scalar model. FIELD20 has genuine marked-Poisson random-field limits, yet deterministic kernels and independently scattered noise with deterministic characteristics. General predictable mark-dependent amplitudes are outside those stated models. The fact that the candidate can be represented as a random-field integral is therefore a route to adapting a proof, not an implication from the retrieved field theorem.

Applying scalar theorems separately to a sum of noises is also insufficient by itself. Quadratic variation contains cross inner products, and marginal stable convergence does not imply the required joint phase independence. With finitely many independent noises those points can be proved by the same finite-jump separation and phase-density argument. That is a very plausible extension, but it is additional mathematics.

## 6. General semimartingale criteria do not bypass the singular convolution

The fact that Y satisfies JAC06's driver characteristics does not make the observed convolution X an admissible observed semimartingale in that theorem. Even in finite-activity cases, where X is a continuous finite-variation path, ordinary quadratic variation gives the unnormalized limit zero. It does not identify the nonzero limit after multiplication by `Delta^(-2alpha)`.

In higher-activity cases, the kernel derivative behaves like `x^(alpha-1)` near zero, so ordinary differentiability/isometry conditions fail there. ID14's decomposition and recognition theorems require their own deterministic infinitely divisible representation and concern the semimartingale property, not this mesh-scale asymptotic. Importing a semimartingale criterion would need to establish both that it applies to X and that it controls the necessary rescaled increments; doing neither transfers the central difficulty to an unsupported claim.

The source's standard martingale isometry, compensator identities, Fubini results and convergence-together theorem remain valid proof ingredients. Citing those ingredients credits the mechanism; their existence does not make every later convolution limit a previously stated theorem.

## 7. What genuinely must change in the classical proof

The full LMA15 relevant proof and the full LSS16 part (i) proof were inspected, not just their abstracts. The adaptation is close:

| Step | Already present | Replacement for the submitted class | Assessment |
|---|---|---|---|
| Singular impulse profile and summable phase weights | LMA15 finite-jump analysis; LSS16 Lemma 4.3 | Same deterministic k=1,p=2 calculation | Established mechanism |
| Independent fresh phases relative to the full original field | LMA15 Lemma 4.1; LSS16 Lemma 4.3 | Show finite truncated jump-time vectors have a density under bounded predictable intensity; L1 Fourier mixing removes smooth-density restriction | Elementary extension; not a new phase phenomenon |
| Negligible long-separated impulses | Both proofs | Same disjoint-neighborhood/Cauchy–Schwarz argument | Established mechanism |
| Arbitrary drift and prehistory | Existing tail estimates/Fubini technology | Controlled L2 derivative on the negative-time part and bounded absolutely continuous drift | Routine simplification under stronger moments |
| Small jumps | LMA15 Lemma 4.2; LSS16 Lemma 4.7 | Replace Lévy/decoupling estimates by the direct compensated-random-measure isometry and a uniform impulse-energy bound | Short, substantial hypothesis extension; mathematically easier at p=2 |
| Remove cutoff and preserve stability | Both proofs use root statistics and convergence together | Same root-statistic inequality and bounded-field tests | Established mechanism |

For the critical small-jump step the audit's independent reconstruction is

`E[Delta^(-2alpha) V(R^epsilon;T)] <= C E integral_0^T integral_(|z|<=epsilon) z^2 nu_s(dz) ds`.

The right side tends to zero by dominated convergence and H, with no activity restriction below 2. Its content is the p=2 energy estimate, not independent increments. In LSS16 Lemma 4.7, the displayed small-mark bound already reduces to an integral of `|z|^p+z^2`; at p=2 that quantity is integrable even for the boundary witness. But replacing the underlying Lévy process and deterministic measure by a general compensator is still a proof modification, not direct substitution in the theorem.

For the phase step, an intensity bound `lambda_s^epsilon<=K/epsilon^2` gives factorial moment domination by the corresponding Lebesgue measure on each ordered time simplex. Therefore the joint law of each finite truncated jump-time list, also weighted by any bounded original-field variable, has an L1 density. The Riemann–Lebesgue lemma yields joint phase mixing for every deterministic mesh sequence. This does not assume conditionally Poisson jumps. The argument is standard in character and checkable; this audit found no materially different mechanism from classical finite-jump phase mixing.

## 8. Differences that should not be promoted as novelty

1. **Full F stability:** LSS16 is explicit about the original sigma field. In the deterministic Lévy case, any bounded external variable can also be replaced by its conditional expectation given the driving path; the statistic and its limit kernel are measurable through that path. Natural-filtration notation does not create a stronger new limit.
2. **Arbitrary deterministic mesh sequence:** SUR14 already writes general Delta_n. LMA15 Lemma 4.1 proves its analytic estimate for arbitrary positive rho, only later setting rho=1/n. Replacing rho by Delta_n is routine.
3. **Joint fixed times:** supplied by existing functional results on the overlap.
4. **Changing the uniform phase convention:** the reindexing in section 2 is exact.
5. **Bounded drift:** convolution of bounded drift has a square-integrable derivative and contributes at most order `Delta^(1-2alpha)`.
6. **Nonmonotone exponentially decaying kernel tails:** K need not imply literal eventual monotonicity of `|g'|` in (A). For example `f(x)=exp(-x)(2+sin(10x))` produces infinitely many derivative zeros. But write `g=f(0)x_+^alpha exp(-x)+r`; then `r(0)=0`, `r'=O(x^alpha)` near zero and r' decays exponentially. Thus r' belongs to L1 and L2. Under H its convolution is absolutely continuous with square-integrable derivative and has negligible normalized variation. This is a routine smooth-remainder reduction, not a convincing independent novelty direction.

## 9. Priority timeline and exact remaining gap

| Date authenticated from primary history | Record | What priority it supports |
|---|---|---|
| 2013 report; workshop 2013-02-10 to 2013-02-16 | OWR13, printed 492 | Compound-Poisson formula and open-ended sufficient-conditions request |
| 2014-05-07 08:24:48 UTC | SUR14 v1, Theorem 4.8(i) | Earlier public Lévy jump-phase announcement; not a retrieved full proof |
| 2015-06-22 17:02:04 UTC | LMA15 v1 | Full retrieved Lévy proof; later AOP 2017 |
| 2016-04-08 11:16:22 UTC | LSS v1 | Adapted scalar-volatility marked-jump theorem and finite-dimensional proof |
| 2016-10-14 14:37:46 UTC | LSS v2 | Corrected functional M1 formulation; later Bernoulli 2018 |
| 2018-03-02 19:31:36 UTC | MULT18 preprint | Multiple singularity extension, still scalar symmetric Lévy |
| 2018-06-27 09:08:09 UTC | FUN18 v1 | Formal nonsymmetric Lévy general-functionals theorem; later EJP 2019 |
| 2020-08-04 08:42:42 UTC; v3 2022-02-21 | FIELD20 | Marked Poisson random-field extension, still deterministic-kernel independently scattered class |

**Strongest verified coverage conclusion:** the candidate's Lévy/low-activity overlap and its adapted scalar-volatility/low-activity overlap have prior marked-jump limit theorems. The uniform-phase phenomenon and truncation mechanism are established. The entire bounded-characteristic predictable-kernel class, especially the integrable activity-2 member, is not a literal instance of the inspected theorem statements.

**Exact unresolved priority gap:** locate a pre-submission theorem or a full proof expressly allowing arbitrary predictable mark-dependent compensators (or an equivalent general random-integrand Poisson formulation) at quadratic power, including finite quadratic rate with activity exactly 2. Alternatively, determine whether the extension was already stated as a corollary of a broader theorem. This lane has not found such a controlling source. Publisher-version verification also remains incomplete. No global novelty conclusion follows from these bounded searches.

The result is best described, pending broader priority verification, as an explicit L2 sufficient-conditions extension using the established proof. It cannot responsibly be advertised as a new limit mechanism, a first non-Lévy/semimartingale extension, or the first nonsymmetric Lévy result.

## 10. Checkable artifacts and boundaries

`scope_checks.py` and SCOPE_CHECK_RECEIPT.json verify the finite-support dilation obstruction exactly with rational arithmetic, the rates K=5/6, and the auxiliary exponent specialization across boundary-near rational parameters. The activity-2 witness is given by the exact analytic integral reductions above. No simulation is used as novelty evidence.

No Git/index/ref mutation, provider mutation, outreach, external individual communication, or sibling-review consultation occurred. The only parent exchange requested source locations and reported this lane's independently derived findings. All authored outputs are confined to this lane folder. Whole PDFs, extracted texts and retrieval/search records are ignored under `private_sources/`; no full source text is included in the publication manifest.
