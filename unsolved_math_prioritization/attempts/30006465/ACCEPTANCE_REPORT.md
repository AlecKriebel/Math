# Independent prior-proof audit: signed representatives

Problem: rank 1214; database ID 30006465; corpus ID OWR-14299577-018.

Audit date: 10 October 2026 (UTC).

## Verdict

**Accept the mathematical proofs of Theorems 1.1 and 1.2 in Alper Ferudun's 28 September 2026 note.** They answer both questions of Christian Bernert and Nuno Arala Santos in the 2025 Oberwolfach problem session, with the exact signed-representative hypothesis and the original ordered-pair count. The full five-page note was read, and all five PDF pages were visually inspected. The two main proof pages and the original problem page were inspected at enlarged resolution.

No proof correction is required. This is an independent mathematical acceptance audit of an existing public argument, rather than a new solution or a claim of priority. The note explicitly describes itself as unrefereed and discloses AI assistance. Acceptance here records the outcome of this audit; it does not confer journal peer-review status.

New-proof-search turns used: **0**.

The accepted conclusions are:

1. For every integer n >= 1 and every A containing exactly one of k and -k for each 1 <= k <= n, at most two integers in [1,n] fail to belong to A-A.
2. For every such A and every B subset of [1,n], including B empty, the number of ordered pairs (a,b) in A squared with a-b in B is at least floor((|B|-1)^2/4).
3. The first bound is attained for every n >= 2. The second is attained, for each n >= 2, for every integer 1 <= m <= floor(2n/3)+1 with |B|=m.
4. For every fixed 0 < epsilon <= 1, the original positive-density ordered-pair question has an affirmative asymptotic answer. For n > 2/epsilon, the explicit lower bound epsilon^2 n^2/9 works. The leading coefficient 1/4 in the expression epsilon^2 n^2 is optimal when 0 < epsilon <= 2/3.

Theorem 1.2 does not claim that its bound is the exact minimum for every possible (n,m). The note's suggested all-n characterization of pairs of missing differences remains unproved there. These limitations do not affect either original question.

## 1. Source identity and exact target

The primary question is printed on page 2756 of Oberwolfach Report 51/2025, PDF page 56, in the problem-session summary compiled by Thomas F. Bloom. The assumptions are A subset of {-n,...,n} excluding zero, |A|=n, and at least one member of each pair {k,-k} lies in A. Since the n pairs are disjoint and A has n elements, this is equivalent to **exactly one** member of each pair. There is no stronger assumption in Ferudun's note.

The first question asks whether |(A-A) intersect [1,n]|=(1-o(1))n. The second counts the sum over a,b in A of the indicator of a-b in B, for B subset of [1,n] and |B| >= epsilon n. This is an ordered-pair count. The alternative pairing {k,1-k}, for which the source describes a congruence obstruction, is a different problem and is outside the accepted result.

The audited note is:

