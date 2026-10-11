# EP 1122 / 2503 conditional exact additive rigidity

## Verdict and scope

This edition gives a self-contained conditional rigidity theorem, two exact lifting lemmas, a sufficient prime-tail condition, and mathematical examples identifying invalid upgrades of variance-normalized approximation. The unrestricted density-zero-decrease problem is not solved by this work, and no counterexample to it is produced. No novelty is claimed.

The target concerns an ordinary real-valued additive function: f(ab)=f(a)+f(b) only when gcd(a,b)=1. With D={n≥1:f(n+1)<f(n)}, the hypothesis is |D∩[1,X]|=o(X), and the desired conclusion is one fixed nonnegative c with f(n)=c log n for every n. Complete additivity is never assumed in the authored arguments. Theorem 3 requires the additional absolute-scale premise that the residual for one fixed c is periodically approximable in density.

## 1. A useful exact lifting principle

Here and below, convergence in density to a real number a means that for each ε>0 the set {n≤X:|h(n)−a|>ε} has size o(X).

**Lemma 1 (coprime-dilation lifting).** If an ordinary additive h:N→R converges in density to a finite real number a, then h(m)=0 for every m≥1 (and a=0).

**Proof.** Fix m≥2 and ε>0. Among 1≤n≤X/m, the number coprime to m is (φ(m)/m)(X/m)+O_m(1), a positive multiple of X. The failures of |h(n)−a|≤ε account for o(X) choices of n, and the failures of |h(mn)−a|≤ε also account for at most o(X) choices: the map n↦mn is injective into [1,X]. Hence, for all sufficiently large X, there is a coprime n satisfying both inequalities. Ordinary additivity gives |h(m)|=|h(mn)−h(n)|≤2ε. Let ε decrease to zero. Also h(1)=0 follows from h(1)=h(1)+h(1). Thus h vanishes identically, forcing its density limit to be zero. ∎

This principle does not require uniformity in m, complete additivity, or control of a density-zero exceptional set on infinitely many dilations at once. Each fixed m is handled separately.

**Lemma 2 (absolute approximation already suffices).** Suppose f is ordinary additive. If for every sufficiently large X there are λ_X,η_X∈R, e_X→0 and a set E_X⊂[1,X] of size o(X) such that

|f(n)−λ_X log n+η_X|≤e_X for n∈[1,X]\E_X,

then f(n)=c log n for every n, with c=f(2)/log 2. No almost-monotonicity hypothesis is needed for this lemma.

**Proof.** Fix m≥2. Choose n≤X/m coprime to m with n,mn∉E_X, by the same positive-density count as above. Subtract the two approximation formulas and use additivity. The offset cancels exactly, giving |f(m)−λ_X log m|≤2e_X. First take m=2, which gives λ_X→c; then take any fixed m and let X tend to infinity. ∎

Consequently, the offset in an absolute o(1) approximation is not an obstruction to exact rigidity. The obstruction in the available theorem is the error scale o(B_f(X)), which need not approach zero.

## 2. The substantive route: a periodically approximable residual

For a set S⊂N let upper density mean limsup_{X→∞}|S∩[1,X]|/X.

**Definition.** A real sequence h is *approximable by periodic sequences in density* if for every ε>0 there is a real periodic sequence a such that

upper density {n:|h(n)−a(n)|>ε}<ε.

The period, values, and approximating sequence can depend on ε. No uniform approximation and no boundedness of h are required.

**Theorem 3 (conditional exact rigidity).** Let f:N→R be ordinary additive and let D={n:f(n+1)<f(n)} have natural density zero. If there is one fixed c∈R such that h(n)=f(n)−c log n is approximable by periodic sequences in density, then

f(n)=c log n for all n≥1, and c≥0.

The proof has two stages. Almost-monotonicity forces the periodic residual to be constant in density; ordinary additivity then lifts this to equality at every positive integer.

### 2.1 A bounded transform has vanishing average variation

Put u(n)=arctan(h(n)), so |u(n)|<π/2. Outside D,

h(n+1)−h(n)≥−c log(1+1/n)≥−|c|/n.

The function arctan is increasing and 1-Lipschitz. Thus, writing t_+=max(t,0),

