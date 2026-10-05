# Research record

Target: ID 2515, KOU-21.6; queue rank 766. Checked 5 October 2026.

## Source and prior-attempt recovery

The numeric problem landing page failed in the web reader. The full supplied public problem corpus identifies the intended cyclic-block question. Its mathematical content was checked against the October 2026 primary Notebook, printed page 177, including visual inspection. The problem is attributed to A. O. Asar and has neither a solved marker nor an unverified-AI marker there. The editor repository contains no textual 21.6 entry in the inspected page.

The live repository main queue still showed this exact target as queued, 0/5. The main attempts directory did not contain 2515. Exact-ID code, branch, commit and pull-request searches found no target attempt. A topic search returned an unrelated Kirby pull request; its actual content was inspected and not treated as prior work on this problem. The complete supplied research-results object has no KOU-21.6 key; the problem record itself contains dated literature triage, not a proof. These checks do not cover deleted branches or every unpublished artifact.

## Approach 1: construct compatible cyclic blocks

The first route was to extract a subgroup from a nested sequence of finite p-actions, guided by Asar's existing cyclic-block construction. Relevant literature includes the 2011 Journal of Group Theory paper and two 2017 papers, not just the 2006 paper in the inherited triage. Small prefixes of the displayed Asar construction were reproduced computationally during exploration; no theorem about arbitrary subgroups follows from those examples.

The obstacle is real: a finite regular action has the desired cycle property, but infinite regular permutations have infinite support. Moreover, even generators whose own cycle supports are blocks do not guarantee the property for products, as the explicit dihedral control in the verifier shows. No extension lemma placing a compatible construction in an arbitrary transitive p-group was established. This route was abandoned rather than assuming compatibility.

## Approach 2: seek a minimally transitive finite obstruction

Inside C_2 wr C_2^2, impose the parity equation sigma(f)=t_1. The resulting group has order 32 and degree 8. Exact enumeration showed that it is minimally transitive and fails the cycle-support condition. Section 1 of PROOFS.md replaces this computation by a complete proof using translation differences on four-point functions. The finite group is a standard kind of minimally transitive p-group construction; no novelty claim is made for it.

A finite obstruction alone would leave a serious gap, since the intended question concerns totally imprimitive infinite finitary groups.

## Approach 3: preserve the obstruction in an infinite wreath tower

Repeatedly take the imprimitive wreath product with C_2, embedding the previous group into the first copy. The increasing union is a transitive locally finite 2-group of finitary permutations on a countable set, and its finite blocks are cofinal. Its bottom eight-point block stabilizer induces exactly the finite obstruction P.

The key universal step is Lemma 4: for every transitive subgroup H of the union, the setwise stabilizer of that block induces a transitive subgroup of P, necessarily P itself. Lifts of the two crossing-cycle witnesses then violate the block property for H. Their behavior outside the block is irrelevant. This closes the finite-to-infinite gap and gives a full negative answer with S=G.

Stop after three substantive approaches: the full counterexample is proved. No fourth or fifth approach is needed.

## Literature status boundary

The 2011/2017 works construct or study cyclic-block groups; they are not being cited as a solution of the universal containment question. The 2022 proper-FC-subgroup paper was checked at publisher/author abstract level only. The related 2026 nonexistence paper currently carries a publisher retraction label; a May 2026 corrigendum was also inspected. Neither is a premise of this proof, and neither was promoted to a solution of 21.6. The bounded searches located no prior exact answer to 21.6, which is not a proof of novelty.

Independent review of the frozen proof and executable certificate is required before any publication step. No remote write was performed in this investigation.
