# Turn3: local parameter selection survives kernel perturbation

AI-assisted mathematical proof candidate; independent review pending. Original unresolved3/5. This is a local Banach-space theorem around the exponential comparison bump of Turn2. It does not assert global uniqueness for an arbitrary source kernel or rule out remote branches.

## 1. Functional setting

Fix beta>1 and u in(m*,m_beta). Let J0(x)=exp(−|x|)/2 and let(q0,h0,m0) be the selected even bump from Turn2. Let X be the real Banach space of even continuous functions vanishing at infinity, with the supremum norm. Let K be the affine Banach space of even real L1 kernels with integral1, with L1 norm. Positivity is not required for applying the implicit-function theorem; it is imposed on the physical kernels afterwards.

For h near h0 let m(h) be the smooth negative metastable mean-field branch. Write q=m(h)+p, p in X. Define

G(p,h,J)=m(h)+p−tanh(beta(J*p+m(h)+h)),
B(p,h)=m(h)+p(0)−u.

The map(G,B) takes X×R×K to X×R and is continuously differentiable (indeed smooth in p,h and continuous multilinear in the convolution variables). Convolution L1×C0 -> C0 is bounded; the constant term cancels because m(h)=tanh(beta(m(h)+h)). Its zero set is precisely even solutions with the specified negative limit and prescribed value at0 in this neighborhood.

## 2. Invertibility at fixed field on the even space

At the reference bump set a(x)=beta(1−q0(x)²) and a_infinity=beta(1−m0²)<1. The p derivative is

L=I−a(x)J0*.

The operator I−a_infinity J0* is invertible on X by its convergent Neumann series. The difference −(a−a_infinity)J0* is compact on X. To verify compactness, convolution of the unit ball has a common modulus of continuity bounded by L1 translation differences of J0. Multiplication by the continuous function a−a_infinity tending to zero gives uniform small tails and preserves equicontinuity. Arzelà–Ascoli in C0 applies. Hence L is Fredholm of index0.

Its kernel on X is zero. If L phi=0, let z=J0*phi. Then phi=a z, z is even and vanishes at infinity, and the Green identity gives

z''=(1−a)z.

Let w0=J0*q0+h0. Its derivative w0' satisfies the same linear ODE by differentiating Turn2's equation. On(0,infinity), w0' is nonzero and tends to0; w0'' tends to0. Also z'=J0'*phi tends to0 because J0' is integrable and phi belongs to C0. The Wronskian z*w0''−z'*w0' is constant and tends to0 at infinity, hence is zero. Therefore z=c*w0' on(0,infinity). Evenness gives z'(0)=0, whereas w0''(0)=H(u)−h0<0. Thus c=0. This proves injectivity; the Fredholm alternative gives a bounded inverse for L on X. The odd translation mode is absent only because the space is even; it must not be ignored on the full function space.

## 3. The peak condition removes the field freedom

At fixed J0, invertibility of L gives a smooth nearby branch p(h). Turn2 identifies it with the centered exponential homoclinic family: ordinary ODE continuous dependence on bounded intervals, together with the uniform exponential approach to the nondegenerate negative equilibrium for h near h0, makes that explicit family continuous in the C0 norm after subtracting m(h). It therefore lies in the implicit-function neighborhood and agrees with its unique branch. Its peak U(h)=m(h)+p(h)(0) has nonzero derivative, namely

U'(h0)=1/h0'(u)=[A(u)−A(m0)]/([H(u)−h0]A'(u))<0.

The derivative of the full pair(G,B) in(p,h) is therefore invertible: solve the G equation with L^{-1}, then solve the scalar peak equation using this nonzero Schur complement. Explicitly G_h=m'−a(m'+1), an element of X because m'=a_infinity/(1−a_infinity). The Schur complement is m'−(L^{-1}G_h)(0)=U'(h0).

The Banach implicit-function theorem now supplies delta>0 and a neighborhood of(p0,h0) such that every even normalized J with ||J−J0||_1<delta has exactly one nearby pair(p_J,h_J) solving G=B=0. The solution depends smoothly on the kernel in its affine L1 space. In particular h_J remains positive, m(h_J) stays on the negative metastable interval, q_J(0)=u, and q_J tends to m(h_J).

For a nonnegative kernel, q_J automatically lies in(−1,1) by its equation. It also satisfies q_J>=m(h_J). If it dipped below m, its negative difference from m would attain a global minimum at a finite point. There J*q is at least that minimum value q_min, so q_min>=tanh(beta(q_min+h)). But H is strictly increasing on(−1,m), giving H(q_min)<H(m)=h and the reverse strict inequality, a contradiction. If J is positive in a neighborhood of0, equality q_J=m at one point propagates through the convolution to all points, contradicting q_J(0)=u>m. Thus q_J>m everywhere. Unimodality and whether0 is the global peak are not assumed from mere C0 closeness; they are a separate shape question.

## 4. Actual smooth compact kernels occur arbitrarily near the model, up to spatial scaling

Even nonnegative smooth compactly supported probability kernels can approximate J0 in L1, while being positive and strictly decreasing inside their support on the positive half-line. One explicit approximation route is to replace |x| by sqrt(x²+epsilon²) in exp(−|x|), multiply by a smooth even cutoff which is positive inside(−R,R) and decreasing for x>0, then normalize. Taking epsilon->0 and R->infinity gives L1 convergence by dominated convergence. Both factors are strictly decreasing for x>0 before the cutoff vanishes; the resulting kernel is C-infinity and flat at its support boundary.

The resulting radius R can be normalized to the source's range1 by replacing J(x) by R*J(Rx) and q(x) by q(Rx). Direct change of variables preserves the equation, field h, limit m and value u. This scaling does not identify the exponential kernel with a compact one; it only normalizes the genuinely compact perturbed kernel.

Hence there are smooth compact nonnegative radial-decreasing source-class kernels for which the parameter pair is locally unique near the constructed even profile at this fixed u. This does not prove uniqueness among all profiles or for every source kernel. The local theorem's even-profile shape is resolved separately; no unstated monotonicity follows from the implicit-function theorem alone.

## 5. Controls and credit

The proof uses standard Fredholm/compactness and implicit-function principles, with the crucial kernel calculation derived explicitly rather than assuming a spectral gap from numerical eigenvalues. The checker verifies the linearization identities, Schur-complement formulas and norm estimates in exact symbolic/finite matrix analogues. Finite matrices do not certify the infinite-dimensional inverse; Sections2–3 supply that argument. No novelty certification is claimed.
