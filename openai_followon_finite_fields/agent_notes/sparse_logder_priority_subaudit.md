# Primary-source subaudit: logarithmic derivatives and low-degree rational reconstruction

Audit timestamp: 2026-10-07 05:24–05:32 UTC, with later additions timestamped below. Scope: prior statements and algorithm mechanisms, independently of the candidate proof. This is a subsection for the sparse priority audit, not a complete priority verdict or a correctness audit of the candidate.

The candidate described to this reviewer asks for deterministic complete factorization of a sparse univariate polynomial over an explicitly represented finite field, polynomial in term count, binary exponent length, field encoding size and dense radical degree D, initially assuming that every non-X factor has multiplicity prime to p. Its additional proposed step recovers valuations by sparse base-p grouping. No first-priority claim is supported by this subaudit.

## 1. Kaltofen 1988: exact reduced numerator/denominator reconstruction

Erich Kaltofen, *Greatest Common Divisors of Polynomials Given by Straight-Line Programs*, Journal of the ACM 35(1) (January 1988), 231–264. Primary author PDF: <https://kaltofen.math.ncsu.edu/bibliography/88/Ka88_jacm.pdf>. Author bibliography confirms this file and publication: <https://kaltofen.math.ncsu.edu/bibliography/index.html>. Section 8 results were disclosed earlier in STOC 1986, pp. 330–337, as stated on p. 231 of the journal article; the precise earlier version was not separately audited here.

Exact locations read: pp. 234, 256–261; Section 8, Algorithm Rational Numerator and Denominator, Theorem 8.1 and Corollary 8.1. Given a length-l SLP for reduced f/g and degree bounds d >= deg f, e >= deg g, the algorithm reconstructs numerator and denominator from d+e+1 Taylor coefficients via Padé approximation. It outputs an SLP of length O(l M(d+e)); uniform arithmetic cost is polynomial in l,d,e. General multivariate transformations and zero tests are randomized. The article also establishes binary bounds over finite fields/rationals; its rational-number theorem includes input scalar size. The rational function's reduced degrees, rather than the degrees of intermediate unreduced expressions, control reconstruction.

The Section 8 review on p. 257 gives the congruence (series)q-p = 0 modulo X^(d+e+1), uniqueness of p/q, and extended-Euclidean reconstruction. Naive arithmetic costs O((d+e)^2), or O(M(d+e) log(d+e)) with fast gcd methods. The p. 261 linear-system formulation and exact-degree verification are also explicit. The initial nonzero series constant is described there as inessential.

### Immediate deterministic univariate specialization — inference from the published machinery

For a univariate SLP whose divisions are all defined at a **known** origin, truncated-series evaluation and rational reconstruction take place over actual field elements. The random multivariate projection and randomized symbolic coefficient zero tests disappear: coefficients are tested exactly. In particular, a sparse F with F(0) != 0 supplies a known regular origin for F'/F. Sparse terms with binary exponents give an SLP of size O(t log(N+1)), or can be truncated directly at the origin without expanding through degree N.

The elementary identity

    F'/F = sum_i (e_i mod p) g_i'/g_i

over a perfect field shows that its reduced denominator is the product of the distinct g_i with p not dividing e_i. The assertion uses separability of each g_i and noncancellation of the corresponding residue. Thus its numerator degree is smaller than this denominator degree. Known degree cap D permits exact rational reconstruction from 2D coefficients, followed by ordinary dense factorization of the recovered denominator. A guessed cap can be checked by the exact sparse identity F'B-FA=0: multiplication by a dense degree-D polynomial introduces at most O(tD) terms with O(log(N+D+1)) exponent bits.

This is a direct specialization of established reconstruction, not evidence that logarithmic-derivative/Padé recovery is a new mechanism. Conversely, Kaltofen's printed theorem is not literally the candidate's deterministic finite-field full-multiplicity theorem. Arbitrary SLPs need not offer a known regular evaluation point; that qualification must be retained.

## 2. Dutta–Saxena–Sinhababu: low radical degree and characteristic-p partial radicals

