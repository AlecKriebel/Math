# Author approach 4: actual Petersson-metric growth at the odd elliptic cusp

Problem 30004711. 7 October 2026. Fourth directed mathematical approach. Earlier frozen files are unchanged; the separate Approach 2 convention clarification is included.

## Goal and outcome

Try to control the boundary contribution by estimating an actual degenerating genus-one spin family, rather than another generic model. The canonical 3/2-differential norm can be bounded uniformly in the pinching parameter using Schwarz–Pick comparisons.

The resulting bounds show that this canonical metric is **not smoothly extendible as a positive Hermitian metric** on the stated natural bundle at the odd Ramond node. In fact its canonical Chern curvature has no bounded-coefficient extension in the plumbing coordinate. This is a correction to the strong smooth-metric/smooth-form extension assertion appearing in the source argument. It does not refute an extension as a current or the claimed intersection-number identity.

The bounds are sublogarithmic for the logarithm of the metric, which is the right type of behavior for a zero-residue argument. They force any *existing finite* Chern boundary-flux limit to be zero. Proving existence of that flux, and comparing the actual torsion representative to this canonical one, are separate steps not supplied by the bounds alone.

## 1. Fix the actual family, bundle, and frame

Take

C_tau = C/(Z+tau Z), tau=a+iT, |a|<=1/2, T>3,
Sigma_tau=C_tau minus {0}.

The external marking is NS. Choose the unique odd theta characteristic on C_tau, the trivial coarse square root of its canonical line. Let omega_tau=dz be the invariant differential with a-period1. Its square root is a frame on a local chart of the spin/Hodge square-root stack.

Approach 2 proves on the compactified odd-spin component that F^dual=H^3 with H^2=lambda. Thus

s_tau=(dz)^(3/2)

is a nonzero holomorphic frame of F^dual on such a chart. This is not a frame obtained by multiplying an extending section by a power of q. Under q=exp(2 pi i tau), the elliptic invariant differential is dz=(1/(2 pi i))du/u in the multiplicative Tate coordinate u. It extends to the nonzero dualizing differential on the nodal rational limit. The odd spin line remains locally free at its Ramond node. Accordingly the square-root frame, and then s_tau, extend nonvanishing on a local spin chart. A finite ramified base change only replaces log(1/|q|) by a constant multiple and does not change the conclusions below.

Write the complete curvature-minus-one hyperbolic metric on Sigma_tau as

h_tau=rho_tau(z)^2 |dz|^2.

Norbury's canonical Petersson metric on F^dual gives the squared norm

M(tau):=||s_tau||^2=integral_(Sigma_tau) dx dy / rho_tau(z).

This follows directly from the 3/2-differential pairing integral bar(eta)eta/sqrt(h). The integral is finite for fixed tau: near the external puncture the differential s_tau has no pole in z, and 1/rho_tau tends to zero. Its growth as the *surface degenerates* is a different question.

The metric on the odd tangent line F is the inverse of this metric. Nothing below identifies either one with a torsion metric.

## 2. First lower bound using only area

The flat coordinate area of C_tau is T. Gauss–Bonnet gives

integral_(Sigma_tau) rho_tau^2 dxdy=2 pi.

Hölder's inequality, applied to

1=(rho_tau^(-1))^(2/3)(rho_tau^2)^(1/3),

yields

T <= M(tau)^(2/3)(2 pi)^(1/3),
M(tau) >= T^(3/2)/sqrt(2 pi).

Already this proves divergence in the nonvanishing compactified frame. It needs no asymptotic formula for uniformization.

## 3. Sharper collar lower bound

For T>3 the annulus

A_T={z modulo Z : 1<Im z<T-1}

embeds holomorphically into Sigma_tau. Put Y=T-2. Its complete curvature-minus-one Poincaré density is

rho_A(z)=(pi/Y)csc(pi(Im z-1)/Y).

Schwarz–Pick for the inclusion A_T -> Sigma_tau gives rho_tau<=rho_A on A_T. Hence

M(tau) >= integral_(A_T) rho_A^(-1) dxdy
       = integral_0^1 dx integral_0^Y (Y/pi)sin(pi y/Y)dy
       = 2(T-2)^2/pi^2.

This estimate is uniform in a. It exhibits the periodic spin zero mode on the long *internal Ramond collar*: s_tau has constant coefficient in z. It should not be confused with the exponential decay at the fixed external NS cusp.

## 4. Uniform upper bound from a fixed comparison surface

The translation cover of Sigma_tau is

U_tau=C minus (Z+tau Z).

Its complete Poincaré metric is the pullback of rho_tau. Since 0 and1 belong to every lattice,

U_tau subset U:=C minus {0,1}.

Schwarz–Pick for this inclusion gives rho_(U_tau)>=rho_U. The fixed surface U is the thrice-punctured sphere, including infinity. Its cusp metric at infinity has rho_U(z) asymptotic to 1/(|z| log|z|). Near0 and1 its density diverges; on the remaining compact region it is positive. It follows that one fixed constant C satisfies

rho_U(z)^(-1) <= C(1+|z|)log(2+|z|)

throughout U. This uses only the usual local cusp coordinate for a complete finite-area hyperbolic surface.

Choose the standard parallelogram as a fundamental domain for the lattice. Its flat area is T and |z|<=T+C_0 there, uniformly for |a|<=1/2. Therefore

