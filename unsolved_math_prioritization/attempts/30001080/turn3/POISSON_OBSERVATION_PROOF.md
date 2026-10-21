Corrected assembly note (2026-10-06): C: canonical probability, strict point-only preserving Markov tests. The complete frozen family body below is retained literally as a credited proof input, SHA256 bd5eb9048439f6e6cac903e0b44b0277180e360dc94439f8eab34fac19efeeef, 9,919 bytes. Its original candidate/pending-review language is historical and is superseded by the exact scoped adversarial credits in independent_review/SCOPED_REVIEW_CREDITS.json. The C-family phrase about replacing original B concerns its strict repair target; in this corrected author tree B is retained as a separately scoped intensity-background theorem. No global review or full non-discrete allocation conclusion is inferred.

---

# Candidate strict Cox-observation repair

Repair campaign turn 3/5. Independent approach: symmetrize the observation reversal and use identifiability of two Poisson laws. This candidate does not use intensity-dependent gates, does not enlarge the auxiliary state, and does not infer an infinite claim from finite controls. It requires adversarial verification before promotion. Original author theorem B is replaced, not reinterpreted.

## 1. Exact theorem

Let G be locally compact, second countable, Hausdorff and Abelian. Let M be the space of locally finite Radon measures with its usual Borel/evaluation sigma field. Let P be a probability law on M excluding the zero measure. For every invariant, point-configuration-only, counting-measure-preserving Markov transport T, put

    K_T(alpha,s,A) = integral T(eta+delta_s,s,A) Pi_alpha(d eta).

Suppose

    integral P(d alpha) integral f(theta_s alpha) K_T(alpha,0,ds)
      = integral f(alpha) P(d alpha)                         (H)

for all nonnegative Borel f and all such T. Then P satisfies the full canonical Mecke reversal identity and is mass-stationary. Conversely, mass-stationarity implies (H) by the credited 2011 Section 4 and transport invariance results.

The sufficient family below consists of genuine Markov transports on the counting configuration alone. It is contained in the strict constant-X specialization of final Last–Thorisson 2011 Remark 4.8, equation (4.7). It is not a family of deterministic allocations or singleton matchings; whether a source requires that still narrower class is a separate coverage question. No auxiliary X theorem is asserted here.

## 2. Entirely observable preserving transports

Fix a symmetric compact neighborhood C of zero. For a locally finite input measure nu and s,t in G set

    a_C(nu;s,t) = 1_{s != t} 1_C(t-s)
                 / [(1+nu(s+C))(1+nu(t+C))].

Let J(nu,t)=(theta_t nu,-t), an involution. Let b:M x G -> [0,1] be any Borel J-invariant function. Define

    j_b(nu;s,t) = a_C(nu;s,t) b(theta_s nu,t-s),
    r_b(nu,s) = integral j_b(nu;s,t) nu(dt),
    T_b(nu,s,dt) = j_b(nu;s,t) nu(dt)
                    + (1-r_b(nu,s)) delta_s(dt).             (1)

Every quantity in (1) is a function of nu and the starting location only. Neither P nor alpha enters the rule. Local finiteness makes the denominators finite and positive. The row bound is

    r_b(nu,s) <= nu(s+C)/(1+nu(s+C)) <= 1.

The function j_b is symmetric in s,t: J-invariance of b changes (theta_s nu,t-s) to (theta_t nu,s-t). It is translation-covariant. Tonelli and symmetry give

    integral T_b(nu,s,A) nu(ds) = nu(A).

Thus (1) is invariant, preserving and Markov for every locally finite nu, in particular every counting measure including multiple atoms. No stationary grid, marks, labels, or original intensity background is used.

## 3. Conditional Poisson Mecke, with two inserted endpoints

For s != 0, write I_s(eta)=eta+delta_0+delta_s, and set

    w_C(eta,s)=a_C(I_s(eta);0,s).

Projection of (1), followed by the ordinary Poisson Campbell–Mecke identity, gives the off-diagonal density

    K_b(alpha,0,ds)
      = alpha(ds) integral w_C(eta,s) b(I_s(eta),s) Pi_alpha(d eta),
                                                        s != 0. (2)

The rest is holding mass at zero. For atomic alpha, both insertions are still present in (2); no singleton or simplicity hypothesis is made. The conditional identity is a property of Pi_alpha and does not assume P mass-stationary.

Let

    c(d alpha,ds) = P(d alpha) alpha(ds),
    R_0(alpha,s) = (theta_s alpha,-s),
    c^R = (R_0)_* c.

On the observation space (alpha,nu,s), define

    L(d alpha,d nu,ds)
      = c(d alpha,ds) Pi_alpha{eta:I_s(eta) in d nu},
                                                        s != 0.

Let R(alpha,nu,s)=(theta_s alpha,theta_s nu,-s). Let J also denote the observation-only involution

    J(alpha,nu,s)=(alpha,theta_s nu,-s).

Both preserve the domain s != 0. Poisson translation covariance implies

    R_*L = c^R(d alpha,ds) Pi_alpha{eta:I_s(eta) in d nu}.  (3)

The observable weight a_C(nu;0,s) is invariant under both R and J and is strictly positive for every s in C excluding zero. Let M=a_C L. By (2) and the row bound, M has total mass at most one. Its reversal R_*M also has mass at most one.

Applying (H) to bounded f and subtracting the finite holding term proves

    integral f(alpha) b(nu,s) M(d alpha,d nu,ds)
      = integral f(alpha) b(nu,s) (R_*M)(d alpha,d nu,ds) (4)

