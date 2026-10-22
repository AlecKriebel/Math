# Frozen independent source-question report

**Outcome:** a full-scope negative answer to Farb Question 7.6 is reconstructed in `DERIVATION.md`: for every fixed genus g>=2 and finite depth k>=3, the spectrum of I_g(k) has unbounded multiplicity when multiplicity counts ambient orientation-preserving Mod_g conjugacy classes. This is a mathematical reconstruction, not a novelty or priority determination.

**Central mechanism:** choose filling separating twists, use explicit commutators to reach the specified Johnson depth, and take high powers of two independent hyperbolics to obtain a free convex-cocompact subgroup H at that depth. Horowitz's trace-word construction produces arbitrarily large common-length families in H. An elementary compact-core lemma gives a uniform finite bound on how many H-conjugacy classes can merge in the full disk-stabilizer group. Uniqueness of a pseudo-Anosov's invariant Teichmuller disk forces every ambient conjugator into that stabilizer, completing the passage to ambient conjugacy.

**Strongest verified claim:** for every N there is a common positive length t, allowed to depend on N, supporting at least N pairwise ambient-nonconjugate pseudo-Anosovs in the single fixed I_g(k). The derivation includes genus 2 and the source's exact filtration indexing.

**Exact limitations:** no claim of infinite multiplicity at one length, no ambient primitivity claim, no simple-loop result for Question 7.7, and no result for the intersection of all Johnson terms. No mathematical gap has been identified in this family's written argument, subject to independent adversarial review of the compact-core lemma and standard input theorems. The proof uses established Horowitz and Thurston/Teichmuller theory; finite computations alone are not offered as proof.

**Adversarial self-checks:**

- An arbitrary infinite-index subgroup is insufficient: a normal subgroup can have unbounded conjugacy splitting within one ambient class. The argument instead first fixes a subgroup with compact convex core and proves a uniform bound explicitly.
- The entire Thurston group need not have finite index in the full stabilizer. The comparison lemma does not assume this.
- A finite derivative kernel does not imply faithfulness on the ambient stabilizer. The proof only needs the restriction to the constructed free subgroup to be faithful, which follows from the faithful original filling-pair representation.
- Entering an arbitrarily deep filtration term by taking powers alone would be invalid. Explicit commutators enter I_g(2r); the later powers stay in that same fixed term.
- The orientable lattice route is obstructed by the faithful homology action of an orientable disk stabilizer. It is not silently substituted for the nonorientable separating-twist disk.
- Root-freeness in H is not promoted to root-freeness in Mod_g.

**Reproducibility:** `verification.py` ran successfully with exact integer arithmetic. It checks 12 commutator cases and Horowitz levels 1-5, including 32 pairwise nonconjugate common-trace words at the largest level. See `verification_results.json`. The full proof is symbolic and does not depend on these finite parameter bounds.

**Independence and provenance:** only the original author-hosted question source and mathematical background were consulted. No PR, submitted result, queue, inventory, candidate/root review, other family work, or outcome was inspected. No individual was contacted. No subagent was spawned. No Git index, branch, commit, push, release, Google Workspace, or Zenodo operation was performed. All work is confined to this family's folder; retrieved source bodies and renders are ignored under `source_bodies/`.

The exact reading scope and hashes of retrieved PDFs are recorded in `SOURCES.json`. The freeze manifest hashes all authored files other than the manifest itself and records the final checkpoint. Authored files are not to be edited after that freeze; corrections after independent comparison should be stored separately by the parent.
