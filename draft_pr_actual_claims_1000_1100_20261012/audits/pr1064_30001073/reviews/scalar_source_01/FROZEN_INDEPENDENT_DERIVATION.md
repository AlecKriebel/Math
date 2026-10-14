# Frozen independent derivation: scalar and source family

This file was frozen before reading submitted ACCEPTANCE.md, AUDIT.md, SOURCE_LEDGER.md, PROVENANCE.md, STATUS.json, README.md, MANIFEST.json, or audit_manifest.json. Inputs then consumed: root AGENTS.md, submitted PROOF.md, pinned Git metadata and SUBMITTED_PINS, and freshly downloaded full primary PDFs. The submitted PROOF contains acceptance/status prose, which was not treated as a premise. This is an independent verification of its argument, not independent invention of the proposed inequalities. No sibling review was read.

## Claim, assumptions, and success criterion

For integer n>=1 and a nonnegative n-by-n matrix A whose rows sum to one, define S=sum a_ij^2. The claim is

log per(A) <= -n + exp(4) sum a_ij^2 log(e/a_ij)
               <= -n + exp(4) S(1+log n),

with the first expression understood as a permanent inequality if per(A)=0. Terms at a=0 have their continuous values zero. For fixed gamma>=1 and doubly stochastic A with S<=gamma, the original asymptotic target follows. The scalar claim is universal on 0<=a,b<=1, except a=0 allows only b=0. Mathematical success requires proof with zero/one endpoints, correct entropy interface and source hypothesis; numerical samples alone cannot establish it. Novelty/priority and present worldwide open status are outside the claim.

## Independent scalar proof

Write g(b)=-b^2 log b/(1-b), extended by g(0)=0 and g(1)=1, and d(b,a)=b log(b/a)-b+a for a>0, with d(0,a)=a and d(0,0)=0. The extensions follow from b^2 log(1/b)->0 as b->0 and log(1/b)/(1-b)->1 as b->1. For a>0 put x=b/a. Then d=a(x log x-x+1)>=0 because this convex function has minimum zero at x=1, including x=0 by continuity.

For 0<b<1, integrating 1/t between b and 1 gives b log(1/b)<=1-b; equivalently log x<=x-1 with x=1/b. Therefore g(b)<=b. Also

log(1/b)/(1-b) <= 1+log(1/b)

is equivalent to the same inequality, so g(b)<=h(b):=b^2 log(e/b). Both comparisons include b=0,1 by their limits. Since h'(b)=b(1+2 log(1/b))>0 on (0,1], h increases on [0,1].

For a,b>0, split at b=exp(2)a. In the large-b case, log(b/a)>=2 yields d>=b+a>=b>=g(b), hence g-d<=0. This case is empty if exp(2)a>1. In the other case, d>=0, so g-d<=h(b). If b<=a use monotonicity: h(b)<=h(a). If a<b<exp(2)a, then b^2<exp(4)a^2 and log(e/b)<=log(e/a), both positive. Thus h(b)<=exp(4)h(a). This proves the requested scalar inequality without evaluating h(exp(2)a) outside its monotonicity domain. At b=0 it reads -a<=exp(4)h(a); at a=b=0 both sides are zero. At b=1 use the defined limit; at a=1, d>=0 and g<=1 while the right side is exp(4), so there is no endpoint exception. The only a=0 point is (0,0). At b=a>0, d=0 and g<=h(a), with equality g=h only at a=1; the exp(4) version is deliberately loose.

## Full entropy interface checked directly

Let X be any random permutation, with b_ij=P(X_i=j). Let row priorities T_i be independent Uniform(0,1) variables independent of X. For each realized priority ordering, the chain rule gives H(X) as the sum of conditional row entropies. At a positive-probability history, let U be the available columns, q the conditional law of X_i, and Z=sum_{j in U} b_ij. For q_j>0 the unconditional b_ij is positive. Thus q is absolutely continuous with respect to the probability vector r_j=b_ij/Z on U and Z>0. Expanding KL(q||r)>=0 gives

H(q)+sum_j q_j log b_ij <= log Z.

Averaging over histories and independent priorities gives

H(X)+sum_ij b_ij log b_ij <= sum_i E log Z_i.

Fix a supported full permutation X and T_i=t. Because each column occurs exactly once, U consists of X_i and the X_k for k!=i with T_k>t. Hence

E[Z_i|X,T_i=t] = b_i,X_i +(1-t)(1-b_i,X_i).

Here conditional Jensen is legitimate: Z_i is always at least the sampled positive number b_i,X_i. Write b=b_i,X_i>0. Direct integration of log over [b,1] gives

integral_0^1 log(b+(1-t)(1-b))dt = -1-b log b/(1-b),

with value 0 at b=1. After averaging over X, each row contributes at most -1+sum_j g(b_ij). Terms b=0 are never sampled; weighted expressions are assigned continuous limit zero. This proves

H(X) <= -sum_ij b_ij log b_ij -n+sum_ij g(b_ij).

If per(A)>0, its Gibbs law has mass product_i a_i,sigma(i)/per(A). Its marginal B is doubly stochastic and b_ij>0 implies a_ij>0. Expanding entropy gives exactly log per(A)=H(X)+sum b_ij log a_ij. Therefore