Pranjal Dutta, Nitin Saxena and Amit Sinhababu, *Discovering the Roots: Uniform Closure Results for Algebraic Classes Under Factoring*. Primary arXiv record: <https://arxiv.org/abs/1710.03214>; v1 publicly submitted 9 October 2017 at 17:48:20 UTC. Preliminary conference version: STOC 2018. Full author journal manuscript: <https://www.cse.iitk.ac.in/users/nitin/papers/factor-closure-jacm.pdf>. The journal article is JACM 69(3) (2022), article 18, DOI 10.1145/3510359; the author PDF is a 37-page manuscript with placeholder publisher metadata, so its page/theorem numbers below refer specifically to that version.

Theorem 1 (p. 5) states: if f=u0 u1 is nonzero and size(f)+size(u0) <= s, every factor of u1 has a circuit of size poly(s+deg(rad(u1))). The default field is algebraically closed of characteristic zero (pp. 4–5). Its allRootsNI proof, Section 4.1 pp. 18–22, uses the classical logarithmic derivative, expands around distinct power-series roots and solves linear systems whose dimensions depend on radical degree. It explicitly accommodates exponentially large multiplicities. This is a circuit-size existence statement in that scope; it must not be recast as deterministic uniform finite-field factoring.

Section 6.3, Theorem 28 (p. 31), defines rad_p(f) as the product of irreducible factors whose multiplicities are not divisible by p. For f=u0 u1 and size(f)+size(u0) <= s, any factor of rad_p(u1) has size poly(s+deg(rad_p(u1))) over the algebraic closure. The proof says the p-divisible terms disappear from allRootsNI, so linear algebra depends on the partial radical degree. Section 6.2 (p. 30) explicitly leaves the transfer of low-radical bounds from splitting-field constants to the base field open; that extension can have exponentially large degree. Section 6.3 also distinguishes low-degree formula/ABP p-power extraction from the high-degree case. These are genuine scope qualifications, not failures that the candidate may silently assume repaired.

An additional independent proof already appeared in Amit Sinhababu's 2019 thesis, *Arithmetic Circuit Complexity and Approximative Algebraic Complexity*, Section 5.3, Theorem 5.3.1, pp. 77–78: <https://www.cse.iitk.ac.in/users/nitin/theses/sinhababu-2019.pdf>. In characteristic zero it applies Kaltofen's single-factor machinery to f+z f', whose distinguished degree-radical factor specializes at z=0 to rad(f). This is further positive prior evidence for the low-radical phenomenon, rather than a finite-field uniform theorem.

## 3. Kaltofen–Trager 1990: black boxes and multiplicities, but total-degree complexity

Erich Kaltofen and Barry M. Trager, *Computing with Polynomials Given by Black Boxes for Their Evaluations: Greatest Common Divisors, Factorization, Separation of Numerators and Denominators*, J. Symbolic Computation 9(3) (March 1990), 301–320. DOI <https://doi.org/10.1016/S0747-7171(08)80015-6>; primary author PDF <https://kaltofen.math.ncsu.edu/bibliography/90/KaTr90.pdf>. Preliminary disclosure was FOCS 1988, pp. 296–305, per the first-page footnote.

Section 2's algorithm (pp. 305–308) takes a black box over a field of characteristic zero with an effective univariate factorization procedure. It returns irreducible-factor evaluation programs and multiplicities, with controlled Monte Carlo error. Theorem 1 counts O(deg(F)^2) black-box calls and polynomial arithmetic cost in n,deg(F), plus univariate factoring. It starts by interpolating full-degree bivariate images. This is not radical-degree complexity. Section 3 reconstructs rational numerators/denominators by mixed-radix Padé; Theorems 3–4 (pp. 316–318) have reduced-degree complexity and randomized/expected guarantees. The conclusion permits adaptation to sufficiently high-characteristic finite fields, without an all-characteristic tame sparse radical theorem.

## 4. Classical auxiliary operation and multiplicity loss

