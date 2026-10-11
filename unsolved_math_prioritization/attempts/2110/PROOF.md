# Density-one distinct consecutive products: credited reconstruction

## Identity, credit, and status

This addresses problem ID 2110 / EP-421: construct an increasing positive-integer sequence of natural density one whose products over all nonempty consecutive blocks are pairwise distinct. Erdős–Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed p.84, asks exactly this question: https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf.

The construction, canonical witnesses, split-product argument and parent-gap organization below are due to Przemek Chojecki's *Distinct Consecutive Products*, dated 13 July 2026, https://ulam.ai/research/erdos421-sol.pdf. The manuscript explicitly credits GPT-5.6 Sol for the proof. It is a public AI-assisted manuscript; no peer-reviewed publication, human review, or independent scholarly acceptance is asserted here. This is a fully written, credited reconstruction, not a novelty claim. The accompanying audit and acceptance report concern this authored reconstruction only.

We replace the manuscript's newer prime-interval input by Jia's published 1996 theorem, change the cutoff exponent, and write an elementary one-step recurrence in place of its multiscale forest sum. This gives weaker quantitative loss but the same density-one conclusion. These changes are expository dependency/verification choices, not a claim of a new mathematical result.

## External theorems used

1. C. Jia, *Almost all short intervals containing prime numbers*, Acta Arithmetica 76 (1996), 21–84, first-page theorem: for sufficiently small fixed epsilon>0 and sufficiently large B, all but O(X(log X)^(-B)) integers n in (X,2X) have a prime in (n,n+n^(1/20+epsilon)). Primary PDF: https://matwbn.icm.edu.pl/ksiazki/aa/aa76/aa7613.pdf. We need only an exponent eta strictly between 1/20 and 3/50. The theorem statement and its quantifiers were inspected. This reconstruction does not reprove the 64-page sieve theorem.
2. W. Castryck, R. Cluckers, P. Dittmann and K. H. Nguyen, *The dimension growth conjecture, polynomial in the degree and without logarithmic factors*, Algebra & Number Theory 14 (2020), 2261–2294, Theorem 3 (printed p.2264): a geometrically integral affine plane curve of degree d has at most C d^3 X^(1/d)(log X+d) integer points in [-X,X]^2, with absolute C independent of its coefficients. Primary PDF: https://msp.org/ant/2020/14-8/ant-v14-n8-p09-s.pdf. The displayed uniform degree dependence was inspected. This reconstruction invokes, rather than reproves, this published determinant-method theorem.
3. Bertrand's postulate and the elementary plane-curve Bezout inequality. The short polynomial-factor argument using weighted degrees is proved below.

Fix theta=3/50, rho=1/(2-theta)=50/97, and alpha=93/100. Fix eta=1/20+epsilon<theta allowed by Jia, and B>2 as large as required there. Implied constants below are fixed and do not depend on X or on any selected gap.

## 1. The stable construction and witnesses

Start with A_2={2}. Given consecutive primes p<q and a collision-free set A_p contained in [2,p], test B=A_p union {p+1,...,q}. If its consecutive-block products are distinct, put A_q=B; otherwise put A_q=A_p union {q}. Let A be the union of these nested finite sets. Thus every prime is retained and each open prime gap is either wholly retained or wholly rejected.

Any equality of two distinct block products can be canceled on the overlap. If one block contains the other, this leaves a nonempty product equal to 1, impossible because all entries are at least 2. Otherwise it leaves separated blocks E,R with every element of E smaller than every element of R. A prime r in R would divide the product of E, impossible since every element of E is smaller than r. Thus R contains no prime.

A new collision when processing (p,q) must have R inside (p,q): if R were in A_p, so would E; and if R crossed from the old prefix to the new portion, it would contain p. Hence R is a full integer interval [m,n] inside (p,q). E cannot cross the boundary p: then p would divide the product of [m,n], whereas Bertrand gives q<2p, so none of those integers is divisible by p. Consequently E is either a consecutive block of A_p, or a full interval inside (p,q). Writing r=|E| and s=n-m+1, product equality forces r>s, since every factor on the earlier side is strictly smaller.

If the tentative gap is rejected, adjoining q alone cannot introduce a collision, since any new later block contains the prime q. This proves by induction that every A_p, and therefore A, is collision-free.

For each rejected gap choose a witness product(E)=product_{t=m}^n t as above. Call a rejected gap raw if it admits such a witness whose earlier block E crosses no prior rejected gap. (Crossing (p,q) means containing both boundary primes p,q.) Choose a raw witness for raw gaps. Then E is a full integer interval: the only possible holes in the established prefix are whole rejected gap interiors, and any hole inside a block would force it to cross that gap. For every nonraw gap choose one witnessed prior rejected gap crossed by E as its parent. Its right endpoint is smaller than the child's, so the resulting directed graph is a forest and every backward path terminates at a raw gap.

