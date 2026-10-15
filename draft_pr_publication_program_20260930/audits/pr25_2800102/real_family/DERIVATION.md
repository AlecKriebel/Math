# Checkable reconstruction of the real square proof

This is independent validation of existing external claims, not a new research discovery. Statements below use ordinary mathematical proof standards, including the elementary Gamma/Beta identities, Laguerre orthogonality and generating function, and the standard transfer theorem for an analytic function in a Delta-domain. Numerical outputs are controls on identities, not substitutes for their quantified derivations.

## 1. Deriving the LOE density from the joint law, including both parities

Fix real lambda>=0. Put omega=(lambda+1)/2,

- w(x)=x^(omega-1) exp(-x/2), p_j(x)=L_j^(lambda)(x), phi_j=w p_j;
- h_j=Gamma(j+lambda+1)/j!;
- psi_j(x)=integral_0^infinity sign(y-x) phi_j(y) dy;
- B_ij=integral phi_i(x) psi_j(x) dx;
- v_j=integral phi_j(x) dx.

Here h_j is the LUE norm for x w(x)^2=x^lambda exp(-x). This h is different from the shifted norm called h in Hutnik Section2.3. All these integrals are finite; x w(x) vanishes at zero and infinity. Define the polynomial operator

D f=x f'+(omega-x/2)f.

The elementary Laguerre derivative and multiplication identities give

D p_j=((j+1)p_(j+1)-(j+lambda)p_(j-1))/2,

with the negative-index term zero. Since w Dp_j=(x phi_j)', integration by parts gives

integral sign(y-x) (y phi_j(y))' dy=-2x phi_j(x),

and therefore

B D=-2 diag(h_j)

in the following explicit sense: ((j+1)B_(i,j+1)-(j+lambda)B_(i,j-1))/2=-2h_j delta_ij, for every i,j>=0. This relation and antisymmetry determine the needed entries. In particular,

B_(2k,2l)=B_(2k+1,2l+1)=0,

B_(2k,2l+1)=0 when l<k,

B_(2k,2l+1)=-4h_(2k)/(2k+1) product_(a=k+1)^l (2a+lambda)/(2a+1) when l>=k.

To check these expressions without assuming the result, start at j=0 in the displayed relation: B_(i,1)=-4h_0 delta_i0. Recursing in even j determines all odd columns. Recursing in odd j and using antisymmetry gives zero for same-parity entries. The nonzero product starts exactly when j=2k reaches the Kronecker delta. This proves the formulas by induction.

The integral of phi_j follows by integrating the Laguerre generating function for |z|<1:

sum_j v_j z^j=2^omega Gamma(omega)(1-z^2)^(-omega).

Consequently v_(2k)=2^omega Gamma(k+omega)/k!, v_(2k+1)=0.

The determinant of the p_j times product w is a nonzero constant times the ordered LOE joint law. Expanding the determinant and integrating over ordered pairs gives the de Bruijn identity: its ordered integral is Pf(B_N) for even N; for odd N it is Pf(M_N), where M_N=[[B_N,v],[-v^T,0]]. This identity follows directly by the Pfaffian pairing expansion; all integrals are absolutely convergent. Its multiplicative constant cancels on normalization. It is used here as an algebraic identity of these explicit finite matrices, not an assumed LOE density formula.

Write D_N for the truncated coefficient matrix of D in p_0,...,p_(N-1), H_N=diag(h_0,...,h_(N-1)). For even N, B_(i,N)=0 whenever i<N, by the entry formula. Hence B_N D_N=-2H_N and

B_N^(-1)=-D_N H_N^(-1)/2.

For odd N=2m+1, the last column of B_N vanishes, and the entry product gives

B_(i,N)=-4h_(N-1) v_i/[N v_(N-1)],  i<N.

It follows by direct multiplication that

M_N^(-1)=[[-D_N H_N^(-1)/2, -e_(N-1)/v_(N-1)],
           [e_(N-1)^T/v_(N-1), 0]].

Indeed the top-left product is the identity after canceling the rank-one boundary term, v^T D_N=0, B_N e_(N-1)=0, and the bottom-right product is one. These assertions are explicit consequences of the two entry formulas above.

