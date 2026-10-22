# Fourth-pass extension: arbitrary fixed harmonic profiles at flat honest records

## Scope and conclusion

This is a separately stated extension of Theorem 3 in REPORT.md, within the same fourth shared substantive pass. It makes no new claim about the unrestricted conjecture, and no priority or remote-publication claim. All cutoffs, source repairs, and tails below are part of the construction, rather than presumed negligible.

### Theorem

Let h_0,h_1,h_2 be real harmonic polynomials on the plane, with h_j(0)=0 and at least one nonzero. Define

C_0=max_(j,theta) h_j(exp(i theta))>0,

J_0=integral_0^(2 pi) med(h_0,h_1,h_2)(exp(i theta)) dtheta.

There exist C-infinity whole-plane subharmonic functions u_j, all flat at zero, positive-denominator radii exp(t_k) tending to zero, integers n_k tending to infinity, and a fixed q>0, such that

b(s)<=b(t_k) exp[q n_k(s-t_k)] for every s<=t_k,

I(exp t_k)/b(t_k) -> J_0/C_0.

More precisely,

U_j(t_k+x/n_k,y/n_k)/b(t_k) -> h_j(exp(x+i y))/C_0

in C-infinity on every compact subset of R^2. At intervening gaps all three constructed functions agree with a strictly positive radial function, so the quotient equals 2 pi. Consequently the actual-denominator supremum and small-radius limsup of the constructed triple are 2 pi. This theorem cannot produce a uniformly negative counterexample.

### Sharpness consequence

The accepted first-pass Fejer harmonic-polynomial construction has J_0/C_0 arbitrarily close to -pi. Applying this theorem to any one fixed triple from that construction shows: for every epsilon>0 there is a smooth all-flat triple and infinitely many honest records with slopes tending to infinity whose quotient tends to a number below -pi+epsilon. Therefore the universal lower bound -pi remains sharp even when the tested circles must be honest records of smooth all-flat triples.

This is a sharpness statement over the class, not a claim that a single constructed triple has limit -pi, nor a negative supremum. The earlier finite-degree construction supplies each chosen input; no new source approximation is presumed.

## 1. A strictly positive record slope for every fixed harmonic input

Write

H_j(x,y)=h_j(exp(x+i y))
 =sum_(m=m_0)^d exp(mx)[A_(jm) cos(my)+B_(jm) sin(my)],

where m_0>=1 is the first nonzero degree of the joint collection and d is its largest degree. Let

b_H(x)=max_(j,y) H_j(x,y).

This function is positive, continuous, convex, and strictly increasing. Positivity follows from the zero angular means and the existence of a nonzero component. Convexity in log radius follows from harmonic comparison on annuli. For strict increase, equality of the maxima on two different circles would give a nonconstant harmonic component attaining its larger-disk maximum at an interior point, which is impossible; that component cannot be constant because the common positive maximum differs from its value zero at the origin.

The finite leading expansion gives

b_H(x)=exp(m_0 x)[c+O(exp x)] as x->-infinity,

where c=max_j sqrt(A_(j,m_0)^2+B_(j,m_0)^2)>0. In particular,

b_H(x-1)/b_H(x) -> exp(-m_0).

It follows that the following constants are strictly positive:

eta_0=inf_(x<=0)[1-b_H(x-1)/b_H(x)]>0,

c_*=inf_(x<=0) exp(-m_0 x)b_H(x)>0.

Indeed each displayed function is continuous, is positive everywhere on this half-line, and has a strictly positive limit at negative infinity. Its infimum is therefore the lesser of positive lower bounds on a sufficiently negative tail and a compact interval. Also eta_0<1.

Set q=eta_0/4, so 0<q<1/4. Convexity gives at every x<=0 the left derivative bound

b_(H,-)'(x)>=b_H(x)-b_H(x-1)>=eta_0 b_H(x)=4q b_H(x).                 (1)

No differentiability of the angular maximizing point, or of b_H everywhere, is assumed. The left derivative of a finite convex function and the indicated secant comparison suffice. In particular (1) holds for its ordinary derivative almost everywhere.

This step supplies a fixed positive honest-record slope even when the harmonic polynomial has cancellations and its maximum is not the sum of its coefficients.

