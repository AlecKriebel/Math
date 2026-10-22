# Quadratic chain characterization and viscosity sign correction

This is an AI-assisted, unrefereed mathematical draft. Acceptance means one independent internal AI mathematical reconstruction accepted the stated partial result with a correction and explicit standard imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

Target: 20002465 / AIM-PDES-0077. This file preserves the complete accepted mathematical reconstruction and correction, including the unresolved unrestricted chain-recurrence question. AUDIT.md records the editorial acceptance checks; it is not a second independent mathematical audit.

## Audit conclusion

For a smooth vector field on a compact connected smooth Riemannian manifold without boundary, the projected zero-class Aubry set of its quadratic Mañé Lagrangian equals the quadratic-chain recurrent set defined below. The corresponding tangent Aubry set is its graph lift. Constants are the only critical viscosity solutions exactly when this set is the whole manifold. These conclusions survive independent reconstruction.

The imported argument contains a false ancillary assertion: negating a viscosity solution does not in general produce a viscosity solution for the Hamiltonian with reversed drift. Section 8 gives an explicit smooth-drift circle counterexample and a replacement proof of the valid uniqueness conclusion for both signs.

**Disposition: ACCEPTED PARTIAL RESULT WITH CORRECTION.** The unrestricted inclusion of ordinary chain recurrence in the Aubry set is not proved or disproved here. The full original problem is not solved. No novelty or exhaustive literature-search claim is made.

## 1 Scope and the original question

The AIM list, *New connections between dynamical systems and PDE's*, PDF page 3, items 1 and 2, asks for a dynamical description of the zero-class Aubry set of

\[
L_f(x,v)=\tfrac12\lVert v-f(x)\rVert_x^2,
\]

