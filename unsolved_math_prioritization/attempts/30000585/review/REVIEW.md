# Independent source audit: 30000585 / OWR-1327-001

**Verdict: PASS_ALREADY_SOLVED_PREFERRED_DIRECTION_TRANSITION. No mandatory correction.**

The exact original horizontal-force model is covered by the published 2007 fully flexible analysis and the 2009 force-variable formulation. The transition is continuous/second order, with a \(3/2\) singularity in the limiting log-partition free energy on the expanded side. This is a credited known result, not a campaign discovery.

Reviewed snapshot: SHA-256 **f00bddd19c414fa00ffecb2b20ab9edb4c7a1cc5129a707058a84a5bc0794a48**.

All **13,347** submitted exact assertions reproduced byte for byte. A separate standard-library implementation passed **7,495** exact model/normalization controls. These finite checks do not prove a critical exponent; the exponent is an explicitly identified published input.

## 1. The original model is matched exactly

I read Whittington's contribution in [OWR 41/2006](https://publications.mfo.de/bitstream/handle/mfo/2971/OWR_2006_41.pdf?isAllowed=y&sequence=1) and visually inspected printed p.2459. The relevant paragraph defines walks with East, North and South steps, no immediately opposite vertical steps, and a first East step. A contact is a pair of occupied lattice-neighbouring vertices that are not consecutive along the walk.

The force is along the preferred horizontal direction. Its conjugate variable weights the horizontal span, which equals the number of East steps. The displayed generating function tracks contacts, span and total number of edges. The question asks for the transition order in the presence of that force. It is distinct from the preceding adsorption example and from transverse pulling.

The candidate's identification with the 2009 first-East-step model is correct. Setting the vertical force fugacity to one leaves precisely these walks and weights. There is no wall, stiffness energy or unrestricted-walk substitution.

The 2007 vertical-segment representation ends in an East step. This difference is repaired by an exact weighted bijection, not by an asymptotic argument. For vertices \(\gamma_0,\ldots,\gamma_n\),
\[
\eta_i=\gamma_n-\gamma_{n-i}
\]
has increments equal to the original increments in reverse order. It therefore retains the permitted directions, maps first-East to last-East and is its own inverse at the word level. The underlying lattice trace is translated and centrally reflected, so contacts and nonconsecutiveness are preserved. Length and horizontal span are unchanged.

## 2. Published resolution and its precise scope

