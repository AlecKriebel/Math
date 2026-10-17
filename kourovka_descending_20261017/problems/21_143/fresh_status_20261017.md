# Fresh public-status audit: Kourovka 21.143

Audit date: 2026-10-17. Started at 2026-10-17 21:06:37 UTC; checkpoint completed at 2026-10-17 21:09:25 UTC.

## Finding and confidence boundary

**The strongest current evidence found supports retaining the standard automaticity of Thompson's group F as open.** The October 6, 2026 official Kourovka update lists 21.143 without a solution star, an unverified-AI sharp sign, or a solution comment. The proposer's own problem list, dated October 8, 2026, still leaves its automaticity question unstruck. These are affirmative observations of two current primary status records, not a proof that no undiscovered or unindexed claim exists.

No solution of standard automaticity, in either direction, was found in the bounded searches below. No mathematical novelty or solution is claimed in this note. The previously known restricted constructions and obstructions do not answer 21.143.

## Exact target and success criteria

Here F means the usual group of orientation-preserving, piecewise linear homeomorphisms of [0,1], with finitely many dyadic breakpoints and slopes powers of 2. Let S be a finite inverse-closed generating set and let a bar denote evaluation of words in F. The standard synchronous automaticity target is a regular language L contained in S* mapping onto F such that, for every s in S union {1}, the padded pair language

    R_s = { conv(u,v) : u,v in L and bar(u)s = bar(v) }

