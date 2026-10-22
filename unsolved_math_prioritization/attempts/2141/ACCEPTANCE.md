# Acceptance of Wang's prior EP486 counterexample

## Accepted theorem and exact formulation

There exists one infinite set A of positive integer moduli, with one fixed
arbitrary subset X_q of Z/qZ for every q in A, such that the positive
survivors B of all activated congruence restrictions have

    liminf_{x -> infinity} (1/log x) sum_{1<=m<x, m in B} 1/m <= 177/200,
    limsup_{x -> infinity} (1/log x) sum_{1<=m<x, m in B} 1/m >= 49/50.

The same A and X work for every cutoff x. In particular, the logarithmic
density does not exist. The construction proves these inequalities with
strict activation q<m and with the original inclusive activation q<=m.
Each installed residue comes from q<m<2q and is nonzero, so the two sets
are exactly equal. The general primitive-set bridge is also valid, but it
is not needed for this particular construction.

The result answers the arbitrary-residue logarithmic-density existence
question in Erdős's 1961 I.26. No uniform bound on the number of residues,
coprimality or summability assumption is imposed. The proof retains the
activation threshold and does not replace it with an undelayed sieve.
This is acceptance of Wang's prior theorem, not a novel solution claim.
Singleton-residue EP25 remains outside the theorem and this acceptance.

## Basis of acceptance

The complete primary audit in AUDIT.md checks the finite periodic recovery,
arithmetic skeleton, finite randomness, exact candidate equivalence,
collision removal, conditional fresh-bit probabilities, entropy margins,
simultaneous block selection, summable footprints, separated scales,
one fixed infinite system, recovery/deletion subsequences and all activation
and cutoff conventions. No unresolved mathematical gap was found in the
specified prose proof of Theorem 1.1.

The separate FOCUSED_AUDIT.md independently reconstructs the finite deletion
lemma and the original-activation bridge. It gives the exact conditioned
probability for each candidate, explains why cross-candidate independence
is neither available nor needed, proves the binomial tail and entropy
bounds, and checks the sum-of-failure-probabilities selection argument.
Its acceptance is expressly focused rather than a second global-theorem
certification. The full general derivations of both audits are retained.

Historical exact arithmetic and finite-mechanism checks passed in normal,
-O and -OO modes where recorded, with byte-identical outputs. They support
the written arguments; they neither prove asymptotic assertions nor provide
formal proof-assistant certification. They were not rerun for this edition.

## Formal evidence and review status

The manuscript is Shouqiao Wang, *A Proposed Solution to Erdős Problem 486*,
ten-page PDF, 350612 bytes, SHA-256
01ce6f1d22b0c9208cc45ecaa15039f0ee13ea75c334908ca65f371c365b9048.
The primary audit text-read all ten pages and the full retained TeX,
and visually inspected manuscript pages 6 and 9 and original Erdős printed
pages 235–236. SOURCES.json records the exact historical inspection scope.

The retained author tree at d28713ac8245ca86a686b8c67370a8d19d81b242
differs from the externally reported replay commit
61325b10bbdc29f4fb5e0618b414b9f2189333ad. Their byte identity was not
established. The formal implementation inspected uses a four-color biased
construction; the prose proof audited here uses fair bits. The statement
readback is not a claim that this prose construction was formally replayed.
No Lean build, imported executable, third-party verification script,
local axiom calculation or full formal dependency audit was performed.

Acceptance is independent internal AI mathematical review of these specified
arguments. The work is AI-assisted and unrefereed. No external human peer
review, journal acceptance, current tracker status or community-wide
resolution is claimed. Lack of a local formal replay is a limitation of
formal evidence, not an unresolved mathematical step in the accepted prose.

## Edition treatment

One optional explicit finite-threshold computation and the focused audit's
finite toy parameters and numerical computational witnesses are omitted.
Historical checker descriptions are clarified and the source metadata
filename is updated. These changes are editorial only. General theorem
constants and their analytic derivations are preserved without alteration.
Code, source copies, PDFs, raw certificates, datasets and private
coordination are excluded. Original sealed audits are immutable inputs.

Sources: [Wang manuscript](https://multiscalar.ai/results/erdos-486/paper.pdf);
[pinned author source](https://github.com/ShouqiaoW/erdos/tree/d28713ac8245ca86a686b8c67370a8d19d81b242/486);
[Erdős original](https://users.renyi.hu/~p_erdos/1961-22.pdf);
[external replay report](https://github.com/ibrahimmian36/Pilus/blob/main/reports/erdos-486.md).
