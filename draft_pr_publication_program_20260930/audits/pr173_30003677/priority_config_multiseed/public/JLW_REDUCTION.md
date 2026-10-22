# Post-seal Janson–Luczak–Windridge attack

This supplements the immutable first assessment. A parent message, received only after that seal, specifically requested checking D6 failure, positive infected stub mass, and a positive-recovery limit. It is an attack prompt, not a family verdict or independent evidence. The primary conclusions below were checked from the actual paper.

For a fixed K, put p_d=P(D=d), mu=E[D], and a_K=sum_(d>=K) d p_d>0. Initially susceptible degrees are d<K. The limiting susceptible vertex function is v_S(theta)=sum_(d<K) p_d theta^d and h_S(theta)=sum_(d<K) d p_d theta^d. The initial infected stub mass is a_K. All degree-class choices occur before matching; the paper's deterministic initial lists genuinely allow this degree bias.

Theorem 2.6 is stated with D6, but **Remark 4.2, PDF p.21**, explicitly handles D6 failure when mu_I>0 and gives terminal infection of all but o_P(n) nonisolated susceptible vertices. Thus D6 is not a valid decisive exclusion of this SI case. The immutable first assessment had called this extension unchecked; the later full-body check resolves that access gap.

The finite-time version can be recovered from the proof on pp.18–21. At recovery zero and recovered stub mass zero,

h_I(theta)=mu theta^2-sum_(d<K) d p_d theta^d >= a_K theta^2,

because every susceptible degree is at least two. Accordingly p_I(theta)=h_I(theta)/(mu theta^2)>=a_K/mu on (0,1]. The proof's time change A(tau)=integral_0^tau [beta p_I(exp(-s))]^-1 ds is finite for each finite tau, with A(tau)<=mu tau/(beta a_K). Lemma 3.1 on PDF p.13 applies under D1–D5 without D6. Its convergence on fixed intervals and the inverse-time-change step of pp.18–19 yield fixed-time susceptible convergence. The limiting solution obeys theta'(t)=-beta theta p_I(theta), so theta(t)<=exp(-beta a_K t/mu) and the susceptible fraction tends to zero. This finite-time deduction requires no waiting until a random terminal time.

An alternative uses positive recovery epsilon. D6 then holds. The recovery-dependent infected-half-edge function is

h_I,epsilon(theta)=mu theta^2-sum_(d<K) d p_d theta^d-mu epsilon theta(1-theta)/beta.

On each compact theta interval [delta,1], it tends uniformly to the zero-recovery function, which is bounded below by a_K delta^2. The ODE solution and fixed-time susceptible limit therefore approach the zero-recovery SI solution as epsilon tends to zero, for fixed finite time. Single-type SI contains the set ever infected by that recovering comparison process under common directed contact clocks. This establishes the same one-type approximation route.

However, neither the one-type terminal statement nor its finite-time extension is by itself a lower bound for the weak infection in two-type competition. An adversarial competitor can block a required route on a general graph. One needs a further spatial-localization/protected-route argument, or the general two-color local theorem. The Ganguly–Ramanan reduction in COROLLARY_DERIVATION.md supplies precisely the latter and removes this gap. The JLW result demonstrates older broad initial-stub precedent, but is not being mislabeled as a stated competing-FPP theorem.

Primary source: [Janson–Luczak–Windridge, arXiv:1308.5493](https://arxiv.org/abs/1308.5493), relevant PDF pp.3–7,13,18–21. Publicly provided formulas and deductions here are our own reduction; raw external PDF/text stays private.
