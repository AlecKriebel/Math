# Independent audit: least totient preimages, EP-51 / ID 1903

## Verdict

**ACCEPT the four mathematical statements as an unconditional partial result.**
The complete finite fibers, minimum, exact ratio, whole-fiber prime transport,
supremum/limsup statement, and positive lower relative-density bound are valid.
This is **not a solution of the least-preimage divergence problem**. No novelty,
priority, or global-record conclusion is approved. This review is an audit of
the submitted result.

The reviewed note has SHA-256
`f7d20faed9be41bc030f2d7901917b4325b257834373d7f8860a3f9c1f251167`.
Its 26-member inventory has SHA-256
`a5167ecda1c9445ed9730b7e0d9450bf5bfd7a1e423796652b59edf2e130666e`.
Hash verification authenticates
the reviewed bytes; the arguments and independent computations below supply
the mathematical audit.

Publication packaging needs a small edit if the separate finite tables and
certificate files are omitted. The current note says that they accompany it.
The safest prose-only edition embeds the complete factor tables and changes
that wording. This does not change any theorem or proof conclusion.

**Prose-edition disclosure.** The recommendation above to embed the complete
factor tables is not implemented in this edition because computational
certificate/table contents and raw data are outside its distribution scope.
The acceptance report expressly permits the alternative used here: accurately
disclose the finite classification left for reconstruction. The 144 cases for
D and 68 for the older seed were independently verified locally and can be
reconstructed from the stated divisor formulas by deterministic trial division.
The proof now states that the full tables, JSON certificates, detailed outputs,
and executable code are omitted. The audit below retains its substantive
analysis and reports what was checked in the reviewed local packet; references
to supplied certificates describe that packet, not distributed attachments.
The Section 4 heading now says positive lower relative density. No mathematical
claim is changed, and no claim that all computational dependencies are
distributed is made.

## 1. Exact scope and the least-preimage quantifier

For a totient value a, let F(a)={n≥1:φ(n)=a}, m(a)=min F(a), and R(a)=m(a)/a.
The original target is a sequence of totients tending to infinity along which
R(a) tends to infinity. The relevant paragraph in [Erdős's 1995 paper,
Section I.9, PDF page 6](https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf)
was inspected, including the distinction from the neighboring Carmichael
multiplicity question. Unboundedness of R is equivalent to the requested
sequence, because there are only finitely many positive integer arguments
below any fixed bound.

An arbitrarily large chosen preimage does not imply a large least preimage.
The candidate avoids that error: its finite calculation proves an entire
fiber identity, and the imported transport input preserves an entire fiber.
Taking its minimum is consequently legitimate in both steps.

## 2. Exhaustive finite proof

The asserted input and output factorizations are exact:

- D=575651577856=2^17·23·257·743;
- C=47·257^2·1487=4616098561;
- M=255C=1177105133055=3·5·17·47·257^2·1487;
- M/D=4580175615/2239889408
  =2.044822212490233803543214933583006612440751360524313886….

Every prime divisor q of a solution must satisfy q−1 | D. The divisor
description 2^i23^j257^k743^l, 0≤i≤17 and j,k,l∈{0,1}, gives precisely 144
distinct candidates q=d+1. All 144 were independently classified using a
sieve-generated list of trial primes. For every one of the 131 composite
candidates the supplied proper factor was independently verified to be an
integer strictly between 1 and q that divides q. All 13 surviving candidates
were proved prime deterministically, not by a probable-prime test. The largest
required square-root bound for a surviving prime is 16732.

The complete prime list is:

2, 3, 5, 17, 47, 257, 1487, 11777, 65537, 188417, 380417, 6086657, 279986177.

The note's predecessor factorizations agree with this list. None has 257 in
q−1. Thus the factor 257 in φ(n) must be supplied by q^(e−1), forcing q=257
with exponent exactly 2 in n. This consumes eight powers of 2. A repeated odd
prime other than 257 is impossible, because no other odd candidate divides D.
The noncandidate primes 23 and 743 cannot supply their own prime-power factors.

