# Independent audit: the transition parameter a=-1/2

Date: 2026-10-20 UTC.

Audited `ATTEMPT_5.md`, final SHA-256 `10718d88ca3ed5d44eff4c46235b6637dcc49c28073e1bca05c38f78f86f953d`, using the exact operator identity and bounds in the independently audited `ATTEMPT_2.md`. The final version adds only the scope qualifier "by these arguments" to the statement about the remaining intervals. Reversing that single phrase restores the originally audited SHA-256 `ae8f9b0832aea14ea6729d549782ae00d19d894f9898555e95a113332b66d424`; this scope-only amendment is accepted and leaves every proof unchanged.

## Verdict

**PASS.** The following three conclusions are rigorously established for the exact linear NW/ES-weighted quadrant-loop series:

    rho_Q(-1/2)=1/9,
    lim_{u increasing to 1/9} Q(-1/2,u)=3/2,
    lim_{u increasing to 1/9} dQ(-1/2,u)/du=+infinity.

The middle statement is a finite Abel limit, not an assertion of ordinary or absolute convergence of the signed coefficient series. No coefficient asymptotic is established.

The exact projection formula for the critical Abel value on the full lower branch is also correct. It does not prove radius equality at other parameters. I found no required mathematical correction.

## 1. Factorization, notation, and dependence on the signed-pencil proof

With C=U+V, one has C*C=2I+B. Expanding

    c t^2(C-alpha I)*(C-alpha I),  alpha=1/(ct),

gives c t^2 B-tA+(2ct^2+1/c)I. Adding eta(t)I, with eta(t)=1-1/c-2ct^2, therefore gives K(t) exactly. This checks every scalar coefficient and the sign of the cross term.

On 3/2<=c<=2, the chosen t_* is exactly the lower-branch threshold from the signed-pencil proof. At c=3/2 it gives t_*=1/3 and c t_*^2=1/6. Consequently

    K_*=(1/6)(C-2I)*(C-2I).

The dependence on Attempt 2 is legitimate: that proof supplies complex-disk holomorphy up to |t|<t_*, real positive invertibility below t_*, and equality of the finite Abel limit with the regularized critical resolvent. In particular the finite limit is not inferred from a formal endpoint substitution.

## 2. Variational formula and projection onto the range closure

For the injective nonnegative operator K_*=d T*T, the regularized resolvent identity implies

    q_* = sup_{f != 0} |<delta,f>|^2 / <f,K_*f>.

Indeed the corresponding identity with K_*+epsilon I follows by Cauchy–Schwarz in its positive inner product and evaluation at its inverse applied to delta. Taking epsilon downward to zero commutes with the supremum: the expressions are increasing in that parameter, and the limit of their supremum is the supremum over all pairs of parameter and vector. Injectivity of T ensures positive denominator for nonzero f. Restricting to finitely supported f is also valid by density and boundedness of T.

For h=Tf, the constant coefficient is exactly h_00=-alpha_* f_00 because C raises total degree. Therefore the quotient becomes

    (d alpha_*^2)^(-1) |<delta,h>|^2/||h||^2.

Taking the supremum over ran(T), then its closure M, gives ||P_M delta||^2. The constant (d alpha_*^2)^(-1) equals c. Thus both projection formulas in the attempt follow exactly, using M-perpendicular=ker(T*).

If alpha_*<2, the vector g_ij=(alpha_*/2)^(i+j) is square summable, lies in ker(C*-alpha_*I), and has nonzero inner product with delta. The kernel projection is therefore nonzero and q_*<c. The opposite strict bound is not problematic: the variational test f=delta already gives q_*>=1 because <delta,K_*delta>=1. The attempt's weaker 0<q_*<c is correct.

## 3. Absence of the critical backward-shift eigenvector

The contraction argument for ker(C*-2I) is valid also over the complex Hilbert space. If U*f+V*f=2f, the chain of norm inequalities forces both ||U*f|| and ||V*f|| to equal ||f|| and forces equality in the triangle inequality. The two vectors therefore coincide; their sum then gives U*f=V*f=f. Invariance under U* makes the coefficients constant in the first coordinate for each fixed second coordinate, which is incompatible with square summability unless f=0.

