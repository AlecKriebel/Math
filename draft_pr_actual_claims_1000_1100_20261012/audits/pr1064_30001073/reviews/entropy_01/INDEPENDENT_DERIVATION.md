# Independent reconstruction frozen before comparison

Review family: entropy_01. Target: PR 1064, problem 30001073, head `bdefe31b9d226c8f27008d13f57775d5de8df3d7`.

This reconstruction uses submitted `PROOF.md` as the hypothesis under audit and a fresh reading of the complete original problem on printed OWR 44/2008 pp. 2549-2550 (official EMS file 46191, PDF pages 73-74). At the freeze time, no other submitted acceptance/audit/status/provenance/source-ledger conclusions, other-family reports, or Anari-Rezaei full text have been read. The arXiv version metadata only has been retrieved. This is a proof audit, not a novelty or historical-priority certificate.

## Exact target and success criteria

For each fixed real gamma >= 1, the original problem concerns nonnegative n by n doubly stochastic matrices with the unnormalized sum S = sum(a_ij^2) <= gamma. It asks for a polynomial factor in n times exp(-n). The source already records the van der Waerden lower bound n!/n^n; the missing part is an upper bound n^{C(gamma)} exp(-n) asymptotically. The statement is not an all-n literal equality or a requirement that every entry be O(1/n). A proof of the asserted row-stochastic upper bound, with C = 3 exp(4) gamma for n >= 2, supplies the missing upper part. No lower bound follows for arbitrary row-stochastic matrices.

Assume n is a positive integer. All logarithms are natural. Define 0 log 0 = 0, h(0)=0 for h(a)=a^2 log(e/a), g(0)=0, g(1)=1 and g(b)=-b^2 log b/(1-b) for 0<b<1. The endpoint g(1)=1 follows from log b/(b-1) -> 1; g(0)=0 follows from b^2 |log b| -> 0.

## 1. Joint law and reveal histories

Let mu be any probability law supported on permutations X=(X_1,...,X_n), and let b_ij = mu[X_i=j]. B has every row and every column sum equal to 1, since each realized permutation uses each column exactly once. Independently draw T_1,...,T_n iid uniform on [0,1]. Their ordering O is a uniform random order, independent of X; ties have probability zero.

For a fixed order o and row i, the preceding-row set R is fixed. A history x_R is admitted only when mu[X_R=x_R]>0. Let q_j = mu[X_i=j | X_R=x_R]. Let S_i be the columns not used by x_R and Z_i=sum_{j in S_i} b_ij. Conditional values outside S_i have q_j=0. If q_j>0, then mu[X_R=x_R,X_i=j]>0, so b_ij>0. Because q is a probability distribution, some q_j>0, hence Z_i>0. The comparison law r_j=b_ij/Z_i on S_i is a probability law, and every positive q_j has positive r_j. Entries with q_j=0 contribute zero to relative entropy, including r_j=0 entries. Thus no log(0) is taken with a positive coefficient.

Finite-support relative entropy gives

D(q||r)=sum_j q_j log(q_j/b_ij)+log Z_i >= 0,

or H(q)+sum_j q_j log b_ij <= log Z_i. Positivity can be established directly by log u <= u-1 on the positive q support; any r mass outside that support only strengthens it.

Average over all positive histories for the fixed order. The conditional-entropy sum is H(X) by the finite chain rule. For each i the cross-entropy average is sum_j b_ij log b_ij by conditional expectation. Then average over O, obtaining

H(X)+sum_ij b_ij log b_ij <= sum_i E_{X,T}[log Z_i].       (A)

The actual priority magnitudes cause no difficulty: the comparison q above conditions on the finite order, not on zero-probability real-valued events. Because T is independent of X, the same q applies to any priority vector realizing that order. The variable Z_i is a deterministic function of X and T through the earlier rows. Every positive-probability X has b_i,X_i>0, and always Z_i>=b_i,X_i; hence log Z_i is integrable (finite support gives a positive minimum over sampled b values). This also justifies the averages and the conditional Jensen step below.