Alper Ferudun, *Differences of Signed Representatives: Sharp Answers to Two Questions of Bernert and Arala Santos*, 28 September 2026, version 1.0, Zenodo DOI [10.5281/zenodo.23006720](https://doi.org/10.5281/zenodo.23006720).

The audited PDF has 92,822 bytes and SHA-256 25a5474f26518179b2b2a8db952868e6689c89adcdbc1a05156aa85cbbdd43ca. Its MD5 agrees with the exact PDF entry in the public Zenodo record. The public metadata and note both identify it as an unrefereed preprint. The original OWR PDF has 569,251 bytes and SHA-256 0ab42f4636cc8f6fb9d3165313c5501ceef1a521f4ecb9a981e022fb68d0f4e1.

Source URLs, original retrieval timestamps, byte checks and inspection history are recorded in SOURCE_LEDGER.md. The audit used previously retrieved public-source bytes; preparation of this edition did not retrieve new source copies.

## 2. Lemma 2.1: involution and the factor of two

Put I={-n,...,-1,1,...,n}. Define g(x)=1 for x in A and g(x)=-1 for x in I outside A. The exact sign condition is equivalent to g(-x)=-g(x).

For a positive d <= n, let I_d consist of x such that both x and x+d lie in I. Let D_d consist of those x in I_d for which g(x)=g(x+d). Write r(d) for the number of ordered pairs (a,b) in A squared with a-b=d.

The proposed map mu_d(x)=-x-d has the following properties, all verified directly:

- If x and x+d belong to I, then their negatives belong to I, so mu_d(x) and mu_d(x)+d belong to I.
- Applying mu_d twice gives x.
- Oddness gives g(mu_d(x))=-g(x+d) and g(mu_d(x)+d)=-g(x). Hence mu_d preserves D_d and exchanges its two sign types, ++ and --.
- A ++ defect x gives exactly the ordered pair (x+d,x) in A squared. The correspondence is bijective. Therefore there are r(d) ++ defects, r(d) -- defects, and 2r(d) total defects.
- A fixed point would require x=-d/2. When d is odd this is not an integer. When d is even, x and x+d are opposite nonzero integers and their g values are opposite. Thus no fixed point belongs to D_d.

The domain I_d is the disjoint union of the integer intervals [1,n-d], [-n,-d-1], and [1-d,-1]. The first two intervals are exchanged by mu_d. The middle interval maps to itself; its two strict halves (-d/2,0) and (-d,-d/2) are exchanged. The only possible midpoint is not a defect, as just checked.

Consequently the set

T_d = (D_d intersect [1,n-d]) union (D_d intersect (-d/2,0))

contains exactly one representative from every mu_d orbit of defects. In particular |T_d|=r(d). This verifies the precise counting budget used later. Charging into all of D_d would give only a weaker factor, but the manuscript charges into T_d, so its stated factor is correct.

All endpoint conventions are correct: x=0 and x=-d are excluded by I_d; when d=n the positive outer interval is empty; when d=1 the middle interval is empty. Empty intervals cause no exception. For n=d=1, I_d is empty and r(d)=0, as required.

## 3. Lemma 2.2 and injective charging

Let 1 <= d < e <= n have the same parity and set j=(e-d)/2. Then j is a positive integer and

j+d=e-j=(d+e)/2.

The common value is a positive integer at most n. It follows that 1 <= j <= n-d. Also 0 < j < e/2, because d>0. Thus j is eligible for the positive part of T_d and -j is eligible for the strict negative part of T_e.

The two defect conditions are

g(j)=g(j+d), and -g(j)=g(j+d),

respectively. Since the values of g are exactly +1 and -1, precisely one condition holds. Therefore each pair {d,e} of equal-parity differences supplies exactly one charge: (d,j) or (e,-j).

The charge map is injective, including across its two cases:

- A positive second coordinate x in a charge (delta,x) determines the unique original pair {delta,delta+2x}.
- A negative second coordinate x determines the unique original pair {delta+2x,delta}.
- A charge from the first case cannot coincide with one from the second case, because their second coordinates have opposite signs.

For a fixed first coordinate delta, every charge belongs to T_delta, whose cardinality is r(delta). Restricting to the pairs in any equal-parity subset S therefore gives

sum over d in S of r(d) >= |S|(|S|-1)/2.

This proves Proposition 1.3 exactly as needed, for arbitrary n and arbitrary S. S empty or of size one gives the valid lower bound zero. There is no hidden asymptotic assumption or dependence on a finite computation.

## 4. The two lower bounds

If three positive differences were missing, two would have equal parity. Applying Proposition 1.3 to those two differences forces their combined representation count to be at least one, contradicting that both vanish. Thus at most two positive differences are missing. Equivalently the coverage is at least n-2; its sharper nonnegative formulation is max(0,n-2).

For B, let its odd and even parts have sizes b_1 and b_2, with m=b_1+b_2. Proposition 1.3 applied separately gives

sum over d in B of r(d) >= b_1(b_1-1)/2 + b_2(b_2-1)/2.

The right side is minimized when the two nonnegative integers b_1 and b_2 differ by at most one. For m=2c it is c(c-1), and for m=2c+1 it is c^2. These are exactly floor((m-1)^2/4). The same formula gives zero at m=0,1,2. Thus the empty-set case and the small cases are included, without extending a positive quadratic assertion beyond its legitimate range.

The left side is the original ordered-pair sum: each (a,b) with positive difference in B contributes to exactly one r(d). Diagonal pairs and negatively oriented pairs do not contribute because B is positive. No additional factor of two is required.

## 5. Proposition 3.1 and all-n sharpness construction

Fix an integer a with n/2 <= a <= n-1, for n>=2, and take

A_a = {1,...,a} union {-(a+1),...,-n}.

The direct ordered-pair count for d in [1,n] is

r(d)=max(a-d,0)+max(n-a-d,0)+max(d-a-1,0).

The first two terms count pairs within the two consecutive blocks. For a positive-minus-negative pair, write d=x+z with 1<=x<=a and a+1<=z<=n. If d>=a+2, the admissible z are exactly a+1,...,d-1. The restriction d<=n ensures the upper bound on z, and d<=n<=2a+1 ensures x<=a. This gives the third term. The reversed cross-block orientation has negative difference and contributes nothing.

Splitting the formula at n-a and a+1 yields the manuscript's three pieces:

- r(d)=n-2d for 1<=d<=n-a-1;
- r(d)=a-d for n-a<=d<=a;
- r(d)=d-a-1 for a+1<=d<=n.

The ordering of the breakpoints follows from 2a>=n. The initial interval may be empty, which causes no problem. On that interval the smallest possible value is 2a-n+2>0. On the other intervals the only zeros are d=a and d=a+1. Both are in [1,n]. Thus exactly two differences are missing, proving sharpness of Theorem 1.1 for every n>=2.

For the representation bound, write L=2a-n and R=n-a-1. On the middle and last intervals the representation values run through 0,...,L and 0,...,R, respectively. On the initial interval every value is at least L+2. Consequently, with q=min(L,R), the first 2q+2 entries of the nondecreasing list of representation counts are exactly

0,0,1,1,...,q,q.

Their initial m-term sum is floor((m-1)^2/4), so taking B to be the corresponding differences realizes equality for all m<=2q+2.

For the claimed range, divide n-2=3t+rho with rho in {0,1,2}, and set a=n-1-t. Then n=3t+rho+2, a=2t+rho+1, L=t+rho and R=t. In particular a>=n/2 and a<=n-1, and q=t. Equality follows up to m=2t+2.

If rho>=1, the middle interval has one further value t+1, located at d=a-t-1. Indeed d= t+rho and n-a=t+1, so that d is in the middle interval. The last interval stops at t, and the initial interval starts at values at least t+rho+2. Hence the next smallest value is t+1. The sum through m=2t+3 is t(t+1)+(t+1)=(t+1)^2, precisely the bound for that m.

Finally floor(2n/3)+1 equals 2t+2 when rho=0 and 2t+3 when rho=1 or 2. This verifies all three residue classes and the endpoints n=2,3,4. The printed equality construction is correct for every stated n and m.

## 6. Asymptotic interpretation and scope of optimality

The coverage assertion gives n-2 <= |(A-A) intersect [1,n]| <= n, hence an affirmative answer to the first original question, uniformly over all signed sets.

For the second, let 0<epsilon<=1 be fixed and m=|B|>=epsilon n. Once n>2/epsilon, m>=3. The integer inequality

floor((m-1)^2/4) >= m^2/9, for all m>=3,

holds by separately substituting m=2c and m=2c+1. In the even case it reduces to c(5c-9)>=0 for c>=2; in the odd case it reduces to (5c+1)(c-1)>=0 for c>=1. Therefore epsilon^2/9 is an explicit admissible implicit constant. Similarly m>=4 gives the note's m^2/8 estimate.

The leading form is (1/4-o(1))epsilon^2 n^2. For every fixed 0<epsilon<=2/3, choose m=ceil(epsilon n). This m lies in the proved equality range for all sufficiently large n (in fact its upper-end inequality holds for every n). The construction then has exactly floor((m-1)^2/4) counted pairs, whose ratio to epsilon^2 n^2 tends to 1/4. This verifies the claimed optimal leading coefficient in that epsilon range.

There is no valid strictly positive lower bound c_epsilon n^2 for every small n. For example, n=2 and A={1,-2} miss both positive differences 1 and 2. Taking B={1,2} gives zero. At n=1 every admissible A is a singleton and the only positive difference is missing. These cases satisfy the finite theorems and require the asymptotic reading of the original question.

The equality construction establishes sufficiency of m<=floor(2n/3)+1. Necessity of that cutoff for every n is not proved in the note. Likewise its proposed coprimality/sum characterization and uniqueness of two-missing-difference sets are explicitly unproved remarks. Neither is used in the accepted proof. This audit makes no additional all-n claim about them.

## 7. Disposition

Recommended mathematical disposition: **existing public resolution validated; credit Ferudun, 28 September 2026**. Both original questions are covered. No correction patch and no new proof-search turn are warranted.

Preserve the distinctions among a verified elementary proof, an unrefereed manuscript's public status, unproved ancillary conjectures, and a claim of bibliographic priority. This audit establishes the first and records the others without upgrading them.

## Public references

- [Original OWR report, printed p. 2756 / PDF p. 56](https://ems.press/content/serial-article-files/52435), DOI [10.4171/OWR/2025/51](https://doi.org/10.4171/OWR/2025/51).
- [Ferudun, Zenodo record 23006720](https://doi.org/10.5281/zenodo.23006720), manuscript dated 28 September 2026.
- [Exact deposited manuscript PDF](https://zenodo.org/api/records/23006720/files/OWR-14299577-018-paper.pdf/content).
