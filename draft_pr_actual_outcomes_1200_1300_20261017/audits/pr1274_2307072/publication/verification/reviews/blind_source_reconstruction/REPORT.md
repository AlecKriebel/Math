# Independent source-only reconstruction

Author: independent reconstruction agent for Alec Kriebel. Mathematical derivation completed without exposure to a submitted candidate or another review. This report addresses the literal 2018 source statement; it makes no priority or literature-status claim.

## Exact target and conclusion

Let U={z:|z|<1}, let dA denote unnormalized Euclidean area, and set

    N={v in L-infinity(U;C): integral_U v(z) phi(z) dA(z)=0
       for every analytic phi on U with integral_U |phi| dA < infinity}.

The product in this definition is bilinear: there is no complex conjugation. Extend v by zero off U and use circular principal values

    Bv(z)=-(1/pi) lim_{epsilon down to 0}
          integral_{U minus D(z,epsilon)} v(zeta)/(z-zeta)^2 dA(zeta).

The strong question combines (i) Bv in L-infinity for every v in N and (ii) existence of one finite C independent of v with norm(Bv) <= C norm(v). Both fail. The weaker question about one constant for all v in N intersect C[z,bar z] also fails. For polynomial inputs individually the transform is bounded, so the failure in that weaker class is precisely the absence of a common constant.

A bounded nonpolynomial counterexample is

    v(z)=z/bar z for 0<|z|<1, with v(0)=0.

It has norm(v)=1 and, at every 0<|z|<1,

    Bv(z)=1+2 log|z|.

An explicit polynomial family is, for integers n>=1,

    v_n(z)=z^2 sum_{j=0}^{n-1} (1-|z|^2)^j.

These satisfy v_n in N, norm(v_n)=1, and

    norm(Bv_n)=H_n=sum_{j=1}^n 1/j.

Thus no finite common constant exists, even on this explicit polynomial subclass.

## All analytic L1 tests

More generally put v_g(re^{i theta})=e^{2i theta}g(r) for bounded measurable g on (0,1), assigning any bounded value at 0. For each fixed r<1 and every analytic phi on U, the Taylor series of phi converges uniformly on that circle, so

    integral_0^{2pi} e^{2i theta} phi(re^{i theta}) dtheta = 0.

When phi is area-integrable, |v_g phi| <= norm(g)|phi| makes Fubini applicable over the full disc. Integrating the preceding identity against g(r)r dr proves integral_U v_g phi dA=0. This verifies the complete test class, without replacing it by polynomials or assuming a density theorem.

The nonpolynomial example uses g=1. The polynomial example has

    g_n(r)=1-(1-r^2)^n,

because the finite geometric-sum identity gives v_n=e^{2i theta}g_n(r). Since 0<=g_n(r)<1 and g_n(r) tends to 1 as r increases to 1, its essential supremum is 1. Each v_n is a polynomial in z and bar z, and v_n(0)=0.

## Cauchy potential and sign of the transform

For a bounded compactly supported input define the absolutely convergent potential

    Cv(z)=(1/pi) integral_U v(zeta)/(z-zeta) dA(zeta).

For v_g above, angular integration yields, when 0<r=|z|<1,

    Cv_g(z)=-2z integral_r^1 g(s)/s ds.                     (1)

Indeed, on circles s<r, the geometric expansion of 1/(z-se^{i theta}) has only nonnegative angular powers, and multiplication by e^{2i theta} leaves no constant term. On circles s>r, the expansion -sum_{k>=0} z^k/(s^{k+1}e^{i(k+1)theta}) has a constant angular term after multiplication only for k=1; that term is -z/s^2. These circle integrals, followed by integration with the area factor s ds, give (1). The exceptional circle s=r has radial measure zero. Fubini is justified by absolute integrability of the Cauchy kernel against a bounded input in two dimensions. At z=0 the same potential equals 0. For |z|>1 every source circle is of the first kind, so Cv_g=0 there.

For inputs smooth in a neighborhood of a point, the standard local Cauchy-kernel differentiation identity is

    partial_z Cv(z)=-(1/pi) pv integral v(zeta)/(z-zeta)^2 dA(zeta).

Here partial_z=(partial_x-i partial_y)/2. For a direct justification, fix a small disc about the evaluation point and subtract the local constant v(z) on that disc. The Cauchy potential of the constant disc input has partial_z derivative zero in the disc, and its centered circular kernel integral is zero. For the remaining input, its numerator is O(|w|) near the point. In the difference quotient with increment h, the integral over |w|<2|h| contributes O(|h|^2); on |w|>=2|h|, expansion of the Cauchy kernel leaves a derivative remainder O(|h|^2 log(1/|h|)). After division by |h| both remainders vanish. This proves complex differentiability of this remainder at the point and gives the absolutely convergent differentiated integral there. Restoring the constant part proves the claimed partial_z/principal-value identity and fixes the negative sign. All points used below are points of local smoothness. No convention about a noncircular cutoff is needed.

If g is smooth near r>0, differentiating (1) gives the radial formula

    Bv_g(z)=g(r)-2 integral_r^1 g(s)/s ds.                 (2)

