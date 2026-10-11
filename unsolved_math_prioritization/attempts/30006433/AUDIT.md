# Independent audit: rank-two subalgebra zeta asymptotics

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

The full authored mathematical proof and audit, including every analytical formula and theorem table, are retained. This is not a computational reproduction package: executable code, raw HNF or root-enumeration datasets, copied source PDFs/text/images, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, or mathematical execution. The original reports remain unchanged.

## Verdict

**Accepted as a correct partial proof for both targets 30006433 and 30006435. No mathematical correction is required.**

The accepted scope is every integral algebra whose underlying additive group is free of rank at most two, with arbitrary bilinear multiplication. Associativity, commutativity, nilpotence, and an identity are not assumed. Subalgebras need not contain an identity. The degree assertion and the positive coincidence assertion follow from one shared calculation. Neither universal conjecture is proved, and no novelty is established.

The audited object is the entire original proof report, SHA256 `6304ad89b3ef270432960d27f9c744bc486c46011f4428aa8b274521d839b788`, inside a closed 19-member package. Its manifest SHA256 is `ba35b778ce665c82bef40896a8e8cf9ba4186a3ff9bc6f2ef0de69356c9eca5a`; the independently supplied outside-seal SHA256 is `9b5496cb4fe34fc14be1aa25aecc8f698bfea50c531d4d23f67660cd56e5b0dc`. Both pins, every member size/hash, and the exact file inventory were verified independently. No candidate checker or source-author program was executed or imported.

## 1. Exact target and normalization

The target is the leading behavior at **infinity**:

\[
m_{\rm top}(A)=\lim_{s\to\infty}s^dZ^A_{\rm top}(s),\qquad
m_{\rm red}(A)=\lim_{T\to1}(1-T)^dZ^A_{\rm red}(T).
\]

This agrees with evaluation of the reciprocal-variable expression at zero. It does not mean the original-variable limit at zero. The report preserves that distinction.

I freshly retrieved Rossmann's [three-page contribution](https://torossmann.github.io/files/mfo25b.pdf), inspected all three pages as text, and visually checked page 3. It identifies the same finite-free algebra class, degree assertion, and positive coincidence assertion. In [*Computing topological zeta functions … I*](https://torossmann.github.io/files/topzeta.pdf), Example 5.11(iii), Definition 5.2, Theorem 5.12, and Definition 5.17 give precisely the candidate's normalization by \((1-q^{-1})^d\) and Euler-weighted constant-term operation. Remark 5.18 distinguishes an older shifted/factorial convention; the candidate does not inadvertently use that convention.

## 2. Arbitrary lattices and ordered cross-products

Let \(B\subseteq\mathfrak o^2\) be a full lattice over a compact DVR. Its largest common power of the uniformizer gives the unique decomposition \(B=\pi^a C\), where \(C\) is primitive. The elementary divisors of \(C\) are \((1,\pi^b)\). When \(b>0\), a primitive generator \(v\) can be extended to an ambient basis \((v,w)\), and

\[
C=\mathfrak o v+\pi^b\mathfrak o w.
\]

The four ordered generator products in \(\pi^a(C C)\) are obtained from
\(v^2,\pi^b vw,\pi^b wv,\pi^{2b}w^2\). All except the first already belong to \(\pi^b\mathfrak o^2\subseteq C\). Therefore closure is equivalent to

\[
\pi^b\mid\pi^a\det(v,v^2).
\]

This directly checks the noncommutative issue: both ordered mixed products are accounted for separately. No polarization or division by two occurs. The determinant criterion is valid because \(\det(v,w)\) is a unit. The case \(b=0\) is automatic, and the index is \(q^{2a+b}\).

Primitive cyclic-quotient lattices are exactly the points of \(\mathbb P^1(\mathfrak o/\pi^b)\). The two disjoint affine charts have sizes \(q^b\) and \(q^{b-1}\). Their reduction fibers have size \(q^{b-k}\). The equation for a homogeneous cubic is invariant under a unit rescaling of a primitive representative, and under changing a lift modulo \(\pi^k\).

It follows that the candidate's all-primes identity is exact:

\[
Z_{\mathfrak o}(T)=\frac1{1-qT^3}
\left(\frac{1+T^3}{1-T^2}+\sum_{k\ge1}N_k(q)T^k\right).
\]

The first summand counts \(b\le a\), including \(b=0\); the second counts \(b=a+k\), using \(q^a\) lifts and index exponent \(3a+k\). This reasoning applies at bad primes too, provided the actual congruence counts \(N_k\) are retained.

