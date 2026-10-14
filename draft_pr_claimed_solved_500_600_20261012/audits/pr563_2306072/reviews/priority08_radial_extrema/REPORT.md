# PR563 / 2306072: full-source priority audit of the maximum-radial-angle family

Audit date: 2026-10-13. Assigned review family: `priority08_radial_extrema`.

## Bounded conclusion

The complete Duren–Leung–Schiffer (DLS, 1983) and Zhang–Ma (ZM, 1991) articles contain no construction that gives either of the two nonmonotonicity conclusions in Hayman–Lingham Problem 6.72. Their classification mechanism begins with **exact attainment of magnitude pi/4 at the finite slit tip**. It supplies a second maximizing Möbius transform and a second differential equation, then forces a half-line in the cases classified. Such half-lines have monotone polar argument and monotone signed and unsigned radial angle; the derivation below checks both signs and the limiting case.

The candidate's functional is in the exact finite-coefficient class of DLS Theorem 3. That theorem proves strict tip inequality, so the equality classification has a false premise for every candidate maximizer. The candidate also has rational type, and its rational differential has no double zeros; checking those additional hypotheses does not restore the absent equality premise. This conclusion is based on the full articles, not their titles or abstracts.

DLS supplies prior general support geometry, the rational-type definition, coefficient extraction, strict tip-angle bounds, and an equality-specific analytic-continuation mechanism. ZM claims the rational-type equality classification without DLS's no-double-zero restriction. An adversarial reading finds one omitted local branch case in ZM's printed proof (detailed below); that is a printed proof-elimination gap, **not** a refutation of its theorem. Neither the candidate proof nor this source-scoped priority verdict depends on resolving the general rational-type classification.

This audit does not certify universal literature clearance, firstness, a still-open-in-2026 assertion, or the entire candidate proof. The full source-critical 2014 commentary remains unread. It has not been assumed to repeat the 1983 article. Other background papers and the final publication decision remain with the root audit.

## Identity, inputs and independence

