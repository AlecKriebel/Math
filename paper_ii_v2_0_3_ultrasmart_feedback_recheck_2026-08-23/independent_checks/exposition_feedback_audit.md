# Independent exposition, metadata, and cosmetic audit of Paper II v2.0.3

**Audit date:** 2026-08-23  
**Role:** independent submission-facing check; the external-AI claims were treated as hypotheses  
**Source reviewed:** `paper_hybrid_threshold/main.tex` and the frozen 21-page PDF at scientific tag `simultaneous-amplification-beyond-three-halves-v2.0.3` (`bd66a3bbf1c530ef67a4b7be5ee69a6825678457`)  
**Source changes made:** none

## Readiness conclusion

**Scientific/expository conclusion:** accept v2.0.3. The feedback's figure, abstract, floor-effect, mechanism, early-establishment, coordinate-uniformity, and gate-union-bound issues are already fixed. The suggested finite-size numbers and polynomial weak-cut extrapolation should **not** be added as claims. The current `R_{\mathbb Q}` display and MSC code `60J10` should be retained.

**bioRxiv conclusion:** I found no manuscript-content blocker. The PDF, abstract, declarations, prior-version disclosure, links, and supplement metadata are coherent. Posting remains conditional on the human author's live-form review, license/terms acceptance, and successful upload. Because a substantially similar v1 manuscript is already public in Zenodo record `21852072`, bioRxiv's duplicate-online-content screen may escalate it; the current package correctly instructs the author to disclose that record rather than answer “No.” This is a screening risk, not a defect that can be removed by cosmetic editing.

**Journal of Mathematical Biology conclusion:** the mathematics is submission-ready, but the present PDF is **not strictly JMB-title-page compliant**. JMB expressly requires city and country, including for unaffiliated authors; the title page currently says only “Independent Researcher.” Before JMB submission, add the author's truthful city and country and rebuild/re-freeze. Do not invent them. This is the only actionable submission blocker found in this audit, and it is journal-specific metadata rather than a scientific issue.

Two nonblocking cleanup items are also worth fixing in a journal-format pass: cite Figure 1 explicitly in the prose, and repair one relative path in `vendor/README.md`. JMB's preferred visible DOI and caption styling can be handled in the same pass or by the Springer Nature template.

## Frozen-artifact checks

- A clean independent Tectonic rebuild produced SHA-256 `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`, byte-for-byte identical to the frozen PDF.
- The build log has no undefined reference, multiply-defined label, overfull-box, underfull-box, or substantive package warning.
- The PDF is 21 US-Letter pages, unencrypted, has the correct title/author/subject/keyword metadata, and embeds all fonts.
- All 12 citation keys have exactly one bibliography entry; there are no missing or duplicate bibliography keys. All 49 LaTeX labels are unique and every `\ref`/`\eqref` target exists.
- The submission-material checker passes. The PDF hyperlinks target the author's email and ORCID, the v2.0.3 repository tree, all three relevant Zenodo records, and the nine external scholarly DOIs.
- Pages 1, 4, and 19–21 were rendered at 200 dpi and inspected. The front matter, figure, discussion, declarations, data/code statement, AI disclosure, and references are legible and free of a visible collision or clipping defect.

## Disposition of every feedback item

### 1. Finite-size sentence — **invalid as a manuscript claim; reject**

The suggested arithmetic is a plausible *heuristic*: the limiting Bd bracket at `r=1.5` is about `0.0070924`, so comparing it with an empirical `3/q` deficit gives `q` of order `423`; at `r=1.502`, the analogous quotient is of order `1.4×10^3`. This does not establish a finite-size threshold for the graph family in the theorem:

- the `3/q` coefficient is an empirical separated-trace approximation, not a proved uniform error bound;
- the exact connected graph also uses the least-dyadic weak-cut diagonal `epsilon_t`, whose finite-size cost is not quantified;
- positivity at a few values of `t` does not certify a first or permanent positivity threshold; and
- converting `t` to `n_t` magnifies a heuristic substantially because `n_t` is dominated by `t^4`.

