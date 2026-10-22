# Independent derivation before historical verdicts

Recorded after reading the current paper and complete six-file submitted proof, before reading any earlier review verdict or derivation. This is an adversarial analytic derivation, not a formal certificate or a numerical proof. The original six Git bodies were authenticated independently.

## Form, essential spectrum and the actual domain

For a smooth compact perturbation the altered boundary has a finite collection of local graph charts: compactness of the altered boundary and the definition of smooth boundary give this finite subcover. Use the local trace inequality with arbitrarily small gradient coefficient there and the flat fiber inequality outside. The form is closed and bounded below; its shifted norm controls H1. A compact Lipschitz graph has the same property by its globally bi-Lipschitz flattening. This avoids a hidden uniform global C-infinity or global H2 operator-domain assumption.

On the flat half-space, expansion of |u_y+beta u|^2 gives the endpoint term -beta|u(0)|^2, so q+beta^2 norm^2 equals tangential gradient plus this square. The outward derivative is -u_y; the decaying mode exp(-beta y) consequently satisfies the attractive Robin condition. A reversed outward normal would invalidate both the threshold and the defect.

Choose chi=1 in a compact neighborhood of every alteration and zeta=0 there, with chi^2+zeta^2=1. The exterior restriction agrees with a half-space function vanishing near every missing/added part; zero extension across those parts is H1. IMS produces a compactly supported error. The compact localization is lower bounded by local L2 mass because of the trace form estimate. A normalized weakly null operator Weyl sequence below -beta^2 has bounded H1 norm. Compact embedding on the bounded smooth local region makes its local L2 mass vanish, contradicting the localized shifted lower bound. This proves the lower essential edge without assuming that a variational negative value is automatically discrete.

For the opposite inclusion, send a tangential compact wave packet to infinity outside the projection of all alterations and multiply by sqrt(2 beta) exp(-beta y). Smooth compact tangential support permits zero continuation to the actual domain. Integration by parts against all H1 functions proves operator-domain membership directly and produces -Delta u in L2, including the Robin boundary term. Translation makes the packet weakly null; dilation makes the residual at |k|^2-beta^2 tend to zero with rates R^-1 and R^-2. This includes k=0. No artificial vertical cutoff may be inserted without accounting for its residual. The construction proves every energy in the stated interval belongs to essential spectrum, also on the Lipschitz graph because these supports are wholly flat.

## Low dimensions, including holes and overhangs

The physical positive solution phi=exp(-beta y) solves Delta phi=beta^2 phi. Expansion and integration by parts yield

Q[phi v] = integral phi^2 |grad v|^2 - beta integral_boundary (1+nu_y) phi^2 |v|^2.

The sign is independent of whether the boundary can be written as one graph. Since a unit normal has nu_y>=-1, the defect is nonnegative; it vanishes on the unmodified boundary. If its integral were zero, continuity would force nu=-e_y everywhere. Each connected component of the boundary is then open in a horizontal plane and closed in that plane, hence the entire plane. Agreement at infinity permits only y=0. The domain, connected and equal to H at infinity, must be H. Thus every nontrivial perturbation, including a compact obstacle or an overhang, has strictly positive finite defect. A compact boundary component cannot have a globally constant downward normal.

Let psi(x)=1 near the full projection of every change, with derivative only in the flat region. The actual domain is bounded below and has the entire upper half-tail. Hence exp(-beta y) psi lies in H1, although exp(-beta y) alone is not globally L2 in tangential variables. Vertical truncation tending upwards justifies using the identity; its weighted errors vanish for each fixed psi. Derivative support sees full fibers (0,infinity), giving precisely (2 beta)^-1 integral |grad psi|^2-beta B. Two linear tails yield energy 2/L in m=1; the logarithmic annulus yields 2 pi/log(R/R0) in m=2. Taking the tangential radius first, then a suitable vertical truncation, gives a strictly negative actual-domain form value. The established essential edge and min-max give a discrete eigenvalue. There is no transferred flat-domain criticality assumption. The auxiliary mixed boundary pair has the same positive solution and the displayed null sequence on the actual geometry.

## Graph absence on all form functions

For a compact graph f, flatten y=t+f(x), with unit volume Jacobian and boundary area sqrt(1+|grad f|^2). Set u(flat)=exp[-beta(t+f)] w. The physical tangential derivative of the transformed v is grad_x w-grad f w_t; the vertical derivative is w_t. Fiber integration of the exponential cross term contributes +beta exp(-2 beta f)|w(0)|^2. Subtracting the Robin area contribution leaves -beta exp(-2 beta f)(sqrt(1+|grad f|^2)-1)|w(0)|^2. Losing this area factor would falsely make every graph flat.

