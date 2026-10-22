# PR630 / 30000700 / OWR-1460-004: independent primary scope and priority recheck

Reviewed immutable head: `810cd5c148bbae7c7c5a47423c375ada98e903b6`.

**Verdict: mathematical pass for the three precisely scoped propositions; no new resolution of the original printed universal IM assertion established. Retain the closed disposition and preserve the valid refinements privately.** This conclusion follows from a directly checked older counterexample, not from trusting the earlier closure or failing to find literature. It is an automated mathematical review, not external peer review.

The older source does not explicitly name the identical OWR question in the pages inspected. The conclusion is that its displayed family already contains a complete counterexample to the OWR assertion after parameter substitution and direct differentiation. No claim of earliest recognition, copying, or exhaustive historical priority is made.

## 1. Claim, input custody, and independence

The claim under review is a negative answer to the universal IM replacement question immediately after Theorem H on printed p. 503 of Oberwolfach Report 9/2007. Success for the mathematics requires one nonconstant entire function satisfying every printed IM hypothesis and failing the proposed conclusion. Success for a new original-problem contribution additionally requires that the central resolution not already follow directly from verified older material.

All 28 native candidate files were compared byte for byte against locally available immutable Git objects at the assigned head. Every file agrees, and the native folder contains no additional files. `INPUT_BINDINGS.json` records paths, SHA-256 digests, Git blob identifiers, byte counts and private copies. This used only read operations; no Git state was changed.

The complete candidate `safe/PROOF.md`, both relevant READMEs, `safe/STATUS.json`, `safe/SOURCE_VERIFICATION.json`, `audit/AUDIT.md`, `audit/CORRECTIONS.json` and audit README were read. The three propositions and all essential guardrails were reviewed. The original controls were inspected but not run here; the root reviewer is replaying them independently. Frozen candidate claims of earlier searches or checks were not treated as current independent evidence.

The two publisher PDFs were retrieved directly before the candidate proof or earlier priority verdict was opened. The source-first derivation was sealed at 2026-10-21 18:13:56 UTC. Only afterward were `ROOT_PRIOR_EXAMPLE_IMPLICATION.md`, `PRIORITY_REJECTION_ACCEPTANCE.json` and the scaling clarification read. Their conclusions agree with the independent source-first derivation, but are not its premises.

This review made no provider changes, sheet changes, PR changes, publication actions, commits, pushes, releases, or communication with external individuals, other agents, or other chats. Current tracker and full-account publication deduplication belong to the root review; they were not independently repeated or certified here.

## 2. Original primary statement recovered

The primary source is Mingliang Fang's contribution, “Normal families and their applications to the uniqueness of entire functions,” printed pp. 501–503 in *Normal Families and Complex Dynamics*, Oberwolfach Report 9/2007. The workshop dates are February 18–24, 2007. The contribution credits joint work with Jianming Chang and Lawrence Zalcman. The full relevant contribution was read in text, and printed pp. 502–503 were visually inspected. Other contributions in the 62-page report were not comprehensively reviewed. [EMS publisher PDF](https://ems.press/content/serial-article-files/46093?nt=1).

On printed p. 502, IM sharing is equality of the sets of points where the functions equal the shared value. CM also requires equal multiplicities. On p. 503, Theorem H assumes a nonconstant entire function f, an integer k>=2, constants a,b with b!=0, CM sharing of a between f and f', and

    f'(z)=b  =>  f^(k)(z)=b.

Its conclusion is

    f(z)=d exp(cz)+((c-1)/c)a,
    c,d != 0,  c^(k-1)=1.

The immediately following question asks whether replacing CM by IM preserves that theorem. This is the universal hypothesis being tested, rather than a theorem assumed true.

There is no a!=0, a!=b, transcendence, growth, or antecedent-attainment requirement in H. The neighboring Theorem G and Theorem 3 separately impose a!=0; importing that assumption into H would change the target. The catalogue's added a!=b and additive term a/c differ from the original, but neither affects the a=0 examples. The printed formula was checked visually; mathematical text extraction alone mangles its fraction.