(u(n)−u(n+1))_+≤|c|/n outside D,

and it is at most π everywhere. Therefore

(1/X)Σ_{n≤X}(u(n)−u(n+1))_+ ≤ π|D∩[1,X]|/X + (|c|/X)Σ_{n≤X}1/n →0.

The signed differences telescope. Since u is bounded,

(1/X)Σ_{n≤X}(u(n+1)−u(n))→0.

Using |t|=t+2(−t)_+, we conclude

(1/X)Σ_{n≤X}|u(n+1)−u(n)|→0.                                    (1)

For each fixed integer j≥0, the triangle inequality and a shift of the summation endpoints give

(1/X)Σ_{n≤X}|u(n+j)−u(n)|→0.                                    (2)

Only fixed j is asserted here. There is no invalid uniform claim for j growing with X.

### 2.2 Periodic approximation forces a constant

For a bounded sequence w define ||w||_B=limsup_{X→∞}(1/X)Σ_{n≤X}|w(n)|. This seminorm is invariant under a fixed nonnegative shift, by boundedness.

The periodic approximability of h implies that u can be approximated arbitrarily well in this seminorm by bounded periodic sequences. Indeed, if |h−a|≤ε outside a set of upper density <ε, then v=arctan(a) is periodic and

||u−v||_B≤(1+π)ε.

Fix such a v of period q, and let C=q^(−1)Σ_{r=1}^q v(r). Its consecutive q-term averages equal C exactly. By (2),

||u−q^(−1)Σ_{j=0}^{q−1}u(·+j)||_B=0.

The triangle inequality and shift invariance imply

||u−C||_B≤q^(−1)Σ_{j=0}^{q−1}||u(·+j)−v(·+j)||_B=||u−v||_B.

We can therefore find constants C_k with ||u−C_k||_B→0. Since

|C_k−C_l|≤||u−C_k||_B+||u−C_l||_B,

the constants are Cauchy, so C_k→C and ||u−C||_B=0. In particular u→C in density, by Markov's inequality.

The limit C lies strictly inside (−π/2,π/2). To check this necessary point, choose a periodic approximant a to h with tolerance 1/4. It is bounded, say |a|≤M. The set |h|≤M+1/4 has lower density greater than 3/4. Hence |u|≤arctan(M+1/4)<π/2 on that set, which rules out either boundary value for the density limit C.

Continuity of tan at C now gives h→tan(C) in density. Since h is ordinary additive, Lemma 1 gives h≡0. Thus f=c log everywhere. Finally c<0 would make every n a strict decrease, contradicting density zero. This proves Theorem 3. ∎

### 2.3 An explicit sufficient prime condition, allowing arbitrary prime powers

The theorem includes the following entirely elementary subclass.

**Corollary 4.** Under the original ordinary-additivity and density-zero assumptions, suppose some fixed c satisfies

Σ_p min(1,|f(p)−c log p|)/p < ∞.                                (3)

There is no condition on the values f(p^k) for k≥2. Then f(n)=c log n for every n.

**Proof of the additional assertion.** Set h=f−c log. Ordinary additivity gives h(n)=Σ_{p^k∥n}h(p^k). We show h is periodically approximable. Choose a prime cutoff P. For p>P, divide the primes into L={p:|h(p)|>1} and S={p:|h(p)|≤1}. Three kinds of errors occur when we keep only the valuations at p≤P:

- Numbers divisible by any p∈L with p>P have upper density at most Σ_{p>P,p∈L}1/p.
- Numbers divisible by p² for any p>P have upper density at most Σ_{p>P}1/p².
- Outside these exceptional sets, the omitted terms come from exponent-one primes in S. The average of their sum of absolute values is at most Σ_{p>P,p∈S}|h(p)|/p, since ⌊X/p⌋/X≤1/p. Markov bounds the upper density of an omitted sum exceeding ε by ε^(−1) times this tail.

All three bounds tend to zero as P→∞, by (3) and convergence of Σ_{n≥2}n^(−2). These union bounds are uniform in X; only divisors p≤X can occur.