Perturb w to w(1+t f), differentiate log Pf(M) using d log Pf(M)=Tr(M^(-1)dM)/2, and use antisymmetry. The unnormalized one-point density (integral N) is

R_even(x)=-phi(x)^T B_N^(-1) psi(x),

R_odd(x)=-phi(x)^T[-D_N H_N^(-1)/2] psi(x)+phi_(N-1)(x)/v_(N-1).

This differentiation initially uses bounded f; exponential integrability extends it to f=sqrt(x). Signs are fixed by psi'_j=-2phi_j. Telescoping the Laguerre recurrence gives, in both parities,

R_N(x)=R_C,N(x)+N phi_(N-1)(x) psi_N(x)/(4h_(N-1))
       +epsilon_N phi_(N-1)(x)/v_(N-1),

where R_C,N=x w^2 sum_(j=0)^(N-1) p_j^2/h_j, and epsilon_N=N mod2. For example, the sum of adjacent pairs

sum_(j=0)^(N-2) (j+1)[phi_(j+1)psi_j-phi_j psi_(j+1)]/(4h_j)

is both the sparse-matrix density and R_C,N+N phi_(N-1)psi_N/(4h_(N-1)). No missing odd-N border is permitted.

Finally, the same psi recurrence is

psi_(j+1)=(j+lambda)psi_(j-1)/(j+1)-4x phi_j/(j+1),

and psi_0=2^omega[2Gamma(omega,x/2)-Gamma(omega)]. Thus

psi_(2m)=((omega)_m/m!)psi_0-4x sum_(k=0)^(m-1) a_k phi_(2k+1),

a_k=Gamma(m+omega)Gamma(k+1)/[2Gamma(k+1+omega)Gamma(m+1)],

psi_(2m+1)=-4x sum_(k=0)^m a_k phi_(2k),

a_k=Gamma(m+1+lambda/2)Gamma(k+1/2)/[2Gamma(k+1+lambda/2)Gamma(m+3/2)].

Let g_N=Gamma((N+1)/2)/Gamma((N+lambda)/2). The Gamma duplication formula gives N a_k/h_(N-1)=g_N w_(k,epsilon)/2, with exactly Hutnik's weights

w_(k,epsilon)=2^(1-lambda) Gamma(k+1-epsilon/2)/Gamma(k+(lambda+3)/2-epsilon/2).

For even N the psi_0 term gives g_N p_(N-1)Phi_2/2; for odd N the border term gives precisely that same expression with Phi_2=2^(1-omega)w. The remaining finite terms are -g_N p_(N-1)Phi_1/2. Dividing R_N by N proves Proposition2.2 for all N>=1 and lambda>=0, independently of simply accepting the printed Livan--Vivo identity. At N1 it reduces to the Gamma density of x with shape omega and scale2.

Livan--Vivo Eq16 now provides a separately checked primary-source cross-check. Their raw eigenvalue weight is exp(-x/2) for both beta values, with rho_beta(x)=R_beta(x/2)/(2N). Their R_2 itself has standard complex weight exp(-x). This explains the factors of two and why real variance one does not acquire an extra sqrt2.

## 2. Abel completion, signs, and convergence

The finite Phi_1 uses Laguerre indices 2m+1-epsilon. Represent w_m by the Beta integral and substitute t=z^2. The parity generating function yields, for 0<zeta<1,

S_(zeta,epsilon)(x)=2^(1-lambda)/Gamma(omega) integral_0^1
 (1-z^2)^(omega-1)[L_lambda(zeta z,x)+(-1)^(epsilon+1)L_lambda(-zeta z,x)] dz,

where L_lambda(a,x)=(1-a)^(-lambda-1)exp[-x a/(1-a)]. The substitutions y=(1+z)/(1-z) and y=(1-z)/(1+z) at zeta=1 give

S_(1,epsilon)=2^(1-omega) x^(-omega)e^(x/2)
 [Gamma(omega,x/2)+(-1)^(epsilon+1)gamma(omega,x/2)]/Gamma(omega).

Multiplying by x^lambda e^-x gives exactly Phi_2, including the odd-N sign. For fixed x>0, the positive branch near z1 has superexponential decay. The negative branch is bounded by a constant times (1-z^2)^(omega-1). Since omega>=1/2, these majorants are integrable. The fixed-x positive branch is uniformly bounded in zeta because t^(-lambda-1)exp(-x/t) is bounded for 0<t<=1.

