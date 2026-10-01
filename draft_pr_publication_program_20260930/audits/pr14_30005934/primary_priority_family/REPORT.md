# PR14 primary sources, parameter theorem and earlier-claim audit

Frozen review target: `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`, problem `30005934` / `OWR-14298374-003`. Audit date: 1 October 2026 UTC. Family completion: **100%**. This is an independent source and imported-theorem audit; it does not replace independent verification of the candidate's stochastic analytic proof.

**Verdict:** the intended noninteger obstruction matches the primary sources, the imported positive-scale theorem matches exactly, and an earlier public manuscript explicitly claims the same narrow obstruction. Recommend **`already_solved` for the intended noninteger target after the proof review passes**, with attribution to the earlier unrefereed candidate and an explicit zero-parameter qualification. No novelty or historical first-priority claim is justified.

Only `CANDIDATE.md`, `SOURCE_AUDIT.md`, and `source_record.json` were read from the frozen snapshot. No historical independent review, sibling audit, external editorial assessment, or broader classification proof was used. ZIP entry names were listed, but review files inside them were not read. No canonical edits, Git edits or external communications were made. Raw source copies and page renders are in ignored `tmp/`; the durable hash ledger is `PRIMARY_SOURCE_HASH_LEDGER.json`.

## Exact primary target and solution scope