Davenport–Carette, *The Sparsity Challenges* (SYNASC 2009), Section III.C, p. 3 of primary author PDF <https://www.cas.mcmaster.ca/~carette/publications/SparsityChallenges.pdf>, explicitly computes sparse f modulo a small-degree dense g by binary powering in O(t_f log(deg f) (deg g)^2) coefficient operations. This is established machinery for sparse divisibility/identity certification; it does not determine huge multiplicities.

Logarithmic derivatives retain multiplicity only modulo p. For example, over F_p the four-term polynomial (1+X)^(p+1)=1+X+X^p+X^(p+1) has the same logarithmic derivative as 1+X, despite multiplicities p+1 and 1. Both are prime to p, and both have radical degree one. Consequently the complete binary multiplicity output requires a separate justified method even in the tame promise. Mattarei's proof supplies the central mechanism, as detailed next.

No primary statement inspected here licenses treating unrestricted output-sensitive sparse gcd, general SLP base-field reconstruction, or all-characteristic p-power extraction as solved by the low-radical arguments. No candidate-proof verdict is supplied by this report.

## 5. Mattarei 2005/2006: the exact residue-and-leading-coefficient mechanism

Primary text: Sandro Mattarei, *Root multiplicities and number of nonzero coefficients of a polynomial*, <https://arxiv.org/html/math/0512239>. Version history and journal metadata: <https://arxiv.org/abs/math/0512239>. First public arXiv submission: 12 December 2005, 12:33:19 UTC; the text inspected is v2, 20 January 2006, 11:25:43 UTC. Published in Journal of Algebra and Its Applications 6(3) (2007), 469–475, DOI <https://doi.org/10.1142/S0219498807002338>.

Theorem 2 states that a nonzero root of multiplicity k over a characteristic-p field forces at least product_t(k_t+1) nonzero coefficients, where k_t are the base-p digits of k. Section 2 proves this by grouping exponents modulo p. Equation (1) divides each child by the same power of Y-1; evaluating the resulting children at 1 forms a degree-below-p polynomial whose root multiplicity is the low digit k_0. Children with nonzero evaluations have multiplicity (k-k_0)/p. This is positive prior evidence for precisely the proposed recursion, rather than merely a superficially related sparsity inequality.

### Constructive extraction and complexity — independently written deduction

For F(X)=sum_r X^r F_r(X^p), only occupied residues 0<=r<p are stored. Recursively compute q_r=ord_1 F_r and its first nonzero Taylor coefficient a_r. Put q=min_r q_r and P(X)=sum_{q_r=q} a_r X^r. Since X^p-1=(X-1)^p,

    F(X)=(X-1)^(pq) [ P(X) + (X-1)^p R(X) ].

P is nonzero, has degree below p, and uses u occupied residues. Its exact multiplicity j at 1 is below u: the matrix with rows binomial(r,h), 0<=h<u, has determinant equal, up to nonzero factorials, to the Vandermonde product of the distinct residues r. Thus at least one of sum_r a_r binomial(r,h), h=0,...,u-1, is nonzero. The first such h is j, and ord_1 F=pq+j. The same first nonzero sum is the Taylor leading coefficient needed by the parent recursion. Constants terminate the recursion.

At each level supports of all children sum to at most t. Exponents divide by p, so there are at most 1+floor(log_p N) levels for N>=1. There are O(t(1+log_p N)) occupied nodes; all low-digit moments together use O(t^2(1+log_p N)) field operations with straightforward arithmetic. Computing binomial(r,h) by its multiplicative recurrence uses only h<p and never divides by zero. Integer exponents, valuations and residues have O(log(N+1)+log p) bits. Grouping and integer division are deterministic polynomial-time operations. No enumeration of all p residues or p Taylor coefficients is required. This proves a routine bit-polynomial implementation over an explicitly represented finite field; it is not a statement printed as an algorithm in Mattarei's paper.

For a specified nonzero root alpha in an explicitly represented extension, replace coefficients c_i by c_i alpha^(e_i) using repeated squaring to normalize the root to 1. For a known monic irreducible g!=X, take alpha=X mod g in K[X]/(g); finite-field separability implies ord_alpha F equals the multiplicity of g. That field has dimension deg g over K, so this use depends polynomially on deg g, m and log p. The X multiplicity is simply the smallest sparse exponent. No construction of a large splitting field is needed.

