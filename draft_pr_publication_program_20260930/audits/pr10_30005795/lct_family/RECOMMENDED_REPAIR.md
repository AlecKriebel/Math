# Concise proposed LCT proof repair

The finite-resolution minimum materially clarifies both endpoint attainment and the real-divisor formula. It also prevents accidental omission of strict transforms. No additional theorem or stronger hypothesis is needed in the algebraic source setting.

## Proposed replacement for BOUND.md:56

The endpoint and positivity follow on a log resolution of (S,D_j), including exceptional divisors and strict transforms. If m_E=ord_E(D_j), then

    c_j=min_{m_E>0} A_S(E)/m_E>0.

This is a finite nonempty minimum, since D_j!=0 and S is klt. At t=c_j, the crepant pullback boundary has SNC support and coefficients 1-A_S(E)+t*m_E<=1, so (S,c_jD_j) is log canonical.

## Optional single sentence after the formula in Section 4

For B!=0, a common log resolution gives lct(S;B)=min_{ord_E(B)>0} A_S(E)/ord_E(B), including strict transforms, so the reciprocal supremum is attained and the computation remains valid for real coefficients.

## Local infinity convention, if one additional precision is desired

Handle c_{j,P}=infinity separately by ord_F(D_j)=0 for the admitted centers, and set 1/infinity=0; no infinite boundary coefficient is used. The frozen text already states this case correctly, so this sentence is optional.
