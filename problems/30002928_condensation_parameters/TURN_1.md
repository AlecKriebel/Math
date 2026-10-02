# Turn1: a half-line energy identity and a strict parameter bound for reflected unimodal bumps

AI-assisted mathematical proof candidate; independent review pending. Original unresolved1/5. Work with the source-supported reflected/even continuation and the decreasing-kernel subclass spelled out below. No existence or full uniqueness theorem is claimed.

## 1. Hypotheses and scalar branch

Let beta>1. Put A(t)=atanh(t)/beta and H(t)=A(t)−t. Let m_beta>0 solve H(m_beta)=0 and m*=sqrt(1−1/beta). Suppose J is an even C1 probability density, supported in[−1,1], positive on(−1,1) and nonincreasing on[0,infinity). This includes the smooth radial-decreasing kernels in the cited critical-droplet construction.

Let q be a nonconstant even C1 solution on R of q=tanh(beta(J*q+h)), with h>0, values in(−1,1), nonincreasing on[0,infinity), q(0)=u in(m*,m_beta), and limit m in(−m_beta,−m*) at both infinities. The half-line profile is its restriction to x<=0. Monotonicity makes q' integrable, and its values lie between m and u.

Passing to infinity in the convolution by dominated convergence gives h=H(m). On the negative metastable interval H'(m)=1/[beta(1−m²)]−1>0. Thus h and m already determine each other uniquely on this branch; the unresolved issue is their selection by u, not an independent two-parameter freedom.

## 2. Exact nonlocal boundary identity

Set D=u−m>0, p=q−m and P(r)=p(r) for r>=0. Then P(0)=D, P tends to0 and P is nonincreasing. The fixed-point equation subtracts its limit to give

A(m+p(x))−A(m)=(J*p)(x).

Multiply by p'(x) and integrate over x<0. The left side is integral_m^u [A(t)−A(m)] dt, using the chain rule. To evaluate the right side, split the convolution into y<0 and y>0. Symmetrizing the first part in x,y and integrating the sum of derivatives yields

integral_{x<0,y<0} J(x−y)p'(x)p(y) dxdy = (D/2)(J*p)(0).

For the cross part use evenness, x=−r,y=s, and symmetrize in r,s:

−integral_{r,s>0} J(r+s)P'(r)P(s) drds
= (D/2)(J*p)(0)+integral_{r,s>0} J'(r+s)P(r)P(s) drds.

Both identities can first be integrated on bounded intervals and then passed to the limit. Compact support of J, boundedness of P, its zero limit and integrability of P' justify all boundary terms and dominated passages. Since (J*p)(0)=A(u)−A(m), subtraction gives the exact identity

I(m,u):=integral_m^u (t−m)A'(t) dt
= integral_{r,s>0} [−J'(r+s)]P(r)P(s) drds.                 (1)

The RHS depends on the entire profile. Replacing it by a function of endpoints alone would be unjustified for a general source kernel.

## 3. A sharper upper bound and strictness

Write K(r,s)=−J'(r+s)>=0. Since integral_0^infinity K(r,s) ds=J(r), and0<=P<=D,

I(m,u)<=D integral_0^infinity J(r)P(r) dr
= (D/2)[A(u)−A(m)].                                      (2)

This inequality is strict for the stated nonconstant solution. First P(r)>0 for every finite r: if p vanishes somewhere, the subtracted fixed-point equation and kernel positivity imply it vanishes on a neighborhood; propagation and continuity then force p identically0, contradicting D>0. Second the peak equation gives (J*p)(0)=A(u)−A(m)<D because H(u)<0<h=H(m). Thus P(s)<D on a set of positive J(s)ds measure. For such s, integral_0^infinity K(r,s)P(r)dr>0, since integral K(r,s)dr=J(s)>0 and P(r)>0. Hence the difference between the RHS of(2) and(1), namely integral K(r,s)P(r)[D−P(s)]drds, is strictly positive.

Equivalently,

integral_m^u A(t)dt > (u−m)[A(u)+A(m)]/2.                 (3)

## 4. Consequence: peak below the magnitude of the negative phase

The sign of the trapezoidal error in(3) is determined exactly by the midpoint of[m,u]. Indeed integration by parts twice gives

integral_m^u A(t)dt −(u−m)[A(u)+A(m)]/2
= −(1/2)integral_m^u (t−m)(u−t)A''(t)dt.

Here A''(t)=2t/[beta(1−t²)²] is odd and strictly increasing. The weight is symmetric about c=(m+u)/2. Pairing equal distances about c shows that the last integral has the same sign as c, and is zero precisely at c=0: for c>0, A''(c+s)+A''(c−s)>0, with the inequalities reversed for c<0. Consequently the strict positive error in(3) forces

m+u<0, or u<−m.

Since H is strictly increasing on the negative metastable interval,

−m_beta < m < −u,
0<h=H(m)<H(−u)=u−atanh(u)/beta.                          (4)

This is a kernel-independent strict selection bound within the reflected unimodal/decreasing-kernel class. It reduces the allowed field interval at every prescribed u and forces h->0 when u approaches m_beta from below. It does not prove that the allowed interval contains a solution or only one solution.

## 5. Scope, credit and controls

The source's positive field/negative phase restrictions are essential in the strictness argument and are restored from the printed contribution. Reflection, kernel monotonicity and unimodality are explicit assumptions; we do not claim that every profile under the OWR shorthand has been proved to satisfy them. Classical mean-field and nonlocal energy methods are credited to the cited papers. The exact boundary identity is derived here without importing a local ODE first integral.

The checker uses exact symbolic integrations on polynomial test profiles/kernels to verify(1)'s convolution integration-by-parts identity independently of the fixed-point equation, and rational checks of the trapezoidal-error sign mechanism. Test profiles are not represented as actual solutions. No floating-point profile scan or finite sample is used to prove(4).
