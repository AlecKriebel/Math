# Independent audit of denominator, bounds, and exact diagnostics

## Decision

The four propositions in the first-pass theory report are accepted under their stated assumptions. The exact harmonic sector integrals and the quantitative Fejer sharpness witness have been independently reconstructed. No theorem-level correction is required. The unrestricted conjecture remains unresolved.

Primary source credit: A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. Its harmonic and homogeneous affirmative cases are prior credited results. The propositions below are an audit of the authored first-pass calculations and deductions, with no claim of historical novelty.

Use the unnormalized angular integral I(r)=integral_0^{2 pi} median(u_1,u_2,u_3)(r exp(i theta)) dtheta and B(r)=max_{j,theta}u_j(r exp(i theta)).

## 1. Zero denominators and integrability

The classification is correct. At every radius B is finite and nonnegative. Submean at 0 makes each circle integral finite and nonnegative: local upper bounds control its positive part and the submean inequality rules out an infinite negative part. Thus all three circle values are finite almost everywhere, and the median is integrable by a lower bound from their sum and its upper bound B.

If B(r)=0, all three functions are at most 0 on the circle, hence at most 0 inside. Their common value 0 at the center and the strong maximum principle force each to vanish throughout the open disk. Upper semicontinuity and the boundary upper bound force vanishing on the closed disk too. Conversely that vanishing plainly gives B(r)=0.

Maximum comparison and harmonic comparison with an affine function of log|z| show, respectively, that B is nondecreasing and B(exp(t)) is finite convex. Thus B is continuous for r>0. Upper semicontinuity at 0 gives B(r)->0 as r decreases to 0. Unless all functions vanish everywhere, its positive set is exactly (R_0,infinity) for a finite R_0>=0.

The convention is indispensable: restricting the supremum to B>0 and treating the globally zero triple separately is precise. Assigning the numerical value 0 to all 0/0 radii is a different, weaker extension for nontrivial triples vanishing on a disk. The report correctly does not claim equivalence. The epsilon formulation must retain the condition B(r)>0. Nor can the supremum assertion be replaced by existence of a radius with I(r)>=0.

## 2. Universal bound and exact sharpness

For finite a<=b<=c<=B, a+b+c<=2b+B. Integrating gives

I(r)>=1/2 sum_j I(r,u_j)-pi B(r)>=-pi B(r).

The upper bound I(r)<=2 pi B(r) is immediate. The upper endpoint is attained by three copies of |z|^2. The lower endpoint is an optimal infimum over the admissible triples at a fixed radius, not an asserted attained minimum.

### Independent reconstruction of the Fejer witness

Divide the circle into three equal arcs. Let g_j be 1 on its assigned arc and -1/2 elsewhere. Each has zero mean, their sum is zero, and their median is -1/2 almost everywhere. For N>=1, n=N+1, convolve with the nonnegative normalized Fejer kernel

F_N(t)=(1/n)(sin(nt/2)/sin(t/2))^2.

A direct cosine-coefficient calculation gives exactly

f_{j,N}(theta)=sum_{k=1}^N (1-k/n) [3 sin(k pi/3)/(pi k)] cos(k(theta-2 pi j/3)).

Replacing cos(k(theta-2 pi j/3)) by Re(exp(-2 pi i j k/3)z^k) gives the claimed entire harmonic polynomial U_{j,N}, with U_{j,N}(0)=0. Positive convolution gives -1/2<=f_{j,N}<=1. Its nonzero first Fourier coefficient excludes the zero function, and a nonzero zero-mean continuous function has a positive maximum. Thus 0<B_N<=1.

The total variation estimate is exact: shifting the assigned arc by |t|<=2 pi/3 changes a set of length 2|t|, which multiplied by its jump 3/2 gives 3|t|. For larger |t|<=pi the symmetric-difference length is at most 4 pi/3, still bounded after multiplication by 3|t|. Hence ||g_j(. -t)-g_j||_1<=3|t|.

The two kernel bounds F_N<=n and F_N<=pi^2/(nt^2) give, splitting at pi/n,

integral_{-pi}^{pi}|t|F_N(t)dt
 <= 2 integral_0^{pi/n} nt dt + 2 integral_{pi/n}^{pi} pi^2/(nt)dt
 = pi^2(1+2 log n)/n.

After the normalized convolution and summing the three L1 errors to bound the median error,

|I(1,median U_{j,N})+pi|<=9 pi(1+2 log n)/(2n).

Therefore I_N->-pi. For sufficiently large N, I_N<0; since 0<B_N<=1, I_N/B_N<=I_N. The universal lower bound then forces I_N/B_N->-pi.

The finite certificate also checks exactly. The first ten terms of exp(10) sum to 5719087/567>10000, so log 10000<10. At N=9999 the relative error is strictly below 189/20000<1/100, proving I_N/B_N<-(99/100)pi. This is an exact one-radius sharpness witness and not a counterexample to a supremum over radii.

## 3. The report's actual root-of-unity harmonic diagnostic

This audit verifies the stated triple, rather than replacing it with another example:

