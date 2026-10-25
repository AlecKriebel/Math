# Independent adversarial review: Zenodo 23592692

**Verdict: PASS at the exact finite-model hypotheses.** I found no substantive mathematical defect or unresolved load-bearing proof gap in *A sharp forest bound and an improved whisker bound for finite WARM graphs*, v1.0.0, 21 October 2026. This is an AI review, not external human peer review, formal proof verification, or priority certification.

## Operative sources and independence

I read all seven published PDF pages, through text extraction, and the complete matching `main.tex`. Main PDF SHA256: `42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157` (91,613 bytes). Source ZIP SHA256: `e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee` (211,840 bytes). Fresh receipt SHA256: `f30b5b667c1794683b0832223046c4e04eab39cca8175e4a69b5cca549aab3f9`. Public metadata SHA256: `d3d7d39facd7a8984640409aba5e4faa22f953901da53c9e8b4a41b7ccb80200`. The embedded main PDF is identical. Both public assets, all 45 extracted members, and ZIP CRCs were independently checked; originals remain unchanged.

Before inspecting packaged helpers, I reconstructed the proof and completed fresh exact controls. I then read and replayed the current helper dependencies in an isolated copy. No current sibling mathematical conclusions or dedicated historical assessment bodies were read. Only raw primary-source paths, versions and hashes were shared by the scope agent.

Incidental exposure is material to disclose: the manuscript's own disclosure describes earlier audits/status labels. File inventory metadata exposes historical filenames. The current verifier calls mathematical code stored under `audit/`; reading that necessary code exposed custody assertions about old inputs, a historical bounded-priority verdict string and several claimed prior-source checks. The prior24 program mechanically parses historical scope/outcome/search JSON and hashes historical reports. I did not open those report/status bodies or use their asserted outcomes to decide correctness or novelty. The independently completed controls and primary readings precede adoption of any packaged numerical results. The old source body's eight artifacts need not supply an unstated proof premise: the operative manuscript contains the complete cycle, whisker, initialization and prior24 derivations.

## Exact supported result

For each fixed finite simple undirected loopless graph, fixed positive vertex firing rates, fixed exponent and fixed **positive integer** initial count vector, independent Poisson clocks select incident edges proportionally to their counts raised to α. Isolated vertices have no effect; the empty-edge case is immediate.

- For **α>4/3**, the infinitely reinforced edges form a forest almost surely, with arbitrary positive rates.
- With **equal rates** and **α≥17/4**, every surviving component has diameter at most three almost surely.
- For each **1<α<4/3**, the unit-start equal-rate triangle has positive probability of retaining all three edges. Therefore no smaller universal forest cutoff works.

The equality case α=4/3 is not decided. The paper does not prove the suggested sharp whisker threshold 4/3, does not claim unequal-rate whiskers, and does not cover infinite graphs, loops, initially zero counts or arbitrary noninteger offsets. Almost-sure quantifiers are for each specified model; no simultaneous event over an uncountable collection of rate/exponent choices is required.

## Stochastic bridge: the essential imported theorem really matches

I inspected the published Hirsch–Holmes–Kleptsyn primary body, *Nonlinearity* 36 (2023), pp.3013–3042: the model and Conditions1/3, Theorem1 on printed p.3016, Proposition1 on p.3021 and its proof, and the complete relevant Section5 proof of Theorem1, including Proposition8. The model starts each count at one, uses the same power reinforcement and positive Poisson rates, and explicitly covers finite graphs with arbitrary positive rates when α>1.

Theorem1 gives almost-sure convergence of N_t/t to a stable or critical equilibrium, meaning its Jacobian has **no strictly positive eigenvalue**; it separately gives positive probability of convergence to a specified strictly linearly stable equilibrium. Proposition1 is stronger than mere divergence: an infinitely reinforced edge has a positive lower asymptotic rate. Under bounded degrees and positive bounded-above firing rates it supplies E_infinity=E_plus almost surely. All these conditions hold for a finite graph after removing isolated vertices. Countably/finitely many edges then permit the simultaneous support identification needed here. Disconnected finite graphs also cause no problem: apply the result componentwise, with independent clocks, and intersect finitely many probability-one events.

