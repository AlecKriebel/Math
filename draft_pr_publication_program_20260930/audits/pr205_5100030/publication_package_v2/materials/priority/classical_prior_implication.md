# Positive prior-implication audit: PR205 / k601

The complete all-odd special-function lemma in the submitted proof is a direct corollary of earlier generalized Landen formulas, explicitly stated for every odd order by Khare and Sukhatme in arXiv:math-ph/0312074v1 (31 December 2003). The predecessor cyclic-identity literature also already states the needed all-odd pair-correlation constancies. The analytical lemma must be credited as existing mathematics, not merely described as a new theorem inspired by a related literature.

This does not alone establish that an earlier paper explicitly applied those formulas to the exact geometric k601 quantity. That application question is separate. This family has not certified firstness, current openness, independent discovery, simultaneous discovery, or exhaustive priority.

## Exact normalization and prior implication

Use parameter notation m=k^2 throughout. DLMF writes a modulus k; the Khare–Sukhatme papers and mpmath use the parameter m. Let p>=3 be odd, K=K(m), and define

    D_p(t) = sum_{j=0}^{p-1} dn(t+4Kj/p | m),
    C_p(t) = sum_{j=0}^{p-1} cn(t+4Kj/p | m).

To avoid confusing the caustic semiaxis alpha with the paper's normalization alpha, rename the latter gamma:

    gamma = [sum_{j=0}^{p-1} dn(2Kj/p | m)]^(-1),
    eta   = [sum_{j=0}^{p-1} cn(4Kj/p | m)]^(-1),
    M = m*gamma^2/eta^2.

