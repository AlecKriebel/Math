# Independent priority and definition audit: Kourovka 21.149

Checkpoint: 2026-10-17 13:22 America/Los_Angeles (20:22 UTC).
Auditor: research subagent, independently searched before sharing findings.
Completion estimate: 90% of this preliminary priority/definition audit; 0% of a new complete solution.
No external individuals were contacted. No QUEUE or PR material was used. No Git state was changed.

## Selection finding

**Do not classify the full October 2026 problem as already solved on the evidence found. Do not claim a new rank-one six-family solution.** The current official Notebook prints 21.149 without a solution mark. The official update explicitly labels its statement as made more precise. A September 2026 preprint proves a substantial restricted result, and makes its restrictions explicit. Higher-rank ambient slope groups remain outside that result. Whether an omitted reflected extended-real family belongs to the intended quantification also needs to be fixed before any complete-solution claim.

## Authoritative current and former statements

Current primary source: [21st edition, October 6 2026 update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed p. 199 (PDF page index 198), Problem 21.149. Attribution: V. M. Kopytov and N. Ya. Medvedev; communicated by A. V. Zenkov. The statement supplied in the assignment agrees exactly with the current PDF: it asks for an order automorphism which cannot be implemented by conjugation in any possibly larger Dlab group. There are no explicit rank or ambient-family restrictions in that statement.

The [official updates-only PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-1.pdf) records the precision change. The locally downloaded text has the entry at lines 1786–1788. The Notebook main-site October 6 post identifies this edition as current as of the audit date. It also explains that unconfirmed AI solutions remain unsolved; this general policy does not certify this specific preprint.

The [older authoritative alglog edition](https://alglog.org/21tkt.pdf), printed p. 182, asks only for an order automorphism which is not inner. That is genuinely weaker: an ambient conjugator need not belong to the source group.

[Van Doorn–Judin–Monticone–Morrison, arXiv:2607.17477v2](https://arxiv.org/html/2607.17477v2), Appendix A, reports a correct solution to that earlier formulation followed by clarification from a proposer. Their account says the revised question was open in July 2026. Their [formal development](https://github.com/pitmonticone/Kourovka/blob/main/Kourovka/Problem_21_149.lean) explicitly identifies its theorem as solving the original formulation only. None of this establishes that the September partial result answers every revised quantifier.

## Primary definition: V. Dlab (1968)

[V. Dlab, On a family of simple ordered groups, J. Austral. Math. Soc. 8 (1968), 591–608](https://doi.org/10.1017/S1446788700006261); [open original PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2FC98980CF8D6CE6001298088EC1E5FA/S1446788700006261a.pdf/div-class-title-on-a-family-of-simple-ordered-groups-div.pdf).

Section 2, printed pp. 591–593, starts with **arbitrary** subgroups H of the positive multiplicative real group. An increasing homeomorphism f of [0,1] is locally right H-linear when for every a in [0,1) there exist epsilon>0 and h_a in H with f(x)=f(a)+h_a(x-a) on the right interval [a,a+epsilon]. This does not require finitely many affine pieces globally. The full group and its normal subgroups impose identity near zero, near one, or both. The compact-support subgroup is algebraically simple. Its bi-orders correspond to group orders on H; rank one is the special case yielding exactly two.

Consequently, restricting the phrase Dlab group to rank-one H would discard groups present in the original defining paper. Also, locally right linear must not be replaced by locally finite piecewise linear: left accumulation of pieces is allowed when the right germ remains affine.

## September 2026 priority result and exact scope

[Ting Gong, Yong Yang, Michael Ruofan Zeng, An order automorphism of a Dlab group not induced by conjugation, arXiv:2609.18630v1](https://arxiv.org/abs/2609.18630), submitted September 16 2026; [HTML](https://arxiv.org/html/2609.18630v1).

Theorem 1.1 constructs one automorphism of G=D_<2>([0,1]) which is not implemented after any order-preserving embedding into the six listed ambient groups, **provided the ambient H has rank one**:

D_H(I), D_H*(I), D_*H(I), bar(D)_H(I), D_H, D_H*.

Section 1 explicitly omits the reflected extended-real D_*H. Remark 2.4 explicitly excludes any assertion for arbitrary higher-rank H. The proof's central obstruction uses well-ordered support components and an embedding-conjugacy theorem proved through the rank-one first-slope order rule. The normalizing homeomorphism has infinitely many support intervals descending to zero.

This is prior art for that witness and mechanism. A purported new theorem merely reproducing those six rank-one cases would fail originality. Extending its embedding theorem to all allowed H is a distinct unresolved gap; merely citing it for higher-rank H is invalid. The paper is a preprint, and this audit has not independently certified its entire proof.

## Other primary literature and access limits

[A. V. Zenkov and N. Ya. Medvedev, On Dlab groups, Algebra i Logika 38(5) (1999), 531–548; English translation Algebra and Logic 38 (1999), 289–298](https://www.mathnet.ru/php/archive.phtml?issue=5&jrnid=al&option_lang=eng&volume=38&wshow=issue&year=1999). The MathNet issue listing verifies title, authors, year and Russian pagination. Full-text fetching timed out in the web tool during this audit. The accessible September preprint cites its interval and extended-real definitions and order classifications; independently reading the original remains desirable before relying on exact reflected-family conventions.

[N. Ya. Medvedev, Partial Orders on Dlab Groups, Algebra and Logic 40(2) (2001), 75–86](https://www.mathnet.ru/eng/al213), DOI [10.1023/A:1010256703986](https://doi.org/10.1023/A:1010256703986), MR1850443, Zbl0974.06012. The primary MathNet indexed abstract explicitly restricts H to rank one and lists exactly the six families used in the September theorem. It concerns partial-order classification, not a solution of the present automorphism question. Searchable database identifiers were available, but no subscription MathSciNet full review was read.

A stale third-party open/solved badge is not reliable: several aggregator pages retain the weaker original wording, and others call the strengthened problem open without addressing the September preprint. These were discovery aids only and are not evidence of definitive status.

## Exact residual claim and publication gate

The affirmative target can be formalized as existence of an ordered Dlab group G and alpha in Aut_ord(G), such that for every permitted ordered Dlab group A, every order-preserving monomorphism e:G->A, and every u in A, there is f in G with e(alpha(f)) != u^-1 e(f) u. The ambient class must be explicitly defined in a manuscript.

Verified priority conclusion: the earlier non-inner assertion is known; a six-family rank-one ambient version is already claimed/proved in the September preprint; the unconstrained ambient assertion is not settled by any source found here.

Still required before publication: all higher-rank ambient orders; all intended ambient families; a mathematically complete embedding/action argument independent of any unjustified Archimedean assumption; fresh adversarial proof review; and a renewed exhaustive priority search for any extension published after September 16. Absence of a search hit is not proof of openness or first priority.

## Search coverage

Queries included exact problem number; Dlab group(s) plus automorphism, conjugation, larger embedding, inner; the Gong–Yang–Zeng title; Zenkov–Medvedev 1999; Medvedev 2001; the Aristotle original solution and its Appendix A. Primary sources inspected: official Notebook and updates text, Dlab original PDF, current arXiv abstracts/full HTML, MathNet article/issue indexed bibliographic entries. No general theorem closing the higher-rank gap was found.
