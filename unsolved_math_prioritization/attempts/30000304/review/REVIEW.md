# Independent review: regenerative allelic partitions, 30000304

## Verdict

**PASS_SCOPED_REGENERATIVE_OBSTRUCTIONS.** No mandatory mathematical correction was found. The four-sample necessary identity, its unique-candidate-mutation-rate consequence, the five-sample failure of sufficiency, and the all-sample bounded-parent full-replacement exclusion are valid under their stated hypotheses.

The full simultaneous-merger conjecture remains **unsolved, 3/5**. This review does not promote the earlier non-simultaneous Λ-coalescent classification, a finite table of identities, or the bounded-parent special case to a general Ξ theorem. Priority remains unestablished. This is an adversarial AI review, not human peer review.

Reviewed artifact: `PARTIAL_RESULT.md`, SHA-256
`ce74df1f2b5270b1327d7f729b621cb7e198ddf7531c046c37fd7e2131607178`.
The author's file was read but not edited. All 1,328 submitted exact assertions reproduce byte-identically. An independently implemented active/frozen-state calculation and symbolic audit pass **583 additional assertions**.

## 1. Exact source and imported results

The full Möhle contribution in [OWR 40/2005](https://ems.press/content/serial-article-files/46019?nt=1), printed pp. 2279–2282, was read. Printed p. 2281 was also visually inspected. It explicitly separates the established Λ-only classification from the conjecture for simultaneous multiple collisions. Mutation is independent at rate r>0 along each ancestral branch, with infinitely many possible new alleles. The paper's compatible family of simplex measures is not an arbitrary array of independent parameters.

[Dong's primary extension](https://arxiv.org/abs/0707.1606), Section 2, equations (6)–(9), gives the modern Ξ representation and the rate of each specified merger pattern. Its discussion of mutation/freezing and the first-event recursion was read. The normalization Ξ₀(dx)/S₂(x), with a separate Kingman atom, agrees with the candidate. This supplies the appropriate simultaneous-merger input; no non-simultaneous theorem is silently substituted.

[Gnedin–Pitman](https://arxiv.org/abs/math/0307307), Definition 1.1, Theorem 5.2, equations (23), (25), (26), (35), and Corollary 7.3 were checked in the full primary text. The representation allows drift and a killing atom at x=1. Corollary 7.3 is an **at-most-one** assertion, not an existence assertion for a regenerative arrangement. The candidate correctly tests every possible sampling-consistent regenerative ordering, rather than merely testing chronological freezing order.

The [official publisher abstract of Möhle's 2007 paper](https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/on-a-class-of-nonregenerative-sampling-distributions/2627C00F8167D0718FE80B4C54D54055) explicitly states the Λ-coalescent result. Its final full journal text was not obtained in this review. The same scope is already visible in the full OWR contribution and in Proposition 4 of the retrieved [Lagerås paper](https://staff.math.su.se/andreas/ECP-2007-1844.pdf). The latter also distinguishes regenerative litters from allelic families; combining litters does not provide a counterexample to the target.

A bounded literature check also found a [short earlier conference abstract](https://www.math.uni-bielefeld.de/~trutnau/abstractbio.html) with broader-sounding wording. It provides no precise all-Ξ classification theorem or proof and does not supersede the explicit conjecture and Λ-only published statement. This review makes no exhaustive current-literature or priority certification.

## 2. Specified rates and mutation recursion

The factor for double-pair mergers is correct. For one specified partition of four lineages into two pairs, the paintbox probability is

$$\sum_{i\ne j}x_i^2x_j^2=S_2^2-S_4.$$

There are three specified pairings, so their total rate is 3d, not d or 6d. The remaining entries are also correct:

$$\lambda_{3;2;1}=a-b,\qquad
\lambda_{4;3;1}=b-c,\qquad
\lambda_{4;2;2}=a-2b+c-d.$$

Summing multiplicities gives $g_3=3a-2b$ and $g_4=6a-8b+3c-3d$. All table entries are nonnegative for an admissible Ξ measure. No positivity is inferred merely from arbitrary formal values of a,b,c,d.

For monomorphism, any freezing before only one active ancestral block remains makes the event impossible. The displayed recursions for P₂,P₃,P₄ therefore follow from the effective merger block counts. In particular a simultaneous double pairing leaves two active ancestral blocks and contributes $3dP_2$.

For all-singleton alleles, any merger is fatal, and the first effective event must be one of n singleton freezes. After deleting that frozen singleton, the remaining active process has the same mutation rate and coalescent law. Thus $E_n/E_{n-1}=nr/(g_n+nr)$. The rate is per active ancestral block, not multiplied by the number of sampled descendants carried by that block.

Finite-sample effective rates remain finite even if the underlying paintbox event measure is infinite. The argument uses those finite rates in Proposition 1 and does not require a global first paintbox event there.

## 3. Necessary regeneration identity

Because the all-singleton composition has only one size sequence, any regenerative ordering must satisfy

$$Q(n,1)=E_n/E_{n-1}.$$

Gnedin–Pitman's singleton identity then gives exactly

$$\frac{\Phi_n}{\Phi_{n-1}}=
\frac{g_n+nr}{g_n+(n-1)r},\qquad \Phi_1=1.$$

All denominators are positive for r>0. The binomial-difference identity for $Q(n,n)$ gives the candidate's necessary monomorphic probability. The independent symbolic calculation verifies the full rational identity

$$P_4-P_4^{\rm reg}=
\frac{2r\{3d(a+r)-2b(a-2b+c)\}}
{(a+2r)(3a-2b+3r)(6a-8b+3c-3d+4r)}.$$

Thus the stated four-sample equation is necessary. If d>0 it permits at most the single displayed positive candidate rate. Nothing in this calculation establishes sufficiency.

The d=0 reduction is also valid: it gives the product of the two nonnegative Λ-integrals $\int x\,d\Lambda$ and $\int(1-x)^2\,d\Lambda$. Its vanishing forces support at one endpoint (including the zero-measure degeneracy) and excludes a nontrivial mixture of the two endpoints. This is a credited check against the prior theorem.

## 4. Five-sample witness

The two paintbox event intensities 10 and 1 correspond to the stated Ξ masses 5/2 and 1/2; there is no confusion between Ξ mass and event rate. The independently derived moments are

$$(a,b,c,d)=(3,3/2,3/4,1/8),\qquad r=3.$$

At five active blocks, the exact rates to 4,3,2,1 blocks are 25/8,25/8,5/2,3/8. A separate continuous-time recursion tracking active block sizes and already frozen block sizes, rather than the author's EPPF recursion, obtains

$$P_5=2857/30687,\qquad P_5^{\rm reg}=934/10229,
\qquad P_5-P_5^{\rm reg}=55/30687.$$

The same independent computation matches **every unordered shape** through sample size four, so this is a genuine warning against sufficiency of the early test, not a rate-normalization artifact.

## 5. Bounded-parent full replacement

The uniform parent bound and full-replacement assumption imply $S_2\ge1/M$. Thus the event intensity K is finite and positive. This justifies using a first paintbox time T in Proposition 2, unlike the unrestricted case.

There are infinitely many singleton mutations before T in the infinite population, but the proof does not assume a first global mutation time. It works coordinatewise: independently retained lineages have conditional density $e^{-rT}$, and their parent choices give frequencies $e^{-rT}x_i$ by the conditional strong law. Full replacement removes all active dust at that event. Subsequent mergers and freezes cannot increase the number of positive-frequency ancestral blocks. The finite active process terminates almost surely because mutation remains positive. The final partition consequently has at most M positive-frequency alleles.

If a first-event vector has at least two positive coordinates, the probability that all its m active blocks freeze before the next paintbox event is the displayed positive product $\prod_{k=1}^m kr/(K+kr)$. This gives at least two positive-frequency terminal alleles with positive probability.

The exchangeable paintbox formula gives $p(2,2)>0$, while the bound M forces the EPPF with M+1 twos to vanish. The factor 3 between $p(2,2)$ and the composition probability of (2,2) is correct. Any regenerative arrangement would therefore have $Q(4,2)>0$, forcing positive mass of its Lévy measure inside (0,1). Drift cannot contribute to this decrement, and a killing atom at 1 cannot contribute when n=4,m=2. The internal mass makes every $Q(2j,2)$ positive. Their regenerative product gives positive probability to arbitrarily many twos, a contradiction.

This is an all-sample support argument, not an extrapolation from the finite controls. It correctly excludes residual dust at replacement, unbounded parent counts, infinite event intensity and a Kingman component from its hypotheses. The star control's subordinator with drift r and killing K gives one terminal gap of length $e^{-rT}$ and initial dust, exactly matching the known hook family.

## 6. Reproduction and deliverables

From the review directory:

- `python independent_checks.py` reproduces the 583 independent assertions and `independent_results.json`
- `cd author_replay && python verify.py > replayed.json && cmp replayed.json verification.json` reproduces the 1,328 submitted assertions byte-for-byte

The independent program uses Python's standard library and SymPy. Its finite calculations include full active/frozen-state normalization, deletion sampling consistency, direct Ewens and star-paintbox controls, bounded-parent support through the forbidden eight-sample shape, and positive even decrements with internal Lévy mass. They support, but do not replace, the analytic arguments.

Copy only the eight publication files listed in `review_summary.json`. Keep the original problem's unresolved status, 3/5 count, stated special-class assumptions, and lack of priority claims.
