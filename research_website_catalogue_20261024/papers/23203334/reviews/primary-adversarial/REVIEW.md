# Focused independent adversarial audit: upstream analytic core for Zenodo 23203334

Disposition: **PASS for the focused import-chain audit; no substantive defect found.** This is an AI proof review of the precise pinned text below. It is not human peer review, a novelty certificate, a publication authorization, or a separate blanket certification of the multispecies theorem. The finite controls corroborate the hand-checked estimates; they do not establish a global PDE theorem by computation.

## Source binding and independence

The reader paper is Alec Kriebel, *Signed impulse estimates and global smooth solutions for finite multispecies relativistic Vlasov–Maxwell*, October 6, 2026, 10 published pages:

- `sources/paper.pdf`, SHA256 `8cfaa828abfe5f91626527a79679c503bb37cb081fb258de68ef7f776a74e046`.
- `sources/source-and-verification.zip`, SHA256 `6b90c4116ba596ee56567be0d540c1866e5f4fdf18bd62f13c489c6ca996849e`.
- Extracted `source-and-verification/main.tex`, SHA256 `9d72d239677c1066ba22ffbea8ff36f26251a2eae532921bd5e8e12b5f9fdb8c`.

Its load-bearing input is OpenAI, *Global classical solutions of the three-dimensional relativistic Vlasov–Maxwell system*, printed September 23, 2026, 49 pages, at repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

