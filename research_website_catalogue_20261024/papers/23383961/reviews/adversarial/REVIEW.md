# Independent adversarial review: Zenodo 23383961

Reviewed work: **Nonmonotone Argument and Radial Angle of a Support Slit**, Alec Kriebel, version 1.0, 14 October 2026, DOI 10.5281/zenodo.23383961. Review completed 25 October 2026 UTC. Reviewer: GPT-6.1 Sol, Ultra reasoning, independent AI review; no human peer review or publication clearance is implied.

**Scientific verdict: PASS within the stated mathematical scope. No substantive mathematical defect or unresolved gap was found in Theorem 1.** The proof establishes the claim for every global maximizer of the displayed functional, subject to the correctly applied classical compactness, coefficient, area and support-slit theorems. Historical firstness and the questions' contemporary open status are not cleared. No source repair was attempted or needed.

## Exact claim and success criterion

Let S be the analytic injective functions on the unit disk with f(0)=0 and f′(0)=1. For ε=10⁻²⁴, set L(f)=a₂(f)+iε(a₄(f)−3a₃(f)). The claim is that global maximizers of Re L exist, and **every** such maximizer omits an actual analytic arc Γ with nonmonotone continuous polar argument, nonmonotone signed outward radial angle, and nonmonotone ordinary nonnegative outward radial angle. Either monotone direction is allowed. This is an existence result for actual support points, not a sufficient condition that an arbitrary differential trajectory be realizable as a support slit.

Success required the entire published reader and current manuscript, primary theorem hypotheses, uniform estimates for all maximizers, an actual-slit continuation argument, branch and orientation control, and strict sign margins. A finite sample or a prior PASS string would not meet that criterion.

## Identity, custody, independence and execution boundary

The actual published PDF was read in full as extracted text and as all five rendered pages. The entire current `support_slit.tex` was read and compared with it. Its SHA-256 is `c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3`.

The published PDF SHA-256 is `a6d227d606fda3e68adc6db4eab462ee3f12b0544a201121b5c3a21aa5099e3d`; the ZIP SHA-256 is `58853fd56272184efe8232c58c356b1a669ba43032e3c4f35e4b17e317898f51`. Independent ZIP reading found 255 regular members, including 12 hidden members. All 255 extracted files agree byte for byte with their archive members. Archive member bodies outside the explicit read ledger were hashed as opaque bytes. There was no additional published reader or nested archive requiring a separate mathematical assessment.

I first reasoned from the current manuscript and primary inputs. I did not read the current sibling analytic review, current scope judgments, or historical internal review/verdict/acceptance bodies. Raw scope maps and read ledgers were used only to locate sources. The historical PRE_GOH and PRIMARY_AUDIT TeX files remained opaque. Selected mathematical derivation excerpts were read later as supporting material. Two incidental historical/local assessment sentences embedded in those supporting files are disclosed in `current-read-ledger.json`; neither was adopted as evidence. Hashing the frozen historical proof for a submitted program did not entail reading or accepting its assertions.

Every submitted program executed here was statically read in full first. Execution was confined to copied files under `runtime/quarantine`, using isolated Python execution. No source program was imported or run in its published directory. The selected scripts use standard-library arithmetic and stdout; the quantitative script additionally reads a copied frozen proof solely to compute its SHA-256. There was no network access by the checks, source write, package installation, Git operation, release, website/Sheet/UI change, or external communication. The all-jobs historical runner and unrelated priority programs were not executed. No finite directed-interval calculation is an input to the proof of this theorem; the archive's Zemyan-specific interval work concerns a different prior construction and was not substituted for the primary theorem interfaces here.

## Primary interfaces checked

The full source identities, hashes and read scopes are in `primary-read-ledger.json`.