For the finitely many p≤P, truncate at an exponent K. Let a(n) be the sum of h(p^{v_p(n)}) over p≤P with 1≤v_p(n)<K, with zero contribution when v_p(n)=0 or v_p(n)≥K. This a is periodic with period ∏_{p≤P}p^K. It differs from the untruncated finite-prime sum only when some p≤P has p^K|n, a set of upper density at most Σ_{p≤P}p^(−K), tending to zero as K→∞. For each ε first choose P and then K so the combined bad density is <ε. This proves the definition and hence the corollary. ∎

In particular, finite prime support for the residual is sufficient even with arbitrary, unbounded, non-completely-additive values at the powers of those primes. A summable reciprocal-prime support is also sufficient, regardless of coefficient magnitudes. This corollary does not establish (3) from the density-zero hypothesis.

## 3. What the route fails to establish

The unresolved step is to deduce, solely from |D(X)|=o(X), the existence of one fixed c for which f−c log is periodically approximable in density. Neither this property, nor the sufficient prime-tail condition (3), was established in full generality.

This is a precise structural upgrade. Periodic approximability is an absolute-scale assertion and implies tightness: for any δ>0, some fixed M has upper density {|h|>M}<δ. In contrast, an error o(B_f(X)) may grow without bound and need not give any fixed-scale control. The proof above cannot use a changing c(X): subtracting its increments and choosing one additive residual require a fixed c.

The absolute-o(1) upgrade in Lemma 2 is an alternative sufficient bridge. It too is not supplied by the general density-zero theorem. No claim is made that the two bridges are equivalent without the original almost-monotonicity premise.

## 4. Negative controls against overclaiming

### 4.1 A bounded, genuinely non-completely-additive defect survives normalized approximation

Let h(n)=1 if 2 divides n, and 0 otherwise, and let g(n)=log n+h(n).

- h is ordinary additive: in a coprime product at most one factor is even.
- h is not completely additive: h(4)=1 but h(2)+h(2)=2.
- The fixed-slope, zero-offset approximation |g(n)−log n|≤1 holds for every n.
- On prime powers, Σ_{p^k≤X}|g(p^k)−log p^k|²/p^k=Σ_{2^k≤X}2^(−k)<1.
- B_g(X)→∞, since g(p)≥log 2 on every prime and Σ_p1/p diverges. For completeness, the latter follows because convergence would bound ∏_{p≤y}(1−1/p)^(−1), whereas its expansion contains Σ_{n≤y}1/n, which diverges. Thus both the everywhere error and prime-power squared error are negligible relative to the corresponding B_g scales. The slope 1 is even fixed, so all slow-variation issues disappear in this control.
- Nevertheless g is not a logarithm. Every even n is a strict decrease: g(n+1)−g(n)=log(1+1/n)−1<0. Every odd n is a strict increase. Its decrease density is 1/2.

This is deliberately NOT a counterexample to the target: its exceptional set fails the density-zero assumption. Its role is to show concretely that the normalized approximation conclusions alone do not detect a fixed prime-power defect. Theorem 3 eliminates it once the density-zero premise is also imposed.

More generally, for a prime p, integer k≥1 and A∈{−1,1}, the ordinary additive defect h(n)=A·1_{v_p(n)=k} gives g=log+h with decrease density (p−1)/p^(k+1). For A=1, decreases occur exactly at n with v_p(n)=k; for A=−1, exactly at n with v_p(n+1)=k. Adjacent integers cannot both have positive p-adic valuation, and 0<log(1+1/n)<1 for n≥1. The equality count is periodic modulo p^(k+1). These densities can be arbitrarily small but are not zero.

### 4.2 Slow variation does not establish a fixed slope

For X sufficiently large, λ(X)=log log log X has λ(X^u)−λ(X)→0 for every fixed u>0, but λ(X) diverges. This is only a scalar negative control, not an additive-function construction. It explains why slow variation alone must not be silently replaced by convergence.

### 4.3 The periodic assumption cannot simply be dropped in the averaging proof

The sequence h(n)=log n has positive increments and arctan(h(n+1))−arctan(h(n)) with vanishing Cesàro variation, but h does not have a finite density limit and cannot be periodically approximable in density: it eventually exceeds the finite range of every periodic real sequence. The periodic approximation and tightness step is essential.

## 5. Historical source review and dependency boundary

