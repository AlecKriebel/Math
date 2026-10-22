# Author approach 3: normalize and test the geometric-recursion route

Problem 30004711. 7 October 2026. Third directed mathematical approach. Earlier frozen approaches are unchanged.

## Goal and result

Try to prove the desired equality of total volumes without proving equality of their Euler representatives: establish that the actual torsion-integral sequence satisfies a triangular geometric recursion with the same initial data as the intersection sequence.

The normalization conjugacy, uniqueness argument, kernel convergence, and first nontrivial values can all be established explicitly. This approach stops at the premise that the **actual OWR torsion integrals**, in a verified convention, satisfy that recursion with no missing remainder. A formal topological recursion or an identity at one fixed surface is insufficient for that premise.

## 1. Fix kernels and three distinct sequences

Write T_(g,n)=V^Theta_(g,n). For L real define

H(x,L)=[sech((x-L)/4)-sech((x+L)/4)]/(4 pi),
D(L,x,y)=H(x+y,L),
R(L,L_j,x)=[H(x,L+L_j)+H(x,L-L_j)]/2.

Let I_D denote integration of x y D against the sum of the handle term and stable separating products; let I_R denote the sum of integrations of x R against the boundary-merging term. Ordered decompositions are used for the separating sum.

Norbury's canonical intersection polynomials satisfy

L T_(g,n)=(1/2) I_D[T]+I_R[T],
T_(1,1)=1/8,
T_(0,3)=0.

The pure-NS unstable disk/annulus entries are zero and not retained as independent initial data. Define two differently normalized sequences

W_(g,n)=2^(1-g-n)T_(g,n),
S_(g,n)=(-1)^n 2^(1-g)T_(g,n)=(-2)^n W_(g,n).

Their recursions are, respectively,

L W_(g,n)=(1/2)I_D[W]+(1/2)I_R[W],
L S_(g,n)=(-1/4)I_D[S]-I_R[S].

These are not the same recursion with the same volume symbol. The notation S labels the SW convention; it is not an unproved assertion that OWR's Vhat uses it.

## 2. Derive the factors instead of guessing them

Suppose S_(g,n)=a_(g,n)T_(g,n), and demand the SW coefficients just displayed. A merging term requires

a_(g,n)/a_(g,n-1)=-1.

A nonseparating term requires

a_(g,n)/a_(g-1,n+1)=-1/2.

Starting from a_(1,1)=-1, these give a_(g,n)=(-1)^n 2^(1-g) for all g>=1,n>=1. For a separating term, n_1+n_2=n+1 and g_1+g_2=g, so

a_(g,n)/(a_(g_1,n_1)a_(g_2,n_2))=-1/2,

exactly the same required factor. The corresponding calculation for W leaves the handle/separating coefficient unchanged and halves the merging coefficient.

SW equation (5.42) uses a kernel one-half of H, explaining its displayed -1/2 handle coefficient rather than -1/4 in the common-H convention above. Its sum of the two single-boundary kernels equals R. Thus all coefficients match without rescaling the lengths.

