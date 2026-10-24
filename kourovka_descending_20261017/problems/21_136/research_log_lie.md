# Independent dense-torsion / Lie research log — 21.136

## 2026-10-24 17:13–17:20 UTC — initial independent investigation

Discovery completion estimate: **8%**. This is a judgment about progress toward the original unrestricted problem, not a probability of correctness. The problem remains open in this effort.

Read the root AGENTS policy, the exact problem and priority screen, and the cached published Wilson paper before reading any newly authored approach notes. The target includes nonmetrizable profinite groups and strict cardinality less than the actual continuum. No arbitrary closed-subgroup inheritance of the ambient class bound is assumed.

The attempted mechanism was to replace finite generation in Wilson's Theorem C by a locality argument for the Zassenhaus Lie algebra. A concrete countercontrol immediately rules out this replacement under Theorem C's two stated topological assumptions alone: an infinite product of finite abelian p-groups, acted on by a cyclic permutation of order p, has dense torsion and a finite-exponent open coset but is not torsion. An independent subagent found the same all-prime construction without seeing the parent's version. Full proof will be recorded in approach_lie.md. Thus finite generation cannot simply be dropped even if the desired conclusion is weakened from finite to torsion.

A stronger consequence of Wilson Corollary 2.3 remains available for pro-p groups satisfying the original few-classes hypothesis: every nonempty open coset contains an open subcoset of finite exponent. The countercontrol fails this stronger condition inside its abelian base. Work is redirected to that stronger condition rather than reopening the disproved weak-locality route.

Independently obtained an abelian-by-torsion fusion lemma: if A is closed abelian normal, G/A torsion, and C≅Z_p lies in A, then N_G(C)'s image in Aut(C) is torsion and therefore finite; generators of C give continuum ambient conjugacy classes. The parent reports an independent derivation by the construction agent, as well as a general finite-prime reduction using Wilson Lemma 4.2. This is a restricted positive result, not a solution of the arbitrary profinite problem and not yet claimed original.

No publication, Git operation, or external communication occurred.

## 2026-10-24 17:20–17:29 UTC — stronger coset theorem and exact completion control

Discovery completion estimate: **10%**. The original arbitrary-profinite problem remains unresolved. The increase reflects proved restricted structure and a sharper exclusion of false repair mechanisms, not a complete solution.

Wrote approach_lie.md with exact proofs of the all-prime weak countercontrol, the failure of torsion lifting to the nonopen coset b+pB in B=∏C_(p^n), and an explicit open weighted p-filtration on B. The latter has locally finite, p-nil restricted graded Lie algebra, but its completion contains an infinite-order diagonal element. This blocks an attempted repair based solely on choosing open finite-dimensional graded layers.

The independent Lie adversary's child developed a substantive stronger partial theorem: virtually metabelian pro-p plus P0 (every open subgroup contains a bounded-exponent open coset) implies bounded exponent and local finiteness. The mechanism successively drops the exponent of commuting conjugation actions on A⊗Q_p. I independently reconstructed the central finite-two-operator argument before reading the child's complete proof; the Lie adversary then completed a step-by-step audit. The proof correctly keeps A fixed when passing to open subgroups and does not assume a global character decomposition in infinite dimension. The exact proof and audit are linked in approach_lie.md. Root has been asked for an additional fresh reviewer.

The direct noncommuting extension is falsified by the faithful two-dimensional Q8 representation and its fixed-point-free coset i⟨j⟩. This route is blocked beyond metabelian actions unless a materially new mechanism is supplied.

Checked the primary current arXiv version of Kionke–Otmen–Toti–Vannacci–Weigel 2507.19086v2, revised 28 May 2026 (HTML front matter dated 24 August 2026), concerning probabilistic/coset identities. Its analytic Examples 5.9 and 5.11 provide prior norm-zero semidirect-product context. It does not state our arbitrary metabelian P0 theorem in the inspected text. This limited inspection is not an originality audit or a proof of novelty. A full priority audit would be needed before any separate claim of originality.

No original complete Kourovka resolution, publication, DOI, or tracker update is claimed. Files remain confined to 21_136; Git/push are left to the root's scoped checkpoint.

## 2026-10-24 17:31 UTC onward — materially distinct isolated-class mechanism

Discovery completion estimate: **10%**. Began a new assignment from the parent after completing the dense-torsion/Lie attempt. The target is now the stronger local assertion that an infinite-order conjugacy class cannot be isolated relatively among infinite-order classes; this assertion is not assumed true.

First tested a possible finite-quotient contradiction from power-conjugators and their conjugates. A primary source, Glebsky arXiv:1604.06359, supplies a control: generalized Higman groups H(k), for p dividing k−1, have p-quotients retaining arbitrarily large orders of their cyclic generators. For p=2 and k odd, the pro-2 completion with its cyclic generator rotation realizes infinite-order conjugate elements x,y with x^y=x^k. Therefore one fixed self-conjugate power relation is not a contradiction. Isolation's uniform family of small conjugators is stronger and remains to be exploited.

The independent child initially obtained a metabelian local theorem. A new centralizer-torsion argument then removed the quotient-abelian restriction: if A is closed normal abelian and x has an isolated infinite-order class, its image cannot be finite in G/A. If that image b were finite, the projected neighborhood would be torsion, making C_(G/A)(b) torsion. A conjugator of x to a nearby integer power x^n, with n≡1 mod ord(b), then has a power in A and cannot act on a=x^ord(b)∞ by n^m. The local isolation passes to the quotient once its image is known infinite. Induction therefore excludes relatively isolated infinite-order classes in all virtually soluble profinite groups.

The Lie adversary independently checked this repair and reported no objection. Root reconstructed it as well and observed the same argument extends to closed normal abstract locally nilpotent kernels, using the explicit terminating-commutator contradiction. Root requested the child's fresh proof and will obtain another independent audit. Full exact notes are in approach_isolated_classes.md. This is a substantive partial local mechanism, not a solution for arbitrary pro-p or profinite groups and not an originality claim.

## 2026-10-24 17:45 UTC — local mechanism checkpoint ready for fresh root review

Discovery completion estimate: **10%**. All currently assigned local-family proof artifacts are complete and stable. The arbitrary local-isolation assertion and original Kourovka problem remain unresolved.

The child completed locally_nilpotent_extension.md and its parent independently audited it. A further fresh subagent verified the exact c-fold commutator index and produced the pro-3 affine control in which the iterated commutators converge to identity but never terminate. This sharply separates abstract local nilpotence from pronilpotence. The consolidated isolated_local_audit.md records the full restricted theorem and remaining gap.

Additional exact constraints were proved: an isolated infinite-order element is approached by torsion of unbounded orders in every neighborhood; its cyclic closure has finite prime support; and its procyclic normalizer has infinite index. Isolation restricts to any open subgroup containing the element after removing the other finitely many compact open-subgroup conjugacy orbits. This last fact gives the normalizer obstruction using the new abelian-kernel theorem.

The Glebsky prior-source control is recorded in isolated_sources/manifest.json. It supplies only fixed power-conjugation relations and is not claimed to realize the uniform small-conjugator family demanded by isolation. The source's entire ring-theoretic proof was not independently reconstructed.

Root has been notified that approach_isolated_classes.md and the descendant proof/audit files are ready for an additional nonauthor adversarial review. No publication, Git operation, or external communication occurred.
