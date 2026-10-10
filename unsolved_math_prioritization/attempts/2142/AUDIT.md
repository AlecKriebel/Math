# Audit of the prior finite counterexample to Erdős problem 488

Date: 10 October 2026. Problem identifier: EP-488 / 2142.

## Finding and attribution

**Accepted as a correct prior mathematical refutation of the finite multiples formulation.** The proof gives a nonempty finite set of positive integer generators and finite integer endpoints satisfying

\[
m>n\geq\max A,\qquad 2mM_A(n)<nM_A(m),
\]

where \(M_A(x)=|\{j\in\mathbb Z:1\leq j\leq x,\;a\mid j\text{ for some }a\in A\}|\).
In particular, \(M_A(m)/m>2M_A(n)/n\), a strict reverse of the proposed strict inequality.

The construction, proof, and Lean formalization are credited to **Declan Gessel, with disclosed GPT-6 Astra assistance in Codex, September 2026**. This audit checks that prior work; it is not a new counterexample or a claim of priority. The author's materials state that specialist review and historical/priority checking are being sought. This AI-assisted audit is not human peer review, and it makes no claim about mathematical-community acceptance or the current status of an external problem catalogue.

The full prose proof was inspected. All 496 lines of the server-source file and the entire additional adapter in the 561-line gist file were read. Independent exact integer checks reproduce the finite constants. No Lean source, imported library, third-party proof program, installation command, or build was executed. The mathematical acceptance here rests on the complete elementary argument below, not on interpreting an external success flag as a local proof replay.

## 1. Original statement and complement convention

The controlling primary formulation is P. Erdős, *Számelméleti megjegyzések V. Extremális problémák a számelméletben, II* (1966), section II.6, printed page 150, PDF page 16 [1]. Its introduction on PDF page 1 fixes the integer variables to be positive. The section orders \(a_1<\cdots<a_k\leq n\), defines the \(b_i\) to be numbers that are multiples of at least one \(a_i\), and asks whether
\[
B(m)/m<2B(n)/n\quad(m>n),\qquad B(x)=\sum_{b_i\leq x}1.
\]
The relevant page images and the introduction were directly inspected. Both the displayed strict inequality and the inclusive counting endpoint are legible. An ordered finite list of distinct positive generators and a nonempty finite set of positive generators are equivalent descriptions. There is no additional requirement that the generators form a primitive set, be coprime, or be squarefree.

The earlier *Some unsolved problems* (1961), I.27, printed page 236, PDF page 16 [2], literally describes **nonmultiples**. That sentence was also checked in the page image. Its following one-generator sharpness discussion motivates concern about the wording, but this audit does not silently replace that sentence. The explicit 1966 multiples statement supplies independent primary authority. The result accepted here concerns multiples; no conclusion about the separate nonmultiples interpretation follows merely by taking complements.

## 2. The fixed finite prime data

Let \(P\) contain the primes strictly below 257, and let \(S=P\setminus\{2\}\). Smooth numbers in this audit are positive integers whose prime divisors lie in the designated set; 1 is included. There are 54 primes in \(P\), 53 in \(S\); its largest prime is 251. Put
\[
Q=\prod_{p\in S}p,\qquad \phi=\prod_{p\in S}(p-1).
\]
Distinctness and primality of these factors give \(\phi=\varphi(Q)\) by multiplicativity of Euler's totient. This identity is about the product of the distinct primes defining \(Q\); it does not require the other smooth numbers in the construction to be squarefree.

During the accepted audit, an authored standard-library checker independently generated the prime list by both trial division and a sieve, reproduced the products, and verified
\[
Q>128,\qquad 3Q<16\phi,\qquad
2^{4096}(32769)^{53}<3^{4096}.
\]
All three exact comparisons passed in the accepted audit. The retained check results use unbounded integer arithmetic, with independent prime-enumeration methods and a repeated-multiplication check of powers. No decimal approximation, probabilistic primality test, numerical integration, or asymptotic density estimate is used. This publication edition retains the analytic constants and exact inequalities while omitting the raw products, gaps, prime lists, and computational certificate contents. Public verification metadata are in `VERIFICATION.json`; this prose edition is not an executable reproduction package.

