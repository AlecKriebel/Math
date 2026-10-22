# PR1141 independent exact-target priority audit

Audit date: 17 October 2026 (UTC). Scope: the exact two-polynomial question at printed p. 445 of Oberwolfach Report 9/2025. This is a bounded primary-literature audit, not an exhaustive historical-priority certificate.

**Verdict: no earlier recorded full-target solution was located in the inspected primary bodies. Essential prior mathematical inputs were located and verified, including a covariance inequality already published in 2005. The target follows by combining those inputs with the square-density calculation below. That logical consequence must not be described as an earlier recorded target solution unless an earlier source actually records the bridge or conclusion. Conversely, this search does not establish novelty or firstness.**

## Exact claim and success criterion

For nonzero real multilinear functions \(f,g\) on the uniform cube \(\{-1,1\}^n\), of degrees at most \(d\), put

\[
\rho_i(f)=\frac{\sum_{S\ni i}\widehat f(S)^2}
{\sum_{S\subseteq[n]}\widehat f(S)^2}.
\]

The denominator includes the constant coefficient. The question is whether absolute positive constants \(c,C\) make \(\max_i\max(\rho_i(f),\rho_i(g))\le c d^{-C}\) sufficient for some vertex with \(f(x)g(x)\ne0\). This is exactly the convention and deterministic conclusion printed in [Austrin's contributed OWR problem](https://ems.press/content/serial-article-files/51353), p. 445, PDF page 41. The report's workshop took place 16–21 February 2025. Its inverse-quadratic obstruction is a necessary restriction, not an inverse-quadratic sufficient theorem.

A decisive priority hit for the present audit would be an earlier primary text stating this conclusion or recording a complete derivation under these assumptions. A theorem about quantum attacks, a conjecture being removed from an application, a theorem requiring the supports to cover the cube, or a generic inequality alone does not automatically meet that criterion.

The zero-polynomial case is excluded because the ratio is undefined. Constants and common zeros are permitted. Degree means a bound, not a requirement that both degrees equal \(d\). The target is not a statement about variance-normalized influences, arbitrary input measures, or all finite groups.

## Original formulation versus the exact target

The official [CRYPTO 2022 conference body](https://crypto.iacr.org/2022/papers/538804_1_En_6_Chapter_OnlinePDF.pdf), Conjecture 1.2, printed p. 168, quantifies over **distributions** \(F,G\) of real degree-bounded, unit-\(L_2\)-norm functions. It bounds each coordinate's influence averaged over the distribution and asks for one function from each support and one compatible vertex. Point masses give the OWR target after normalizing each nonzero polynomial. The reverse implication is not established merely by that specialization: small average influence does not assert that every member of either family has small influence.

Conjecture 5.5, printed p. 190, uses an existential finite Abelian group and average coordinate influences in its character basis; Theorem 5.6 connects it to the quantum-state formulation. Section 5.2 proves the exponential-in-degree regime. The official [ePrint landing page](https://eprint.iacr.org/2022/218) records receipt on 25 February 2022. The full ePrint PDF, including its appendix, could not be fetched during this audit; the complete 30-page official conference body was fetched and inspected. Appendix snippets from search were not used as substantive authority.

Thus neither a result proved only for one polynomial, nor a cryptographic separation that bypasses the conjecture, settles the recorded target by its title alone. The present PR's operative claim remains the deterministic OWR problem.

## Primary-source comparison and chronology

| Primary work | Verified content relevant to this audit | Exact missing step to a recorded full-target solution |
|---|---|---|
| [O'Donnell–Saks–Schramm–Servedio, 2005](https://arxiv.org/abs/cs/0508071), primary PDF §3.3, Eq. (6), printed p. 8; arXiv v1 submitted 16 August 2005 | Generic covariance bound for a decision-tree-computed bounded function against an arbitrary real function, using revealments and expected absolute change under coordinate rerandomization. | No degree-bounded polynomial-support separator or OWR target conclusion is stated there. |
| [Homin K. Lee, 2010](https://theoryofcomputing.org/articles/v006a004/), Theorem 1.2, printed p. 82; published 17 August 2010 | Reproves the Boolean covariance form of OSSS. | The theorem is generic and does not state a low-degree polynomial-compatibility conclusion. |
| [Austrin et al., CRYPTO 2022](https://crypto.iacr.org/2022/papers/538804_1_En_6_Chapter_OnlinePDF.pdf), Conjectures 1.2/5.5, §5.2 | Introduces the distribution question and proves an exponential threshold. | The inverse-polynomial regime is conjectural in the inspected body. |
| [Bouaziz–Ermann–Grilo–Vergnaud–Vu, arXiv:2311.03512v1](https://arxiv.org/abs/2311.03512), 6 November 2023, §2.4 and Theorem 3.2 | Reuses the conjecture for an extended key-agreement setting with a final quantum message and an oracle-free final Alice step. | Theorem 3.2 explicitly assumes Conjecture 2.16; it does not prove compatibility. |
| [Li–Li–Li–Liu, ITCS 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2025.71), Conjecture 1 and Remark 2 | Studies a different randomized partial-assignment/nonvanishing conjecture for a single polynomial; distinguishes it from PCC. | Partial cases and a different conjectural route do not state the exact two-polynomial influence result. |
| [Li–Li–Li–Liu, arXiv:2504.05710](https://arxiv.org/abs/2504.05710), v1 8 April 2025, v2 1 June 2026; v2 Theorems 1.1/1.3/4.1 and Lemma 3.4 | Gives unconditional perfect-completeness QPKE separations. The proof uses quantum-query simulation, reprogramming, and a structural partial-assignment lemma. | Removing a conjecture from these cryptographic conclusions is not a statement or derivation of the uniform-cube influence target. The body was inspected, not classified from its abstract alone. |
| [Kothari–Kovacs-Deak–Wang–Yang, arXiv:2601.08727](https://arxiv.org/abs/2601.08727), v1 13 January, v2 8 April, v3 28 September 2026 | Polynomial bounds relating rational degree and degree for total Boolean functions. Theorem 4 in v3 gives a deterministic query bound. Bernoulli symmetrization and the Markov inequality supply the bounded-polynomial ingredient. | The total-function theorem alone does not handle arbitrary common zeros of the two OWR polynomials. In v1, Effective Hypercube Nullstellensatz Theorem 5 explicitly requires both zero product and no common zero. |
| [Li–Li–Li–Liu, arXiv:2608.03824v1](https://arxiv.org/abs/2608.03824v1), 4 August 2026, Lemma 3.5, printed pp. 7–8 | A deterministic depth-\(O(d^4)\) tree separates disjoint supports of two real degree-\(d\) polynomials under the promise that at least one is nonzero. Its construction gives a total tree after arbitrary labels on the common-zero set. | The text does not state an influence theorem or perform the square-density/covariance conversion. That conversion is the additional target-directed deduction. |

The arXiv primary landing for 2608.03824 lists only v1, timestamp 4 August 2026 15:33:42 UTC, at access time. The exact depth constant \(16d^4\) is an explicit extraction from its proof, not the displayed constant in its \(O(d^4)\) statement. Kothari's v1/v2 bodies were downloaded, and the permitted v3 body was inspected; version-specific theorem numbering was kept separate.

The [Chung–Lin–Mahmoody 2023 followup](https://eprint.iacr.org/2023/570) was also found through forward searches and its official landing inspected. Its full PDF and archive-version page were unavailable during this audit. Its abstract is a discovery lead only; this audit makes no body-wide exclusion claim for that unread PDF. Austrin's primary author bibliography and a coauthor's bibliography were checked as additional leads; neither is a complete current-literature inventory.

## Checkable bridge from the verified prior tools

This section records a deduction now supplied in this audit, not evidence that an earlier author recorded the target solution.

Suppose \(fg=0\) pointwise. The separator lemma supplies a total Boolean \(h\), with \(h=1\) on \(\operatorname{supp}f\) and \(h=0\) on \(\operatorname{supp}g\). Extracting the constant: at a stage with degrees at most \(D\), the bounded sign-change polynomial has degree at most \(2D\); the Markov/Bernoulli inequality gives at most \(8D^2\) disjoint maximum monomials. Their union contains at most \(8d^3\) coordinates. At most \(2d\) degree-sum reductions occur, giving depth \(T\le16d^4\). This is the mechanism in Li et al.'s separator proof, not an independent new separator theorem.

Let \(r_i\) be the probability the tree queries coordinate \(i\). For independent coordinate rerandomization \(X^{(i)}\), define

\[
A_i(u)=\mathbb E|u(X)-u(X^{(i)})|.
\]

OSSS Eq. (6), applied to \(2h-1\), gives **exactly**

\[
|\operatorname{Cov}(h,u)|\le\tfrac12\sum_i r_i A_i(u).
\]

There is no requirement that \(u\) be Boolean, bounded, computed by the tree, or monotone. This exact generality appears in the original OSSS body, so presenting it as a newly obtained covariance inequality without credit would be inaccurate. Lee's Boolean theorem is a useful secondary route to the covariance principle; OSSS Eq. (6) is already the directly matching prior statement.

Put \(u=f^2/\|f\|_2^2\) and \(v=g^2/\|g\|_2^2\). For a sign flip \(X^{\mathrm{flip}(i)}\), Parseval and Cauchy–Schwarz give

\[
\begin{aligned}
A_i(u)
&=\frac{\mathbb E|f(X)^2-f(X^{\mathrm{flip}(i)})^2|}{2\|f\|_2^2}\\
&\le2\sqrt{\rho_i(f)(1-\rho_i(f))}\le2\sqrt{\rho_i(f)}.
\end{aligned}
\]

The same holds for \(v\). Both densities have expectation one. With \(\mu=\mathbb Eh\), the support identities give

\[
\operatorname{Cov}(h,u)=1-\mu,\qquad
\operatorname{Cov}(h,v)=-\mu.
\]

Their absolute values sum to one even if the supports do not cover the cube. Therefore, with \(\delta=\max_i\max(\rho_i(f),\rho_i(g))\),

\[
1\le 2\Bigl(\sum_i r_i\Bigr)\sqrt\delta
\le2T\sqrt\delta\le32d^4\sqrt\delta.
\]

Consequently disjoint nonzero supports require \(\delta\ge1/(1024d^8)\). In particular \(\delta\le1/(4096d^8)\) suffices for compatibility. The affine substitution between \(\{0,1\}^n\) and \(\{-1,1\}^n\) preserves degrees and tree depth; the Fourier calculation is made directly in the latter coordinates under the uniform measure.

This supplies a complete mathematical link from earlier tools to the exact target. It also identifies precisely what is historical evidence and what is the currently assembled consequence. Prior existence of every ingredient does not prove that the target-directed combination had already appeared; failure to find that combination does not prove that it had not.

## Priority decision boundary and required credit

The strongest verified historical conclusion is that the decisive separator was publicly available on 4 August 2026 and the exactly matching covariance inequality was already available in 2005. The exact target can now be deduced from those two results with the elementary density calculation above. No source inspected here explicitly records that complete conclusion or deduction before the present work.

Accordingly, **this audit supplies no verified earlier full-target publication on which to base a strict skip under a rule requiring an already recorded solution**. It also supplies no positive novelty certification. If the user's rule instead excludes every short new corollary of existing theorems, that is a different policy criterion; the report does not silently substitute one criterion for the other.

The operative proof already disclaims novelty. Its source-credit paragraph should explicitly identify OSSS2005 §3.3 Eq. (6) as the covariance input; Lee2010 Theorem 1.2 may also be cited. Reproving an input is useful for verification but does not remove its historical attribution. The remainder of the argument should be described as an explicit consequence or synthesis of the cited inputs, with no firstness assertion.

The unresolved historical gap is precise: an earlier primary paper, appendix, author note, or public talk text may already record the separator-to-square-density influence bridge or an equivalent full-target theorem. Search indexing, inaccessible full ePrint bodies, unpublished work, and author-page freshness limit this audit. No external human input was requested or prepared, consistent with project policy. An independently verifiable earlier body would change the priority assessment; another generic inequality or another cryptographic application would need its full implication checked.

## Search record and custody

`QUERY_LOG.json` records 47 actual search queries in 18 query/operation batches, relevant result URLs, access failures, and which leads were not substantive authority. The initial four entries were contemporaneous; later entries explicitly say when they were reconstructed retrospectively. Search response timestamps were not retained for every call. Irrelevant keyword-match URLs and truncated raw result lists are not claimed to be a complete search-engine dump. `SOURCE_METADATA.json` records fetched byte hashes, primary locations, version dates, available extracts, and allowed nonself input pins.

The review was conducted independently from primary literature before reading `inputs/PROOF.md`. No other review report or root decision was read. The only local contents outside this review directory read were the project policy, the explicitly allowed source PDFs/texts, and the operative proof. An initial broad read-only status/file-name inventory produced unrelated path names, not their file contents. No Git index/ref mutation, branch change, PR change, tracker change, paper change, release, push, or external message occurred. All authored files and downloads are confined to this review directory. The receipt pins the public artifacts and all read nonself files; its own digest is sent separately to root.

Completion estimate: **100% of this bounded audit assignment**. This is not a percentage estimate that global historical priority is known.
