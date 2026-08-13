# Independent audit of the one-linkage theorem in at most three species

**Audit date:** 2026-08-12 PDT  
**Verdict:** **STRICT PASS.**

This audit concerns the exact target

```text
b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563
    research_notes/proof_first_single_linkage_at_most_three_species_theorem.md
```

at 314 lines and 12807 bytes.  The theorem is classwise, uses one physical
CTMC, and quantifies over arbitrary strongly connected reaction graphs and
arbitrary fixed positive rate constants.  The proof is structural and
analytic; no list of supports, orientations, reaction words, or population
states is inspected.

## 1. Exact dependency replay

The displayed local dependencies were rehashed at the following exact
bytes:

```text
9be70e2b6c9ce5c4762bf3130246f1ea660bea73f41aa7abdd997853cc0a6b04
    research_notes/proof_first_hard_enabled181_access_word.md
4028c026a7d01c1e0930bdbdaa75216a79402078999d6450c283a77eb2a04883
    research_notes/proof_first_hard_enabled181_access_word_independent_audit.md
5b64e251035eedb3e5afe1d37881b3e1f4db45055ac5ab9a9ab165764720f0d1
    research_notes/proof_first_single_linkage_structural_exhaustion_audit.md
9d878860cb6427688995784ed230776d982eca758a6c306be4180c3e8ffaaf03
    research_notes/proof_first_single_linkage_2d_exception_service_theorem.md
26e97c6edd5566e0fad9326523b017d86c1391c2b8762ca8eacddc06c41fd52a
    research_notes/proof_first_single_linkage_2d_exception_service_independent_audit.md
8a34f9934f9ffdd078850070de561aa3cf3f734a9fbeb2e4f08bc68c5e106262
    research_notes/proof_first_single_linkage_structural_reduction_and_mesoscopic_gap.md
933c14cad99b8cf5bc1e2237f3be417aebfb344d1751f7c58be2b284c562d5ab
    research_notes/proof_first_single_linkage_balanced_full_five_independent_audit.md
afd696d3b28709619759936cfb6e4536859300985bb6e594cff840fb4c7db7f9
    research_notes/proof_first_single_linkage_two_disabled_top_bounded_carrier.md
c96995531a79570d26330f2babeeba2998323c1787bda3627b2c538a38ee7922
    research_notes/proof_first_single_linkage_two_disabled_top_bounded_carrier_independent_audit.md
389e3b446006e9313238a0b4b0029f39e0f1cee0c2d90faf6e63cccf38a581e1
    research_notes/proof_first_separated_full_all_clock_joint_return_theorem.md
096ba806daa3f7f1bc336986d3248976ac8ade084cfbf5a60e524ceec96f75a6
    research_notes/proof_first_separated_full_all_clock_joint_return_independent_audit.md
3d45867b4dd07a92ce43054767b7e7a680fa77035b7f2e1021dcb5004097f962
    research_notes/proof_first_global_t3_2_classwise_skeleton_scoped_audit.md
```

In particular, the separated dependency is the final post-audit target
`389e3b...` with exact-byte hostile audit `096ba8...`.  Neither rejected
predecessor `08c216...` nor `490f424...` is used.

## 2. Projection and nonexplosion

Let coordinate \(i\) have the fixed value \(m_i\) on the closed class
\(\Gamma\).  If an active linkage has an enabled complex \(y_0\) at \(x\),
put \(r=x-y_0\ge0\).  A directed path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_k
\]

is realized by the literal population path

\[
                         r+y_0,r+y_1,\ldots,r+y_k.
\]

Each next source is enabled by the preceding target.  Closure keeps every
state in \(\Gamma\), so every complex on the path has the same
\(i\)-coordinate.  Strong connectivity reaches the whole linkage.  The
constant falling-factorial factor is positive and can be absorbed into
each labelled rate.  Deleting the fixed coordinates is injective on
\(\Gamma\), and it is surjective onto the projected class by definition;
the rate calculation intertwines the generators.  Projected strong graphs
which share a vertex have strongly connected union, and parallel labelled
channels preserve the sum of transition rates.  Thus the asserted
projection is an exact CTMC conjugacy.

A positive total-population increment can have only a degree-zero or
degree-one source, hence its aggregate rate is \(O(1+|x|_1)\).  Before a
population-level exit, the state space is finite and all rates, including
quadratic neutral rates, are bounded.  Localization and Gronwall exclude
population escape in bounded time; bounded rates on the remaining finite
sublevel exclude accumulation there.  This proves nonexplosion without
discarding a quadratic physical clock.

## 3. Tier identity, proper top block, and access word

For an enabled complex, its stochastic propensity is its deterministic
monomial times a factor converging to a finite positive constant; a
disabled complex has zero propensity.  Consequently the top stochastic
sources are the highest deterministic tier meeting the eventually enabled
set, and failure is exactly the case in which every member of \(D^1\) is
disabled.

The common top scale diverges.  Indeed, an escaping retained coordinate is
dynamic, hence occurs in some complex; that complex's deterministic
monomial diverges, and the top monomial dominates it.  This supplies the
\(A_n\to\infty\) premise used in target Section 3.

If \(D^1\) were the whole support, normalize
\(\log(x_n\vee1)\) to a nonzero \(w\ge0\).  Tier equivalence makes \(w\)
orthogonal to every reaction vector.  A positive component of \(w\) occurs
on a divergent coordinate, so the exact invariant \(w\cdot X\) would be
unbounded along one fixed class.  This contradiction proves that \(D^1\)
is proper.

