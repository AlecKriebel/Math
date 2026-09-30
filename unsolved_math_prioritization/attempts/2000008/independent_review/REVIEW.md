# Independent review: elastic equilibrium multiplier criterion

**Verdict: PASS_RESTRICTED_UNIQUENESS_WITH_PHYSICAL_SCOPE_HOLD.** No mandatory correction was found. The common-constant-minor-multiplier proposition is valid under its stated regularity, convex-domain and full-boundary assumptions. Ball's general physical Problem8 remains **unsolved in this package, 2/5 approaches**.

Frozen artifact: PARTIAL_RESULT.md, SHA-256 `9d0f1e9ee9a0238bb2b9965facd8dcf8d398b0b5baf9509298ce9b597f9ce5fa`.

Reviewer: separate GPT-6 Astra agent, reasoning effort xhigh. This is an adversarial AI review, not human peer review. No historical-priority claim or complete audit of the cited nonuniqueness construction is made. The author's mathematical file was not edited.

## 1. Exact original problem and the nonuniqueness-source distinction

I checked Section2.1 and the exact Problem8 statement on printed p.17 of [Ball, Some Open Problems in Elasticity](https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf). The surrounding model is equidimensional nonlinear elasticity, initially in three dimensions, with homogeneous stored energy, positive Jacobian, frame indifference and determinant-collapse blow-up. Pure displacement means the entire boundary trace is prescribed. The question concerns sufficiently smooth equilibria, not just global minimizers. On printed p.7, Ball explicitly describes strict polyconvexity by strict convexity of the representing function g of the minors.

The preceding uniqueness discussion separates mixed/traction boundary conditions, annular or toroidal domains and discontinuous cavitating maps. None is an automatic example for the ball-like, pure-displacement, sufficiently smooth target. The artifact preserves these distinctions.

