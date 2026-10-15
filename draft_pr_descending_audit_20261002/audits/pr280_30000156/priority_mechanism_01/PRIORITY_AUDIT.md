# Independent priority audit: multiplicative triangular mechanism

Audit date: 2026-10-06 UTC. Original head: `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`. Target: PR280 / problem30000156. This review concerns priority and claim framing only. ROOT's accepted mathematical/source audit is an input, not a novelty decision.

## Finding

**No verified earlier publication negating the exact original point-period limit assertion was found within this bounded mechanism audit. Historical novelty remains uncertified.** The map family, its finite-field permutation mechanism, primitive-value character estimates, and substantial arithmetic oscillation behind the example are established prior work. The possible contribution is the explicit application of these ingredients to the literal 2004 universal conjecture, together with the written unconditional fixed-map CDF separation. It must not be described as a new triangular-map construction or a new primitive-root/totient theorem.

The search covered 62 exact queries, primary-paper reference chains, 22 distinct downloaded primary PDF bodies, and the specific result bodies listed below. Full download is distinguished from selected-page reading. The source hashes, failed retrievals, and exact page reading scopes are in `SOURCE_RECEIPTS.json` and `READING_RECEIPTS.json`; all source bodies and rendered images remain in ignored `private_reading/`. `SEARCH_COVERAGE.json` records every query. No people were contacted and no remote state was changed.

## Exact comparison target and falsification criteria

The unchanged submission gives the fixed rationally invertible map

\[
L(u,v)=(u,(u^2+1)v),\qquad L^{-1}(u,v)=(u,v/(u^2+1)).
\]

For every prime \(p\equiv3\pmod4\), it is a permutation of the whole affine plane. Its generic fibers are rational curves, its invariant is \(u\), and the period of every point with \(v\ne0\) is \(\operatorname{ord}_p(u^2+1)\). If \(P_p\) counts those \(u\) for which \(u^2+1\) is primitive, the submitted proof establishes

\[
P_p/p=\varphi(p-1)/(p-1)+o(1).
\]

For each fixed \(x\in[1/2,1)\), it proves, through this same prime class,

\[
D_p(x)=p^{-2}\#\{z:T_p(z)\le px\},\qquad
\limsup D_p(x)=1,\quad \liminf D_p(x)\le23/24.
\]

The priority collision sought was an earlier checked theorem or explicit example showing failure of this ordinary fixed-map, point-weighted, p-scaled CDF limit for a map admitted by the broad original question. An earlier equivalent map with that same application would suffice. A map family containing the formula, primitive-value counts, arithmetic nonconvergence alone, a prime-averaged law, a fixed orbit law, or ensemble permutation statistics are comparable ingredients, but do not alone establish priority of the target-negative application.

The [two-page 2004 source](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf), p.1 equation (1) and Conjecture 1, explicitly defines the point-weighted p-scale distribution and says the limit exists for any birational map. Its p.2 heuristic specifically uses genus-one translations and an elliptic Artin analogue. This audit preserves the literal broad assertion. It does not turn the genus-one heuristic into an unstated hypothesis.

## Closest established mechanisms

### The formula is a specialization of an established triangular family