When \(D^1\) contains an enabled seed, strong connectivity supplies a
simple path from that seed to the first exit from \(D^1\).  Each target
creates the next source.  Bounded displacement preserves comparison of
every preterminal rate with the common top scale and leaves every competing
rate at most a fixed multiple of that scale.  The first-exit edge has a
divergent factorial gap.  These are exactly the hypotheses of the generic
all-clock access-word estimate at `9be70e...`/`4028c0...`; arbitrary
competitors, actual endpoints, physical duration, and the common fourth
power are included.  The proof does not assume an immediate descending edge
from the initially enabled top vertex.

## 4. Exhaustion of a disabled top

A disabled pure complex has deterministic monomial one.  Since the top
scale diverges, every failed top complex is therefore mixed binary, with
one zero cofactor and one divergent carrier.  The number of divergent
coordinates gives the symbolic split.

* In one dimension the published pure-multiple theorem applies.
* In two dimensions, absence of a pure multiple for \(A\) forces
  \(\mathcal C=\{A+B\}\cup T\) with
  \(\varnothing\ne T\subseteq\{0,B,2B\}\).  For
  \(|T|=1,2\), direct rank gives deficiency zero.  The sole residual
  support is \(\{0,B,2B,A+B\}\), covered by the audited all-clock
  two-dimensional theorem.
* With three divergent coordinates every complex is enabled.  With two
  divergent coordinates, the failed top is a nonempty subset of
  \(\{A+C,B+C\}\): a singleton is exactly the separated family and has
  \(\log(A/m(B))\to\infty\), while a tie is exactly the balanced family.
  Every proper balanced support has rank \(m-1\) and deficiency zero; only
  the full five-complex support has rank three and deficiency one.
* With one divergent coordinate, a singleton is again separated, while the
  tie \(\{A+B,A+C\}\) has \(B=C=0\) and is exactly the bounded
  two-disabled-top family.

The frozen and invariant alternatives in the three local theorems cannot
support the corresponding escaping sequence inside one fixed irreducible
class.  This verifies that the target list has neither a missing face nor
an incorrect rank assertion.

## 5. One potential and a uniform statewise selector

Take \(\ell=0\) and one fixed \(K\ge1\).  Then

\[
             W(x)=\left(K+\sum_i\log(x_i!)\right)^4
\]

is nonnegative and proper on the projected lattice.  Every residual local
theorem is valid for this same choice.  The two-dimensional exception,
pure-multiple, and deficiency-zero cases prove recurrence for their entire
fixed support and do not enter this stopped composition.

For a fixed residual network, the candidate menu is finite: the support has
finitely many proposed proper top blocks and simple labelled first-exit
paths, and there are finitely many exceptional types and species
relabellings.  Each candidate is a literal statewise, all-clock stopping
rule on its start domain.  Its duration and actual endpoint have the
integrability stated by the corresponding local theorem.

Choose one \(0<\eta\le1\).  Call a state bad if no admissible candidate
\(R_j\) satisfies

\[
 \mathbb E_x[W(X_{\tau_j})-W(x)+\eta\tau_j]\le-1.
\tag{5.1}
\]

If the bad set were infinite, propriety would give an escaping sequence of
bad states.  Extract a proper tier subsequence, then use finiteness to fix
availability, tier ordering, relabelling, and the candidate delivered by
the structural split.  On an enabled-top, separated, balanced, or
two-disabled-top subsequence, that one fixed candidate has drift tending to
\(-\infty\), contradicting badness.  A frozen or invariant subsequence is
impossible in the fixed class.  Hence the bad set is finite.

Outside it, select the least candidate satisfying (5.1).  This is the
repair which an arbitrary priority among merely admissible candidates
would not provide.  The state space is countable, so the selector is
measurable, and it supplies target (5.2) with the uniform choices
\(\delta=1\) and the fixed \(\eta\).  No compactness assertion is being
used to infer a positive infimum of unrelated statewise margins.

## 6. Physical-time Foster conclusion

Apply the state-selected Foster lemma with the episode region equal to the
whole complement of the finite bad set (or with any separately supplied
generator-good region).  Conditional iteration telescopes the one common
\(W\), pays \(\eta\) times actual physical duration, and pays \(\delta\)
per completed exceptional episode.  If the finite target is met inside an
episode, its hit is recorded immediately; completing that single episode
only for the drift ledger gives an accounting time no smaller than the
physical hitting time.  Target equation (6.1), monotone convergence, and
nonexplosion therefore give finite mean physical hitting time of the finite
target from every state.

For completeness, if the class is not a singleton, every target state has
positive finite total jump rate.  Wait for one ordinary physical jump.  It
has finite mean holding time and only finitely many possible successors;
the just-proved hitting estimate returns each successor to the target in
finite mean time.  These excursions define a stochastic return kernel on a
finite set with finite statewise mean duration.  A recurrent state of that
finite kernel consequently has finite mean positive physical return.
Irreducibility promotes positive recurrence to every state of \(\Gamma\).

## 7. Render and final disposition

Pandoc's MathJax render completed with 60 inline and 17 display-math nodes.
An independent Pandoc-to-LaTeX render using the single-backslash TeX-math
extension compiled successfully with Tectonic to a six-page PDF.  The only
TeX warnings were harmless box-layout warnings, largely from unbreakable
SHA strings; no formula, tag, character, or control-sequence error occurred.

The exact target `b7306d...` therefore earns **STRICT PASS** as an
unconditional proof of its stated one-active-linkage theorem.  This audit
does not assert any two-active-linkage theorem or the full global
\((\mathrm{T3})\text{--}(2)\) composition.
