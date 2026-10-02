# Turn5: one compact source-class kernel family for a whole peak interval

AI-assisted proof candidate; independent review pending. Original unresolved5/5. No sixth author search. This turn makes the local persistence uniform over any fixed compact peak interval, and states the remaining crossing obstruction explicitly. The general all-kernel, all-peak uniqueness conjecture is not claimed solved.

## 1. Uniform continuation theorem

Fix beta>1 and a compact interval I=[u0,u1] strictly inside(m*,m_beta). For the exponential reference kernel J0, let z0(u)=(p0(u),h0(u)) be the centered selected family of Turns2–3, with p0=q0−m(h0). The family is smooth in the even C0 Banach space times R. Its bordered derivative A_u=D_z(G,B) at z0(u) is invertible for every u in I, and the inverse depends continuously on u. Compactness gives a finite bound M for ||A_u^{-1}||.

There exist r,delta>0 such that every normalized even real kernel J with ||J−J0||_1<delta has, for each u in I, a unique solution z_J(u) in the radius-r neighborhood of z0(u). These solutions form a jointly smooth local family. The radii can be chosen so h_J>0 and m(h_J) remains in the negative metastable branch throughout I.

Here is a uniform argument rather than a bare pointwise appeal to the implicit-function theorem. Uniform continuity of the derivative near the compact reference family allows r,delta so small that

||A_u^{-1}(D_z F(z,u,J)−A_u)||<=1/2

whenever ||z−z0(u)||<=r, u in I, ||J−J0||_1<=delta, where F=(G,B). The residual at z0(u) is bounded by C||J−J0||_1 uniformly, since tanh is Lipschitz and the reference p0(u) are uniformly bounded. Shrink delta further so MC delta<=r/2. The map z -> z−A_u^{-1}F(z,u,J) is then a contraction mapping of the closed radius-r ball into itself. It gives a unique solution for every(u,J), uniformly. Local smooth implicit functions agree on overlaps by this uniqueness, proving the smooth family claim.

Since h0'(u)<0 continuously on I, there is c_I>0 with h0'(u)<=−c_I. Continuity of the differentiated implicit equations and uniform inverse bounds permit a further common delta for which

partial_u h_J(u)<−c_I/2<0 for every u in I.

Thus the selected branch is strictly decreasing in its peak and is unique in the stated uniform neighborhood. This is branch-local uniqueness, not a statement that every solution at that u lies in the neighborhood.

## 2. One genuinely smooth finite-range kernel works for all u in I

For epsilon>0 and R>2 choose an even C-infinity cutoff chi_R, equal to1 on[−R+1,R−1], positive inside(−R,R), zero outside, and nonincreasing for x>0. Set

K_epsilon,R(x)=(1/2)exp(−sqrt(x²+epsilon²))*chi_R(x),
J_epsilon,R=K_epsilon,R/integral K_epsilon,R.

It is smooth, positive inside its support and strictly decreasing for x>0 there. Since0<=sqrt(x²+epsilon²)−|x|<=epsilon, its mass loss from J0 is at most epsilon+exp(−(R−1)). Normalization costs at most the same loss again, so

||J_epsilon,R−J0||_1 <=2[epsilon+exp(−(R−1))].

Choose epsilon small and R large so this is less than the uniform delta/2. This **single** kernel has the continued family for every u in I. Since it is nonnegative and positive near0, Turn3 gives q_J>m. Turn4 then gives its unique symmetry center and strict unimodality; evenness fixes that center at0. These are genuine bumps with peak u, not merely even nearby solutions.

Normalize the range to1 by tildeJ(x)=R*J_epsilon,R(Rx) and tildeq_u(x)=q_J(Rx). A change of variables proves the same integral equation with identical h(u),m(u),u. Thus tildeJ belongs to the actual smooth compact radial-decreasing source class. A sufficiently small relative L1 neighborhood of this kernel within that physical class has the same uniform local branch property, because scaling is an L1 isometry on the kernels and a supremum-norm isometry on profiles.

The neighborhood depends on beta and I. Nothing here supplies one uniform perturbation size as u tends to either endpoint, especially u->m_beta where the exponential branch field and its peak derivative vanish. One must not exchange these limits to claim the full open interval for a fixed arbitrary source kernel.

## 3. A necessary crossing pattern for competing selected parameters

For clarity, suppose two centered even bumps for the same normalized nonnegative kernel have the same peak u, but fields h2>h1 on the negative metastable branch. Then m2>m1 because H is increasing there, so q2−q1 tends to a positive number at both infinities. At the common peak, subtracting A(u)=J*q_i(0)+h_i gives

integral_R J(y)[q2(y)−q1(y)]dy=−(h2−h1)<0.

Hence q2<q1 somewhere inside the kernel's effective support, despite its higher far-field level. Continuity forces a crossing on each side between that negative region and the positive tail. Moreover

integral J(y)[q1(y)−q2(y)]_+ dy >= h2−h1,
sup_y[q1(y)−q2(y)]_+ >= h2−h1.

Thus globally ordering profiles by their tail magnetization is an invalid route to general uniqueness. If two such solutions were globally ordered, their fields would have to agree: the tail order and the peak equation rule out strict field order. With equal fields and global order, equality at the peak and positivity of J near0 propagate equality to the whole line. So an ordered family has at most one solution at each peak, but the existence of such an order for all bumps has not been proved and cannot be assumed.

This explains the precise remaining gap between the locally unique branch above and the original global parameter uniqueness question.

## 4. Final disposition and checks

Five substantive turns are complete. The packet proves an actual-kernel necessary field bound, a fully solvable exponential comparison model, local persistence, compact-kernel bump shape, and a uniform locally unique source-class family on each compact peak interval. It does not prove full existence/uniqueness for every source kernel and every peak, or exclude other distant branches for the constructed kernels. The half-line continuation convention remains explicitly source-qualified.

The checker verifies the uniform-contraction bookkeeping with exact rational constants, the normalization-error inequality algebra, scaling identities and the crossing-area lower bound in finite exact fixtures. It is not an infinite-dimensional numerical certificate. All analytic claims rest on the written proofs. Classical Green-kernel, phase-plane, Fredholm, implicit-function and moving-plane methods retain their credit; no novelty certification is made.
