# Independent pre-exposure physical identities

2026-10-16 18:55 UTC (before package exposure; theorem remains unproved). Review completion estimate: 5%.

For an original vertex P=(x,y), focus F=(f,0), and D(P)=|P-F|^2, unit inversion is J_F(P)=F+(P-F)/D(P). Translation invariance of the closed shoelace sum gives exactly

2 A_F = sum_j det(P_j-F,P_{j+1}-F)/(D(P_j)D(P_{j+1}))
      = sum_j [x_j y_{j+1}-y_j x_{j+1}+f(y_j-y_{j+1})]/(D_j D_{j+1}).

The second term does NOT telescope after the denominators appear. Replacing it by zero is invalid in general. This identity holds for arbitrary indexed closed polygonal lists, including self-intersections and repetitions.

On x=a cos t, y=b sin t, f^2=a^2-b^2, direct expansion yields

D_+(t) = (a-f cos t)^2,
D_-(t) = (a+f cos t)^2.

Since a>|f| in the required domain, both denominators are strictly positive at every physical real vertex. Therefore no physical focal collision occurs. Complex poles require separate handling and cannot be dismissed using this positivity.

Reversing the list negates each area; repeating a primitive list r times adds identical edge summands r times, so A_F(repeated)=r A_F and A_+ A_-(repeated)=r^2(A_+ A_-). These identities alone cover all positive integer repetitions once a primitive ordered cycle is proved. They impose no convexity assumption and avoid absolute-area substitutions.

A useful rational parametrization is u=exp(it), alpha=(a+b)/2, beta=(a-b)/2, q=sqrt(beta/alpha)=f/(a+b), with f>0 and 0<q<1. Then

z(u)=alpha u+beta/u,
conj(z)(u)=beta u+alpha/u,
z(u)-f=alpha(u-q)^2/u,
conj(z)(u)-f=beta(u-q^-1)^2/u.

Thus the translated inverted complex coordinate is w_+(u)=u/[beta(u-q^-1)^2], while its real-circle conjugate is wbar_+(u)=u/[alpha(u-q)^2]. The opposite focus replaces q by -q in these factorizations. Signed area is (1/(4i)) sum_j [wbar(u_j)w(u_{j+1})-w(u_j)wbar(u_{j+1})]. The poles have order two before the closure trace; a proof must handle any cancellations and coinciding shifted poles explicitly.

No phase-constancy or positivity has been established here. The outstanding central task is a closure-aware identity for the two rational area traces along the billiard correspondence, valid for all admitted odd stars.