The source's convergence proof is not a claim that ODE stability alone proves stochastic convergence. It combines stochastic approximation, an interior convergence argument and a removal/coupling induction; its instability exclusion and stable-point attainment are explicit conclusions of the published theorem. I checked the theorem interfaces rather than re-proving all of its stochastic-approximation background. The 2016 WARM paper's older full-convergence statement was a conjecture; the submission correctly uses the 2023 result for that part. The 2016 published body separately supplies the positive-attainment theorem and triangle/uniform-cycle results, and I read its Theorem1(ii), Section2.1 proof interface, Proposition2(iv),(v), and their proofs. No finite simulation is used as proof of any stochastic conclusion.

The normalization is consistent. With Λ=sum λ_v, p_v=λ_v/Λ and x=a/Λ, F_λ(a)=ΛF_p(x), so the Jacobians agree. Continuous time and embedded-jump normalization differ by the almost-sure Poisson event-rate factor Λ, not by a changed stability threshold. With common rate λ, rescaling time and weights reduces the whisker calculation to rate one.

### Initialization and boundary attack

For a target integer vector n, start from all ones and prescribe exactly n_e−1 reinforcements of each edge, specifying one endpoint's firing each time. The finite event has strictly positive probability because rates and all current counts are positive. At its end, the count vector is exactly n. The strong Markov/memoryless property supplies the future law started at n. Convergence, limit values and infinite reinforcement are unaffected by a finite prefix or finite time shift. Thus a positive-probability failure from n would contradict the unit-start almost-sure theorem. This is the correct direction of conditioning.

That argument does **not** prove positive attainment of each chosen stable equilibrium from every n. The manuscript explicitly avoids that reversal: triangle attainment is used only from unit counts. Noninteger targets cannot in general be reached by this prescription and are excluded.

At a stochastic limit, the incident count sum at vertex v dominates its number of firings. Dividing by time gives sum_(e incident v) a_e≥λ_v>0. Therefore no denominator S_v vanishes, including at boundary equilibria. For α>1, differentiation of a zero coordinate's αth power yields zero, so the full Jacobian splits into the positive-support block and −I on vanished edges, with zero cross blocks. The local C1 extension max(x,0)^α justifies this statement even for noninteger α. A positive eigenvalue on the support therefore remains a positive full-system eigenvalue and is excluded by the stochastic theorem.

## Weighted-cycle mechanism: no hidden uniformity assumption

On the positive face the potential is L(a)=−sum a_e+(1/α)sum λ_v log S_v(a), and F=diag(a)∇L. At equilibrium its gradient vanishes, giving J=diag(a) Hess L. Positive diagonal similarity takes J to a real symmetric matrix. Hence a positive Hessian direction yields a genuinely positive real eigenvalue, even if other directions are critical.

The coordinate change y_e=a_e^α is a local diffeomorphism on this face. At a critical point there is no extra first-derivative term in the Hessian transformation. With b_v=λ_v/S_v, c_v=λ_v/S_v² and D_e=a_e^(1−2α), direct differentiation gives

α² Hess Φ[w,w]=(α−1)Σ_e D_e w_e²−αΣ_v c_v(Σ_(e incident v)w_e)².

The equilibrium relation is a_e^(1−α)=b_u+b_v. For a chosen simple cycle, A_i=a_(e_i)^α, so Σ_cycle D_e=Σ_cycle_vertices b_v(1/A_prev+1/A_next). At a cycle vertex, S_v≥A_prev+A_next, and the positive-variable identity

1/A+1/B−4/(A+B)=(A−B)²/[AB(A+B)]≥0

gives 4Σ_cycle_vertices c_v≤Σ_cycle D_e. Chords and attachments only increase S_v and do not invalidate the inequality. Perturbation coordinates on those extra edges are zero, so their presence does not create an omitted nonzero incidence sum at another vertex.

For an even cycle, the alternating vector cancels every vertex incidence sum. Its positive diagonal term is strictly positive for α>1. This is precisely the classical mechanism credited to HHK Lemma2; positive unequal rate coefficients do not affect cancellation.

For an odd cycle of length m, θ=π−π/m satisfies mθ∈2πZ. The cosine and sine edge vectors are therefore well-defined cyclically. Their edgewise squared norms sum to1, while the sum of their squared neighboring incidence sums is4 sin²(π/(2m)). Adding the two Hessian forms gives at least

