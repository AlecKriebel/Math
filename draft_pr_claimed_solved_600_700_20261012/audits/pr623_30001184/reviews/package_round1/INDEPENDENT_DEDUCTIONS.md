# Independent mathematical deductions

This reviewer treated all claims as hypotheses. The analytic arguments here were checked directly against the paper and primary sources, independently of earlier PASS labels. Exact computations are recorded separately and supplement these arguments.

## Exact success criterion

For the source's general unital C*-dilation category, exhibit an exactly forward-generated algebra with a point-norm continuous injective E0-semigroup, conditional expectation, genuine Markov compression, and non-invariance of the **fixed expectation's left GNS representation kernel**. The strengthened paper claim additionally requires a nonzero positive witness for each real s>0, globally positive in A. A counterexample only to a vector-null space, a discrete-time compression, an enlarged unrelated ambient algebra, or a different dilation category would fail this criterion.

## Construction, all-real continuity and exact generation

The order compactification X is compact metrizable. Translation fixes both endpoints and is jointly continuous: when t is bounded, a sufficiently far right or left tail stays in any prescribed tail neighborhood. The continuous function V=R(g) has endpoint limits. Thus (t,x) -> V(x)*V(x+t) f(x+t) V(x+t)*V(x) is continuous on each compact time interval times X. Uniform continuity there proves point-norm continuity for every fixed f, without imposing norm continuity of the automorphism maps themselves. The telescoping cocycle identity proves the full group law.

The actual dilation algebra is A=C*(alpha_r(D):r>=0). A is forward invariant because alpha_t shifts r to r+t; the ambient algebra is only a construction device. Consequently theta is an injective unital endomorphism semigroup and the claimed forward-generation equality holds exactly. Countably many rational translates and a finite basis of D generate A, by point-norm continuity, establishing separability. The map p=Delta ev_0 is UCP, p i=id, and its D-bimodule property proves that i p is a conditional expectation.

The compression on a constant diagonal b has coefficients cos^2 g(t)=(1+exp(-t))/2 and sin^2 g(t)=(1-exp(-t))/2. The orthogonal idempotents J and K give P_s P_t=J+exp(-(s+t))K. This verifies a genuine UCP norm-continuous Markov semigroup for every real nonnegative time; finite samples are unnecessary.

## Full GNS kernel and every-positive-time witnesses

Evaluation at zero of q and theta_log(2)(q) produces nonzero off-diagonal matrix units, so ev_0(A)=M2. The algebraic GNS map a tensor b -> a(0)b preserves the D-valued inner product. Its finite-dimensional range is all M2, whose column norm inner product is definite. Therefore the specified GNS correspondence is precisely E=M2, xi=I, pi(f)=left multiplication by f(0). Its kernel is exactly ev_0(f)=0. The two independent columns identify Ba(E)=M2 direct-sum M2, with pi(A) the diagonal copy. This reasoning avoids conflating a vector-state null space with the representation kernel.

For s>0 put r=exp(-s) and a_s=q theta_s(q) q-(1+r)q/2. It belongs to A and evaluates to zero at x=0. At x=s it equals d_s q, with

    d_s = (1-r^2)(sqrt(1+r^2)-r)/2
        = (1-r^2)/(2(sqrt(1+r^2)+r)) > 0.

The angle identity follows by multiplying cosines and positive sines of 2g(s) and 2g(2s): the radical product is (1-r^2)sqrt(1+r^2), since 0<r<1. Thus theta_s(a_s)(0)=d_s theta_s(q)(0) is nonzero at each positive time. For x>0 the derivative g'(x)=1/(2 sqrt(exp(2x)-1)) is decreasing and integrable at zero. The increment over [x,x+s] is at most the increment over [0,s]. For x<=0, the increment is zero or g(x+s)<=g(s); the endpoint increments are zero. Hence 0<=g(x+s)-g(x)<=g(s), and cos^2 monotonicity proves a_s>=0 globally. There is no hidden differentiability requirement at the cusp. The nonzero evaluation at x=s also proves a_s is nonzero.

