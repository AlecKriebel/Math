# The preferred-direction force transition was resolved in 2007–2009

**30000585 / OWR-1327-001. Proposed status: already_solved, 0/5 original proof attempts. Independent source review pending.**

The exact original model has a **second-order (continuous) compact-to-expanded transition**. The singular part of the limiting log partition function has exponent **3/2** on the expanded side. This is a credited result of Owczarek–Prellberg (2007), made explicit in force variables and treated further by Brak et al. (2009). It is not a new result of this package.

## 1. Exact model and identification

Whittington's contribution to OWR41/2006, printed pp.2458–2460, states the question on p.2459. The walk starts at the origin of Z², has an initial East step, and subsequently uses East, North and South steps. Opposite vertical steps cannot be consecutive. Thus each visited vertical column is traversed monotonically, and there is no self-intersection. Contacts are pairs of lattice-neighbouring vertices that are not consecutive along the walk. The force is horizontal, in the preferred East direction. The horizontal span s is exactly the number of East steps.

With k contacts and n steps, the report's generating function is

    H(x,y,z)=sum b_n(k,s) x^k y^s z^n.

This is the same first-East-step model as Brak et al., Sections 2–5. To avoid conflicting uses of x and y across papers, use contact fugacity omega and force fugacity h:

    H(omega,h,z)=Ghat(z;h,1,omega).

There is no force perpendicular to the preferred direction, no adsorbing wall, and no stiffness parameter in the original question. The North/South steps here are axis-aligned, not the diagonal steps in the preceding Dyck-path adsorption example in the report.

Set the contact energy magnitude and lattice spacing to1. At inverse temperature beta>0 and tensile force f>=0,

    omega=exp(beta),  h=exp(beta f),
    Z_n(f,beta)=sum b_n(k,s) exp(beta k+beta f s),
    kappa(f,beta)=lim_(n→infinity) n^(−1) log Z_n(f,beta).

Brak et al., Section 3.2, establish this limit by concatenation and its convexity in log(omega), log(h). Their equations (2.17)–(2.19) identify kappa with minus the logarithm of the length-fugacity radius of convergence. This is the fixed-force canonical thermodynamic limit. It is not a statement about fixed-extension finite-size plateaus.

## 2. Published resolution and critical curve

Owczarek–Prellberg, *Exact solution of semi-flexible and super-flexible interacting partially directed walks*, J. Stat. Mech. (2007) P11010, Section 3.2, treats the fully flexible case sigma=1. Its uniform Airy asymptotics, equations (3.7)–(3.12), yield a second-order transition with crossover exponent2/3. The final paragraph of Section 3.2 explicitly substitutes horizontal force fugacity p and says that the location changes with p but the transition's character does not.

Brak, Dyke, Lee, Owczarek, Prellberg, Rechnitzer and Whittington, *A self-interacting partially directed walk subject to a force*, J. Phys. A42 (2009)085001, Sections3–5, matches the original model exactly. Equations(5.1)–(5.5) give the critical curve and the force-side3/2 free-energy asymptotic. Section 9 explicitly states that preferred-direction pulling leaves the second-order transition unchanged.

Write a=sqrt(omega). The physical critical-force fugacity is

    h_c(omega)=omega (sqrt(omega)−1)/(sqrt(omega)+1),        (1)

which satisfies

    omega = ((omega+h_c)/(omega−h_c))²,  0<h_c<omega.

Let a_theta>1 be the unique root of a³−a²−a−1=0, and beta_theta=2 log(a_theta). Then h_c(exp(beta_theta))=1. For beta>beta_theta, the critical tensile force is positive and equals

    f_c(beta)=beta^(−1) log[h_c(exp(beta))]
             =beta^(−1) log[(exp(beta/2)−1)/
                              (exp(−beta/2)+exp(−beta))].  (2)

For 0<=f<=f_c(beta), kappa(f,beta)=beta. As f decreases to f_c from the expanded side,

    kappa(f,beta)−beta ~ D_beta (f−f_c(beta))^(3/2),
    D_beta>0.                                             (3)

Equation (3) is the published result, not an extrapolation from bounded walk enumeration. At beta=beta_theta the endpoint is f_c=0 and the corresponding positive-force asymptotic applies. For beta<beta_theta there is no positive tensile-force collapse threshold: the model is already expanded at f=0. A zero-temperature limiting curve is not needed for the finite-temperature statement.

## 3. Conventions that could otherwise change the conclusion