## 2. Conditional expectation and integral

Fix X=x in the positive support, and condition regularly on T_i=t. The other priorities remain independent uniforms and independent of X. As x is a permutation, each available column is either x_i itself or x_k for a unique k != i with T_k>t. Therefore

Z_i = b_i,x_i + sum_{k != i} b_i,x_k 1_{T_k>t},
E[Z_i | X=x,T_i=t] = b_i,x_i+(1-t)(1-b_i,x_i).

The last identity uses the row sum of B and bijectivity of x. No stochasticity property of A occurs here. For b=b_i,x_i>0, Jensen for the concave logarithm gives

E[log Z_i | X=x,T_i=t] <= log(1-t(1-b)).

For 0<b<1, integration in t gives

I(b) = integral_0^1 log(1-t(1-b)) dt
     = (1/(1-b)) integral_b^1 log u du
     = -1-b log b/(1-b).

For b=1, the integrand is zero and I(1)=0. Although I(0)=-1 is a harmless limit, b=0 is never sampled in this conditioning. Averaging over X_i, using P[X_i=j]=b_ij, yields

E log Z_i <= sum_{j:b_ij>0} b_ij I(b_ij)
            = -1+sum_j g(b_ij).

Substitute into (A):

H(X) <= -sum_ij b_ij log b_ij - n + sum_ij g(b_ij).        (B)

This is valid for every permutation law, including deterministic laws and sparse laws. For a deterministic permutation it is equality: H=0, all positive b=1, and sum g=n. No positive-density or independent-coordinate assumption is present; dependence among the X_i is handled by the chain rule. Independence is assumed only for X versus T and among the priorities.

## 3. Gibbs law and the divergence identity

Let A be nonnegative row-stochastic. Then 0<=a_ij<=1 and sum_ij a_ij=n. If per(A)=0, the desired positive exponential upper bounds are immediate; no Gibbs distribution or log permanent is defined in that case.

If P=per(A)>0, set mu(sigma)=prod_i a_i,sigma(i)/P. This is a probability law on the finite set of permutations. A positive b_ij implies that a positive-weight permutation contains edge (i,j); all its factors are positive, so a_ij>0. Conversely a_ij may be positive with b_ij=0 when that edge is not used in any positive-weight perfect matching.

Directly from -log mu(sigma)=log P-sum_i log a_i,sigma(i) on positive weights,

log P = H(mu)+sum_ij b_ij log a_ij.

Inserting (B) proves

log P <= -n+sum_ij g(b_ij)-D(B||A),
D(B||A)=sum_{b_ij>0} b_ij log(b_ij/a_ij).                  (C)

D is an unnormalized relative entropy: it equals n times the KL divergence between the probability distributions B/n and A/n. Total masses are both n, so

D(B||A)=sum_ij d(b_ij,a_ij),
d(b,a)=b log(b/a)-b+a.

For a>0 and b>=0 this is a times [x log x-x+1] with x=b/a, and is nonnegative; its b=0 value is a. Define d(0,0)=0. The forbidden case a=0<b never occurs. In particular zero b with positive a must retain d(0,a)=a in this entrywise splitting; deleting it would break the exact mass-cancellation identity. Column stochasticity of A is never used; B's column sums are a consequence of its permutation law. Row stochasticity of A provides its total mass, the a<=1 range, and the later S>=1 estimate.

## 4. Entrywise absorption

For 0<b<1, log(1/b)<=1/b-1 implies b log(1/b)<=1-b. It gives two useful inequalities:

 g(b)<=b,
 g(b)<=h(b)=b^2(1+log(1/b)).

For the second, log(1/b)/(1-b)<=1+log(1/b) is equivalent to b log(1/b)<=1-b. The inequalities remain true at b=0,1 by the stated limits. On (0,1], h'(b)=b(1+2 log(1/b))>0, so h is increasing; h(0)=0.

