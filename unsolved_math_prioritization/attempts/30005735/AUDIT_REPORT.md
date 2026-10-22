# Publication context for the independent traffic audit

The mathematical audit below is preserved byte-for-byte after this preamble. It describes the earlier independent audit. In particular, original-output replay, float-contamination findings, optimization-disabled asserts, 39 historical audit runs, source PDF comparisons, and preservation of the original inputs are historical observations. The superseded full report, original checker, and original outputs are not in this portable delivery. Their replay is NOT_RUN here. CORRECTIONS.patch records authored historical changes; applying it to the excluded original is NOT_RUN. Links to corrected_packet/ and REPRODUCIBILITY.json in the historical text refer to that earlier layout; the corrected report and both accepted checkers are at this directory's top level, and current portable evidence is described in VERIFICATION.md.

Current fresh checks authenticate and rerun only the corrected check_calculations.py, independent audit_exact.py, and semantic guard_checks.py. Historical checks and current fresh checks are separate evidence. Source retrieval and manuscript-status review were not repeated for this packaging step.

---

# Independent mathematical and reproducibility audit: traffic BV target 30005735

Date: 2026-10-08. Disposition: **accept the corrected packet as five scoped partial results, not a solution of the general switching BV problem.** The five-approach budget is exhausted; this audit introduces no sixth approach and makes no originality claim.

The complete submitted report was read. Its input SHA-256 was `888c86d7905aed25237faa101626fb44219276d2eb83726f3b4fc91ef605cb89`. Original files were preserved. This document supplies the independent reasoning and the limits of acceptance; `CORRECTIONS.patch` and `corrected_packet/` contain proposed corrections separately.

## 1. Required corrections and their severity

1. **Source bridge:** after equation (7), jump endpoint conditions alone do not characterize the piecewise-C1 memory equation. Fan–Shu's Theorem 3.2 also requires the corresponding conditions where the ordinary time derivative of memory is positive or negative. The corrected wording supplies both smooth-part conditions and retains feasibility. A continuous, nonconstant memory path in the strict scanning interior has no temporal jumps, hence vacuously satisfies (7), while violating the memory law. Thus the omitted qualification matters.
2. **Arithmetic claim:** in the original calculation script, `f(2)` evaluates an integer division using `/` and is a float. Subtracting it from a Fraction contaminates every flat-scanning velocity increment, speed and L1 total. The original JSON's decimal strings expose this. The corrected function coerces its argument to Fraction before arithmetic.
3. **Verification integrity:** every original check is an `assert`; Python optimization removes them. A semantic mutation doubling the transmitted H value fails normally but reports success under both `-O` and `-OO`. The proposed replacement uses explicit runtime checks and rejects the same mutation in all modes.
4. **Accurate computation labels:** the square-root rows in the small calculation script remain numerical illustrations, now labeled as such. Exact root brackets and exact flat-scanning calculations are distinguished. The separate independent verifier uses only rational arithmetic, including exact brackets for irrational roots. Neither program proves the analytic compactness or entropy assertions.
5. **Precision and presentation:** make boundary regularity explicit for the common entropy pair, spell out moving scanning-shock profile admissibility in the restricted theorem, restrict the countable glued construction to its proved interval `0<t<=1`, and repair two malformed source hyperlinks. These clarify already intended scopes rather than enlarging results.

No incorrect displayed H formula, Rankine–Hugoniot speed, BV sum, viscosity choice, or substantive general-resolution claim was found in the submitted report.

## 2. Source restoration and compatibility

### 2.1 Controlling question and prior results

The controlling OWR contribution occupies printed pages 2968–2969 and asks separately about rational Riemann selection and general BV initial data, possibly small. It gives no smallness norm or uniform hyperbolicity requirement. Equation (9) is correctly labeled as the authors' proposed test formulation. [Official report](https://ems.press/content/serial-article-files/48173).

