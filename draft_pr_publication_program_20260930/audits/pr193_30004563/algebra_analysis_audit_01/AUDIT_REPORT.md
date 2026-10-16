# Independent adversarial algebra and analysis audit of PR193 / 30004563

Audit target: original submission HEAD `b9a399eeac816dbb8f0e50e81b498c26e5acef81`.

Result: **the asserted existence of an admissible alpha=16 cube configuration with at least five distinct outgoing centers survives this independent algebra/analysis audit.** No mathematical gap was found in the claim under the crossing-allowed realization hypotheses. A new exact verifier independently reconstructs the data, without executing or importing original code or loading an author certificate. It also replaces the enormous final numerical sign test with a short concavity argument at a smaller endpoint.

Completion toward this assigned algebra/analysis audit: 100%. This is neither a priority assessment nor a claim of the actual maximal number of centers, and it does not establish anything about proper embeddings.

## Independence and evidence

`INDEPENDENT_PLAN.md` was sealed before reading submission proof or results. `FIRST_PRINCIPLES.md` records the cube-equation reduction derived from the primary definition. After that reduction I read only the original `CANDIDATE.md` and `certify_five_centers.py`. I did not read any original `review/` file or any other independent audit. The original source was inspected as evidence but never executed.

The independent `independent_check.py` uses exact `Fraction` arithmetic and obtains eighth-root intervals by binary search on integer eighth powers on a decimal grid. This differs from the author's iterated integer-square-root mechanism and dyadic precision. It bisects the algebraic boundary roots independently, computes all geometry afresh, and supplies independent endpoint intervals. Its replay passes 17,463 internal assertions. `independent_certificate.json` gives full rational enclosures; `replay_stdout.txt` gives compact output. Pass/fail decisions use no floating-point arithmetic.

