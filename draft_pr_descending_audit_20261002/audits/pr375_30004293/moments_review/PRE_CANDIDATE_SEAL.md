# Source-first independent specification and controls

Sealed no later than 2026-10-03 06:53:04 UTC (the clock call immediately before the first candidate-text read). At sealing, candidate text, root/sibling analysis, author verification code and historical review had not been read. This specification and the mechanisms below were formulated from the source PDFs and elementary reasoning. The initial timestamp was a future placeholder; this metadata-only correction records the observed clock without changing any pre-candidate mathematics.

## Literal object and separate quantitative question

Let independent Bernoulli variables (X_n) satisfy (P(X_n=1)=1/n), and let (A=\{n:X_n=1\}). In particular (1\in A) surely. For integer (D\ge1), let (B_D=A\cap[1,D]), (N_D=|B_D|), and (S_D=\sum_{n\in B_D}n). Define

\[
r_D(s)=\#\{C\subseteq B_D:\sum_{c\in C}c=s\},\qquad M(D)=\max_{s\in\mathbb Z}r_D(s).
\]

Each representation is a distinct subset, not an ordered tuple or multiset; the empty subset is allowed and has sum zero. For the infinite set, (r_A(s)=r_{A\cap[1,s]}(s)) is finite for every nonnegative integer (s), because summands are positive. The maximum over all (s) need not be finite. Real cutoffs reduce to their integer floor.

Green's OWR contribution, printed pp. 3164-3167, introduces the full-set representation model and then a truncated fixed-(k) threshold. FGK v3 and the published paper define the independent Bernoulli model, the distinct-subset threshold \(\beta_k\), and \(\zeta_\pm\). Their full Lemma 2.1 and remark explicitly give a prefix lower bound by taking \(D_1=3,D_2=D\). The proof uses disjoint geometric-in-log blocks, success in a (1-o(1)) proportion of blocks, and injective union of one equal-sum choice in each block. Thus increasing multiplicity for a prefix is already within source scope. The precise rate question I use here is whether \(\log M(D)/\log\log D\) converges in probability to a specified finite constant. This is a distinct quantitative hypothesis, not a verbatim OWR problem statement. To resolve it requires matching typical upper and lower bounds; unboundedness alone is insufficient.

Source access, byte lengths and SHA-256 hashes are recorded in SOURCE_IDENTITY.json. Visually inspected OWR PDF pages 24-27 (printed 3164-3167) and published FGK PDF pages 9-10 (printed 1035-1036), including the complete Lemma 2.1 proof and remark. Compared v3 text. Raw/extracted/rendered material remains private under ignored tmp/.

## Independent mechanisms and falsifiable controls

1. **Universal pigeonhole mechanism.** For every finite positive-integer set (B), writing (N=|B|), (S=\sum B), the (2^N) subsets land in (S+1) possible sums, so (M(B)\ge2^N/(S+1)). Must check empty set, singleton, full interval, superincreasing sets, complements and coefficients of \(\prod_{b\in B}(1+z^b)\).
2. **Exact probability mechanism.** For (B\subseteq[1,D]), its probability is zero if (1\notin B); otherwise it is \(D^{-1}\prod_{b\in B\setminus\{1\}}(b-1)^{-1}\). This follows by factoring \(\prod_{n=2}^D(1-1/n)=1/D\). Exact fractions and total mass one will test it.
3. **Moment change of measure.** For fixed (q>0), set (t=2^q), (a=t-1), and (Z_D=E[t^{N_D}]=\prod_{n=1}^D(1+a/n)\). Weighting configurations by (t^{N_D}/Z_D) gives independent tilted inclusions (t/(n+a)). Their expected total sum is \(t\sum_{n=1}^D n/(n+a)\le tD\). Convexity of (s\mapsto(s+1)^{-q}\) gives
   \[
   E[M(D)^q]\ge Z_D/(1+tD)^q.
   \]
   Since \(Z_D\sim D^a/\Gamma(1+a)\), the lower exponent is \(2^q-1-q\), positive for (q>1\). For (q=2\), \(Z_D=(D+1)(D+2)(D+3)/6\), giving \(\liminf E[M(D)^2]/D\ge1/96\). Exact small-cutoff enumeration must check the tilted identity and the stronger bound using the exact tilted mean, not just the coarse bound.
4. **Rare-tail mechanism.** The tilted number of inclusions is approximately (t\log D\), whereas the ordinary count is approximately \(\log D\). For (q>1\), choose \(1<\alpha<t\), e.g. \((1+t)/2\). Chernoff gives the ordinary high-count event probability at most \(D^{\alpha-1-\alpha\log\alpha+o(1)}\to0\). Under the tilt the same event has probability tending to one; imposing \(S_D\le2tD\) still leaves probability at least (1/2-o(1)\) by Markov. Therefore polynomial moment mass can be contributed by an event of vanishing ordinary probability. Test this distinction with exact configuration products and a standalone sequence (Y_D=1\) except (Y_D=D^s\) with probability (D^{-r}\): its log-normalized value tends to zero in probability while any moment with (sq>r\) diverges polynomially.
5. **Convergence and logarithmic expectation.** Since (1\le M(D)\le2^{N_D}\), raw moments control neither the proposed limit nor automatically the expectation of \(\log M(D)/\log\log D\). If one also establishes uniform integrability of these normalized logarithms, probability convergence implies expectation convergence. Without uniform integrability even bounded-in-probability logarithmic variables can have diverging means; record an explicit counterexample. Markov with a raw positive moment is a one-sided upper-tail tool and cannot infer a lower bound in probability from a large expected moment.

## Scope cautions fixed before candidate access

Mao-Song v2 (2026-09-27) claims a fixed-(k\) close-divisor threshold identity and local repairs to FGK; its full proof has not been independently audited here. Tenenbaum's powers paper concerns integer powers and polynomial arguments, including divisor multiplicity; it is not automatically a theorem for distinct-subset Bernoulli prefixes. Neither is an implicit proof of the target prefix limit. The source-dependent FGK threshold premises and recent claimed repairs must remain explicit rather than silently promoted to independently verified premises.

Independent bounded-audit completion estimate: 30%. Original rate discovery remains unresolved.