Consequently, for the original non-X multiplicity-prime-to-p promise, exact univariate Padé reconstruction plus dense factorization plus this constructive extraction yields the candidate mechanism by combining established machinery. The exact complete sparse finite-field theorem and its full parameter accounting were not found printed verbatim in the inspected sources; that fact does not supply mathematical novelty. The parent subsequently proposed a stronger sparse/dense rational p-power recursion without the promise; its priority comparison is a separate remaining task, and the tame inference does not establish it.

## 6. Added comparison: sparse/dense quotient recursion and Cartier sections

Added 2026-10-07 05:32 UTC after the parent proposed a stronger algorithm without the multiplicity-prime-to-p promise. Proposed representation: a polynomial F=U/V with sparse U and dense V dividing U; remove visible multiplicity residues from U, write U=A_U H_U^p, and represent H_U by a sparse Cartier section of U divided by a dense Cartier section of A_U. Then combine with the corresponding dense denominator root and recurse. This subaudit compares primary prior mechanisms, not the correctness of the proposed invariant or its claimed degree bound.

Alin Bostan, Gilles Christol and Philippe Dumas, *Fast Computation of the Nth Term of an Algebraic Series over a Finite Prime Field*, ISSAC 2016, DOI <https://doi.org/10.1145/2930889.2930904>; primary text <https://arxiv.org/html/1602.00545>, v2 dated 18 May 2016. First public arXiv submission: 1 February 2016, 14:42:39 UTC, per <https://arxiv.org/abs/1602.00545>. Section 2.3, Definition 2.5 and equation (7), explicitly define coefficient sections and prove S_r(f(X)h(X^p))=S_r(f(X))h(X), with extension to Laurent series. Section 3.2 derives S_r(a/b)=S_r(a b^(p-1))/b and iterative common-denominator closure. Their main Theorem 9 gives O(h^2(d+h)^2 log N)+soft-O(h(d+h)^5 p) prime-field operations for a specified algebraic-series coefficient. The p term is genuine; it cannot be replaced by log p.

For a perfect coefficient field, let sigma send coefficients to pth powers and leave X fixed. Independently applying the elementary section identity to U=A H^p=A sigma(H)(X^p) gives

    S_0(U)=S_0(A) sigma(H),
    H=sigma^(-1)(S_0(U))/sigma^(-1)(S_0(A)),

provided S_0(A) is nonzero. A nonzero constant term of A ensures that condition. Hence the proposed individual sparse/dense root formula is an immediate constructive specialization of classical Cartier machinery. Extracting a sparse section requires only scanning the support and dividing qualifying exponents by p. This specific formula does not require computing a generic b^(p-1) expansion. Its identity itself should not be advertised as new.

What the inspected Cartier theorem does **not** print is the candidate's combined repeated radical recovery, maintenance of a sparse numerator of nonincreasing term count, linear-in-levels dense-denominator degree bound in the original radical degree, signed multiplicity bookkeeping, and full bit-polynomial uniform factoring reduction with binary-large degree. Those are the exact assertions whose proof and priority need separate checking. No failure to find that combined statement is treated as evidence of novelty. Conversely, the existence of classical Cartier identities alone does not establish that a prior algorithm had the candidate's parameter dependence.

Mark Giesbrecht and Daniel S. Roche, *Detecting lacunary perfect powers and computing their roots*, J. Symbolic Computation 46(11) (2011), 1242–1259, DOI <https://doi.org/10.1016/j.jsc.2011.08.006>; primary <https://arxiv.org/html/0901.1848>, v2 dated 3 December 2010, first publicly submitted 13 January 2009. Theorem 3.1 and Algorithm 5 compute an integer-polynomial perfect root with sparsity bound mu in bit cost polynomial in input sparsity, log degree, coefficient size and mu. Section 3.2's finite-field sparse Newton algorithm assumes characteristic greater than the input degree; its sparsity complexity relies on Conjecture 3.3. These exact hypotheses exclude using it as an all-characteristic sparse/dense p-power closure theorem.