The official [OWR 26/2024 PDF](https://ems.press/content/serial-article-files/49484), pp. 1478–1480, identifies the Hilbert-space Wishart equation and injective-noise question. On printed p. 1480 it is **Open problem 1**, not 1.2. The [final CCK article](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf), EJP 29 (2024), article 123, labels the corresponding question **Open problem 1.2** on printed p. 5. Thus the identifiers refer to the same target. OWR Open problem 2 / EJP Open problem 1.3 concerns degenerate noise and is separate.

The source setting has real separable infinite-dimensional $H$, bounded positive self-adjoint $Q$, a $C_0$-semigroup generator $A$, cylindrical Hilbert–Schmidt Brownian noise, and real $\alpha$. Its operational weak-solution class is adapted, positive trace class with continuous paths, and satisfies scalar integral identities for every (g,h\in D$A$). Theorems 3.1 and 4.3 additionally assume an integrable random initial trace-class value and the printed smoothing condition. The candidate removes those extra assumptions for its necessity result; it therefore covers that source class. The source's unbounded-generator question arises after the injective-semigroup result and explicitly allows the missing semigroup-injectivity case. These facts were checked against full extracted pages and visual renders.

### Zero and the exact notation boundary

The literal source uses $\alpha\notin\mathbb N$. The frozen record also calls the question “noninteger,” while the candidate proves $\alpha\in\mathbb N_0=\{0,1,\ldots\}$. No explicit definition of $\mathbb N$ was found in the inspected article. The proof of Corollary 4.11 on printed p. 29 separately uses $\mathbb N_0$; this is a reason to preserve, rather than silently resolve, the convention.

The concrete boundary is checkable without any cited theorem: with $\alpha=0$, $X_0=0$, and $X_t=0$ for all $t\ge0$, every weak-equation drift and noise term vanishes for **any** $C_0$ generator $A$ and any allowed $Q$. In particular one may choose an unbounded noninjective shift generator. This proves neither positive-integer existence nor a broader classification; it only checks the exceptional zero solution.

Consequently:

- If the source's $\mathbb N$ includes zero, the obstruction supplies the literal negative answer.
- If the source's $\mathbb N$ means positive integers, the literal question permits the trivial affirmative zero example. Its intended noninteger part, $\alpha\notin\mathbb N_0$, still has the verified negative obstruction.

A publication or queue entry should say “no noninteger parameter; $\alpha=0,X=0$ is allowed,” retain the printed source notation, and state this qualification. Do not assert the authors intended either convention.

## Imported finite-dimensional theorem

Read the full [GMM arXiv paper](https://arxiv.org/pdf/1607.00206), current version identified as v3; visually checked Definition 1.1 (printed p. 2) and Theorem 1.3 (p. 4), and inspected Section 3.2 (p. 16). The [arXiv metadata](https://arxiv.org/abs/1607.00206) identifies the journal publication as SPA 128(4) (2018), 1386–1404.

In the candidate transform

\[
L(v)=\det(I_n+2Cv)^{-\alpha/2}
\exp\{-\operatorname{tr}[b\,v(I_n+2Cv)^{-1}]\},
\qquad v\ge0,
\]

the exact Definition 1.1 substitution is $p=n$, shape $\beta=\alpha/2$, scale $\Sigma=2C>0$, and noncentrality $\omega=b\ge0$. Cyclicity gives the source's exponential order. Theorem 1.3(ii)–(iii) yields

\[
\alpha\ge n-1
\quad\text{or}\quad
\alpha\in\{0,1,\ldots,n-2\},\quad \operatorname{rank}(b)\le\alpha.
\]

Membership in $W$ means existence of **one** probability law with this transform. The theorem does not require the candidate's compressed process to be Markov. Its own proof builds an auxiliary semigroup from law existence; that is not an extra hypothesis on the supplied law. Definition 1.1 prints $\beta>0$, but Theorem 1.3 and Section 3 explicitly include $\alpha=0$/$\beta=0$. Negative parameters are outside Theorem 1.3's hypothesis and need a separate check.

### Independent normalization and boundary checks

For $v\ge0$, the identity

\[
v(I+2Cv)^{-1}
=\sqrt v(I+2\sqrt v C\sqrt v)^{-1}\sqrt v
\]

shows that this matrix is symmetric positive semidefinite. The determinant is positive because $\det(I+2Cv)=\det(I+2\sqrt v C\sqrt v)>0$. Thus there is no unmentioned sign or noncommuting-order change in the matching.

The following cases test every boundary needed by the candidate:

| Dimension | Parameter | Required noncentrality condition |
|---|---:|---|
| $n=1$ | $\alpha\ge0$ | arbitrary scalar $b\ge0$; discrete part empty |
| $n=2$ | $\alpha=0$ | $b=0$ |
| $n=2$ | $\alpha\ge1$ | arbitrary $b\ge0$ |
| $n=3$ | $\alpha=1$ | $\operatorname{rank}b\le1$ |
| $n=3$ | $\alpha=2=n-1$ | arbitrary $b\ge0$ |

For the scalar zero-shape boundary, set $c>0$ and $\lambda=b/$2c$$. Then

\[
e^{-br/(1+2cr)}
=\exp\{\lambda[(1+2cr)^{-1}-1]\}
\]

is the Laplace transform of a compound Poisson sum of exponential random variables of mean $2c$, with Poisson intensity $\lambda$. This independently confirms that $n=1,\alpha=0$ must not impose $b=0$. By contrast, $\alpha=0$ is discrete for $n\ge2$.

For $\alpha<0$, the scalar transform behaves as

\[
(1+2cr)^{-\alpha/2}\,e^{-br/(1+2cr)}\longrightarrow\infty,
\qquad r\longrightarrow\infty,
\]

which violates the bound $L(r)\le1$ for a probability law on the nonnegative line. For nonnegative noninteger $\alpha$, any integer $n>\alpha+1$ puts $\alpha$ strictly below $n-1$ and outside the discrete set. The candidate's dimension choice is therefore correct. A rank inference at the integer threshold $n-1$ would fail, but the candidate's narrow obstruction makes no such inference.

One further independent structural check is useful: strong continuity at $s=0$ and injectivity of $Q$ imply $\|\sqrt Q S(s)h\|>0$ on a small interval for every nonzero $h$. Hence $C_t=\int_0^t S(s)^*QS(s)\,ds$ is strictly positive for every $t>0$, so all finite-dimensional compressions have positive scale. Semigroup injectivity at positive times is unnecessary. This does not require a global trace-class determinant.

## Earlier immutable claim and archived evidence

The [immutable prior manuscript](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md) has the same equation and continuous trace-norm weak-solution meaning. Lemma 3 supplies the finite-rank conditional transform without smoothing or semigroup injectivity; Corollary 2 excludes $\alpha\notin\mathbb N_0$ for injective $Q$ and arbitrary $C_0$ generator on infinite-dimensional $H$. Its scope section explicitly extends this nonexistence conclusion to random initial data. This is the precise prior narrow claim and mechanism, not merely a related existence result. The source identifies the manuscript as **Anonymous, Evidence Press, unrefereed candidate**, dated 22 September 2026. Git commit metadata names Ian Pitchford as author and committer; that metadata is not a basis for replacing the manuscript's Anonymous attribution.

The [Zenodo version record](https://zenodo.org/records/22892681) is published, DOI **10.5281/zenodo.22892681**, version **0.1.0-candidate**, publication date **2026-09-22**, creator **Anonymous**, resource type **preprint**. Its API reports creation at **2026-09-22T07:29:24.820191Z** and modification at **07:29:25.198074Z**. The [GitHub commit](https://github.com/ipitchford/wishart-reachable-noise/commit/73dd242a4450400e2f8f16b65929cb77fee76be1) records both dates as **2026-09-22T07:27:04Z**; it is unsigned. Zenodo's concept DOI is `10.5281/zenodo.22892680`; the version endpoint returned one listed version at audit time.

Fetched and verified all four deposit files:

| Archived file | Bytes | Checks performed |
|---|---:|---|
| `wishart-reachable-noise-v0.1.0-candidate.zip` | 355974 | advertised MD5; SHA256SUMS; manuscript/PDF comparison |
| `wishart-reachable-noise-v0.1.0-candidate-review-target.zip` | 321386 | advertised MD5; SHA256SUMS; manuscript/PDF comparison |
| `wishart-reachable-noise-v0.1.0-candidate.pdf` | 273181 | advertised MD5; SHA256SUMS; both ZIP PDFs equal |
| `SHA256SUMS` | 347 | advertised MD5; all three listed SHA-256 values match |

Both ZIP `paper.md` entries equal the immutable GitHub bytes. The manuscript SHA-256 is `8ac4fe3bf81f4ec70cf17fcd4e3413b13271cf61524dacd7209119a3ae86b184`; its computed Git blob SHA-1 matches the commit's listed object `54ff9ccf53045aa22230e8f03c4127f54bb98902`. This securely ties the inspected narrow claim to the cited version. Public archive identity supports earlier availability relative to the 30 September candidate; it does not prove the earliest historical discovery, external referee validation, or any of the prior manuscript's broader classification claims.

## Bounded current-literature and duplicate check

On 1 October 2026, searched exact title/ID and combinations of “infinite-dimensional Wishart,” “noninteger,” “noninjective,” and “Open Problem 1.2,” including arXiv/Zenodo-focused queries. The exact earlier candidate was found. The live UnsolvedMath record was inaccessible to the web reader; exact ID/title searches returned no additional indexed record, so this is not an exhaustive duplicate-registry check.

The primary [HKK arXiv v2 source](https://arxiv.org/html/2508.14813v2), last revised 13 April 2026, Section 2.2.1, uses integer $n$, initial rank at most $n$, and a bounded Wishart drift operator. That section does not state the injective-noise noninteger obstruction with arbitrary $C_0$ dynamics. The OWR and EJP statements are two primary presentations of the same question, not distinct research targets; their degenerate-noise neighbors remain outside this disposition. No stronger historical-priority conclusion follows from these bounded searches.

## Gate and recommended release wording

Source matching, imported theorem application, boundary checks, exact earlier-claim identity, and version/archive checks **pass**. The remaining independent gate is the candidate's moving-test/localization, quadratic variation and conditional-law proof; this family does not certify those by reading an earlier claim. If that gate passes, the intended noninteger target should be recorded as **already solved in an earlier unrefereed source, with an independently reviewed narrow negative answer**. Retain the zero convention qualification and credit Anonymous (2026), Lemma 3 and Corollary 2, version `0.1.0-candidate`, DOI `10.5281/zenodo.22892681`. Do not promote a full existence, rank, degenerate-noise, continuity, or strong-solution classification.
