# Classical Fourier implication: complete audit deduction

This is a NEW deduction written during the priority audit on 2026-10-17. The cited earlier papers are not alleged to state Novak's comparator explicitly. All measures below have total mass one.

Let `e(t)=exp(2 pi i t)`, `Q=(1/n) sum delta_{t_j}`, and `F(x)=Q([0,x))-x` for x in [0,1]. Its L4 norm is exactly the normalized anchored discrepancy in the target question (the opposite discrepancy sign has the same norm).

For every point t in [0,1], the ordinary Lebesgue integral is

    integral_0^1 1_{t<x} e(x) dx = (1-e(t))/(2 pi i).

This includes t=0 and t=1. Endpoint conventions affect only a null set of x. Also `integral_0^1 x e(x) dx=1/(2 pi i)`. Taking the finite sum proves, without an endpoint Stieltjes convention,

    integral_0^1 F(x)e(x) dx = - Qhat(1)/(2 pi i).

This is the nonzero Fourier identity in the proof of Su's Lemma 4, printed p.451. Su centers F by adding a constant K; its integral against e(x) is zero, so this has no effect. Crucially, the Hölder bound is applied to the UNcentered F after recovering its nonzero Fourier coefficient:

    |Qhat(1)| <= 2 pi ||F||_1 <= 2 pi ||F||_4.

No supremum discrepancy is substituted for the L4 norm; no relation between the zero Fourier mode and K is assumed. It follows for each deterministic point set, with multiplicity, that

    disc_4(Q)^4 >= |Qhat(1)|^4/(2 pi)^4.

For the EXACT target law `t_j={jZ+Delta}`, j=0,...,n-1, we have

    Qhat(1) = e(Delta)/n * D_n(Z),
    D_n(Z) = sum_{j=0}^{n-1} e(jZ).

The common shift has modulus one, hence disappears in this lower bound. Therefore uniform continuous averaging over Z and independent uniform Delta gives

    E disc_4^4 >= [1/((2 pi)^4 n^4)] integral_0^1 |D_n(z)|^4 dz.       (1)

The Dirichlet-kernel convention is exactly (1.1) in Anderson--Ash--Jones--Rider--Saffari (AIF57,2007). Its Lemma2.1, printed pp.1383--85, gives the published general formula

    integral_0^1 |D_n(z)|^p dz = delta_p n^(p-1)+o(n^(p-1)), p>1,
    delta_p = (2/pi) integral_0^infinity |sin u/u|^p du > 0.

That formula ALONE with p=4 and (1) gives a positive-constant/n lower bound, so it exceeds the iid fourth moment (3n-1)/(30n^3) for all sufficiently large n. There is no additional Diophantine, irreducibility, equidistribution, or nonresonance hypothesis: the integration variable in this lemma is precisely uniform Z on the whole unit interval.

For an exact finite threshold independent of asymptotic errors, expand |D_n|^4 and integrate integer exponentials. The integral equals the number of ordered quadruples a,b,c,d in {0,...,n-1} with a+b=c+d. The pair-sum multiplicities are 1,2,...,n-1,n,n-1,...,1. Consequently

    integral |D_n|^4 = n^2+2 sum_{k=1}^{n-1} k^2 = (2n^3+n)/3,
    E disc_4^4 >= (2n^2+1)/(48 pi^4 n^3).                         (2)

The iid moment can be derived by the fourth moment of n centered independent Bernoulli(x) variables, followed by integration over x; it is (3n-1)/(30n^3). Thus (2) is a strict reverse comparison exactly when

    P(n) := 60 n^2+30 -48 pi^4(3n-1) > 0.

The classical rational bounds 223/71 < pi < 22/7 certify

    P(233) < -79254828294/25411681 <0,
    P(234) > 5975502/2401 >0.

Moreover `P'(n)=120n-144pi^4`, and for n>=234 it is at least `33687216/2401>0`. For integers1<=n<=233 the lower-pi rational upper bound is negative (checked exactly; alternatively the convex quadratic's endpoint maximum on [1,233] is negative). Hence234 is the least positive integer for which THIS coarse Fourier lower bound proves reversal. This does not assert no reversal for smaller n: the candidate's n=3 counterexample is much sharper, and this lower bound does not prove it.

`verify_fourier_bridge.py` independently checks the ordered count, Laurent polynomial coefficient, formal shift cancellation, endpoint Fourier numerators and rational threshold. This numerical checker supplements, rather than replaces, the universal proof above.

Historical classification limit: the implication (1) and its application to the Novak problem are deductions of this audit. The two ingredients were already stated in the cited earlier primary publications; their combination leaves only elementary Hölder/orthogonality and normalization checks. Whether this suffices for the program's strict PRIOR_FULL classification is the root auditor's decision. No claim is made that these authors explicitly answered Novak or that this consequence appeared elsewhere before the source PR.
