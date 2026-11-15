# Independent analytic reconstruction before external/supplied evidence

This note was written after authenticating and reading the entire published four-page PDF and complete controlling TeX, including all four rendered pages. No foreign primary body, supplied verifier/code/data, archived/current review, triage or scientific opinion was read before this reconstruction. Hashing opaque source payloads for custody is distinguished from inspecting their contents. The theorem is treated as a hypothesis to be checked, not an authority.

## Exact object and success criterion

For every integer n≥2 and N≥1, use the unit-radius round geodesic distance on S^(n−1). On U(N), use either the length metric obtained by integrating the **unnormalized** Hilbert–Schmidt norm of the matrix derivative or that obtained from the operator norm. Fix any p on the sphere. For every Φ with intrinsic Lipschitz constant L≤1/2, put A=Φ(p), W(x)=A*Φ(x), and

F_t(W)=(W+tI)(I+tW)^−1, H_t(Φ)(x)=A F_t(W(x)), q_t=(1−t²)/(1+t²).

The complete claim is a jointly continuous strong deformation retraction, in the uniform topology, of the closed L≤1/2 mapping subspace onto its constant maps, restricting to the strict L<1/2 subspace, with Lip(H_tΦ)≤q_t L for every t∈[0,1]. Endpoints are Φ and the constant Φ(p); every constant is fixed throughout. It stays in the original U(N). The based subspace Φ(p)=I is contractible; the full constant copy U(N) is not claimed contractible. Additional literal statements concern S^0 with assigned angular distance π, arbitrary topological parameter spaces, constant left/right frame changes, the classical Cayley identity, and a weaker logarithmic deformation for L<1 without a preserved Lipschitz bound. Printed version1.1/date23September2026 and declared date are not priority certification.

## Analytic mechanism A: right-trivialized tangent congruence

First localize the image without guessing a unitary distance formula. For a unit eigenvector v of W with eigenangle θ∈[−π,π], any unitary path U from I to W induces a path Uv in the real Euclidean unit sphere. Its length is at least |θ| and at most ∫||U'||op≤∫||U'||ν. Taking the infimum gives |θ|≤dν(I,W). Because diam(S^(n−1))=π and L≤1/2, every normalized image W(x) satisfies dν(I,W(x))≤π/2 and consequently Re W(x)≥0. This argument works for both stated norms and every finite N.

For a unitary W with Re W≥0, R_t=(I+tW)^−1 exists for the **closed** time interval, since

(I+tW)*(I+tW)=(1+t²)I+t(W+W*)≥(1+t²)I.

Thus ||R_t||op≤(1+t²)^−1/2. Equality of the two Gram matrices for W+tI and I+tW proves F_t(W) unitary. This also excludes endpoint singularities: t=1 never encounters W=−I.

An independent useful form of the derivative is obtained by right-trivializing a tangent E=WX, X* = −X. Direct differentiation gives

DF_t(W)[E]=(1−t²)R_t E R_t.

Moreover F_t(W)* R_t W=R_t*, so

F_t(W)* DF_t(W)[WX]=(1−t²) R_t* X R_t.

This is one congruence on the skew-Hermitian tangent space, not a scalar eigenangle argument applied to noncommuting matrices. The ideal inequality yields ||DF_t(W)[E]||ν≤(1−t²)||R_t||op² ||E||ν≤q_t||E||ν. For HS the ideal inequality follows from the Frobenius trace norm bound, and for op from submultiplicativity. No commutation between a perturbation and W is assumed.

For an absolutely continuous matrix curve W(s) remaining in this semicircle domain, the ordinary finite-dimensional chain rule therefore gives lengthν(F_t∘W)≤q_t lengthν(W). This is a genuine path-length argument; chordal contraction alone would not prove the target intrinsic-metric claim.

Given x,y, take any minimizing round geodesic γ between them. The input curve Φ∘γ is intrinsically L-Lipschitz and hence rectifiable with length≤L length(γ); chordal norm distance is bounded by intrinsic distance, giving matrix absolute continuity. Its normalized image remains in the semicircle domain. Integrating the derivative bound along this **image curve** gives dν(H_tΦ(x),H_tΦ(y))≤q_t L d(x,y). No geodesic convexity of the target semicircle set, simultaneous diagonalization of two unitaries, or smoothness of Φ is required. At antipodal x,y, any minimizing γ suffices; no continuous choice of γ is used.

The finite-dimensional curve-length fact can be checked locally: multiplication trivializes tangent speed isometrically; a small group increment has log(increment)=increment−I+O(||increment−I||²), so the length metric's metric derivative equals the matrix-norm derivative. Partitions and absolute continuity then identify curve length with the integrated speed. This validates the Finsler op case without requiring differentiability of the norm itself.

## Analytic mechanism B: scalar-angle flow and spectral norm gauge

For a single eigenvalue e^(iθ), |θ|≤π/2,

F_t(e^(iθ))=exp(i g_t(θ)), g_t(θ)=2 arctan(((1−t)/(1+t))tan(θ/2)).

Thus g_t is odd, preserves sign, fixes0, takes the semicircle into itself and has

g'_t(θ)=(1−t²)/(1+t²+2t cosθ)≤q_t.

This independently checks semicircle invariance, the closed boundary, all time endpoints, and the scalar contraction. With s=2 artanh(t), the scalar angles satisfy dθ/ds=−sinθ, while the matrix evolution satisfies dZ/ds=(I−Z²)/2. The separated tangent congruence above provides the essential noncommuting extension; an eigenangle-only proof would leave that central point unsupported.