At s=0 the witness vanishes, as required. As s decreases to zero, d_s tends to zero and d_s/(1-exp(-s)) tends to sqrt(2)-1. As s increases without bound, d_s tends to 1/2. No failure is asserted at zero. The boundary x=-s, x=0, x=positive infinity and x=negative infinity are covered by the same formula or the separately established endpoint values.

Even an arbitrary set map intertwining pi and theta at positive s would need to assign both pi(0) and pi(a_s) the same image but also the distinct images 0 and pi(theta_s(a_s)). Thus the proposed descent fails before extension to Ba(E). The example is not strong because p(a_s)=0 but p theta_s(a_s) is nonzero, and it cannot be weak/corner with its unital i: the corner projection would be 1, forcing i p=id_A. Neither faithfulness, a normal W*-version, nor failure for a different dilation is obtained.

## Finite-image proposition and prior-result implication

If ker pi is invariant at every time, beta_t(pi(a))=pi(theta_t(a)) is a well-defined unital *-endomorphism semigroup on C=pi(A). Lifting a basis of finite-dimensional C proves operator-norm continuity. Choose h>0 with S=integral_0^h beta_u du invertible, since S/h tends to I. Then beta_t S=integral_t^(t+h) beta_u du, so beta_t is right differentiable at zero. Its generator delta is a *-derivation by differentiating multiplicativity and adjoints. The map pbar(c)=<xi,c xi> factors p through C and is UCP; j=pi i is faithful because pbar j=id. The original expectation bimodule identity descends to pbar. Therefore L=pbar delta j satisfies the Leibniz and star identities on B. This is a proved deduction, not an imported finite-Hamiltonian theorem.

BFH's explicit amplitude-damping path has G(x)=sgn(x) arccos(exp(-abs(x)/2)) and U(x)=exp(-i G(x) Hflip), with two finite endpoint limits. Its Step 2 equation (11) produces the translated-unitary clock action. Taking the observable Heisenberg orientation gives the cocycle u_t(x)=U(x) U(x+t)*. At zero this is U(t)*, giving the BFH compression with the finite pure bath. After endpoint compactification and restriction to the exactly forward-generated observable algebra, all the continuity, expectation and generation properties needed above remain valid. Evaluation at zero followed by finite bath compression makes the GNS image a quotient of a finite-dimensional evaluation image; one need not equate the bath-vector null space with the representation kernel.

For the decaying system-level projection q, BFH's compression gives T_t(q)=exp(-t)q and hence L(q)=-q. The finite-image proposition would force a derivation, but q L(q) q=-q whereas a derivation always has q delta(q) q=0. Thus the earlier explicit model yields the negative generation-only result as a short corollary. Generic strong Hilbert-space continuity on C_b(R) would not establish the needed point-norm continuity; the finite endpoint limits of the concrete path close that gap. The package's corollary framing is therefore necessary and mathematically justified. It is not evidence that BFH explicitly stated the fixed-GNS consequence or that the new positive-witness refinement has first priority.

## Primary-source fit and limits

OWR printed pp.497–498 require p:A->B, i p a conditional expectation, and p theta_t i=T_t. Its pp.542–543 offer generation by B and its time translates and ask for a proof or counterexample; the reversed p arrow in the problem prose is a typographical reversal, resolved by the definition and both diagrams. Restricting to an E0-semigroup is permitted. A negative answer to this concrete generation-only proposal does not classify every good stronger minimality condition or settle the source's future-algebra question.

DMB Appendix B supplies the initial finite-Hamiltonian first-derivative antecedent. Vom Ende Theorem 1 proves the related bounded-total-Hamiltonian obstruction. Neither is misrepresented as a fixed-GNS-kernel theorem. Shalit–Skeide Appendix B(i) distinguishes the general, strong and weak categories, and Skeide–Sumesh Section 5 asks the related fixed-action extension question. The paper's references and exclusions accurately reflect these primary texts.

No mathematical gap or counterexample was found for the precise current theorem and proposition. Publication priority remains bounded evidence, not an exhaustiveness certificate. The contribution under review is the explicitly credited formulation-specific corollary, small matrix realization and global positive witnesses; no new general mechanism is verified or claimed.