The current discussion—“the proof gives eventual positivity ... but no useful finite-size bound on `t_0(r)`”—is accurate. Adding the proposed numbers would blur the manuscript's careful separation of proof from numerical evidence. No edit is warranted. If such estimates are ever published, they should be a separately labelled exploratory numerical supplement with a specified computation and no threshold claim.

### 2. Floor non-monotonicity — **valid concern, already fixed; accept current text**

The current discussion now states that `m_t=floor(lambda_* t)` contributes `O(t^{-1})` oscillations to the scaled finite-`t` responses and that positivity need not appear monotonically before the eventual regime. That directly resolves the expository concern.

The four alleged finite values are not needed for the theorem or the warning and should not be promoted without a frozen, independently specified computation. Switching to round-to-nearest would define a different frozen family and require a new package/replay/review cycle for no mathematical benefit. **Reject** that change.

### 3. Mechanism sentence — **valid, already fixed; accept current text**

The discussion now says exactly that the singular boundary `sigma downarrow 0` gives `F_r(0)=r(2r-3)`, recovering the `3/2` endpoint, while optimizing over positive `sigma` moves the tangency to `R_hyb`. This is clearer and more exact than merely saying the gain is “about 0.0029.” No further edit is needed.

### 4(a). `O(K^2/C)` versus `O(K/C)` — **valid, already fixed; accept**

The early-establishment lemma and proof now give `O(K/C)`. The proof explicitly separates an expected `O(K)` number of ordinary-count changes from an `O(1/C)` hub-change hazard ratio per such change. This removes the earlier ambiguity.

### 4(b). Uniformity in hub and pendant coordinates — **valid, already fixed; accept**

The paragraph immediately introducing the displayed deficit odds now says “uniformly in the hub and pendant coordinates.” No edit is needed.

### 4(c). Gate union bound — **valid, already fixed; accept**

The gate proof now explains that failure requires at least one reversal even though reversal need not imply failure; hence the union bound on reversals upper-bounds failure. No edit is needed.

### 4(d). Empirical exponential reciprocal quantities — **optional observation; reject as an addition**

The paper proves the weaker bound it needs, uniformly on fitness compacts. An uncited numerical impression of exponential decay would not strengthen the theorem and would introduce a new evidentiary burden. Retain the proved `o(C^{-1})` statement.

### 5. Weak-cut scale and polynomial `e_t` — **invalid extrapolation; reject**

Linear response in `epsilon` for each fixed small finite chain is compatible with finite-dimensional perturbation theory, but it does not imply that the corresponding coefficient is polynomially bounded as graph size grows. The transient state space grows with `t`, and neither the finite examples nor the proof supplies a uniform polynomial condition bound. Consequently the proposed conclusion that `e_t` is “only polynomial” is unsupported.

The current discussion is appropriately cautious: the exact diagonal may select very small positive weak edges. No change is required. If an extra defensive sentence is desired, the exact safe addition is:

> No quantitative upper bound on `e_t` is claimed.

That sentence is **optional and nonblocking**.

### Figure 1 — **already fixed; accept**

The source draws all ten edges of the displayed five-vertex clique. In particular, both formerly alleged missing chords `c_1c_4` and `c_2c_3` are present and visible in the rendered PDF. The `C_t/sigma_*` label is above the upper heavy-pair edge and does not collide with a dashed satellite–clique representative. The caption correctly explains that dashed edges are representative and that every satellite vertex is adjacent to every clique vertex.

One JMB-specific style nit remains: the figure has a label but is not cited in the prose. JMB says every figure should be cited. Minimal edit immediately before the figure:

> `Figure~\ref{fig:hybrid} summarizes the construction.`