The complete published [Owczarek–Prellberg 2007 paper](https://webspace.maths.qmul.ac.uk/t.prellberg/papers/pub065.pdf) was available. I checked its model definitions, force weighting, free-energy convention and §3.2, including the rendered p.12. That section treats the fully flexible case \(\sigma=1\), derives the uniform Airy asymptotics and identifies a second-order transition. Its final paragraph explicitly changes to horizontal-force variables and states that the transition's character is unchanged.

The complete published [Brak et al. 2009 paper](https://webspace.maths.qmul.ac.uk/t.prellberg/papers/pub068.pdf) was also available. I checked the first-East model, the thermodynamic-limit/convexity discussion, the horizontal critical curve and §5. In particular, the rendered p.15 shows equation (5.5):
\[
\kappa(f,0,\beta)-\beta
\sim D\,(f-f_c)^{3/2}
\quad\text{as }f\downarrow f_c\text{ from above}.
\]
The paper credits the preceding exact asymptotic analysis. This is a limiting-free-energy assertion; it is not the later conjectured low-temperature finite-size expression.

The source-status package correctly keeps \(\sigma=1\). The 2007 result that positive stiffness can change the transition to first order concerns a different model. Likewise, the 2009 discussion of a force with vertical component contains an explicit “indicates, though does not prove” qualification. That unresolved extension is not the horizontal OWR target.

The full uniform asymptotic machinery is accepted here as a published theorem/input. I have checked its model, statement and application, not independently reconstructed all contour and q-series estimates or the foundational 1995 proof.

## 3. Force variables, physical branch and signs

With contact energy magnitude and lattice spacing normalized to one,
\[
\omega=e^\beta,\qquad h=e^{\beta f}.
\]
The 2007 reduced free energy has the opposite sign to the positive log-partition convention used in the package. The latter is \(\kappa=-\log z_c\). The sign adjustment is correct.

Writing \(a=\sqrt\omega>1\), the physical critical branch is
\[
h_c=\omega\frac{a-1}{a+1},\qquad 0<h_c<\omega.
\]
Substitution gives
\[
\omega(\omega-h_c)^2=(\omega+h_c)^2.
\]
The alternative exponential formula for \(f_c=\beta^{-1}\log h_c\) in the artifact is algebraically identical.

Moreover,
\[
h_c-1=\frac{a^3-a^2-a-1}{a+1}.
\]
The cubic is strictly increasing for \(a>1\), since its derivative is \((3a+1)(a-1)\). Its values at one and two have opposite signs. Hence the stated unique zero-force threshold and its division into positive critical force, zero endpoint and already-expanded tensile regime are correct.

The compact-side value \(\kappa=\beta\) agrees with 2009 equation (5.3). The expanded-side coefficient in the asymptotic is positive: the singular difference is positive there and the asserted asymptotic coefficient is nonzero. The paper separately describes the zero-force critical-temperature endpoint, with extension slope diverging as \(f^{-1/2}\), consistently with the same \(3/2\) free-energy behaviour.

## 4. The thermodynamic interpretation is justified

The candidate does not formally differentiate an arbitrary asymptotic equivalence. Its convex secant argument is valid. For a convex function \(g(\delta)\sim D\delta^{3/2}\), sandwiching its derivative between secants at \(a\delta,\delta,b\delta\), then taking \(a\uparrow1\), \(b\downarrow1\), gives
\[
g'(\delta)\sim(3/2)D\sqrt\delta
\]
where the derivative exists. The source's expanded branch is analytic away from the transition.

The compact-side derivative is zero, so the limiting extension is continuous and tends to zero at the threshold. The \(3/2\) asymptotic precludes a finite second derivative there. This is consistent with the published second-order classification.

For finite \(n\), differentiating \(n^{-1}\log Z_n\) gives \(\beta\) times the expected horizontal span per step. Convexity and pointwise thermodynamic convergence justify convergence of these derivatives wherever the limiting function is differentiable. Thus the stated factor \(\beta^{-1}\) is correct.

The potentially delicate statements following 2009 equations (5.7) and (5.8), involving a surmised discrete finite-size formula and a qualified Darboux step, are not needed for this conclusion. The artifact properly excludes them from its proof of the transition-order interpretation.

## 5. Exact replay and independent controls

The frozen source note, verifier and receipt were copied to author_replay/ and the verifier was rerun there. All 13,347 assertions pass and the receipt is byte-identical.

The independent checker builds 407 walks through length seven by allowed step extensions and counts contacts incrementally from occupied neighbours. It verifies those contacts against a separate column-intersection count, reconstructs the endpoint-reversal coordinates, and checks contact/span preservation. It also checks the no-interaction generating-function recurrence
\[
G=\frac{hz(1+z)}{1-(1+h)z-hz^2},
\]
rational critical-curve identities, the unique zero-force cubic root, exact covariance convexity and the elementary secant factors. All 7,495 assertions pass using only Python's standard library.

Neither bounded enumeration nor these algebraic identities estimate the thermodynamic exponent. Their role is to catch a model or normalization mismatch before applying the published analysis.

## 6. Recommendation

Recommend **already_solved, 0/5**, credited to Owczarek–Prellberg (2007) and Brak et al. (2009), for the exact preferred-direction, fully flexible OWR question. No correction is required.

Preserve the endpoint bijection, opposite free-energy signs, finite-temperature/tensile-force conventions and explicit exclusions of transverse force, stiffness and unrestricted self-avoiding walks. The package should remain a source-status correction with an elementary interpretation, not a new proof of the published asymptotic theorem or a historical-priority claim. This report is independent AI source review, not additional human peer review.

