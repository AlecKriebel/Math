# Hostile audit of integrated Paper I

**Audited source:** `paper/main.tex`

**Source SHA-256:**
`4e6bc3b47dd36b399920841261177f07aad6c240f0d6a161be924640bbc152f2`

**Date:** 2026-08-01 (America/Los_Angeles)

**Literature policy:** no new search; attribution was checked only against the
repository's completed narrow literature audit.

## Verdict

**Mathematical verdict: PASS.**  I found no incorrect directed index, missing
factor, false sign, quantifier reversal, denominator gap, equality error, or
triangle-certificate mismatch.  The complete-support theorem, non-strong
source-component bound, cited strongly-connected branch, and equality class
form an exhaustive directed trichotomy under the stated loopless and positive
incoming-degree hypotheses.

**Production verdict: PASS with minor wording revisions recommended.**  The
audited source compiles under Tectonic into a nine-page PDF with no warnings,
undefined references, overfull boxes, or underfull boxes.  The current source
contains the correct TeX commands `\quad` and `\qquad` in the triangle SOS
display.  One phrase in the abstract and section title should say
"beneficial fitness" rather than the potentially broader "every finite/all
fitness," because the exact formula reverses sign for `0<r<1`.  The theorem
itself correctly states `r>1`.

No manuscript file was edited during this audit.

## Claim-status table

| Integrated claim | Status | Audit result |
|---|---|---|
| Source-to-target convention `w_uv` | Correct | Every later index follows target-column normalization |
| Complete directed `1/r` coefficient | Correct | Factor `n^2(n-2)` and sign independently checked |
| Complete-support equality class | Correct | Exactly constant incoming columns; full-chain equality follows by column scaling |
| `n=2` exception | Correct | Every admissible two-vertex directed weighting fixes with probability `1/2` |
| Two-or-more source SCC branch | Correct | A resident source SCC is invariant, so singleton fixation is impossible |
| Unique source SCC bound | Correct | First-gain calculation and `(n-1)^2/n^2` factor are exact |
| Strongly connected noncomplete branch | Correctly attributed | Matches the completed hypothesis audit of Tkadlec et al. Theorem 1 |
| Exhaustiveness of directed trichotomy | Correct | Non-strong / strong noncomplete / complete are disjoint and exhaustive |
| Undirected support limit | Correct | Neighbor-degree limit and termwise deficit match the exact phase proof |
| Analytic differentiated system | Correct | Limiting complete-support chain is transient; derivative recursion is triangular |
| Pair loss indices `a_ji,a_ij` | Correct | Loss of target `i` uses surviving source `j`, hence `w_ji` |
| Singleton index `a_iv` | Correct | Source `i` competes into resident target `v` |
| Directed SOS identity | Correct | Columnwise product-reciprocal defect has the displayed pair-square form |
| Triangle denominator `P` | Correct and positive | All coefficients and `det M=3P/L` match the phase-two certificate |
| Triangle numerator `H` and SOS | Correct | `A,D,E` and strictness off `a=b=c` match exactly |
| Triangle replay `(2,3,5)` | Correct | Both displayed palindromic polynomials and prefactor check |
| Fixed-graph family quantifier | Correct | A graph-dependent tail is enough to refute `exists N0 forall N forall r` |
| Reversed `forall r exists N0(r)` order | Correctly left open | No limit interchange is made |
| TeX compilation | Clean | Tectonic log has no warning/error diagnostics |

## 1. Directed model and complete-support theorem

The model at lines 63--74 fixes the convention unambiguously:

\[
 w_{uv}=\text{weight of reproducing source }u\text{ into dead target }v,
 \qquad d_v^- = \sum_{u\ne v}w_{uv}.
\]

Thus all parent competitions normalize an incoming target column.  The
complete-support defect at lines 76--91 is consequently oriented correctly:

\[
 \mathcal E_{\rm dir}
 =\sum_v\sum_{\substack{u<z\\u,z\ne v}}
 \frac{(w_{uv}-w_{zv})^2}{w_{uv}w_{zv}}.
\]

The comparison