[α cos²(π/(2m))−1] Σ_cycle D_e.

Strict positivity implies that at least one of the two real directions is positive. This proves the bound for **every** equilibrium with the cycle in its support, not just a uniform bare cycle. For odd m≥3 its threshold is at most4/3. Every finite nonforest has a simple cycle, proving the deterministic forest exclusion, and the stochastic bridge supplies the almost-sure conclusion.

There is no spurious radial instability: sum F_e=Λ−sum a_e implies 1ᵀJ=−1ᵀ. Every eigenvector with a positive eigenvalue is tangent to the fixed-total simplex. At the unit-weight, unit-rate triangle, the eigenvalues are −1 and3α/4−1 twice. Thus strict stability holds below4/3 and the two transverse eigenvalues are exactly zero at equality. The claimed sharpness is a positive-probability obstruction below the threshold, not a claimed almost-sure cycle outcome and not a decision at the endpoint.

## Whisker proof: closed endpoints and the infinite tail

For equal rates normalized to one, write a=q+r, where q and r are the two endpoint selection probabilities. Both are in(0,1], hence a≤2. The symmetric Jacobian representative is negative semidefinite at a non-unstable equilibrium; its diagonal condition is

q²+r²≥(1−1/α)(q+r).

This is only necessary for stability; the proof never treats it as sufficient. For α>2, a least positive edge in a component cannot have two nonleaf endpoints, because each endpoint would have an at-least-as-large competitor and q,r≤1/2, contradicting that diagonal condition. A leaf contributes one to its edge weight, so every positive edge in that component has weight≥1.

Suppose an internal edge has a∈[1,3/2]. Each endpoint has a competing edge of weight≥1. Therefore q,r≤s_α(a)=a^α/(1+a^α), with q+r=a. For a feasible split, s≥a/2, and convexity of q²+(a−q)² on [a−s,s] gives (q²+r²)/a≤f(a,s)=[s²+(a−s)²]/a. It is increasing in s on this domain.

For 3≤B≤7 and1≤a≤3/2, the claimed bounds 1/2≤s_B(a)/a≤2/3 are valid. The lower bound reduces to a^(B−1)(2−a)≥1, using (a−1)(1+a−a²)≥0. The upper bound follows from R(a)=2a^7−3a^6+2: R′=2a^5(7a−9), and its minimum on a≥0 is R(9/7)=52763/823543>0. If z=s_B/a, differentiation gives

(d/da) f(a,s_B(a))=1−2z²+2(2z−1)s_B′(a)≥1/9.

Thus the maximum needed on any closed exponent interval [A,B] is bounded by f(3/2,S), where S=T/(1+T) and T≥(3/2)^B. I recomputed all five exact caps and margins. They are positive, respectively:

1/1734; 163/65598; 5399/1361250; 74117/6288490; 527104/16077675.

The closed intervals cover [17/4,7] without a gap. The first margin is strictly positive even at α=17/4; the fractional-power caps are certified by raising positive rationals to integer powers. There is no numerical tolerance or omitted endpoint. Since f is strictly below1−1/A≤1−1/α, the diagonal condition is contradicted throughout this range.

For α≥7, set a=1+r0 with0≤r0≤1/2. Convexity with q,r≤1 bounds q²+r² by1+r0², so h(r0)=αr0²−(α−1)r0+1≥0 is necessary. Since h(0)>0 and h(1/2)<0, the admissible r0 lies at or below the smaller root; the larger-root region is outside [0,1/2]. With C=3−√2, the identity C²+C=7(C−1) gives h(C/α)=−(C−1)(1−7/α)≤0 and C/α<1/2. Therefore r0≤C/α, including α=7.

Now a^α≤exp(αr0)≤e^C<6≤α−1. The strict exponential bound follows from the exact Taylor/geometric-tail upper bound exp(8/5)≤510973/103125<6 and C<8/5. Consequently both q,r<(α−1)/α, contradicting their weighted mean (q²+r²)/(q+r)≥(α−1)/α. This proves the entire unbounded tail, not a sampled set of exponents.

