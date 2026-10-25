# Independent adversarial review — Zenodo 23524971

**Verdict: PASS for the exact stated mathematical theorem.** No substantive defect was found in the complete six-page manuscript, the necessary proof support, or the load-bearing recurrence argument. This is an internal mathematical assessment, not external human peer review, formal proof-assistant verification, a historical-firstness certificate or permission to publish.

The strongest verified result is: for **each fixed real λ>0**, the continuous-time Markov chain on nonnegative integer quadruples with exactly the six displayed rates is nonexplosive, irreducible and positive recurrent, and hence has a unique stationary probability law. The proof gives a finite set F and a coercive V with `LV≤−1` off F, plus finite expected continuous-time hitting/return times. There is no remaining mathematical gap identified for that theorem. The source-version and novelty limitations below remain real limits on attribution, not defects in the generator-specific proof.

## Source binding and coverage

The reviewed record is **23524971**, row65, *All-load stability of a deterministic-first-chunk file-sharing chain*, version1.0,20October2026.

| Material | SHA256 |
|---|---|
| Published main PDF,6pages | bee5abffcfdb1ce8bc50f706480c81c4a80e8d609bec2a9d99c6aa4e9b805036 |
| Published source/verification ZIP | 38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e |
| Current main.tex | 9949c92633f1654cceadfc40f6988e3e2363db4ed229face05eb2d1b681a7611 |
| Required original/TURN_4.md | 34e043b456ddc25cc37d86d3e5a39d10243de91c6a5d5002952252d2eab1b0fa |

Read and visually inspected all six current PDF pages; read all current TeX and the complete required original proof `TURN_4.md`. The archive's embedded `paper.pdf` is byte-identical to the main PDF, so there is one distinct six-page reader. The current README and all three relevant mathematical programs were read. Every one of92 regular extracted files was compared byte-for-byte with its ZIP member without interpreting historical verdict bodies. Public assets retain their receipt size, MD5 and SHA256. Details are in `source_integrity.json`.

Independence was preserved: `INDEPENDENT_DERIVATION.md` and `fresh_exact_controls.py` were written and executed after reading the current PDF but **before** opening `TURN_4.md` or submitted helpers. No sibling findings were read. Dedicated historical reports, `original/RESULT_ACCEPTED.md`, `ROOT_ANALYTIC_ASSESSMENT.md`, saved old result bodies and old review verdicts remained opaque. Incidental historical candidate/pending/acceptance wording in the current manuscript/README and required `TURN_4.md`, and PASS literals in mathematical code, was seen and is not treated as evidence. Archived prior proof attempts1–3 were not needed for the current global proof and were not used to fill a gap.

## Literal model and falsification boundary

At state `(a,b,x,y)`, set `D=x+y+1`. Arrivals increase `a` or `b`, each at rate `λ/2`; first downloads move `a→x` and `b→y` at rates `a(x+1)/D` and `b(y+1)/D`; departures decrease `x` and `y` at rates `x(y+1)/D` and `y(x+1)/D`. Zero-coordinate decrements have zero rate. In particular, neither empty population enters D.

This exact rate table passes comparison with Figure2 in fresh arXiv:0910.5577v1 and the retained January5,2011 author proof. The latter explicitly explains invisible waiting rooms. Their conjectures differ: the2009 preprint conjectured high-load instability, whereas the2010 OWR contribution and retained2011 proof state stability. The original OWR contribution, the2011 model/stability definition/conjecture and adjacent fluid proposition were read directly. The2011 publisher body was not substituted for the retained author proof.

The aggregate seed-origin rate is `(a+b+x+y)/D`. At `(2,3,0,0)` it is5, so a capacity-one seed model is incompatible with these rates. The current manuscript explicitly warns that no aggregate seed bound is imposed. This is a required scope qualification, not a discovered flaw. The theorem must not be described as stability under an arbitrary bounded-bandwidth seed or as a general file-sharing result.

## Adversarial reconstruction of every load-bearing step