There is also a geometric source for the asymmetry of the coefficients. [Stanford–Witten, 1907.03363v5](https://arxiv.org/abs/1907.03363v5), Appendix D.6, printed p.134 / PDF p.135, counts spin structures with chosen boundary trivializations and explains the extra factor2 in the boundary-merging term. The same passage uses parity-weighted spin sums and cancellation in a transverse spin choice at a Ramond seam. These data must be mapped to the unweighted algebraic spin stack; they cannot be dropped while retaining its recurrence.

## 3. Exact genus-one kernel computation

The all-NS pants kernel used in SW (D.44) is

D_SW(b,x,x)=-[sech((2x-b)/4)-sech((2x+b)/4)]/(8 pi).

The improper integral is absolutely convergent for every fixed b. Let a=b/4 and substitute t=x/2. Oddness of u sech(u), together with integral_R sech(u)du=pi, gives

integral_0^infinity t[sech(t-a)-sech(t+a)]dt=pi a.

Therefore

integral_0^infinity x D_SW(b,x,x)dx=-b/8.

So the *kernel formula* b S_(1,1)(b)=integral x D_SW dx yields S_(1,1)=-1/8, and the convention map yields T_(1,1)=1/8 and W_(1,1)=1/16. The limit b->0 is harmless for this kernel expression.

This is not yet an independent evaluation of the torsion integral: it validates the last analytic integral in the pants-unfolding argument, conditional on the geometric identity and justified unfolding leading to it. In particular, (D.45) also combines the one-holed-torus half-volume convention and a spin-sum factor2. Those cannot be reconstructed from the scalar integral alone.

## 4. Verify a nontrivial recursive coefficient

The useful moment identities are

integral_0^infinity x H(x,L)dx=L,
integral_0^infinity s^3 H(s,L)ds=L^3+12 pi^2 L.

For example, convert the odd-power difference to an integral over the whole real line and substitute s=L+4u. The moments integral sech(u)du=pi and integral u^2 sech(u)du=pi^3/4 follow from

integral_R exp(tu)sech(u)du=pi/cos(pi t/2), |t|<1,

by differentiating at t=0. The integral formula itself follows by v=exp(u) and the elementary beta integral.

The first moment gives integral x R(L,L_2,x)dx=L and hence T_(1,2)=1/8. For (2,1), the handle and separating inputs sum to

T_(1,2)+T_(1,1)^2=1/8+1/64=9/64.

Changing x,y to s=x+y, integral_0^s x(s-x)dx=s^3/6. Thus

L T_(2,1)=(1/2)(9/64)(L^3+12 pi^2 L)/6,
T_(2,1)=3(L^2+12 pi^2)/256.

Consequently W_(2,1)=3(L^2+12 pi^2)/1024 and S_(2,1)=-3(L^2+12 pi^2)/512. This agrees with the distinct source normalizations; it does not merge them into one undefined hat symbol. Exact symbolic and rational checks are supplied alongside this note.

## 5. Conditional uniqueness is sufficient, but only after a geometric theorem

For n>=1 and 2g-2+n>0, order pairs by c=2g-2+n. The two base pairs at c=1 are (0,3) and (1,1). Every merging or nonseparating term has complexity c-1. Every stable component of a separating term has smaller complexity, since its two positive complexities sum to c-1.

It follows by induction that two sequences with the same finite-integral recursion, the same base data, and the same omitted unstable terms agree for L_1>0. If they extend continuously to zero lengths, equality extends there. No assumption that the unknown geometric volumes are already polynomials is needed for this uniqueness implication.

For the polynomial sequence T, convergence of the recursion is direct: |H(x,L)|<=C_L exp(-x/4), and |D(L,x,y)|<=C_L exp(-(x+y)/4). The same holds for R with a constant depending on the external lengths. These bounds integrate against every polynomial input. They do not prove growth bounds for an independently defined torsion-volume sequence.

The n=0 values never enter this positive-boundary recursion. If the intended claim includes closed surfaces, a separate justified closed-volume relation is needed. Analytic evaluation of the known polynomial at a complex length does not by itself provide such a relation for an unverified geometric sequence.

## 6. The exact unproved geometric premise in this route

To apply the induction to the original torsion integrals, one must verify all of the following for those integrals, with their precise conventions:

1. A super-McShane identity in the required genus/boundary range, interpreted in the same retraction as the integration.
2. A valid passage from the infinite geodesic/pants sum to the noncompact moduli integral, including the top odd coefficient of the product with the torsion density.
3. The torsion gluing/disintegration formula with all automorphism, boundary-trivialization, orientation, and parity factors.
4. Vanishing or cancellation of the Ramond-seam contributions actually discarded, with no remaining cusp or cutoff term.
5. The geometric base integrals in those conventions.

A precise sufficient condition for item2 is coefficientwise L1 summability of the terms after multiplication by the torsion density, or an alternative dominated-convergence argument for the remainder. If Phi_P denotes the pants contribution and E_R the remainder after a finite truncation, the required statement is

lim_R integral top_odd(E_R mu_tau)=0.

Pointwise convergence E_R->0 at each surface does not give this limit. Finite volume of mu_tau alone also does not control the coefficients of E_R mu_tau.

[Huang–Penner–Zeitlin, Super McShane identity, 1907.09978v3](https://arxiv.org/abs/1907.09978v3), proves a rigorous identity for each fixed once-punctured super torus. Theorem5.5 explicitly uses a constant depending on the super surface; Theorem6.1 and Proposition6.3 establish the identity and absolute convergence there. Its introduction distinguishes this theorem from the heuristic volume-recursion program. This is substantial input but not a proof of items1–5 in the full required range.

[Norbury, 2608.25237v2](https://arxiv.org/abs/2608.25237v2), section4.3.3, p.33, still identifies additional rigorous work in the supergeometric derivation, specifically including the positive-length Ramond-boundary volume issue. Norbury's proved intersection recursion cannot simply supply the geometric premise here: that would substitute the already accepted canonical definition for the torsion measure under investigation.

[Johnson, 2606.20796v1](https://arxiv.org/abs/2606.20796v1), derives volume-recursion formulae from a spectral curve, with explicitly stated convention changes. This advances formal/spectral equivalence; it does not independently establish the missing noncompact torsion integration and interchange statements for OWR's measure.

## Outcome

If the actual torsion sequence satisfies the fully specified geometric recursion, then the normalization map and induction above give an immediate total-volume comparison without pointwise Euler-form equality. But that premise is not certified by the inspected sources, and the exact remainder needed to certify it is displayed above. Matching formal recursions and base kernel integrals cannot be promoted to an equality of independently defined geometric integrals.

This third approach therefore establishes the complete conditional recursion argument and its normalization constants, while locating the missing geometric theorem. The literal OWR identity remains pending; this is not a final unsuccessful disposition.
