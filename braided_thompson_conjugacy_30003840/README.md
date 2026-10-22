# Conjugacy in braided Thompson groups

**Problem 30003840 / OWR-16167-010. Status: unresolved after five substantive attempts.**

The question asks for a conjugacy decision algorithm in **F_br and T_br**. The existing result for V_br does not answer it. This packet supplies proved partial reductions and checkable obstruction examples; it does not claim a solution, an undecidability theorem, or historical novelty.

## Main results of the attempts

1. [Ambient conjugator restriction](ATTEMPT_1.md): an exact centralizer-image coset criterion, and ambient-conjugate elements that are not F_br-conjugate.
2. [Linking-pattern orbits](ATTEMPT_2.md): a finite algorithm for the F/T orbits of kernel linking data; ambient-conjugate elements that are not T_br-conjugate; and a zero-linking nontrivial commutator proving the invariant incomplete.
3. [Cabling search](ATTEMPT_3.md): a necessary-and-sufficient finite-refinement witness criterion for kernel inputs, decidable fixed-strand stages, and the exact missing termination bound.
4. [Split-extension approach](ATTEMPT_4.md): the full twisted-kernel equation for F_br, linear necessary conditions, and why the analogous T_br splitting cannot be assumed.
5. [Powers and invariant partitions](ATTEMPT_5.md): a finite-order quotient reduction for T_br and an equal-cubes witness showing that powers lose conjugacy information.

The substantive gaps are a terminating global refinement procedure and a solution to the relevant nonabelian twisted/centralizer orbit problems. The mathematical source's Question 48 remains unresolved by this work.

## Reproduce the elementary checks

Use Python 3 with the standard library only:

```sh
python verify.py
```

Expected output is [verify_results.json](verify_results.json). Checks cover exact linking matrices, the braid relation and a nonidentity SL_2(Z) commutator image, 2,240 deterministic cloning/rotation tests, the equal-cubes quotient witness, and 24 finite transporter-coset checks. They do not implement a full braid-centralizer solver or decide the target problem. The full proofs are in the attempt files; passing finite tests is not substituted for those proofs.

See [SOURCE_GATE.md](SOURCE_GATE.md) for precise problem identity, primary sources, current-literature scope and access limitations. The exact UnsolvedMath page was blocked; the pinned corpus and original OWR report independently establish the statement. No downloaded papers or corpus copies are included.

## Independent audit and correction record

The [full independent audit](audit/AUDIT.md) accepts the five attempts as partial results and retains the unresolved disposition. Its [independent controls](audit/independent_controls.py) and [recorded output](audit/independent_controls_results.json) are included. Run them with Python's standard library:

```sh
python -B audit/independent_controls.py
```

The audit examined the immutable first packet. This release preserves all five attempt files and both checker implementations byte for byte. [CHANGE_MAP.md](CHANGE_MAP.md) records the two citation repairs and explicit packaging exclusion. The audit's historical snapshot receipt continues to describe the first packet, not this revised release. The root SHA256SUMS manifest covers the revised release; audit/AUDIT_SHA256SUMS covers the unchanged audit deliverables.