In [math-ph/0312074v1](https://arxiv.org/abs/math-ph/0312074v1), gamma is the paper's alpha (Eq.14, p.4), eta is its alpha_1 (Eq.32, p.8), and M is the common transformed parameter. Eq.53 (p.10) gives the ratio m*alpha^2/alpha_1^2. Section 3.1, pp.12–13, identifies that parameter with the dn and cn transformed parameters and removes the apparent difference of argument scales. Equations 68–70 on p.13 state the common-argument odd-p formulas.

There are two grid spacings in the source: dn uses 2K/p while cn uses 4K/p. This does not obstruct the implication. For odd p, multiplication by 2 permutes residues modulo p. Since dn has real period 2K,

    sum_j dn(t+2Kj/p | m) = sum_j dn(t+4Kj/p | m) = D_p(t).

Consequently the source formulas give exactly

    gamma*D_p(t) = dn(t/gamma | M),
    eta*C_p(t)   = cn(t/gamma | M).

The elementary relation dn^2(u|M)-M*cn^2(u|M)=1-M then implies

    D_p(t)^2 - m*C_p(t)^2
      = gamma^(-2) [dn^2(t/gamma|M)-M*cn^2(t/gamma|M)]
      = (1-M)/gamma^2.                                      (P)

This is the submitted all-odd lemma with an explicit prior normalization. It is not a numerical extrapolation or only a three-point result. The algebra requires m*gamma^2/eta^2=M; assuming equal cn/dn amplitudes would be wrong.

For the already-audited geometry-to-functions bridge of PR205, with caustic semiaxes alpha_c,beta_c, the product of focal distance sums is alpha_c^2*(D_p^2-m*C_p^2). Thus the prior Landen formulas, combined with that bridge, imply the exact geometric invariant with family constant

    I = alpha_c^2*(1-M)/gamma^2.

This is a present checkable implication from cited prior mathematics. It is not a finding that the 2003 paper itself discusses billiards or k601.

## Independent verification of the source normalizations by classical trace formulas

The implication above does not need to trust every informal ODE argument or internal cross-reference in the 2003 paper. The necessary common scaling follows directly from the classical Fourier expansions recorded in [DLMF 22.11.2–3](https://dlmf.nist.gov/22.11), with nome q=exp(-pi*K(1-m)/K(m)):

    dn(t|m) = pi/(2K)
       + (2pi/K) sum_{n>=1} q^n/(1+q^(2n))*cos(n*pi*t/K),

    cn(t|m) = (2pi/(sqrt(m)*K))
       sum_{n>=0} q^(n+1/2)/(1+q^(2n+1))
          *cos((2n+1)*pi*t/(2K)).

For real t and 0<m<1, these series are absolutely and uniformly convergent. Finite orbit sums may therefore be interchanged with them. The root-of-unity filter for the 4K/p shifts keeps exactly n divisible by p in dn, because p is odd, and exactly the odd harmonics divisible by p in cn. Set Q=q^p, choose M with nome Q, and put K_M=K(M). [DLMF 22.2.1–2](https://dlmf.nist.gov/22.2) gives

    M = [theta_2(0,Q)/theta_3(0,Q)]^4,
    K_M = (pi/2)*theta_3(0,Q)^2,
    gamma = K/(p*K_M).

The surviving Fourier series are precisely

    D_p(t) = gamma^(-1)*dn(t/gamma|M),
    C_p(t) = sqrt(M)/(sqrt(m)*gamma)*cn(t/gamma|M).

At t=0 the coefficients in the cn trace series are strictly positive, so C_p(0)>0 and eta is a valid positive normalization for every real 0<m<1. It follows that eta=sqrt(m)*gamma/sqrt(M), giving M=m*gamma^2/eta^2. This verifies every amplitude, shared argument and parameter conversion used in (P). This is an explanatory derivation of the classical distribution formulas, not a novelty claim for this audit.

The circular limit m=0 must be handled separately because eta diverges and M tends to zero. The geometric result then follows directly as p^2*beta_c^2. The m=1 caustic degeneration is outside the proper-confocal theorem.

Coprime billiard winding tau only permutes the 4K/p grid. It creates no additional analytic assumption. If an odd list repeats a shorter odd orbit d times, both traces multiply by d and (P) scales by d^2. No primitive-period claim is gained by repetition. Even p has different Landen formulas and is not covered by the dn-grid reindexing used here.

## Earlier cyclic identities and what was actually proved

[Khare–Sukhatme, math-ph/0201004v2](https://arxiv.org/abs/math-ph/0201004v2), Table 1 Eq.29, p.9, explicitly lists all-odd cyclic dn and cn pair correlations as constants, for every separation through (p-1)/2. The dn values use the 2K/p grid and the cn values the 4K/p grid. For a fixed separation r, the dn correlation on the latter grid is the former correlation with separation 2r modulo p; symmetry identifies r with p-r. All ordered off-diagonal pairs are thus covered. Combining these prior constant correlations with the diagonal identity dn^2-m*cn^2=1-m proves the submitted lemma immediately.

The 2002 preprint discusses algebraic derivations for low p and numerical checks for higher p. Its general catalog should not be misrepresented as a fully supplied all-p proof on its own. Similarly [math-ph/0204054v1](https://arxiv.org/abs/math-ph/0204054v1), p.9, explicitly says that common transformed parameters were established analytically for p=3 and p=4 and numerically checked for higher p. It is an earlier statement of the relevant transformation family, but the all-p common-parameter conclusion should be credited using the later expanded source or the classical Fourier derivation.

[Khare–Lakshminarayan–Sukhatme, math-ph/0207019v2](https://arxiv.org/abs/math-ph/0207019v2), pp.3–8, supplies a general Liouville/principal-part and finite-Poisson/master-identity derivation. For each pair product, the residues at shifted Jacobi poles cancel; the periodic sum has no remaining poles and is constant. Eq.6, p.4, and Appendix A Eqs.112 and 114, p.22, give explicit dn and cn correlation constants. For a real shift a=4Kr/p, they match

    sum_j dn(t_j)dn(t_j+a)
        = p*[dn(a)-cn(a)*Z(a)/sn(a)],

    sum_j cn(t_j)cn(t_j+a)
        = p*[cn(a)-dn(a)*Z(a)/(m*sn(a))].

The products have real period 2K even though their cn factors individually are antiperiodic. For odd p, the 4K/p sample set of each product is a permutation of its 2K/p sample set. One must not wrap the individual sn or cn index modulo p when using a 2K/p grid: the sign across 2K matters. Noncoprime separations reduce to shorter subgroup orbits with multiplicity, as the source explicitly notes; the reduction preserves the constant formulas.

The correct sn correlation already appears as Eq.5, p.3, of the same source and is precisely the intermediate correlation in PR205:

    sum_j sn(t_j)sn(t_j+a) = p*Z(a)/(m*sn(a)).

Here Z(a) denotes the argument form epsilon(a|m)-(E(m)/K(m))*a. The historical source writes Z with an amplitude argument beta_a; comparison requires Z_arg(a)=Z_amplitude(am(a)|m), using the continuous Jacobi amplitude and its periodic continuation. A principal arcsin(sn(a)) substitution outside the principal range can lose a sign or branch. The checker uses the argument-form theta derivative and checks every separation, including shifts beyond K.

Thus this intermediate identity is existing mathematics too. The submitted telescoping verification is correct, but it cannot justify a claim that the correlation identity itself is new.

## Printed-source cautions checked visually

The positive overlap does not depend on silently accepting several typos:

- math-ph/0207019v2 Appendix A Eq.113, p.22, prints cs(a) in the sn correlation, whereas Eq.5, p.3, correctly has 1/sn(a). The erroneous extra cn(a) factor is caught by an explicit negative control. Eqs.112 and 114, which suffice for the needed pair-constant argument, match the correct formulas.
- math-ph/0312074v1 p.12 refers to Eqs.105–106 as the cyclic identities used in its common-parameter discussion; those numbered equations are actually even-p product transformations on p.18. The final odd-p formulas on p.13 are unambiguous.
- The x_j/tilde-x_j notation in Eqs.103–104, p.18, should not be used literally to transfer odd sn/cn traces to the 2K grid. The exact grids used in Eqs.18 and 68–70, and the Fourier derivation above, resolve the needed normalization without that transfer.

These cautions do not revive novelty of the correct classical trace formulas.

## DLMF's three-point formulas are supporting special cases

[DLMF 22.9.9–10](https://dlmf.nist.gov/22.9) gives explicit three-point cn/dn pair constants. Together with the diagonal identity they imply (P) at p=3. Those two displayed formulas alone do not prove the all-odd theorem. The general prior implication comes from the all-odd cyclic catalog/master derivation and generalized Landen formulas above.

## Actual calibration and fail-closed controls

ACTUAL_CONTROL_RECEIPT.json binds actual complete ordinary and optimized Python executions of prior_implication_checker.py. Each passes 2 exact symbolic reductions, 9,103 integer arithmetic checks and 2,884 finite noninterval scalar diagnostics at 160 decimal digits. The 20 parameter/order configurations use m in {0.09,0.5,0.99,0.999999} and p in {3,5,9,15,25}, with four real phases. The worst scaled residual is about 1.71e-109. Relative comparisons separately test very small transformed parameters, including M about 2.92e-55, so an absolute-error threshold does not silently accept a wrong small parameter.

Both modes refuse 13 genuine controls: nonfinite and complex values, invalid period/parameter types or domains, wrong cn grid, wrong common argument, m/k confusion, conflated amplitudes, the printed Eq.113 extra cn factor, and an incorrect antiperiodic sn index wrap. The code has no bare asserts. The earlier sealed analytic family and all read primary-source files remain unchanged. These runs calibrate the exact prior mapping; the universal implication rests on the written algebra and convergent Fourier trace, not the finite samples.

## Bibliographic and access boundaries

Four complete primary arXiv PDFs were lawfully retrieved and pinned in DOWNLOAD_MANIFEST.json. Relevant equation pages were rendered with Poppler and inspected visually. The selected versions and cover dates are: 0201004v2, 4 January 2002 (14 pages); 0204054v1, 30 April 2002 (11 pages); 0207019v2, 24 March 2003 (38 pages); and 0312074v1, 31 December 2003 (26 pages). Full copyrighted PDFs, text extractions and page images remain in private/ and are not proposed as public supplement contents.

The DOI 10.1063/1.1484541 is linked by the primary arXiv record for 0201004; 10.1063/1.1560856 is linked for 0207019 and its journal title is “Cyclic identities for Jacobi elliptic and related functions,” J. Math. Phys. 44 (2003), 1822–1841. The Pramana article “Connecting Jacobi elliptic functions with different modulus parameters,” DOI 10.1007/BF02704331, November 2004, 63:921–936, is a separate related publication: its publisher page explicitly cites math-ph/0312074 as a separate reference. It must not be conflated with that expanded preprint. Its full text was not required for the positive 2003 implication established here; a lawful IAS direct full-text request returned HTTP 403 and is recorded. No institutional access or human outreach is needed to establish the specific classical overlap in this report.

## Disposition for Root

The all-odd analytical lemma, its pair correlations, and the generalized-Landen route are prior mathematics. Any final package should cite these as direct antecedents, with the exact normalization above. The report supplies a complete positive implication from prior formulas to the checked lemma and then, using the audited geometric bridge, to k601.

The remaining distinct priority question is whether an earlier author explicitly published that exact complete-original-side focal-pedal application. This family has not established or excluded such an application and has not searched the separate contemporary Zenodo lineage assigned to Root. The 2021 table's question mark and a missing geometric keyword in the classical papers cannot establish current openness. No novelty or firstness certification follows from this bounded audit.