For the half-moment insertion expand the fixed p_(N-1) into monomials x^j. Integrating the absolute value of either generating-function branch against x^(lambda+j+1/2)e^-x gives

Gamma(lambda+j+3/2)(1 plus or minus zeta z)^(j+1/2),

bounded uniformly by a constant. The remaining Beta factor is integrable. Hence Fubini and dominated convergence are valid. For zeta<1, coefficient bounds on any generating-function circle of radius a with zeta<a<1 produce an integrable exponential majorant; this separately justifies exchanging the series and x integral.

The finite parity sum cancels the initial segment through m=(N+epsilon-2)/2. Its uncanceled tail starts at (N+epsilon)/2 and has index N-1+2u, u>=1, in either parity. This establishes the stated diagonal completion before invoking positivity.

For the connection kernel use sigma_0=1, sigma_j=-b_j for j>=1, with sum sigma_j z^j=sqrt(1-z). Orthogonality after the parameter shift lambda->lambda+1/2 gives

Q_lambda(r,s)=sum_(j=0)^min(r,s) sigma_(r-j)sigma_(s-j) hhat_j,

hhat_j=Gamma(j+lambda+3/2)/j!. Here b_j>0 and b_j=O(j^(-3/2)). The absolutely convergent Fourier series of |1-e^(it)| gives

b_d-sum_(t>=1)b_t b_(t+d)=1/[pi(d^2-1/4)]=kappa_d.

The positive Beta representation b_n=pi^(-1)integral_0^1 x^(n-3/2)(1-x)^(1/2)dx and Tonelli give

sum_(t>=1)t b_t b_(t+d)=1/[pi(2d+1)].

Thus -Q(r,r+d)=hhat_r(kappa_d+E_(r,d)), with

E_(r,d)=sum_(t=1)^r [1-hhat_(r-t)/hhat_r]b_t b_(t+d)+sum_(t>r)b_t b_(t+d)>=0.

The ratio hhat_(r-t)/hhat_r=product_(j=0)^(t-1)(r-j)/(r+lambda+1/2-j) increases in r. Extending it by zero for t>r proves E decreases in r, including r0. Fixed r and s->infinity gives Q(r,s)=O(s^(-3/2)). The weight is O(m^(-omega)); consequently the tail is absolutely convergent with exponent omega+3/2>=2. All positivity and adjacent-dimension decompositions therefore concern ordinary convergent sums, not only Abel values.

## 3. Supporting AP upper decrement bound reconstructed

The complex law has standard variance-one entries and LUE weight exp(-x). Define Y_n=E Tr((XX*)^(1/2)), Y0=0. Direct connection with L_j^(1/2) gives the positive convolution for u_j=integral sqrt(x)e^-x L_j(x)^2 dx/sqrt(pi):

u_j=sum_(k=0)^j sigma_(j-k)^2 Gamma(k+3/2)/(sqrt(pi) k!).

Hence, for |z|<1,

H(z)=sum_(n>=1)Y_n z^n=sqrt(pi)/2 z(1-z)^(-5/2)F(z),

F(z)=2F1(-1/2,-1/2;1;z).

This avoids a fractional-moment Carlson-continuation premise for the square half moment. The hypergeometric power series solves z(1-z)F''+F'-F/4=0. With D=z d/dz, direct differentiation gives

