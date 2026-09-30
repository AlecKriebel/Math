# Independent review: two Gaussian MA persistence coefficient identities

**Verdict: PASS_SCOPED_ALL_ORDER_COEFFICIENT_IDENTITIES.** No mandatory mathematical correction. The original AR and MA convergence-radius questions remain unresolved in this package; retain **unsolved, 2/5 approaches**.

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent using xhigh reasoning. This is an adversarial AI review, not human peer review or a priority certification.

## 1. Frozen object and exact scope

The reviewed `PARTIAL_RESULT.md` has SHA-256
`72abb281c18796b934dc8ea8a3bb85a530730ddcc32495aea8e3ef0f1611cc4e`.
The submitted verifier has SHA-256
`8ea0a7dc1ab86eb1d040ad721cd4815c325ac90c0ba1e47211c57a1f8baddec7`,
and its receipt has SHA-256
`b14212519d471b75b212393eca352f6b0bde1af6bffab84ae4b9d5d78ce47cd9`.

The result proves the two highest inverse-pi components of every Taylor coefficient of the Gaussian MA(1) persistence base. It does not determine the full coefficient, either requested radius, or a singularity of the physical branch. The two component formulas were already conjectured by the MA paper's authors and are correctly credited.

## 2. Primary-source audit

The full [OWR report](https://ems.press/content/serial-article-files/46870), printed pp.1625–1626, was checked, including the rendered page carrying the questions. The parameter is the exponential base in the persistence probability, not its negative logarithm. The source distinguishes Gaussian AR(1) and Gaussian MA(1), asks for the AR radius, and conjectures radius one for MA. It also expresses interest in closed-form coefficients, which the partial result addresses only for two components.

The [AR paper, v2](https://arxiv.org/abs/1810.09861v2) supplies the Gaussian initial-law convention and the known radius lower bound. The [MA paper, v1](https://arxiv.org/abs/2407.06870v1) supplies the local eigenvalue/persistence correspondence, coefficient recursion, and the two conjectured patterns following Theorem 3. Its Lemma 6, equations (18)–(19), was checked in the rendered original. The relevant source identity is valid on a real interval containing positive parameters near zero; only its local analytic germ is needed here. The source's Slepian application is not used.

There is an important source inconsistency that the submitted proof handles correctly: an adjacent remark after Lemma 7 describes all kappa terms as probabilities. Equation (19) is an *oriented nested integral*, and its second term is negative for positive rho. The proof uses that equation and its actual integration limits, not the incorrect positivity description. The local eigenfunction iteration establishing equation (18) uses signed integrals and an absolute remainder bound, so it does not require the erroneous positivity assertion.

The current arXiv version histories were checked. These checks establish the cited sources and their scopes; they do not certify a globally exhaustive priority search.

## 3. Independent derivation of the signed moments

Write `s_i=(-rho)^i u_i` in the nested integral, with `s_0=u_0>0`. At the i-th stage the new limits initially run from `u_(i-1)` to zero. Combining this reversal with the differential contributes `(-1)^(i+1) rho^i`. Their product is

    (-1)^(k(k-1)/2) rho^(k(k+1)/2).

The transformed region is `0<u_k<...<u_1<u_0`. Thus the sign and power in the candidate's equation (4) follow directly, including kappa_2<0.

For a fixed vector of exponential indices `(j_1,...,j_k)`, successive integration from the innermost variable gives the denominator

    product_(l=1)^k sum_(i=l)^k (2j_i+1)

and numerator `u_0^(k+2J)`, where `J=sum j_i`. Include the exponential coefficients `(-1)^J/(2^J product j_i!)`. The final half-Gaussian integral then gives the single expression

    sigma_k (-1)^J Gamma((k+2J+1)/2)
      / [2 B(j) pi^((k+1)/2)].

For odd k, the Gamma factor is an integer factorial. For even k, the half-integer Gamma factor cancels one square root of pi and gives the displayed even-k formula. This independently reproduces equations (6)–(7), including every factor of two.

The rho degree is `d_k+2 sum i*j_i`, while the q degree is `ceil(k/2)`, with q=1/pi. Their difference is even and nonnegative. For k=2h the minimum difference is `2h^2`; for k=2h-1 it is `2h(h-1)`. Hence only k=1 contributes to difference zero, and only the next k=1 term and the first k=2 term can contribute to difference two.

## 4. Formal uniqueness and analytic justification

Every kappa term has strictly positive rho order. Therefore, at each rho degree, the equation for lambda uses only its previously determined coefficients. Its constant term is 1/2, so negative integer powers are legitimate formal series. Addition, multiplication and inversion of a series with nonzero rational constant preserve the nonnegative even difference grading. This proves the polynomial degree and parity statements without assuming the desired coefficient formulas.

The grouping by `X=q*rho` is well-defined in the completed graded algebra: a monomial `rho^n q^j` becomes `rho^(n-j) X^j`, and `n-j` is nonnegative and even. At any fixed original rho order, only finitely many terms occur. Thus extracting the zero and two diagonals is a legitimate formal operation, not an analytic substitution involving an independent unbounded q.

For the physical value q=1/pi, the claimed analytic justification is valid. Fix `r<1/sqrt(2)`. On the simplex all u_i are at most u_0. Summing absolute values of the Gaussian exponential expansions gives the dominating factor

    exp(-A*u_0^2/2),  A=(1-2r^2)/(1-r^2)>0.

After integrating its simplex volume, the k-th bound is

    r^(k(k+1)/2) / [(2pi)^((k+1)/2) k!]
      * integral_0^infinity u^k exp(-A*u^2/2) du.

The half-moment divided by k! grows at most exponentially times a reciprocal Gamma factor, whereas the initial power of r decays quadratically in k. Multiplication by lambda^(-k) therefore still gives a locally normally convergent sum when lambda stays away from zero. This establishes analyticity of the scalar equation near `(0,1/2)`. Its lambda derivative there is one after moving all terms to the left. The analytic implicit-function theorem supplies the unique germ, and the prior real-positive eigenvalue identity identifies it with the physical Taylor germ. No extension to the whole unit disk is inferred.

## 5. All-order coefficient extraction

The difference-zero equation is

    Lambda=1/2+X/(2Lambda).

The root with constant term 1/2 is `(1+sqrt(1+8X))/4`. Expanding its square root gives precisely

    a_n=(-1)^(n-1) 2^(n-1) binom(2n-2,n-1)/n.

Write the difference-two component as `rho^2 B(X)`. The only forcing terms are `-rho^2 X/6` in kappa_1 and `-rho^2 X/8` in kappa_2. Expansion of the lambda inverses gives

    B*(1+X/(2Lambda^2))=-X/(6Lambda)-X/(8Lambda^2).

Putting `s=sqrt(1+8X)` yields `B=-(s-1)(s+4)/(24s)`. Independently differentiating `A=Lambda-1/2` gives the same expression from `-(8X A'-3A)/6`. Thus the coefficient of X^m in B is `-(8m-3)a_m/6`. Taking m=n-2 gives exactly the asserted second-highest coefficient for every n>=3. The indexing, signs and first nontrivial case `-5q/6` are all consistent.

## 6. Independent finite verification

The submitted verifier reproduced **all 528 assertions** and its receipt byte for byte. It covers Taylor order 24 and the eight full coefficients printed in the MA source.

The separate `independent_checks.py` uses a materially different construction. Normalize the eigenfunction by f(0)=1 and write

    lambda*f(x)=lambda+integral_(-rho*x)^0 f(s) phi(s) ds,
    lambda=integral_0^infinity f(s) phi(s) ds.

It expands the eigenfunction as polynomials in x and the formal variable `z=(2pi)^(-1/2)`. If V_j is the rho^j coefficient of the displayed integral operator, the recursion is

    f_n=2*(sum_(j=1)^n V_j f_(n-j)
             -sum_(i=1)^(n-1) lambda_i f_(n-i)).

Gaussian half-moments then recover lambda_n; the conversion `z^2=q/2` is made at the end. This procedure does not use nested simplex coefficients or the author's inverse-power recurrence. It agrees with every full author coefficient through order 24 and checks the two formulas through order 30. Additional exact convolution controls verify the quadratic equation and difference-two equation through order 160, together with orientation, Gaussian moment and grading controls. **All 1,307 independent assertions pass.**

These finite assertions are reproducibility controls. Sections 3–5 above supply the all-order mathematical review; the computations do not prove a radius statement.

## 7. Remaining gap and publication recommendation

At fixed q=1/pi, all other graded diagonals contribute to each physical coefficient. The singularity of an extracted diagonal at X=-1/8 need not persist after their summation. Cancellation can change both coefficient asymptotics and the physical analytic continuation. Consequently the package has established neither radius one for MA nor the exact AR radius, and it has not identified a physical singularity at rho=-pi/8.

Publish as an explicitly partial result with the existing conjectures and eigenvalue machinery credited. Preserve the unresolved status, two-approach count, local analytic scope, and absence of novelty or human-peer-review claims. No mathematical revision is required for this frozen version.