Under a basis change with matrix \(g\), the new cubic is \(\det(g)^{-1}f(gv)\). Consequently the projective root multiplicities used in the theorem are intrinsic. Independent symbolic checks included determinant \(+1\) and \(-1\) basis changes.

## 3. Good primes, root schemes, and all finite extensions

For a nonzero cubic, divide its projective zero scheme into its reduced multiplicity strata \(V_e\), for \(e=1,2,3\). In characteristic zero these are finite étale schemes. After excluding finitely many rational primes, they extend to disjoint finite étale subschemes, the content is a unit, and the multiplicities remain unchanged.

Crucially, these are conditions over a localization of \(\mathbb Z\), not conditions requiring a fixed splitting field or an unramified local extension. For any finite extension \(K/\mathbb Q_p\) at a good prime:

- A residue-field-rational point of \(V_e\) lifts uniquely over the complete Henselian valuation ring of \(K\).
- The corresponding simple factor is a local coordinate \(z\), and the full cubic is \(z^e\) times a unit on that residue disk.
- Unit content and disjointness remain unit conditions after ramified base change.
- Non-rational residue roots contribute no projective point and hence no lift.

Thus each rational multiplicity-\(e\) root contributes exactly \(q^{k-\lceil k/e\rceil}\) points modulo \(\pi^k\). Summing gives

\[
\sum_{k\ge1}N_k(q)T^k
=\sum_{e=1}^3\#V_e(\mathbb F_q)
\frac{\sum_{j=1}^e q^{j-1}T^j}{1-q^{e-1}T^e}.
\]

This proves the necessary extension-uniform Denef formula while retaining nonuniform point counts. It does not assume a single rational function with prime-independent root counts. For \(x^3-2y^3\), the counts over \(\mathbb F_5\) and \(\mathbb F_7\) are respectively one and zero, while the geometric count is three. The audit also checks splitting after the extension from \(\mathbb F_5\) to \(\mathbb F_{25}\).

## 4. Topological and reduced specializations

Each rational summand has two vanishing denominator factors after substituting \(T=q^{-s}\). Multiplication by \((1-q^{-1})^2\) makes each summand individually regular in \(q-1\), as required for the cited topological specialization. Its denominator factors have leading terms \((bs-a)(q-1)\), so the constant-term calculation in the report is valid in the rational-function field in \(s\).

