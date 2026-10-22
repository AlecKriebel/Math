# Root reconstruction of the classical-identity bridge

UTC: 2026-10-15T12:44:09.739165+00:00. Case estimate45%, priority-family integration pending seal/replay. This is an independent algebraic verification after reading the new bridge, not an independent historical-discovery claim. It does not change the submitted proof.

Let s=sn(z,k), t=cn(z,k), d_z=dn(z,k), k'^2=1-k². The normalized polar-circle coordinates are

    X=(k-s)/(1-ks), Y=k't/(1-ks).

Direct differentiation, using s'=t d_z, t'=-s d_z and d_z'=-k²st, gives

    X'=-k'^2 t d_z/(1-ks)²,
    Y'=k'd_z(k-s)/(1-ks)²,
    XY'-YX'=k'd_z/(1-ks).

For f=sqrt((1-k)/(1+k))*d_z/(1-ks), direct differentiation gives

    f'=sqrt((1-k)/(1+k))*k t/(1-ks),
    f''/f=k(k-s)/(1-ks).

Since f²=((1-k)/(1+k))*(1+ks)/(1-ks), this is exactly

    f''=(1+k)²/4*((2-m_b)f-2f³), m_b=4k/(1+k)².

At z=K, f=1 and f'=0. The smooth autonomous second-order equation has a unique solution with these initial conditions, so f=dn((1+k)(z-K)/2,m_b). The angular derivative above equals(1+k)f; the normalized circle coordinate and -exp(2i am(u,m_b)) agree at z=K and have identical derivative. This proves the phase origin and orientation, not merely a numerical modulus fit.

For the contact geometry, O lies strictly on the left of each oriented image chord: the positive-denominator projectivity sends the original interior caustic and Fminus=Tplus^-1(O) together. Thus det(Q_j,Q_j+1)>0, each contact-angle increment lies in(0,pi), and t_j=r tan(epsilon_j)>0. Direct circle geometry gives

    Bplus=r³ sum t_j/(r²+t_j²), A_R=r sum t_j.

These identities use ordered signed determinants and continue to hold for primitive stars. Substituting t_j=t_M dn(u+j sigma,m_b), the sum of the addition identity for dn at plus/minus sigma gives

    sum dn(u_j)/(1-m_b sn²u_j sn²sigma)=(1/dn sigma) sum dn(u_j).

The cyclic reindexing is valid for every coprime tau because N sigma=2K_b tau is a dn period. Therefore Bplus=Gamma sum dn(u_j), Gamma=r³t_M/(R²-dcenter²), and Bplus/A_R=r²/(R²-dcenter²). The denominator is positive: R-|dcenter|>r for the nested circle pair.

As an independent normalization check, write h=sn(v,k), C=cn(v,k), D=dn(v,k), W=1-k²h⁴. The geometric formulas reduce to

    R=alpha/C², |dcenter|=alpha k h²/C²,
    r=alpha D/C, t_M=alpha(1+k)h/C²,
    Gamma=alpha²(1+k)h D³/(C W).

Gamma has length-squared units, so its squared area product has length-four units. No projective area preservation is assumed.

Finally, for any nome q in(0,1), the classical Fourier series for dn has constant coefficient pi/(2K) and nth cosine coefficient(2pi/K)q^n/(1+q^(2n)), with argument n*pi*u/K. Uniform absolute convergence on the real axis allows finite cyclic summation. The N equally spaced phases annihilate every mode except multiples of N. If the reduced modulus has nome q^N and complete integral K_N, the result is

    sum_j dn(u+2jK/N,m)=(N K_N/K)dn((N K_N/K)u,m_N).

This fixes both amplitude and argument scale and agrees with Khare-Sukhatme's published reciprocal normalization. Odd N makes the opposite-focus u shift K_b a reduced real half-period; dn(x)dn(x+K_N)=sqrt(1-m_N) yields the constant product. Even N instead gives a full-period shift and need not give a constant square.

The published arbitrary-order identity and all quadratic/addition/Fourier tools are old. The exact focal-foot-to-contact construction, contact-area sum and focus-phase alignment were newly written in this audit. Their derivability from old identities does not alone certify prior publication or novelty of this source-specific application. Root has read the actual Pramana Eq7-9, full section2.1, and period normalization Eq54/odd summary58; the Fourier derivation above supplies a direct analytic check without depending on the paper's informal endpoint-to-range argument for its integration constant. The separate submitted two-simple-pole proof remains independently sufficient.
