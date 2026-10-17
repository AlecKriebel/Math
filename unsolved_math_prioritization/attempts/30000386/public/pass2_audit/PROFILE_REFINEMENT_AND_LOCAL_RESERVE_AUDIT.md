# Acceptance: sharper triple certificate and local-linear reserve obstruction

Shared PASS2 scoped supplement. These results preserve every previously frozen proof and audit.

## Audited inputs

- `../pass2_invariant/THREE_DEADLINES_PROFILE_REFINEMENT.md`, SHA-256 `41c9f1edb447eb8aba645602823d3ee583481be4264d1a903b583c5a3be8a926`.
- `../pass2_invariant/LOCAL_LINEAR_RESERVE_OBSTRUCTION.md`, SHA-256 `70c1a39b4c2b4f5e5498ec55add96d550481a207fdfe576a86c610ca5ef2c1e3`.
- `../pass2_invariant/profile_certificate.py`, SHA-256 `bc2c62874c2a9710d8839a75e782c349b4adbded87a78d52923d2e7bf4261409`.

Both mathematical statements are accepted within their stated scope. The numerical claim about the uniform recursion was also independently replayed.

## 1. The improved 52/103 certificate

For g=b_17+(U*b_21)/53, where U is the side-nine square indicator, the exact maximal square-average profiles are c_g(9)=1/53 and c_g(3)=1/9. The first follows by comparing delta mass 1/81 with the uniform kernel's constant value 1/53 on a complete side-nine square. The second follows by comparing 1/9 with 1/53.

The profile-aware gap-four boundary denominator is therefore

D_2=81[1−1/53−3(1/9)]=2781/53>0.

This reserves the post-time-13 announcement by c_g(9), and the updates after moves 14,15,16 by 3c_g(3). With pre-boundary local mass strictly below D_2, the terminal g value at time 17 is strictly below one. The already accepted integer reserve at time 17 then permits the round-17 update and wins at time 21.

The earlier hazard f has update kernels delta, U/D_2, and (U*U)/2781. Write u=1_[−4,4]. Since U=u tensor u, its convolution factors into two copies of the triangular sequence 9−|x| for |x|≤8. The maximal sum in nine consecutive entries is the centered sum 61. Hence the largest side-nine average of the double convolution kernel is 3721/(81·2781), which is less than 53/2781 because 3721<4293. Both it and the delta average 1/81 are below the middle kernel's exact average 53/2781.

Thus c_f(9)=53/2781. At side three, each smeared kernel's peak is below 1/9, while the delta attains average 1/9. Therefore c_f(3)=1/9 and the terminal-time-13 bound is

9(53/2781)+3(1/9)=52/103<1.

All fields use only already announced pairs. The improvement changes no phase timing or allowed timestamps. It strengthens the certificate for {13,17,21}; it is not a theorem for a larger family of deadlines.

## 2. Exact local-linear one-round reserve criterion

For nonnegative weights w on the nine available next positions, consider the implication: a nonnegative field g with sum w_v g(v)<1 retains some value below one after any single unit point update.

Necessity of the eight-subset condition is exact. If an eight-element subset A has total weight below one, set g=1 on A and zero at the remaining point. The test passes, but updating the remaining point leaves no safe move.

For sufficiency, if fewer than two points had value below one, some eight-element subset would have all values at least one. Its weights sum to at least one, contradicting the test. Thus at least two subunit points exist; a single update can alter at most one and leaves another safe.

Writing S=sum w_v and M=max w_v, the criterion is S−M≥1. Since M≥S/9, this forces S≥9/8. Equality forces every weight to be 1/8, and these weights do satisfy the criterion. The claimed minimum mass and uniqueness are therefore correct for arbitrary nonnegative fields in this local linear class.

## 3. Repeated smoothing and its scope

Nonnegative convolution multiplies total mass. A chain of k such locally robust kernels has mass at least (9/8)^k and support in [−k,k]². Its peak is therefore at least (9/8)^k/(2k+1)², which tends to infinity. A side-three square containing a peak has average at least one ninth of it, so concentration cannot remain uniformly bounded either.

For the particular uniform profile recursion with consecutive unit gaps, the current-deadline delta is always a kernel type, forcing c(3)≥1/9 and D=9[1−c(3)]≤8 whenever the denominator is positive. Its uniform convolution kernel thus has mass at least 9/8 at each successful step. Assuming infinitely many positive steps would make the old kernel's concentration eventually reach one, contradicting positivity of the next D. This proves eventual finite failure of that certificate analytically.

This is not an impossibility result for all linear potentials, nonlinear tests, structured reachable fields, simultaneous treatment of multiple deadlines, or actual Angel strategies. In particular, the universal local test requirement is stronger than a condition established only on a maintained state family.

## 4. Independent exact check of the reported 27th step

The supplied program was run and returned the denominators 53 and 2781/53, bound 52/103, and first nonpositive consecutive-gap denominator at smoothing step 27.

The independent program `check_profile_recursion_independent.py` imports none of that code. For each convolution age m it computes the one-dimensional coefficients directly as trinomial counts, finds the largest three-entry sum, and divides its square by nine and the product of the relevant previous divisors. This gives each candidate kernel's exact side-three average. Taking the maximum and applying D=9(1−c(3)) produces positive denominators for steps 1–26 and a negative denominator at step 27.

Every rational profile and divisor is retained in `independent_profile_recursion_replay.json`, SHA-256 `90a57ef2c10953d1de3d403ffb12d5d01aae00934a74aaf41fb5b8e063fab3e8`. This certifies a failure of this sufficient recursion, not a loss in a game with 28 allowed times.
