# AIM Problem 29: known Wasserstein generator criteria

**Source assessment, zero substantive author proof-search turns. Independent source-coverage review pending. No new discovery is claimed.**

The proposed disposition is **already solved as an open-ended request for a method of bounding temporal W1 convergence under stated hypotheses**, by the credited generator-coupling results below. This is not a claim that every local generator converges, that the best rate for every model is known, or that every possible Wasserstein/limit interpretation is covered. The independent reviewer must decide whether that disposition matches the actual short source question; if only partial coverage is justified, research remains open with all five author turns available.

## 1. Exact original scope

The original is Problem29, printed p.3 of the AIM problem list *Stochastic Methods for Non-Equilibrium Dynamical Systems*, notes by Ben Webb. The official workshop page dates the meeting June1–5,2015. The source is not titled “A Wasserstein rate dictionary for local-update generators”; that is an imported descriptive title.

The displayed generator is

    L A(x_1,...,x_n) = sum_i integral omega_i(x,dy) [A(y)-A(x)].

The question asks how Wasserstein convergence rates can be bounded when each term involves only finitely many coordinates near i. The stray imported `> i` is a layout extraction artifact; the original has i below the summation sign. The full three-page list and the target page were read, and the target display was inspected visually. The six-page workshop report and surrounding questions do not specify additional assumptions for Problem29.

The original does not name the coordinate state space, the Wasserstein order/ground metric, stationarity or irreducibility, clock normalization, a contraction constant, or a precise limiting parameter. In particular, it does not assert convergence solely from locality. The standard interpretation treated here is temporal convergence in W1 on a specified configuration metric. Infinite-volume limits, numerical discretization error, and Wp for p>1 are not silently inserted into the source request or claimed to follow from the theorem below.

## 2. Directly applicable known theorem

Villemonais, *Lower bound for the coarse Ricci curvature of continuous-time pure jump processes*, arXiv1705.06642v4, Theorem2.1 (p.6) and Corollary2.5 (p.12), gives an explicit bound for state-dependent jump measures. The pinned full primary author version is dated January2019; the later journal publication is J. Theoret. Probab.33(2020),954–991, DOI10.1007/s10959-019-00918-9. Publication metadata is not a claim that an unavailable final PDF was inspected.

Here is its one-state-space formulation. Let (E,d) be a complete separable metric space (Polish) and let J_x be a measurable finite nonnegative jump measure. Suppose the associated process is nonexplosive, integral d(o,z) J_x(dz) is finite for every x and one (hence every) reference point o, and its semigroup preserves P1(E). Write r(x)=J_x(E). For x≠y form two measures with equal mass r(x)+r(y):

    m_(x,y)=J_x+r(y) delta_x,
    n_(x,y)=J_y+r(x) delta_y.

W_d below denotes the optimal d-transport cost for finite measures of equal mass, without probability renormalization. Define

    G_d(x,y)=W_d(m_(x,y),n_(x,y))-[r(x)+r(y)]d(x,y).

If, for some real kappa,

    G_d(x,y) <= -kappa d(x,y)  for every x≠y,          (1)

then the established coupling theorem gives

    W_(1,d)(mu P_t,nu P_t) <= exp(-kappa t) W_(1,d)(mu,nu).

For finite E all measurability, first-moment and nonexplosion issues are automatic. For general Polish E they are assumptions to check, not consequences of finite spatial range. The statement deliberately includes semigroup P1 preservation explicitly, avoiding any reliance on a pointwise jump-moment assumption alone as a substitute for that property.

When kappa>0, completeness of P1(E) and invariance of that space under P_t give a unique stationary probability pi in P1(E), with the same exponential convergence bound to pi. Indeed the contraction mapping theorem gives the unique fixed point of P_(t0) for any fixed t0>0; commutation with every P_s makes this point stationary for the full semigroup. On a finite state space it is simply the unique stationary probability. No uniqueness among arbitrary infinite-first-moment stationary probabilities is claimed for an unbounded metric. If kappa<=0, the bound by itself gives no positive convergence rate.

### Why the augmented measures are the right ones

This is the published coupling construction, restated to make the application checkable. Couple m_(x,y) and n_(x,y) optimally. The added atoms are “false jumps”: a first marginal atom at x contributes zero to f(u)-f(x), and similarly at y. Thus the coupling has the required two marginal generators. Its drift of d is exactly G_d, since the total coupling mass is r(x)+r(y). Dynkin's formula/localization and the stated integrability conditions give the exponential bound. No equality of the original masses r(x) and r(y) is required. Normalizing both measures separately to probabilities before comparing them would lose the rate information and is incorrect here.

This is an existing theorem and its standard explanation, not a new proof-attempt contribution.

## 3. Matching the original local generator, including block updates