\[
 \rho_{\mathrm{dB}}(K_n,r)-\rho_{\mathrm{dB}}(G,r)
 =\frac{\mathcal E_{\rm dir}}{n^2(n-2)r}+O(r^{-2})
\]

has the correct sign and factor.  The equality condition is also sharp:
every off-diagonal entry in column `v` must equal a target-dependent constant
`c_v`.  Multiplying column `v` by `1/c_v` cancels from every competition at
that target, giving the literal `K_n` type-state chain for every `r>0`.  No
relation among different `c_v` is needed in the directed setting.

For `n=2`, positive incoming degrees force both off-diagonal weights positive.
From either singleton, mutant death gives extinction and resident death gives
fixation, each with probability `1/2`; the separately stated exception is
correct.

### Minor asymptotic-language recommendation

Theorem 1 displays an `O(r^{-2})` expansion without appending "as
`r -> infinity` for fixed `G`."  The abstract, surrounding discussion, and
final quantifier section make that meaning clear, so this is not a logical
error.  Adding the phrase directly to the theorem would make its quantifiers
self-contained and rule out any accidental reading that the remainder is
uniform over graph families.

## 2. Source-component bound

The condensation-DAG argument at lines 238--260 respects the edge direction.
A source SCC has no incoming support edge from another SCC.  If at least two
source SCCs exist, a singleton mutant leaves at least one source SCC entirely
resident.  Because that component cannot receive offspring from outside, it
stays resident forever; fixation probability is zero.

If there is a unique source SCC `C`, non-strong connectivity makes it a proper
subset of `V`.  A singleton outside `C` cannot send a descendant into `C`, so
only initial vertices in `C` can fixate.  For mutant `i in C`, write

\[
 s_i^+=|\{v:w_{iv}>0\}|.
\]

While `i` is the sole mutant, death of `i` is an extinction event with common
embedded-chain weight one.  Death of out-target `v` gives a gain with embedded
weight `p_iv(r)<=1`; every failed competition or irrelevant target death is a
holding event.  Therefore

\[
 \Pr_i(\text{first gain before extinction})
 =\frac{\sum_{v:w_{iv}>0}p_{iv}(r)}
 {1+\sum_{v:w_{iv}>0}p_{iv}(r)}
 \le \frac{s_i^+}{s_i^++1}\le\frac{n-1}{n}.
\]

Fixation requires such a gain.  Since `|C|<=n-1`, uniform initialization gives

\[
 \rho_{\mathrm{dB}}(G,r)
 \le\frac1n\sum_{i\in C}\frac{s_i^+}{s_i^++1}
 \le\frac{(n-1)^2}{n^2}.
\]

The limiting complete baseline is `(n-1)/n`; their difference is exactly
`(n-1)/n^2>0`.  This proves eventual strict suppression.  No assumption that
the non-strong chain absorbs almost surely is needed: the argument only bounds
the probability of ever hitting fixation.

## 3. Exhaustive directed trichotomy and attribution

The cases at lines 262--267 are exhaustive:

1. support not strongly connected: the source-component proof applies;
2. support strongly connected but noncomplete: the cited prior theorem
   applies; or
3. support complete: Theorem 1 applies, with exact ties only for constant
   incoming columns.

The first and third branches are proved in the paper.  The second is properly
attributed to Tkadlec--Pavlogiannis--Chatterjee--Nowak rather than presented as
new.  The repository's already-completed literature audit records that their
Theorem 1 uses the same source-to-target convention, directed nonnegative
loopless weights, uniform singleton initialization, strong connectivity, and
gives `r^*<=2n^2`.  I performed no new literature search in this audit.

The Allen et al. and Svoboda et al. contextual statements also match the
completed literature notes.  The bibliography entries and DOI strings agree
with those notes.

### Attribution wording caution

The abstract calls the source-component bound "new."  The repository audit
establishes that the cited Tkadlec theorem does not cover non-strong supports,
but it was deliberately narrow rather than a systematic novelty review.  A
maximally conservative paper would say "a source-component bound" instead of
"a new source-component bound," or qualify novelty by "to the best of our
targeted audit."  This does not affect attribution of the prior theorem or the
mathematical result.