The remaining 2-adic budget is nine. The possible carriers of 23 are
47,11777,188417,279986177, with costs 1,9,13,14. Those of 743 are
1487,380417,6086657,279986177, with costs 1,9,13,14. The shared carrier costs
14 and is impossible. Once it is excluded, separate carriers are needed;
any carrier costing at least 9, together with the other required carrier
costing at least 1, exceeds the budget. Therefore 47 and 1487 are forced.
The prime 65537 costs 16 and is also excluded. This checks every full-fiber
exclusion rather than just verifying the displayed solution.

Consequently n=C·2^e·∏(q∈T)q, where T⊆{3,5,17}. The residual equation is
max(e−1,0)+s(T)=7, with binary weights 1,2,4. For e=0 the only solution is
T={3,5,17}; for e≥1 each of the eight subsets has e=8−s(T). The coefficients
of C, in increasing order, are

255, 256, 272, 320, 340, 384, 408, 480, 510.

The even coefficients are 256∏q/(q−1)≥256, so the odd coefficient 255 is
uniquely minimal. This proves the complete fiber and minimality without a
search cutoff on n:

1177105133055, 1181721231616, 1255578808592,
1477151539520, 1569473510740, 1772581847424,
1883368212888, 2215727309280, 2354210266110.

The smaller seed d0=387383296=2^16·23·257 was audited separately: all 68
divisor-plus-one candidates, 59 composite exclusions, and 9 primes check out.
Its least preimage is 791597265 and its fiber is the same coefficient list
times 47·257^2. Its identity F(D)=1487F(d0), with D=1486d0, follows from the
two finite calculations. It is not inferred by applying an almost-all-primes
statement to the particular prime 1487.

## 3. Independent computation and what it certifies

The candidate's three routes were inspected and rerun normally and under
Python -O and -OO. The two enumeration algorithms have different combinatorial
structures but share factorization and primality helpers. Their agreement
alone would not protect against a shared helper error.

The independent checker imports no candidate code. It regenerates divisors
from the prime-exponent formula, classifies candidates by an independently
built sieve, and visits the entire Cartesian box

0≤e_q≤v_q(a)+1

for every possible prime divisor q. This box covers every solution because
q^(e_q−1) | a for e_q≥1. Every tuple is evaluated, with no early pruning,
residual-divisor recursion, or upper bound on n. The audit visits 116736
tuples for D and 6912 for d0, obtaining exactly nine solutions in each case.
These agree with the separately derived coefficient list, including all
forward totient identities and the exact reduced ratio. The strict threshold
2.0448 was checked with rational arithmetic.

All 212 cells in both supplied Markdown factor tables were matched against
their JSON certificates. The certificates were verified as complete ordered
divisor lists, not merely as a selection of valid rows.

For an additional independent algorithm test, a totient sieve on n≤20000 was
compared with the independent exponent-box inverse calculation for every
1≤a≤100, including a=1 and odd nontotients. It is complete: for odd q,
φ(q^e)^2/q^e=q^(e−2)(q−1)^2≥1, and the factor from 2^e is at least 1/2.
Multiplication yields φ(n)^2≥n/2, hence φ(n)≤100 implies n≤20000.

Eight malformed-certificate controls were rejected: missing row, duplicate
row, changed candidate, bad factor, false prime, false composite, wrong seed,
and a Boolean masquerading as an integer factor. Every independent check
passes in all three Python optimization modes; no required condition is an
assertion removed by optimization.

The supplied mathematical checker permits an absent delivered certificate,
whereas its inventory verifier rejects absence. The audited combined packet
is intact, and the independent checker requires the certificate. This is a
robustness observation, not a mathematical failure. These computations do
not constitute a computational proof of the imported analytic theorems.

## 4. Scholarly-input audit