log per(A)<=-n+sum(g(b_ij)-b_ij log(b_ij/a_ij)).

A and B each have total mass n, so sum(-b_ij+a_ij)=0 and the last sum can replace b log(b/a) by d(b,a). This replacement depends on row stochasticity of A, not column stochasticity. All entries of A and B are in [0,1]; (a,b)=(0,0) handles support zeros. Applying the universal scalar inequality entry by entry proves the first permanent bound. The per(A)=0 case holds directly without defining Gibbs law.

## Frobenius conversion and all n

Cauchy-Schwarz in each row gives sum_j a_ij^2 >=1/n and hence S>=1. Let p_ij=a_ij^2/S, a probability distribution on at most n^2 points. Entropy relative to the uniform n^2-point law yields H(p)<=log(n^2)=2log n. For a>0, log p=2 log a-log S; summing yields the exact identity

sum a_ij^2 log(1/a_ij) = (S/2)(H(p)-log S) <= S log n,

since log S>=0. The identity respects zero terms. Add sum a^2=S to obtain sum a^2 log(e/a)<=S(1+log n). Replacing S by gamma is valid because 1+log n>0. Thus

per(A)<=exp(exp(4)gamma) n^(exp(4)gamma) exp(-n)

for every n>=1. For n>=2, 1<=2log n (use log 2=integral_1^2 dt/t>=1/2), hence 1+log n<=3log n and per(A)<=n^(3exp(4)gamma)exp(-n). At n=1, A=[1], per(A)=1, so a prefactor-free n^C exp(-n) is false for every C. The submitted all-n formulas retain the needed prefactor. At gamma=1 the Frobenius condition forces the uniform matrix by the row Cauchy-Schwarz equality conditions.

## Necessary polynomial loss and no sharpness claim

For fixed integer k>=1, set n=km and take k disjoint J_m/m blocks. Each block contributes one to S, so S=k. Independence across blocks yields per(A)=(m!/m^m)^k. Stirling for fixed k and m->infinity gives

per(A) ~ (2pi/k)^(k/2) n^(k/2) exp(-n).

Thus the exponential scale cannot have a constant prefactor depending only on gamma at gamma=k, and any power exponent uniformly valid there must be at least k/2. This establishes necessary polynomial loss; it does not identify the optimal exponent or make exp(4)gamma sharp.

## Original source and exact condition

Fresh official EMS PDF 46191, printed pages 2549-2550 (PDF pages 73-74), was read in text and rendered images. Problem 9 fixes gamma>=1 and asks for permanent of doubly stochastic A to have polynomial-factor exp(-n) order when the unnormalized sum of squared entries is <=gamma. The preceding paragraph gives the known van der Waerden lower bound n!/n^n. The following note calls a_ij<=gamma/n a stronger sufficient hypothesis. Consequently the proposed upper bound addresses the actual Frobenius condition; a lower-bound proof is not part of the proposed contribution. Fixed gamma and asymptotic n are essential to the notation.

The Frobenius condition really permits larger entries: for gamma>1 and n>=gamma, A=(1-t)J_n/n+tI_n with t=sqrt((gamma-1)/(n-1)) is doubly stochastic and S=gamma. Its diagonal entries have order n^(-1/2), exceeding gamma/n eventually. Therefore replacing Frobenius by the entrywise condition would lose valid inputs.

## Fresh prior-proof boundary

Fresh arXiv:1811.02933v2, sections 1.4 (printed pages 5-6) and 4 (printed pages 10-13), including the complete derivation through Eq. (6) on printed page 12, was read. It uses Gibbs assignment marginals for the sequential reference law and averages random orders. Eq. (6) is precisely the permanent upper bound with a row suffix-log-mass expectation. Conditioning independent priorities and applying Jensen as above turns that expectation into -n+sum scalar g(b). Its later universal row-maximization result is not needed by this derivation, so no computer certificate in its section 5 is imported.

There is a support nuance in directly applying the old sequential-law description to zero entries: a greedy history outside Gibbs support can run into a zero reference denominator. The submitted conditional-chain proof avoids defining those histories; every history it consumes has a positive available Gibbs-marginal entry. Alternatively one could add a failure state to the old procedure. This nuance does not invalidate the submitted self-contained entropy proof.

Fresh arXiv:2608.28031v2, section 4, printed pages 9-10, Lemma 7 and its full proof were read and visually checked. Its explicit positive-A scope prevents zero denominators and it retains the sequential KL quantity exactly. Its vector function named g is different from the submitted scalar g. Discarding its nonnegative sequential KL gives the same random-order expectation comparison; it supplies no proof of the scalar absorption or original input Frobenius bound. Full-text Frobenius occurrences concern optimization geometry. These bounded reads verify a close prior mechanism and fail to certify novelty, priority, or current open status. The original lower bound and the Gibbs-marginal/random-order mechanism must remain credited.

## Frozen early verdict

No mathematical counterexample or missing step was found in the submitted scalar-to-Frobenius argument after checking the entropy interface directly. All-n and source scope are correctly qualified in PROOF. Independent numerical controls and consistency with the remaining eight submitted files are still pending. No acceptance labels, historical audit results, or omitted historical code are evidence for this verdict.