At k=2, c=1 and the proposed conclusion gives f=d exp(z), hence f=f'.

## 3. Older Example 1 directly supplies the central counterexample

The essential older primary source is Feng Lü, Junfeng Xu and Hongxun Yi, *Uniqueness theorems and normal families of entire functions and their derivatives*, Annales Polonici Mathematici 95.1 (2009), 67–75, DOI 10.4064/ap95-1-5. All nine pages were read in text for scope, and printed pp. 68–69 and 75 were visually inspected. The cover/header identifies 2009; printed p. 75 records receipt on 27 May 2008 and final form on 20 September 2008. This is the publisher's journal PDF, not a search snippet. The article's full theorem proofs were read for scope but were not independently re-proved, and the counterexample implication does not depend on their validity. [IM PAN publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/84815).

Printed p. 68, Example 1 supplies

    g(z)=(B/4)z^2,

where B renames the source's parameter b to prevent confusion with the target parameter. Its surrounding theorem uses the different additional condition

    g'=B  =>  g=B.

That condition is not transferred to the OWR theorem. Instead, fix any target b!=0 and set B=2b. Directly,

    g(z)=(b/2)z^2,    g'(z)=bz,    g''(z)=b.

Take a=0 and k=2. Each hypothesis is now checked over all complex z:

1. b!=0 makes g a nonconstant entire polynomial.
2. Both zero sets are exactly {0}. Their multiplicities are 2 and 1, so sharing is IM and fails CM.
3. g'=b holds precisely at z=1, and g''(1)=b. In fact g''=b identically. Thus the target implication is nonvacuous.
4. g(0)=0, whereas every d exp(z) with d!=0 has no zeros. Also g-g'=b(z^2/2-z) is a nonzero polynomial. The proposed k=2 conclusion fails.
5. The catalogue's stronger b!=a holds because a=0 and b!=0.

At b=1 this is exactly the candidate's central f=z^2/2 counterexample. The original question universally quantifies over k>=2; one permitted k=2 instance refutes it in full. A proof at every fixed order is a refinement, not a necessary missing step in that negative answer.

The different source predicate is independently consistent: g'=B occurs at z=2, and g(2)=B. The target predicate occurs at z=1. Without B=2b, using the old formula with B=b gives g''=b/2 and fails the target implication. The certificate deliberately rejects that faulty transfer. This is why checking the target by differentiation is essential.

The positive dated evidence establishes that the displayed old family already contains a full counterexample. It does not show that the 2009 authors explicitly recognized or announced the OWR implication, and the report does not make that stronger historical assertion.

## 4. Candidate mathematics independently checked

### Proposition 1: all-order polynomial construction

For any k>=2, b!=0 and z0 in C,

    f(z)=b(z-z0)^k/k!

has f'=b(z-z0)^(k-1)/(k-1)! and f^(k)=b. Both zero sets are {z0}, with unequal multiplicities k and k-1. Its f'=b fiber consists of the k-1 distinct solutions of (z-z0)^(k-1)=(k-1)!, so it is nonempty. Its zero rules out the proposed nonzero exponential at a=0. All assertions in this proposition are correct.

### Proposition 2: complete polynomial classification

Let f be a nonconstant polynomial of degree n. If a!=0, every zero of f-a has f'=a!=0 and is simple. For n>=2 there are n distinct such points, all zeros of the degree n-1 polynomial f'-a, a contradiction. For n=1, the f-a fiber is one point whereas the f'-a fiber is empty or all C. Thus a=0 is forced and n>=2.

At a=0, let f have r distinct roots with multiplicities m_j. Sharing implies each m_j>=2 and that f' has no other roots. Hence

    n-1 = sum_j(m_j-1) = n-r,

so r=1 and f=A(z-z0)^n with A!=0. Now f'=b has n-1 distinct nonzero translated roots. If k>n, f^(k)=0 fails the b-condition there. If 2<=k<=n, f^(k)-b has degree at most n-k<n-1 and vanishes at all those n-1 points. It is identically zero. Since f^(k) is nonzero of degree n-k, this forces n=k and A n!=b. The converse is Proposition 1. This independently verifies the complete classification without the candidate's roots-of-unity step.