The relevant primary setting is arbitrary alpha-realizations with six distinct boundary points and noncollinear alternating triples; the article explicitly allows crossed quadrilaterals. The proposed upper bound is stated in [Remark 4.8, printed p.811](https://ems.press/content/serial-article-files/39488), and the earlier maximum-three conjecture appears in [OWR35/2020, printed p.1785](https://ems.press/content/serial-article-files/46871?nt=1). The definitions and full cube notation also appear in [arXiv:2003.08941v2](https://arxiv.org/pdf/2003.08941v2). No primary PDF was copied into this audit package.

## 1. Exact equations and absence of extraneous solutions

Write N(P,Q)=|P-Q|^16. The proposed common-focus system has

A=(0,0), B=(b,0), C=(c,d),

b=2073/10000, c=4719/10000, d=64/10000, lambda=27/1250,

N(X,B)-N(X,A)=lambda, N(X,C)-N(X,A)=1.                         (1)

Because b*d=2073*64/10^8>0, the three foci are distinct and noncollinear.

For s>=0, set u=s^(1/8), v=(s+lambda)^(1/8), w=(s+1)^(1/8), always the nonnegative real roots. Squared-distance subtraction gives

2b*x=b^2+u-v,

2c*x+2d*y=c^2+d^2+u-w.                                       (2)

The determinant 4bd is strictly positive. Define x,y by (2), and G(s)=x^2+y^2-u. Then:

* If G(s)=0, (2) gives |X-A|^2=u, |X-B|^2=v, |X-C|^2=w. Eighth powers give (1).
* If X satisfies (1), s=N(X,A)>=0. Taking unique nonnegative eighth roots recovers those three squared distances; their differences force (2), and hence G(s)=0.

There is no elimination by squaring, denominator clearing at a possibly zero denominator, branch switch, or raising a negative quantity to an even power in this equivalence. Different s values give different points because s=N(X,A). In particular five disjoint s intervals give five distinct X even without uniqueness inside an interval.

G is continuous on [0,infinity): its three principal roots are continuous, and every denominator in (2) is a fixed nonzero rational. Differentiability at s=0 is unnecessary; all sign intervals used lie strictly above zero.

## 2. Independent outgoing signs and fifth-root mechanism

The following strict coarse intervals were reconstructed using independent decimal-grid root bounds. Every displayed terminating decimal means an exact rational.

| s | exact enclosure of G(s) |
|---|---|
| 9/10000 | (0.38,0.39) |
| 11/10000 | (-0.28,-0.27) |
| 13/10000 | (0.51,0.52) |
| 1/2 | (-0.91,-0.90) |
| 1 | (9,10) |
| 10^16 | (-4.766,-4.765), by the independent analytic argument below |

The first five enclosures alone give four sign-changing intervals; the final negative sign gives a fifth. Continuity and strict endpoint signs give a zero in each of

(9/10000,11/10000), (11/10000,13/10000), (13/10000,1/2),

(1/2,1), (1,10^16).

For the final endpoint put s=10^16, so u=100 exactly. Concavity of t^(1/8) on t>0 gives, for a>0,

0 < (s+a)^(1/8)-s^(1/8) <= a/(8s^(7/8)).

Let delta_v=v-u and delta_w=w-u. Then

0<delta_v<=lambda/(8*10^14), 0<delta_w<=1/(8*10^14).

The exact limiting circumcenter is

x0=b/2=2073/20000,
y0=(c^2+d^2-bc)/(2d)=1249057/128000,

x0^2+y0^2=39007985196121/409600000000 < 95.235.

Equations (2) imply the exact rational boxes

x0-lambda/(16*b*10^14) <= x <= x0,

y0-1/(16*d*10^14) <= y <= y0+(c/b)*lambda/(16*d*10^14).

Squaring these positive-coordinate boxes gives -4.766<G(10^16)<-4.765; the verifier proves the stronger upper requirement G(10^16)<-4.7. Thus the fifth root is not a subtraction-cancellation artifact. More generally delta_v,delta_w tend to zero, X(s) tends to (x0,y0), and G(s)=x0^2+y0^2-s^(1/8)+o(1) tends to minus infinity. The remote root is finite, at approximately s=6.766258243562386*10^15.

The code refines each of the five intervals by sign-preserving bisection, never assuming uniqueness. Independent resulting centers agree with the explanatory positions:

(-0.3864062930,0.5196541287), (-0.3589856359,-0.5501782938),

(0.0896235465,-0.9408699996), (0.0936742413,0.9643898289),

(0.1036500000,9.7582578125).

These decimals are explanatory; the proof is the rational sign certificate and IVT. The exact last x is strictly below b/2 despite rounding to the same decimal.

## 3. Algebraic boundary roots are uniquely and continuously defined

For nonzero q and real h define g(t)=(t^2+h^2)^8 and

F(t)=|q|^16[g(t-1)-g(t)]-L.

For the boundary choices h=10,1,-10, h is nonzero and

g''(t)=16(t^2+h^2)^6(h^2+15t^2)>0.

Consequently F'(t)=|q|^16[g'(t-1)-g'(t)]<0 everywhere. Also g(t-1)-g(t) has leading term -16t^15, so F tends to plus infinity at minus infinity and minus infinity at plus infinity. Exactly one real root exists. This supplies global uniqueness, rather than merely uniqueness within the numerical brackets. For h=0, g=t^16 is also strictly convex, so the same uniqueness statement remains valid; that boundary case is unused here.

If these input parameters vary while q stays nonzero, the derivative with respect to t stays nonzero at every solution, so the implicit function theorem gives local continuous dependence, with uniqueness joining the local branches. In the actual proof, the boundary parameters are fixed exact algebraic numbers, rather than varying choices from interval boxes.

The independent verifier brackets the three exact roots with rational endpoint signs after 128 bisections, from the different starting interval [-8,8]. These roots yield the same A1,A3,A5 as the submission. The even boundary points are A2=A,A4=B,A6=C. The exact coordinate intervals prove all six points are distinct. They give

0.00132672=det(A4-A2,A6-A2),

6.37<det(A3-A1,A5-A1)<6.39.

The checker additionally proves that no three boundary points are collinear. No boundary degeneration or inversion ambiguity remains.

## 4. All outgoing quad identities, without reliance on a flip theorem

The boundary construction gives exactly

N(A1,C)-N(A1,A)=1,
N(A3,B)-N(A3,A)=lambda,
N(A5,C)-N(A5,B)=1-lambda.                                    (3)

For compact checking, write a=N(A1,A), f=N(A3,A), g=N(A5,B). In cyclic boundary order the six edge powers are

a, f, f+lambda, g, g+1-lambda, a+1.                            (4)

Their odd and even sums both equal a+f+g+1. This is the exact telescoping identity needed for the cube equations; it is not an approximate interval equality.

For each X solving (1):

* A2 A3 A4 X: f+N(X,B)=N(X,A)+(f+lambda).
* A4 A5 A6 X: g+N(X,C)=N(X,B)+(g+1-lambda).
* A6 A1 A2 X: (a+1)+N(X,A)=N(X,C)+a.

Each is the alpha-quad definition, in the correct combinatorial order. Their derivation uses exact identities (1) and (3), so rational enclosures are not being mistaken for proofs of equality.

Every outgoing center is distinct from each boundary point. Positive lambda excludes B and forces x<b/2; positive second level excludes C. The point A fails the lambda equation because b^16!=lambda. Independently certified A1 and A5 have x>b/2. Finally A3 has second-equation residual in (0.98,0.99), so it fails that equation. Refined root boxes additionally verify these exclusions and show that every selected X avoids every line through two boundary points. Edges incident to a center therefore cannot collapse or overlap one another.

## 5. Incoming IVT with fixed algebraic coefficients

Set

L=N(B,A5)-N(B,A3)=g-f-lambda,
M=N(A,A1)-N(A,A3)=a-f.

Independent boundary enclosures prove both levels strictly positive. Approximate magnitudes are L=5.9175845*10^6 and M=6.1789357*10^10; these rounded figures do not decide any sign.

Translate the common incoming focus A3 to zero. Put b'=A5-A3, c'=A1-A3 and D'=det(b',c'). The exact D' equals the positive odd determinant above. For s in [0.01,0.011], the scalar residual H is defined by solving

2b' dot Y=|b'|^2+s^(1/8)-(s+L)^(1/8),
2c' dot Y=|c'|^2+s^(1/8)-(s+M)^(1/8),

and setting H(s)=|Y|^2-s^(1/8). All root arguments are positive, and D' is bounded away from zero. Thus H is continuous for this one fixed algebraic boundary triple. Interval arithmetic encloses that same fixed function, uniformly over its certified coefficient boxes; it does not choose a different boundary triple at either endpoint.

The independent exact reconstruction gives

H(0.01) in (0.00037,0.00038),
H(0.011) in (-0.00081,-0.00080).

The sign margin survives all dependency overestimation in the interval calculation. IVT gives a root and Z=A3+Y with

N(Z,A5)-N(Z,A3)=L, N(Z,A1)-N(Z,A3)=M.

The same first-principles equivalence from section 1 applies with the invertible translated linear system, so no incoming extraneous root is introduced. The enclosure for the whole retained s interval has Zx in (0.1677,0.1717), Zy in (-0.0036,-0.0026), disjoint from every boundary point. All lines through boundary pairs are also excluded.

The incoming alpha-quad identities are now directly checkable from (4):

* A1 A2 A3 Z: a+N(Z,A3)=N(Z,A1)+f, since M=a-f.
* A3 A4 A5 Z: (f+lambda)+N(Z,A5)=N(Z,A3)+g, since L=g-f-lambda.
* A5 A6 A1 Z: (g+1-lambda)+N(Z,A1)=N(Z,A5)+(a+1), since M-L=a-g+lambda.

The last equality also reads M-L=N(C,A1)-N(C,A5), by exact (3). No existence theorem, conjectured bound, or desired conclusion is assumed.

## 6. Strongest verified result and limits

The strongest verified result is the existence of one fixed admissible alpha=16 incoming realization admitting at least five distinct, nonboundary outgoing centers. All six old/new face identities follow algebraically; interval certificates establish the required strict inequalities and IVT signs. This contradicts the maximum-three assertion in the crossing-allowed setting.

No unresolved algebra/analysis gap remains for that existence claim. This audit does not show that any interval contains exactly one root, that exactly five is the total count for these data, that five is a universal maximum, or that the configurations are proper embeddings. Those stronger statements are unnecessary for the submitted counterexample and remain unproved here. Historical novelty and publication disposition are outside this audit's assignment.
