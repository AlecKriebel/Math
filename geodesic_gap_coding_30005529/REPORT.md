# Compatible geodesic/horocycle root-gap coding: five-approach checkpoint

Problem: row 1844, ID 30005529, OWR13750333-010 (Pohl, 2023).
Assessment: **not solved**. Five concrete approaches were developed. The rigorous results below identify the observable and normalization, reject direct reuse and flow-displacement repairs of the horocycle sheet, provide explicit reconstruction formulas and finite arithmetic tests, and isolate a finite-multiplicity issue. They do not construct the requested geodesic symbolic successor producing horizontally adjacent root gaps.

## Scope and sources

The source question asks whether a geodesic-flow coding can give the gaps obtained from the Marklof–Welsh horocycle coding. It does not specify an alphabet, smoothness class, or require conjugacy of the flows. Consequently neither an entropy argument against flow conjugacy nor the failure of one particular section resolves it. The intended substantive target appears to be a geodesic coding with a proved root-gap observable and usable ordering rule, potentially suitable for spectral applications. This is an interpretation of an informal question, not an extra hypothesis attributed to its author.

Public sources inspected:
- Pohl's question, Oberwolfach Report 22/2023, printed p.1255, Question 2: https://ems.press/content/serial-article-files/47016
- Marklof–Welsh, *Fine-scale distribution of roots of quadratic congruences*, arXiv:2105.02854, sections 2.3, 3.1, 4.5 and Theorem 5.1: https://arxiv.org/abs/2105.02854
- Arnoux–Schmidt, *Cross sections for geodesic flows and alpha-continued fractions*, particularly section 4 and Lemma 5.2: https://sites.science.oregonstate.edu/~schmidtt/research/ourPapers/Arnoux/AS2.pdf ; https://arxiv.org/abs/1207.7299
- Series, *The Modular Surface and Continued Fractions* (1985): https://doi.org/10.1112/jlms/s2-31.1.69

A targeted web search on 2026-10-21 located these sources and a 2026 Arnoux–Schmidt overview, but did not establish that anyone has resolved Pohl's specific question. This is a bounded search result, not a literature-wide proof of openness.

## Approach 1. Exact observable and clock normalization

Let D>1 be squarefree, D not congruent to 1 modulo 4, and let
R_D(M) = {(m,mu): 1<=m<=M, 0<=mu<m, mu^2 congruent to D modulo m}.
Retain these labels even when mu/m agrees for different m. For a label define
F(X,Y)=m X^2-2 mu XY+((mu^2-D)/m)Y^2.
Its discriminant is 4D. Its real roots are (mu-sqrt(D))/m and (mu+sqrt(D))/m. The corresponding positively oriented semicircle has top mu/m+i sqrt(D)/m. These last assertions follow directly from the quadratic formula and the center/radius of a semicircle.

Set y=sqrt(D)/M. The geometric window alpha y<=Im(top)<beta y corresponds exactly to
M/beta < m <= M/alpha,
where M/infinity=0. Thus alpha=1, beta=infinity gives m<=M, including the endpoint m=M. Reversing the strict lower bound is an error.

With a(y)=diag(sqrt(y),1/sqrt(y)) and n(t)=[[1,t],[0,1]], direct multiplication gives
n(x)a(y)n(t)=n(x+y t)a(y).
Therefore distinct consecutive root locations x_i<x_{i+1} on the circle have positive horocycle elapsed time (x_{i+1}-x_i)/y; the wrap-around elapsed time is (1+x_1-x_last)/y. The period is 1/y, not 1.

If N=|R_D(M)|, the empirical mean-one gaps are N times the labelled cyclic rational gaps, not automatically the horocycle return times themselves. The conversion factor is N y. If the asymptotic root intensity is kappa with N y tending to kappa, the corresponding limiting mean-one scale is kappa times horocycle time. For a truncated alpha,beta window the intensity includes the additional factor 1/alpha-1/beta.

Outcome: the target data and necessary clock conversion are explicit. This is not yet a geodesic coding.

## Approach 2. Continued-fraction suspension: what it gives and what it does not

The regular continued-fraction natural extension has coordinates x,z in (0,1), digit a=floor(1/x), and update
(x,z) -> (1/x-a, 1/(a+z)).
Arnoux–Schmidt provide the modular geodesic realization with an orientation double cover and return time -2 log x. In their area coordinates one uses w=z/(1+x z); representatives are
A_-(x,w)=[[1,w],[-x,1-xw]],
A_+(x,w)=[[x,1-xw],[-1,w]].
A suspension point is represented by Gamma A_sign(x,w)a(e^t) for 0<=t<-2 log x, with the standard almost-everywhere qualifications. The orientation label is essential: dropping it does not produce the same geodesic return system.