There is also a verified classical shape mechanism. When f'=0 implies f=0 and n>=2, the only critical value of f is zero. The Cornell author manuscript of Novikov–Yakovenko states the translated-monomial theorem as Proposition 7, author p. 27, crediting Chademan. The dated arXiv v1 has the same statement and proof as Proposition 5, author p. 26. Both relevant pages and the Cornell date page were visually inspected. The Cornell file is 32 pages and is byte-distinct from the 31-page arXiv v1; their proposition numbers must not be interchanged. The arXiv v1 was submitted 20 January 2000 and bears an internal 19 January 2000 date. This verifies the shape mechanism in a dated pre-candidate body. Its cited Chademan 1996 original was not independently obtained. [Cornell author manuscript](https://pi.math.cornell.edu/~novikov/Papers/redundant.pdf), [arXiv v1 body](https://arxiv.org/pdf/math/0001111v1), [arXiv version history](https://arxiv.org/abs/math/0001111v1).

The specialization n=k and A=b/k! is then an elementary derivative-fiber argument. The exact earliest publication of this whole target-specific classification is not established. Its mathematical validity is preserved; it should not be called a newly certified first result.

### Proposition 3: zero-value transcendental family

For k>=3 choose lambda!=0 satisfying

    lambda^(k-1)=-1/(2^(k-1)-2),

and put b=-lambda/2 and f=(exp(lambda z)-1)^2. With t=exp(lambda z), t ranges over C excluding zero and

    f=(t-1)^2,
    f'=2 lambda t(t-1),
    f^(k)=lambda^k(2^k t^2-2t),
    f'-b=2 lambda(t-1/2)^2.

The common zero fiber is t=1, with multiplicities 2 and 1. The b-fiber is exactly t=1/2, attained at every z=(-log(2)+2 pi i m)/lambda. At these points,

    f^(k)=lambda^k(2^(k-2)-1)=-lambda/2=b.

The infinitely many zeros z=2 pi i m/lambda prove transcendence because f is entire and not identically zero. They also exclude the target pure exponential. The denominator is nonzero for every asserted k, so a nonzero complex lambda exists. This proves the proposition for every k>=3.

The amplitude/translation clarification is also valid. For any prescribed b!=0 and z0, set A=-2b/lambda and f=A(exp(lambda(z-z0))-1)^2. The same formulas give f'-b=2A lambda(t-1/2)^2 and f^(k)=b at that fiber. A!=0, so sharing, transcendence and the conclusion failure persist.

The 2009 paper already displays the squared-exponential shape: Theorem 1.2(d) on pp. 68–69 gives a family proportional to (A exp(w/4)/2+1)^2. Set its A=-2 and amplitude 1 to obtain (exp(w/4)-1)^2; composing w=4 lambda z yields the candidate's functional shape. This does not transfer the old derivative-value predicates through a change of variable. The higher-derivative resonance equation above is separately derived and checked. Its exact historical firstness remains unknown. Thus the known shape plus a verified calibration is an accurate description, not evidence for a newly available negative answer to the universal OWR question.

## 5. Falsification and boundary checks

- b=0 is outside the target and collapses the normalized polynomial example; none of the arguments silently uses it.
- Requiring b!=a or requiring an attained f'=b fiber does not exclude the quadratic.
- CM excludes every displayed zero-sharing counterexample because multiplicities at a=0 differ.
- For the same quadratic, k>=3 gives g^(k)=0 and fails at z=1; the central older-example implication asserts only k=2.
- At k=2 the squared-exponential critical-fiber calculation gives f''=0 at t=1/2 while b=-lambda/2!=0. The displayed transcendental ansatz therefore does not solve that restricted case.
- In Proposition 3 the b-fiber of f' is double, while that of f^(k)-b is simple: its t-derivative at 1/2 is lambda^k(2^k-2)!=0 and dt/dz=lambda/2!=0. A multiplicity-dominating b-implication would fail, but the printed target asks only for a value implication.
- Adding a constant to a zero-sharing example does not shift its derivative by that constant and does not establish an a!=0 solution.
- No proof of a nonzero-a variant, a transcendental k=2 example or a classification of all entire instances is present. No assertion is made that those different questions remain open in the current literature.