## 4. Undirected support refinement

For singleton mutant `i`, the limiting changing events are death of `i`
(extinction) and death of one of its `s_i` support-neighbors (formation of an
adjacent pair), each target having the same death rate.  Hence the pair-before-
extinction probability is `s_i/(s_i+1)`.

An adjacent pair produces a connected mutant set of size at least two.  Every
mutant then has a mutant support-neighbor, so no mutant loss occurs at infinite
fitness; boundary deaths add mutants monotonically.  The exact averaged limit
and deficit in lines 283--295 follow:

\[
 \lim_{r\to\infty}\rho_{\mathrm{dB}}(G,r)=\frac1n\sum_i\frac{s_i}{s_i+1},
\]

\[
 \frac{n-1}{n}-\frac1n\sum_i\frac{s_i}{s_i+1}
 =\sum_i\frac{n-1-s_i}{n^2(s_i+1)}.
\]

The perturbation lemma correctly controls `O(1/r)` leakage from the limiting
reachable set.  The proof does not silently assume uniformity over graphs.

## 5. Directed differentiated expansion

The analytic argument at lines 308--406 is correct.  Under complete directed
support, a set with at least two mutants is pure birth at `epsilon=0` apart
from holdings, and a singleton goes either to extinction or a pair.  The full
limiting transient matrix therefore has spectral radius below one, so the
extinction vector is analytic.

For a proper `m`-mutant state with `m>=3`, differentiation gives

\[
 (n-m)q'_S(0)=\sum_{v\notin S}q'_{S\cup\{v\}}(0).
\]

Backward induction from `q'_V=0` proves `q'_S=0` for `|S|>=3`.  No derivative
of a smaller state enters because loss probabilities themselves vanish at
zero.

For pair `{i,j}`, loss of target `i` uses the only surviving mutant source
`j`; the relevant weight is therefore `w_ji` and the coefficient is `a_ji`.
The reverse loss uses `a_ij`.  The manuscript's

\[
 b_{ij}=\frac{a_{ij}+a_{ji}}{n(n-2)}
\]

is exact.

For singleton `{i}`, a resident target `v` receives the mutant source through
`w_iv`, producing `a_iv`.  With

\[
 O_i=\sum_{v\ne i}a_{iv},\qquad I_i=\sum_{u\ne i}a_{ui},
\]

the vertexwise coefficient

\[
 q_{\{i\}}(\varepsilon)
 =\frac1n+\frac{\varepsilon}{n^2}
 \left[O_i+\frac{O_i+I_i}{n-2}\right]+O(\varepsilon^2)
\]

has every factor correct.  Averaging uses `sum_i O_i=sum_i I_i=T_dir` and gives
`T_dir/[n^2(n-2)]`.

Finally, columnwise expansion yields

\[
 \begin{aligned}
 T_{\rm dir}(G)-n(n-1)(n-2)
 &=\sum_v\left[d_v^-\sum_{u\ne v}\frac1{w_{uv}}-(n-1)^2\right]\\
 &=\sum_v\sum_{\substack{u<z\\u,z\ne v}}
 \frac{(w_{uv}-w_{zv})^2}{w_{uv}w_{zv}}.
 \end{aligned}
\]

The equality class and comparison in Theorem 1 follow with no hidden
symmetry assumption.

## 6. Triangle theorem integration

The integrated six-state equations use the same indices as the phase-two
certificate.  All symmetric coefficients are copied correctly:

\[
 \begin{aligned}
 B_5&=12s_1s_2s_3-36s_3^2,\\
 B_4&=12s_1^3s_3-56s_1s_2s_3+12s_2^3+72s_3^2,\\
 B_3&=-24s_1^3s_3+12s_1^2s_2^2+80s_1s_2s_3
      -24s_2^3-90s_3^2.
 \end{aligned}
\]