[Ostafe–Shparlinski, 2009 preprint / Math. Comp. 2010](https://arxiv.org/pdf/0902.3884v3), §2.1, equations (1)–(4), PDF pp.2–3, give polynomial systems

\[
f_0=X_0g_0(X_1)+h_0(X_1),\qquad f_1=aX_1+b.
\]

Swapping the candidate coordinates gives \((v,u)\mapsto(v(u^2+1),u)\), obtained with \(a=1,b=0,g_0=X_1^2+1,h_0=0\). This specialization is the reviewer's inference from their displayed family; the retrieved paper does not display the candidate as an OWR counterexample. The paper's principal conclusions concern degree growth and orbit exponential sums/discrepancy. Thus family priority is established; target-negative application priority is not established by this source.

Their [2011 preprint / 2012 rational-systems paper](https://arxiv.org/pdf/1109.0575), equation (5), and §§5–6, PDF pp.10–14, continue the family and give short-trajectory bounds and Möbius reductions of rational triangular systems. These are genuine dynamics results, but the inspected statements do not give prime-by-prime nonconvergence of the candidate point-period CDF.

[Roy–Steiner, arXiv2204.01802v6, 2023](https://arxiv.org/pdf/2204.01802v6), Definition 7 and Proposition 8, PDF p.6, give generalized triangular permutations with nonvanishing multiplier polynomials, inverted by solving coordinates successively. Their §4.4, equation (21), PDF p.13, explicitly includes a family whose last coordinate is fixed and whose earlier coordinates are multiplied by zero-free polynomials in later coordinates. This contains the swapped candidate. Equation (22), PDF p.14, uses quadratic multipliers with nonsquare discriminant. It establishes prior use of the quadratic no-root device as well. The inspected bodies analyze cryptographic properties, not the target CDF limit.

**Consequence:** calling the construction, coordinate-wise inversion, or quadratic zero-free trick novel would be unjustified. A specific publication containing a family is not evidence that its authors previously singled out the same formula and disproved the 2004 conjecture.

### The torus and linearization mechanism are classical

[Colón-Reyes–Jarrah–Laubenbacher–Sturmfels, Complex Systems 16 (2006), 333–342](https://wpmedia.wolfram.com/sites/13/2018/02/16-4-4.pdf), printed pp.336–337, Lemma 2 and Corollary 3, show that a monomial map on \((\mathbb F_q^*)^n\) is conjugate by discrete logarithms to its exponent matrix on \((\mathbb Z/(q-1))^n\), preserving cycle lengths. Thus the torus map \((u,v)\mapsto(u,uv)\) corresponds to the unipotent exponent matrix \(\left(\begin{smallmatrix}1&0\\1&1\end{smallmatrix}\right)\). This particular specialization is our inference, not an example displayed in the retrieved paper. The paper's main theorem is a fixed-point-system criterion. The torus formula has an affine zero-fiber problem; the candidate's zero-free multiplier removes it on its stated prime class.

[Sakzad–Sadeghi–Panario, 2012 author preprint](https://arxiv.org/pdf/1011.1539), §3.4, Theorem 3.9, PDF p.8, records classical Möbius cycle structures in terms of multiplicative orders of eigenvalue ratios, crediting an earlier source. This confirms that genus-zero cycle lengths governed by multiplicative order are established. It is a fixed-field/interleaver result, not a varying-prime CDF obstruction.

[Gerike–Kyureghyan, 2020](https://d-nb.info/1210002604/34), Theorem 1 and Proposition 1, PDF p.3, study permutations preserving parallel affine lines; Lemma 3, p.9, computes a multiplicative-order cycle length on a distinguished line. Their later invariant-cycle-type results impose 1-homogeneity absent here. The general fiber-permutation viewpoint is comparable; the inspected statements give no exact target-negative result.

### Primitive quadratic values are established character-sum arithmetic

[Booker–Cohen–Sutherland–Trudgian, 2018 preprint / Math. Comp. 2019](https://arxiv.org/pdf/1803.01435v2), §2, PDF pp.3–4, use the classical e-free multiplicative-character indicator, obtain a double character-sum formula for primitive quadratic values, and state square-root character estimates in Lemma 1. Setting their first primitive-input condition trivial gives the same kind of primitive-value count needed for \(u^2+1\). Their main theorem is the stronger simultaneous primitive-input/primitive-output existence result, with exact small exceptions. This is prior arithmetic machinery, not a dynamics counterexample.

The submission itself derives its indicator and Jacobi estimates and disclaims a new analytic-number-theory theorem. That disclaimer is supported by this comparison.

### Totient oscillation and maximal-order densities predate the submission

[Aivazidis–Sofos, arXiv1308.5701v2, 2014](https://arxiv.org/pdf/1308.5701v2), equation (1.1), p.1, give the maximal-order element density

\[
p_n(q)=\frac1n\frac{\varphi(q^n-1)}{q^n-1}.
\]

Their p.2 explicitly says that the ordinary limit does not exist as \(q\) runs through prime powers with \(n\) fixed. For \(n=1\), this is precisely the primitive-element density. Theorem 1.3(i), p.3, gives a continuous empirical distribution law; its proof on pp.16–17 treats primes first and then shows prime powers have the same empirical law. These are extremely close arithmetic antecedents. They do not build a fixed planar rational map, restrict to \(p\equiv3\pmod4\), or negate the OWR point-period claim. The ordinary nonlimit assertion is about prime powers, so this audit does not silently substitute the candidate's restricted prime sequence for their stated parameter set.

[Deshouillers–Hassani, J. Aust. Math. Soc. 93 (2012), 77–83](https://doi.org/10.1017/S1446788712000250), Theorem 1.1 and Proposition 2.1, printed pp.78–79, establish nontrivial empirical shifted-prime totient distributions and progression-conditioned versions \(p\equiv1\pmod m\). Theorem 1.1 gives large one-sided variation at every \(\varphi(m)/m\) for even \(m\). These statements are arithmetic laws, not the candidate's fixed-map CDF. The progression statement is not cited as though it directly states the \(3\pmod4\) law.

[Kátai, Compositio Math. 19 (1968), 278–289](https://www.numdam.org/item/CM_1968__19_4_278_0.pdf), actual Theorems 1–2 on printed p.279 and explicit examples on p.288, concern \(g(p+1)\), \(f(p+1)\), and the distribution of \(\varphi(p+1)/(p+1)\). Later primary papers cite its shifted-prime application to \(p-1\). The retrieved original typography was checked visually; this audit does not misreport its displayed \(p+1\) formulas as displayed \(p-1\) formulas.

[Pillai, Proc. Indian Acad. Sci. A13 (1941), 526–529](https://www.ias.ac.in/public/Volumes/seca/013/06/0526-0529.pdf), Theorem I on p.526 and its proof on p.528, establish \(\sum_{p\le x}\varphi(p-1)=A\operatorname{Li}(x^2)+O(x^2/(\log x)^m)\), with \(A=\sum\mu(n)/(n\varphi(n))\). Partial summation yields the familiar prime-average totient-ratio mean. This deduction is independently ours; Aivazidis–Sofos Remark 1.2 explicitly identifies Pillai's theorem as an equivalent earlier form of the n=1 mean credited also to Stephens 1969. Hence a historical credit chain should include Pillai, rather than imply the underlying mean originated with the present argument.

A recent [2026 preprint v1](https://arxiv.org/pdf/2603.11196v1), Theorem 3, PDF p.6, uses Dirichlet primes in classes \(1\pmod{\text{primorial}}\) to make a primitive-determinant density tend to zero; §§5.1–5.2, pp.9–13, transport shifted-prime totient laws to another density. It supplies a recent independent arithmetic application, not a cycle-statistics counterexample. Only v1 was read; the later title/version was not represented as its body.

## Adjacent results do not silently change the target

[Maubach arXiv1106.5800](https://arxiv.org/pdf/1106.5800), p.2, defines polynomial automorphisms by formal polynomial inverse and strictly triangular maps by additive coordinates. [Maubach arXiv1307.6469](https://arxiv.org/pdf/1307.6469), p.3, defines triangular polynomial automorphisms with constant coordinate multipliers. The candidate's Jacobian is \(u^2+1\) and its inverse is rational. These automorphism classes are narrower, even though the candidate is an affine-plane permutation at the stated primes. Their finite-field maximal-cycle results do not cover the accepted map as a formal polynomial automorphism.

[Roberts–Vivaldi 2005](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Symmetry.pdf), §2.2, author p.6, likewise explicitly requires a polynomial inverse and constant nonzero Jacobian. Its dynamically nontrivial class excludes maps conjugate to affine or elementary maps. Those restrictions cannot be retroactively inserted into the broad OWR claim.

[Jogia–Roberts–Vivaldi 2006](https://web.maths.unsw.edu.au/~jagr/IntegrabilityRS.pdf), author pp.13–15, derives elliptic translation period windows, formulates a fixed-orbit density conjecture, and separately discusses a point-sampled family of elliptic curves. The text recognizes genus-zero curves but does not give the candidate negative conclusion. [Roberts's 2012 survey](https://www.dma.uvigo.es/~eliz/pdf/Roberts.pdf), §4, continues to present fixed-map distribution signatures experimentally and distinguishes them from ensemble results.

[Sha–Hu, 2011](https://arxiv.org/pdf/0910.5550v5), Proposition 2.5, p.4, gives monomial cycle counts, and §§3–4 discuss averages. Proposition 4.9, p.18, proves nonexistence of an asymptotic mean of fixed-point counts over prime ideals of a function field. This is a verified earlier failure of a different finite-field dynamics average, so nonconvergence in finite-field dynamics generally is not new. Its field parameter, mean statistic, and map \(x\mapsto x^n\) differ from the target.

[Shparlinski 2007](https://arxiv.org/pdf/math/0607779v3), §§2.6 and 3, PDF pp.12–14, corrects Arnold conjectures and studies multiplication by a fixed integer on residue rings. Theorem 3.4 is explicitly conditional on ERH and concerns average multiplicative order over integer moduli. This must not be confused with the candidate's unconditional averaging over all fiber multipliers.

[Arnold’s 2003 survey](https://www.mathnet.ru/eng/rm641), *Topology and statistics of formulae of arithmetics*, §1, printed pp.638–641, and §10, p.663, provides an actual earlier body on multiplicative period statistics. §1 records equal cycle lengths for multiplication by a fixed group element and expressly treats the plotted asymptotics as unproved observations. §10 reports finite fixed-base-2 computations for odd n≤2001 and smooths periods by Cesàro sums. The inspected sections give no ordinary planar point-CDF obstruction. The body was recovered through a fresh official full-text endpoint after the stale indexed PDF link failed; printed p.663 was visually checked. This survey does not substitute for the two distinct inaccessible original papers below.

## Unavailable bodies and scope limits

Two potentially relevant Arnold primary bodies were not recovered: *Fermat–Euler Dynamical Systems and the Statistics of Arithmetics of Geometric Progressions* (2003), DOI10.1023/A:1022915825459, and *Ergodic and arithmetical properties of geometrical progression's dynamics and of its orbits* (2005), DOI10.17323/1609-4514-2005-5-1-5-22. MathNet and AMS metadata identify the latter as multiplication by a fixed constant modulo n, but metadata is not a result-body exclusion. MathNet full-text and AMS PDF endpoints returned HTML/unavailable responses; the Dauphine preprint endpoint returned404. These are real body gaps in the broader mechanism history. They do not reopen the accepted mathematics, but they limit any comprehensive priority claim.

A 2011 Roberts/Neumärker/Viallet/Vivaldi birational-dynamics manuscript appeared as a bibliographic lead; no actual body was recovered. A 2012 thesis search result describes related rational-map experimental work as in preparation. This audit neither treats an unpublished title as a prior proved counterexample nor asserts that its unknown body contains none. Latest GTDS/eprint2024/1316 was unavailable, but the accessible 2023 full preprint already verifies the relevant family definitions; that version gap is not necessary to the family-priority finding. The original Stephens1969 body was not recovered here; Pillai1941 and Aivazidis–Sofos provide actual earlier primary-body mean evidence.

## Verdict and concrete framing

The exact-application priority question remains open after a substantial, bounded independent search. No exact earlier negative result was verified. Strongest verified historical findings are: an older family contains the formula; quadratic zero-free multipliers are established; primitive-value arithmetic and primitive-element density fluctuations are established; earlier finite-field nonconvergence results exist for different statistics.

The unchanged submission already says that historical novelty is not certified and limits its result to the literal broad 2004 assertion. Retain those limits. A review or eventual write-up should credit the closest mechanism sources above, especially Ostafe–Shparlinski, Booker–Cohen–Sutherland–Trudgian, Aivazidis–Sofos, and Pillai. It should identify its possible novelty as the explicit target-negative fixed-map application and full unconditional point-CDF argument. It should not claim classification, new arithmetic, or resolution of narrower polynomial-automorphism, elliptic-family, or random-involution statements.

Assigned bounded audit completion: **100%**. Worldwide priority certainty: **unknown**, not a percentage certified by this search.
