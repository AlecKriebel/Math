# Paper II hostile-audit ledger

Date: 2026-08-21 (America/Los_Angeles)

This ledger distinguishes proof obligations from exact computational checks.
It contains no claim that a numerical solve proves an asymptotic statement.

| Obligation | Required hostile check | Evidence boundary |
|---|---|---|
| fitness-independent family | every graph parameter, including the dyadic weak cut, is selected before fitness is quantified | analytic theorem proof |
| graph class | every finite graph is connected, loopless, undirected, and positively weighted on its stated edges | construction inspection |
| finite strong lumping | both update kernels commute with the stated orbit action | proof plus 512-state/108-fibre labelled audit |
| weak-cut trace | fast mixed states are transient and the Schur complement gives introduction rate times local fixation | analytic finite-state proof |
| gain-scale uniformity | cut error and center errors are `o(q/C)`, not merely `o(1)` | analytic compact-uniform estimates |
| center establishment | stopped drift comparisons cover the route from one core mutant to a density strip | analytic proof |
| center cleanup | the density strip reaches full fixation, including pendant cleanup, with failure negligible at gain scale | analytic proof |
| reciprocal invasion | reverse-fitness portal values are `o(C^{-1})` uniformly on each fitness compact, which is the scale needed by the sweep | analytic proof |
| pair gate | all four introduction rates have the stated orientation and yield `Z_B` and `Z_D` | rate derivation plus exact coefficient audit |
| global sweep | the two-coordinate macro chain retains adverse reversals and controls all `q` satellites | analytic proof |
| response functions | center, pair, pendant, and baseline terms occur on one common scale with correct signs | exact algebra plus analytic estimates |
| sextic threshold | root count, quadratic minimizer, tangency, and derivative signs are exact | two symbolic certificates |
| rational-edge family | endpoint margins and algebraic threshold are exact | symbolic certificate |
| claim boundary | optimality is limited to fixed positive parameters in the displayed first-order response model; no unrestricted upper bound is inferred | abstract, theorem, discussion, and package integration audit |
| computational boundary | replay coverage is not described as a computer proof of the weak-cut or population asymptotics | Data and Code Availability and package notes |

The finite affine-separator calculation from the v1 package is intentionally
absent.  It is not load bearing: the main theorem includes fitness `3/2`, so
a sufficiently large graph already has both normalized fixation ratios above
one there.  The sparse numerical core diagnostic is likewise absent from the
public replay and release archive.

## Final verdict

Three independent final reviewers re-read the corrected theorem chain and
the frozen manuscript after the literature update, major-revision response,
and targeted specialist rereview.  In particular, they re-audited the adapted
hidden-coordinate drift, explicit stopped cleanup recursion, adverse pendant
reset, killed-Green tail, finite-horizon immigration maximum, and rule-specific
reciprocal renewal at the claimed gain scales.  No substantive
theorem, rate, scale, quantifier, citation, rendering, replay, or package
objection remained.  The deterministic archive was independently regenerated and
clean-extracted; its internal manifest, pinned replay, and byte-identical PDF
rebuild all passed.  Human confirmation of contact, funding,
competing-interest, contribution, license, and portal fields remains an
explicit pre-submission gate rather than a research-package claim.

## 2026-08-22 final notation-freeze audit

An independent final pass rechecked the only mathematical change after the
preceding verdict.  With $m=O(C^{1/4})$ and
$T=\beta_0(B_0)\log C$, the displayed conditions
$\beta_0-1/4\geq B_0+2$ and $\kappa\beta_0\geq B_0+2$ give, respectively,
$m e^{-T}=O(C^{-B_0-2})$ and
$R_0e^{-\kappa T}=O(C^{-B_0-2})$.  The hub-deactivation integral remains
$o(1)$ because its bound is independent of $T$.  No related exponent,
compact-uniformity, or quantifier defect was found.

The complete exact replay, fresh archive extraction, pinned bootstrap,
byte-identical PDF rebuild, compiler-log scan, embedded-font check, and visual
inspection of the changed pages all pass.  The compact 20-page bibliography
remains readable.  At that checkpoint no blocker or minor mathematical issue
had been identified; the later independent referee audit recorded below
supersedes that verdict.  The annotated, unsigned v2.0.1 tag was placed on the
exact scientific commit before its frozen source link was relied upon.

A subsequent package-integrity adversary found one reproducibility-only gap:
the clean bootstrap created `.venv-paper2`, while the standalone release
script's replay default preferred only `.venv`.  The replay selector now
prefers the pinned clean environment, and a fresh extraction has reproduced
both the 19-member archive and 20-page PDF byte-for-byte through a plain
`release_bundle.sh` call.  The source epoch now matches 22 August 2026 UTC.
No mathematical or certificate claim changed.

The final wrapper received three independent adversarial passes.  The prompt
audit required and then confirmed an honest incomplete-review verdict,
non-exhaustive counterexample search, and full wrapper/dependency inspection.
The package audit confirmed safe canonical members, internal byte consistency,
an independent remote tag/blob/mode comparison, deterministic archive and PDF
regeneration, bounded temporary cleanup, and failure propagation under five
negative tests.  The annotated tag was unsigned, so the comparison did not
constitute independent signer authentication.  A fresh blind referee
independently re-derived the gate rates, response functions, tangency data,
and corrected cleanup exponents and reported no theorem, software, or package
defect at that checkpoint.  A later referee found the missing synchronization
stop and optimized-Python false pass described in the superseding audit below.