including its relation to chain recurrence, and a uniqueness condition for a stationary Hamilton-Jacobi equation. Its printed tangent zero-section identification and minus-sign Hamiltonian are inconsistent with this Lagrangian under ordinary tangent coordinates and Legendre duality. Its literal uniqueness question also omits additive normalization. These are source defects, not hypotheses silently adopted in this audit. [Original problem list](https://aimath.org/WWN/dynpde/dynpde.pdf).

The exact imported question was read and compared with primary-domain parsed PDF text. Original PDF-byte retrieval still returned HTTP 403; an original-page screenshot was unavailable. Thus this audit does not claim direct visual inspection of the AIM PDF. The scope was additionally checked against the proposer's own reformulation in Fathi, Figalli and Rifford [FFR], PDF pages 5-6.

Throughout, M is nonempty, compact, connected, smooth and without boundary, with a smooth Riemannian metric, and f is smooth. Write phi^t for its complete flow. All distances below use this fixed metric. The argument is not asserted for arbitrary noncompact spaces, boundaries, nonsmooth vector fields, or unrelated Lagrangians.

Direct Legendre calculation gives p=(v-f)^flat and v=f+p^sharp, hence

\[
H_f(x,p)=\tfrac12\lVert p\rVert_x^2+p(f(x)).
\]

The invariant graph in TM is Graph(f); its cotangent image is the zero section. The printed minus-sign Hamiltonian is H_{-f}. Constants solve either equation, so literal uniqueness of the function zero is impossible. Uniqueness means modulo constants or with u(x_*)=0 at a prescribed base point.

## 2 Definitions and explicit mathematical dependencies

For t>0 let A_t(x,y) be the infimum of the L_f-action among absolutely continuous curves from x to y in time t. The critical value is zero since the constant function solves H_f(x,Du)=0. Put

\[
h_f(x,y)=\liminf_{t\to\infty}A_t(x,y),\qquad
\mathcal A_f=\{x:h_f(x,x)=0\}.
\]

Actions are nonnegative. They are also uniformly bounded above for t>=1: follow the flow until t-1 and join its endpoint to y by a minimizing geodesic in one unit of time. If D=diam(M) and F=max|f|, its action is at most (D+F)^2/2. Thus h_f is finite everywhere.

A returning T-chain at x has N>=1, points x=x_0,...,x_N=x, times t_i>=T, and errors

\[
e_i=d(\phi^{t_i}(x_i),x_{i+1}).
\]

Ordinary chain recurrence CR requires max_i e_i<epsilon for every T,epsilon>0. Strong chain recurrence SCR uses sum_i e_i<epsilon. Define

\[
\mathcal R_2(f)=\{x:\ \forall T,epsilon>0\ \exists\text{ returning T-chain at }x
\text{ with }\sum_i e_i^2<epsilon\}.
\]

Strict versus non-strict lower time bounds makes no difference: invoke the definition at 2T. Bi-Lipschitz changes of distance preserve all three sets. Smooth Riemannian metrics on compact M are mutually bi-Lipschitz.

The following standard weak-KAM facts are used as cited foundations, not reproved here: finite h_f(x,.) is a critical viscosity solution for every x; the tangent Aubry set projects bijectively to A_f; critical subsolutions are differentiable on A_f and share the derivative there. These appear in [FFR], PDF page 3, Theorems 2.1 and 2.5-2.6 (pages 7-9). This dependency is explicit: the action-to-chain proof below is elementary, while identification with the conventional tangent Aubry set and the viscosity criterion use these foundations. The pointed-Peierls assertion is in the introduction on page 3, not immediately after the Section 2 definition as the imported report suggested.

## 3 A uniform controlled-curve estimate

For R>0 set

\[
K_R=\max\left(1,\sup_{|r|\le R,\,z\in M}\|D_z\phi^r\|\right),\qquad C_R=R K_R^4.
\]

Compactness and smoothness give K_R<infinity. Derivative bounds imply the corresponding Lipschitz bounds by applying the map to curves and taking infima of lengths.

Let gamma:[0,s]->M be absolutely continuous, 0<=s<=R. If its action is infinite the desired estimate is automatic. Otherwise put q=dot gamma-f(gamma) and z(r)=phi^{-r}(gamma(r)). The chain rule for absolutely continuous curves and the flow identity give, almost everywhere,

\[
\dot z(r)=D\phi^{-r}_{\gamma(r)}q(r).
\]

Consequently

\[
\begin{aligned}
d(\gamma(s),\phi^s(\gamma(0)))
&\le K_R d(z(s),z(0))\\
&\le K_R^2\int_0^s\|q(r)\|\,dr,
\end{aligned}
\]

and Cauchy-Schwarz yields

\[
d(\gamma(s),\phi^s(\gamma(0)))^2
\le C_R\int_0^s\|\dot\gamma-f(\gamma)\|^2\,dr. \tag{1}
\]

The same C_R works for every starting point and every interval of length at most R. In particular it is independent of how many such intervals a long curve has.

## 4 Aubry loops give quadratic chains

Fix x in A_f and T,epsilon>0. The nonnegative liminf defining h_f(x,x)=0 supplies arbitrarily long times S with arbitrarily small A_S(x,x). By the defining infimum, choose a closed absolutely continuous curve gamma based at x, of duration S>=2T, with action less than epsilon/(2C_{2T}). No existence of an action minimizer is needed.

Set N=floor(S/T) and tau=S/N. Then N>=2 and T<=tau<2T. Put x_i=gamma(i tau). Apply (1) after translating time on every block. Summing gives

\[
\sum_{i=0}^{N-1}d(\phi^\tau(x_i),x_{i+1})^2
\le C_{2T}\int_0^S\|\dot\gamma-f(\gamma)\|^2\,dr
=2C_{2T}\operatorname{Action}(\gamma)<epsilon.
\]

Therefore A_f is contained in R_2(f). The bounded block lengths are essential: no control constant depending on the total loop duration has been used.

## 5 Quadratic chains give Aubry loops

First R_2 is flow invariant. For any fixed a in R, applying phi^a to the chain points preserves all flight times and multiplies each error by at most Lip(phi^a). Choosing the original quadratic budget divided by the square of this constant gives a chain at phi^a x. Applying the same argument to -a proves equality of the images.

For y,z in M choose a constant-speed minimizing geodesic eta:[0,1]->M from y to z, and define

\[
\beta(s)=\phi^s(\eta(s)).
\]

Its endpoints are y and phi^1 z. Almost everywhere,

\[
\dot\beta(s)-f(\beta(s))=D\phi^s_{\eta(s)}\dot\eta(s),
\qquad
\operatorname{Action}(\beta)\le\tfrac12K_1^2 d(y,z)^2. \tag{2}
\]

A minimizing geodesic exists on the complete compact manifold. No unique geodesic or injectivity-radius restriction is needed.

Let x in R_2(f), and set w=phi^{-1}x. Given T>=1, take a returning T-chain x_0=w,...,x_N=w. Put y_i=phi^{t_i}x_i. A block beginning at phi^1 x_i first follows the true orbit for t_i-1 units, reaching y_i, then follows the bridge in (2) from y_i to phi^1 x_{i+1}. Its duration is exactly t_i. All blocks concatenate to a loop based at phi^1w=x, of duration

\[
S=\sum_i t_i\ge T
\]

and action at most K_1^2(sum_i e_i^2)/2. This shift is necessary: an unshifted bridge ends at phi^1 x_{i+1}, not at x_{i+1}.

For each integer n>=1 use T=n+1 and a quadratic budget below 2/(n K_1^2). The resulting loop has S_n>=n+1 and action below 1/n. Hence h_f(x,x)=0. Together with Section 4,

\[
\boxed{\mathcal A_f=\mathcal R_2(f).} \tag{3}
\]

For the tangent lift, zero is a critical subsolution and its calibrated trajectories are precisely the flow trajectories: zero calibration means integral L_f=0, hence dot gamma=f(gamma) almost everywhere. Thus I-tilde(0)=Graph(f). The standard Aubry graph facts in Section 2 imply

\[
\boxed{\widetilde{\mathcal A}_f
=\{(x,f(x)):x\in\mathcal R_2(f)\}.} \tag{4}
\]

This also identifies the precise invariant copy of the original flow.

## 6 Recurrence bounds and a strict separation

If sum e_i<sqrt(epsilon), then sum e_i^2<epsilon. If sum e_i^2<epsilon^2, every e_i<epsilon. Therefore

\[
\operatorname{SCR}(f)\subseteq\mathcal R_2(f)=\mathcal A_f\subseteq\operatorname{CR}(f). \tag{5}
\]

The first inclusion can be strict even for smooth circle flows. Take the circle R/(2pi Z), let I=[pi,2pi] modulo 2pi, and choose a smooth a>=0 which vanishes exactly on I and is positive on (0,pi). Set f=a(theta) partial_theta. Such an a exists, for example a(theta)=exp(-1/[theta(pi-theta)]) on (0,pi) and zero on I. Flatness at the endpoints makes the periodic extension smooth.

Every point of I is fixed. If x in (0,pi), its forward orbit approaches pi and its backward orbit approaches 0. Given T and a desired quadratic budget, flow forward for at least T until near pi and jump to pi. Cross I through N equally spaced fixed points, with a wait of length T before each jump. The squared jump cost for this part is pi^2/N. At 0, wait T and jump to z=phi^{-s}x with s>=T sufficiently large that z is close to 0; flow for time s exactly back to x. The first and penultimate errors can be made arbitrarily small, and then N arbitrarily large. Thus R_2=CR=S^1.

Define the continuous periodic 1-Lipschitz function lambda(theta)=-theta on [0,pi] and lambda(theta)=theta-2pi on [pi,2pi]. It is constant along fixed orbits and strictly decreases along every nonfixed orbit. For a chain starting at x outside I, its first flight of duration at least T loses at least

\[
\delta=\lambda(x)-\lambda(\phi^T x)>0.
\]

Every other flight has nonpositive lambda increment, and the total possible increase across jumps is at most sum e_i. Telescoping a returning chain gives sum e_i>=delta. Hence x is not strongly chain recurrent. Fixed points are strongly recurrent with one exact flight. Therefore

\[
\operatorname{SCR}(f)=I\subsetneq\mathcal R_2(f)=\mathcal A_f=\operatorname{CR}(f)=S^1.
\]

This example rules out replacing the squared cost in (3) by the strong-chain cost. It supplies no counterexample to the reverse ordinary-chain inclusion.

## 7 The exact normalized uniqueness criterion

If A_f=M, the common-derivative Aubry property from Section 2, compared with the constant zero solution, gives Du=0 everywhere for every critical viscosity solution u. Connectedness implies u is constant: a differentiable function with zero derivative is constant along every smooth path.

Conversely, suppose every critical viscosity solution is constant. Fix any x in M. By the pointed-Peierls fact, h_f(x,.) is constant; x need not already be an Aubry point. By compactness choose t_n->infinity with phi^{t_n}x->y. For t_n>=1 follow the orbit from x for t_n-1, then use (2) with

\[
y_n=\phi^{t_n-1}x,\qquad z=\phi^{-1}y.
\]

The bridge ends at y and has action at most K_1^2 d(y_n,z)^2/2, which tends to zero because phi^{-1} is continuous. The total time is t_n. Nonnegativity now gives h_f(x,y)=0. Since h_f(x,.) is constant, h_f(x,x)=0. This holds for all x.

Thus

\[
\boxed{\text{only constant critical viscosity solutions}
\iff\mathcal A_f=M\iff\mathcal R_2(f)=M.} \tag{6}
\]

With u(x_*)=0, this is exactly uniqueness of zero. No disconnectedness hypothesis is needed for (6). Connectedness is necessary for the single-constant conclusion; components otherwise admit independent constants.

## 8 Correct time reversal and a rejected viscosity claim

For every absolutely continuous path gamma from x to y in time t, its reverse bar-gamma(s)=gamma(t-s) goes from y to x and satisfies

\[
L_{-f}(\bar\gamma(s),\dot{\bar\gamma}(s))
=L_f(\gamma(t-s),\dot\gamma(t-s)).
\]

Reversal is a bijection of the path families. Therefore

\[
A_t^{-f}(y,x)=A_t^f(x,y),\qquad
h_{-f}(y,x)=h_f(x,y),\qquad
\mathcal A_{-f}=\mathcal A_f. \tag{7}
\]

Apply (3) and (6) separately to -f, which satisfies all the same assumptions. It follows that R_2(-f)=R_2(f), and constants-only viscosity uniqueness is equivalent for the plus and minus equations. This proves the claimed uniqueness criterion for the equation actually printed in the AIM list.

**Rejected step.** The algebraic identity H_{-f}(x,p)=H_f(x,-p) does not imply that u->-u carries viscosity solutions to viscosity solutions. Negation exchanges upper and lower touching tests without reversing the sign of H; the requisite inequalities consequently point the wrong way. The identity is valid for classical differentiable solutions, which does not settle the nonsmooth case.

**Explicit counterexample.** On S^1 with its usual metric take f(theta)=sin(theta) partial_theta and

\[
u(\theta)=\min\{0,2\cos\theta\}.
\]

Away from a=pi/2 and b=3pi/2, u is smooth and its derivative is either 0 or -2sin(theta), so H_f(theta,u')=0. At a the left and right slopes are 0 and -2; at b they are 2 and 0. At either downward corner there is no C^1 lower touching test. Every upper touching derivative lies between the right and left slopes. At a, H_f(a,p)=p(p+2)/2<=0 for -2<=p<=0; at b, H_f(b,p)=p(p-2)/2<=0 for 0<=p<=2. Thus u is both a viscosity subsolution and supersolution on the circle.

But v=-u has an upward corner at a. The smooth local function psi(theta)=theta-a touches v from below at a: on the left psi<=0=v, and on the right v=2sin(theta-a)>theta-a for sufficiently small positive theta-a. Its derivative is 1, while

\[
H_{-f}(a,1)=\tfrac12-1=-\tfrac12<0.
\]

This violates the viscosity supersolution condition. Therefore -u is not a viscosity solution of H_{-f}=0. The imported blanket solution-bijection claim is false; the corrected proof of the uniqueness criterion uses (7), not that claim.

## 9 Precisely what remains unresolved

For smooth f in dimension at most three, [FFR, Theorem 1.6, page 6] establishes A_f=CR(f). More generally its Lemma 4.13, pages 35-36, gives that equality under its Mather disconnectedness hypothesis: for every pair of weak-KAM solutions u_1,u_2, the set (u_1-u_2)(A_f) is totally disconnected. At C^k regularity, k>=2, the stated three-dimensional alternatives are that f is nowhere zero or f is C^{3,1}. These are cited established results, not new proofs of their Hausdorff-dimension ingredients.

Outside such hypotheses, the missing assertion remains

\[
\operatorname{CR}(f)\subseteq\mathcal R_2(f).
\]

The obstacle is quantitative: a chain with N errors each below delta has squared cost below N delta^2, and ordinary chain recurrence gives no bound on N as delta decreases. Repeating a chain increases rather than decreases its total squared cost. Long flow times also cannot be absorbed in a uniformly bounded derivative estimate unless the finite-time partition or shifted-bridge constructions above are used. None of these observations proves that the inclusion fails; they explain why the elementary argument does not establish it.

Cheng and Wei [CW], inspected pages 1-4, impose closed-one-form and geometric conditions in their newer results; those pages do not furnish the missing unrestricted implication. This is a bounded source observation, not an exhaustive assertion that no later theorem exists. Their journal version was not inspected. The exact quadratic-chain terminology and proof may have antecedents; novelty remains unassessed.

## 10 Acceptance boundary and verification

The original candidate's main action-chain argument, tangent lift, recurrence bounds, separating example and normalized uniqueness criterion pass after the stated source and sign corrections. The claim of a general viscosity-solution bijection under negation is rejected. The original unrestricted chain-recurrence question remains unresolved by this work.

The standard weak-KAM foundations explicitly identified in Section 2 are external dependencies. This report does not pretend to reprove all of weak-KAM theory or [FFR]'s dimension estimates. The finite checks in the original audit scripts, which are not distributed in this prose edition, confirm integrity, exact algebraic examples, boundary declarations and error rejection; they do not constitute a formal proof of the continuum theorem. The mathematical argument is in Sections 3–8.

Only authored mathematical prose, compact acceptance data, public bibliographic information and verification metadata are distributed in this edition. Source PDFs, copied source text, source datasets, private coordination records and executable code are not included. No source-author code was executed. Source retrieval and inspection limits are recorded in SOURCES.json; verification boundaries are recorded in VERIFICATION.json.

## References

- AIM, *New connections between dynamical systems and PDE's*, version dated August 15, 2003, PDF page 3, items 1-2. [Primary problem list](https://aimath.org/WWN/dynpde/dynpde.pdf).
- [FFR] Albert Fathi, Alessio Figalli and Ludovic Rifford, *On the Hausdorff Dimension of the Mather Quotient*, arXiv:0711.1359v1, November 8, 2007. [Versioned record](https://arxiv.org/abs/0711.1359v1), [versioned PDF](https://arxiv.org/pdf/0711.1359v1). Associated journal citation: *Communications on Pure and Applied Mathematics* 62 (2009), 445-500, [DOI](https://doi.org/10.1002/cpa.20250). The retained and inspected item is the preprint, not the journal PDF.
- [CW] Wei Cheng and Wenxue Wei, *A geometric approach to Mather quotient problem*, arXiv:2409.00958v1. [Versioned record](https://arxiv.org/abs/2409.00958v1), [versioned PDF](https://arxiv.org/pdf/2409.00958v1). Used for bounded contextual inspection only.