The determinant identity `det M=3P/L`, positivity argument, `A,D,E,H`
definitions, rational difference, four gap identities, and three numerator
identities all match `phase2_triangle/triangle_classification.md` exactly.
The current TeX source correctly uses `\quad` and `\qquad` in these displays.

The theorem's strictness is complete: nonuniform positive weights give
`U>0`, hence

\[
 E=4s_2(3s_2U+V)>0,\qquad H\ge Er^2>0,
\]

while uniform weights make all gaps vanish and reproduce the baseline chain.

The `(2,3,5)` replay is also exact.  In terms of the global certificate,
`H=4P_{\rm replay}` and `P_{\rm global}=12Q_{\rm replay}`, so

\[
 -\frac{r(r-1)H}{3(r+1)P_{\rm global}}
 =-\frac{r(r-1)P_{\rm replay}}{9(r+1)Q_{\rm replay}},
\]

with exactly the coefficients printed in lines 537--539.  The strong-loss
coefficients `22/27` and `343/320`, and the path/star limits `7/12` and `9/16`,
also recompute exactly.

### Fitness-domain wording correction

The abstract says the paper classifies triangles "at every finite fitness"
and the section is titled "All-fitness classification."  The formal theorem
correctly restricts to `r>1`.  For a nonuniform triangle the exact formula has
the opposite comparison sign on `0<r<1`, because `r-1<0` while `H,P>0`.
Therefore the prose should read "at every beneficial fitness" and
"All-beneficial-fitness classification" (or explicitly "all `r>1`").
Within the paper's model the domain was already set to `r>1`, so this is a
scope-wording issue rather than a flaw in Theorem 2.

### Notation recommendation

The replay at lines 528--540 reuses `P(r)` for its numerator polynomial even
though `P` denoted the global denominator certificate immediately above.
The formula is correct, but names such as `N_{235}(r)` and `D_{235}(r)` would
avoid a local role reversal.

## 7. Quantifier and figure language

The family statement at lines 123--129 has the intended order:

\[
 \neg\left[\exists N_0\ \forall N\ge N_0\ \forall r>1:
 \rho_{\mathrm{dB}}(G_N,r)>\rho_{\mathrm{dB}}(K_{|V(G_N)|},r)\right].
\]

For any fixed `N`, the trichotomy either gives an exact tie or a graph-specific
tail `r>R_{G_N}` of strict suppression.  A threshold uniform in `N` is not
needed.  The reversed order

\[
 \forall r>1\ \exists N_0(r)\ \forall N\ge N_0(r)
\]

is logically distinct and is correctly left open.  The final section repeats
this distinction accurately.

The sentence before Figure 1 says "The two branches of the certificate."
The figure and caption are explicitly the **undirected** incomplete/complete
dichotomy, whereas the directed closure has three branches.  To prevent a
reader from mistaking the picture for the directed trichotomy, say "The two
branches of the undirected support certificate."  The caption already mostly
does this, so the issue is presentational only.

## 8. TeX and reproducibility

The audited hash compiles with

```sh
tectonic --keep-logs --outdir paper/audit_directed_v2 paper/main.tex
```

Tectonic produced a nine-page PDF.  Searching the retained log found no
`Warning`, `Overfull`, `Underfull`, `Undefined`, or `Error` diagnostics.
The compiled audit artifacts and exact verifier summaries are recorded in
`verification_summary.txt`.

## Required and recommended revisions

1. **Required scope wording:** replace "every finite fitness" / "all-fitness"
   for the triangle result by "every beneficial fitness" / "all `r>1`."
2. **Recommended theorem precision:** add "as `r -> infinity` for fixed `G`"
   to Theorem 1's asymptotic display.
3. **Recommended figure precision:** identify Figure 1's two branches as the
   undirected dichotomy, not the full directed trichotomy.
4. **Recommended attribution caution:** remove or qualify "new" before
   "source-component bound" unless a broader novelty review is intended.
5. **Recommended notation cleanup:** do not reuse `P` as the replay numerator
   after using it as the global denominator certificate.

None of items 2--5 changes a proof.  After item 1, the prose scope agrees
perfectly with the formal theorem.  No mathematical correction is required.
