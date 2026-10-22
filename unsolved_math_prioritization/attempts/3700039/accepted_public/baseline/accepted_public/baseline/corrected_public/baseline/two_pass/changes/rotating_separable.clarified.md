# Common rotating-separable patterns

This extension is a partial result, not the unrestricted conjecture. It includes the logarithmic-spiral class in `spiral_lemma.md`; no novelty claim is made.

## Angular lemma

Let A>0, C>0, B real, and let h_j be real continuous 2*pi-periodic functions satisfying

A h_j'' + B h_j' + C h_j >=0

in distributions. Then the angular integral of median(h_1,h_2,h_3) is nonnegative.

Proof. Divide by A and consider the two characteristic roots.

If they are a+-i*b with b>0, the operator is (D-a)^2+b^2. The variation-of-constants proof in `spiral_lemma.md` gives

h_j(theta+pi/b)+exp(a*pi/b) h_j(theta)>=0.

This passes to the median and integrates to the assertion.

If both roots are real, they are nonzero and have the same sign, since their product is C/A>0. First take smooth h and write (D-lambda_1)(D-lambda_2)h=f>=0. For any nonzero real lambda, a smooth periodic solution of y'-lambda*y=f>=0 has sign opposite to lambda: at a positive maximum when lambda>0, or a negative minimum when lambda<0, the equation would otherwise contradict f>=0. Applying this twice shows h>=0. The same reasoning works for repeated roots. For distributional data, convolve h with nonnegative circular mollifiers, apply the smooth argument, and pass to the uniform limit. Thus every h_j is nonnegative in this case, proving the assertion.

## Rotating-separable theorem

Let F:R->(0,infinity) and psi:R->R be C^2, with F(t)->0 as t->-infinity. Let h_j be real continuous periodic functions. Suppose

u_j(r exp(i theta))=F(log r) h_j(theta-psi(log r)), u_j(0)=0,

are subharmonic on the punctured plane (hence, by boundedness above near 0, on the whole plane). Then I(r,median(u_1,u_2,u_3))>=0 at every radius.

Proof. F'' must be positive somewhere. Otherwise F is positive and concave on R. If F'(t)>0 at one point, concavity forces F to become negative far enough to the left; thus F'<=0 everywhere. But monotone decrease from left limit 0 would then give F<=0, again a contradiction.

Choose t_0 with F''(t_0)>0. In logarithmic polar coordinates the subharmonicity condition, after dividing by F(t)>0, is

(1+psi'(t)^2) h_j''
- (2 F'(t) psi'(t)/F(t)+psi''(t)) h_j'
+ F''(t) h_j/F(t) >=0.

For continuous h_j, justify the selected-radius inequality by positive angular mollification. Average each planar u_j over rotations against a smooth nonnegative circular approximate identity eta_epsilon. Rotations and positive averaging preserve subharmonicity. The resulting profile h_{j,epsilon}=h_j*eta_epsilon is smooth in angle, and F and psi are C^2, so the averaged planar function is C^2 away from zero. Its nonnegative pointwise Laplacian gives the displayed angular inequality for every t and every angle, with h_j replaced by h_{j,epsilon}. At t=t_0 the angular lemma applies with A>0 and C>0 and the same coefficients for all three indices. The profiles converge uniformly to h_j; the median is 1-Lipschitz for the maximum norm, so their median integrals converge. Thus integral median(h_1,h_2,h_3)>=0. Positive scaling by F(t) and angular translation by psi(t) preserve the conclusion at every radius. This argument requires no restriction of an arbitrary distribution to a fixed-radius slice.

## Scope boundary

The theorem requires a common scalar amplitude and common rotation of fixed angular profiles. It does not cover changing angular shapes as the radius changes, different amplitudes or drifts for different functions, or general log-periodic H_j(t,theta). Such genuinely two-variable dependence remains outside these arguments.