| Current location | Verification and attempted failure mode | Conclusion |
|---|---|---|
| p2,(2)–(3) | Compute W and Z increments separately for all six jumps. Every internal jump removes one workload unit; first downloads leave Z unchanged. `u+d≥n/(n+1)` because the numerator is≥n and D≤n+1. | Exact identities and the independent small-load range `0<λ<1/2` hold. |
| p2,(4) | At the nonsmooth-looking rounding interfaces, h is C1 with globally1/m-Lipschitz derivative. The bound follows by integrating the derivative, including crossings of±m. Quadratic variation has rate λ+d; `c/(2m)=1/8` yields β17λ/8 and q7/8. | The departure quadratic-variation contribution is present; dropping it is caught by a fresh negative control. |
| pp2–3,(5)–(6),Lemma1 | Detailed balance gives weightsγ^k. Truncated means increase toθ+1, so finite R with both strict inequalities exists for every fixed realλ. Prefix centered sums have negative sign; the terminal equation is `Rg(R−1)=R−μ`. Birth increments are nonpositive, death increments nonnegative. | Corrector nonnegative, bounded and decreasing; comparison holds at y=0,R; all increments vanish at y=R+1 and above. No stationary averaging of the original chain is used. |
| pp3–4,(7)–(11),Lemma2 | Use the **post-jump** product rule. Every first download increases D and decreases or preserves both numerators; all its interface terms are nonpositive even when waiting rooms are arbitrarily large. Departure bound uses D≥2; D=1 has no departures. | Both global bounds(8),(9) hold pointwise. Departure errors can be positive and are actually budgeted. |
| p4,(12) | Both visible counts≥R+1 ensure current and successor correctors vanish, including a drop toR. `d≥min(x,y)`. | Strict drift below−2; the threshold is correctly R+1, notR. |
| p4,(13)–(15) | In y≤R,x≥N: `d≤2R+1`, `(x−y)/D≥1/2`, `qd≥(21/32)(2y+1)≥y`, and interface remainder≤1. If b/D≥η, μ>β+c+4 supplies negative drift. Otherwise the N constraint forces Z≥m, and `f(y−μ)≤y` handles the entire ramp. | Both corners and cutoff boundaries covered; drift≤−3. Symmetry is exact. |
| pp4–5,(16) | Complement of the preceding regions has x+y≤N+R; arbitrary waiting queues are handled by `u≥(a+b)/(N+R+1)`. Constants R,G,N,B depend on fixedλ and are finite. | Exhaustive all-state coverage; drift≤−1 outside finiteF. No switching between unrelated Lyapunov functions. |
| p5,(17)–(18) | `V≥W≥n` and `V≤(1+c)W+cm/2+2G`; jumps bounded by `2+c+2G`. Finite-state localization, nonexplosion, Fatou and monotone convergence yield `E_s τ_F≤V(s)`. | Coercivity and continuous-time integrability are justified without assuming an invariant moment. |
| p5,regeneration | Choose finite positive-rate paths from every state ofF to zero. FiniteF yields common horizon and positive success probability. Workload and the Poisson arrival count bound `E V(S_T)` uniformly overF. Strong Markov geometric trials have bounded mean; zero holding time is1/λ. | Finite mean regeneration cycle and unique stationary distribution follow. This concerns the actual continuous-time clock, not just the embedded jump chain. |

The detailed fresh reconstruction is preserved in `INDEPENDENT_DERIVATION.md`. It already contains the entire mechanism before any historical mathematical helper was read. At the parameter edges, λ=0 is excluded because irreducibility of the whole space fails; arbitrarily small positiveλ and arbitrarily large fixedλ are allowed. No uniform constants or computational efficiency are required by the theorem.

## Primary Foster interface and attribution