* **Duren (1981), pp.352–355:** actual definition of S and support point, positive differential Φ(w)dw²/w², one omitted analytic arc with increasing modulus, L(f²)≠0, and the radial-angle convention. These pages were read and visually inspected. The current L is continuous complex-linear and Re L is nonconstant: the Koebe function and identity give real values 2 and 0. A compactness maximizer therefore meets the support-point hypotheses; no uniqueness assumption enters.
* **Pfluger (1971), introduction and §§3.3–3.4, 3.6, 4.1–4.5:** kernel class, global maximizing hypothesis, slit geometry, nonzero coefficient at infinity, and radial ordering. Here the kernel is K(z)=z⁻³−3iεz⁻⁴+iεz⁻⁵, which is rational, holomorphic outside any sufficiently small positive radius, vanishes at infinity, and defines precisely the current finite coefficient functional. The nontriviality condition is met. Pfluger's differential sign is opposite Duren's; the manuscript uses Duren's sign consistently. These classical results are imported, rather than claimed to have been formally reproved by the check programs.
* **de Branges (1985), pp.137–138:** the published coefficient bound applies to the exact normalized class used here. Only |a₂|≤2, |a₃|≤3 and |a₄|≤4 are needed. The complete proof of the Bieberbach theorem was not independently reconstructed.
* **Pavlović–Peláez (2011), pp.909–910:** the complete classical area theorem statement and the two-sided distance/conformal-radius inequality were read, including their hypotheses. For their Theorem 1 take φ(z)=z/g(z)=H(z²). Then φ is analytic, φ(0)=1, and φ/z=1/g is meromorphically injective. The theorem yields the required weighted exterior coefficient inequality. Their Eq.(1.4) applies to the simply connected proper image f(D) and gives distance ≤ conformal radius in the direction actually used. Neither classical result is credited to that paper as its originator.
* **Brown (1979), restricted point-evaluation theorem and proof:** L(g)=g(z₀), with the stated disk and conjugation reductions, has the positive monotonicity conclusion. Brown's A=arg(w/w′) is the negative of the current signed outward angle. His theorem is restricted to that functional family and does not contradict the fourth-degree perturbation. The complete hypotheses, theorem statements and relevant monotonicity proof were inspected.
* **Hayman–Lingham v2, printed p.143/PDF page144:** the full Problem 6.72 asks exactly the two actual support-slit questions addressed here. Its 2018 update is not evidence of current open status.

## Adversarial reconstruction of the proof

### Every maximizer, without a selection hypothesis

Compactness and continuity provide a global maximizer. Since its value is at least the Koebe value 2,

Re a₂≥2−ε|a₄−3a₃|≥2−13ε.

Combining this with |a₂|≤2 gives |a₂−2|²≤52ε and 0≤1−|a₂|²/4≤13ε. The last inequality uses Re a₂>0 before squaring. Thus |a₂−2|<8η for η=10⁻¹².

The normalized root g(z)²=f(z²) exists analytically and is odd. If g(z₁)=g(z₂), injectivity of f gives z₁=±z₂; the minus case forces g(z₁)=0 and then z₁=z₂=0. Hence g is injective. Its normalized reciprocal exterior map is injective, so the area theorem gives |a₃−3a₂²/4|≤2√(13/3)η<5η and the full weighted H-tail bound. Since |a₂+2|≤4, |a₃−3|<29η. Consequently |A+2|<106η and |B−3|<24η for A=2a₃+a₂²−6a₂ and B=3a₂−3.

Every step uses inequalities shared by every maximizer. No maximizing selection, differentiability in ε, uniqueness, actual-map solver, or assumption that all points in the coefficient enclosure are realizable is used. Enlarging to the full coefficient enclosure only strengthens the robustness requirement.

### Actual tip, rather than a perturbative tip guess

The exterior area theorem applied to H(z)=√(z/f(z)) yields Σₙ≥₂(2n−1)|cₙ|²≤13ε. On |z|≤2/3, weighted Cauchy–Schwarz uses the explicit sums 16/135<1/4 and 56/25<9/4. It gives |H−(1−z)|<5η and |H′+1|<10η. These are whole-disk analytic estimates, not just estimates along the negative real axis.

At z*=−2/3, H₀=5/3. The strong proximity estimate supplies |H+H₀|<7/2 as well as 3/2<|H|<11/6. The reciprocal-square identity gives |f(z*)−k(z*)|<2η. In f′=(H−2zH′)/H³, the numerator error is <(5+40/3)η<19η; division contributes <6η and the reciprocal-cube remainder <2η. Thus |f′−k′|<8η.

For an inscribed image disk of radius d, compose its inverse with a disk automorphism taking f⁻¹(f(z)) to zero. Schwarz's lemma gives d≤(1−|z|²)|f′(z)|. Passing to the maximal disk proves the inequality in the manuscript. At z*, k=−6/25 and k′=9/125, so the actual omitted set contains a boundary point with modulus below 7/25+7η<3/10. Since the actual arc has increasing modulus, its actual finite tip lies below that radius. This does not assume continuity of tips as ε→0. A reversed inequality is false even for the identity map at z=2/3, where boundary distance is 1/3 and conformal radius is 5/9.

