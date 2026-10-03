# Independent adversarial audit: compact linear domino games

Problem 30005528 · OWR-13750333-009 · rank 492  
Audit date: 3 October 2026

## Verdict

**PASS_FULL_LITERAL_TARGET.** The frozen packet gives a complete counterexample to universal periodic minimization for the abstract game in Felipe Gonçalves's Question 1, printed p. 1254 of Oberwolfach Report 22/2023. Equivalently, it supplies the game that the question requests. Recommend **solved by counterexample, one substantive approach out of the five-approach budget**, with the exact source boundary retained.

There are no blocking findings or required mathematical corrections. All six release files matched their frozen hashes before and after examination. The author checker was replayed in a temporary copy and reproduced its recorded output byte for byte. Independent exact-arithmetic controls passed 47,513 checks, including six rejected code mutations. Counts are coverage information, not proof of an infinite claim.

This verdict does **not** settle the motivating interval-packing problem, Gonçalves–Vedana Conjecture 4, or any claim of historical priority. It does not authorize uploading source documents or private research material. No remote writes or publication were performed in this audit.

## 1. Source identity and literal target

The primary source is Felipe Gonçalves, *Linear domino size problem*, Question 1, printed p. 1254, in *Group Actions and Harmonic Analysis in Number Theory*, Oberwolfach Reports 20 (2023), report 22/2023, pp. 1195–1262. [Official report](https://ems.press/content/serial-article-files/47016), [DOI](https://doi.org/10.4171/OWR/2023/22). The problem session credits Jens Marklof as chair and Paul Nelson for notes.

The page was inspected as local extracted text and a rendered image, then independently corroborated from the official EMS PDF, PDF page 60. It defines arbitrary symbols, ordered-pair tiles, and a size function. Sequences are indexed forward from 1 and obey exact endpoint matching. The objective is the limsup of the first left-endpoint cost plus the next N right-endpoint costs, divided by N. Question 1 requests an infinite compact topological alphabet, continuous positive size, and strict inequality between every periodic sequence's average and the unrestricted infimum.

No condition there requires an interval alphabet, injective size, symmetric tiles, a distance-packing realization, or a finite tile set. Closedness of tiles is not required; the submitted example supplies it anyway. The annulus alphabet is therefore admissible. The source's informal compactification example is not used as a premise of the submitted proof. [Source, p. 1254](https://ems.press/content/serial-article-files/47016#page=60).

## 2. Construction and all legal sequences

The audited construction is exactly

\[
\Sigma=S^1\times[0,1],\qquad s(z,t)=1+t,
\]
\[
F(z,t)=(e^{2\pi i(\sqrt2+t)}z,t),\qquad
T=\{[x,F(x)]:x\in\Sigma\}.
\]

The earlier angle sketch mentioned outside the frozen packet is not an input to this verdict. The frozen construction uses the increasing angle **√2+t**.

The alphabet is an infinite compact connected metric space. The size is continuous and takes values in [1,2], so both positive and nonnegative conventions for the codomain are satisfied strictly. The formula for the inverse rotation is continuous. Thus F is a homeomorphism. Its graph is compact and closed in the Hausdorff product space. There is exactly one legal successor and predecessor for each symbol.

Take an arbitrary legal sequence with initial symbol x=(z,t). Exact matching and the graph definition force its j-th tile to be [F^(j−1)(x),F^j(x)]. This is an induction, not a restriction to a preferred class of legal words. Conversely, every such orbit defines a legal word. Consequently there are no additional height-changing paths, discontinuous choices of successors, or exceptional non-orbit words that could evade the objective calculation.

All symbols in that word have size 1+t. Its exact N-tile prefix average is

\[
\frac{N+1}{N}(1+t).
\]

The ordinary limit exists and equals 1+t, hence agrees with the source limsup. The extra initial cost has not been dropped. Dividing instead by N+1 would give the same limiting value but would not reproduce the printed finite-prefix formula; the submitted packet uses the correct formula. No reciprocal-density or liminf/limsup interchange is needed anywhere.

## 3. Attainment and the universal periodic quantifier

Because 0≤t≤1, the global infimum is 1. For every z on the circle the orbit (z,0) exists, so the infimum is attained. Conversely, an orbit attaining 1 must have t=0. This proves the assertion about **all** minimizers, not merely one aperiodic minimizer.

Iteration gives

\[
F^p(z,t)=(e^{2\pi i p(\sqrt2+t)}z,t).
\]

Periodicity here means exact repetition of the ordered tiles. Repetition with period p implies equality of their first coordinates and therefore F^p(x)=x. The converse follows by iterating F. As z has modulus one, it is never zero; the return condition is precisely p(√2+t)∈Z. The word is periodic for some positive integer p if and only if √2+t is rational.

At height zero this is impossible, since √2 is irrational. The parity proof of irrationality in the packet is sufficient and valid. Every periodic word therefore has t>0 and average 1+t>1. This is the exact strict inequality needed in the source, without a bounded-period or finite-sample qualifier.

The eventual-periodicity strengthening is also valid: a return after a transient gives F^(m+p)(x)=F^m(x), and applying F^−m yields a return from x. All minimizers fail even eventual periodicity.

The source is one-sided. If a reader imposes a bi-infinite convention instead, every point still has a unique full orbit because F is invertible; all heights and all averaging calculations remain constant. The counterexample is robust to that extension, although the audit does not need to substitute it for the printed convention.

An important semantic boundary is preserved: the **numerical size sequence** is constant even on an aperiodic orbit. Periodicity in the problem is that of tiles/symbols, not of their real-valued scores. Identifying symbols solely by their equal size would change the game.

## 4. Periodic competitors, density, and the gap

The permitted periodic heights form

\[
(\mathbb Q-\sqrt2)\cap[0,1].
\]

They are dense in [0,1], including arbitrarily close to both endpoints, by translation of the dense rationals. At every such height every starting point on the circle is periodic. A product basis for S¹×[0,1] then proves density of periodic starting points in the whole alphabet. Neither endpoint itself is periodic; density does not require that.

For n≥1, let m_n=⌊n√2⌋+1 and t_n=m_n/n−√2. Irrationality ensures 0<t_n<1/n≤1. In particular n=1 is admissible. The angle is m_n/n and its reduced denominator n/gcd(m_n,n) is its least period, for every initial point. The heights need not be monotone; their bound suffices to prove t_n→0. Thus the periodic costs have infimum 1 without attaining it, and the universal inequality is not vacuous.

For a rational angle r=p/q in lowest terms and 0<t=r−√2≤1, p²−2q² is a strictly positive integer. Rationalization gives

\[
t=\frac{p^2-2q^2}{q^2(r+\sqrt2)}
\geq\frac{1}{(2\sqrt2+1)q^2}.
\]

If q≤Q, replacing q² by Q² preserves the lower-bound direction. Hence costs approaching 1 must have unbounded least periods. The argument is exact and has no hidden numerical separation assumption. Compactness does not make the union of all finite-period sets closed; it is consistent for periodic starting points to converge to an aperiodic minimizer.

The annulus coordinate change is also correct. The map (z,t)↦(1+t)z has continuous inverse u↦(u/|u|,|u|−1) on 1≤|u|≤2. It preserves the score, graph relation, and all orbit assertions.

## 5. The later packing paper is outside the solved claim

The related primary source is F. Gonçalves and G. Vedana, *Sphere packings in Euclidean space with forbidden distances*, Forum of Mathematics, Sigma 13 (2025), e49, pp. 1–35, [DOI 10.1017/fms.2025.9](https://doi.org/10.1017/fms.2025.9). The local published text was checked against the [official Cambridge PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8980920479977FE37DB355A8E601A5A8/S205050942500009Xa.pdf/sphere_packings_in_euclidean_space_with_forbidden_distances.pdf). Direct DOI retrieval failed, but official-PDF retrieval succeeded.

Conjecture 4 on p. 10 concerns maximal-density periodic packings for compact K⊂[1,∞) containing 1. Section 4's packing construction uses fixed-length blocks with conditions on every consecutive subword sum. Theorem 13 on p. 17 assumes a finite domino set and additional norm hypotheses; it does not claim the submitted infinite graph has a periodic optimizer. The paper's broader discussion of a compact-alphabet generalization does not supply a reverse realization theorem for every abstract graph. [Published paper, pp. 10, 16–17](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8980920479977FE37DB355A8E601A5A8/S205050942500009Xa.pdf/sphere_packings_in_euclidean_space_with_forbidden_distances.pdf).

The audited construction provides no such K and no packing realization. A counterexample among arbitrary ordered graphs cannot be transferred to that structured subclass without an additional argument. All statements excluding the packing problem are necessary and correctly retained.

## 6. Reproducibility and independent controls

The original checker is standard-library-only and uses fractions and the quadratic field Q(√2). Its sign comparator correctly handles zero, equal signs, and opposite signs; in the latter case squaring absolute values is valid. The coefficient identity for 1/(2√2+1) is correct.

An isolated, unmodified copy of the author script reproduced its recorded JSON byte for byte, including:

- 256 explicit periodic competitors;
- 23,955 candidate periods below their claimed least periods;
- 1,280 finite-prefix normalization instances;
- 5,022 reduced rational-angle instances with denominator at most 128;
- 5,022 associated bounded-period-gap checks.

The separate `audit_controls.py` independently encloses √2 between two rational numbers certified by exact squaring. It uses those enclosures rather than the author's sign algorithm to check 5,625 quadratic-field sign cases and the height/gap inequalities. Its rational-angle count is independently checked against the sum of Euler totients through 128. Period returns are tested by integer divisibility, and normalization is recomputed from coefficient sums.

It additionally rejects six isolated code mutations: using the unreduced period, approximating from below, omitting the initial symbol cost, reversing the height sign, corrupting rationalization, and reversing the sign comparator. Simple boundary controls show why rational α, constant costs, or adding reverse tiles could destroy the desired conclusion. In particular, a symmetric tile relation would admit bottom-circle two-cycles; such symmetry is neither claimed nor required.

The controls perform 47,513 checks in total, including byte/inventory guards. That number includes repeated finite instances and is not evidence of novelty or a replacement for the proofs of irrationality, compactness, density, or the all-period quantifier. The script executes and mutates only temporary copies. It checks the six frozen input hashes again at the end.

To replay from this audit directory:

    python3 -B audit_controls.py --release ../release

Only Python's standard library and the six frozen release files are needed. No source PDFs, network connection, secret, environment-specific location, or private corpus is needed.

## 7. Attribution, limitations, and release gate

The problem is attributed to Gonçalves, and the 2025 paper to Gonçalves and Vedana. Irrational circle rotations are elementary standard constructions. Targeted independent searches for the problem title, linear-domino irrationality, and the related paper did not identify a prior publication of this exact counterexample. This limited search establishes no priority, novelty, exhaustive literature coverage, or continuing open status of the packing conjecture.

The source, theorem, and checker gates all pass. The accepted resolution is confined to the literal compact-alphabet ordered-pair question. No additional attempts are needed merely to exhaust an attempt budget after a full proof passes review.

Portable audit allowlist:

- `AUDIT_REPORT.md`
- `FROZEN_INPUTS.json`
- `audit_controls.py`
- `audit_controls.json`
- `AUDIT_MANIFEST.json`

Source PDFs, rendered source pages, full extracted texts, private source records, search work, and other research files are excluded. The frozen author release remains unchanged.