for every bounded f and every observable J-invariant b in [0,1]. In deriving (4), b(theta_s nu,-s)=b(nu,s). The intensity alpha occurs only in the permitted output test f, never in the transport gate.

## 4. Observable symmetrization and positive deweighting

For any Borel observation set E, the function

    b_E(nu,s) = [1_E(nu,s)+1_E(theta_s nu,-s)]/2

is allowed. In (4), choose f=1_A. Uniqueness of finite measures on product rectangles gives

    M + J_*M = R_*M + J_*R_*M.                           (5)

This is an equality of positive finite measures, not a formal cancellation of infinite signed Campbell measures. Since a_C is observable and J-invariant, (5) says

    a_C (L+J_*L) = a_C (R_*L+J_*R_*L).

Integrate min(n,1/a_C) and let n tend to infinity. On s in C excluding zero this yields the equality of positive measures

    L+J_*L = R_*L+J_*R_*L.                               (6)

Infinite values after deweighting are permitted. The passage is valid because all measures are nonnegative and the same positive weight occurs on both sides. No convergence of a single Poisson realization to alpha is claimed.

## 5. Two Poisson laws force edge reversal

Let I(alpha,s)=(alpha,-s), and write c^I=I_*c and (c^R)^I=I_*c^R. Restrict all four measures to s in C excluding zero. They are sigma-finite. For c use a compact exhaustion C_n and sets {alpha(C_n)<=k} x C_n; P is finite. Images under Borel involutions remain sigma-finite. A finite sum of sigma-finite measures is sigma-finite by intersecting their countable finite covers. Therefore

    lambda = c + c^I + c^R + (c^R)^I

is a common sigma-finite dominating measure on (alpha,s). Let u,v,u',v' be their respective Radon–Nikodym densities. All lie in [0,1].

Under J, an edge originally at -s is translated by -s, so its residual Poisson intensity becomes theta_{-s} alpha. Removing the two deterministic inserted endpoints from nu in (6) gives, for lambda-almost every (alpha,s),

    u Pi_alpha + v Pi_{theta_{-s} alpha}
      = u' Pi_alpha + v' Pi_{theta_{-s} alpha}.             (7)

For rigor, test (6) against a countable generating class of residual-configuration events and arbitrary base sets, then use Radon–Nikodym uniqueness. A single common lambda-null set suffices. Including the whole configuration space gives

    u+v = u'+v'.                                          (8)

Poisson intensity identifiability: if alpha != beta, some set B in a countable relatively compact generating ring has alpha(B) != beta(B), hence

    Pi_alpha{eta(B)=0}=exp[-alpha(B)]
      != exp[-beta(B)]=Pi_beta{eta(B)=0}.

Combining (7) and (8) therefore forces u=u' and v=v' whenever theta_s alpha != alpha. Thus

    c = c^R on {(alpha,s):theta_s alpha != alpha,
                              s in C excluding zero}.     (9)

This also covers order-two displacements s=-s: if the intensities differ, the two Poisson laws still distinguish them. If they agree, the remaining locus is handled below. There is no orientation selection on infinite orbits, no global pair enumeration, no finite-volume-to-infinite-volume inference, and no reconstruction of alpha from one sample.

## 6. Equal-intensity locus and completion

For fixed alpha, H_alpha={s:theta_s alpha=alpha} is a closed subgroup, since translations are continuous on Radon measures in the vague topology. The restriction alpha|_{H_alpha} is a locally finite translation-invariant measure on the Abelian group H_alpha, hence zero or a multiple of its Haar measure. Haar inversion symmetry gives

    alpha|_{H_alpha}(B)=alpha|_{H_alpha}(-B).

On the period graph R_0 fixes alpha and reverses s. The preceding pointwise statement proves c|_H=c^R|_H without selecting a measurable family of Haar normalizations. At s=0, R_0 is the identity and equality is automatic.

Choose increasing symmetric compact neighborhoods covering G. Equation (9), the period-graph argument, and monotone exhaustion prove c=c^R globally. Equivalently,

    E integral g(theta_s alpha,-s) alpha(ds)
      = E integral g(alpha,s) alpha(ds)

for every nonnegative Borel g. Final Last–Thorisson 2011 Section 2, equation (2.5), identifies this with mass-stationarity under the stated nonzero locally finite probability-law assumptions.

## 7. Scope and exact remaining review work

The mathematical candidate closes the missing point-configuration-only condition for the full projected Markov class in Remark 4.8. It uses the stronger richness of all configuration-only preserving Markov transports; it has not proved that deterministic Cox allocations or the original isolated-singleton matching subclass alone suffice. The probability-law scope is exactly the constant-X assumption P(X in .) sigma-finite in the 2011 source: a nonzero constant-X law must have finite total mass; finite nonzero P rescales to probability. A general sigma-finite canonical-law extension would require careful finite-P localization of (4) and is not included in this frozen theorem.

Required adversarial checks: (i) (3)'s Poisson covariance and endpoint insertion signs; (ii) whether (4) really permits all observable symmetric gates; (iii) (5)'s product-measure uniqueness; (iv) common positive deweighting; (v) all four Campbell measures' sigma-finiteness and conditional RN passage; (vi) the two-law separation; (vii) period-graph inversion; (viii) exact original OWR class coverage. No novelty or publication clearance is asserted.