### Exact Schiffer algebra and inverse branch

Direct extraction gives coefficients of f²/(f−w): z²↦−1/w, z³↦−2a₂/w−1/w², and z⁴↦−(2a₃+a₂²)/w−3a₂/w²−1/w³. Thus Q=−a/w³−b/w⁴−c/w⁵ with a=1+iεA, b=iεB, c=iε. The coefficient a₄ does not enter this differential, although its bound was needed in the maximizing comparison.

For w=−v⁻², dw=2v⁻³dv and Qdw²=4(a−bv²+cv⁴)dv². The alternating signs are essential. On |v|≤3, P lies within 111ε of 1, so it has the analytic square root p with Re p>0. Its primitive G differs from v by at most 333ε. Rouché's comparison with v−t has boundary gap >1 for every |t|<2, giving one root in |v|<3. Since p≠0, these roots patch to a holomorphic inverse V. There is no unsupported assertion that a merely local inverse extends globally. A separate check is that integrating |p−1|<111ε along straight segments in the convex disk makes G injective.

Evenness of p makes G and V odd. V has no zero away from t=0, W=−V⁻² is regular, Q(W)W′²=4, and |W|>25/81>3/10 for 0<t≤7/4. Equal W-values force V(t₁)=±V(t₂), then t₁=±t₂, so positive parameters give no self-intersection. Changing the square-root sign changes G and V by the corresponding odd sign and leaves the geometric W and Z unchanged.

### The central continuation attack

A distant tail of the **actual** Γ lifts under w=−v⁻² to v→0. Along it, (p(v)dv)² is positive, so p(v)dv is real and Im G is constant. Its limit is zero. The lifted tail therefore has real natural coordinate tending to zero; its two possible signs project to the same W by oddness. This proves coincidence near infinity directly in this instance.

Let E={t∈(0,7/4]:W(t)∈Γ}. It is nonempty and relatively closed because Γ is the closed complement of f(D). At a member of E, W cannot be the actual finite tip: its modulus exceeds 25/81, while that tip is below 3/10. The gap is at least the explicit 7/810. It is not infinity, and Q is finite and nonzero there by the exact trajectory identity. In a local square-root coordinate, regular positive trajectories are horizontal line segments. The actual Γ contains a local open segment through this interior point, so uniqueness makes E relatively open. The connected interval forces E to be the whole tested interval.

This closes the main possible realizability gap. It does not transfer the problem to an unproved converse extremality criterion or assume that any formal trajectory is omitted. The argument would fail if the tip separation or the actual support theorem were absent; both are independently supplied here.

### Uniform errors and angle reversal

The manuscript's error bookkeeping survives direct recomputation. The square-root expansion costs 161εη+(111²/2)ε²<162εη. Its primitive costs <486εη, and inversion adds at most 55·333ε²=18315ε², giving <487εη. For V′, complex Taylor's integral remainder is valid on |x|≤1/4: the inverse-root second derivative has modulus <4, giving remainder ≤2|x|². Coefficient uncertainty, quadratic error and composition cost are respectively 161εη, 24642ε² and 20979ε², totaling <162εη. Straight segments used in these replacements remain inside the convex disk. The estimates cover complex coefficient errors and every point of the stated domains.

With d=t+t³/2−t⁵/10, q=d′−d/t=t²−2t⁴/5, and Z=tV′/V, subtraction before division yields the exact identity

V(Z−1−iεq)=tRᵥ′−Rᵥ−iεq(V−t).

No cross term was discarded. On 1≤t≤7/4, |V|>1/2 and |q|<7 give error ≤1541εη+4662ε²<2000εη. The normalized error 2000η is only 2·10⁻⁹. The values q(1)=3/5 and q(7/4)=−441/640 therefore imply strict signs beyond ±ε/2.

For all 0<t≤7/4, the independent identity Z=[G(V)/V]/p(V), with G(v)/v a radial average of p, gives |Z−1|≤222ε/(1−111ε)<223ε. This does not divide a crude absolute V error by small t. Hence Re Z>0 uniformly, including toward infinity, and increasing t is inward.