The original full source is Paul Erdős, *On the distribution function of additive functions*, Annals of Mathematics 47(1) (1946), 1–20, https://users.renyi.hu/~p_erdos/1946-06.pdf. The original report records reading its PDF pages 1–3 in retained text: ordinary real-valued additivity is defined on page 1, and the exact density-zero conjecture is on page 3. It is distinct from the neighboring conjecture on successive differences approaching zero on a density-one sequence.

The retained modern source is Alexander P. Mangerel, *Additive functions in short intervals, gaps and a conjecture of Erdős*, arXiv:2108.12351v1 (27 August 2021), https://arxiv.org/abs/2108.12351v1. The original report records reading its introductory definitions and results through Theorem 1.9, the complete printed proofs of Theorem 1.8 (both parts), Corollary 1.7 and Theorem 1.9, Lemmas 7.3–7.7, Proposition 7.1 and Corollary 7.8 in the retained text. This does not claim that every upstream theorem from other cited papers has been inspected or independently accepted.

Precisely:

- Corollary 1.7 assumes complete additivity, the stated normalized prime-tail variance condition, and |B(X)|≪X/(log X)^(2+δ). Its proof reaches an absolute averaged gap o(1), then invokes the Kátai–Wirsing characterization quoted as Theorem 2.7. This is not a theorem for the unrestricted target.
- Theorem 1.8 assumes the class A_s and obtains variance-relative approximation on prime powers with a slowly varying slope. It is not applied to a general ordinary additive function here.
- Theorem 1.9 treats ordinary additivity and density-zero decreases, but its error is o(B_f(X)), with scale-dependent slope and offset. Its complete concluding argument was inspected. It does not supply the absolute approximation required in Lemma 2 or the periodic residual required in Theorem 3.
- Formula (25) in Lemma 7.5 shows the source's basic estimate: average absolute gaps are bounded by a constant times B_f(X)(sqrt(|B(X)|/X)+log X/sqrt X). The hypothesis alone does not make that product tend to zero.

These source results are contextual comparisons only, not mathematical dependencies of Lemmas 1–2, Theorem 3, or Corollary 4. Those authored statements were proved above using elementary density counts, additivity, periodic averaging, bounded transforms, elementary probability/Markov bounds, and convergent series. No uninspected external proof is imported into the authored conclusions.

These are historical, version-specific comparisons, not an audit of the complete external papers or all their cited proof chains. SOURCES.json separately records the candidate's inspection history and the independent auditor's narrower confirmed inspection. This edition does not independently establish every historical inspection assertion. Neither source is an external-theorem dependency of the authored conditional proofs.

## 6. Historical supporting checks

The original standard-library checks used exact integers and rational arithmetic for finite boundary examples and deliberately incorrect claims. The retained receipts report identical substantive results in normal, -O, and -OO modes: 42,871 coprime pairs, 9,840 finite cycles, 24 isolated prime-power examples, 29 dilation examples, nine rejected mathematical controls, and five rejected manifest-tampering controls in each mode. Logarithmic signs are justified by the written bound 0<log(1+1/n)<1, not floating-point logarithm tests.

The independent audit reconstructed the stated finite arithmetic without importing or executing the candidate program. Its additional tests and evidence identities are summarized in AUDIT.md and VERIFICATION.json. The receipts are historical evidence; edition preparation reauthenticated their bytes without replaying those mathematical programs. The general implications rest on the complete proofs above rather than finite extrapolation.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the original report and its separately retained supporting checks. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No mathematical correction was required.

The authored conditional theorem, lifting lemmas, prime-tail corollary, and boundary examples are fully proved in this edition. Their proofs are self-contained and do not depend on omitted computational certificates or external analytic theorems. Finite checks are supporting tests, not proofs of asymptotic implications. The edition omits executable code, raw computational certificates, copied source text and PDFs, and private coordination material. Hashes establish identity and integrity, not mathematical truth.

The unrestricted EP 1122 / 2503 problem remains unresolved by this work. No counterexample to that unrestricted problem, novelty, priority, or exhaustive current literature-status claim is made. Historical source inspection and independent audit are distinguished from edition preparation: no new scholarly-source retrieval or inspection and no new mathematical computation were performed for this edition. Local packaging checks establish the identities and scope of the distributed files only.
