# Independent initial hand controls

These controls were formulated from the five-page native manuscript before reading supporting proof/code/results/opinions or dependency bodies. They are symbolic checks, not source-helper runs.

A. Scaling identity: α+2 = [2(p+1)+2(pq−1)]/(pq−1) = 2p(q+1)/(pq−1)=pβ. Similarly β+2=qα. The normalization is U^(1/α)+V^(1/β)=λ(u^(1/α)+v^(1/β)); using U+V=1 instead would be wrong for unequal exponents. Published text uses the correct powered sum.

B. Unequal-exponent subcritical example: n=3,p=2,q=3 gives pq−1=5, α=6/5,β=8/5, pβ=16/5=α+2, qα=18/5=β+2, and 1/3+1/4=7/12>1/3. Scaling factors differ and cannot be silently interchanged.

C. Critical negative control: n≥3 and p=q=s=(n+2)/(n−2) give α=β=(n−2)/2 and equality in the hyperbola. Let w(x)=[n(n−2)]^((n−2)/4)(1+|x|²)^(-(n−2)/2). Radial differentiation gives −Δw=w^s. Thus u=v=w is a positive bounded entire pair at the excluded critical equality. Restricting w to Ω_L=Rⁿ\{Le₁} gives d(0)=L and u(0)>0; a domain-uniform bound u(0)≤CL^(−α) fails as L→∞. The theorem cannot be extended to critical exponents with the same assumptions. This tests strictness without alleging a counterexample in the stated region.

D. p=q=1 is excluded: pq−1=0 and the stated α,β undefined. p,q>1 guarantees positive exponents and bounded-range Lipschitz nonlinearities. A proof must not silently cover p≤1 via this argument. The n≥3 claim similarly must not be read as n=1,2 or as a weighted theorem.

E. Zero/sign control: if u≡0, then first equation gives v^p=0, so v≡0. If u touches zero at one point and is nonnegative, −Δu=v^p≥0 lets the strong minimum principle apply. Dropping nonnegativity breaks this argument and can make nonintegral powers undefined.

F. Boundary compactness control: for boundary graph φ with uniform Hessian bound, ψ(y')=λ^(−1)φ(λy') has Hessian λD²φ(λy'); curvature shrinks, rather than growing as λ^(−1). The boundary normalized point is at scaled height t=d/λ. Up-to-boundary convergence is necessary when t=0; interior C² convergence alone cannot pass this normalization.

G. Constants/control: universal C(n,p,q) is fixed for each admissible triple; no uniform assertion as p,q approach the hyperbola or 1 is stated. C(Ω,n,p,q), W²,r, C¹,γ and Schauder constants may also depend on fixed Ω and exponents. A family of degenerating Ω need not have uniform boundary estimates.

H. Compactness endpoint control: uniform W²,r alone gives only weak compactness at fixed r; the published difference equation is necessary for strong W²,r. Uniform C²,θ gives compactness only at η<θ; equal Hölder exponent need not be compact. The manuscript uses strict η<θ and γ<1.

I. Half-space control: the arbitrary-domain estimate has d=x_n and diverges as x_n→0. It does not independently imply a uniform bounded-domain estimate. A valid half-space Liouville argument is an indispensable separate dependency, and bounded entire nonexistence must be connected to it by an exact applicable theorem.