## 2. A positive repair of every annular transition

Use the fixed smooth eta,zeta of REPORT.md: eta rises from zero to one on [0,1], and zeta is one on [0,1], between zero and one everywhere, and supported in [-1,2]. Let

S=sum_(m=m_0)^d max_j sqrt(A_(jm)^2+B_(jm)^2)>0,

C=S(||eta''||_infinity+2d||eta'||_infinity)>0,

K_0=3C exp(2m_0), K=S+6C exp(2d).

For L>=3 define

chi_L(x)=eta(x+L)eta(L-x),

R_L(x)=C[exp(m_0 x)zeta(x+L)+exp(d x)zeta(L-x)],

F_L(x)=integral_(-infinity)^x (x-s)R_L(s) ds.

On the inner cutoff transition, every mode exp(mx) is at most exp(m_0 x); on the outer one it is at most exp(d x). Also the x derivative introduces at most the factor d. Thus

(partial_x^2+partial_y^2)(chi_L H_j+F_L)
 =chi_L''H_j+2chi_L' partial_x H_j+R_L>=0.                         (2)

The correction is nonnegative, nondecreasing, convex, zero before -L-1, and affine after L+1. For x<=0,

F_L(x)<=C exp(m_0 x)/m_0^2,

F_L(0)<=K_0(L+1)exp(-m_0 L).                                      (3)

For every x>=-L-1 an all-x upper envelope is

F_L(x)+chi_L(x) b_H(x)
 <=K exp(dL)[1+x+L+1].                                            (4)

The left side is zero for x<-L-1. For (4), the total mass of R_L is at most 6C exp(dL+2d), and the angular maximum on the support of chi is at most S exp(dL). The baseline bound (3) follows by integrating the inner source exactly as in the explicit two-mode construction. These estimates also bound the absolute angular term, which is useful for convergence and flatness.

## 3. Fully specified scales and inner-tail bound

Put A=C/m_0^2+S and K_q=(2+3/q)K. Choose an integer N satisfying

N>=max(400,256(d+1)^2),

A exp[-(m_0-q)sqrt(N)/2] <= C_0/4,

K_q exp(-N/4) <= C_0/4,

K_0(sqrt(N)+1)exp(-m_0 sqrt(N))+K_q exp(-N/4)
 <=c_* exp[-m_0 sqrt(N)/2].                                       (5)

These conditions have a solution. After division by the right sides, each exponential-polynomial expression decreases for n>=N: in the last expression use sqrt(n)>m_0 and m_0(sqrt(n)+1)>2. Therefore they hold with N replaced by every larger n.

Set n_k=N 2^k, L_k=sqrt(n_k), t_k=-log n_k, a_k=exp(-n_k), and x_k(t)=n_k(t-t_k). Define

U_j(t,theta)=sum_(k>=0)a_k[F_(L_k)(x_k(t))
                         +chi_(L_k)(x_k(t))H_j(x_k(t),n_k theta)].                (6)

The curvature and angular-support intervals J_k=[t_k-(L_k+1)/n_k,t_k+(L_k+1)/n_k] are disjoint, by the same 4/sqrt(N)<log 2 estimate. Thus no outer packet indexed below k contributes at any t<=t_k.

Fix k and M=q n_k. For an inner packet l=k+p, p>=1, (4) and sup_(v>=0)(1+n_l v)exp(-Mv)<=1+n_l/M give, after division by a_k, a weighted envelope bound with prefactor K(1+2^p/q) and exponential exponent

E=-n_k(2^p-1)+q n_k p log 2+d sqrt(n_k 2^p)
                         +q(sqrt(n_k 2^p)+1)/2^p.

Since q<1/4<1/2, the first two terms are at most -n_k 2^p/4, using 2^p-1-p log(2)/2>=2^(p-2). Write z=n_k 2^p. The other terms are at most (d+1/8)sqrt(z)+1/8. The lower bound on N in (5) makes this at most z/8. Thus E<=-z/8.

For 0<Q<=1/4,

sum_(p>=1)(1+2^p/q) Q^(2^p)
 <=Q^2[1/(1-Q^2)+(2/q)/(1-2Q^2)]
 <=(2+3/q)Q^2.

Taking Q=exp(-n_k/8), the sum of all inner packet upper envelopes therefore satisfies for every real t

exp[-M(t-t_k)] sum_(l>k) upper_envelope_l(t) <=a_k T_k,

T_k=K_q exp(-n_k/4).                                               (7)

This controls all earlier packet transitions and all completed tails, not merely their center values. No truncation of the infinite past is made.

## 4. Honest records and actual normalization

For x=n_k(t-t_k)<=-L_k/2, (3) and the coefficient bounds give

exp(-q x) times the kth upper envelope /a_k
 <=A exp[(m_0-q)x]
 <=A exp[-(m_0-q)L_k/2] <=C_0/4.

Adding (7), the weighted actual maximum is at most a_k C_0/2. At the center, the actual maximum is at least a_k C_0. Thus no point in this earlier region exceeds the center in the weighted record comparison.

On the remaining core -L_k/2<=x<=0, the angular cutoff is one, every inner angular packet is absent, and the total radial baseline divided by a_k, denoted D_k(x), is nonnegative, nondecreasing and affine. Its endpoint bound is

D_k(0)<=K_0(L_k+1)exp(-m_0L_k)+T_k
 <=c_* exp(-m_0L_k/2) <=b_H(x).                                    (8)

The actual joint maximum is exactly

b(t)/a_k=b_H(x)+D_k(x).                                             (9)

This equality requires no common maximizing angle for the polynomial modes: all three components receive the same scalar baseline, so taking their joint maximum gives precisely (9).

By (1), at almost every core x,

(d/dx)[b(t)/a_k]-q b(t)/a_k
 >=3q b_H(x)+D_k'(x)-q D_k(x)
 >=2q b_H(x)>0.

A finite convex b_H is locally Lipschitz; D_k is affine. Thus the weighted maximum is absolutely continuous on compact subintervals, and its almost-everywhere nonnegative derivative proves monotonicity on the whole core. Together with the earlier-region bound this proves

b(s)<=b(t_k)exp[q n_k(s-t_k)] for every s<=t_k.                       (10)

Write delta_k=D_k(0). Equations (5),(7),(8) give delta_k->0. Integer angular frequency and the common baseline then give exactly

b(t_k)=a_k(C_0+delta_k),

I(exp t_k)=a_k(J_0+2 pi delta_k).                                    (11)

Therefore the actual normalized ratio tends to J_0/C_0 as claimed.

## 5. Smoothness, all-radii behavior and the limiting profiles

Equation (2) gives positivity of every packet's cylindrical Laplacian. Uniform convergence on compact t intervals and all-order smooth flatness follow as in REPORT.md, now with fixed exp(d sqrt(n_k)) in place of exp(2 sqrt(n_k)). For completeness, any fixed-order packet derivative introduces only powers of n_k, with constants depending on the fixed polynomial and fixed cutoff derivatives. Since

exp(-n_k+d sqrt(n_k)) <= exp(-n_k/2)

for all sufficiently large k, the active packet and the dyadic sum of completed tails are bounded, after conversion to Cartesian derivatives, by C_alpha exp(-c_alpha/r) r^(-p_alpha). Completed tails are affine in log r, higher cylindrical derivatives are locally supported, and no outer packet contributes sufficiently far inward. This proves the C-infinity extension by zero at the origin, all-order flatness, and whole-plane subharmonicity.

Every component has strictly positive angular mean at every r>0, from infinitely many completed inner radial corrections. Hence B(r)>0 throughout. At all gaps between consecutive support intervals, the components equal that same positive radial mean, giving quotient 2 pi exactly. All transition radii remain subharmonic by (2). Beyond the outermost interval all components again equal a common radial affine function of log r. There is no uncontrolled future extension.

On each fixed rescaled compact set, the kth angular cutoff eventually equals one. Its own baseline is affine with coefficients tending to zero after division by a_k, by (3), and all inner radial tails have the same property by (7) evaluated at fixed interval endpoints. All other angular packets vanish. Equation (11) therefore yields C-infinity local convergence to H_j/C_0. This completes the theorem and the sharpness transfer.