In particular, for g=1 one has Cv(z)=2z log|z|=z log|z|^2 and

    partial_z Cv=1+2log|z|,
    partial_bar_z Cv=z/bar z.

These identities also provide an elementary sign and normalization check.

## Essential norm, origin, and boundary

For v=e^{2i theta}, the principal value at z=0 is not finite: the truncated integral is 2log(epsilon), which tends to minus infinity. This isolated failure is not the reason for the negative L-infinity result. Formula (2) holds at every nonzero point of U. Given any M>0, choose R=exp(-(M+1)/2). Then Bv(z)<-M on 0<|z|<R, a set of positive area. Hence the essential supremum of |Bv| is infinite, under the usual almost-everywhere definition of the transform.

The choice of v(0) changes no integral or essential norm. The potential zlog|z|^2 tends to 0 at the origin and at the unit boundary; zero extension outside U causes no boundary jump in the potential. Its interior derivatives grow only logarithmically near 0, so they are locally integrable, with no point mass there. Off the closed disc the potential and its transform both vanish. Unit-circle values are outside U and form a plane-null set, so any questions about principal values exactly on that circle cannot alter either conclusion. In particular, the counterexamples fail already in the interior, whether the output norm is interpreted over U or over the whole plane after zero extension.

For every polynomial v_n, the integrand at the origin is absolutely integrable because v_n(zeta)=O(|zeta|^2). Writing t=|z|^2, q_n(t)=1-(1-t)^n, formula (2) gives

    Bv_n(z)=F_n(t):=q_n(t)-integral_t^1 q_n(u)/u du.      (3)

The quotient q_n(u)/u equals sum_{j=0}^{n-1}(1-u)^j, a polynomial, including at u=0. Thus (3) is continuous on the closed interval 0<=t<=1 and agrees with the actual principal value at 0. In particular,

    Bv_n(0)=-integral_0^1 sum_{j=0}^{n-1}(1-u)^j du
           =-sum_{j=1}^n 1/j=-H_n.

Continuity on a whole neighborhood of 0 makes this a lower bound on the essential supremum, not merely a pointwise value. In fact, for 0<t<1,

    F_n'(t)=n(1-t)^{n-1}+q_n(t)/t >0,

and its endpoint values are -H_n and 1. Since H_n>=1, its essential maximum absolute value is exactly H_n. Finally H_n>=integral_1^{n+1} dx/x=log(n+1), so these norms diverge.

## Individual polynomial boundedness

For completeness, the boundedness part of the polynomial question is true for every polynomial input, with or without the annihilator restriction. Angular integration gives, for integers a,b>=0 and z in U,

    C(z^a bar z^b)(z) = z^a bar z^{b+1}/(b+1)
                       - z^{a-b-1}/(b+1), if a>=b+1;
                     = z^a bar z^{b+1}/(b+1), if a<=b.

The expression z^a bar z^b on the left denotes the input on U, extended by zero, not a global polynomial input on the plane. Each displayed potential is a polynomial in the interior. Its partial_z derivative is likewise a polynomial and equals the circular principal value throughout U. By linearity, the transform of each polynomial is bounded on U. This does not provide a uniform constant as degree and coefficients vary; the preceding family disproves one.

## Independent checks and self-audit

The proof uses direct angular annihilation for all analytic L1 tests and a separate Cauchy-potential calculation. It does not use the candidate, a sibling review, a current source edition, or an unsupported norm theorem. Finite checks in CHECKS.py use exact rational arithmetic for coefficient identities, harmonic-number growth, and polynomial origin integrals for n=1,...,40. A separate direct numerical integral in coordinates centered at the evaluation point tests four polynomial inputs and the singular input at three nonzero radii. All passed in normal Python, -O, and -OO. The largest numerical discrepancy was below 0.000298. They are checks, not replacements for the proof. All executable guards use explicit exceptions and remain active under Python -O and -OO. See VALIDATION.md for the authored run summary.

Potential failure points checked explicitly: no conjugation in the pairing; no use of monomial tests alone; zero extension is part of the operator; the origin is not used as a lone essential-norm witness; polynomial origin values come with continuity; boundary values have measure zero; one uniform C is distinct from each polynomial having its own finite norm; the polynomial family really has norm one; and the negative sign matches the source kernel.

Strongest verified mathematical result: the explicit counterexample and the exact polynomial norm formula above settle both literal uniform-boundedness questions negatively. Remaining mathematical gap: none identified for the literal statement. No assertion about novelty, historical resolution, intended unprinted variants, or publication suitability is made here.

## Exposure chronology

The first inputs read were the project AGENTS.md and the designated original-problem JSON. A fresh download of https://arxiv.org/pdf/1809.07200v2 was rendered at PDF page 184, and the printed page 183 notation was inspected visually. The JSON's prior triage text supplied no proof. This reconstruction has not read any candidate, submitted/, current_edition/, sibling review, root report, PR body, or other research material. No comparison has been performed. The accompanying seal will record the authored report hash before any such exposure; the parent can compare later without changing this original derivation.
