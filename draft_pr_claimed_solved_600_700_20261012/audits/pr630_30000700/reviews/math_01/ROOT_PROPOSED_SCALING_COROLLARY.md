# Separately labeled routine scaling corollary proposed by the root reviewer

This is not part of the 28 frozen inputs. It is a direct scaling and
translation of their Proposition 3, independently checked here. It carries
no historical novelty claim and is optional for the audit report.

For any integer k>=3, any prescribed complex b!=0, and any z0 in C, choose
lambda satisfying

    lambda^(k-1)=-1/(2^(k-1)-2),

and put A=-2b/lambda, t=exp(lambda*(z-z0)), f=A(t-1)^2, a=0. The defining
equation ensures lambda!=0, and b!=0 ensures A!=0. Then

    f'=2A*lambda*t*(t-1),
    f'-b=2A*lambda*(t-1/2)^2,
    f^(k)=A*lambda^k*(2^k*t^2-2*t).

At every b-point of f', t=1/2, and

    f^(k)=A*lambda^k*(2^(k-2)-1)=-A*lambda/2=b.

There are infinitely many such b-points because exp maps C onto C\{0}.
The common zero set of f and f' is exactly t=1, with orders two and one;
it too is infinite. Thus f is transcendental entire, shares zero with f'
IM but not CM, and cannot be d*exp(cz), for any nonzero d,c. This verifies
the root-proposed strengthening for arbitrary prescribed b and z0.

The exact controls separately check the factorization symbolically in
arbitrary B and lambda and its value identity for k=3,...,15. The algebra
above establishes the claim for all k>=3.
