# Attempt 1: a self-contained reference-dependent lower bound

## Target and convention

Fix an alphabet of even size S >= 2 and observe exactly n iid draws from P. The reference Q is known. Write

R_n(Q) = inf_T sup_{P in Delta_S} E_P (T - ||P-Q||_1)^2.

This is global minimax over P with the reference held fixed. It is one natural precise meaning of the reference dependence asked about in the source; it is not risk in a shrinking neighborhood of Q.

## Easy reference

For Q=e_1, ||P-e_1||_1=2(1-p_1). The estimator 2(1-N_1/n) has risk 4p_1(1-p_1)/n <= 1/n, independently of S.

A matching lower bound is elementary. Restrict to P_0=(1/2,1/2,0,...) and P_1=(1/2+h,1/2-h,0,...), h=1/(8 sqrt(n)). Their functionals differ by 2h. Their n-sample chi-square divergence is

(1+4h^2)^n-1 <= exp(1/16)-1 <= 1/15.

Hence their total variation is at most 1/(2 sqrt(15)). The standard nearest-functional-value test converts any estimator into a test and gives max MSE >= (2h)^2(1-TV)/8. Thus R_n(e_1) is of order 1/n.

## Hard reference

Let Q=u_S and d=S/2. For z in {-1,1}^d set

p_{z,2j-1}=(1+a z_j)/S, p_{z,2j}=(1-a z_j)/S, 0<a<=1.

Every P_z has L1 distance a from u_S. Let M be the equal mixture of P_z^{otimes n}. Under U=u_S^{otimes n},

1+chi^2(M,U)
 = E_{z,z'} [1+(2a^2/S) sum_j z_j z'_j]^n
 <= cosh(2 n a^2/S)^{S/2}
 <= exp(n^2 a^4/S).

The first inequality uses (1+x)^n<=exp(nx) for x>=-1; the boundary x=-1 is harmless for n>=1. The second uses cosh(t)<=exp(t^2/2).

Choose a^4=S/(16n^2), assuming n>=sqrt(S)/4. Then chi^2<=1/15 and TV(M,U)<=1/(2sqrt(15)). A threshold at a/2 yields

R_n(u_S) >= [a^2/8] [1-1/(2sqrt(15))]
 = [1-1/(2sqrt(15))] sqrt(S)/(32n).

At n=S, R_S(e_1)<=1/S whereas R_S(u_S)>=c/sqrt(S). Thus the reference can change even the order of the minimax risk, by a factor diverging with S. The same alphabet and sample size are used.

## Attribution and limit

This is a standard paired-sign/mixture lower-bound argument from discrete identity testing, transferred to functional estimation; see [Paninski (2008)](https://sites.stat.columbia.edu/liam/research/pubs/sparse-unif-test.pdf). No novelty is claimed. The bound proves existence of strong reference dependence but is not sharp for the uniform reference. It does not classify functionals or density classes and does not determine tolerant-testing transitions. Attempt 2 pursues the sharp existing functional-estimation theory rather than claiming a full answer from this example.