For a continuous polar lift θ, θ′=−2 Im Z/t has both signs. For the outward tangent, (−W′)/W=2Z/t, so the canonical signed angle is β=arg Z in the right half-plane. Odd analyticity gives V=a⁻¹ᐟ²t+O(t³), hence Z→1 and β→0 as t↓0. The values β(1)>0 and β(7/4)<0, together with that initial zero limit, exclude both monotone directions. Opposite endpoint signs alone would not suffice: β(s)=−s on [−1,1] is a counterexample to that shortcut.

Continuity then supplies an interior zero while |β| is positive at both endpoints, so the ordinary angle |β| has an interior minimum and is nonmonotone on the compact tested subarc. The inward-tangent unsigned convention gives π−|β|, retaining nonmonotonicity; the acute tangent-line convention gives |β|. No branch jump is used. At ε=0 the strict signs disappear, as the paper states. No conclusion for arbitrary positive ε is asserted.

## Reproduction and falsification artifacts

Four submitted programs were read completely, copied and replayed:

| Program | Passed finite checks | Role |
|---|---:|---|
| original `verify.py` | 56 | Coefficient algebra, constants and controls |
| `reviews/analytic01/checks.py` | 31 | Exact algebra and alternative propagated bounds |
| `reviews/quantitative01/quantitative_checks.py` | 97 | Exact constants, alternative disk-2 bounds and nine mutation predicates |
| `root_reproduction/verify_angle_distinction.py` | 8 | Auxiliary distinction between tangent turning and the target angles |

These are 192 finite checks, not 192 independent mathematical arguments. The angle-distinction construction is not asserted to be a realizable support slit and is not used to prove the main theorem. Existing script names and PASS fields were not treated as proof.

Fresh authored controls add 38 exact checks. Four physically mutated copies of the authored program—wrong quotient sign, wrong double-cover sign, invalid tip bound and changed test endpoint—each fail at the intended assertion. Their exact single-line changes and stderr are retained in `evidence/mutant-execution.json`. Additional exact controls reject dropping the quartic term, dropping the −3a₃ term, using an inflated uncertainty without reproof, reversing the boundary-distance inequality, and claiming strict signs at ε=0.

A separate implementation forms a fourth-order binomial polynomial for p and its integrated natural coordinate, then uses 110-digit Decimal complex Newton iteration. It probes the nominal coefficients plus 64 independent axis/Pythagorean boundary combinations for A and B, at t=1, t=7/4 and t=10⁻⁶: **195 probes across 65 cases**. The worst normalized endpoint values were approximately 0.599999999992 and −0.6890624999755. The largest observed |Z−1−iεq|/(εη) was below 24.501, compared with the analytic allowance 2000. The largest polynomial-root residual was about 10⁻¹⁰⁹. On the disk the binomial truncation in G is bounded by 6(111ε)⁵≈1.0111·10⁻¹⁰⁹.

These Decimal probes are consistency diagnostics, not interval arithmetic or a validated construction of an extremal map. Floating point and residual checks do not prove the every-maximizer statement; the analytic enclosure proof above does. The exact coefficient composition check also uses a standard method present in a submitted script, so it should not be counted as a wholly distinct algebraic approach. The independent Newton implementation, primary-interface assessment, tip/continuation analysis and branch countercontrols provide the materially different adversarial checks.

## Strongest verified result and exact remaining limits

The strongest verified result is the complete mathematical statement of Theorem 1 for ε=10⁻²⁴: every global maximizer exists as a genuine support point and has all three stated failures on its actual omitted arc. The uniform estimates and the open/closed continuation supply the universal quantifier. **No unresolved mathematical gap in that statement remains from this review.**

The proof relies on established classical theorems whose applicable statements and hypotheses were checked against primary sources; their full historical proofs were not formally verified here. There is no explicit extremizer formula, uniqueness result or numerical construction of a maximizing map, and none is needed. The work is an unrefereed AI-assisted note. The broad historical comparisons in Section 5 were not comprehensively re-audited by this mathematical adversarial review; no priority or continued-open-status conclusion follows. The paper itself disclaims those claims. Root must read and reconcile all final reports before any promotion.

The before/after custody comparison, explicit read ledgers, evidence hashes, machine verdict and final file seal accompany this report. The completion estimate is 100% for this assigned adversarial review only; it does not measure completion of the wider publication program.