[z^(-1)(D-1)^2-2D^2+z(D+1)^2-3/4]H
 =sqrt(pi)/2 z(1-z)^(-3/2)[z(1-z)F''+F'-F/4]=0.

Coefficient extraction gives n^2(Y_(n+1)-2Y_n+Y_(n-1))=3Y_n/4 for every n>=1. H has no constant term and Y1=sqrt(pi)/2, so no fictitious negative-index term is needed.

The convergent logarithmic hypergeometric expansion at z1 is

F(1-t)=4/pi-t/pi-t^2/(4pi) sum_(k>=0) (3/2)_k^2/[k!(k+2)!] t^k
 [log t-psi(k+1)-psi(k+3)+2psi(k+3/2)].

It is valid 0<|t|<1, |arg t|<pi. In particular the t^2 coefficients are (8log2-5)/(16pi) and -1/(8pi) for the analytic and log parts. These signs agree with AP Eq3.7. F is analytic off [1,infinity), so after multiplying by z(1-z)^(-5/2), subtraction of any finite singular sum leaves an analytic Delta-domain remainder of order t^(J-3/2)(1+|log t|). The standard coefficient transfer theorem bounds that remainder by O(n^(-J+1/2)log n). This is an applicable analytic theorem, not a conclusion inferred from a few coefficients.

Extracting the j0,1,2 terms by [z^n](1-z)^a=Gamma(n-a)/[Gamma(-a)Gamma(n+1)] and differentiating in a reproduces

alpha_C(n)=8/(3pi)+[log n+gamma+6log2-17/6]/(16pi n^2)+O(log n/n^4).

The missing odd powers are justified by the moment recurrence: at index j the coefficient multiplier is j(j-2), and it couples only j,j-2,j-4,...; index1 vanishes, then every odd index vanishes by induction. Since the analytic expansion exists to arbitrary finite order with a controlled remainder, this coefficient comparison is legitimate. Therefore

Delta_n=alpha_C(n)-alpha_C(n+1)
 =[log n+gamma+6log2-10/3]/(8pi n^3)+O(log n/n^4).

Write q_(d-1)=2d^(3/2)sum_(j>=2)binom(3/2,2j)d^(-2j), and E_n=8pi[n(n+1)]^(3/2)Delta_n-log n. The recurrence gives exactly

E_d-E_(d-1)=8pi q_(d-1)Y_d-log[d/(d-1)].

Every coefficient of q is positive. AP's auxiliary bound alpha_C(d)<8(d+1/2)/(3pi d) follows from the positive convolution, bounding (3/2)_(k-m)/(k-m)! by (3/2)_k/k!, extending the sum to F(1)=4/pi, then the strict Gamma log-convexity inequality Gamma(d+1/2)<sqrt(d)Gamma(d). All denominators are positive.

The needed q upper estimate is

q_(d-1)<3 log[d/(d-1)]/[64 sqrt(d)(d+1/2)],  d>=2.

AP Lemma6 is printed for q_j with j>=2, while the proof uses q1 as well. This is a local indexing omission, not an unsupported additional premise: its actual power-series proof holds for every 0<t<1 and therefore includes q1 at t=1/2. Specifically,

64[(1+t)^(3/2)+(1-t)^(3/2)-2-3t^2/4]/(3t^4)
 =sum_(j>=0)lambda_j t^(2j),

lambda0=1, lambda1=7/24, lambda2=33/256, and lambda_j<1/[3(j+1)] for j>=3 by the explicit coefficient ratio. The coefficients a_m of -log(1-t)/[t(1+t/2)] satisfy a0=1, a2=1/3>lambda1, a4=19/120>lambda2, a_(2j)>1/[3(j+1)], and a_(2j+1)>=0. The latter follows from

sum_(k=0)^j 4^(-k)[1/(2j+2-2k)-1/(2(2j+1-2k))]>=0.

Every bracket is nonnegative. Both series converge for 0<t<1, so coefficientwise comparison proves the q upper estimate, including its needed smallest index.

Combining that estimate with alpha_C upper proves E_d<E_(d-1) for every d>=2. The independently reconstructed asymptotic identifies E_n->C0=gamma+6log2-10/3. Therefore E_n>C0, Delta_n>0 and alpha_C(n)>8/(3pi) using the known limit. (Also C0>0 because log2>2/3 and gamma>0.) Retaining the first positive q term gives q_(d-1)>3/(64d^(5/2)); hence 8pi q_(d-1)Y_d>1/d. Consequently

E_(d-1)-E_d<log[d/(d-1)]-1/d.

Summing the positive differences to infinity and using the established limit gives

E_n-C0<H_n-log n-gamma.

This is exactly the required strict universal upper bound

0<Delta_n<[H_n+6log2-10/3]/[8pi(n(n+1))^(3/2)], n>=1.

There is no circular use of that upper bound to establish its premises: the alpha_C auxiliary upper bound comes first from the positive convolution, the Delta lower sign comes from decreasing E and its limit, and only then is the stronger alpha_C lower bound used for the Delta upper bound. The 2016 withdrawn Lemma1 is not used.

## 4. Universal square comparison and small dimensions

After the verified Abel completion, Xi_N=sum_(u>=1)A_N,u K_(N-1),u. All terms converge absolutely, K>0 and K decreases with its first index. At lambda0 the coefficient is

A_N,u=sqrt(2) G(N/2) (N/2)_u/[N^(3/2)((N+1)/2)_u],

G(x)=Gamma(x+1/4)Gamma(x+3/4)/[Gamma(x)Gamma(x+1/2)].

For N>=3 every A_N,u>A_(N+1),u. A checkable way to prove this is the exact adjacent ratio in Hutnik Eq3.17. Its shape derivative Eq3.18 is nonnegative on lambda>=0, N>=3, since its first summand reduces to x^2-x-1/2>=0 at x=(N+lambda)/2>=3/2. At lambda1 the ratio telescopes to

sqrt[N/(N+1)] (2N+3)/(2N+2) (N+2u)/(N+2u+1)<1,

because N(2N+3)^2<4(N+1)^3. Monotonicity in shape implies the lambda0 ratio is <1 for EVERY u>=1. No restriction to a tested finite set of diagonals enters this assertion.

Only u1 is needed. Put q(x)=G(x)/sqrt(x). Its logarithmic derivative is

q'/q=integral_0^infinity e^(-xt)/(1+e^(-t/4)) dt-1/(2x)>0.

This follows directly from the digamma difference representation; the integrand denominator is <2 for t>0. q(3/2)=(15/16)sqrt(pi/3)>15/16, so A_N,1>15/[16(N+1)] for N>=3. Its exact adjacent ratio is

A_(N+1),1/A_N,1=(2N+1)sqrt(N+1)/[2sqrt(N)(N+2)]<1-1/(2N).

Squaring is permitted because both sides are positive. The last inequality is equivalent to 4N^3-4N^2-13N+4>0. Substituting N=t+3 gives 4t^3+32t^2+71t+37, positive for every t>=0. Since kappa2=4/(15pi),

Xi_N-Xi_(N+1)>[A_N,1-A_(N+1),1]kappa2>1/[8pi N(N+1)].

Subtract the already validated AP upper bound. For c0=6log2-10/3,

alpha_R(N+1)-alpha_R(N)>
 [sqrt(N(N+1))-H_N-c0]/[8pi(N(N+1))^(3/2)], N>=3.

The log2 bound log2<7/10 gives c0<13/15. H4+c0<59/20<3, and induction (increment1/(N+1)<3/4) gives H_N+c0<3N/4 for every N>=4. Then the preceding expression is greater than

[N/(N+1)]^(3/2)/(32pi N^2)>= (4/5)^(3/2)/(32pi N^2)>1/(160N^2),

using (4/5)^3>(7/10)^2 and pi<22/7. At N3 the exact rational bounds in Hutnik A.1 give the same reserve. They also follow from the direct-law rational interval control below.

For N1,2 independent exact joint-law integration gives

Y1=sqrt(2/pi), Y2=sqrt(pi)(2-sqrt(2)/2), Y3=3sqrt(pi)/2+2sqrt(2/pi).

Dividing Y_N by N^(3/2) produces exactly Hutnik's displayed I1 and I2. The new standard-library code performs de Bruijn differentiation in a MONOMIAL basis directly from the joint density, rather than using the proposed LOE one-point formula. Polar substitution x=s^2,y=t^2 gives exact angular and radial integrals and exact rational coordinates. It verifies agreement with a separate integration of the printed density for N1..8, both parities. Machin's alternating arctangent formula provides a rational pi enclosure; integer-square-root bounds provide rational radical enclosures. Certified interval subtraction gives alpha_R(N+1)-alpha_R(N)>1/(160N^2) for N1..7. In particular the finite N1,2,3 exceptions close without floating-point extrapolation.

Together these arguments certify the real square reserve for EVERY integer N>=1. The limit 8/(3pi) follows from the square Marchenko--Pastur law and uniform integrability: E[N^(-1)Tr(XX^T/N)]=1 bounds the large-eigenvalue contribution to the square-root statistic by 1/sqrt(M). It does not require the paper's broader rectangularity or transition results.
