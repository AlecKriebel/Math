# Turn4: symmetry and strict unimodality of compact-kernel homoclinic profiles

AI-assisted proof candidate; independent review pending. Original unresolved4/5. The method is classical moving planes for positive integral kernels; no novelty claim. Related homoclinic existence/stability literature includes Chmaj–Ren,JDE155(1999),17–43, DOI10.1006/jdeq.1998.3571; its publisher abstract was checked, but the present argument is self-contained and is not attributed as a new result absent a full priority comparison.

## 1. Hypotheses and positivity above the negative phase

Let J be an even bounded continuous probability density, zero outside[−R,R], positive for |x|<R and strictly decreasing as a function of |x| inside(0,R). Let q be a nonconstant continuous full-line solution q=tanh(beta(J*q+h)), taking values in(−1,1), with the same limit m at both infinities. Assume beta>1,h>0 and m in(−m_beta,−m*), so m=tanh(beta(m+h)) and beta(1−m²)<1. We do not initially assume q even or unimodal.

As in Turn3, q cannot dip below m: a negative deviation attains its minimum, and monotonicity of H on(−1,m) contradicts the equation there. If q=m at a finite point, positivity of J near0 propagates equality to an open neighborhood and then to the whole line. Thus p=q−m is strictly positive and tends to0 at both infinities.

Choose eta>0 so small that m+eta<−m*. There is kappa<1 bounding beta(1−t²) for t in[m,m+eta]. Outside a sufficiently large compact interval p<eta. This supplies the tail contraction used below. There is no global contraction assumption across the unstable middle of the bump.

## 2. Reflection equation and strict positivity propagation

For a plane point lambda put p_lambda(x)=p(2lambda−x), D_lambda(x)=p(x)−p_lambda(x), x>lambda. Splitting the full convolution into reflected half-lines gives

D_lambda(x)=a_lambda(x) integral_{y>lambda} K_lambda(x,y)D_lambda(y)dy,
K_lambda(x,y)=J(x−y)−J(x+y−2lambda),

where0<a_lambda(x)<=beta is the tanh secant derivative. When D_lambda(x)>0 and x is in the far-right tail, both q(x) and q(2lambda−x) lie in[m,m+eta], so a_lambda(x)<=kappa. This last implication uses positivity and the ordering at a violation; it does not require the reflected point itself to lie in the tail.

For x,y>lambda, |x−y|<x+y−2lambda, hence K_lambda>=0. It is strictly positive whenever |x−y|<R, by strict radial decrease and support. Also integral_{y>lambda}K_lambda(x,y)dy<=1.

If D_lambda<=0 everywhere, either it vanishes identically or it is strictly negative everywhere on the open half-line. Indeed a point of strict negativity gives negativity in its R-neighborhood through the integral equation; iteration along overlapping intervals propagates it to every point. This is the strong comparison step, not an assumed differential maximum principle.

## 3. Starting and moving the plane

For lambda sufficiently far to the right, D_lambda cannot have a positive maximum. If it did, its maximizer x>lambda lies in the small tail, so the reflection equation gives M<=kappa*M with M>0, a contradiction. A positive maximum is attained because D_lambda is continuous, vanishes at the plane and tends to0 at infinity. Thus D_lambda<=0 for every sufficiently large lambda.

Let lambda0 be the infimum of plane locations such that D_mu<=0 for every mu at or to their right. This is finite: it is bounded above by the starting region, and bounded below because reflecting any fixed positive-height point far to the left eventually compares it with a tail value tending to0. Continuity gives D_lambda0<=0.

Suppose D_lambda0 is not identically zero. Then it is strictly negative on the open half-line by Section2. We show the plane can move a little farther left, a contradiction.

Choose epsilon>0 small enough that2*beta*||J||_infinity*epsilon<1. Choose a far-right cutoff M so that p(x)<eta for x>M and M>lambda0+epsilon+R+1. On the fixed compact interval[lambda0+epsilon,M], strict negativity at lambda0 has a uniform margin. For lambda sufficiently close to lambda0 on its left, continuity preserves negativity on this interval. Any positive part of D_lambda is therefore supported only in the strip(lambda,lambda0+epsilon), whose length is at most2epsilon, or in the tail x>M.

There is no kernel coupling from the strip to the tail, since their separation exceeds R; the reflected term also vanishes there. At a positive strip maximum the reflection equation therefore gives

M_strip<=2*beta*||J||_infinity*epsilon*M_strip,

so M_strip=0. A remaining positive tail maximum then satisfies M_tail<=kappa*M_tail, so it too is zero. Supremum arguments give the same conclusion if one of the regions has no maximizer. This proves D_lambda<=0 for all nearby leftward planes; together with the existing inequalities for mu>=lambda0 it contradicts the defining infimum.

Hence D_lambda0 is identically zero: q is symmetric about lambda0. There is only one such center, because two distinct reflection centers would make a nonconstant function periodic, inconsistent with its limit m at infinity.

For every lambda>lambda0, the established inequality D_lambda<=0 is strict, since symmetry about another center is impossible. Given lambda0<=a<b, choose lambda=(a+b)/2 and x=b to obtain p(b)<p(a). Thus q is strictly decreasing to the right of its center and strictly increasing to its left.

## 4. Consequences for the source-supported family

Any nonconstant homoclinic profile under these hypotheses is a single symmetric bump, up to translation. If the profile is already even about0, as in Turn3, uniqueness of the reflection center forces lambda0=0, so its prescribed q(0)=u is its actual global peak. Hence the locally persisted profiles for smooth compact strictly decreasing kernels are genuine reflected unimodal bumps. Turn1's energy bound applies to them.

This removes a shape assumption in the strictly decreasing compact-kernel subclass. It does not prove uniqueness of the field or of the centered bump for a fixed general kernel: distinct single bumps can still differ in their profile and parameter. Non-strictly decreasing, sign-changing, noncompact or unspecified half-line kernels require separate treatment and are not silently included.

## 5. Checks and limitations

The checker verifies exact reflection-kernel positivity/support inequalities for a C3 compact polynomial kernel, the strip/tail contraction arithmetic, and the reflected-convolution splitting on polynomial test functions. These fixtures are not solutions and do not prove a global maximum principle by sampling. The full continuation argument with its narrow-strip and tail estimates is supplied above. Classical moving-plane reasoning is credited and no priority claim is made.