## 3. Finite growth, including all quantifiers

For every integer \(j\geq0\), let \(H(j)\) count the \(S\)-smooth integers in \([1,256^j]\). If \(p^e\) divides a counted number, then
\[
2^e\leq p^e\leq256^j=2^{8j};
\]
therefore \(0\leq e\leq8j\). Unique factorization injects the counted integers into 53-tuples with entries in \(\{0,\ldots,8j\}\). The injection need not be onto. Consequently
\[
H(0)=1,\qquad 1\leq H(j)\leq(8j+1)^{53}.
\]

Suppose that no integer \(k\) with \(0\leq k<4096\) satisfies \(2H(k+1)\leq3H(k)\). Then for each such \(k\), \(2H(k+1)>3H(k)\), which in particular implies the weak inequality in the same direction. Induction starting at \(H(0)=1\) gives
\[
3^r\leq2^rH(r)\quad(0\leq r\leq4096).
\]
At \(r=4096\), the polynomial bound contradicts the checked strict endpoint comparison. Thus at least one integer
\[
0\leq k<4096,\qquad 2H(k+1)\leq3H(k)
\]
exists. The weakening from strict to weak growth in the induction is harmless; the contradiction comes from the strict upper comparison at the endpoint.

Fix one such \(k\), and set \(T=256^k\) and \(h=H(k)\). Both are positive. All subsequent arguments use this single fixed choice. This is a finite existence proof: it does not supply an enumerated value of \(k\), nor does this audit claim to have enumerated it.

## 4. Generators and endpoint obligations

Take the entire smooth band
\[
A=\{a\in\mathbb Z:T<a\leq256T,\;a\text{ is }P\text{-smooth}\},
\quad n=256T,\quad m=2TQ.
\]
It is finite. Since \(T\geq1\), every generator is positive and is greater than 1. Moreover \(2T=2^{8k+1}\) belongs to the band, so it is nonempty. Every generator is at most \(n\); indeed \(n\) itself is a power of 2 and belongs to the band, so \(\max A=n\). Only the weaker inequality is needed. The verified inequality \(Q>128\) and \(T>0\) imply \(m>n\). Thus all denominators are positive, all required endpoints are integers, and the full finite original domain is respected.

Redundant divisibility generators are permitted by the original statement. The proof needs the complete band for its near-count identity; no unjustified replacement by a minimal generating family occurs.

## 5. Exact identification of the near count

For \(j\in[1,256T]\) divisible by some \(a\in A\), write \(j=ac\) with a positive integer \(c\). From \(a>T\), one obtains \(c<256\), and certainly \(c<257\). Every prime divisor of \(c\) is therefore in \(P\). Multiplication preserves \(P\)-smoothness, so \(j\) is \(P\)-smooth; also \(j\geq a>T\). It follows that \(j\in A\). Conversely each \(a\in A\) is counted by its own divisibility. Therefore
\[
M_A(n)=|A|.
\]
This uses the strict lower end and inclusive upper end of the band. Neither 0 nor a multiple below the positive counting interval is introduced.

Every \(a\in A\) has a unique form \(a=2^e d\), with \(e\geq0\) and \(d\) an \(S\)-smooth number at most \(256T\). The map
\[
a\longmapsto(d,e\bmod8)
\]
is injective: two unequal exponents with the same residue modulo 8 differ by at least 8, and multiplying the smaller band member by at least \(2^8=256\) exceeds \(256T\). The strict lower endpoint is essential to that last strict conclusion. Hence
\[
M_A(n)\leq8H(k+1)\leq12H(k)=12h.
\]
No assumption that all potential pairs \((d,e\bmod8)\) occur is needed.

## 6. The finite far-count injection

For each positive \(S\)-smooth \(d\leq T\), choose the least \(e(d)\geq0\) with \(2^{e(d)}d>T\). Such an exponent exists because powers of 2 are unbounded, and the starting bound \(d\leq T\) forces \(e(d)\geq1\). The preceding exponent gives
\[
2^{e(d)-1}d\leq T,\qquad T<c_d:=2^{e(d)}d\leq2T.
\]
In particular \(c_d\in A\).

