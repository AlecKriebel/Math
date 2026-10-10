# Approach 1: a local-to-compact realization argument

**Authored partial theorem submitted for independent audit.** This is one new approach addressing the PDE/ODE distinction, not a new attempt at the missing global Weyl inequality. No historical novelty is claimed.

Throughout, n >= 4, d > 0, curvature-operator norms are Hilbert–Schmidt norms, Q(R)=R^2+R#, and

\[
 F_d(R)=\operatorname{scal}(R)-d\|W(R)\|,\qquad K_d=\{F_d\ge0\}.
\]

A condition is *PDE-preserved* here if every smooth Ricci flow on every closed n-manifold initially satisfying it continues to satisfy it throughout its smooth existence interval. We do not use the terminology that defines “Ricci-flow-invariant cone” to mean ODE invariance in advance.

## Claimed theorem

For this particular family, K_d is PDE-preserved if and only if it is preserved by the Hamilton ODE. In fact, every failure of ODE preservation gives a smooth initial metric on S^n satisfying F_d >= 0 everywhere and a subsequent negative value under its Ricci flow.

The sufficiency is Hamilton's tensor maximum principle. The converse follows from the lemmas below. The proof controls the normal component of the curvature Laplacian; it does not claim to set the entire curvature Laplacian, or the full second covariant derivative, to zero.

## 1. Exact conformal covariance

Put a_n=4(n-1)/(n-2). For any smooth positive v and g_tilde=v^{4/(n-2)}g,

\[
 F_d(g_{\rm tilde})=v^{-\frac{n+2}{n-2}}
 \big(-a_n\Delta_gv+F_d(g)v\big). \tag{1}
\]

Indeed, scalar curvature has the usual conformal-Laplacian transformation, and the Weyl-operator norm transforms by v^{-4/(n-2)}. A change between tensor and operator norm only rescales the fixed coefficient d. This identity is pointwise and remains valid where W vanishes; differentiation of the norm is used only where W != 0.

## 2. A boundary germ with vanishing first curvature jet

Let R_* be any algebraic curvature operator with W_* != 0 and F_d(R_*)=0. There exists a real analytic metric g near 0 in R^n such that

\[
 R_g(0)=R_*,\qquad \nabla R_g(0)=0,\qquad F_d(g)\equiv0
 \text{ on a neighborhood of }0. \tag{2}
\]

Start with the quadratic normal-coordinate model
h_ij(x)=delta_ij-(1/3) R_{*ikjl} x^k x^l, using the sectional-positive sign convention. It is positive definite on a sufficiently small ball. Directly from the normal-coordinate curvature formula, its curvature at 0 is R_*; its first derivatives and third derivatives at 0 vanish, giving nabla R_h(0)=0. Consequently F_d(h)(0)=0 and its first coordinate derivatives vanish. Since W_*(0) != 0, the squared Weyl norm stays positive near 0 and F_d(h) is real analytic there.

Solve the linear analytic Cauchy problem

\[
 \Delta_h v=a_n^{-1}F_d(h)v,\qquad
 v(x',0)=1,\qquad \partial_n v(x',0)=0. \tag{3}
\]

The coefficient of partial_n^2 v is h^{nn}>0, so the hypersurface is non-characteristic. The Cauchy–Kowalevski theorem supplies an analytic local solution. This is local analytic existence, not a claim of well-posedness of elliptic Cauchy data in a smooth norm. Shrinking the neighborhood ensures v>0.

The data give v(0)=1 and all tangential derivatives of v and tangential derivatives of partial_n v equal to zero. At 0, equation (3), together with F_d(h)(0)=0, gives partial_n^2 v=0. Differentiating (3) once in any coordinate, all coefficient terms multiplying first or second derivatives of v vanish; dF_d(h)(0)=0 then gives partial_k partial_n^2 v=0. Thus every derivative of v of orders 1, 2, or 3 vanishes at 0: v=1+O(|x|^4). Set g=v^{4/(n-2)}h. Its metric 3-jet equals that of h, and (1), (3) imply (2).

