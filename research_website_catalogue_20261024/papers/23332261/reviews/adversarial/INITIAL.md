# Source-only adversarial INITIAL — annular Martin kernel

This is a scientific falsification family, independently reconstructed from the full actual five-page PDF and all171 TeX lines. All five fresh own source rasters were individually viewed. No support/native program, supplied result, archived review, README opinion, current other-family/root finding or foreign primary body was read. Source-handoff metadata alone preceded the manuscript. The own controls and mathematical results below are frozen before such exposure.

## Claim and attempted failure mechanisms

For D={1<|z|<e}, a=e^(1/2), inner-boundary point xi=-1, the normalized MINIMAL Martin kernel K_xi(a)=1 has K_xi(z)<H_a(z) at every z in some punctured neighborhood of a. H_a is the supremum of strictly positive harmonic functions normalized by h(a)<=1. The conclusion is local isolated contact, not absence of all farther contact. It rules out any equality curve with non-base points arbitrarily close to a, without needing differentiability or a particular Green-line construction. The extra source claim is that a polar-puncture domain already gives a broader negative example; it does not supply the smooth-annulus result or historical priority.

Main attacks were: a wrong Poisson normalizing factor; failure of minimality; tangential source approaches defeating the Martin limit; cancellation in tiny P(A); a missing sign in Px; finite-direction evidence substituted for an all-direction bound; competitors failing global positivity or periodicity; envelope differentiability smuggled in; a common Taylor radius absent; and the distinction between local isolation and global contact. None is assumed away. Original question wording and any priority assessment remain a later primary-interface check.

## Independent support-function optimization

Use cylinder x=log|z|, y=arg z mod2pi. At A=(1/2,0), the four explicit admissible competitors have gradients (1,0),(-1,0),(0,b),(0,-b), b=1/(2cosh(1/2)). Their values equal1. The radial pair is between1/2 and3/2; the transverse pair is at least1/2 because |sin y|cosh(x-1/2)<=cosh(1/2). Both Laplacians vanish directly, so no positivity or topology hypothesis is missing.

Write the kernel gradient (-c,0). The maximum gradient gap on a displacement (u,v) is M+cu, M=max(|u|,b|v|). Rather than repeat the manuscript's successive rough norm estimates, minimize this support function exactly on u^2+v^2=1. For u<0 put s=-u, t=|v|. On s>=bt the value is (1-c)s and is minimized at s=b/sqrt(1+b^2). On s<=bt the value is bt-cs, decreasing as s approaches that endpoint. For u>=0 it is no smaller. Thus, for 0<=c<1,

    min_unit_direction max_gradient_gap = b(1-c)/sqrt(1+b^2).

The source derivative calculation can be checked independently: at x=1/2 the strip denominator is2cosh(pi t), its x-derivative2pi, and its numerator derivative0. Thus p_x=-pi/(2cosh(pi t)^2). Pairing the odd y derivatives cancels them, and c=pi S2/S1, with positive q_k=sech((2k-1)pi^2). A positive weighted average gives c<=pi sech(pi^2)<8/83. The elementary cosh series gives b>=3/8, not merely the manuscript's weaker b>1/4. Since b/sqrt(1+b^2) is increasing,

    margin >=225/(83 sqrt(73)) >1/4,

where the last check is the exact integer inequality810000>502897. This is a uniform real-direction derivation. The exact4224 integer directions in the own program corroborate it but do not prove it. Negative controls produce zero gap at c=1, negative gap at c=3/2 in direction(-1,0), and zero transverse first-order gap if the transverse pair is removed. Thus one cannot silently drop strict interiority or one competitor family in this mechanism.

All four h_j-K are C2 near A. A common compact Hessian bound C makes their remainders at most C|d|^2. The support lower bound then supplies max(h_j-K)>|d|/4-C|d|^2>0 at all sufficiently small nonzero d. Taking a maximum over four actual admissible functions establishes the claim without differentiating H_a or interchanging a supremum with differentiation. The exponential chart is a local diffeomorphism at a, so a genuine cylinder neighborhood maps to a genuine annular neighborhood.

## Distinct Fourier-cylinder cross-check

Separation of variables for the inner-boundary Dirichlet density on a circumference2pi cylinder gives

    P_eta(x,y)=(1-x)/(2pi)+(1/pi) sum_{n>=1} sinh(n(1-x))/sinh(n) cos(n(y-eta)).

