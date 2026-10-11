# Substantive turn 5: Poissonization, a pointwise-transfer obstruction, and branching

## Aim and outcome

The final author route tried to estimate zeros in an independent-cycle model and then transfer an averaged result to the source's fixed-n uniform table. It gives precise conditioning losses, a rigorous countercontrol showing that even a diagonal grand-canonical limit would not determine the pointwise limit, a sufficient local regularity condition, and exact branching support bounds. None supplies the required asymptotic regularity or residual-zero estimate. The original problem remains unresolved after five substantive turns.

The partition asymptotic and branching inputs are classical, and the current strongest zero-type theorem remains credited to Peluse–Soundararajan. No general zero-density theorem or historical novelty is asserted here.

## 1. Independent geometric counts and the exact conditioning cost

For 0<q<1 put F(q)=product_(j>=1)(1-q^j)^(-1). The probability measure on all partitions assigning weight q^(|mu|)/F(q) makes the multiplicities of the parts independent geometric variables. Conditional on |mu|=n it is exactly uniform among partitions of n. This identity is valid, but the conditioning cannot be dropped.

Set c=pi/sqrt(6), q_n=exp(-c/sqrt(n)). The saddle-point form of the Hardy–Ramanujan estimate, also recorded as equation(9) in Peluse–Soundararajan2026, gives

alpha_n:=Pr_(q_n)(|mu|=n)=p(n)q_n^n/F(q_n)
        ~1/[2*6^(1/4)n^(3/4)].                            (1)

Consequently, an exceptional event of unconditioned probability epsilon_n has conditioned probability at most epsilon_n/alpha_n. To transfer an unconditioned o(1) estimate by this inequality requires epsilon_n=o(n^(-3/4)). For two independent Boltzmann partitions conditioned separately to size n, the sufficient loss is order n^(3/2). These are sufficient error requirements for this elementary transfer, not an assertion that all more refined conditioning methods suffer exactly this loss.

The obstruction is real at the level of logic: the event {|mu|=n} itself has unconditioned probability tending to zero and conditioned probability one. Independence of cycle counts before conditioning is therefore not an anti-concentration proof after conditioning.

Moreover, if two independent Boltzmann partitions are used and a character-zero event is defined only when their sizes agree, its unconditional probability tends to zero even if every same-size pair is declared a zero. Indeed it is bounded by Pr(|lambda|=|mu|). The largest atom of the Boltzmann size law is O((1-q)^(3/2)) by the same partition saddle estimate, and the coincidence probability is at most that largest atom. This would be a vacuous “zero-density” argument for the fixed-size problem.

## 2. Even conditioning on equal sizes gives only a weighted average

Let P_m be any sequence in[0,1], interpreted for the application as the uniform character-table zero proportion. Conditional on the two Boltzmann sizes agreeing, the relevant average is

A(q) = [sum_(m>=1) p(m)^2 P_m q^(2m)] /
       [sum_(m>=1) p(m)^2 q^(2m)].                        (2)

If P_m tends to zero then A(q) tends to zero as q tends to1: first separate finitely many small m, whose normalized mass vanishes, and then bound the tail by sup_(m large)P_m. The converse needs an additional hypothesis.

Here is a fully quantified countercontrol. Let P_m be1 if m is a power of2 and0 otherwise. This sequence has infinitely many values1 and does not tend to zero, while A(q) tends to zero.

To prove this, write q=e^(-t) and n0=(c/t)^2. The Hardy–Ramanujan formula gives weights

p(m)^2 e^(-2tm) ~ [1/(48m²)] exp(4c sqrt(m)-2tm).

The exponential part satisfies the exact identity

4c sqrt(m)-2tm-2c²/t = -2t(sqrt(m)-sqrt(n0))².             (3)

For m in[n0/2,2n0], the polynomial amplitude is comparable to n0^(-2), and(3) is a Gaussian-scale bound with width n0^(3/4). There are a positive multiple of n0^(3/4) integers in a fixed such central window with weights comparable to the maximum. Thus the maximum normalized weight is O(n0^(-3/4)). Outside[n0/2,2n0] the total normalized weight is bounded by a polynomial in n0 times exp(-a sqrt(n0)) for an absolute a>0: on the lower range use(3) and at most O(n0) terms; on the upper range its quadratic-in-sqrt(m) decay is bounded by an integrable exponential tail. Fixed small m are likewise exponentially negligible. Hardy–Ramanujan asymptotics can be bounded above and below by fixed constants once m is large, so these estimates are uniform and require no unproved local limit theorem.

