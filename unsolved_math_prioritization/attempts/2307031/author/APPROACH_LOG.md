# Five substantive approaches

Dates are UTC on 2026-10-05. Percentage estimates describe progress on
the broad classification, not probability that a proof is correct.
Source triage and finite replay do not count as additional proof attempts.
No more than the five approaches below are claimed.

## 1  Pointwise comparison and sparse controls

Checkpoint 07:19 UTC. Mechanism: compare c_n/a_n directly with n^2, testing
the bound on delayed mass before using a termwise convergence argument.
Exact result: a_1=1, a_N=N and zeros elsewhere give c_N/a_N=2 at any
prescribed N>=2. The hoped-for uniform pointwise quadratic lower bound
fails. This route cannot prove the full comparison. Completion estimate
10 percent. The control is retained in PROOFS.md and verify.py.

## 2  Factorization and a first-order summability transfer

Checkpoint 07:22 UTC. Mechanism: factor c_n/a_n into b_n/a_n and c_n/b_n,
then try to iterate the first-order convergence theorem cited by the source.
Exact obstruction: a_1=1 and a_{2*3^(j-1)}=2*3^(j-1) make b_n/a_n=3/2
at infinitely many active indices. Thus the first factor can defeat every
positive test at 3/2. The source's result for c_n/b_n cannot simply be
applied to b_n/a_n. No claim that the cited theorem itself is false.
Completion estimate 10 percent; route blocked as a full proof.

## 3  Global sublevel counting by a normalized potential

Checkpoint 07:25 UTC. Mechanism: for a fixed threshold T=m^2, use
P_n=(c_n+m b_n)/(n+m). It is nondecreasing, increases by at least
1+1/(2m) at every good index n>=m, and is at most m^2(1+m) at a good
index. This proves a uniform O_{a_1}(sqrt(T) log T) global count.
Dyadic summation then proves a weighted integral sufficient condition,
including t^(-1/2)(log(e+t))^(-p) for p>2. This goes beyond fixed powers.
Exact gap: necessity or removal of the logarithmic weight is not proved.
Completion estimate 35 percent.

## 4  Inverse design of exact constant-ratio blocks

Checkpoint 07:26 UTC. Mechanism: prescribe c_n/a_n=m^2 and solve the
second-order positive recurrence for a_n. The eigenquantity c_n+m b_n
has exact multiplier m/(m-1). Choosing the initial scale relative to the
old mass proves a_n<=n throughout a block. For a_1=1, single blocks have
order m log m terms, proving the logarithm in the uniform counting bound
cannot be deleted. This is a finite extremal construction, not yet one
infinite counterexample. Completion estimate 45 percent.

## 5  Infinite concatenation and a positive Laplace mixture

Checkpoint 07:29 UTC. Mechanism: concatenate blocks of lengths 2^j m_j
at ratios m_j^2, then choose the single entire function
f(z)=sum 2^(-j)m_j^(-1)exp(-z/m_j^2). A Gaussian integral makes the
comparison series summable, while each block contributes at least 1/e
to the double-sum series. Local uniform convergence of all derivatives
proves strict complete monotonicity on the positive ray. This gives a
complete negative result under several strong smoothness conditions.
Completion estimate 55 percent for the broad problem: the full class of
admissible f and stronger shape restrictions remain unresolved.

## Final bounded outcome

Five of five approaches used. Complete proofs of the subresults are frozen
for independent challenge. No sixth search approach was used. Exact finite
controls are corroboration and error detection, not a substitute for the
infinite proofs. Recommend retaining the broad target as exhausted/partial.