- Supplied pinned PDF `../scope/primary-sources/openai362.pdf`, SHA256 `56691a44941097fa1a5131470d44c5bc23930faeda22836e177d2391252817d8`.
- All ten raw section files were copied into this audit's `raw-source/` only after checking their exact hashes against the raw-source acquisition receipt. Their full bodies were read, including the setup and continuation sections in addition to the requested Sections 4–8. The full PDF text was extracted, its page/section map checked, and critical statements crosschecked against the PDF text. This was not a PDF typography audit or a fresh TeX compilation.
- The independent external import check used [Luk–Strain, arXiv:1406.0165v1](https://arxiv.org/pdf/1406.0165v1), saved locally with SHA256 `a3bbd52e5e9a15ca7219fe52b15cfc8a088644d0c8abe182f52870d49ea1e223`.

No sibling mathematical verdict, historical audit, priority assessment, or archived reviewer judgment was read. Only raw pinned sections and a source-acquisition receipt in the analytic review directory were used. Incidental directory listings disclosed filenames, not their contents. The disposition here was formed independently. No original source, website, spreadsheet, Git state, Zenodo record, or outside communication was changed.

## Exact question and success criterion

The reader paper imports substantially more than the final one-species theorem. Its coupled argument requires the upstream conditional **signed momentum increment estimate**, together with its preliminary occupation bounds, absolute-force estimate, signed source-trajectory identity, direction count, improved occupation window, and selected receiver coefficient. The source acceleration must disappear before taking absolute values. The final bound must have constants independent of the bootstrap parameters before those parameters are fixed.

The upstream target on each compact classical prefix is

\[
 |V_X(t_2)-V_X(t_1)|\le MP\sqrt I+A I P^2\log(2+P)/w,
 \qquad I=t_2-t_1,
\]

for every supported receiver, each dyadic momentum scale with `w/8 <= q_X <= 8w` throughout the interval, and every dyadic `P` exceeding 1024 times the maximum supported momentum energy on the prefix. The final `M,A,P0` depend on the datum and fixed time horizon, not the chosen prefix or `P`. Preliminary nonnegative estimates allow any measurable eligible subset of an interval of length at most `I`; the final signed estimate requires eligibility throughout an interval of length exactly `I`.

I tested this chain by tracking the small angular deficits, time-change factors, dependence on `M,A`, interval quantifiers, and places where an estimate could be used before its proof. Success means no central unsupported implication or counterexample was found in this specified chain, with the external continuation theorem used only in its actual stated scope.

## Verified nodes and attempted failure modes

### 1. Retarded representation and the three measures

Upstream Section 3, PDF pp. 7–13; `retarded.tex`, especially lines 103–148, 155–293, 318–428.

I reconstructed the distinction among these transformations:

\[
 dz=d\,dy\,dv,\quad dy=r^2D\,dt\,dn\ \text{at fixed }s,
 \quad dt/ds=d/D\ \text{at fixed source label},
\]

where `d=1-n·u`, `D=1-n·a`. Thus the combined identity is `ds f0 dz = D dt f dy dv`. Confusing either `d` and `D` would invalidate the later force and occupation exponents; the actual source uses them consistently.

The retarded roots are unique because both curves are timelike. At fixed receiver spacetime point the phase Jacobian follows from the rank-one determinant correction to the volume-preserving characteristic flow. At fixed source time the spatial Jacobian is the normal component of `a-n`, namely `D`. The same-time collision labels are null with respect to the absolutely continuous initial particle measure: the time-grid argument has `O(1/ζ)` samples and `O(ζ^3)` spatial mass per sample on a compact prefix. This avoids assuming a uniform positive source–receiver distance for all labels.

I checked the source-force decomposition giving the `G+θ²|B|` acceleration bound and its extra `θ` in the normal component. The transport kernel is retained in the signed identity. Cone-tip cutoffs use bounded quantities on a fixed compact prefix only to justify the identity; those prefix bounds are not subsequently inserted as constants in the uniform momentum estimate. Initial-cone terms use the fixed compact initial momentum support, not current high-momentum bounds.

### 2. Preliminary occupation and the joint energy budget

Section 4, PDF pp. 13–18; `occupation.tex`, lines 135–294 and 296–416.

The first-exit argument genuinely uses the assumed **signed increments** to obtain local velocity stability. It does not assume an absolute acceleration bound. The length

\[
 \lambda^{-1/2}=C_1(P/m)\left(M/\omega+\sqrt{AL/\omega}\right)
\]

makes both bootstrap terms small relative to `m ω`. The `actual` condition ensures that the inverse-momentum deficits cannot account for all the relative-velocity separation. Deficit bins with `h <= min(I,λ)` are explicitly excluded and handled later; the claimed stable-cell crossing estimate is not silently applied there.

On an actual stable cell, projecting `Y(s)-X(s)` onto a fixed relative-velocity direction bounds the total hit duration even for a disconnected hit set. All hit labels have energy comparable to `p` at one common cell time, so their mass is bounded by `C/p`; this avoids summing an energy bound separately for each label. For `h>λ`, the crude spatial-energy bound suffices.

The refined small-sector budget is a significant load-bearing detail. `E_{pφ}` is independent of `h,θ` and of the eligible receiver subset, and its total over `p,φ` is bounded independently of `M,A`. One indicator averages stable-cell mass; a different indicator records the unique retarded receiver angle. The latter deliberately does not require the retarded time to remain in the original interval. The fixed enlargement `J*` has length `O(I)`: averaging is used only when `λ<=I`; when `λ>I`, the proof uses a bounded number of cells without averaging outside `J*`. I found no hidden enlargement proportional to an uncontrolled bootstrap parameter.

### 3. Absolute/direct estimates

Section 5, PDF pp. 18–24; `direct.tex`, lines 35–428.

I rederived the near/far table from `N<=Cp³ν²`, the occupied measure, the cone `G²` budget and the spatial magnetic budget. In particular the magnetic change of variables needs `r²φ²`, whereas the good-field budget has the cone factor `r²`. The radial balances give the displayed `I^(3/4)` and `R^(1/2)` powers.

The small-sector transport sum uses the **joint** `E_{pφ}` budget, yielding `L+sqrt(L)P/w` rather than an unaccounted extra logarithm. The remaining-sector split between `θ≫φ` and `θ≈φ`, including the possible small `σ`, gives the claimed convergent angular factors. The magnetic terms with `h>I` instead use the label time-change estimate. The exceptional deficit sums are bounded by `IS(w)` with a vanishing `O(L³/P)` ratio. The unselected baseline is

\[
 \mathcal B=P\sqrt I+(M+\sqrt A)IS(w),
\]

while the full absolute force retains `sqrt(w) B`. I did not replace this weaker absolute estimate with the desired signed estimate anywhere in the dependency chain.

### 4. Signed cancellation, cutoff derivatives and endpoints

Section 6, PDF pp. 24–29; `cancellation.tex`, lines 21–112, 138–273, 278–382.

The source-time primitive is `k0/(r d)`, where `k0=u-(e/D)n`. Differentiation yields the geometric residual and receiver-acceleration residual claimed by the source. The latter has no inverse source deficit, but its gain depends on the stronger identity `a_t=(Id-a⊗a)K/q_X`: `a_t·k0` is bounded by `C θ |K|/w`, not the weaker product of the separate norms. This supplies the displayed `φ^-2`, not an extra `φ^-1` loss.

The selected set is a fixed set of representative indices throughout each interval. Hence differentiating the smooth selected sum does not differentiate an evolving inequality. The identity `∂χ=-∑unselected ∂β` is used only after factoring out the common physical multiplier. Neighboring indices differ by bounded factors and remain in the enlarged small-sector range; the later nonnegative `σ` partition is not differentiated. Receiver derivatives are retained on selected supports, with their acceleration coefficient explicitly estimated. Time-weight and varying-projection derivatives are also retained.

I independently differentiated the primitive using exact rational dual numbers in 100 timelike configurations, including very small deficits and radii. Every equality held exactly. Dropping either the transport term or receiver term broke all 100 cases. These are sensitive algebraic controls, not a replacement for the general product-rule derivation or the integration argument.

The initial boundary estimate depends on initial momentum and the fixed horizon. The endpoint-zero weights remove the other time endpoints. The selected receiver coefficient is obtained in two independent ways—density and cone particle flux—and is the minimum used in the later selection lemma.

### 5. Direction count before improved occupation

Section 7, PDF pp. 29–34; `direction.tex`, lines 22–220 and 222–377.

I specifically looked for circularity here. The direction proof uses the fixed rough selection `p θ sqrt(h)<=1` and the **unrefined** stable-cell occupation factor, plus the already proved absolute estimate. It does not invoke the improved occupation lemma or the final selection coefficient.

The short endpoint ramps are controlled by integrating endpoint-relative direction increments against the ramp derivative. This is valid from the signed bootstrap and does not assert a bound on total direction variation. Complete exit intervals have a uniform positive lower length on the compact prefix. Their nonnegative bulk weights have disjoint supports; therefore their bulk cost is estimated over the original interval once. Only the time-weight error pays per complete exit. Its `O(L²)` coefficient is absorbed by `w δ`, which has a positive power margin under the lemma's ranges. Consequently the claimed `C(M,A)L^6/δ` count is obtained without feeding the enhanced occupation bound back into its own proof.

For enhanced occupation, I checked the distinction between source time `s` and retarded receiver time `t`. Bad hits crossing a receiver direction boundary have source-time duration `O(h)` per boundary, independent of `dt/ds`; no bounded retarded derivative is assumed. On good hits, direction stability makes the simultaneous separation `|Y(s)-X(s)|<=Chφ`. The common refinement of source and receiver direction partitions costs their **sum**, not their product. Monotone relative motion then limits hit duration to `O(h)` per refined interval.

The intermediate window `p,w>=P^.7`, `j^-.49<=φ<=j^-.16` guarantees both direction-count hypotheses after fixed-factor changes of dyad and enough angular margin over the velocity deficits. The final absorption is legitimate only after fixing `M,A`:

\[
 C(M,A)L^7\le C\phi^{-(\beta-1)},\quad
 \beta=29/25,\quad \phi^{-(\beta-1)}\ge P^{56/3125}.
\]

This changes the lower threshold for `P`, not the final estimate's multiplicative constant.

### 6. Exact selection and its exponent margins

Section 8.1–8.2, PDF pp. 34–37; `selection.tex`, lines 39–275.

The pure occupation entries contain no implicit constants. The actual occupation is only bounded by a fixed constant times their minimum. This distinction permits the strict representative selection inequalities to be used exactly; otherwise the small exponent margins would need a new argument.

I independently reconstructed the contradiction for an unsafe selected bin. In the source's exponent variables, the energy entry and near selection first imply

\[
 \Delta/z<4/99995<.001.
\]

The branch `H<=2c` is incompatible with the first unsafe inequality. In the other branch, `H>.496z+3(α+c)`. This forces actual velocity separation before any bootstrap-dependent constant is absorbed into a power of `P`. The actual entry subsequently gives high momenta and places `φ` strictly inside the improved window for both source and receiver. The thresholds are uniform over indices because `z` is first bounded away from zero.

There is a transparent strict margin after the improved entry becomes available. Near selection, the first unsafe inequality and improved far selection imply, even after dropping favorable nonnegative terms,

\[
 H/z<37487/93500\simeq .4009305,
\]

whereas the preceding lower bound gives `H/z>62/125=.496`. The rational gap is `8889/93500`. The exact control script checks this combination and the positive radial/time-weight exponents.

As a negative control, take normalized exponents

\[
 (α,c,z,H,y,b)=(0,0,1,3/5,3/10,29/50).
\]

They satisfy near selection, energy far selection, the relaxed actual far inequality, both unsafe inequalities, and the improved window; they fail the improved far selection. Thus the improved occupation input is genuinely needed. The control would not falsely certify the coefficient from the elementary bounds alone. This supports, but does not itself prove, the analytically established improved occupation estimate.

### 7. Transition errors and weighted impulse

Section 8.3–8.5, PDF pp. 37–40; `selection.tex`, lines 277–488.

The spatial cutoff transition cannot simply be charged to a baseline pointwise force term. I checked the actual radial-crossing argument. Its balancing quantity `D0=sqrt(I) R p φ` is independent of `θ`. The parameter `n0/D0` changes geometrically with `θ`, with positive exponent `(1-4ε)/(1-2ε)`. Both resulting geometric tails are summable. This removes the extra logarithm that would arise from bounding each `θ` bin separately. Structural neighbors and deficit radii are handled separately.

For time-weight terms with `h>I`, both near and far selection are needed. They bound the increasing source-angle factor; the residual powers of `h` and `φ` are strictly positive. For `h<=I` the central residual estimate applies directly. Finally the selected receiver coefficient sums to `Cw^-1/2`, which cancels the factor `sqrt(w)` in the previously established absolute-force bound. No desired signed estimate is substituted at this point. The resulting weighted impulse has constant `C_eta` independent of `M,A`.

### 8. Bootstrap closure and continuation

Sections 9–10, PDF pp. 40–47; `closure.tex`, all lines; `continuation.tex`, all lines. The first-hit consequence is in `setup.tex`, lines 71–116.

The edge restoration is an integration by parts against endpoint-relative momentum. It only costs `MP sqrt(eta I)+A eta I S(w)` per edge, so it does not lose the absolute `sqrt(w)` factor. The order of choices is legitimate: fixed ramp fraction, then `M`, then `A`, and only then the large-`P` threshold. The trivial large-increment-bound case and small-time case are both included. A compact-prefix bound on `|K|` is used solely for initial/short-interval bootstrap validity and openness for fixed `P`; it does not enter the uniform final constants.

The first-hit doubling argument selects a possibly different maximizing label for each hit level and uses that label's last crossing of the preceding level. Thus its interval lies after the previous global first hit. Each global doubling consumes at least `c/log(P)` time, and the lower bounds have divergent sum. The argument does not require one label to maximize momentum at all times.

For the non-Sobolev field class, I checked the finite-horizon modification: retain the initial Coulomb field, cut off vector potentials of the divergence-free remainders, and add back a vacuum field which vanishes on the full particle region for that horizon. The Coulomb field is in every `H^k` even with nonzero charge in three dimensions; its low-frequency singularity is only `|ξ|^-1`. Classical uniqueness, exterior comparison and the tame estimate explain why smoothness persists through a closed classical slab. No spatially compact electric field with nonzero charge is assumed.

The original Luk–Strain v1 source confirms the exact imported criterion on PDF p. 2: nonnegative compact phase `H^5` particle data, constrained `H^5` fields, a classical solution and a bounded continuous momentum-support bound suffice for unique `C^1` extension. Footnote 1 explicitly removes the need to bound approximants in this higher-regularity formulation. Its normalization uses `4π` in both charge and current, correctly matched by `f_LS=f/(4π)`. I inspected pp. 1–3 for this import, not its complete proof. The full criterion remains an external established theorem input.

## What this review does and does not establish

The checked chain supplies the upstream conditional weighted signed-impulse estimate and its parameter-uniform closure as written at the pinned commit. I found no hidden use of improved occupation in its own direction-count proof, no unsupported removal of the angular deficit, no missing selected cutoff/time-weight term, and no continuation-model mismatch. There is no concrete defect to defer or repair from this focused audit.

The remaining boundaries are explicit:

1. This task does not independently certify the reader paper's entire finite-species transfer, every species coefficient, or its complete literature/priority claims. Its source was read to identify the exact dependency. Those are separate review obligations.
2. The original Glassey–Strauss continuation result is accepted through the checked Luk–Strain theorem statement and footnote; its full historical proof was not rederived. Standard characteristic ODE, Fourier/Maxwell, Sobolev and Green-function facts were checked for applicability, not re-proved from foundational analysis.
3. The estimate checks are analytic reasoning plus limited exact controls, not formal proof-assistant verification, PDE simulation, or evidence of journal acceptance. No unrestricted global-PDE pass is inferred from an author name, repository posting, or old audit.
4. No effective numerical value for the enormous large-`P` threshold is provided or required by this qualitative argument. The result does not assert uniformity in the time horizon, the initial data, or any massless/infinite-species limit.
5. Introductory historical assertions and the current state of the surrounding literature were not audited for novelty. This review reports only the specified proof dependency.

## Reproducible evidence

Run `python3 independent_controls.py` from this directory or pass its absolute path. It needs only the Python standard library and writes `independent-controls.json`. The saved result has 100 exact identity successes, 200 detected omission failures, the exact selection contradiction margin, the baseline-only unsafe witness, and positive summability/absorption exponents. `source-bindings.json`, the two primary receipts, `evidence-manifest.json`, and `verdict.json` bind the source and review artifacts. `RESEARCH_LOG.md` records timestamped checkpoints and completion estimates.