For a=0,b=0 the desired inequality is 0<=0. For a>0,b=0, g-d=-a<=0. For a,b>0 split into two exhaustive regimes:

* If b>=e^2 a, then log(b/a)>=2 and d(b,a)>=b+a>=b>=g(b), hence g-d<=0.
* If b<e^2 a, discard the nonnegative d. When b<=a, monotonicity gives g<=h(b)<=h(a)<=e^4 h(a). When b>a, b^2<e^4 a^2 and log(e/b)<=log(e/a), with both logs positive; therefore g<=h(b)<=e^4 h(a).

The b=1 endpoints are already covered by g(1)=h(1)=1. At the exact regime boundary b=e^2 a the first case applies. Thus the following holds on the complete permitted scalar domain:

g(b)-d(b,a)<=e^4 a^2 log(e/a).                           (D)

Sum (D) in (C), obtaining per(A)<=exp(-n+e^4 sum a_ij^2 log(e/a_ij)). No matrix-level inequality has been used to absorb a negative divergence; the cancellation and entrywise nonnegative d are explicit.

## 5. Frobenius reduction and dimensions

For each stochastic row, Cauchy-Schwarz yields sum_j a_ij^2>=1/n, so S>=1. Also S<=n because a_ij^2<=a_ij. Define p_ij=a_ij^2/S, a probability distribution on at most n^2 entries. Its entropy satisfies H(p)<=2 log n, with zero entries contributing zero. Since log p_ij=2 log a_ij-log S on positive entries,

sum a_ij^2 log(1/a_ij) = (S/2)(H(p)-log S)
 <= (S/2)(2 log n-log S) <= S log n.

Consequently sum h(a_ij)<=S(1+log n), and

per(A)<=exp(-n+e^4 S(1+log n)).                           (E)

If S<=gamma, replace S by gamma since its coefficient is nonnegative. For n>=2, 1+log n<=3 log n (because 2 log 2>1), yielding per(A)<=n^{3e^4 gamma}e^{-n}. At n=1, A=[1], S=1, and both unabsorbed bounds hold; a prefactor-free n^C e^{-n} bound fails because 1>e^{-1}. The source is asymptotic and the submission states this boundary. Empty n=0 matrices are outside the asserted problem.

For doubly stochastic A the source's recorded van der Waerden lower bound is n!/n^n, asymptotic to sqrt(2 pi n)e^{-n}. Combining it with the proved upper bound supplies the original polynomial-factor exponential order. This is not an independently new lower-bound result.

## 6. Polynomial necessity and falsifiable boundaries

For fixed positive integer k and n=km, block diagonal A with k blocks J_m/m is doubly stochastic, S=k, and per(A)=(m!/m^m)^k. Stirling's formula gives per(A)e^n ~ (2 pi/k)^{k/2}n^{k/2}. Thus a prefactor constant depending only on gamma cannot suffice even at gamma=1. Any polynomial exponent applicable at gamma=k must be at least k/2 in its asymptotic power; a pure all-n bound with exponent exactly k/2 may additionally fail because of its constant. This does not claim optimality of 3e^4 gamma.

Adversarial checks demanded by the proof include: per=0 row-stochastic examples; identity matrices and deterministic Gibbs laws; input-positive/marginal-zero edges; all-zero entries; n=1; arbitrary sparse permutation laws; non-column-stochastic inputs; b approaching either endpoint; b=e^2a; and normalization with S=1. All are handled deductively above. Computation may corroborate these facts for finite instances but cannot certify the universal inequalities.

## Frozen conclusion

No mathematical gap has emerged in the reconstruction. The strongest proved result is the complete asserted row-stochastic upper bound (including zero entries), hence the original fixed-gamma doubly stochastic upper target for n>=2. Prior-method comparison and consistency checks across the other submitted files remain to be done after this freeze. Novelty, first-solution status, and present worldwide open status remain outside this reconstruction.
