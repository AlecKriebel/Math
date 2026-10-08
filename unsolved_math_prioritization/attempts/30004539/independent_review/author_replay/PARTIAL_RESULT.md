# Two all-order coefficient identities for the Gaussian MA(1) persistence series

**30004539 / OWR-2654828-004. Status: unsolved, 2/5 approaches.** Both requested convergence-radius questions remain open in this package. The result below proves the two leading inverse-pi coefficient patterns explicitly conjectured in the cited MA paper. It does not determine a radius or establish novelty. Independent review is pending.

## 1. Source and normalization

The original question is Marvin Kettner's contribution to *Stochastic Processes under Constraints*, Oberwolfach Report 32/2020, printed pp.1625–1626. Its persistence exponent is the base lambda in p_N=lambda^(N+o(N)), **not** −log(lambda). Innovations are independent standard Gaussians. The AR model is X_n=rho X_(n−1)+xi_n; the MA model is X_n=rho xi_(n−1)+xi_n. Persistence means X_0,...,X_N are nonnegative, and the series is expanded in rho at zero, with lambda(0)=1/2. In the AR reference the initial X_0 is also standard Gaussian and independent of the innovations.

The report asks for the AR series radius and conjectures radius one for MA. Aurzada–Kettner's AR Theorem2 gives a lower bound 1/3. Aurzada–Bothe–Druet–Kettner–Profeta's MA Theorem2 reports a lower bound exceeding0.332. The latter's Section2, following Theorem3, conjectures formulas for the highest and second-highest powers of 1/pi in each coefficient. These are the restricted assertions proved here. Full radius determination would require control of the entire coefficients or of complex continuation of the distinguished eigenvalue; neither follows from two coefficient components.

## 2. Result

Write lambda(rho)=sum_(n>=0) K_n rho^n. There are rational polynomials P_n(q) with K_n=P_n(1/pi), P_0=1/2, degree P_n<=n, and only powers q^j with n−j even. For n>=1 set

    a_n = (−1)^(n−1) 2^(n−1) binom(2n−2,n−1)/n.

Then

    [q^n] P_n(q) = a_n,                                    (1)
    [q^(n−2)] P_n(q) = −a_(n−2) [8(n−3)+5]/6,  n>=3.      (2)

These match the two patterns stated in the cited paper; this package credits that prior conjecture. They concern the MA model only. No analogous AR formula is asserted.

## 3. Signed nested integrals and exact polynomial grading

We use the prior exact eigenvalue identity (MA Lemma6, equation18): near rho=0 the germ with lambda(0)=1/2 satisfies

    lambda = 1/2 + sum_(k>=1) kappa_k(rho) lambda^(−k).      (3)

For real rho>=0, the kappa_k are the nested, oriented integrals in equation19. With d_k=k(k+1)/2 and sigma_k=(−1)^(k(k−1)/2), changing the alternating-sign integration variables to positive coordinates gives

    kappa_k(rho) = sigma_k rho^d_k /(2pi)^((k+1)/2)
      integral_[0<u_k<...<u_1<u_0<infinity]
        exp(−u_0²/2) prod_(i=1)^k exp(−rho^(2i)u_i²/2)
        du_k ... du_0.                                     (4)

The orientation is essential: sigma_1=1 and sigma_2=−1. The raw signed kappa_2 must not be replaced by a positive probability. This follows directly from the integration limits, not a sign convention chosen to fit coefficients.

Expanding the k exponentials, let j_i>=0, J=sum_i j_i and W=sum_i i j_i. The associated rho degree is d_k+2W. The simplex integral of prod u_i^(2j_i), for fixed u_0, is

    u_0^(k+2J) / prod_(l=1)^k [sum_(i=l)^k (2j_i+1)].       (5)

This is proved by successively integrating u_k,u_(k−1),...,u_1. The remaining Gaussian half-moment is elementary. Put

    B(j)=prod_i j_i! * prod_(l=1)^k [sum_(i=l)^k(2j_i+1)].

For k=2h−1 its coefficient in kappa_k is

    sigma_k (−1)^J (h+J−1)! / [2 B(j)] * pi^(−h),           (6)

and for k=2h it is

    sigma_k (−1)^J [2(h+J)]! /
       [2^(2(h+J)+1) (h+J)! B(j)] * pi^(−h).               (7)

