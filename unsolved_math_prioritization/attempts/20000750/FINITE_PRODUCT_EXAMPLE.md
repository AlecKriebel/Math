# Exact arithmetic illustration, not an asymptotic improvement

Take R=8, H={0,2}, X={10,...,49}, and D={1,2,3,5,6,7}, all squarefree d<8. Choose a smooth cutoff Q with Q(log(8/d))=1 on D and Q(0)=0, possible by finite polynomial interpolation. The baseline is u_d=mu(d), with explicit support d<8. Let q(n)=1_prime(n)+1_prime(n+2).

The baseline denominator is 35, numerator 15, and ratio 3/7. Choose a smooth h on [0,1] with h(log(2)/log(8))=1 and h(log(p)/log(8))=0 for p=3,5,7. Such a polynomial exists. Then f_epsilon=exp(epsilon h) is a genuine smooth prime-local family and its coefficient tangent is v_d=u_d 1_(2|d). Its exact Rayleigh derivative at epsilon=0 is −24/245.

At epsilon=−log(2), the coefficients are u−v/2. Direct enumeration gives denominator 65/2, numerator 15, ratio 6/13>3/7. Equivalently the integer vector 2u−v has denominator 130 and numerator 60. This is a genuine finite arithmetic example inside the exact product-local family, not merely the abstract 3x3 Hessian example.

It illustrates the test, not progress on a prime-gap bound: R=8 is fixed, only forty integers are checked, and Q was allowed finite interpolation. No uniform asymptotic gain is established. Fixed-R successful finite tests do not resolve the historical question.