Attempt: pull the root-gap function back to this explicit geodesic suspension. This indeed defines a measurable observable wherever the original function is defined. It can reconstruct a matrix representative from symbolic coordinates and compute geometric quantities. But defining F(code,t)=tau_horocycle(Gamma A(code)a(e^t)) simply imports the horocycle return problem unchanged. It gives no proof that iterating the geodesic shift produces successive horizontally ordered roots. Thus it is a weak information-representation answer, not an accepted solution here.

There is another limitation for exact finite roots: the states Gamma n(x)a(y) have a vertical geodesic endpoint at infinity; x is rational. These cusp-to-cusp geodesics lie outside the full-measure recurrent two-sided continued-fraction coding. An almost-everywhere coding cannot silently be applied to all of these exceptional finite-data states. A different geodesic construction or an explicit boundary extension would be needed. Random limiting Haar states do not have this obstruction.

Outcome: a concrete geodesic model and two missing compatibility steps: exceptional-state coverage and horizontal successor ordering.

## Approach 3. Transversality and attempted section repairs

Write h_l(s,v)=Gamma g_l a(s)k(-pi/2)a(v^-1), with 1<=s<epsilon_l^2 and alpha<=v<beta.
For geodesic time t,
h_l(s,v)a(e^t)=h_l(s,v e^-t).
For alpha<v<beta, this remains in the sheet for all sufficiently small positive and negative t. Hence the geodesic vector field is tangent and the infimum of positive times returning to the sheet is zero at its interior. This rules out interpreting this same sheet as a geodesic Poincare section with a positive roof.

A stronger limited no-go statement follows. A smooth variable-time displacement
h_l(s,v) -> h_l(s,v)a(exp(f(s,v)))
is still h_l(s,v exp(-f(s,v))). Wherever its image has rank two, it is locally inside the same geodesic-tangent surface; where the rank falls, it is not a two-dimensional transverse section. Merely sliding points along geodesic orbits therefore cannot repair this sheet.

A genuinely different local transverse surface can be built. Fix v0>0 and put
C_l={(Gamma g_l a(s)k(-pi/2)a(v0^-1)n(u)): s near s0, u near 0}.
Let H=diag(1/2,-1/2) and N=[[0,1],[0,0]]. At u=0 its tangent space, translated to the identity by g^{-1}dg, is spanned by N and
Ad(a(v0)k(pi/2))H = [[0,v0/2],[1/(2v0),0]].
These two vectors together with H are linearly independent. The surface is locally transverse to geodesic flow, and transversality persists near u=0. This is a valid local geometric repair, unlike a geodesic-time slide.

However, replacing v by a horocycle coordinate discards the original height-window parameter. No global return map, recurrence assertion, or root-neighbor relation has been proved for this replacement. A local flow box is not a coding solution.

Outcome: rigorous obstruction for two naive constructions and an explicitly transverse but incomplete alternative.

## Approach 4. Symbolic modular lifts and a non-tautological decoder

Suppose a positively oriented closed geodesic has finite endpoints u<v, recovered from a periodic geodesic word. For gamma=[[a,b],[c,d]] in SL(2,Z), set P=(cu+d)(cv+d). The endpoints of gamma c are
U=(au+b)/(cu+d), V=(av+b)/(cv+d).
Their difference is (v-u)/P. Therefore gamma c is positively oriented exactly when P>0, and its top has
center X=((au+b)(cv+d)+(av+b)(cu+d))/(2P),
radius Y=(v-u)/(2P).
These formulas are obtained by elementary subtraction and addition, not by querying a horocycle-return oracle. Since u,v are quadratic irrationals, integer Möbius denominators do not vanish.

Candidate decoder: recover endpoints of the finitely many discriminant-4D closed classes from periodic words; enumerate modular translates modulo their stabilizers and integer horizontal translations; retain P>0, alpha y<=Y<beta y; reduce X modulo one; preserve all class/lift labels; sort by X; subtract neighboring values. By the geodesic/root correspondence this reproduces the finite root multiset and all its gaps. For guaranteed finite termination in the arithmetic case, enumerate the bounded integer forms in Approach 1 rather than blindly increasing group-word length: m and mu then have explicit finite ranges.

