# Supplementary all-odd-prime proposition (version 1.1)

The class3 full-affine theorem and its limsup1/liminf-at-most23/24 statement
remain unchanged. Primes1mod4 do not give full-affine permutations. This
additional proposition states exactly how natural exceptional-fiber conventions
address a choice of any positive-upper-prime-density selection.

For every odd p, N=p-1, theta=phi(N)/N, r=#roots(u^2+1) in {0,2}, and
Omega={(u,v):u^2+1 !=0}, |Omega|=p(p-r). Let P count nonzero primitive
multipliers. The zero-extended character indicator has principal term
(p-r)theta, all nonprincipal sums have modulus <=sqrt(p), and S_eta=-1.
Thus |P/p-theta| <=r theta/p+theta(2^omega(N)-1)/sqrt(p)
<=2/p+64p^(-1/4), uniformly over all odd primes.

For fixed1/2<=x<1 with p(1-x)>1, exact uniform regular-point weighting gives
D_reg(x)=1-(p-1)P/[p(p-r)], and the globally bounded continuous ramp
h(t)=max(0,min(1,2t-1)) gives integral h=(1-2/p)(p-1)P/[p(p-r)].
These equal1-theta+o(1) and theta+o(1), respectively.

Retain all regular points and any e of at most rp exceptional points, assigning
finite nonnegative periods only to those exceptional points. Uniformly
renormalized weights give mu_tilde=R/(R+e) mu_reg+xi with R=p(p-r) and
mass(xi)=e/(R+e)<=r/p. Every [0,1]-valued statistic differs by at most r/p;
a general bounded real statistic differs by at most2||f||_infinity r/p.
This includes deleting all exceptional fibers, deleting only nonperiodic
points, and completing all p^2 points. Assigned periods can exceed p, so the
measures are on [0,infinity), and h is globally bounded there.

The credited atomless whole-prime theta law excludes convergence of theta
on every positive-upper-prime-density set. The uniform formulas and error
bound therefore exclude both fixed-x CDF convergence and weak convergence
under each stated convention, including prime selections within class1 or
mixing both odd classes. The source need not be read as specifying a unique
completion convention. No elliptic-fiber, polynomial-automorphism, prime-average,
new arithmetic-law or historical-firstness claim is added.

check_all_odd_primes.py supplies separate exact finite diagnostics: all167 odd
primes through1000 (80 class1,87 class3), 46,298 controls and10,178 raw regular
graph points. Its assignments include normalized periods greater than1.
These are not a numerical proof of the classical atomless law. The existing
147,619-check class3 receipt remains a separate run.