## 2. Long gaps occupy o(X) integers

A prime gap (p,q) is short if g=q-p<=p^theta and long otherwise. For p in [Y,2Y], Bertrand confines q to [Y,4Y]. If g>p^theta, all but O(Y^eta+1) integer starting points a inside this gap have (a,a+a^eta) entirely within it and thus contain no prime. Since eta<theta, for large Y this accounts for at least g/2 starting points. Different gap interiors give disjoint starting points. Jia's theorem on [Y,2Y] and [2Y,4Y] implies

sum_{Y<=p<2Y, q-p>p^theta}(q-p) = O(Y(log Y)^(-B)).

Summing dyadically for p<=X gives o(X). For clarity, gaps beginning below X^(1/2) have total length O(X^(1/2)), while for the others log Y is comparable with log X, and the sum of the dyadic Y is O(X). Boundary integer choices and the finitely many small gaps are harmless. This proves the asserted long-gap estimate without using Li's 2025 preprint.

## 3. Uniform counting of raw short gaps

Let r>s>=1, h=gcd(r,s), u=r/h, v=s/h; then u>v, gcd(u,v)=1, and u>=2. Consider

F(X,Y)=product_{i=1}^r(X-a_i)-product_{j=1}^s(Y+b_j)

with integer shifts. Give X weight v and Y weight u. The highest weighted part is X^r-Y^s, a product of the h distinct irreducible binomials X^u-zeta Y^v over C, with zeta^h=1. Irreducibility of each binomial follows from coprimality of u,v (equivalently its primitive lattice exponent difference).

For any absolute irreducible factor H of F, multiplicativity of weighted initial forms and the squarefreeness just noted imply that its initial form is a nonzero constant times a product of e>=1 distinct such binomials. It contains X^(ue), while every monomial X^iY^j of H satisfies vi+uj<=uve. As u>v, i+j<=ue. Therefore deg H=ue>=u>=2.

Absolute components defined over Q satisfy the curve theorem stated above. A rational point on a component not defined over Q lies on one of its distinct Galois conjugates as well. Bezout bounds the total of these exceptional rational points by O(r^2), after summing the component-degree products. The sum of all component degrees is r, so the sums of their cubes and fourth powers are at most r^3 and r^4. Thus uniformly in the shifts,

#{(x,y) in Z^2 intersect [-X,X]^2:F(x,y)=0}
  <= C X^(1/2)(r^3 log X+r^4).

For a raw short rejected gap ending at most X, both witness blocks are full numerical intervals. They have the form product_{i=0}^{r-1}(x-i)=product_{j=0}^{s-1}(y+j), with x,y<=X and r>s. Shortness gives s<=X^theta. Because every earlier entry is at least 2 and every later entry is at most X, 2^r<=X^s, so r<=L=ceil(X^theta log_2(2X)). Summing the preceding curve estimate over s<r<=L gives

R(X) <= C X^(1/2)(L^5 log X+L^6)
     <= C X^(1/2+6theta)(log(2X))^6.

Here R(X) counts raw short rejected gaps. Each right-side numerical interval belongs to at most one prime gap, so counting witnesses bounds the number of gaps.

## 4. Parent edges and their quantitative bounds

Suppose the parent is (p,q), g=q-p, and a child is rejected with right-side witness [m,n] of length s. Since p,q are both in E, there are integers a,b>=2 with ap,bq in [m,n]. Classify the edge as equal if some common multiplier j>=2 satisfies jp,jq in [m,n]. Otherwise it is unequal. For an unequal edge choose any such a,b; then a!=b and |ap-bq|<=s-1.

If a>b, write ap-bq=(a-b)p-bg. Since b<=n/p, this yields p<=ng/p+s. If a<b, bq-ap=(b-a)p+bg>=p, yielding p<=s. In both cases

p^2 <= ng+ps.                                             (1)

Four consequences hold for children with right endpoint at most X:

(a) A fixed parent has at most C X^(3theta)(log(2X))^2 short children. Indeed s<=X^theta and r=|E|<=L above. The endpoints p,q remain consecutive in the final A. For each r there are at most r-1 consecutive r-blocks of A crossing that adjacency. For each such E and each s, the strictly increasing function m -> product_{i=0}^{s-1}(m+i) permits at most one m. Its interval determines at most one child gap. Summing r and s proves the bound. Stability of the construction is essential to counting in this single final A.