No arbitrarily assigned fourth-order metric jet is being assumed compatible with differential Bianchi identities. The actual analytic metric solves that compatibility obligation automatically.

## 3. Compact extension preserving F_d >= 0

More generally, let g be a smooth metric germ with F_d(g)>=0 near its center. Its restriction to a sufficiently small ball is isometric to a region of a smooth metric G on S^n with F_d(G)>=0 everywhere. The construction leaves g exactly unchanged on an inner ball.

Use geodesic normal coordinates at the center, so g_ij x^j=x_i. Let b be the unit round sphere metric in its normal coordinates. Both metrics have the same value delta at the center, vanish to first order there, and have the same radial gauge. Fix a small coordinate radius r_0. For sufficiently small epsilon, define

\[
 g_\epsilon=\chi(r/\epsilon)g+(1-\chi(r/\epsilon))b,
\]

where chi=1 for r<=2epsilon and chi=0 for r>=3epsilon. Extend it as b outside the coordinate chart. This convex combination is positive definite and remains in radial gauge; thus |grad r|=1 away from the center. The usual differentiated cutoff estimates give constants A,B independent of sufficiently small epsilon such that on 0<r<r_0,

\[
 \Delta_{g_\epsilon}r\ge\frac{n-1}{r}-Ar,\qquad
 |F_d(g_\epsilon)|\le B\quad(2\epsilon\le r\le3\epsilon). \tag{4}
\]

For clarity, the estimates follow from g-b=O(r^2), partial(g-b)=O(r), and bounded second derivatives. Differentiating chi(r/epsilon) costs epsilon^{-1} or epsilon^{-2} only where r is comparable to epsilon. Therefore g_epsilon-delta=O(r^2), partial g_epsilon=O(r), and partial^2 g_epsilon=O(1), uniformly. The radial-volume formula gives (4). The possible negative values of F_d(g_epsilon) are confined to the cutoff shell [2epsilon,3epsilon].

Choose a nonnegative smooth phi vanishing outside [1,4], positive throughout (1,4), and at least 1 on [2,3]. Set

\[
 w(r)=r^{n-1}e^{-Ar^2/2},\qquad
 v_\epsilon'(r)=-\frac M{w(r)}
       \int_\epsilon^r w(s)\phi(s/\epsilon)\,ds,\qquad
 v_\epsilon(\epsilon)=1, \tag{5}
\]

and v_epsilon=1 for r<=epsilon. Here M is a fixed constant with a_n M>B, independent of epsilon. This function is smooth across r=epsilon. It is nonincreasing and satisfies

\[
 v_\epsilon''+\left(\frac{n-1}{r}-Ar\right)v_\epsilon'
       =-M\phi(r/\epsilon).
\]

Because v_epsilon'<=0, the *lower* bound on Delta r in (4) gives the needed *upper* bound

\[
 \Delta_{g_\epsilon}v_\epsilon\le -M\phi(r/\epsilon). \tag{6}
\]

For fixed r_0 and A, the integral in (5) is O(epsilon^n) after r>=4epsilon. Near its support, |v_epsilon'|=O(M epsilon). Integrating the tail r^{1-n} gives, since n>2,

\[
 \sup_{r\le r_0}|v_\epsilon(r)-1|=O(M\epsilon^2). \tag{7}
\]

All constants may depend on the fixed germ, n,d,r_0,phi, but not epsilon. In particular, v_epsilon lies between 1/2 and 1 when epsilon is small.

On r<=r_0/2, (6) and (1) show nonnegativity: where F_d(g_epsilon)>=0, both terms in the numerator of (1) are nonnegative; on the cutoff shell the numerator is at least a_n M-B>0. The Weyl tensor need not be nonzero in this step.

