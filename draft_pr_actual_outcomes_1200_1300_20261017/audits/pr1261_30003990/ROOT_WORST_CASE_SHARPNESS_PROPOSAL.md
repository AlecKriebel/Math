# Optional classical worst-case clarification — pending independent review

This is a proposed explanatory addition, not an unreviewed promotion or novelty claim. The immutable submitted theorem supplies the upper bound. The original report asks for the convergence regime, so a known interval lower example can clarify that exponent two is worst-case sharp across the full class, while constant objectives still have zero error. This does not claim a positive Theta rate for every objective/body.

Take K=[0,1], f(t)=t and any normalized global SOS q=Σ p_j² with deg p_j<=r. Write the orthogonal Legendre expansion of each p_j in basis ℓ_i(t)=sqrt(2i+1) P_i(2t−1). The standard identities ∫_0^1 ℓ_iℓ_k=δ_ik and |P_i(x)|<=1 for x∈[-1,1] give, by Cauchy–Schwarz,

    |p_j(t)|² <= (r+1)² ∫_0^1 p_j(s)² ds.

Thus 0<=q(t)<=(r+1)²=M, since the squared norms sum to one. Set α=1/(2M). Then ∫_0^α q<=1/2, so

    ∫_0^1 t q(t)dt >= α ∫_α^1 q >= 1/(4M)=1/[4(r+1)²].

Taking the infimum proves H_r>=1/[4(r+1)²]. Combining with the general upper theorem proves Θ(r^-2) for this fixed interval/linear instance and excludes a universal o(r^-2) rate over all fixed instances. For each fixed dimension n>1, use K=[0,1] x [-1,1]^(n-1), f(t,y)=t. Apply the same Legendre bound to each p_j(t,y) with y fixed and integrate over y. The marginal density in t is at most M and has unit mass, so the same lower bound follows. This gives a fixed sharpness instance in each dimension, without needing to assert a marginal SOS representation.

A layer-cake argument improves this particular coarse constant to1/2, but the weaker1/4 constant suffices and is simpler.

The Legendre identities are classical, not discoveries. A self-contained note can recall Rodrigues P_i(x)=(2^i i!)^-1 d^i/dx^i (x²−1)^i; i integration-by-parts steps give orthogonality and ∫_-1^1P_i²=2/(2i+1). The bound |P_i|<=1 follows from the finite-polynomial identity

    P_i(x)=(1/pi)∫_0^pi (x+i sqrt(1−x²) cosθ)^i dθ,

where the imaginary unit should be written iota in a final typeset proof to distinguish it from the integer index. For each integrand its base has modulus<=1. This identity can be verified by expanding the finite power and using the even cosine moments; no branch or noninteger continuation theorem is needed.

Before inclusion, an independent adversary must check the identities/normalizations, SOS degree reduction, endpoint convention and worst-case quantifiers. The original submitted proof is not modified, and its upper bound does not depend on this proposal. Priority sources already record interval/Jacobi lower rates, so any inclusion must explicitly credit that known context. No new firstness/current-openness assertion follows.
