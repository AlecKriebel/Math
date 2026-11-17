# Post-INITIAL derivations and closure

These notes continue, and do not replace, the independent source-only INITIAL and OWN_DERIVATIONS. No current root or peer findings were read. The first nine groups of controls were already sealed before any supporting program or outside mathematical body. The convex-hull calculation below was prompted by the subsequently read native diagnostic and is not represented as presealed discovery.

## Full-original proof interfaces

The original theorem concerns every normalized holomorphic injection with real Taylor coefficients, not a finite coefficient truncation or a subclass of slit maps. A proposed counterexample must remain globally univalent on the entire open disk; local nonvanishing of the derivative alone is insufficient.

For F(z)=z+a₂z²+… in S, let L be the normalized holomorphic logarithm of F(z)/z and H(w)=w exp(−L(w⁻²)/2), |w|>1. If H(w₁)=H(w₂), injectivity of F after squaring gives w₂=±w₁. Oddness and nonvanishing eliminate the minus sign. Thus H is an exterior injection. Green area on the positively oriented image of |w|=R gives Σ n|bₙ|²R⁻²ⁿ≤R². Taking finite partial sums, R↓1, then the number of terms to infinity yields Σ n|bₙ|²≤1. Here b₁=−a₂/2. If |a₂|=2, every other negative coefficient vanishes and H=w−λ/w, |λ|=1, which recovers F=z/(1−λz)². This independently closes the coefficient-equality input used by the manuscript; it does not assume the target strict inequality.

For the normalized Koebe transform Tₐf, the quadratic coefficient is A_f(a)/2. Equality therefore classifies Tₐf as a Koebe rotation. It does not classify f itself as such a rotation. Undoing the transform classifies f(D) as the complement of a ray. The presealed example T_{i/2}k₊, with equality at −i/2 but a₂=(6+4i)/5, makes this distinction substantive.

For a real-coefficient f the omitted ray is invariant under conjugation. Its unique endpoint is real, but that alone is insufficient: invariance also forces the ray's direction to be real. Since 0 belongs to f(D), its endpoint is nonzero and the ray points away from 0. The image is therefore exactly that of 4|c|k₊ or 4|c|k₋. Composing inverse conformal maps produces a disk automorphism fixing 0. Its derivative has modulus 1/(4|c|), so |c|=1/4; the derivative is positive and normalized, so the rotation is the identity. This eliminates oblique rays and nontrivial precompositions, and forces f=k₊ or k₋.

For these two functions |A|²=16−48(Im z)²/|1−z²|². No nonreal point is an equality point. Equality at both opposite real endpoints A_{k₊}(x)=4 and A_{k₋}(x)=−4 also forbids a smaller enclosing radius after translating the center, for the original question at nonzero real x. At z=0 that original expression is identically zero, whereas A_f(0)=f″(0); the source explicitly separates them.

The remaining logical risk is a supremum approaching 4 without equality. The radial P estimate gives uniform compact-disk bounds on f and f′. Montel yields subsequences; the normalization f′(0)=1 prevents constant limits. Applying Hurwitz to the nonvanishing divided differences retains injection and nonzero derivative in the limit. Reflection is closed. Thus S_R is compact and (f,z)↦|A_f(z)| is jointly continuous on interior compact sets. An attained maximum of 4 would contradict the equality classification. The same argument on S_R×K gives the claimed uniform compact-nonreal gap. Separate pointwise strictness alone would not have justified this step.

The coefficient argument, reflection classification, and compactness are classical analytic deductions. The arithmetic diagnostic below does not establish these universal steps.

## Reduction, edges, and competing examples

For real a, Tₐ preserves S_R bijectively with inverse T₋ₐ and covariance phase (1+a conjugate(w))/(1+aw). That phase has modulus one. Reflection and real disk automorphisms preserve δ=|Im z|/|1−z²|. The identity |1−z²|²=(1−|z|²)²+4(Im z)² gives δ<1/2 for all interior z. Solving x a²−(1+|z|²)a+x=0 with the interior root moves z to ±it; δ=t/(1+t²) is strictly increasing for 0≤t<1. This proves the orbit reduction without asserting arbitrary rotational invariance of the real class.

The Koebe maps give 4√(1−3δ²). The function h=z/(1−z²) is an admitted injection because h(z)=h(w) implies (z−w)(1+zw)=0 and |zw|<1. Its pre-Schwarzian is 2z(3+z²)/(1−z⁴), so A_h(it)=8it/(1+t²); real transforms give the lower bound 8δ at all points. At i/2, the squared bounds 208/25 and 256/25 show that the two real Koebe maps cannot be the sole possible maximizers. This gives no sharp formula or classification of the actual maximizers.

No positive global gap survives: approach an interior real point through nonreal points for δ→0, or let it→i for δ→1/2. Conversely merely Im z→0 near ±1 does not force δ→0; along z=1−s+ics, δ→c/(2√(1+c²)). These presealed controls prevent overstating either the uniformity or the endpoint obstruction.

## A post-code control against a convex-hull shortcut

The average q=(k₊+k₋)/2 equals z(1+z²)/(1−z²)². Differentiation gives q′=(1+6z²+z⁴)/(1−z²)³. At z=i(√2−1), z²=−3+2√2 and the numerator vanishes. Since 0<√2−1<1, q is not locally univalent throughout the disk and hence q∉S_R. The class is not convex. Koepf's classification of extreme points for linear functionals cannot be converted into an optimization of the nonlinear quotient f″/f′ over a convex hull. This is an obstruction to that shortcut, not a defect in the manuscript's different proof.

## Actual diagnostic interpretation

The sole ordinary native run used the exact 4040-byte author/exact_controls.py, copied without alteration into native-route. It used standard-library Fraction arithmetic, including a Gaussian-rational Q class and pairs representing Q(√2). The actual result was PASS, 3558 predicates across 16 labels, exit 0, stdout 843 bytes, stderr empty. The pre-run hand count matched the output. NATIVE_INVOCATION and NATIVE_RECEIPT retain exact argv, times, streams and source guards.

Executed native operations were the top-level fixed rational loops; Q construction/coercion/arithmetic/conjugate/norm2/power; pk, ph, A, require, check; pairadd and pairmul; and final JSON serialization. Assertions were not used as proof, and no optimized interpreter variant ran. No ODE, Loewner exploration, other script, archived stored result, import campaign or formal prover was executed.

One diagnostic label requires a narrower reading: negative_control_uniform_gap_rejected evaluates the real point 1/2. Its result rejects a purported improvement on the entire disk including the real diameter. That finite test alone does not disprove a uniform gap restricted to nonreal points. The separate analytic nonreal sequences above establish the stronger statement actually claimed by the paper. The other negative labels distinguish 48 from 47 and the conjugate covariance phases at chosen exact points; finite distinction is not a universal identity proof.

No counterexample or substantive gap was found in the full original mathematical conclusions. Historical priority and exhaustive literature overlap are different questions and remain explicitly limited in PRIMARY_INTERFACES and REPORT. No repair or narrowed replacement was attempted.
