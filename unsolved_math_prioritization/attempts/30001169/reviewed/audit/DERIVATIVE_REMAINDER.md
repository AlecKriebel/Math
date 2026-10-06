# Differentiating the heat asymptotic without differentiating an O-term

This is an authored audit clarification. It does not change the frozen author's mathematical claim.

Let L be the positive conformal Laplacian for a fixed smooth positive conformal metric on the compact sphere, let p=n/2, and set H(t)=Tr(e^{-tL}). Standard heat-kernel theory on a closed smooth manifold gives the full real-time expansion. In particular, with fixed-metric constants,

H(t)=E(t)+R(t),  E(t)=sum_{k=0}^5 a_k t^{k-p},  R(t)=O(t^{6-p}).

We do not infer an estimate for R' merely from this formula. Instead use positivity of the spectrum and the convergent differentiated spectral series. Since x^2 exp(-x/2) is bounded for x>=0,

H''(t)=sum_j lambda_j^2 exp(-t lambda_j)
       <= C t^{-2} H(t/2)=O(t^{-p-2}).

These series and their derivatives converge locally uniformly on t>0, for example by the usual polynomial eigenvalue-counting bound. For 0<t<1/2 put h=t^4. Taylor's theorem, or its integral remainder, implies

[H(t+h)-H(t)]/h = H'(t)+O(h t^{-p-2})
                = H'(t)+O(t^{2-p}).

The finite sum E satisfies E''(s)=O(t^{-p-2}) for t<=s<=t+h, so the same secant estimate holds for E. Meanwhile, without differentiating R,

[R(t+h)-R(t)]/h=O(t^{6-p}/t^4)=O(t^{2-p}).

Subtracting these identities yields H'(t)=E'(t)+O(t^{2-p}). Consequently

(d/dt)[t^p H(t)]
 =p t^{p-1}H(t)+t^p H'(t)
 =sum_{k=0}^5 k a_k t^{k-1}+O(t^2)
 =a_1+2a_2 t+O(t^2).

For n=4, the independently checked coefficients are a_1=0 and a_2=-1/90, hence f'_W(t)=-t/45+O_W(t^2). For n>=5 the first coefficient is strictly negative, so f'_W(t)<0 near zero as well. This proof requires only the standard full, undifferentiated heat expansion and a spectral second-derivative estimate. No uniform remainder over varying W, and no uniform small-time interval, follows from it.

Reference for the conformal-Laplacian heat expansion and coefficients: Andreas Juhl, *Heat kernel expansions, ambient metrics and conformal invariants*, §14.2, https://arxiv.org/pdf/1411.7851. All finite-difference reasoning above is supplied in this clarification.
