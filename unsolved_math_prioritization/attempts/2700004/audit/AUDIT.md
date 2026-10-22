# Independent audit: AMR-026-0004

## Disposition

**PASS, with an essential scope qualification.** The frozen packet proves a literature-known affirmative answer to the literal existential question for the unrestricted, non-isentropic full Euler system. It does not prove an isentropic, bounded-specific-entropy, near-constant-entropy Sobolev, or compact-support result.

The appropriate catalogue disposition is **already_solved, 1/5**, provided its accompanying explanation explicitly says:

> Literature-known unrestricted non-isentropic full-Euler example; specific entropy is spatially unbounded. No novelty claim or resolution of the narrower variants.

An unqualified assertion that every intended version of Serre's problem is settled is **not approved**. If the target is subsequently specified to require one of the excluded hypotheses, this disposition must become a scope-qualified partial result or source hold. The positive scope adjudication here is an interpretation of the explicit mathematical statement, not a claim that the original author's intended function space has been confirmed personally.

## 1. Frozen object and reproducibility

The reviewed object consists of nine author files, including a manifest whose SHA-256 is

`630d9dd1a379f0d40be98e193d4bfe8caaa1a9a3697dc961720202685d0b1e2a`.

Every filename, byte count, and content hash agrees with that manifest. The author files were not changed. The verification script was copied into an isolated replay directory before execution, because it writes its result next to itself. Its **60 exact controls pass**, and the output is byte-for-byte identical to the frozen `checks.json` under SymPy 1.14.0.

A separately written script gives **20 additional exact controls**, including all three conservative momentum components, conservative total energy for arbitrary gamma in dimension three, Gaussian integrals, and agreement with the published mass/energy normalization. These computations support, but do not replace, the following analytic audit.

## 2. Source-scope ruling