(b) For an unequal edge with short parent and short child, the parent right endpoint is at most C X^rho. In (1), n<=X, s<=X^theta, g<=p^theta. If p<=2X^theta this is immediate. Otherwise ps<=p^2/2, giving p^(2-theta)<=2X; Bertrand transfers the bound to q.

(c) The number of long parents of unequal edges to short children ending at most X is at most C X^(1-rho)log(2X). For p<=2X^theta, simply count integers; theta<1-rho. Otherwise (1) implies g>=p^2/(2X), while longness gives g>p^theta. On a dyadic scale p comparable with P, disjoint prime gaps lie in an interval of length O(P), so the count is at most C min(P^(1-theta),X/P). The two expressions meet at P=X^rho and their common value is X^(1-rho). There are O(log X) scales.

(d) An equal edge cannot join a long parent to a short child. If the child is (P,Q), then P<jp<jq<Q, so Q-P>j(q-p). Were q-p>p^theta, we would get Q-P>jp^theta=j^(1-theta)(jp)^theta>P^theta, contradicting shortness.

## 5. Compress equal chains and close a single recurrence

Fix a rejected gap (p,q) of length g. For any path of equal edges, multiplying their integer multipliers gives J, and the terminal prime gap contains both Jp and Jq. This follows inductively: if the intermediate gap contains Jp,Jq, the next equal edge contains multiples of its endpoints and hence these two multiplied interior points as well. For fixed J, there is at most one prime gap containing Jp,Jq. If the terminal gap is short and ends at most X, its length exceeds Jg but is at most X^theta. Thus the number of endpoints reachable by only equal edges is at most floor(X^theta/g); including the starting vertex bounds its equal-chain closure by 1+X^theta <= 2X^theta for X>=1.

Let N(X) be the number of short rejected gaps ending at most X. Trace any such gap backward through its last equal-edge chain until its root w. By (d), all vertices in that chain are short. Either w is raw, or w has an unequal edge from a parent. In the second case the parent is short with right endpoint at most C X^rho by (b), or is one of the long parents counted by (c). Combine the raw estimate, the branch bound (a), and the equal-chain closure to obtain, with one fixed C and log(2X) abbreviated by l,

N(X) <= C X^(1/2+7theta)l^6
      + C X^(4theta)l^2 N(C X^rho)
      + C X^(1-rho+4theta)l^3.                            (2)

No claim about independent branch choices or a variable-depth product is needed. Every terminal vertex is covered by one of these three cases; overcounting is harmless.

We now prove N(X)=O(X^alpha) with alpha=93/100. The strict inequalities required are

1/2+7theta = 23/25 = 0.92 < alpha,
4theta+rho*alpha = 3489/4850 < alpha,
1-rho+4theta = 1757/2425 < alpha,
rho<1.

For sufficiently large X, C X^rho<X. Choose a fixed threshold so that the first and third terms of (2), divided by X^alpha, have sum at most 1/2, and C X^(4theta)l^2 (C X^rho)^alpha/X^alpha <=1/2. This is possible because the displayed exponent gaps are positive. Take K>=1 large enough that N(t)<=K t^alpha below that threshold. Strong induction on integer X, using monotonicity to replace C X^rho by its ceiling and enlarging constants, gives N(X)<=K X^alpha. More explicitly the first and third terms cost at most K X^alpha/2, and the recursive term at most K X^alpha/2. This also proves the assertion for real X by taking integer parts.

Each short gap ending at most X has length at most X^theta, so their total rejected length is O(X^(alpha+theta))=O(X^(99/100))=o(X).

## 6. Density and conclusion

A prime gap meeting [1,X] has left endpoint at most X and right endpoint at most 2X by Bertrand. The total removed integers up to X are at most 1 plus the total lengths of the rejected short gaps ending at most 2X and all long gaps beginning at most X. Sections 2 and 5 give o(X) for each part. Thus |A intersect [1,X]|/X tends to one. Section 1 proves all nonempty consecutive-block products in its increasing enumeration are distinct. This completes the exact-target affirmative proof, subject only to the explicitly stated standard/published external theorems.

## Audit boundaries

This is a proof reconstruction, not a finite-experiment inference. It neither depends on running source-author code nor on accepting a claimed Lean artifact. Source theorem statements were read, but their full 34-page determinant-method and 64-page sieve proofs have not been re-audited here. The reconstruction does not certify every sentence or the sharper 9/10 exponent in Chojecki's manuscript. The accompanying independent computational-assistant audit accepts this authored reconstruction as a complete analytic proof using the stated published and standard theorems. This is not a claim of human review, peer review, or external scholarly acceptance. All authors and prior sources retain credit.