omega=exp(2 pi i/3),
u_j(z)=Re(omega^j z+omega^(2j)z^2), j=0,1,2.

On a circle let f_r(s)=rs+r^2(2s^2-1). The three arguments are cos(theta+2 pi j/3). Permutation under a 2 pi/3 shift and reflection symmetry reduce the integral to six times that on 0<=theta<=pi/3. There set

x=cos theta, y=cos(theta-2 pi/3), z=cos(theta+2 pi/3).

Then x>=y>=z, x+y+z=0, and the difference identity

f_r(p)-f_r(q)=r(p-q)(1-2r w)

holds when p+q+w=0. In particular f_r(x)>=f_r(y) throughout. With c=1/(2r), there are exactly the following order changes:

- If r<=1/2, x<=c and y<=c, so the median is f_r(y).
- If 1/2<=r<=1, y<=c while x crosses c at alpha=arccos c. The median is f_r(z) before alpha and f_r(y) after alpha.
- If r>=1, x>=c while y crosses c at beta=2 pi/3-arccos c. The median is f_r(z) before beta and f_r(x) after beta.

No additional crossover can change the median, because the displayed comparisons already account for all three pairwise orderings. Ties agree continuously.

The primitive of r cos(theta+d)+r^2 cos(2theta+2d) is

A_d(theta)=r sin(theta+d)+(r^2/2)sin(2theta+2d).

Independent endpoint evaluation, using cos alpha=c, sin alpha=sqrt(1-c^2) and the elementary addition formulas at beta=2 pi/3-alpha, yields

I(r)=-3 sqrt(3) r^2,                         0<r<=1/2;
I(r)=3 sqrt(3)(r^2-2r+1/2),                 1/2<=r<=1;
I(r)=-3 sqrt(3)/2,                          r>=1.

Both junctions agree. The middle factor decreases from -1/4 to -1/2, so all values are strictly negative. Every u_j is bounded above on the circle by r+r^2, and u_0(r)=r+r^2, hence B(r)=r+r^2 exactly. The normalized ratio tends to 0 at both ends of the radius interval. Its supremum is therefore exactly 0 and is not attained. This is not a counterexample to either normalized conjecture.

The independent calculation evaluates primitive endpoints directly and does not rely on numerical angular integration.

## 4. Finite-jet corollary

The proof is valid for a common leading homogeneous degree m>=1 with uniform remainders u_j(z)=P_j(z)+o(|z|^m), where some P_j may vanish but at least one does not. Positive rescaling gives locally uniform limits P_j; these are subharmonic. Their degree-m angular profiles obey h_j''+m^2h_j>=0, and the source's credited half-period median argument gives nonnegative leading median integral.

The leading maximum C=max_{j,|z|=1}P_j(z) is positive by the maximum principle. Uniform expansions and the maximum-norm Lipschitz property of the median yield the limit I(r)/B(r)=I(1,median P_j)/C>=0 as r decreases to 0. Thus a hypothetical counterexample smooth near 0 would need every component to be flat there. This necessary condition neither solves nor excludes all-flat triples.

## 5. Separate independent clamp control

The following is an additional audit control, not the triple in Section 3 and not a replacement for its calculations:

w_1(z)=Re z, w_2(z)=-Re z, w_3(z)=-Re z^2.

Here B(r)=max(r,r^2). At c=|cos theta|, the median is r times the clipping of r(1-2c^2) to [-c,c]. Let

a=(sqrt(1+8r^2)-1)/(4r),
b=(sqrt(1+8r^2)+1)/(4r).

Then a is the positive crossing r(1-2a^2)=a, b is the crossing r(1-2b^2)=-b, ab=1/2, and b>=1 exactly when r<=1. Integrating with c as variable gives the separate exact formulas

I_w(r)=4r[1-(1+ra)sqrt(1-a^2)],                         0<r<=1;
I_w(r)=4r[1-(1+ra)sqrt(1-a^2)+(rb-1)sqrt(1-b^2)],       r>=1.

For the sign, a simpler proof avoids manipulating radicals. Pair theta and pi/2-theta for 0<=theta<=pi/4, and put Q=r^2 cos(2theta)>=0. Their two median values sum to

min(Q,r sin theta)-min(Q,r cos theta)<=0.

At theta=0 this is strictly negative for every r>0, and it remains so on an interval. Reflection symmetry therefore gives I_w(r)<0 at every radius. Since all three functions are harmonic, the normalized small-radius limit is 0; explicitly the first formula has I_w(r)=-2r^3+O(r^5). Also I_w(r)/r tends to 4(1-sqrt(2)) at infinity by dominated convergence, and B(r)=r^2 there, so the large-radius ratio tends to 0 as well. This independently confirms that strictly negative integrals at every radius do not refute the normalized supremum target.

## Audit outcome

No fatal gap was found in the theory propositions or construction exclusions. The accompanying construction acceptance provides a fully explicit angular-mollification proof for the only potentially delicate distributional slicing step. The exact independent calculation checks supplement the analytic proofs; they do not certify the unresolved general statement. The public [finite certificate](../certificates/first_pass_exact.json) records the principal identities and constants.
