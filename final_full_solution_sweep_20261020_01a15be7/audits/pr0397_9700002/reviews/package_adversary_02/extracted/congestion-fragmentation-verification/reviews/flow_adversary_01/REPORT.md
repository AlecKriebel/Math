# PR397 independent flow-family adversarial review

Reviewed frozen head `3705c5102b58c48e29991c61771978bf756a62e7`, problem9700002/AMR-096-0002. All24 original files independently match the snapshot byte counts, SHA256 and Git blob hashes; they remain unchanged. No other fresh reviewer's report was consulted. No external communication, branch/index write, PR mutation, publication or spreadsheet write occurred.

**Mathematical verdict: PASS for the specified turn-2 model.** The deterministic design, full physical-to-transport reduction, exact finite value and right-marginal formulas, and every-optimizer outer-phase claims are valid. I found no mathematical counterexample or unresolved proof gap in this family. This is not a full-package publication clearance: the historical replay wrapper has a concrete cross-version portability defect requiring a disclosed new derivative or an actually reproduced pinned environment before making a portable publication-replay claim.

## Deliberate falsification

I reconstructed the argument without using its LP code. `INDEPENDENT_DERIVATION.md` gives the decisive deductions, including endpoint strictness and the assumptions needed for every-optimizer language. `independent_flow_controls.py` uses exact rational Dinic flows with matching residual-cut dual witnesses and an independent binary-word representation of physical tree paths.

- 534 exact rational flow instances, 687 primal/dual certificates, 153 actual lower-envelope kinks and 3972 physical-edge identities pass.
- The smallest-active-slope right derivative is tested at true ties. Replacing it by the largest slope fails the synchronized critical controls.
- Actual offered-slope normalization is indispensable to an exact finite subcritical marginal of one. A concrete rate array with S=10/7 and baseline k²=4 distinguishes the two denominators.
- A new k=4 mixed-cut witness has every offered terminal total above capacity but maximum throughput156/5<32. Thus checking only terminal totals would be false. The candidate genuinely proves an all-cut bound and avoids that error.
- Two exact optimal k=2 matrices at an intermediate positive-rate instance have respectively four and five spare edges. Universal critical-time optimizer invariance would be false. The candidate correctly confines full/edgeless conclusions to its proved outer phases.
- Positive capacity prices and simple physical paths are necessary declared hypotheses. I found no hidden extension to zero-price designs, arbitrary circulations or generic cyclic networks.

The finite controls support a separate general proof; they do not establish an asymptotic theorem by enumeration.

## Strongest verified claim and scope

On the declared sparse binary-tree family with dense cross-root OD traffic, positive linear capacity prices force C_e=2kk_e. For every finite positive rate array, throughput is the exact minimum of its stated affine transportation cuts and its normalized right derivative uses the minimum active cut slope divided by S. Strict offered terminal slack forces the unique full-demand admitted matrix and a full spare tree; total throughput2k² forces every terminal and internal edge to saturate for every optimizing admitted matrix. The candidate's exponential all-cut event correctly invokes these deterministic conclusions simultaneously over the two outer time intervals.

The complete [primary Aldous page](https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html) was read and privately archived with hash341bf2e5f1e024c9e654a450cc0849518d1c3ad52fcfd086702a7e4fd28baed8. It asks for a tractable conceptual example rather than a uniquely quantified conjecture. The construction implements the admitted-demand objective and fixed-topology doubled-demand design, while openly choosing affine random slopes and a specialized demand pattern. Correctness does not certify that it is the uniquely appropriate model, a universal network theorem, or a historically new construction. Those are separate scope/priority decisions. Standard ingredients alone do not establish prior exact application.

For a publication, retain dense OD scaling, capacities growing with graph size, quadratic time variance, actual-slope normalization, simple-path interpretation, the outer-phase-only optimizer quantifier and the absence of a claimed critical profile. State quenched formulas for positive finite rates, or almost surely under the exponential law; a fictitious all-zero rate vector would make S-normalization undefined and is outside the stated S>0 domain.

## Reproduction and required package repair

The existing system `.venv` is Python3.9.6/NumPy2.0.2/SciPy1.13.1. Its clean public wrapper returns1 at the turn-1 strict CHECKS.json byte comparison. Original files are unchanged. Component isolation establishes:

1. Turn1 exits0 and passes all its original assertions. Exactly37 floating JSON leaves differ, maximum absolute drift4.440892098500626e-16. Exact paths and values are retained in `REPLAY_COMPONENT_DIFFS.json` and `PORTABILITY_ASSESSMENT.json`.
2. Turn2 exits0, passes all assertions and reproduces CHECKS.json byte-for-byte.
3. The portable independent program, executed on a fresh frozen layout, exits0 and passes all eight assertion groups. Comparing with the historical receipt leaves three gamma-union floating diagnostics with maximum absolute drift2.2737367544323206e-13 (on value1841, about1.2e-16 relative), version fields, and the already declared projected8-versus25 input binding. This is not equality of every historical mathematical JSON record on an unpinned platform.

The first component probe ran the portable checker after author replays had changed the copied historical turn1 output; its input-hash assertion therefore failed as designed. That probe is preserved and explicitly superseded for portable correctness by the fresh-frozen-layout run. No original or candidate assertion was weakened and no passing flow/turn2 test was repeated to manufacture acceptance.

If scientific and priority gates clear, preserve all original24 files and add a clearly identified new publication replay derivative. It should verify frozen hashes, run unchanged original mathematical assertions in clean copies, compare exact/discrete fields exactly, and disclose tightly bounded tolerance only for identified floating diagnostics, or use a truly reproduced pinned environment. Explain this qualification consistently in the paper, README and metadata. The current unversioned byte-match wrapper should not be advertised as portable proof of byte-identical historical outputs.

## Remaining gap

No deterministic mathematical gap remains. The publication replay/documentation repair above remains mandatory before publication readiness. Originality and full source-model eligibility are outside this family's final verdict and require their separately assigned reviews. No claim is rejected merely because it uses classical transport or concentration.