M(tau) <= C_1 T^2 log T

for all sufficiently large T, with C_1 independent of a.

Combining the two estimates gives

2(T-2)^2/pi^2 <= M(a+iT) <= C_1 T^2 log T,
log M(a+iT)=2 log T+O(log log T),

uniformly in a.

## 5. Consequences in the plumbing coordinate

Let q=exp(2 pi i tau), so T=(1/(2 pi))log(1/|q|). The squared norm of a nonvanishing extending frame therefore tends to infinity, while its logarithm

u(q)=log M(tau)

satisfies

u(q)=2 log log(1/|q|)+O(log log log(1/|q|)).

In particular u is unbounded above but u(q)=o(log(1/|q|)), uniformly in the argument of q.

### The metric cannot extend positively and continuously

A positive continuous Hermitian metric evaluated on a nonvanishing holomorphic frame extending over q=0 has a finite positive limit. M(tau) does not. The inverse metric on F tends to zero and likewise has no positive nondegenerate continuous extension. Thus neither metric can have the asserted positive smooth extension on that fixed bundle.

### The canonical Chern curvature cannot extend as a bounded form

Suppose, for contradiction, that partial barpartial u had bounded coefficients in a disk about q=0. A bounded local solution v of the associated Poisson equation can be constructed from its logarithmic potential. Then w=u-v is harmonic on the punctured disk.

The uniform sublogarithmic bound w=o(log(1/|q|)) excludes both a logarithmic singularity and all negative-power terms in the isolated-singularity expansion of a real harmonic function. Hence w extends harmonically and is bounded near0. Since v is bounded, u would be bounded, contradicting the lower estimate. Therefore the curvature, and hence the actual canonical Euler two-form in rank one, has no bounded-coefficient extension in this coordinate.

This statement concerns the actual form determined by the metric. It does not exclude a different smooth representative of its characteristic class, nor a distributional/current extension of the original form. The logarithmic growth makes u locally integrable, so its distributional partial barpartial is well-defined.

## 6. What the bounds imply about residue, and what they do not

Put t=log(1/|q|) and let m(t) be the angular average of u(e^(-t+i theta)). The bounds give m(t)=O(log t). The boundary integral of the rank-one Chern connection, relative to a smooth extending reference metric, is a fixed convention factor times m'(t), plus a term tending to zero from the reference metric.

If this boundary flux has a finite limit b, then m'(t) has a finite limit proportional to b. Averaging its derivative over [t_0,t] shows m(t)/t tends to that same limit. But m(t)/t->0. Consequently **any existing finite boundary-flux limit is zero**.

The estimates do not prove the existence of that derivative limit. A uniform O(log t) bound by itself allows oscillating derivatives. One sufficient next step would be local absolute integrability of the canonical Chern curvature: integrating curvature over shrinking annuli would then give a finite limiting flux, which the sublogarithmic bound forces to vanish. Alternatively, a direct controlled derivative expansion would suffice. Neither is established here by differentiating an inequality.

Still less do these bounds evaluate the boundary transgression between the canonical Chern connection and the actual torsion-induced representative. That comparison requires the second connection/retraction and its asymptotics. The canonical divergence must not be mistaken for evidence of a nonzero torsion correction.

## 7. Distinguish external NS decay from the internal degeneration

At an external NS cusp with local coordinate q_cusp=exp(2 pi i w), w=x+iy, a permitted 3/2-differential eta=f(q_cusp)dq_cusp^(3/2)/q_cusp has w-coefficient O(exp(-pi y)) when f is bounded. Since the cusp hyperbolic density is 1/y,

|eta|^2/sqrt(h)=O(y exp(-2 pi y))dxdy,

and the norm tail beyond y=Y is O(Y exp(-2 pi Y)). This elementary estimate is useful for fixed-surface norm integrability.

It is not a bound uniform in a pinching *moduli parameter*. The internal Ramond collar in sections2–4 has a constant spin mode and yields the opposite phenomenon, quadratic growth in T. Thus external-NS cusp estimates alone cannot justify the uniform moduli-integrability step in Approach3 or a smooth metric extension at every boundary stratum.

## 8. Relation to the source and supported status

Norbury 2005.04378v4, section3.4, defines the metric used here, and the proof of Theorem6 on pp.37–38 argues for its smooth extension. The later 2312.14558v3, section3.1.1, makes a similar assertion. Under the explicit odd-spin bundle/frame identification of Approach2, the estimates above contradict that strong positive-smooth-metric assertion at the Ramond node. They also rule out interpreting the actual rank-one Euler form as a bounded differential-form extension there.

This is a candidate analytic correction requiring independent review. It does not, by itself, contradict an equality of integrated characteristic classes: logarithmically singular metrics often require a current-level extension argument instead. The previously credited canonical volume theorem is not replaced by a claimed counterexample to its numerical conclusion. Any use of the source's stronger extension language should now distinguish the form/metric assertion from the possible weaker current/cohomological result.

Approach4 therefore supplies actual uniform estimates on the relevant degenerating family, identifies an analytic obstruction to the smooth-extension shortcut, and reduces a possible replacement to proving a finite curvature/flux limit. The original torsion-volume identity remains unresolved by this approach. Four substantive approaches have been completed; no final unsuccessful disposition is made.