Replace pi^−1 by the indeterminate q. Equations(6)–(7) construct a series kappa_k(rho,q) with rational coefficients, each of its monomials having q-degree ceil(k/2) and rho-degree d_k+2W. For any fixed rho-degree only finitely many k and j contribute. The degree difference

    d_k+2W−ceil(k/2)

is nonnegative and even. Its minimum is0 for k=1, 2 for k=2, and at least4 for k>=3.

Equation(3) now uniquely determines a formal series in Q[q][[rho]] with constant1/2: at degree n its right side uses only the earlier lambda coefficients because every kappa_k has positive rho order. Induction shows the same nonnegative even degree-difference property for lambda and its negative integer powers. Evaluating q=1/pi recovers the physical Taylor coefficients through the prior germ identity.

For analytic justification of the termwise Gaussian expansion in a neighborhood of zero, fix r<1/sqrt(2). On the simplex, u_i<=u_0 and sum_(i>=1) r^(2i)=r²/(1−r²)<1. Thus the sum of absolute values of the exponential expansions is dominated by exp(−A u_0²/2), where A=(1−2r²)/(1−r²)>0. The simplex volume is u_0^k/k!. Consequently the absolute kappa_k bound has the factor r^d_k times a Gaussian half-moment divided by (2pi)^((k+1)/2)k!. Its sum after multiplication by lambda^−k converges locally uniformly when |lambda| is bounded below, since r^d_k decays quadratically in k. Hence (3) is analytic near (rho,lambda)=(0,1/2), and its derivative with respect to lambda at that point is1 after moving everything to the left. The analytic implicit function theorem supplies the unique germ. This argument justifies local coefficient manipulations; it does not reach the proposed unit disk.

## 4. Extracting the two diagonals

Introduce X=q rho to record the zero degree-difference part. The grading just proved permits the unique decomposition

    lambda(rho,q)=Lambda(X)+rho² B(X)+terms of difference>=4.

From (6)–(7), the only kappa terms of difference at most2 are

    kappa_1 = X/2 −rho² X/6 + terms of difference>=4,
    kappa_2 = −rho² X/8 + terms of difference>=4.

All kappa_k with k>=3 have difference at least4. The first equation in (3) therefore gives

    Lambda=1/2+X/(2Lambda),
    Lambda=(1+sqrt(1+8X))/4,                                (8)

with the square-root branch of constant term1. The binomial series of (8) gives (1).

Equating the terms of difference2 gives the linear equation

    B [1+X/(2Lambda²)] = −X/(6Lambda)−X/(8Lambda²).          (9)

Set A(X)=Lambda(X)−1/2. Using X=2Lambda²−Lambda in (9), direct algebra yields

    B(X)=−[8X A'(X)−3A(X)]/6.                              (10)

For example, one may put s=sqrt(1+8X); both sides of (10) are −(s−1)(s+4)/(24s). Since [X^m]A=a_m, equation(10) says [X^m]B=−(8m−3)a_m/6. Taking m=n−2 proves (2) for every n>=3.

## 5. What is and is not established

The proof is all-order formal algebra with a local analytic justification. The checker reconstructs the nested-integral coefficients by exact factorial moments, solves (3) recursively through order24, independently checks the inverse-power convolutions, and matches all eight full coefficients printed in the source. The finite checks supplement, rather than replace, Sections3–4.

At q=1/pi the complete coefficient P_n(1/pi) contains the other diagonals as well. They may cancel with or dominate the two terms isolated here. The singularity X=−1/8 of the extracted diagonal is therefore **not** a demonstrated singularity at rho=−pi/8 of the physical persistence series. No coefficient ratio computed from a finite truncation is used as a radius certificate. Both original convergence-radius questions remain unresolved. We have neither excluded complex eigenvalue collisions inside |rho|<1 nor proved that the physical branch is holomorphic throughout that disk.

The prior MA eigenvalue/persistence correspondence and equation(3) are credited to the cited authors. The source's separate Slepian-process application is not used. The current search found newer work with uniform or Laplace innovations; those distributions do not answer this Gaussian question. No new-discovery or human peer-review claim is made. The inherited native runtime was used unchanged, and its exact model identifier was not exposed.

### Primary references

- OWR question, pp.1625–1626: https://ems.press/content/serial-article-files/46870
- Aurzada–Kettner, AR(1), Theorem2: https://arxiv.org/abs/1810.09861v2
- Aurzada, Bothe, Druet, Kettner, Profeta, MA(1), Theorems2–3 and Lemma6: https://arxiv.org/abs/2407.06870v1