This follows by solving u_n''-n^2 u_n=0, u_n(0)=1,u_n(1)=0 for each boundary Fourier mode; the constant mode is1-x. It is a different representation from the source's periodized strip images. At A with eta=pi,

    pi P(A)=1/4+(1/2)sum_{n>=1}(-1)^n sech(n/2),
    -pi Px(A)=1/2+(1/2)sum_{n>=1}(-1)^n n csch(n/2).

The own90-digit Decimal calculation uses400 modes and25 strip-image terms and agrees below1e-70 for both value and radial derivative. It finds c about0.00032498636 and exact-support margin about0.40521649. These are explicitly numerical comparisons, not interval arithmetic or formal proofs. Strong cancellation in the Fourier radial sum is handled at high precision; no finite truncation is used to carry the analytic theorem.

## Green/Martin and minimality audit

The strip Green ratio has numerator-minus-denominator2sin(pi x)sin(pi s)>0, zero values on both boundary lines and one logarithmic pole. Its image terms and every fixed interior derivative decay exponentially in |k|, uniformly on compact first-variable sets and source eta in a small neighborhood of pi, s in[0,s0]. Consequently periodization, boundary differentiation and the first-order expansion in s are valid. The denominator after division by s stays uniformly positive near eta=pi because P_pi(A)>0. This closes the all-approach Martin limit, including tangential eta(s); no comparison s~|eta-pi| is required.

For minimality, let0<=v<=P. Domination forces continuous zero boundary values except at xi. Near xi, expansion of sin(pi x) and cosh(pi t)-cos(pi x) gives P=x/(pi(x^2+t^2))+O(x), uniformly even along nearly tangential approaches. The leading correction is proportional to x, so an O(1/r) bound is uniform. Odd reflection of v across the straight boundary is harmonic on a punctured full disc. Its circle Fourier coefficients with negative degree n>=2 obey |a_-n|<=C r^(n-1) and hence vanish as r->0. The only singular possibilities are a log term and the normal/tangential degree-one dipoles. Oddness in x kills the log and tangential dipole. Thus v=B x/r^2+v0, with v0 regular and odd in x. Positivity/domination along t=0 give0<=B<=1/pi. Subtracting pi BP removes the dipole; bounded removable-singularity theory and oddness give value0 at xi. All annular boundary values are then zero and the maximum principle gives v=pi BP. No unproved assertion that a Poisson kernel is automatically minimal is substituted for this argument.

The ordinary harmonic reflection/removable-singularity/Fourier expansion/maximum-principle facts are the explicitly identified standard interfaces; their use and hypotheses are described above rather than imported from a current peer. No probabilistic or Martin-boundary classification theorem is needed to establish the exhibited minimality.

## Independent punctured-disc ancillary check

Let D*=disc minus{0}, a=1/2. Exhaust by epsilon<|z|<1. For a fixed pole away from0, the difference between disc Green and annular-exhaustion Green is bounded on fixed compact sets by C log|z|/log epsilon, which tends to0. Hence puncturing does not change the interior disc Green function. Taking its pole to0 yields the normalized Martin kernel L=-log|z|/log2; boundary limits yield normalized disc Poisson kernels. A dominated harmonic function beneath a disc Poisson kernel is bounded near0 and removable, so ordinary disc boundary minimality applies. Beneath L, the logarithmic Fourier singularity is the only one compatible with positivity/logarithmic growth, and subtracting it leaves a zero-boundary regular harmonic function: L is minimal too.

At a, the normalized pole-minus-one kernel has gradient(-8/3,0). The pole-plus/minus-i gradients are(-32/15,+/-8/5), and the logarithmic gradient is(-2/log2,0). The trapezoid inequality for the strictly convex function1/t on[1,2] gives log2<3/4. Therefore

    -2/log2 < -8/3 < -32/15.

The target gradient lies strictly inside the triangle: its weight on L is (8/15)/(2/log2-32/15), in(0,1), and the other two positive weights are equal. The same finite-family Taylor reasoning gives local isolation. This is a source-only derivation of the stated ancillary deduction, not a claim of prior historical recognition or a substitute for the annular theorem.

## Status and exact remaining boundary

No internal counterexample or substantive analytic gap was found in the full stated annulus claim. The all-direction mechanism is independently optimized and boundary/minimality details were explicitly tested. The literal mapping to the foreign Problem7.42 wording and the cited historical/edition statements remain uninspected until PrimaryGO. Those are actual external-interface limits, not a narrowed replacement theorem. Follow-up remains null; the stronger internal support bound is validation detail, not a proposed new research programme.