The fresh Meyn–Tweedie primary PDF was read at the extended-generator/Dynkin definitions and condition(CD2), Theorems4.1–4.4, with Theorem4.2 visually inspected at printed p529. Here use f≡1,c=1,C=F and finite `d≥1+max_F LV`. A finite positive-rate path from every state ofF to zero, followed by holding there until a common timeT, gives `P_T(s,{0})≥ε>0` for s∈F. Hence F is small/petite and closed, and V is bounded on it. Finite stopped neighborhoods ensure the localized generator-domain conditions. Nonexplosion was separately proved from `jumps≤W(0)+3Pλ(t)`. These meet the continuous-time theorem hypotheses. The manuscript's direct regeneration proof supplies a second way to the same conclusion.

For this application, π(f)<∞ means only π(1)=1. It does **not** establish finite stationary population/workload moments, π(V)<∞, geometric ergodicity or useful performance bounds. The paper correctly disclaims these. The large finite thresholds illustrate a proof certificate, not a realistic estimate of queue sizes.

Read the full retained Allerton2012 body (five pages) to test the comparison with Common Chunk. Its state sampling and departure rule differ. Independent enumeration of the eight equally likely three-sample outcomes at `{seed{1,2},peer{1}}` gives departure probability7/8; the six-rate DFC chain gives1/2. `protocol_control.json` records this. Positive fixed arrival rates also prevent a mere state-dependent time rescaling from identifying the natural generators. The final rare-chunk conjecture in that paper concerns another protocol, not evidence that DFC remained open. These checks support the manuscript's bounded comparison, not a comprehensive priority search.

Primary versions/URLs/hashes and access qualifications are preserved in `primary-bindings.json` and `PRIMARY_INTERFACES.md`. The2011 author proof and2012 Allerton PDF are retained raw primary copies, **not freshly authenticated public downloads**; that limit is explicitly recorded. Fresh public arXiv2009 independently supports the generator, fresh OWR2010 supports the historical stability question, and fresh author-host Meyn–Tweedie supports the theorem interface. The final2011 publisher body, final2015 extension and worldwide priority remain outside this review.

## Checkable controls and unmodified replays

Fresh independent exact-rational controls reconstruct the generator directly and check4,149 load-state pairs,1,383 at each of λ=1/8,1,4. They include zero coordinates, R−1/R/R+1/R+2, N−1/N/N+1, both cutoff endpoints and ramp neighborhoods, extremely large waiting rooms just at/aboveB, both asymmetric corners and symmetric states. Full finite Poisson equations, terminal extension, direct V drift, coercivity and bounded jumps are checked. The finite test set does not replace the all-real-load proof.

Fresh negative controls detect omission of the d/8 rounding contribution and reject a capacity-one reinterpretation. The separately enumerated Common Chunk comparison rejects a mistaken protocol identification. No float is used in a mathematical assertion in the fresh controls.

After that reconstruction, these published programs were read and executed **unmodified** in a dedicated isolated copy containing only the three mathematical scripts and required proof file:

| Program | Fresh exit | Reported assertions |
|---|---:|---:|
| original/checks/turn4_checks.py | 0 | 71,165 |
| original/checks/independent_review_portable.py | 0 | 36,709 |
| reviews/foster_recheck_02/exact_falsification.py | 0 | 315,600 |

The latter two reconstruct the corrector by backward reflecting-boundary recurrence and killed tridiagonal elimination, respectively. The tridiagonal program includes scalar-interface and20 mutant diagnostics. Raw stdout/stderr, source pins and dates are retained. These counts overlap and must not be summed as independent universal evidence. This was a relevant mathematical replay, **not** a claim to have rerun the complete historical packaging/Monte Carlo/priority wrapper. The tridiagonal output's final hash inventory naturally describes the isolated proof/script subset, not the full historical original directory. No old expected-result or opinion file was copied into the replay tree.

## Final scope and remaining gap

The exact six-rate, all-fixed-positive-load theorem passes this independent adversarial review. There is no identified remaining mathematical gap for Theorem1, Lemmas1–2, the global drift partition, nonexplosion, irreducibility or the continuous-time recurrence conclusion. Full formal verification has not been performed. Mathematical validity does not certify global novelty or resolve the explicitly retained source-access limits. Root scientific clearance and every publication, website, spreadsheet, Git and outreach action remain outside this review. No source repair was made.