Let \(R=\{r\in\mathbb Z:0\leq r<Q,\;\gcd(r,Q)=1\}\). Its size is \(\varphi(Q)=\phi\). Because \(Q>1\), zero is excluded by the coprimality condition, so every \(r\in R\) is positive. The products \(c_dr\) lie in \([1,m]\) and are divisible by a member of \(A\).

To check injectivity, suppose
\[
2^{e(d)}dr=2^{e(d')}d'r'.
\]
Every prime dividing \(d\) belongs to \(S\) and divides \(Q\), whereas \(r'\) is coprime to \(Q\). Also \(d\) is odd. Thus \(\gcd(d,2^{e(d')}r')=1\). Euclid's divisibility lemma applied to the displayed equality gives \(d\mid d'\). Reversing the roles gives \(d'\mid d\), and positivity implies \(d=d'\). The selected value \(c_d\) is now identical on the two sides, so positive cancellation gives \(r=r'\). This reasoning handles arbitrary prime powers in \(d\) and \(d'\), rather than only squarefree integers.

There are \(h\phi\) input pairs, so
\[
M_A(m)\geq h\phi.
\]
The proof counts actual distinct positive integers below the fixed finite endpoint. It does not replace a finite count by a limiting density or assume a complete residue period occurs below \(m\).

## 7. The strict reverse and the negated quantifier

Combining the estimates gives
\[
2mM_A(n)\leq48TQh
<256T\phi h\leq nM_A(m).
\]
The middle strict inequality is exactly \(3Q<16\phi\) multiplied by the positive integer \(16Th\). Thus strictness is not lost even if either counting bound is attained. Dividing by the positive product \(mn\) proves the reverse density inequality.

The conjecture quantifies universally over the eligible finite sets and over every \(m>n\geq\max A\). One eligible set and one eligible pair of endpoints with this strict reverse refute that universal claim. No asymptotic statement, infinite set of generators, or change in the order of quantifiers is being substituted. The accepted result is stronger than merely the weak reverse needed for a logical negation of a strict inequality.

## 8. Lean source inspection and statement bridge

The server file at commit `ccf4a26cb8a8c49f476d44304070a2b677da4d7e` [3] and the gist file at revision `9bbb516e782229c8ee2fe08dfe3bd53acac8b258` [4] were inspected as text. The whole 20,230-byte server file occurs unchanged exactly once in the 22,801-byte gist file. Its definitions use `Ioc T (256*T)` for the generators and `Icc 1 x` for the counted multiples, matching the mathematical endpoints.

The complete server source follows the argument in sections 2–7:

- Lines 17–48 define the fixed primes, products, smooth counts and band.
- Lines 57–154 implement the exponent-vector bound and the finite-growth contradiction, including the exact endpoint check.
- Lines 162–283 encode the band by odd part and exponent residue, prove the near count, and prove nonemptiness.
- Lines 291–407 prove the coprimality facts, dyadic crossing, and far-count injection. The formal far-bound proof chooses one admissible exponent for each \(d\); leastness is used to establish existence of an admissible exponent, and no later step requires a computable least-value function.
- Lines 415–443 derive the totient formula and check the numerical ratio.
- Lines 451–492 assemble the strict finite counterexample and contradict the universal root statement.

These were all read for mathematical dependencies, domain restrictions, cancellation positivity, and inequality directions. A textual scan found no active `sorry`, `admit`, `axiom`, `native_decide`, `sorryAx`, or `unsafe` token in the reviewed gist proof. That limited scan is not a transitive axiom audit or a check of imported Mathlib declarations.

The added `Erdos488ExactAdapter.proposition` agrees with the entire right side of the retained Formal Conjectures statement [5] after removing only comments and whitespace. This is a literal retained-source comparison, not a claim that a mutable upstream branch can never change. The `answer(sorry)` wrapper and the proof's placeholder in the statement catalogue are not imported as evidence for the counterexample.

The adapter's mathematical bridge is valid for four separate reasons:

1. **Positivity.** A nonempty finite set excluding 0, with all members at most \(n\), forces \(n>0\); then \(m>n\) forces \(m>0\).
2. **Excluding 1.** The displayed band already excludes 1. The adapter also derives this directly from any strict counterexample: if \(1\in A\), then \(M_A(x)=x\), and its strict reverse becomes \(2mn<mn\), impossible.
3. **Maximum.** The pointwise bounds \(a\leq n\) imply `A.max ≤ (n : WithBot ℕ)` through the finite-maximum characterization. No empty-set bottom case is exploited.
4. **Counts and division.** The set comprehension explicitly requires \(j\geq1\), which is redundant inside `Icc 1 x`; the cardinalities therefore coincide. Division is over \(\mathbb Q\), not truncated natural-number division. Cross-multiplication is legitimate because both denominators are positive, and yields the integer inequality opposite to the counterexample.

No gap was found in this statement bridge. The adapter does not prove merely an unrestricted result while leaving the restricted `0,1 ∉ A` formulation unresolved.

## 9. External formal-verification evidence and its limits

The retained GitHub response for run **33990129375** reports `completed` / `success`, with head commit `ccf4a26cb8a8c49f476d44304070a2b677da4d7e`, created 5 September 2026 [6]. The source hash at that commit is independently bound to the retained server file. The project materials pin Lean `4.33.0` and Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.

The author's report states that only `propext`, `Classical.choice`, and `Quot.sound` occur in the formal axiom audit. This audit records that as the author's report. It did not replay Lean, inspect the full imported dependency graph, or independently reproduce that printed axiom list. The GitHub run is useful external evidence, but it is not this auditor's kernel replay, and its success at the server-source commit must not be relabeled as an independently replayed verification of the later gist adapter.

These limits do not leave the ordinary mathematical proof conditional: sections 1–8 supply a complete audit of its elementary argument and of the adapter's stated mathematical content. A future formal replay, if separately authorized, would be an additional reproducibility check, not a missing hypothesis in the human-readable proof.

## 10. Acceptance scope

**Accepted:** the prior full finite refutation, exact constants, admissible generators/endpoints, both finite counting estimates, strict reverse inequality, primary-source multiples interpretation, and mathematical correctness of the retained exact-statement adapter.

**Not claimed:** a newly discovered proof, an enumerated witness, an independently executed Lean verification, a current community consensus, an exhaustive historical-priority determination, or any result for the literal nonmultiples sentence in the 1961 source.

No mathematical correction to the audited proof is required. The necessary reporting discipline is to retain the prior author and AI-assistance credit, distinguish the 1966 and 1961 formulations, and keep external formal-verification reports separate from work independently performed in this audit.

## References

1. P. Erdős, *Számelméleti megjegyzések V. Extremális problémák a számelméletben, II* (1966), introduction and II.6, printed p. 150. [Primary PDF](https://users.renyi.hu/~p_erdos/1966-20.pdf).
2. P. Erdős, *Some unsolved problems* (1961), I.27, printed p. 236. [Primary PDF](https://users.renyi.hu/~p_erdos/1961-22.pdf).
3. Declan Gessel, with disclosed GPT-6 Astra assistance, *A finite counterexample to the density-doubling inequality for sets of multiples*, server Lean source, September 2026. [Immutable source commit](https://github.com/WoshuaJolk/jig-verifier/blob/ccf4a26cb8a8c49f476d44304070a2b677da4d7e/Submissions/ErdosMultiplesSmoothRefuted/Counterexample.lean).
4. Declan Gessel, *Erdős #488: counterexample and exact statement adapter*, gist revision `9bbb516e782229c8ee2fe08dfe3bd53acac8b258`, including the complete prose note. [Pinned prose note](https://gist.github.com/declangessel/d8e15e5ff1b6c7e99e3d86d7c66f1d08/raw/9bbb516e782229c8ee2fe08dfe3bd53acac8b258/proof-note.md).
5. The Formal Conjectures Authors, *Erdős Problem 488*, retained source snapshot retrieved 10 October 2026; SHA-256 `0f41c0f6d4fd550082b14dd909809be7c0904f03cf2294d793cd7c004858fe8a`. [Upstream file](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/488.lean).
6. WoshuaJolk/jig-verifier, GitHub Actions verification run 33990129375. [Run](https://github.com/WoshuaJolk/jig-verifier/actions/runs/33990129375).