Every internal edge therefore has weight>3/2. At either endpoint its selection probability exceeds1/2 because the other endpoint contributes at most one. Two internal edges cannot meet. Cycles would contain adjacent internal edges, as would the middle two edges of any four-edge path. Hence components are trees of diameter≤3. This argument is logically independent of the new odd-cycle theorem. The stochastic bridge and integer-initialization argument then yield the stated almost-sure whisker result.

## Fresh falsification controls and published replay

The pre-helper `independent_controls.py` passed **15,045 explicit exact checks**. The controls supplement the universal proofs above; none substitutes a simulation for stochastic reasoning.

- Forty-five deliberately nonuniform equilibria were built on cycles of lengths3–11, adding chords and multiple attachments. For α=2 choose positive rational b_v, a_uv=1/(b_u+b_v), and λ_v=b_vΣ_(e incident v)a_e². This makes the equilibrium exact rather than an approximate solver output. Direct Jacobians, Hessian congruence, column sums−1 and weighted-cycle inequalities were checked. Each case has a stored **rational vector with strictly positive exact Hessian energy**. Trigonometric approximations only choose candidate vectors; Fraction arithmetic certifies their final energies.
- Exact triangle eigenvectors check exponents5/4,4/3,17/12 and17/4. The equality case is critical, detecting a false strict-stability claim at4/3.
- An additional exact unequal-rate path with four edges, α=5 and weights(1,10,100,1000), has positive rates and a negative-definite Hessian certified by four positive leading principal minors of its negative. The full rational data are saved. By the imported attainment theorem it supplies a valid positive-probability non-whisker example when rates are unequal. It is a boundary-of-scope control, **not** a defect in this paper's equal-rate assertion.
- All closed-interval rational caps, positive margins, tail identities in Q(√2), and Taylor bounds were recomputed. The current first-interval certificate fails when its lower endpoint is falsely changed to4; that does not assert the whisker theorem itself is false at4.
- All33,867 labelled simple graphs on one through six vertices were enumerated. The1,771 with matching internal edges all have tree components of diameter≤3. This is a finite corroboration of the graph argument, not evidence extrapolated to all graph sizes.
- A concrete finite unit-to-(3,2,4) count prescription has exact positive probability50421/22333829939200. The general initialization conclusion still rests on the Markov argument, not this example.

Afterward I read the current runner, forest mathematical dependency, whisker verifier, and prior24 mathematical/custody dependency. The unmodified runner in a disposable copy passed all **nine suite/mode combinations**: forest, whisker and prior24, each in normal, `-O` and `-OO` Python. Every mode rejected the six forest and seven whisker internal false alternatives. A separate deliberately false external manifest anchor was rejected. Source-copy and original bytes stayed unchanged. The prior24 suite also authenticates historical assertions; its successful execution is not a fresh priority certification. Historical custody programs that require private captures were not run, and no such run is claimed. The temporary copy was removed after preserving complete stdout/stderr and execution receipts.

## Primary credit and exact remaining limits

Four fresh primary PDFs and text extracts are hash-bound in `primary-source-checks.json`, with precise read ranges. The original OWR contribution on printed pp.653–655 distinguishes the improvement requests (>2 and>25) from the suggested sharp4/3 threshold. VHHKR already provides the uniform odd-cycle and triangle thresholds. HHK already provides the stochastic convergence/support bridge and even-cycle method. HK already provides the least-weight/champion mechanism and the unequal-rate warning.

I checked the manuscript's separate prior24 comparison directly against HK Section5.1, Lemmas5–8 and their proofs. The displayed2.25 constants give the small/large weight split for α>81/4. The small-edge contradiction needs α>(9/4)(e^(9/4)+1); the exact exponential bound implies this is below189/8<24. At α>24, large weights exceed29/16>3/2. Thus the stated prior-method improvement is supported, and the paper does not misrepresent17/4 as the first possible numerical improvement of25.

No unresolved central proof gap was found. The underlying published stochastic-approximation theorems are accepted at their explicitly checked primary interfaces; this review is not a recursive recertification of all background results. Novelty and exhaustive priority remain uncertified. The stochastic endpoint4/3 and the sharper equal-rate whisker interval remain open **within this paper**. The final disposition is PASS for the exact finite stochastic model and parameter ranges above. No source repair, site/Sheet modification, Git operation, publication, deployment, UI action or outreach occurred.