Thus ran(C-2I) is dense, not necessarily closed or equal to the whole space. Density is exactly what the projection formula needs, and it gives q_*=c=3/2. The proof does not confuse dense range with surjectivity.

## 4. Failure of the critical range equation

Assume K_*f=delta and put g=(C-2I)f. Then (C*-2I)g=6delta. The vector -3delta is a particular solution because (C*-2I)delta=-2delta. The preceding trivial-kernel result makes that solution unique. Hence (C-2I)f=-3delta.

The total-degree recurrence uniquely fixes all coefficients, giving the formal solution

    f=(3/2) sum_{n>=0} (C/2)^n delta.

This is a coefficientwise identity, not an unjustified norm-convergent Neumann series. Different n occupy disjoint total-degree subspaces. Within degree n, the binomial coefficients yield squared norm binom(2n,n). Therefore the total squared norm would be

    (9/4) sum_{n>=0} binom(2n,n)/4^n.

The elementary lower bound binom(2n,n)/4^n>=1/(2n+1) proves divergence. Hence delta is not in ran(K_*).

If the below-threshold vectors f_t=K(t)^(-1)delta had a bounded subsequence as t increases to t_*, weak compactness would supply a weak limit. Operator-norm convergence K(t) to K_* then implies K_*f=delta by testing against arbitrary fixed vectors. This contradicts the range obstruction. It excludes every bounded subsequence and proves the full limit ||f_t|| to infinity, rather than merely an unbounded limsup.

## 5. Derivative divergence detects the scalar threshold

For real t<t_*, differentiating the bounded inverse is justified by operator-norm analyticity. Self-adjointness yields

    q'(t)=<f_t,(A-2ctB)f_t>.

The operator identity

    A-2ctB=(I-ct^2B-K(t))/t

is exact. Since <f_t,K(t)f_t>=q(t) and B<=2I, it gives the stated inequality

    q'(t)>=[(1-2ct^2)/t]||f_t||^2-q(t)/t.

At c=3/2 and t increasing to 1/3, the first coefficient tends to 2>0, while q(t)/t tends to 9/2. The norm term diverges. Thus q'(t) tends to positive infinity, with no use of coefficient positivity or monotonicity of the power series.

The chain rule q'(t)=2t Q_u(-1/2,t^2) transfers the divergence to the half-length variable. A holomorphic extension across u=1/9 would have a locally bounded derivative, so this is a genuine scalar singularity. The previously proved disk holomorphy supplies the opposite radius bound. Hence the exact radius is 1/9.

Unlike a Weyl sequence escaping to infinity, this argument directly detects the corner matrix element through its inverse-applied vector. It closes the precise gap left by the bulk noninvertibility result.

## 6. Additional comparison and scope checks

For 1<c<3/2, expansion of the stated critical form gives

    d[(alpha_*-2)(4I-A)+(C-2I)*(C-2I)]
      =d[(4alpha_*-2)I-alpha_*A+B].

The critical first-branch equation 1-4t_*+2ct_*^2=0 identifies the constant coefficient as one, while d alpha_*=t_*. Thus this comparison identity is correct. The bound

    (C-2I)*(C-2I)<=2(4I-A)

is equivalent to C*C<=4I and follows from ||C||<=2. The resulting two-sided form comparison is valid, but does not justify comparison of higher inverse powers. The attempt correctly refrains from that inference.

For alpha_*<2, ker(C*-alpha_*I) is nontrivial, so the unique-solution step used at alpha_*=2 fails. The transition proof therefore cannot simply be transferred to the rest of the lower branch. The known finite first derivative at a=-1 is consistent with this warning.

The arguments establish the transition parameter and the nonnegative range from the separate nonnegative proof; they leave the two open intervals (-1,-1/2) and (-1/2,0) unsettled by these arguments. This audit makes no independent claim about whether later literature has already resolved any part of those intervals.

No required correction was identified. 