**Endpoint convention.** The 2007 segment formulation ends in an East step, while the original report and 2009 formulation begin with one. These ensembles are exactly equinumerous, with all relevant weights preserved. For vertices gamma_0,...,gamma_n, use

    eta_i=gamma_n−gamma_(n−i),  0<=i<=n.

This reverses the order of steps while preserving their East/North/South directions; geometrically it reverses traversal and rotates/translates the trace. It maps first-East walks bijectively to last-East walks, preserving length, horizontal span and contacts. Thus no thermodynamic approximation is used to transfer the 2007 result at sigma=1.

**Free-energy sign.** The 2007 paper defines its reduced free energy with a minus sign, as log(z_s). The 2009 kappa used here is the positive log-partition convention, −log(z_c). All formulas above use the latter convention. A change of sign does not change transition order, but it changes derivative signs.

**No stiffness.** In the 2007 paper, positive stiffness can produce a first-order transition. The original question is the fully flexible sigma=1 case, for which Section 3.2 gives the continuous result. The extra cases in that paper are not silently substituted.

**No transverse-force transfer.** The 2009 paper explicitly distinguishes the more difficult case with a vertical force component. Its discussion says some observations in that case indicate but do not prove unchanged transition order. The original OWR question fixes the force in the horizontal preferred direction, so that remaining caveat concerns a different target.

**No unrestricted-walk transfer.** The original report itself chooses the partially directed model to obtain solvability. Nothing here settles force-induced transitions for unrestricted self-avoiding walks or a three-dimensional polymer model.

## 4. Reading the transition order without differentiating an unproved finite-size expansion

The source's statement can be interpreted directly at the level of its limiting free energy. Fix beta>beta_theta and put g(delta)=kappa(f_c+delta,beta)−beta. Then g=0 on the compact side and g(delta)~D_beta delta^(3/2) for delta>0. In particular g'(0)=0. Convexity and secant bounds show that the derivative on the expanded side tends to0; more precisely, where g is differentiable,

    g'(delta) ~ (3/2)D_beta sqrt(delta).

To see this without formally differentiating an equivalence, bound g'(delta) between the backward secant from a delta to delta and the forward secant from delta to b delta, where 0<a<1<b. Divide by sqrt(delta), use (3), and then let a and b tend to1. Thus the thermodynamic extension per step is continuous and vanishes at the transition. The singularity is not twice differentiable there: a finite second derivative together with g(0)=g'(0)=0 would imply g(delta)=O(delta²), contradicting (3).

The canonical extension is beta^(−1)kappa_f. This identification can be justified using convergence of convex functions: each n^(−1)log Z_n is differentiable and convex in f; secant inequalities squeeze its derivative to kappa_f wherever the latter exists. This does not require differentiating a subleading finite-n asymptotic. In particular, the speculative low-temperature finite-size formula and the explicitly qualified Darboux step discussed after Brak et al. (5.7)–(5.8) are not needed to infer the transition order from(3).

The uniform q-series/Airy analysis remains a credited published input. This package checks its exact model and normalization and explains the elementary thermodynamic consequence; it does not claim a new contour-asymptotic proof or a numerical proof of the exponent.

## 5. Bounded controls and source-status conclusion

The exact checker passes 13,347 assertions, including all 2,377 first-East walks through length nine, an independent vertical-segment count of the contact/span coefficients, the endpoint reversal, rational critical-curve identities, and finite partition-function covariance checks. These validate model matching and normalization. They do not establish the infinite-volume singularity or estimate its exponent.

The report's 2006 open question was answered by the later exact analysis. The imported 2026 triage did not identify that coverage. The appropriate status is therefore **already_solved, 0/5**, subject to separate source review. No novelty, priority, or independent reproof of the entire exact-solution machinery is claimed.

### Primary sources

- [Original OWR41/2006](https://publications.mfo.de/bitstream/handle/mfo/2971/OWR_2006_41.pdf?isAllowed=y&sequence=1), printed p2459
- [Owczarek–Prellberg 2007, complete published paper](https://webspace.maths.qmul.ac.uk/t.prellberg/papers/pub065.pdf), especially Sections 1 and 3.2; DOI 10.1088/1742-5468/2007/11/P11010
- [Brak et al.2009, complete published paper](https://webspace.maths.qmul.ac.uk/t.prellberg/papers/pub068.pdf), especially Sections 2–5 and9; DOI 10.1088/1751-8113/42/8/085001