To make the conformal change compactly supported, take a fixed smooth eta=1 on r<=r_0/2 and eta=0 near r>=r_0, and put
v_tilde=1+eta(r)(v_epsilon-1).
On the fixed outer annulus, equation (5) yields first and second derivatives O(epsilon^n), while (7) gives v_epsilon-1=O(epsilon^2). Hence v_tilde-1 tends to zero in C^2 there. This annulus has g_epsilon=b and F_d(b)=n(n-1)>0, so
-a_n Delta_b v_tilde+n(n-1)v_tilde>0 for all sufficiently small epsilon. Set
G=v_tilde^{4/(n-2)}g_epsilon.
It is smooth globally, equals g on r<=epsilon, and satisfies F_d(G)>=0. This proves the extension lemma rather than presupposing an arbitrary cone-preserving gluing theorem.

## 4. An outward ODE velocity becomes a PDE failure

Suppose R_* is on the smooth boundary and

\[
 D F_d(R_*)[Q(R_*)]<0. \tag{8}
\]

Apply the boundary-germ lemma and the compact-extension lemma. Start the smooth short-time Ricci flow from G on the closed sphere. In moving orthonormal frames,
partial_t R=Delta R+2Q(R). At the chosen point, nabla R=0 and F_d(G) is identically zero in a neighborhood. The chain rule therefore gives

\[
 D F_d(R_*)[\Delta R]=\Delta F_d(G)=0.
\]

The Hessian-of-F term in the chain rule vanishes because nabla R=0. Therefore

\[
 \left.\partial_t F_d(R_{G(t)}(0))\right|_{t=0}
       =2D F_d(R_*)[Q(R_*)]<0.
\]

The initial condition belongs to K_d everywhere, but the evolved curvature leaves it at this point for all sufficiently small positive times. This is a compact geometric counterexample, not just an algebraic ODE trajectory.

## 5. The nonsmooth scalar-zero locus

The only nonsmooth boundary points have scal=0 and W=0, with unrestricted traceless Ricci component. For a tangent vector V at such a point, membership in the tangent cone is exactly
scal(V)>=d||W(V)||.

If Q(R_0) violates that condition, its Weyl part is nonzero: scal Q(R_0)=|Ric R_0|^2>=0. Let U be the unit Weyl tensor in the direction W(Q(R_0)). With I the sectional-one operator, define

\[
 R_\epsilon=R_0+\epsilon I+
           \frac{n(n-1)}d\epsilon U.
\]

These are smooth boundary points, and

\[
 D F_d(R_\epsilon)[Q(R_\epsilon)]
 \longrightarrow \operatorname{scal}Q(R_0)-d\|W(Q(R_0))\|<0.
\]

Thus every failure of the tangent-cone condition is witnessed at a smooth boundary point. The finite-dimensional tangent-cone invariance theorem for locally Lipschitz vector fields says that a closed convex cone is ODE-preserved exactly when that condition holds everywhere. Combining this with section 4 proves the claimed equivalence.

## 6. Consequence, and what remains missing

The rank-815 packet defines
mu_n=max ||P_W(S wedge S)||/|S|^2 over nonzero traceless symmetric S, and
beta_n=max <Q(W),W>/||W||^3 over nonzero Weyl W.
Its audited ODE criterion, combined with the theorem above, becomes

\[
 K_d\text{ is PDE-preserved}\quad\Longleftrightarrow\quad
 n\beta_n\le d\le\frac{n-2}{\mu_n}. \tag{9}
\]

This is an exact reduction with unevaluated extrema, not the requested explicit high-dimensional classification. At every even dimension, the rank-815 model bounds force d=d(n) if preservation occurs. At n=12 the unresolved bound remains beta_12^2<=55/36; all larger even dimensions and the strict odd-dimensional margin remain obligations. No estimate for those missing global extrema is supplied here.

The proof concerns the closures appearing in the actual 2008 theorem and necessity conjecture. A statement about strict initial inequalities is not silently substituted. Nor is a theorem for arbitrary closed convex curvature cones claimed: the conformal covariance (1) is essential.

## Audit priorities

Independently check analytic Cauchy solvability and preservation of the full metric 3-jet; uniform radial-gauge cutoff estimates; the sign in (6); the O(epsilon^2) tail and outer cutoff; and the normal-Laplacian cancellation in section 4. The executable diagnostics check identities and sign-sensitive algebra only. They do not replace the geometric existence arguments.