For g=grad f, the inverse shear estimate |a|^2+|b|^2 <= 2(1+G^2)(|a-gb|^2+|b|^2) is valid also for complex a,b by the norm triangle inequality. It is deliberately nonsharp but positive uniformly. Let A=4 R^2/(m-2)^2. Tangential Hardy first bounds local weighted L2 by A E_x. Vertical integration gives T_K=2 beta L_K-2 Re integral exp(-2 beta t) conjugate(w)w_t, and Cauchy plus 2sqrt(E_x E_t)<=E_x+E_t yields T_K <=(2 beta A+sqrt A)E. The bulk coefficient is exp(-2 beta M)c and the negative trace coefficient is at most beta exp(2 beta M)D. Their difference is nonnegative under the manuscript's condition.

Hardy regularization is legitimate: div[x/(r^2+delta^2)]=[(m-2)r^2+m delta^2]/(r^2+delta^2)^2. The completed-square lower bound is a0^2 r^2/(r^2+delta^2)^2 plus a0 m delta^2/(r^2+delta^2)^2 for a0=(m-2)/2. The second term is nonnegative for m>=3, and Fatou gives the claimed Hardy constant. This homogeneous control is false in m=1,2, consistently with the cutoff calculation.

These calculations start on flattened compact-support core functions. Multiplication by exp(beta y) is bounded only on each such support, which suffices. Flattening and local smooth approximation yield H1 density. When the coefficient is nonnegative, Q>=0 for every core function, so continuity of the closed form gives Q>=0 on all H1; no globally growing exponential multiplier or weighted-energy assertion for arbitrary H1 is necessary. For each fixed graph the condition holds on a small interval of beta. If f=0 it holds at every beta. No statement about one nonzero graph at all beta follows.

## Independent prior-theorem bridge

The different transform U=exp(beta f)u(flat) is a bounded invertible H1 map on all form functions because f and its weak gradient are bounded. Write b=U_t+beta U. Direct derivatives give grad_x u(flat)=exp(-beta f)[grad_x U-grad f b] and u_y=exp(-beta f)U_t. Adding beta^2 mass and integrating the vertical cross term yields bulk exp(-2 beta f)(|grad_x U-grad f b|^2+|b|^2) minus exactly the normal/area defect. The same shear inequality gives Q>=a_beta(E_beta-v_beta local trace mass), with a_beta=exp(-2 beta M)c and v_beta=beta D exp(4 beta M)/c.

For each Fourier fiber p let rho=sqrt(|p|^2+beta^2). Expanding squares and integrating (|U|^2)' gives

integral(|U_t+beta U|^2+|p|^2|U|^2) = integral|U_t+rho U|^2+(rho-beta)|U(0)|^2.

This identity first holds on a core and extends to H1. The trace lies in H1/2, and the last form is T_beta=sqrt(-Delta+beta^2)-beta. A bounded compact-support potential is infinitesimally form bounded, and multiplication by its square root is compact from H1/2 to L2 by restricting to a containing ball and local Rellich. The perturbed essential spectrum is therefore [0,infinity). A count of strictly negative eigenvalues is sufficient to exclude all negative spectrum; without the compactness/essential-spectrum step it would not be sufficient.

The printed HHRV formula must be checked separately from the older preprint. If its coefficient is theta^2/(1-2theta)^2 for 0<theta<1/2, theta=1/4 gives 1/4. Substituting v_beta<=beta C_f and mass beta into the two factors produces beta^m, not beta^(m/2). An integer upper bound <=1/2 forces zero negative eigenvalues. This yields the full fixed-graph weak-beta claim as a prior-theorem corollary, rather than a new kinetic-energy mechanism. The alternative older denominator (1-4theta)^2 would be undefined at the chosen theta and cannot certify this argument.

## Exact example and scope

For h=exp[-1/(1-r^2)], differentiation gives |grad h|=2r q^2 exp(-q), q>=1. The maximum of q^2 exp(-q) is 4/e^2, and e>2 gives |grad h|<2. Smoothness through r=1 follows because every power of 1/(1-r^2) times its exponential tends to zero. For f=h/100, M<1/100, G<1/50, D<G^2/2<1/5000, c>1250/2501. The power series comparison exp(1/25)<25/24 makes the Hardy-side defect <1/480. Subtracting from c gives 597499/1200480>0. The graph is nonzero and its domain and boundary are connected; the flattening is a smooth diffeomorphism. Its symmetric difference with H is bounded.

For the independent count certificate at m=3, v<2501/6000000, s=16v<1/100, s(s+2)<201/10000<1/40, C3=1/(2 pi^2), and the unit-ball measure gives count <=[s(s+2)]^(3/2)/(6 pi)<1/240. Thus it has no below-threshold spectrum at beta=1. Equality of spectral sets with the essential interval does not eliminate embedded eigenvalues. For a separately prescribed beta, reducing epsilon in epsilon h drives D quadratically to zero, establishing an example depending on beta. The theorem does not solve arbitrary high-dimensional nongraph geometry or certify novelty, worldwide openness, or independent priority.

Pending independent source-body verification, package reproduction, and output-path fault probes. Completion estimate at this derivation checkpoint: 30%.