[Erdős (1958), proof of Theorem 4, printed pp. 15–18](https://renyi.hu/~p_erdos/1958-18.pdf)
counts the excluded primes by o(x/log x), and identifies every remaining
solution as p times an old solution. The proof pages were visually inspected;
its stronger whole-fiber conclusion is not inferred solely from the theorem's
multiplicity headline. For p>d+1, coprimality with every old preimage follows
from q−1 | d.

[Pollack–Pomerance–Treviño (2013), author-hosted paper](https://math.dartmouth.edu/~carlp/MonotonePhi.pdf)
defines convenience by exact fiber scaling on p. 2. Lemma 4.1, pp. 8–9,
allows equal fixed seeds, a fixed B≥max(d1,d2), and supplies ≫B Z(x)
convenient u with φ(u)≤x/B; the preceding comparison is V(x)≈Z(x).
The lemma is unconditional. Its additional uniform bound on u/φ(u) is
unneeded here. No distinctness, coprimality, or separate bound on u is being
silently assumed. The paper relies on Ford's corrected version; this audit
checks application of the published lemma, not an independent reconstruction
of all analytic estimates underlying it. The
[author's publication list](https://math.dartmouth.edu/~carlp/)
confirms Ramanujan Journal 30 (2013), 379–398.

The two PDFs were freshly retrieved from the official cited URLs and match
the submitted byte counts and hashes: Erdős, 1197232 bytes,
57d6660b80ddc74dfb6e3cb7521f52249a3cb598a1380faebc6465ea73221981;
Pollack–Pomerance–Treviño, 394691 bytes,
763eef23afd69a2afeb2addb54b15f25771ba91b717f4e35abb996f510a8e1c4.
Fresh retrieval is byte-identity evidence, not a separate scholarly review.

## 5. Transport, limsup, and density are different conclusions

For a fixed seed d and a convenient sufficiently large prime p, the fiber
identity immediately gives m(d(p−1))=p m(d) and
R(d(p−1))=R(d)p/(p−1)>R(d). The good primes have relative density one among
primes. Distinct p produce distinct arguments, tending to infinity, with
ratios tending down to R(d). For d=D, their count below X is asymptotic to
X/(D log X). This proves the stated infinite family and limsup lower bound.
It does not itself prove positive relative density among all totients.

For the global claim, put S=sup R(a) and L=limsup R(a) at infinity over
totients. For every fixed d, its transported family gives L≥R(d). Hence
L≥S, while L≤S by definition. For strictness above a particular attained
R(d), choose a convenient prime p>2, then use the same argument at the new
fixed seed d'=d(p−1): L≥R(d')>R(d). The extended-real case is valid as well.
The note's bound L≥R(D) is deliberately weaker than its general strictness
consequence; this is not a contradiction.

For the density claim, take d1=d2=B=D in the counting lemma. For every
supplied u>1, a=Dφ(u)≤x and m(a)=Mu, whence R(a)=r* u/φ(u)>r*. If two
supplied integers u,v had the same a, their least preimages would satisfy
Mu=Mv, and u=v. Thus the map is injective on the counted set. Discarding u=1
removes at most one element. Converting Z(x) to V(x) and, if necessary,
reducing the constant proves the displayed inequality for every sufficiently
large x. The exact conclusion is **positive lower relative density among
totients**, not existence of a relative-density limit, positive natural
density among integers, or a seed-uniform lower bound.

Neither a bounded limiting ratio, nonattainment of a finite supremum, nor
positive lower relative density above a fixed attained threshold proves
unboundedness. Repeated transport raises ratios, but the theorem for a fixed
seed gives no uniform control on the next usable prime as the seed changes.
A convergent product of the successive factors p/(p−1) is not excluded.

## 6. Attribution and release boundaries

The [August 2026 claim page](https://api.scinet.pub/f/2c289002-70f6-45bd-8624-440601935d9a)
was used by the candidate only to attribute the older seed. Its saved public
status is partial and awaiting independent review. Its ratio-2 theorem and
census are not accepted dependencies. The audit independently proves the
older finite seed and therefore does not inherit that claim's unreviewed
mathematics. This audit does not assert a freshly verified current status
for that manuscript or for any external problem tracker.

The exact candidate list is a genuine finite proof dependency. The table and
JSON are interchangeable certificates for that step, independently
reconstructible from the explicitly specified 144 divisors by deterministic
trial division. They are not a numerical census assumption. It would be
misleading to say that the argument needs no candidate classification or
that excluded attachments accompany a prose-only release. Embedding the
small factor table provides a transparent finite proof in the note itself;
the JSON and executable checks can then remain separate audit evidence.

No mathematical correction is required. The only recommended changes are
precise density terminology and honest packaging of the finite certificate.
The accepted result remains **PARTIAL** and the divergence target remains
unresolved by this work.