The default article-class caption renders “Figure 1:” whereas JMB asks for “Fig. 1” styling without punctuation after the number or at the caption end. This is **not a bioRxiv or scientific blocker** and is best handled by the Springer Nature class/template rather than hard-coded caption text.

### `R_{\mathbb Q}` reduced form — **optional identity, no improvement; reject edit**

It is true that `5069/6439=37/47`. It does not follow that the displayed radical fraction is unreduced: `gcd(12,6439)=1`, and the entire numerator `5069+12 sqrt(147001)` has no common integer factor with `6439`. The current expression is the compact plus root of

`6439 r^2 - 10138 r + 703 = 0`.

Writing `37/47 + 12 sqrt(147001)/6439` is equivalent but visually less compact. Keep the current display.

### Abstract wording — **already fixed; accept**

The abstract now defines `R_sim` as “the supremum of `R` for which one fitness-independent graph family eventually amplifies fixation under both rules for every fixed `r` in `(1,R)`.” This removes the earlier awkward phrase and matches the main theorem's quantifiers. The portal rendering is consistent and its approximately 217 words are within JMB's 150–250-word range.

### MSC `60J10` versus `60J27` — **replacement invalid; keep `60J10`**

The official [AMS MSC2020 list](https://mathscinet.ams.org/mathscinet/msc/msc2020.html?t=60-08) defines:

- `60J10`: Markov chains, i.e. discrete-time Markov processes on discrete state spaces;
- `60J27`: continuous-time Markov processes on discrete state spaces.

The Moran processes whose fixation probabilities the paper defines are finite discrete-time transition chains. Continuous-time clocks/generators are used as proof representations and time changes, not as the primary stochastic model. `60J10` is therefore the correct code. Adding `60J27` would be defensible only as an optional secondary proof-method classification, but it is unnecessary; replacing `60J10` would be wrong.

### CPython 3.14.6 pin — **valid and confirmed; accept**

`bootstrap_replay.sh` rejects every interpreter other than exactly `3.14.6`, both before and after creating the environment. It also requires SymPy `1.14.0` and mpmath `1.3.0`; `requirements.txt` installs the two vendored pure-Python wheels offline with exact SHA-256 hashes. CPython 3.14.6 is a real final release dated 2026-06-10, as confirmed by the official [Python 3.14.6 release page](https://www.python.org/downloads/release/python-3146/). It has since been superseded by 3.14.7, but that does not invalidate a deliberate reproducibility pin.

The manuscript's “once Python 3.14.6 is available” is logically correct but temporally awkward now that it is available. An optional copyedit is:

> The two pure-Python dependencies are supplied as hash-pinned wheels, so the exact certificate replay requires no package-index access **provided Python 3.14.6 is installed**.

This is not a blocker.

### Three Zenodo DOI links — **valid and independently verified; accept**

The official Zenodo API currently returns all three exact records, and the PDF contains active `https://doi.org/...` annotations:

- [`10.5281/zenodo.21753405`](https://doi.org/10.5281/zenodo.21753405): *No universal death–birth amplifier*, v1.0.0 source/software release;
- [`10.5281/zenodo.21850042`](https://doi.org/10.5281/zenodo.21850042): *Simultaneous amplification below fitness three halves*, v1.0.0;
- [`10.5281/zenodo.21852072`](https://doi.org/10.5281/zenodo.21852072): *Simultaneous amplification beyond fitness three halves*, v1.0.0.

The manuscript correctly states that `21852072` contains the unrefereed v1 manuscript/source/software and is **not** the persistent identifier of the superseding v2.0.3 revision. No DOI is stale or misassigned.

## Submission-facing metadata and policy implications

### bioRxiv — **accept, with human screening caveat**

The official [bioRxiv scope page](https://www.biorxiv.org/about-biorxiv) permits mathematical papers when they have direct life-science relevance and lists Evolutionary Biology and New Results as valid selections. This manuscript is directly about evolutionary fixation under Moran updating, so the prepared selection is reasonable. The same page says bioRxiv screens rather than peer reviews submissions. Its official [screening description](https://connect.biorxiv.org/news/2022/06/13/screening_procedures) says text analysis identifies material already appearing online; disclosure of the v1 Zenodo manuscript is therefore important and is correctly prepared.

No bioRxiv-facing text edit is required. The prepared materials appropriately reserve license choice, truthful affiliation/address fields, prior-online-material answers, and final approval to the human author. A bioRxiv posting can precede JMB submission: Springer Nature's official [preprint policy](https://support.springernature.com/en/support/solutions/articles/6000258807-preprints) says preprints are not prior publication.

### Journal of Mathematical Biology — **one metadata blocker plus format pass**

The current official [JMB submission guidelines](https://link.springer.com/journal/285/submission-guidelines) require the title page to contain institution/department as applicable, city, state as applicable, country, an active corresponding email, and ORCID if available. For unaffiliated authors they say city and country of residence are captured. The PDF lacks city and country.

**Required minimal title-page edit before JMB submission:**

> `Independent Researcher, [truthful city], [truthful country]\\`

The human author must supply the bracketed facts. After that edit, rebuild and re-freeze every identity-bearing artifact.

The same JMB guide also asks for full DOI links in the visible reference list, explicit in-text citation of every figure, journal caption styling, and a cited/captioned “Online Resource” if the archive is uploaded as Supplementary Information. Current DOI targets are technically full clickable links, but the visible labels are `doi:...`; replacing each visible label with `https://doi.org/...` would be the strictest style compliance. These are journal-format tasks, not reasons to delay bioRxiv posting or doubts about the mathematics.

## Independent new package-documentation finding

### Dangling relative path in `vendor/README.md` — **valid low-severity nit; fix when re-freezing**

The final sentence points to `submission/ENVIRONMENT.md`. Resolved relative to `vendor/README.md`, that denotes nonexistent `vendor/submission/ENVIRONMENT.md`. The intended existing file is one level up.

Exact minimal edit:

```diff
- described in `submission/ENVIRONMENT.md`.
+ described in `../submission/ENVIRONMENT.md`.
```

This does not affect replay, hashes internal to already frozen files, or scientific correctness. It is a reader-navigation defect only. It is harmless for bioRxiv, but should be corrected in any v2.0.4/JMB package.

## Final accept/reject summary

| Item | Disposition | Submission effect |
|---|---|---|
| Figure chords/label collision | **Already fixed — accept** | None |
| Abstract definition | **Already fixed — accept** | None |
| `R_Q` split rational part | **Optional — reject edit** | None |
| Replace/add MSC `60J27` | **Invalid as replacement — keep `60J10`** | None |
| Finite-size estimates sentence | **Invalid as a proved claim — reject** | None |
| Floor warning | **Already fixed — accept** | None |
| Round-to-nearest family | **Optional — reject** | Would force unnecessary re-freeze |
| Mechanism sentence | **Already fixed — accept** | None |
| `O(K/C)`, coordinate uniformity, gate explanation | **Already fixed — accept** | None |
| Empirical exponential wording | **Optional — reject** | None |
| Polynomial weak-cut/`e_t` inference | **Invalid — reject** | None |
| Python 3.14.6 pin | **Confirmed — accept** | None |
| Three Zenodo DOI links | **Verified — accept** | None |
| bioRxiv content/metadata | **Accept** | Human portal/screening only |
| JMB city/country title-page field | **Valid required fix** | **JMB-only blocker** |
| Figure in-text citation/JMB caption and visible DOI style | **Valid low-priority format pass** | Nonblocking for bioRxiv |
| `vendor/README.md` relative path | **Valid low-severity nit** | Nonblocking |

**Bottom line:** v2.0.3 is ready for bioRxiv submission after human portal review. It is scientifically ready for JMB, but a strict JMB submission should first add truthful city/country and perform the small journal-format/package-documentation pass above.