For S^0 assigned distanceπ, the Lipschitz constant is dν(A,B)/π. Normalize one endpoint toI. The principal-angle distance formulas dHS(I,W)=||θ||₂ and dop(I,W)=||θ||∞, combined with |g_t(θ_j)|≤q_t|θ_j|, prove the S^0 assertion. These formulas are finite-dimensional unitary geometry: exponentiating the principal logarithm supplies the upper bounds; continuous eigenphase lifting along a piecewise smooth unitary path gives a vector of phase speeds whose ℓ₂ norm is bounded by its HS speed and whose maximum is bounded by op speed. Principal endpoint absolute angles are no larger than the corresponding lifted absolute angles, giving the lower bounds by integrating. No disconnected-sphere length metric is inferred.

The quantitative coefficient is sharp already for N=1 on every connected round sphere: Φ(x)=exp(i d(p,x)/2). It has L=1/2, and the one-sided derivative near the antipode approaches (1/2)g'_t(π/2)=q_t/2. This is a falsifiable sharpness observation, not needed for validity and not a priority claim. It also tests whether a claimed smaller universal coefficient could be valid.

## Topology, retraction, and parameter dependence

F_0(W)=W, F_1(W)=I, F_t(I)=I directly establish the endpoints/fixed constants. Hence H_0Φ=Φ, H_1Φ=Φ(p), and H_t fixes the entire constant copy. Since0≤q_t≤1, both the closed and strict sublevels are preserved. Evaluation at p is continuous in the uniform topology. The based terminal constant isI, giving an actual based contraction without stabilizing N.

For two input maps, δ=sup_x||Φ(x)−Ψ(x)||ν gives ||A−B||ν≤δ and ||A*Φ(x)−B*Ψ(x)||ν≤2δ. The noncommuting identity

F_t(U)−F_t(V)=(1−t²)(I+tU)^−1(U−V)(I+tV)^−1

is verified by multiplying on the appropriate left and right; its order matters. Thus the output sup-norm difference is≤(1+2q_t)δ≤3δ. An additional independent time modulus follows from ∂_tF_t(W)=(I−W²)(I+tW)^−2: its op norm is≤2 and HS norm≤2√N on the semicircle. Therefore the output norm changes by at most2cν|t−s|, with cop=1 and cHS=√N. These bounds directly give joint continuity in t and Φ. Intrinsic and matrix-norm uniform topologies agree; indeed the principal-angle formulas yield ||U−V||ν≤dν(U,V)≤(π/2)||U−V||ν.

For any topological parameter space Y and continuous Φ:Y×S^(n−1)→U(N), the formula uses only the continuous evaluations Φ(y,p), Φ(y,x), matrix multiplication and a uniformly nonsingular inverse on the eligible domain, hence is jointly continuous in (y,x,t). No regularity/separation/countability condition on Y is needed. Under constant frames Q,R, the normalized image transforms by R*WR; rational functional calculus then gives H_t(QΦR)=QH_t(Φ)R.

The Cayley algebra identity follows by writing I−F_t=(1−t)(I−W)(I+tW)^−1 and I+F_t=(1+t)(I+W)(I+tW)^−1. Since Re W≥0, I+W is invertible. Their quotient gives C(F_t(W))=((1−t)/(1+t))C(W). This identifies a classical mechanism rather than claiming it new. For L<1, normalized images have eigenangles<π, so the principal logarithm chart provides the stated weaker deformation to Φ(p); no Lipschitz-sublevel preservation for that alternative follows here.

## Boundary falsifiers and exact limits of this reconstruction

1. The manuscript's unnormalized HS metric is essential. For the normalized HS metric, Φ(e^(iθ))=diag(e^(iθ),1,…,1) has Lip=1/√N≤1/2 when N≥4 and nonzero determinant winding. It cannot deform to a constant in the same U(N); for N≥5 this even lies in the strict sublevel. This is an excluded-metric falsifier, not a counterexample to the written theorem.
2. Allowing a left-semicircle eigenangle makes the stated q_t bound fail locally because cosθ<0 lowers the denominator in g'_t. W=−I makes t=1 singular. Thus neither an arbitrary image nor the weaker L<1 domain inherits this specific q_t proof without new arguments.
3. A chordal bound on pairs does not establish the induced length-metric estimate. The source-image geodesic route above closes this gap explicitly.
4. N=1, L=0, t=0, t=1, L exactly1/2, antipodal endpoints, S^1, S^0 angular distanceπ, noncommuting tangent directions and arbitraryY are required controls. n=0, infinite-dimensional unitaries, non-round/disconnected length metrics, arbitrary bi-invariant metric normalizations and sphere fibrations are not claimed.
5. Algebraic and numerical checks can falsify implementations or illustrate finite instances; they cannot certify all n,N and all Lipschitz maps. The analytic argument above covers that universal scope. No formal proof-assistant certification or human peer review is claimed.

Provisional analytic conclusion at this early independent checkpoint: the complete stated theorem and its explicit boundary/family assertions admit the reconstruction above, with no central mathematical gap currently identified. External interpretation of the precise printed Gromov question and classical-source credit remains to be checked from actual primary bodies after sealing this note. Historical firstness and present worldwide openness are not inferred. Default follow-up: none. Scientific findings remain withheld from root pending its initial-independence gate.