DLS is P. L. Duren, Y. J. Leung and M. M. Schiffer, *Support Points with Maximum Radial Angle*, *Complex Variables, Theory and Application* 1 (1983), 263–277, DOI [10.1080/17476938308814018](https://doi.org/10.1080/17476938308814018). The supplied PDF has 16 pages: publisher wrapper, then all 15 article pages. The wrapper's online publication date in 2007 is not the article's 1983 publication year. Article p.263 gives receipt on 16 July 1982. SHA-256: `6de1be27237a8d0a2f4fe0a3987a3e4276160f685d5dddecbef2c82c538300bc`.

ZM is **Yulin Zhang and Jinxi Ma**, in that order on article p.598, *A Note on Support Points with Maximum Radial Angle*, *Journal of Mathematical Analysis and Applications* 160 (1991), 598–601, DOI [10.1016/0022-247X(91)90330-3](https://doi.org/10.1016/0022-247X(91)90330-3). The supplied PDF has exactly four article pages, with receipt on 20 March 1990. SHA-256: `7bf8cc64c51f4e0b14bb3e18d8278b8bb1e897bfb9aaec27ececb0e9235512b2`.

Both supplied PDFs were read in full through extracted text **and full-page rendered images**, including every proof, equation, remark, example reference, acknowledgement and bibliography. Visual reading corrected extraction damage in equation numbers, signs, phi/Phi, the tilde equations, exponents, author names and article pagination. The complete original problem page was also visually inspected: printed p.143 is PDF page 144 of the Hayman–Lingham PDF.

The independent theorem/proof scope and angle derivations were recorded in `SOURCE_INDEPENDENT.md` before any previous review was consulted. No previous review was needed or read in this audit. The frozen original `PROOF.md` and current manuscript were then compared. Hashes and coverage are in `SOURCE_IDENTITY.json`. The current manuscript read was preserved privately in ignored `.cache/support_slit_read.tex`; the receipt refers to that snapshot, because the root may continue editing the preparation draft.

Only this assigned review folder was written. The branch remained `main`; no canonical source, index, branch, remote, release or publication was modified. The root owns commits and pushes. No external individual, other review family or other agent was contacted; only the parent received findings.

## Exact target and angle conventions

HL6.72 asks whether the analytic arc omitted by a support point of S must have monotonic argument, and whether the angle between its radius and tangent vectors must be monotonic. Its parenthetical statement says that the second property implies the first, and credits Brown for both properties for point evaluations. Its update records no progress reported to those authors; that historical update alone is not a current-priority certificate.

For an actual omitted arc parametrized outward with increasing modulus, write

\[
 w(r)=r e^{i\theta(r)},\qquad
 \phi=\arg w_r,\qquad
 \beta=\phi-\theta=\arg(w_r/w).
\]

The polar argument is theta, the tangent direction is phi, and the signed radial angle is beta. DLS p.264 and ZM p.598 define their radial angle as `arg(dw/w)`, hence beta, not theta or phi. The support bound selects the branch `|beta|<pi/4` in the regular interior. Directly,

\[
 \frac{w_r}{w}=\frac1r+i\theta_r,
 \qquad \beta=\arctan(r\theta_r),
 \qquad \theta_r=\frac{\tan\beta}{r}.
\]

Polar monotonicity concerns the sign of beta. Radial-angle monotonicity concerns beta's variation. A bound on beta's magnitude supplies neither sign constancy nor a sign for its derivative. From the trajectory condition

\[
 \Phi(w)(dw/w)^2>0,
\]

one obtains

\[
 \beta=-\tfrac12\arg\Phi(w),\qquad
 \beta_r=-\tfrac12\Im\left(\frac{\Phi'(w)}{\Phi(w)}w_r\right),
\]

with the support branch; this derivative has no automatic one-sided sign. A tangent-direction turning point is a statement about phi, and cannot replace a checked statement about theta or beta.

Reversing the traversal of an arc preserves whether any of these functions is monotone in either direction. Reversing only the directed tangent makes its ordinary angle with the radius the supplement of the outward angle, which also preserves nonmonotonicity. The candidate explicitly handles outward signed beta and unsigned `|beta|`.

## Full DLS coverage and proof scope

| Printed pages (PDF pages) | Complete material inspected | Mechanism and exact scope |
|---|---|---|
| Wrapper (1), 263–265 (2–4) | Identity, normalization, support-point definition, examples and introduction | All support points omit one analytic arc with increasing modulus; radial-angle magnitude is strictly below pi/4 in the interior. Koebe rays and prior Brown/Pearce derivative and evaluation problems motivate the **tip-equality** question. Brown's near-equality numerical observation is reported, not an exact equality example. |
| 265–267 (4–6), Theorem 1 | Complete Möbius-transform derivation, equations (2)–(11) | Equality `Re Phi(w0)=0` makes `ftilde=w0 f/(w0-f)` another maximizer for the same L. Pulling its trajectory back yields a second equation. Rational Phi then makes the equality slit algebraic. No converse extremality assertion is given for arbitrary trajectories. |
| 267–268 (6–7), Theorem 2 | Complete point-evaluation contradiction | For `L(f)=f(xi)`, quotient of the two equations makes a half-line; its original equation forces a radial ray. This contradicts a pi/4 tip and proves a **strict bound**, not a bent equality construction. The remark that numerical near-equality is misleading is a scope warning, not a nonmonotonicity result. |
| 268–271 (7–10), Theorem 3 | Complete coefficient expansion, paired equations, all continuation branches, unique germ and monodromy argument | Every finite coefficient functional has **strict** tip inequality. Under assumed equality, `Phi=-P_n(1/w)` and two rational differential equations force an algebraic continuation. All sheets vanish at the origin and have one local germ, yielding a rational map. A cited coefficient classification makes it a Koebe rotation, giving a contradiction. |
| 271–272 (10–11), Theorem 4 and corollary/converse remark | Complete rational-function discussion | Srebro's theorem, quoted here rather than reproved, classifies rational f omitting an arc as a Marty transform of Koebe with a half-line. Rational **f** is not rational **type L**. The converse remark says half-lines with the support angle bound and appropriate conformal radius can be omitted by rational support points. They are all monotone examples. |
| 272–274 (11–13), Theorem 5 | Rational-type definition, complete proof, all three alternatives (22)–(24), final remark | Rational-type L **and** no double zeros of Phi **and** tip equality imply a half-line. The proof centers the continuation at z0 (finite-tip preimage). A nonzero other sheet whose Phi has a double zero is exactly the case the stated restriction removes. The remark that the restriction is probably unnecessary is conjectural in DLS. |
| 274–275 (13–14), §7 | Complete derivative-functional application | For `L=e^(-i alpha) f'(xi)`, `Phi=e^(-i alpha)BC(B-2w)/(w-B)^2`, B=f(xi), C=f'(xi). The absence of double zeros lets Theorem 5 apply. Tip equality can occur only for the previous half-line derivative-angle extremum. |
| 275–277 (14–16), Theorem 6 | Complete quarter-plane proof, limit/asymptote calculation and concluding suggestion | For arbitrary L with exact tip equality, the slit stays in a quarter-plane based at w0 bounded by `w0+w0 t` and `w0±i w0 t`. Its bisector is the tip tangent and is parallel to the asymptote. The suggestion that every such slit is a half-line is not proved for arbitrary L. |
| 277 (16) | Acknowledgements and all ten references | Prior references concern support points, Brown's two problems, Duren's 1981 article/book, Pearce, Schaeffer–Spencer, Schiffer, Schober and Srebro. No additional nonmonotone construction is supplied in the bibliography. Referenced papers are leads, not silently read substitutes. |

The central equality step is checkable. DLS use

\[
 f-\widetilde f=\frac{f^2}{f-w_0},\qquad
 \widetilde w=\frac{w_0w}{w_0-w}.
\]

Thus `Re Phi(w0)=0` gives `Re L(ftilde)=Re L(f)`. Their exact pullback gives

\[
 [\Phi(w)-\Phi(w_0)](1-w/w_0)^{-2}(dw/w)^2>0,
\]

and division by the original condition gives equation (11),

\[
 \frac{\Phi(w)}{\Phi(w)-\Phi(w_0)}(1-w/w_0)^2>0.
\]

Rational Phi alone gives only the original equation; it does not supply the second extremizer or equality condition. Extending a formal solution past the actual finite tip does not change that scope.

## Full ZM coverage, claimed extension and precise printed-proof gap

All four pages were read visually in full. Page 598 fixes the support/radial-angle conventions and restates DLS's equality-conditioned second equation. Page 599 states the rational-type classification **without** DLS's double-zero restriction and begins the full proof. Page 600 contains all branch exclusions and the unique-germ argument. Page 601 finishes monodromy/rationality and invokes DLS Theorem 4; its two references are Duren's 1983 book and DLS. The source has no additional construction, numerical example, independent general monotonicity conclusion or nonmonotonicity counterexample.

Let z0 be the finite-tip preimage and z1 the infinity preimage, and put `u=1/w`, `u0=1/w0`, `P(u)=Phi(1/u)`. The printed equations become

\[
 P(u)(u'/u)^2=z^{-2}Q(z),\tag{ZM \widetilde5}
\]
\[
 [P(u)-P(u_0)](1-u_0/u)^{-2}(u'/u)^2
 =z^{-2}R(z).\tag{ZM \widetilde6}
\]

Q has a double zero at z0 and is nonzero at z1; R has a double zero at z1 and is nonzero at z0. P has a simple zero at u=0, `P(u0)≠0`, `P'(u0)≠0`. Their quotient is

\[
 \frac{[P(u)-P(u_0)]u^2}{(u-u_0)^2P(u)}=\frac{R(z)}{Q(z)}.\tag{ZM 7}
\]

ZM shift the sheet analysis from z0 to z1. If every continuation branch satisfies `u(z1)=0`, the left side has a nonzero linear term at u=0 because P has a simple zero there and P(u0) is nonzero. It supplies one analytic germ with `u=c(z-z1)^2+...`; the usual return-germ monodromy argument then produces a rational f and a half-line via DLS Theorem 4.

The printed elimination of all other sheets is incomplete. Its case (9) is

\[
 u=\omega+c(z-z_1)^\alpha+\cdots,
 \quad \omega\ne0,u_0,\quad c\ne0,\quad\alpha>0.
\]

For `P(omega)≠0`, the first equation requires `2(alpha-1)=0`, hence alpha=1. The source includes this as its `m=0` case and asserts that the second equation has order `2(alpha-1)=2`. That assertion presupposes `P(omega)-P(u0)≠0`. If `P(omega)=P(u0)` and `P-P(u0)` has a zero of order n at omega, the second equation instead has order

\[
 n\alpha+2(\alpha-1)=2.
\]

With alpha=1, **n=2 passes both required orders**. This branch has not been eliminated. It is the double-level-value case of `P-P(u0)`, not a zero of P itself. The other pole and zero cases on that page do not cover it.

There is an explicit checkable local witness satisfying the cited nonzero premises:

\[
 P(u)=i+(u-1)^2\left[(-1-i/2)u^2+(2+3i/2)u-i\right],
 \qquad u_0=2,\quad\omega=1.
\]

Then

\[
 P(0)=0,\quad P'(0)=2+7i/2\ne0,
\]
\[
 P(2)=P(1)=i,\quad P'(2)=-2-i/2\ne0,
 \quad P'(1)=0,\quad P''(1)=2.
\]

In particular P has the required simple zero at 0, P(u0) is nonzero and purely imaginary, and `P-P(u0)` has exactly a double zero at omega. For `z1=1`, the local branch `u=1+c(z-1)+...` with `c^2=-i` has

\[
 Q(1)=P(1)c^2=1,
 \qquad R(z)=-(z-1)^2+\cdots.
\]

Along the unit circle `z=e^(is)`, the latter has leading term `s^2>0`. Thus even the leading boundary positivity requirement does not immediately repair the missing local-order case.

**Limit:** this witness is an algebraic/local-order and leading-sign compatibility check. It is not a constructed global rational-type support functional, not a proof that all higher coefficients give positive real Q/R on the circle, and not a counterexample to ZM's theorem. A repair could use additional global support/rational-type information, but the printed proof does not provide it. DLS Theorem 4/Srebro and other cited standard geometry are also external proof dependencies. The root independently read the relevant ZM pages and DLS Theorem 3 after this independent finding and concurred with precisely this restricted gap assessment.

No priority or candidate-validation claim here is transferred to solving that unrelated general theorem. The finite-coefficient candidate already fits DLS Theorem 3, and its proof never invokes ZM's classification.

## Half-lines cannot settle either target negatively

For an outward half-line `w(t)=a+bt`, t≥0, rotate by b and write `a/b=x+iy`. The support angle bound gives `x>0`, `|y|≤x` at the tip. Changing polar lifts adds constants only. Direct calculation yields

\[
 \theta_t=-\frac{y}{(x+t)^2+y^2},\qquad
 \beta=-\arg(x+t+iy),\qquad
 \beta_t=\frac{y}{(x+t)^2+y^2}.
\]

For y>0 theta decreases and beta increases toward zero; for y<0 the signs reverse. In both cases `|beta|` decreases toward zero. If y=0 both angles are constant. If `|y|=x` the tip has magnitude pi/4 and the same monotonicity statements hold, with a strict angle bound for t>0. The tangent direction phi is constant.

The converse half-line support points discussed in DLS therefore demonstrate limiting-angle attainability **within a monotone family**. They are not hidden counterexamples to HL6.72. The quarter-plane theorem alone is weaker still: containment and parallel asymptotic/tip tangents do not assert a monotonic theta or beta for all its possible curves.

## Exact comparison with the candidate

The frozen original and read current manuscript claim that **every** global maximizer of

\[
 L(f)=a_2(f)+i\varepsilon(a_4(f)-3a_3(f)),
 \qquad \varepsilon=10^{-24},\quad\eta=10^{-12},
\]

omits an actual slit with nonmonotone theta, beta and `|beta|`. No uniqueness of a maximizing selection is assumed.

The functional is continuous, nonconstant and finite-coefficient, with `lambda2=1`, `lambda3=-3i eps`, `lambda4=i eps≠0`. DLS Theorem 3 therefore applies directly to every maximizer and guarantees **strict** `|beta(w0)|<pi/4`. ZM's published theorem and DLS Theorem 5 have no equality premise to act on.

The degree-four extraction was checked independently and exactly:

\[
 \Phi(w)=-\frac{a}{w}-\frac{b}{w^2}-\frac{c}{w^3},
\]
\[
 a=1+i\varepsilon A,
 \quad A=2a_3+a_2^2-6a_2,
 \quad b=i\varepsilon B,
 \quad B=3a_2-3,
 \quad c=i\varepsilon.
\]

Thus L is rational type. The numerator of Phi is `-(a w^2+bw+c)`. The candidate's uniform bounds `|A+2|<106 eta`, `|B-3|<24 eta` imply `|A|<3`, `|B|<4`. Its discriminant is

\[
 \Delta=b^2-4ac=-4i\varepsilon+\varepsilon^2(4A-B^2),
\]

so `|Delta+4i eps|<28 eps^2<4 eps`; Delta is nonzero. The numerator has no double zero. Phi has a pole of order three at 0 and a simple zero at infinity. Even the stricter original DLS Theorem 5 thus has its rational/no-double-zero premises, **but lacks exact tip equality**.

The candidate's mechanism is quantitative perturbation of the a2 extremum near Koebe, control of every actual maximizer by coefficient/area estimates, an actual-tip radius bound, and controlled inversion of one Schiffer differential in `w=-v^(-2)`. It does not use a second equality-generated maximizing Möbius transform or paired differential equations to force rationality.

At the Koebe limiting coefficients it has

\[
 P(v)=1+i\varepsilon(-2-3v^2+v^4)+O(\varepsilon\eta),
\]
\[
 V(t)=t+i\varepsilon d(t)+O(\varepsilon\eta),
 \quad d(t)=t+t^3/2-t^5/10,
\]
\[
 Z(t)=tV'(t)/V(t)
 =1+i\varepsilon q(t)+O(\varepsilon\eta),
 \quad q(t)=t^2-2t^4/5.
\]

The exact endpoint values are `q(1)=3/5` and `q(7/4)=-441/640`; the stated error `2000 eta=2e-9` preserves opposite signs with margin eps/2. The outward tangent is `-W'`, since increasing t goes inward. Therefore

\[
 \theta_t=-2\Im Z/t,\qquad\beta=\arg Z.
\]

The candidate's opposite Im Z signs prove a theta derivative reversal, while beta's two signs and its limit zero at infinity preclude either monotone direction. A zero between opposite signed angles makes `|beta|` positive at both endpoints and zero in between. These are the target quantities, not a substituted tangent-direction quantity.

The degree-four term matters. For comparison, a perturbation `a2+i eps(mu a3+lambda a2)` with real mu, lambda has limiting `P0(v)=4mu+lambda-mu v^2` and first-order `q(t)=mu t^2/3`, which has a constant sign. The extra fourth-degree coefficient yields the quartic term allowing the demonstrated reversal. This first-order comparison is explanatory; it does not assert a general lower-degree monotonicity theorem without reading those proofs.

The actual-tip issue is also separate from equality classification. The candidate bounds its true tip radius by `7/25+7eta<3/10` and its entire witness arc radius by `|W|>25/81`. Their exact gap is `25/81-3/10=7/810`. Combined with its regular natural coordinate, the connected open/closed continuation argument keeps the witness inside the actual omitted slit, not a fictitious extension beyond its tip. This audit checked that finite radius arithmetic and the orientation algebra; it is not a fresh complete-package validation of every analytic estimate.

Both articles quantify over any support point satisfying their assumptions. The candidate quantifies over all maximizers by uniform estimates. Multiple maximizers do not widen an equality theorem to a strict-tip case or undermine the scope distinction.

## Checks, artifact boundaries and final disposition

`python3 exact_checks.py` succeeds with only standard-library exact fractions; `EXACT_CHECKS.json` records the result. It checks the complete z2/z3/z4 coefficient identities and candidate Phi, the source omitted branch and polynomial witness, its leading positivity, discriminant nonvanishing under the candidate's recorded bounds, the opposite endpoint sign margins, the exact tip/witness radius gap, and the role of the fourth-degree term. These finite checks supplement the derivations; they do not prove global extremality, the classical analytic theorems, global realization of the source-gap witness, the entire candidate proof, or historical novelty.

Authored outputs are sealed by `SEAL.json`; raw PDF/text/rendered copyrighted material and the private read snapshot stay in ignored `.cache/` and are excluded from the seal/publication output set. The supplied source PDFs were not copied into authored outputs.

**Disposition:** complete-source comparison in this specific family yields **no direct earlier negative answer or identical sign-reversal construction found**. Attribute DLS's classical geometry, rational-type formulation and coefficient strict-tip bound. Cite the ZM result as a published equality-classification claim with the bounded printed-proof qualification preserved in audit notes. This family alone does not justify universal priority clearance or final publication promotion. The unread 2014 commentary and other close sources remain explicit root-level gaps.