For reduced specialization, every summand is regular at \((q,T)=(q_0,T)\) as an element of \(\mathbb Q(T)\), for every positive integer \(q_0\), including \(q_0=1\). This verifies the full regularity hypothesis of Lemma 7.1 and Remark 7.2 of [Rossmann's local-zeta paper](https://torossmann.github.io/files/padzeta.pdf), rather than checking only a formal substitution at one point.

There is also a direct coefficientwise explanation over \(\mathbb C[[t]]\): each root-lifting stratum is an affine space of dimension \(k-\lceil k/e\rceil\); its additional primitive-lattice lifts form an affine space of dimension \(a\). Each has Euler characteristic one. Summing over the geometric roots gives their number, regardless of multiplicity. When \(b\le a\), the base projective line has Euler characteristic two. This justifies the reduced expression without supposing that numerical point counts alone determine the motivic class.

Writing \(r_e=\#V_e(\mathbb C)\) and \(R=\sum r_e\), the two resulting expressions are

\[
Z_{\rm top}(s)=\frac{1}{3s-1}
\left(\frac1s+\sum_e\frac{e r_e}{es-e+1}\right),
\]
\[
Z_{\rm red}(T)=\frac{1}{1-T^3}
\left(\frac{1+T^3}{1-T^2}+\frac{RT}{1-T}\right).
\]

The three possible nonzero-cubic multiplicity partitions give exactly the displayed table in the candidate:

| Cubic | Topological function | Reduced function | Common leading value |
|---|---|---|---|
| Zero | \(1/[s(s-1)]\) | \(1/(1-T)^2\) | \(1\) |
| Triple root | \(2/[s(3s-2)]\) | \((1+T^2)/[(1-T)(1-T^3)]\) | \(2/3\) |
| Double and simple | \(2/[s(2s-1)]\) | \(1/(1-T)^2\) | \(1\) |
| Three distinct | \(4/[s(3s-1)]\) | \((1+T)^2/[(1-T)(1-T^3)]\) | \(4/3\) |

All four topological rational functions have exact degree \(-2\) after cancellation. Both leading evaluations are finite and strictly positive.

For the zero cubic, the determinant criterion makes every lattice a subalgebra; substitution into the all-primes expression gives \(1/[(1-T)(1-qT)]\). This case must be handled separately from a finite root scheme. Its one-dimensional subalgebra variety is all of \(\mathbb P^1\), so the candidate's geometric formula still gives \((1+2)/3=1\).

In rank one, \((ne)^2=n^2ce\in n\mathbb Ze\), so all finite-index subgroups are subalgebras. The claimed functions and leading value one follow. Rank zero contributes only the zero lattice, and all functions equal one.

## 5. Conditional specialization lemma and scope controls

The conditional lemma is correct, with \(d\) interpreted as the nonnegative integral normalization exponent, as in its application. Absorb the analytic unit into the numerator and let its first nonzero homogeneous Taylor component have degree \(k\). Under \(X=1+h\), \(T=(1+h)^{-s}\), its first term is \(h^kP_k(1,s)\). Each nonvertical denominator contributes one factor of \(h\) with leading coefficient \(b_js-a_j\).

If \(k<r-d\), regularity would require the homogeneous polynomial \(P_k(1,s)\) to vanish identically, contradicting its choice. Thus the degree bound and equality of the two leading evaluations follow from the homogeneous component of degree \(r-d\). If that component vanishes, or if \(r<d\), the corresponding leading evaluations vanish. No positivity or exact degree follows merely from the lemma.

The report's artificial nonnegative-coefficient family and vertical-denominator example are valid warnings, not claimed algebraic counterexamples. The rank-three Heisenberg example correctly shows that vanishing squares do not ensure closure of arbitrary higher-rank lattices. The cited [Evseev Proposition 4.1](https://arxiv.org/pdf/0710.0387) has specific nice-and-simple-basis hypotheses. The formulas in [Voll, §3.4](https://arxiv.org/pdf/1902.01794) concern the stated ideal-zeta family. Neither is used to smuggle in an unrestricted subalgebra theorem.

## 6. Independent verification

The audit checker was written separately from the candidate checker and uses only standard Python and SymPy. Its final normal, `-O`, and `-OO` runs all pass, with identical mathematical results:

- 356 distinct multiplication tables, including all 256 binary structure-constant tables, 96 deterministically selected signed tables, and named degeneracy/nonuniform examples.
- 640 table/prime jobs and 300,672 individual HNF lattice/test instances per mode; all four ordered products are checked against direct lattice membership before comparison with the determinant criterion.
- 3,728 independent coefficient comparisons with direct projective root enumeration.
- 76 root-count comparisons in eight mixed-characteristic DVR extension configurations, including residue fields of sizes 4, 9, and 25 and ramification indices 2 and 3; these checks supplement the all-extensions proof.
- Exact symbolic local identities, topological specializations, reduced specializations, canceled degrees, leading values, rank-zero/rank-one cases, basis covariance, and four conditional-lemma examples.
- Eleven deliberately false mathematical claims are rejected in every mode. They cover omitted infinity roots, lost multiplicity, bad primes, fixed root counts, residue-field extension, the original-variable origin, false positivity, vertical specialization, and rank-three square-only reasoning.

The package verifier uses explicit exceptions rather than `assert`. Its independent tiny-fixture controls accept three intact packages and reject 33 mutations across the three optimization modes. The mutations include extra/missing members, duplicates, unsafe paths, symlinks, wrong sizes/hashes, bad outside pins, and coordinated manifest/seal changes. These tests never mutate the candidate.

During checker development, a structurally different but equal SymPy expression triggered one false alarm. It was corrected to rational-function equality. All published audit receipts come from the final checker, rerun in all three modes. Finite testing and byte integrity are supporting evidence; the written proof establishes the universal rank-two statement.

## 7. Prior work, source boundaries, and final status

Fresh whole-file downloads of the four dependency PDFs exactly match the candidate's source hashes and sizes. The three-page target contribution also matches its published metadata. Whole-file retrieval does not imply whole-paper inspection; detailed reading and visual-inspection boundaries are listed in SOURCES.json.

The primary [Snocken thesis repository record](https://eprints.soton.ac.uk/372833/) explicitly describes two-dimensional-ring subring formulas via Igusa zeta functions. The audit independently found that record's indexed abstract. Direct repository/PDF access failed through the web tool; no thesis PDF was retrieved or inspected. The detailed overlap, any stronger prior classification, and the precise relationship between the thesis formulas and this proof remain unverified. This is sufficient reason to retain the candidate's explicit lack of a novelty claim.

This audit does not establish the absence of later general work, certify the complete proofs of the cited papers, or turn this rank-two result into a resolution in rank at least three. The correct disposition remains **one accepted shared rank-at-most-two partial proof for two unresolved general targets**. The original proof and audit reports remain unchanged; this edition records their accepted shared partial scope.