The current primary Huang–Cao–Qiu–Gao manuscript *Deterministic Polynomial-time Exact-root Computation for Sparse Polynomials with Bounded Total Degree*, <https://arxiv.org/html/2607.02364>, arXiv v1 publicly submitted 2 July 2026, was also checked at its Algorithm 1 steps 12–15 and Theorem 5.2. It applies exponent/coefficient inverse Frobenius to an already represented sparse exact power. Its stated cost is poly(s^(O(Td)),n,d,T)+s R(e), with T the **total input degree** and R(e) scalar-root cost. The proof qualifies polynomial absorption by availability of suitable deterministic scalar-root routines. This is a different parameter regime from binary-large N and dense radical degree D, and it does not provide the proposed quotient representation invariant. Only these scope comparisons were audited; its full proof was not validated here.

Priority framing supported by positive evidence: Padé reconstruction, partial-radical logarithmic derivatives, the valuation-trie mechanism, sparse modular powering and the section product identity all have explicit older sources. Any proposed contribution must isolate and establish the new combined representation/degree invariant and resulting all-multiplicity theorem, if these survive the parent proof and broader priority audits. A description claiming a new logarithmic-derivative method or new sparse root-multiplicity mechanism would be inaccurate.

## 7. Evidence and limits

Read directly: Kaltofen1988 Section 8 and surrounding introduction/conclusion; DSS author-journal Theorem1, proof Section4.1 and Sections6.2–6.3; Sinhababu2019 Section5.3; Kaltofen1987 Theorems2–5; Kaltofen–Trager1990 Sections1–3; Davenport–Carette SectionIII.C; Mattarei Theorem2 and its entire Section2 proof; Bostan–Christol–Dumas Sections2.3,3.2,4.2–4.3; Giesbrecht–Roche Algorithms5–6/Theorems3.1–3.2 and Section3.2 assumptions; Huang–Cao–Qiu–Gao Algorithm1 Frobenius steps and Theorem5.2. Bibliographic metadata and public version history were checked at primary/author sites. Source paragraphs were paraphrased; no external communication occurred. This was a source audit, not a rebuild or independent validation of these papers' full proofs. The valuation recurrence and root-section formula were derived algebraically here, not tested computationally in this subaudit.

Temporary research-only downloaded PDF SHA-256 values (third-party PDFs were not placed in the publication package):

| File | SHA-256 |
|---|---|
| Kaltofen1987 Ka87_stoc.pdf | 56ea27444f536253f8e7bbbbb08c675c7dfc8c811b2f34ce5851e9f8c7e05257 |
| Kaltofen1989 Ka89_slpfac.pdf | 630ece94a6580aba0a0deabc6f1a361285d48d76f3a61accfd4581656bdf40a8 |
| DSS author factor-closure-jacm.pdf | da06b5f1834802165ea2b8e20735fd4d87dc878be0982169ce1f8c82513451bb |
| Sinhababu2019 thesis | 9b31e7dc3cea8dbd84bc51421ef548febe16ad1348148e63c97fb9cc996e527b |
| Kaltofen–Trager1990 KaTr90.pdf | 118f646ad35440379b3b4dce5c440e3ed848ca30f116987aad356082c4de5f1e |

Kaltofen1988 and Davenport–Carette were read with the web PDF extractor; Mattarei and the Section6 additions were read in arXiv HTML. No local-byte hash is claimed for those sources. Some server dates displayed by search are crawler dates and are not priority evidence. A failed query or an inaccessible publisher endpoint was not counted as absence of prior art. Focused additional searches included radical-degree finite-field factoring, sparse/dense pth roots, sparse Cartier radical recovery, and sparse squarefree factoring in positive characteristic; their inconclusiveness supplies no novelty certification.

Checkpoint estimate: this delegated source-subsection audit is 100% drafted, subject to incorporation and independent checks; the parent mathematical-resolution and publication-package percentages are not estimated here.