I also read and visually checked printed p.10 of [Ball, Progress and puzzles in nonlinear elasticity](https://people.maths.ox.ac.uk/~ball/Papers/Ball%20Udine%202009.pdf). Ball expressly distinguishes Spadaro's planar-domain-to-three-dimensional-target examples with injective boundary from the equidimensional injective-boundary cases n=2 or3. This is decisive evidence against silently importing a membrane example into the stated physical model.

The Spadaro preprint text was independently checked through the [retrieved text mirror](https://paperzz.com/doc/8462194/15-2007---institut-f%C3%BCr-mathematik), especially Theorem1 and the immediately following injective-boundary variant. The first maps the planar disk to the plane with noninjective boundary; the second maps the planar disk to three-dimensional space. [Institutional publication metadata](https://iris.uniroma1.it/handle/11573/1117524) confirms the2009 Archive for Rational Mechanics and Analysis article,193(3),659–678, DOI10.1007/s00205-008-0156-y. Its abstract uses a broader statement of Ball's question; the detailed dimensions and Ball's later warning control the scope here.

The full final journal PDF was not independently compared with the mirror, and the minimal-surface regularity and multiplicity proofs were not recertified. The package does not need them as a proof dependency for its restricted proposition. It correctly refrains from claiming a present-day complete resolution of the original physical problem.

## 2. Null-Lagrangian identity, including the boundary requirement

Let u be C2 up to the boundary and let phi have zero full trace. For a two-by-two minor

M(Du)=u_(i,alpha)u_(j,beta)−u_(i,beta)u_(j,alpha),

its first variation is the sum of the four divergence terms

partial_alpha(phi_i u_(j,beta))−partial_beta(phi_i u_(j,alpha))
+partial_beta(u_(i,alpha) phi_j)−partial_alpha(u_(i,beta) phi_j).

The extra second-derivative terms cancel by equality of mixed derivatives. Every boundary flux contains phi, so its integral vanishes when the entire boundary trace is zero. Each cofactor entry is a signed minor of this form. The determinant identity follows from div(cof Du)=0 and the same integration-by-parts argument.

Consequently the first variation of the integral of Q:cof Du+p det Du is zero for constant Q,p, exactly as used in the artifact. This is a polynomial identity for all gradients. It does not require the whole segment u+t phi to remain orientation preserving, or to correspond to valid arguments of g. Nor does it require Dy=Dz on the boundary: equality of the maps' full traces suffices.

The full-boundary assumption is indispensable for this argument as written. Prescribing only part of the boundary would leave an uncontrolled flux; the proposition does not make that substitution.

## 3. Testing equilibria and strict positivity

The stated C2 regularity on the closure, bounded smooth domain, and C1 representing function on an open set containing the compact minor images make both stresses bounded. Thus y−z is a legitimate zero-trace test. If weak equilibrium is initially defined only against compactly supported smooth tests, use density in H1_0: y−z belongs to that space, and the bounded stresses define continuous linear functionals on it. No unstated stress integrability estimate for a rough minimizer is being assumed.

At each point, put U=(F,cof F,det F) and V=(G,cof G,det G). Since g is differentiable and strictly convex on a convex open domain, the two strict supporting-hyperplane inequalities give

(Dg(U)−Dg(V))·(U−V)>0 whenever U differs from V.

The convexity domain is important: it contains the full straight segment in the enlarged minor variables. That segment need not be the minors of a matrix interpolation, and no such assertion is required.

Under the same constant values g_C=Q and g_d=p for both deformations, the last two components of the gradient difference vanish. The remaining positive pairing is precisely (g_F(U)−g_F(V)):(F−G). Separately applying the null-Lagrangian identity to each equilibrium leaves its integral equal to zero. It is pointwise nonnegative and strictly positive wherever F differs from G. Continuity then forces F=G everywhere. Connectedness and the common full trace give y=z.

This proves the proposition for its actual hypotheses. It requires strict convexity, not a quantitative uniform convexity modulus. The domain need not be ball-like for this restricted result, but that observation does not remove the multiplier restriction or solve the broader problem.

## 4. Adversarial controls against dropping the extra assumption

Spatially variable multipliers are not harmless. On the unit cube, take u equal to the identity and phi=(b,0,0), where b=x(1−x)y(1−y)z(1−z). The determinant multiplier p(x,y,z)=x gives

integral p cof(Du):Dphi = −1/216,

rather than zero. A variable cofactor multiplier gives an analogous control. Constant-multiplier null-Lagrangian cancellation therefore cannot simply be reused pointwise for variable coefficients.

There is also an explicit algebraic control against promoting strict polyconvexity to global monotonicity of DW. On d>0 let

g(F,C,d)=(||F||²+||C||²+(d−10)²)/2+1/d.

It is strictly convex in all its variables, since its d-second derivative is1+2/d³>0. The induced W is frame indifferent and has the determinant-collapse barrier. At I and R=diag(−1,−1,1), both of determinant one, direct differentiation gives DW(I)=−7I and DW(R)=−7R. Hence

(DW(R)−DW(I)):(R−I)=−56.

These affine deformations have different boundary traces; this is expressly not a counterexample to Ball's question or to the submitted proposition. It only falsifies the tempting global-stress-monotonicity shortcut and supports the artifact's explanation of its gap.

## 5. Reproduction and independent checks

All75 submitted symbolic assertions passed on replay in an isolated directory. The newly generated verification.json is byte-identical to the submitted receipt. The tests concern algebraic identities, not existence or uniqueness of arbitrary PDE solutions.

The independent checker passes **188 exact assertions**. It constructs cofactors through the Levi-Civita formula, verifies the full cofactor and determinant polarization identities, and checks the divergence and integrated first variation of each of the nine cofactor entries and the determinant on four independent polynomial maps. It also verifies the nonzero variable-multiplier controls and the strictly polyconvex negative stress pairing above.

The checker uses SymPy. Its replay dependencies are included in the publication list; the rendered primary-source pages are excluded. The continuous strict-convexity and test-function arguments are verified analytically here rather than inferred from these finite tests.

## 6. Recommendation

Publish the restricted proposition and source-separation record with **unsolved2/5** for the original target. Keep the common constant matrix/scalar hypothesis prominent. Preserve the distinction between physical equidimensional injective-boundary elasticity and the credited planar membrane/noninjective examples. Do not label this a general uniqueness theorem, a nonuniqueness construction, or an independently audited resolution of Spadaro's complete analytic argument.

No mandatory correction remains.