is regular. The s=1 case handles equality when representatives are not unique; it may be supplied directly or its regularity derived from the generator relations. Merely recognizing L is insufficient. In the equivalent geometric formulation the relevant representative paths synchronously fellow travel with one uniform bound whenever their endpoints differ by a generator or equality. The property is independent of the finite generating set. These conventions are the group-theoretic notion of Epstein et al.; see [Elder–Taback, §2.1](https://arxiv.org/pdf/1501.04313) and [Hauze, §2](https://arxiv.org/html/1801.01965v1).

A positive solution needs a complete regular automatic structure (or a fully justified equivalent criterion) for the whole group. A negative solution must exclude every possible structure, not just a convenient encoding, geodesic choice, or a bounded computational search.

## Primary status and priority records

1. [Official Kourovka home page](https://kourovkanotebookorg.wordpress.com/) identifies its latest post as the October 6, 2026 update-2. Its linked [main PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed p.198 / physical PDF page 198, has the exact question “Is Thompson’s group F automatic?” under 21.143, attributed to M. C. B. Zaremsky and described as well known. The entry is unmarked. The official page explains that a sharp sign means an AI proposal is still unconfirmed and the problem remains unsolved. Both text and rendered page were checked; snapshot retained.

2. [Zaremsky, Some open problems](https://zaremsky.github.io/open_problems.pdf), dated October 8, 2026, §2 question 2, still has the automaticity question. Its first-page update says it crosses out AI-solved problems. **Visual check matters:** on p.2 the immediately preceding amenability question is crossed out; the automaticity question is visibly not crossed out. PDF text extraction alone loses this distinction. The search engine initially returned an older January 2026 description for this same URL, so the fetched PDF controls. This is evidence of the proposer's displayed status, not independent validation of any crossed-out result.

3. The full current [mathematical manuscript catalogue](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/CONTENTS.md) at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a` was fetched and searched for `Thompson`, `automatic`, `automaticity`, `Kourovka`, and `21.143`. No standard automaticity claim appears in that catalogue. This check is limited to its titles, descriptions, and abstracts, not every proof file. It neither verifies nor endorses any other claim.

The question predates its 2026 Kourovka number: the primary [AIM January 2004 problem list](https://aimath.org/WWN/thompsonsgroup/thompsonsgroup.pdf), Q4.2, already asks about automaticity and synchronous/asynchronous combability. This note does not establish the earliest formulation or assign origin priority.

## What the nearby literature establishes

| Result or notion | Actual scope | Why it does not answer 21.143 |
|---|---|---|
| [Corwin–Golan–Hermiller–Johnson–Šunić, Autostackability of Thompson's group F](https://arxiv.org/html/1811.11691v1), Theorem 1.1; published Journal of Algebra 545 (2020), 111–134 | F is autostackable; an explicit bounded synchronously regular convergent **prefix** rewriting system is constructed. | Autostackability is a wider property. Its termination/flow condition does not supply a synchronous fellow-traveller bound for normal forms. The paper explicitly leaves automaticity open. |
| [Elder–Taback, Thompson's group F is 1-counter graph automatic](https://arxiv.org/pdf/1501.04313), Theorem 3.6; published 2016 | A deterministic nonblind 1-counter graph automatic structure over a symbol alphabet, using the infinite normal form. | Counters provide memory beyond finite automata, and encoded words need not be generator paths. The same paper excludes regular multiplier recognition only for its particular encoding (Lemma 3.7). It explicitly permits other encodings. |
| [Taback–Younes, Tree-based language complexity of Thompson's group F](https://arxiv.org/pdf/1501.04315), Theorem 4.1 | A deterministic nonblind 3-counter graph automatic structure with quasigeodesic normal forms over caret-type symbols. | It is another generalized structure; its normal-form obstruction does not exclude every symbol alphabet or generator language. |
| [Hauze, Restrictions on Potential Automatic Structures on Thompson's Group F](https://arxiv.org/html/1801.01965v1), Theorem 1.1; 2017 dissertation, arXiv 2018 | For standard S={x0,x1,x0^-1,x1^-1}, a language choosing one representative for each g of length at most \|g\|_S+c, for a fixed c, cannot sit inside an automatic-structure language. | This excludes geodesic and additive-near-geodesic structures over that standard generating set. General quasigeodesic distortion allows multiplicative slack; no implication from arbitrary automaticity to this additive bound has been supplied. This audit checked the statement, not its full proof. |
| [Kruengthomya–Berdinsky, Cayley Linear–Time Computable Groups](https://gcc.episciences.org/12503/pdf), Theorem 4.2; published March 31, 2024 | F has quasigeodesic normal forms with right multiplication computable in linear time on two tapes. §5 explicitly still calls standard automaticity open. | A two-tape Turing-machine time bound is not finite-state synchronous recognition. The paper also asks the weaker one-tape position-faithful question. |
| [Guba, The Dehn Function of Richard Thompson's Group F is Quadratic](https://arxiv.org/abs/math/0211395); published Inventiones Mathematicae 163 (2006) | Quadratic Dehn function. | This meets a necessary condition for automaticity; necessity cannot be reversed. |

Graph automaticity, also called Cayley automaticity, keeps regular padded multiplier relations but permits arbitrary symbol encodings instead of evaluation of generator words; see [Kharlampovich–Khoussainov–Miasnikov, §§6–7](https://ems.press/content/serial-article-files/29681). Counter graph automaticity relaxes the finite-state language requirement further. Neither change preserves the defining path interpretation automatically.

Two additional terminology traps require explicit separation:

- A **regular language of normal forms** exists (Guba–Sapir). That does not make the generator multipliers regular. Moreover “regular rewriting system” in the older [Guba–Sapir text](https://citeseerx.ist.psu.edu/document?doi=ee7445b4a2336be9085e65c7300562f1e9267dcb&repid=rep1&type=pdf) means its left-hand sides form a regular language. The later autostackability paper, §2.2, explains that the paired rule relation in that system is not synchronously regular (indeed not context-free). These different regularity conventions must not be silently identified.
- **FA-presentability of the entire group operation** requires finite automata for multiplication with both inputs variable. For finitely generated groups this is stronger than standard group automaticity, which only asks for multiplication by each fixed generator; the implication passes through virtual abelianness, not an identification of arbitrary encodings with generator paths. [Nies–Thomas, FA-presentable groups and rings](https://www.cs.auckland.ac.nz/~nies/papers_till_09/NiesThomas_FAPresentableGroups.pdf), pp.569–571, states that finitely generated FA-presentable groups are virtually abelian. Thus statements that F is not automatic *in the Khoussainov–Nerode sense* concern another property and cannot settle 21.143.

## Search scope, provenance, and exact remaining gap

Checks ran on 2026-10-17 from 21:06:37 UTC to 2026-10-17 21:09:25 UTC. Search families combined the exact group name, variants of automaticity/automatic/not automatic, 21.143/Kourovka/Zaremsky, claimed/solved/solution/proof, arXiv, and 2025/2026. Search results alone were not treated as verification; relevant primary texts were opened. Broad queries also produced unrelated uses of “Thompson” and “automatic”. No external communication was initiated or prepared.

The original Albany URL for Zaremsky's list redirected to institutional login during the check. The author's active GitHub Pages URL supplied the current public PDF. The `alglog.org/21tkt.pdf` mirror returned a fetch error; the official WordPress-hosted current PDF was directly accessible. Neither failure was interpreted as mathematical evidence.

The two current status PDFs, their checked rendered pages, the full catalogue snapshot, retrieval times, and SHA-256 hashes are retained in `fresh_status_sources/manifest.json` and adjacent files. Rendering used `pdftoppm`; complete relevant pages were visually inspected. The source snapshots are evidence for reproducibility, not new authored results.

**Exact remaining mathematical gap:** no regular synchronous automatic structure for all of F, and no universal obstruction ruling out every such structure, is established here. Bounded failures, nearby language classes cannot bridge that gap by themselves.

**Checkpoint estimate:** status/priority audit 100% of this assigned bounded check; discovery/solution of 21.143 remains 5% as an early scouting estimate, not a quantitative probability of success. No automaticity result was promoted.

Independent adversarial wording check completed at 2026-10-17 21:10:02 UTC: no fatal status or definitional overclaim found. The standard-generating-set scope of Hauze and finitely-generated scope of the FA-presentability comparison were made explicit. Audit completion remains 100%; solution scouting estimate remains 5%.

Final checkpoint 2026-10-17 21:11:10 UTC: completed the requested public-status and terminology audit, independently adversarially reviewed the companion priority note, and incorporated the equality-relation precision correction. Bounded audit completion: 100%; solution scouting estimate: 5%. No further research, Git mutation, publication, or outreach performed.