This is a meaningful explicit geometric-to-arithmetic decoder, not just 'every point is reconstructable.' Nevertheless its horizontal sorting operation is external to the geodesic successor map. A periodic geodesic word follows one closed orbit, while the height-truncated root list aggregates many translates and classes. No claim is made that the next root is the next geodesic symbol, the next return, or an induced geodesic return. Nor has a regular/finite-memory observable been proved. Under an exceptionally weak interpretation allowing arbitrary global postprocessing of a coding, the construction supplies the desired data; under the substantive surface-of-section interpretation it leaves the central question open.

Outcome: explicit decoder and completeness route, but missing intrinsic dynamical ordering.

## Approach 5. Exact arithmetic checks and finite multiplicity

The included Python script uses only exact integers and Fraction arithmetic. For each root it checks discriminant 4D and computes labelled cyclic gaps, coefficients of horocycle times in units 1/sqrt(D), and empirical mean-one gaps. No floating-point comparison determines ordering.

Executed cases (D,M,N,distinct positions,zero gaps):
- (2,10,4,3,1)
- (3,10,4,2,2)
- (6,20,12,7,5)
- (2,100,40,39,1)
- (3,100,46,44,2)
- (6,100,58,51,7)
All cyclic rational gap sums equal 1 exactly.

For D=2, M=10 the labelled positions are 0/1, 0/2, 3/7, 4/7. The gap list is (0,3/7,1/7,3/7). The ordinary strict positive first-return function on an unlabelled section has only three distinct event locations and cannot emit the zero gap. Consequently an exact finite statement needs sheet labels/coincident-event multiplicities, or must explicitly pass to distinct locations or a limit. Thin-window injectivity and broad-window multiset statistics are not interchangeable.

### Lemma: only finitely many collisions for fixed squarefree D

Suppose two distinct labels have the same reduced fraction p/q in [0,1), gcd(p,q)=1. Write (m,mu)=(kq,kp). The congruence k^2 p^2 congruent to D modulo kq implies k divides D. For a second label k' likewise divides D, and k' differs from k. Reducing both congruences modulo q and subtracting gives
(k^2-k'^2)p^2 congruent to 0 modulo q.
As p is invertible modulo q, q divides k^2-k'^2. Therefore q<=D^2-1 and m<=D(D^2-1). There are only finitely many such labels, uniformly in cutoff M. The case p=0 has q=1 and satisfies the same conclusion. (For q=1, invertibility is interpreted through gcd(p,1)=1, or handled separately.)

Thus the total number of zero gaps is bounded by a constant depending only on D. Their empirical mass is O_D(1/N) and vanishes as N grows. Collapsing these finitely many duplicate positions also changes only O_D(1) terms and the normalization asymptotically. This explains why the finite multiplicity issue does not contradict a simple limiting point process. It does not license dropping multiplicities in an exact finite decoder.

Outcome: reproducible tests, a counterexample to an overstrong finite first-return statement, and a proof that the discrepancy is asymptotically negligible.

## What is still required for a solution

At minimum, supply an actual geodesic symbolic system or induced geodesic section together with a proved rule producing the relevant gap process, including the ordering, normalization, and treatment of exceptional or repeated events. A distributional answer may bypass exact cusp-state coding but must prove the claimed law and explain why the construction is more than evaluating the original horocycle-return oracle after a coordinate change. An exact finite answer must keep the root labels or explicitly handle their collisions.

The findings above do not prove nonexistence. They do not justify marking the queue solved. Independent adversarial review accepted the scope, normalization, collision lemma, Möbius orientation test, and local transversality calculation. A trivialization terminology correction was applied. The reviewer did not independently source-certify the Arnoux–Schmidt domain and roof formulas; those were checked against the primary paper by this research worker. Its report is separate.

### Additional explicit symbolic-lift unit test

For the D=2 geodesic with endpoints -sqrt(2),sqrt(2), a determinant-one matrix [[a,b],[c,d]] gives P=d^2-2c^2, top center (bd-2ac)/P and height sqrt(2)/P, provided P>0. The four matrices
[[1,0],[0,1]], [[1,1],[1,2]], [[0,1],[-1,3]], [[0,-1],[1,3]]
produce precisely (m,mu)=(1,0),(2,0),(7,3),(7,4), the complete M=10 list above. The matrix [[0,-1],[1,0]] has P=-2 and is correctly excluded for negative orientation. The separate exact script endpoint_decoder_check.py verifies all determinants, congruences, and expected labels, giving an elementary non-oracle test of Approach 4.