For finitely many local terms with finite total rates, take the full configuration as the state in E and set

    J_x(dz)=sum_i omega_i(x,dz).

Then the original displayed generator is exactly the pure-jump generator used above. In this application there is no need to interpret y as a single replacement coordinate: arbitrary local block updates and state-dependent rates are included in J. A chosen finite product of Polish coordinate spaces with a complete compatible product metric supplies a legitimate configuration space. On finite configuration spaces this application has no extra analytic existence issue.

For a more spatially organized sufficient bound, one may couple each pair of local measures separately with their own false jumps and add the coupling operators. If

    sum_i {W_d(omega_i(x,.)+r_i(y)delta_x,
               omega_i(y,.)+r_i(x)delta_y)
             -[r_i(x)+r_i(y)]d(x,y)}
       <= -kappa d(x,y),                                  (2)

where r_i(x)=omega_i(x,E), the same existing coupling criterion applies. This is the finite-sum coupling argument already underlying Villemonais's particle theorem. It is only a sufficient local bound; separate local optimal couplings need not minimize the transport cost of the summed generator.

For actual single-coordinate updates, Villemonais Theorem2.1 additionally gives a more spatially explicit coordinate-summed formula using the coordinate metric and the averaged product distance. That recovers the familiar Dobrushin influence approach without requiring constant update masses. The imported report's constant-rate finite-state matrix formula is a special synthesis of this older coupling methodology, and is not reissued here as a new invention.

Countably many sites with infinite total update rate are a separate infinite-volume interacting-particle construction. They cannot be turned into an N=1 finite-jump-measure process by this argument. The present assessment does not claim that extension.

## 4. Optimality under the graph theorem's hypotheses

Cheng–Li–Wu, arXiv1907.11036v1, Theorems2.2 and2.4, establishes a stronger characterization on its stated class of locally finite connected graphs. The introduction assumes positive jump rates along the graph edges, a conservative process and an invariant probability; its global hypothesis(H) gives the requisite recurrence conditions. Keep these assumptions when using the theorem on countable graphs.

Within that class, a curvature lower bound for the chosen metric is equivalent to the existence of a coupling generator with the corresponding distance-drift bound. Coupling the two augmented jump measures at total mass at least r(x)+r(y) attains the optimal generator drift. Consequently the above criterion computes the best uniform prefactor-one contraction constant for the fixed metric in that setting. It is not a claim to compute the best large-time mixing exponent after allowing an arbitrary prefactor or changing the metric.

The publisher confirms the revised paper appeared as *Ollivier–Ricci curvature and W1-exponential convergence of Markov processes on graphs*, CPAA36(2026),14–54, DOI10.3934/cpaa.2026074. Its abstract confirms the optimal-coupling and false-jump framework. The final full text is access-restricted and its PDF export yielded no content; no alternate access route was attempted after that restriction was confirmed. All detailed theorem numbers and hypotheses in this assessment refer to the openly available **2019v1 full author version**, not a presumed byte-identical final version. The primary Villemonais criterion is sufficient for Sections2–3 independently of this extra optimality statement.

## 5. Scope calibration and coverage decision

Known rate criteria necessarily carry hypotheses: locality allows frozen configurations and arbitrarily slow clock rescaling. For example, a two-state single-site process jumping0→1 at rate a and1→0 at rate b has exact W1 contraction rate a+b for the unit discrete metric. Scaling both rates scales that rate. With a=b=0 there are two stationary point masses and no positive contraction. These elementary calibrations explain why “a positive rate for every local generator” is not a correct replacement for the original methods question.

The source asks how to bound rates, rather than prescribing a conjectured universal exponent. Equations(1)–(2), their explicit hypotheses and the credited transport/coupling construction give an established quantitative method for the displayed finite local-update generator, including the state-dependent/block ambiguity left by the imported partial report. This is the basis for the proposed **already_solved,0/5** source disposition under the temporal-W1 reading.

The qualifications are substantive. There is no supplied exact model from which to calculate a numeric kappa, no guarantee of positivity from locality, and no claim about every possible order of Wasserstein distance, infinite-volume generator or other limiting regime. If those additional targets are judged required by the exact original source rather than possible alternative readings, the proper verdict is partial coverage and the source problem stays active. This classification decision is explicitly left to independent review. No historical priority or novelty assertion accompanies either outcome.

## 6. Reproduction

The finite exact checker verifies the augmented-measure masses, marginal generator identities, monotone-transport primal/dual certificates on three-point line metrics, and the two-state rate normalization. It neither proves the general Polish-space theorem nor verifies arbitrary process existence. Those are audited from the full pinned primary proofs with the assumptions above. All source PDFs, full texts, screenshots and the imported machine report remain reading-only and are not redistributed.