The full [2012/2013 question](https://perso.ens-lyon.fr/denis.serre/DPF/Ouverts.pdf), Section 4, pp.9–10 (journal pp.204–205), explicitly admits the isentropic and non-isentropic laws. Its all-time classical-solution question imposes finite nonzero mass and energy. A bounded fluid domain appears as an example, not a required hypothesis.

I checked the possible contrary reading: the journal's p.197 uses H^s to describe smooth initial data for a Navier–Stokes–Fourier local theory; p.204 describes small Sobolev perturbations of constant entropy and affine velocity. Neither passage supplies an explicit additional assumption in Question 4. The latter's motivating theorem cannot be a requirement to put the raw velocity in H^s, since affine velocities are expressly allowed. No source-wide definition requiring bounded specific entropy or temperature decay is stated. Nevertheless, those surrounding theories and the subsequent boundary heuristic motivate a narrower interpretation, which this example does not answer. This distinction must remain visible. [Journal version](https://intlpress.com/site/pub/files/_fulltext/journals/maa/2013/0020/0002/MAA-2013-0020-0002-a006.pdf).

The underlying [1997 theorem](https://www.numdam.org/article/AIF_1997__47_1_139_0.pdf), introduction and Theorem 3.1, was also checked. Its smallness hypotheses apply to density variables, velocity relative to an affine field, and entropy relative to a constant. They are sufficient hypotheses for that theorem. They do not establish a necessity theorem for every classical solution of the Euler conservation laws. This Gaussian lies outside that theorem's entropy class.

The selected catalogue statement is an existential question without the extra restrictions. A single valid non-isentropic example in dimension three answers that statement. The generated report's insertion of “isentropic” cannot remove a branch expressly admitted by the primary question. This audit does not use the generated report as mathematical or historical authority.

## 3. Direct full-Euler verification

Write alpha = 1+t^2. For C>0, dimension d, and gamma=1+2/d, the fields are

\[
\rho=C\alpha^{-d/2}e^{-|x|^2/(2\alpha)},\quad
u=\frac{t}{\alpha}x,\quad
e=\frac{d}{2\alpha},\quad p=\frac{\rho}{\alpha}.
\]

The pressure satisfies exactly p=(gamma−1)rho e. In gas-constant-one units the temperature is T=1/alpha, the specific heat is c_v=d/2, and e=c_v T. Pressure, temperature, density, and specific internal energy are positive at every finite spacetime point. This is a calorically perfect ideal gas with the monatomic exponent, not an arbitrary pressure chosen without a compatible energy law.

Let h=t/alpha and D=partial_t+u·grad. Direct differentiation gives

\[
\operatorname{div}u=dh,\qquad
D\log\rho=-dh,\qquad
Du=(h'+h^2)x=\alpha^{-2}x,
\]

\[
-\rho^{-1}\nabla p=\alpha^{-2}x,\qquad
De=-dt\alpha^{-2},\qquad
(\gamma-1)e\operatorname{div}u=dt\alpha^{-2}.
\]

Thus continuity, material momentum, and internal energy all hold pointwise. Since density is positive, multiplying the material momentum equation by rho and using continuity gives conservative momentum. Its scalar product with u gives the kinetic-energy balance. Adding rho times the internal-energy equation and using div(pu)=u·grad p+p div u gives

\[
\partial_t\left[\rho(e+|u|^2/2)\right]
+\operatorname{div}\left(\left[\rho(e+|u|^2/2)+p\right]u\right)=0.
\]

No dissipative, isothermal, forced, or pressureless replacement system has been substituted. The energy equation is the full conservative one.

Because alpha is positive on the entire real line, these formulas are C-infinity on all finite spacetime points. Gaussian-times-polynomial conserved densities and fluxes have rapidly decaying spatial tails, uniformly on compact time intervals. Thus the local equations also give classical distributional solutions globally, with no hidden boundary source.

## 4. Integrals, entropy, and complete flow

The change of variables x=sqrt(alpha)y yields

\[
M=C(2\pi)^{d/2},\qquad
\int |x|^2\rho\,dx=d\alpha M.
\]

Consequently kinetic energy is dMt^2/(2alpha), internal energy is dM/(2alpha), and their sum is E=dM/2. Both mass and energy are strictly positive, finite, and constant for every real t. These are direct integral evaluations, not formal conservation assertions that leave flux limits unproved. In dimension three the prior-source energy agrees with 3M/2. Its mass formula likewise agrees with C(2pi)^(3/2); no factor of two or temperature/internal-energy normalization discrepancy is present.

The dimensionless specific entropy is

\[
S=\log(p/\rho^\gamma)
=(1-\gamma)\log C+\frac{\gamma-1}{2\alpha}|x|^2.
\]

The time-only term cancels precisely because d(gamma−1)=2. The physical entropy is c_v S plus a constant. Since D(|x|^2/alpha)=0, DS=0, and the conservative entropy equation follows. The total absolute entropy weighted by rho is finite. For C=1 its dimensionless value is M. This finite integral does **not** make S bounded: at every fixed time S grows quadratically, and grad S grows linearly. No additive entropy normalization fixes this.

The velocity is spatially affine; it is unbounded for nonzero t, although its spatial gradient is bounded. Specific internal energy and temperature are spatially constant and do not tend to zero at infinity. Density and conservative energy density do tend to zero. These distinctions are genuine and preclude any claim of a decaying raw state vector or bounded-entropy Sobolev perturbation.

The particle map between finite times s,t is

\[
\Phi_{t,s}(x)=\sqrt{\frac{1+t^2}{1+s^2}}\,x.
\]

Its derivative in t equals u(t,Phi), its determinant is positive, and it has the inverse Phi_{s,t}. Every trajectory exists at every real time. The gas contracts to a finite-width minimum at t=0 and then expands; it does not collapse or reverse orientation. Its support is all of Euclidean space, so there is no finite vacuum boundary on which the compact-front parity argument could act.

It is not an isentropic solution: p/rho^gamma varies with x. The exact negative-control residual is 1/6 at t=0, |x|^2=3 log 2 for d=3, C=1 after substituting the pressure rho^(5/3). This prevents mislabeling the validated full-Euler solution.

## 5. Independent kinetic mechanism and prior art

The distribution

\[
f=C(2\pi)^{-d/2}\exp\{-\tfrac12(|x-tv|^2+|v|^2)\}
\]

solves free transport. Completing its square in v gives a Maxwellian with the asserted rho, mean u, and temperature T. Gaussian velocity integration yields isotropic stress rho T I and zero centered heat flux, so its mass, momentum, and energy moments close as full Euler with e=dT/2. Differentiation under velocity integrals is justified by Gaussian bounds on compact spacetime sets. There is no weak-regularity or formal hydrodynamic-limit step in this construction.

[Fellner–Schmeiser, 2007](https://homepage.univie.ac.at/christian.schmeiser/Euler.pdf), Section 1, pp.2–4, supplies this moment closure; Section 5, pp.11–12, gives the finite-mass/energy family, alpha=1+t^2, and the exponential profile. Setting its rotation parameter to zero and taking phi(g)=C exp(−g) gives exactly the fields audited here. The source explicitly distinguishes its entropy profiles from Serre's near-constant-entropy construction. Its remarks about compactly supported profiles failing a different regularity class do not turn the positive Gaussian into a nonsmooth finite-spacetime field. The attribution is direct and precedes the 2012 question. No new-discovery claim is justified. [Publication DOI](https://doi.org/10.1007/s10955-007-9396-8).

## 6. Arbitrary-gamma extension

The extension is analytically valid for every d≥1 and gamma>1. Set q=d(gamma−1)>0 and solve

\[
a''=\theta_0 a^{-q-1},\quad a(0)=1,\quad a'(0)=0,
\quad \theta_0>0.
\]

The first integral is (a')^2/2+theta_0 a^(−q)/q=theta_0/q. On a maximal positive-domain solution it implies a≥1 and |a'|≤sqrt(2theta_0/q). Over any finite time interval, a also has a finite upper bound. Thus (a,a') stays in a compact subset of the smooth ODE domain; it cannot reach either a=0 or infinity in finite time. Continuation works at both endpoints. Uniqueness gives time symmetry. This argument is not a numerical extrapolation from positive times.

For rho=C a^(−d)exp(−|x|^2/(2a^2)), u=(a'/a)x, p=theta_0 a^(−q)rho, and e=theta_0 a^(−q)/(gamma−1), the conservative equations follow as above. The mass is M, and

\[
E=\frac{dM}{2}(a')^2+\frac{M\theta_0}{\gamma-1}a^{-q}
=\frac{M\theta_0}{\gamma-1}.
\]

Its entropy has the same quadratic spatial term and is transported by the complete scaling flow x↦a(t)x/a(s). Positive constant heat capacity c_v=1/(gamma−1) gives a compatible calorically perfect gas in the same units. This mathematical ideal-gas extension asserts no molecular interpretation of every arbitrary gamma. The d=3, gamma=5/3 example alone already answers the odd-dimensional existential statement. Prior-art attribution is limited to the explicitly inspected monatomic family; the extension is not claimed as new.

## 7. Later nonexistence theorem

[Serre, *Expansion of a compressible gas in vacuum*](https://arxiv.org/abs/1504.01580), Section 1 and Sections 2.1–2.2, works with an isentropic gas occupying a bounded domain. The inspected Theorem 2.5 requires a compact initial sound-speed support with smooth boundary, all-time C^1 regularity of sound speed and velocity, odd d, and the printed restriction gamma≤1+1/(d−1). Its proof uses a nonaccelerated front, polynomial support volume, parity, and a dispersive estimate. The Gaussian meets neither the isentropic nor the compact-front assumptions. Moreover, gamma=5/3 is outside that printed restriction at d=3. None of these observations promotes the theorem to a broader nonexistence result or repairs possible typographical inconsistencies elsewhere in that paper. Its abstract alone cannot justify a stronger statement.

## 8. Limits and publication boundary

The four inspected source PDFs match the source manifest's byte counts and hashes. The journal question continuation and the prior-construction page were visually inspected in addition to text. The 2007 manuscript and the additional 1997 theorem were independently read online; attempts to reopen the two question PDFs in the live web reader failed, so their detailed inspection relied on the supplied hash-matching copies. This audit does not independently certify every repository-history search reported in the author packet, or exhaustive present-day literature coverage.

There are no mathematical corrections required in the frozen proof. The main release condition is preservation of the scope qualification. A minor presentation issue is that the README's shell fence is escaped; it does not affect the result.

This audit contains original exposition, verification code/results, bibliographic links, and hashes only. No source PDFs, extracted source pages, raw catalogue records, source-image copies, account information, or unrelated material are included. No remote changes were made. The audit hash manifest binds this report and its reproducibility files to the unchanged author freeze.