The HARZ paper's statements, coefficient page and profile equations were checked against the author PDF and publisher. Its viscosity differentiates velocity, unlike the spacing diffusion used in the 2019 HLWR paper. HARZ Assumption 2 prints positive scanning memory derivative and increasing endpoint maps; Assumption 3 strengthens the scanning slope and imposes concavity. Theorem 1 presupposes regular viscous solutions; Remark 2 labels the velocity-TVD argument formal. Theorem 5 and Remarks 5–6 state the monotone-velocity Riemann selection. This audit verifies attribution, not every proof in that source. [Publisher](https://onlinelibrary.wiley.com/doi/full/10.1111/sapm.12769), [author PDF](https://sfera.unife.it/retrieve/502a3b8a-a6fc-417a-814c-544d928b2ed1/2024_Corli-Fan-SAM.pdf).

The HLWR profile equation is `B(u)u'=-s(u-u_-)-(V-V_-)`. At speed zero its memory equation is identically satisfied; Theorem 4.2 allows a velocity excursion inside a stationary profile. The base scanning slope permits zero. These facts were checked in sections 3–4. [Author preprint](https://iris.unife.it/retrieve/e309ade4-5dc1-3969-e053-3a05fe0a2c94/Corli-Fan_M3AS.pdf).

Fan–Shu's Definitions 3.1–3.2 and Theorem 3.2 were read, including both jump and ordinary derivative clauses. Theorem 6.1 explicitly assumes that the limit is piecewise C1. Its theorem cannot be quoted as an unrestricted BV closure theorem. [Author manuscript](https://par.nsf.gov/servlets/purl/10226107).

The publisher-indexed abstract for Fan's 2024 paper concerns a two-parameter hysteretic flux and describes front-tracking compactness. Direct full-text retrieval was unavailable in this audit; no full proof comparison is certified. [Publisher-indexed record](https://www.sciencedirect.com/science/article/abs/pii/S0022039624001013). Goatin–Moreti's 2026 article treats `u_t+w_t+f(u)_x=0` with a Play relation and was published on 26 September 2026. Its equation and scope differ from the traffic system. [Publisher article](https://link.springer.com/article/10.1007/s00030-026-01271-7). These checks support the packet's modest statement that no exact full-target resolution was established by its checks; they are not an exhaustive absence-of-literature certificate.

All four locally available PDF hashes and byte counts match `SOURCE_VERIFICATION.json`. Source bodies are not copied into this audit deliverable.

### 2.2 Signs and the conditional free-zone conflict

At fixed w, let `a=h^A(u,w)` and `d=h^D(u,w)` both lie in the represented memory interval. Since `u^D<=u^A` and both endpoint maps increase, `a<=d`. Every intermediate memory value is feasible at this fixed u. Endpoint matching and the fundamental theorem of calculus then give

\[
v^D(u,w)-v^A(u,w)=\int_a^d v^S_h(u,w,r)\,dr\ge0.
\]

If `a<d` and the printed memory derivative is positive, the inequality is strict. Therefore a fully represented section with `v^A>v^D` conflicts with these signs. When the critical memory is interior and both endpoint maps have positive derivative, their inverse functions exist on a common neighborhood of the critical spacing, giving the stated nearby free-zone conflict.

This reasoning is conditional on endpoint representation. It does not prove incompatibility for a congested-only local chart, a truncated chart lacking both endpoints, or every intended traffic parameterization. The packet correctly avoids a vacuous existence conclusion, a silent global sign change, and conversion of a coherent local example into a complete source-level counterexample.

The material derivative correction in Eulerian variables is also correct: a Lagrangian time derivative becomes `D_t=partial_t+V partial_x`. This is an explicitly identified correction of notation, not a faithful transcription of the source's Eulerian indicator formula.

## 3. Restricted common-scanning construction: accepted

The hypotheses must mean that `z_0(x)` takes values in Z; the proof uses the inverse map on the entire common velocity band and a positive distance from both switching boundaries. No activation is allowed. Compactness of K makes the derivative and inverse-map bounds uniform.

For a cell, write the update as `T_j(r,c)=r+lambda(c-V(r,z_j))`. Its derivative in r is `1-lambda V_u>=0`; comparison with the two inverse-band endpoints proves invariance. The mean-value formula then supplies `0<=a_j<=1`. The difference identity

\[
d_j^{n+1}=(1-a_j^n)d_j^n+a_{j+1}^n d_{j+1}^n
\]

has the stated indexing. Summing absolute values gives exact velocity TVD: each old difference receives total coefficient one after reindexing. It is important that this is the velocity variation, not directly the spacing variation. The Lipschitz inverse supplies the latter with the factor `m^-1` and the frozen-parameter variation.

The time estimate follows directly from the conservative update. Combining spatial BV, bounded values and local L1 time translation control yields compactness on bounded space-time cylinders, followed by a diagonal subsequence. Approximation of both initial components gives the initial trace; summation by parts identifies the scalar equation. Uniform estimates pass by lower semicontinuity. No global L1 compactness of a nonintegrable background is being asserted.

For entropy, the sequence `k_j=G(c,z_j)` is exactly stationary. Applying the monotone update to coordinatewise maxima and minima yields equation (15), including its flux sign. Strong local convergence permits passage to (16); the frozen coefficients and comparison states converge as well. This supplies adapted scalar entropy inequalities, not a new entropy for switching modes.

For a nonstationary jump, the frozen components have no jump across it. At fixed z, `-V` is strictly convex. Its entropy shocks have `u_->u_+`. If ell is the chord of V, then `ell-V<0` between these endpoints and

\[
B V_u u'=\ell-V.
\]

The coefficient is positive and the endpoint zeros are simple. The scalar autonomous equation therefore has the required decreasing heteroclinic with the correct limits. For a stationary jump, the conservative equation forces equal velocities. Convexity of Z allows a connecting parameter path; applying G gives a constant-velocity scanning path. HARZ velocity diffusion vanishes identically on that path. These are wavewise admissibility statements; no assertion that the entire BV solution is already the limit of globally constructed viscous solutions is needed.

The theorem is a valid conventional conditional construction. It does not treat data near a switching boundary without a common scanning band, nor degenerate scanning slopes. It proves no uniqueness claim beyond what is stated.

## 4. Switching contact and closure obstruction: accepted

### 4.1 Exact contact interaction

For the local constitutive law in (18)–(19), the acceleration boundary at marker w=3 is `h=u-3`. The rarefaction's transmitted endpoint therefore satisfies

\[
\alpha=f(3+H)+H-3=2H-H^2/4.
\]

The small positive root is exactly `H=4-2 sqrt(4-alpha)`. Rationalization gives `2alpha/(2+sqrt(4-alpha))`, hence `alpha/2<H<alpha`. The series coefficient `alpha^2/32` is correct; substituting its quadratic truncation gives residual `-alpha^3/128-alpha^4/4096`.

On the right, `f(r)=3+alpha` gives the small root `r=5-2sqrt(1-alpha)`. The bound `alpha<delta-delta^2/4` is precisely what keeps r below the right acceleration boundary. Thus the incoming wave is a scanning rarefaction, and the transmitted wave is an acceleration rarefaction. It would be incorrect to replace this increasing fan by one entropy shock. The final contact states and velocities match exactly.

For `alpha=delta/2`, the new memory-contact strength satisfies `H/(alpha delta)>1/(2delta)`. All states approach the same boundary state as delta tends to zero. This disproves a uniform bound with the displayed product of incoming velocity strength and marker jump in these coordinates. It does not disprove every possible quadratic estimate in other coordinates or every switching-aware interaction functional.

The velocity-TVD statement for a finite configuration uses only velocity monotonicity of each replacement fan and the triangle inequality. It does not supply the existence of that front construction for all times or a full-state BV bound.

### 4.2 Thin-pulse quantifiers

Take positive t0 and n large enough that the pulse support lies at positive times. On the rising half, h follows the lower endpoint. On the falling half, the upper endpoint remains at least one, so `0<e<1` makes the final memory stay e. Consequently the claimed variations and local L1 limits hold.

The limit has a positive temporal memory jump whose final value is not the acceleration endpoint at the constant limiting input. It violates the intended monotone-jump constitutive graph. The counterexample concerns strong L1 convergence with bounded variation, not strict BV convergence or graph convergence retaining excursions. Its input is not uniformly Lipschitz in time.

It is not a sequence of conservative PDE solutions. A vanishing distributional residual for the spatially homogeneous input is much weaker than satisfying the actual numerical or viscous scheme. The packet makes that distinction correctly. No general PDE nonexistence conclusion is accepted.

## 5. Common convex entropy obstruction: accepted with boundary regularity explicit

Assume the pair is C2 up to the two boundaries and has a common flux. In an interior scanning neighborhood, arbitrary signs of the smooth gradients are allowed. Thus the entropy inequality for every smooth scanning solution forces both coefficient identities in (27), not merely an inequality for a favored class of gradients.

Taking mixed derivatives cancels the terms involving `V_uh` and yields

\[
V_u\eta_{uh}=V_h\eta_{uu}.
\]

For positive `V_u,V_h` and strictly positive `eta_uu`, `eta_uh>0`. Continuity carries the flux identities to the boundaries. Matching there gives `v^B_u=V_u+V_h(h^B)_u`. Along a smooth active branch the entropy production reduces to `eta_h h_t`. Acceleration admits positive `h_t`, forcing `eta_h(A)<=0`; deceleration admits negative `h_t`, forcing `eta_h(D)>=0`.

At fixed h, however, integration of the strictly positive mixed derivative across the nonzero spacing gap gives `eta_h(A)>eta_h(D)`. This is incompatible with those boundary inequalities. The argument is valid for the announced local class, and in fact needs only strict convexity in u, not full positive definiteness of the Hessian.

It does not exclude entropies lacking this boundary regularity, separate mode-dependent entropy fluxes, nonsmooth or history-dependent dissipation, or a different compactness mechanism.

## 6. Flat-scanning waves and countable amplification: accepted locally

### 6.1 Moving profiles and the exact glued solution

With `f(r)=r-r^2/20`, all relevant boundary slopes are positive and boundary second derivatives are negative. The scanning derivative in u is zero. The velocity increment is exactly `Delta v=4e/5-e^2/20`.

For the increasing edge, the spacing jump is `1/2+e`; for the decreasing edge it is `-1/2`. The stated speeds solve `s[u]+[V]=0`, have the correct negative direction, and satisfy `-1/4<s_down<s_up<0`.

On the first shock's horizontal scanning segment the chord is strictly above the path. On its acceleration segment, the chord slope is less than the minimum boundary derivative, so the positive gap decreases to zero only at the endpoint. For the second shock, put `u=2+r` on its deceleration part. The path-minus-chord gap is

\[
r\{4/5-r/20-2\Delta v\}>0\quad(0<r\le e).
\]

The horizontal part has the same strict chord-below orientation. Thus the scalar profile ODE has the proper sign throughout both moving waves. The switching paths end at the appropriate new boundary, as required by the memory rule.

For a pulse on `[a,b]=[3n,3n+1]` and `0<t<=1`, the successive states are background, high-spacing state on `(a+s_up t,a)`, original pulse on `(a,b+s_down t)`, low-spacing state on `(b+s_down t,b)`, and background. No intervals overlap. This explicitly realizes the claimed four-wave local pattern.

### 6.2 Stationary contacts for spacing diffusion

A constant-velocity nonconstant spacing profile cannot solve the stationary HLWR equation: with B=1 it would give `u'=0`. The correction using a small velocity excursion is valid, and can be made fully explicit.

For the high-spacing contact put `u_L=3+e`, `u_R=5/2`, `L=u_L-u_R`, `h_0=2+e`, and choose `kappa=1/8`. Define

\[
u(\xi)=u_R+\frac{L}{1+\exp(\kappa L\xi)},\qquad
u'=-\kappa(u_L-u)(u-u_R),\qquad
h=f^{-1}(f(h_0)-u').
\]

Here the inverse uses the increasing branch near h=2. For finite xi, `h>h_0>u-1`. Also `|u'|<=kappa L^2/4`, and `L<=33/64`; this excursion is smaller than `f(5/2)-f(2+e)`, so `h<5/2<u`. Both limits are correct, and derivatives tend to zero at infinity.

For the low-spacing contact take `u_L=2`, `u_R=5/2`, `L=1/2`, `h_0=2` and

\[
u(\xi)=u_L+\frac{L}{1+\exp(-\kappa L\xi)},\qquad
u'=\kappa(u-u_L)(u_R-u),\qquad
h=f^{-1}(f(2)-u').
\]

Now `h<2<u` and `u-1<3/2<h`, since `u'<=1/128<f(2)-f(3/2)`. At the limiting left state the expected boundary equality is restored. Both profiles solve `u'=v_0-f(h)` exactly and are stationary; hence the memory time derivative is zero. This proves existence of the claimed local stationary profiles, rather than merely checking the sign at a sample point.

It does not construct one global viscous approximation of the entire countable pattern. Acceptance is of the explicitly glued inviscid rational waves and their individual profile admissibility.

### 6.3 BV and L1 quantifiers

The high and low spacing rectangles contribute L1 changes `t Delta v` each and variations `1+2e` and `1`, respectively. Hence equations (35)–(36) are exact.

For `e_n=2^{-n-6}`, finite pulse families have initial memory TV strictly below `1/16` and spacing TV `2N+2 sum e_n` at each `0<t<=1`. The countable locally finite family has initial TV exactly `1/16`, not strictly less, and infinite global spacing TV at every time in that interval. Its L1 spacing change is finite:

\[
2t\sum_{n\ge0}\Delta v_n
=2t\left(\frac45\frac1{32}-\frac1{20}\frac1{3072}\right)
=\frac{307}{6144}t.
\]

The sum of memory-pulse areas is finite too. Multiplying all amplitudes by a positive scale makes both the initial sup norm and variation arbitrarily small. The order-one spacing height persists while its support widths shrink; this is compatible with the L1 initial trace.

This proves nonuniform full-state BV propagation for the specified rational solution in the local flat-scanning model. It does not prove that all weak solutions fail to be BV, does not supply a globally crossing traffic constitutive law, and does not refute the compact-patch positive-slope problem. No claim for all later times after interactions is accepted.

## 7. Reproducibility and acceptance boundary

The original recorded output reproduces byte-for-byte. Its success label is nevertheless too strong for the reasons in section 1.

The independent verifier covers discrete scanning algebra, exact transmitted-root brackets, the projection pulse, an entropy sign certificate, shock speeds and chord certificates, finite and countable sums, and exact stationary profile-equation values. Analytic proofs are the arguments above, not outputs of a finite sample program.

A total of 39 runs were performed under Python 3.12.14 as UID/EUID 1000. Inputs and current working directory were verified nonwritable to that user; the complete input tree was unchanged. Normal, `-O` and `-OO` modes were tested. The independent verifier passed in all three modes. Each of eight semantic mutations failed in every mode: reversed upwinding, wrong transmitted-root polynomial, loss of right-state scanning feasibility, erased pulse memory, reversed entropy mixed-derivative sign, wrong increasing-shock direction, wrong decreasing-shock speed, and wrong stationary-contact excursion sign. The corrected small script also rejects its incorrect-H mutation in every mode. See `REPRODUCIBILITY.json` for exact outcomes.

**Final acceptance:** the corrected report is an accurate bounded partial-results packet. It supplies neither a global switching BV construction nor source-compatible closure through arbitrary BV limits. The unresolved points are full-state estimates, existence/continuation of approximants, and closure/admissibility of the memory law through all relevant singular parts. Keep the target at five exhausted approaches with the general switching problem unresolved. No full-resolution, nonexistence-for-all-solutions, or novelty claim is justified.