The independent stdout-only control script uses exact rational arithmetic and imports no frozen code. It verifies the formal B=2b specialization and the distinction between its two fibers; rejects the unscaled B=b transfer; checks 124 expanded translated polynomial examples; and checks the derivative recurrence and resonance for k=3 through 64, including arbitrary-b amplitude scaling and negative boundary controls. It was run from a newly created private copy both normally and with optimized Python; outputs are byte-identical. These finite checks corroborate the algebra. The universal conclusions rest on the written deductions above.

## 6. Bounded search, read scope and exact remaining gap

The search was bounded to reconstruction of the given OWR source, the identified 2009 primary example, two query rounds (six exact query strings in `SEARCH_LEDGER.md`), the classical polynomial mechanism, and the candidate's neighboring Chang–Fang source. Search noise concerning other unrelated “Theorem H” labels was not promoted to evidence. No exact prior paper explicitly announcing a resolution of this named OWR question was verified. That absence is not the reason for the adverse novelty conclusion.

The 2003 Fang–Zalcman publisher search result supplies the title, DOI and abstract, but direct primary-page access returned 403. Its full theorem body was not obtained. The 2007 Chang–Fang publisher abstract was freshly read; it requires nonzero a and the same value a in both derivative implications, so it does not cover the target's exceptional a=0, distinct-b example. The publisher records online publication on 15 December 2006 and the June 2007 issue, which are compatible. Its full body remains subscription-only through the inspected route. The candidate's 2010 neighboring source was not freshly read here and is not used to decide priority. [Fang–Zalcman publisher page](https://www.sciencedirect.com/science/article/pii/S0022247X03000416), [Chang–Fang publisher abstract](https://link.springer.com/article/10.1007/s10114-005-0861-5).

| Route | Strongest verified result | Exact limitation |
|---|---|---|
| Original printed universal assertion | False by the nonvacuous quadratic at a=0,k=2 | Exact quadratic is already in a 2009 displayed family |
| All-order polynomials | Full target-specific polynomial classification is correct | Shape mechanism is classical; earliest exact calibration/classification unknown |
| Zero-value transcendental examples | Valid for every k>=3; arbitrary b by scaling | Known squared-exponential shape plus checked resonance; firstness unknown |
| Nonzero-a restriction | No polynomial instances; no general solution here | Not proved for arbitrary entire functions |
| Transcendental k=2 | This ansatz fails | No general construction or impossibility theorem here |
| All entire instances | Counterexamples and polynomial classification only | No complete entire-function classification |

No new mechanism is needed for the original universal negative answer once the dated quadratic is recognized. The candidate refinements may be preserved as attributed, checkable deductions, but none restores a newly established resolution of the original target. A separately scoped new theorem would need an independently checked statement and priority analysis; it cannot be inferred merely by changing the target to a!=0, transcendental k=2, or full entire classification.

## 7. Recommendation and replay side effects

Recommend retaining the closed disposition for promotion as a novel original-problem resolution. Preserve the correct proofs and exact certificates. Do not create a paper, DOI, release, publication record, or new tracker row on the basis of this review. This is a recommendation to the root reviewer, not an action taken against any external state.

**Side-effect warning for the root reviewer:** all sources under `sources/` are private research custody, including complete copyrighted PDFs, extracted text, HTML and page images. Do not publish this review folder wholesale. Original candidate controls were not executed here. Any original or future script that writes its own certificates must be replayed only on a NEW PRIVATE COPY, never in canonical files or the bound immutable input tree. The frozen release wrapper also creates temporary extraction directories; put its temporary directory inside the new private replay area if reproducing it. The independent script supplied here writes only stdout and was itself copied into `certificates/new_private_replay_01/` before execution. Its replay receipts record all outputs and exact hashes.

Completion estimate: 100% of this assigned independent recheck. This is not a claim of an exhaustive literature search, completed root control replay, completed live deduplication, or a new discovery.