## 2026-08-22 superseding post-referee audit

The referee's mathematical counterexample was reproduced.  The former
unstopped next-pendant and `ell=m` expectations could be infinite after
positive-probability extinction.  The revised proof stops at upper-strip exit,
gives that exit favorable boundary value in the pendant committor, derives an
explicit positive-drift stopped trace with `O(m)` expected outcomes, and then
derives `O(C)` expected calendar time per outcome.  A separate hostile pass
also found and repaired the adjacent `ell=0` boundary of the resident-hub loss
bound.  The resulting synchronization-or-exit estimate is precisely the one
used by the later block recursion.

A fresh full-manuscript adversary then rechecked every theorem dependency from
the model and weak-cut trace through reciprocal invasion, gate sweep, response
optimization, rational specialization, and the final diagonal quantifiers.  It
found no remaining blocking or minor mathematical issue and no unsupported
downstream use of the repaired estimate.

The optimized-Python false pass was also reproduced.  Every critical condition
now raises explicitly, all verifier entry points reject optimized execution,
and disposable early and late mutations prove that failures suppress the
whole-replay success sentinel.  The Python dependency wheels are included and
hash-pinned for offline replay; one verified interpreter is used throughout
release construction; archive modes and internal manifest syntax, paths, and
uniqueness are checked.  Negative tests covered optimized entry points,
mutated identities, a corrupted wheel, wrong source modes, a corrupted archive
payload, and a duplicate manifest entry.

Two deterministic archive generations, a fresh offline bootstrap, archive and
PDF regeneration, compiler-log and embedded-font checks, and visual inspection
of all 21 pages pass.  Tectonic/Poppler and Tectonic resources remain externally
provisioned; the Git tag is annotated but unsigned; the literature search is
not exhaustive; and the stochastic asymptotics are analytic rather than
machine-formal.  These are stated limitations, not evidence supplied for the
theorem.

**Post-repair verdict:** no theorem, rate, scale, quantifier, verifier,
reproducibility, or rendering issue remains in the scientific source.  The
corrected source was frozen without moving v2.0.1 at commit
`03e94e877ce10d9d459fd284bd652934cde08bb3` and annotated, unsigned tag
`simultaneous-amplification-beyond-three-halves-v2.0.2`.

The regenerated neutral wrapper then passed its own exact 34-payload
manifest, all 23 source-archive members, a full clean offline Python replay,
byte-identical source-archive and PDF regeneration, and comparison of all 21
repository-backed archive blobs and modes with the frozen tag.  Optimized
execution and independent top-level and extracted-source mode mutations were
rejected.  Its deterministic 35-file outer archive has SHA-256
`2216c6a31545b38d9ca89c9d43c5a309bfcc6c2c1f7ab63ea5fabc171116e1d2`.
The tag remains unsigned and the optional Git comparison is consistency
evidence, not signer or authorship authentication.

## 2026-08-22 v2.0.3 submission-polish audit

A second-model review was checked claim by claim rather than adopted as a
block.  The final revision accepts only the supported changes: Figure 1 is now
a complete five-vertex clique with collision-free representative weak edges;
the abstract states the supremum quantifiers directly; the early-establishment
error is sharpened consistently to `O(K/C)`; the reversal union bound states
the needed implication direction; and the discussion records only the
response-model `sigma -> 0` mechanism and qualitative `O(1/t)` floor
oscillations.

The proposed numerical finite-size thresholds were rejected because they
concern the separated trace rather than the connected diagonal family and do
not establish an all-later-index threshold.  No exponential reciprocal bound
or polynomial weak-edge exponent was added because neither follows from the
proof or certificates.  The optional algebraic-number rewrite and additional
continuous-time MSC code were omitted as unnecessary presentation changes;
the model and exact absorbing chains remain correctly classified by 60J10,
while continuous-time clocks are an auxiliary proof representation.  The
claimed hidden-coordinate uniformity was already explicit.  Python 3.14.6,
the cited references, and all three related Zenodo records were independently
checked.

Independent proof and figure adversaries then re-read the complete v2.0.3
diff and all 21 rendered pages.  They found no mathematical, quantifier,
caption, edge, overlap, clipping, or layout defect.  A separate editorial and
package adversary found one status-note inconsistency: three human-completed
portal checks conflicted with an old sentence saying that no portal had been
opened.  The completed boxes were preserved and the status note was corrected;
re-review was clean.

The exact replay, submission verifier, package verifier, Git-binding check,
optimized-mode rejection, clean offline bootstrap, and fresh outer-archive
replay all pass.  Two source-archive builds and two outer-wrapper builds are
byte-identical.  The scientific source is frozen at commit
`bd66a3bbf1c530ef67a4b7be5ee69a6825678457`, annotated unsigned tag
`simultaneous-amplification-beyond-three-halves-v2.0.3`; the PDF, source
archive, and outer referee archive have SHA-256 values
`1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`,
`e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`,
and `f4baf76a66a12e4942f13bd7c73bbead0ff31555df5b69a489b914064c597bdf`,
respectively.

**v2.0.3 verdict:** no actionable mathematical, software, metadata, package,
or rendering issue remains.  External submission and its remaining consent,
license, address, terms, proofing, and approval gates remain human actions.
