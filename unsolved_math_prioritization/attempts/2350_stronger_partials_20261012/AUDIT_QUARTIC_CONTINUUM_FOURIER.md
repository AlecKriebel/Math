# Independent continuum and Fourier audit

## Verdict

Sections 2–4 are mathematically valid under their stated hypotheses and the finite identities in Section 1. No correction to the positive-part bound, local constants, Fourier transfer, parity treatment, residual energy, or numerical threshold is required. The claimed obstruction remains conditional on an additional structural phase bound; these sections do not establish such a bound or exclude the endpoint profile.

Reviewed source: the original quartic proof, whose complete corrected mathematics is presented in QUARTIC_EXCESS_PROOF.md. [Editorial redaction: unpublished-version identity metadata omitted.] This review did not change the source or any remote object.

## Weak limits and the positive-part bound

For d nonzero, the ordered core-difference multiplicity is twice its occupation indicator except when a representation is fixed by reflection. There are at most |C| such representations over all d. The core zero-difference mass is |C|. Consequently the occupation measure for c differs in total variation by O(|C|/N) from half the convolution of the two core empirical measures. The corresponding errors for q and for omission of the r zero atom are O(|U|/N). The mixed count m is the centered mixed-sum convolution exactly away from the omitted origin. The origin has no mixed or unpaired-sum representation.

The centered supports are uniformly bounded because A is contained in [1,N] and an actual exceptional sum is in [2,2N]. The empirical masses are O(1), so products of the weakly convergent measures converge. This justifies all four linear weak limits in Theorem 1. The finite weighted inequality then gives

    liminf P_T(U)/N >= 2 integral phi(t) J(t) dt

for every continuous, compactly supported 0 <= phi <= 1. The function J is continuous and equals -1 outside a compact set. Continuous approximation to the indicator of {J>0} gives exactly 2 integral [J]_+. No product of discrete occupation indicators is being passed through weak convergence.

## Interval calculations and localization

Put A0=7-2 sqrt(2). In the stated short-shift range, the three overlap formulas give

    J(t) = b/2 - (A0/2)|t|.

Thus the positive triangle has radius b/A0, and twice its integral is b^2/A0. The cutoff condition is exactly b <= A0/(A0+2).

At b=1-sqrt(2/3), one has b < (1-b)/2, so this formula covers every |t| <= b. The claim that J<=0 outside this interval is correct. It can also be verified without invoking any previously accepted domination result. Set I=[-1/2,1/2], H=1_I*1_V, and W=1_V*1_V. Since 1_E=1_I-1_V,

    J(t) = (1-|t|)_+ + (sqrt(2)-2)H(t)
           + (5/2-sqrt(2))W(t) - 1.

For |t|>=b, W=0, H>=0, and sqrt(2)-2<0. Therefore J<=0 directly. This identity is an optional self-contained replacement for the reference to earlier difference domination.

For fixed 0<delta<=b/A0, restricting the finite weighted inequality to 0<|d|<=delta N yields

    liminf P_N(delta)/N >= 2b delta-A0 delta^2.

The upper bound is the mass of ordered U-sums in that band, since each nonzero U-difference has at most one representation. Its limit is 2b delta-delta^2. The limiting sum and difference convolutions are continuous, so the sharp interval boundaries introduce no portmanteau ambiguity. Squeezing after division by 2delta gives the two iterated limits b in (10b).

If S_N(delta) is the number of short ordered U-sums, then

    limsup (S_N(delta)-P_N(delta))/N <= (A0-1)delta^2,
    S_N(delta)/N -> 2b delta-delta^2.

This proves the stated failed-alignment proportion. The limits are iterated in the stated order, N first and then delta down to zero; they do not establish the same assertion for an arbitrary shrinking delta_N.

The mixing comparison is exactly

    integral_{-delta}^{delta}(b-|t|)^2 dt
      = 2b^2 delta-2b delta^2+(2/3)delta^3.

The local-density enhancement is 1/b=3+sqrt(6). Maximizing the localized lower bound at delta=b/A0 recovers b^2/A0.

## Centering and parity

Every frequency of F and G lies in Z-T/2. When T is odd both are antiperiodic, but all quartic exponents relevant to the displayed orthogonality identities are integers. In particular, the exponent for F^3 conjugate(F) is

    u1+u2+u3-u4-T.

Thus its integral is the required integer count with no parity factor. The symmetric lattice interval L_N is invariant under negation, so G is real for either parity. It has M_N=bN+O(1) consecutive lattice points. Its additive energy is exactly (2M_N^3+M_N)/3, hence the G fourth integral is ((2/3)b^3+o(1))N.

## Mixed terms and residual energy

Weak convergence and uniform boundedness of rescaled supports imply

    sup_{|t|<=K}|R_N(t/N)| = o_K(sqrt(N)).

One can see uniformity directly from equicontinuity: the derivatives of F_N(t/N)/sqrt(N) and G_N(t/N)/sqrt(N) are uniformly bounded on the real line. Also |G_N|=O(sqrt(N)). Therefore the jth mixed absolute integral over |alpha|<=K/N is o_K(N), for j=1,2,3.

Strong Sidonicity gives integral |F_N|^4=2|U|^2-|U|=O(N); the interval energy gives the same bound for G. Hence integral |R_N|^4=O(N). The geometric-series estimate supplies

    integral_{|alpha|>K/N}|G_N(alpha)|^4 = O(N K^-3).

Holder therefore bounds the outer jth mixed integral by

    O(N K^{-3(4-j)/4}).

Taking N to infinity for fixed K, then K to infinity, proves (13). The pure residual fourth moment is deliberately not shown negligible.

Expansion consequently yields exactly the two asymptotics

    E_N/N -> 2b^2-(2/3)b^3,
    P_T(U)/N = (2/3)b^3
               + Re integral R_N^3 conjugate(R_N)/N + o(1).

The first limit is positive for 0<b<1. Dividing the lower bound for the second by this positive limiting energy proves (16), including its sign and all factors of two.

## Constants and wording

Independent symbolic evaluation gives

    b^2/A0 = 0.00807213629443446150435235336721563,
    (2/3)b^3 = 0.00411946884333636443184260579519961,
    gap = 0.00395266745109809707250974757201602,
    residual energy coefficient
      = 0.0632275407790928379717786279302785,
    rho = 0.0625149642449023979620979936369564.

These agree with the manuscript's rounded constants.

One optional wording refinement concerns the parameterized version of Theorem 2. Its bound is positive precisely when 0<b<3/(2A0), not throughout the full geometric cutoff range 0<b<=A0/(A0+2). The formula itself is valid throughout the latter range. If the theorem is meant for that whole parameterized family, rename its heading to “necessary residual phase bound,” or explicitly reserve “positive” for b<3/(2A0). The relevant endpoint value lies strictly in the positive range, so this does not change any endpoint conclusion.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