The interval[n0/2,2n0] contains at most three powers of2. Their combined normalized weight is O(n0^(-3/4)), and the remaining powers lie in the negligible tails. This proves the claimed countercontrol. It is an abstract bounded sequence, not a claim that actual character-zero proportions have such spikes.

## 3. A sufficient pointwise-transfer condition

The same estimates show that, for any fixed a>0, a positive amount of the weight in(2) at q_n is carried by |m-n|<=a n^(3/4). Therefore the following one-sided local regularity would suffice:

eta_n := sup_(|m-n|<=a n^(3/4)) (P_n-P_m)_+ ->0.           (4)

If A(q_n)->0 and(4) holds, then

A(q_n)>=c_a(P_n-eta_n)

for some constant c_a>0 and all sufficiently large n. Hence P_n->0. This gives an exact additional target for de-Poissonization. Neither(4) nor a suitable averaged residual-zero estimate is proved in this packet.

## 4. What ordinary branching does and does not give

To test(4), let B_n denote the number of nonzero pairs(lambda,mu) in the n-th table. Let C_(n+1) count nonzero pairs at size n+1 whose cycle partition has at least one unit part. Removing one unit part identifies those columns with all partitions mu of n.

The ordinary multiplicity-free branching rule gives

chi_Lambda(mu union1)=sum_(lambda covered by Lambda) chi_lambda(mu).

Thus a nonzero value on the left requires at least one nonzero term. If b_n is the maximum number of addable boxes in a partition of n, this implies

C_(n+1)<=b_n B_n.                                         (5)

Conversely the induced character from lambda satisfies

sum_(Lambda covering lambda) chi_Lambda(mu union1)
 =(m_1(mu)+1) chi_lambda(mu).

This follows from the induction formula: the fixed cosets correspond to the fixed letters of a permutation of cycle type mu union1, and removing any such fixed letter leaves type mu. A nonzero right side forces at least one nonzero extension. If d_(n+1) is the maximum number of removable boxes, double counting possible preimages gives

B_n/d_(n+1)<=C_(n+1).                                     (6)

Finally the columns without unit parts number p(n+1)-p(n), so

B_n/d_(n+1)<=B_(n+1)
 <=b_n B_n+p(n+1)[p(n+1)-p(n)].                           (7)

A partition with d removable corners has d distinct positive row lengths, so d(d+1)/2<=n. Every partition has one more addable than removable corner. Hence d_n<=floor((sqrt(8n+1)-1)/2) and b_n<=d_n+1. These are exact elementary bounds.

After normalization, writing Q_n=1-P_n and r_n=p(n)/p(n+1), equation(7) becomes

r_n² Q_n/d_(n+1) <= Q_(n+1)
 <= b_n r_n² Q_n+(1-r_n).                                 (8)

Although 1-r_n tends to zero, the corner factors are of order sqrt(n). The resulting bounds do not imply the additive local regularity(4). More importantly, a zero sum in the branching rule may be cancellation among nonzero constituents, so replacing(5)–(6) by an equivalence of individual zeros is invalid. The finite n11 annihilator in turn4 is consistent with this obstruction.

## 5. Closing boundary after the required five turns

This turn identifies the precise loss in the independent-cycle route and the extra pointwise information a diagonal averaged theorem would require. It does not claim those analytic routes are impossible in principle. The missing information is now explicit in several equivalent or sufficient forms: bulk residual-zero counts beyond the known criteria; irreducible fiber anti-concentration; annihilator-frequency/fourth-moment control; or an averaged theorem together with valid pointwise transfer. None has been established here.

The final disposition is therefore unsolved after five substantive author turns, subject to separate review of the retained partial results. The known2/log n asymptotic for typesI–III is not promoted to the total zero density. No sixth author search is counted through review, source lookup, or packaging.
