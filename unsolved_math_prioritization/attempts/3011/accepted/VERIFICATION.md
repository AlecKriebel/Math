# Verification scope

Date: 2026-10-08. Mathematical status: partial; KP-5.4 compact core unresolved.

## What was checked

The supplied checker uses exact rational arithmetic for its PL, symbolic-word, homology and normalized-angle calculations. Every condition uses an always-active `require`/`raise` path; no Python `assert` is used. It runs under the standard library and writes no files by default.

Actual executions used non-root UID 1000 against a tree whose directories were mode 0555 and files mode 0444. Normal Python, `-O`, and `-OO` all passed, with the program itself checking non-root identity and read-only accessibility. The environment disabled bytecode writing. The default output was JSON on stdout. An explicitly external JSON output file also succeeded.

Each of the three modes completed:

- 1,280 exact Alexander pair-distance cases, with inverse and displacement checks
- 900 exact convex interval-interpolation cases
- 2 explicit rotation-based shortcut counterexamples
- 78 finite homology-twist cases, with inverse and symplectic-form checks
- 270 cube-family monotonicity/boundary checks
- 30 symbolic noncommutative interpolation-factor cases, including zero-coordinate faces
- 8 exact radial-amplification cases: N=1,2,3,5,8,13,32,64

The normalized radial angles are rational multiples of π, so the accumulated angle is verified as exactly π, not inferred from floating-point sine/cosine values. The displacement 1/2 then follows from the proved rotation geometry. The word calculation preserves product order instead of testing only commuting radial examples.

## Meaningful controls

- A non-strict PL map is rejected by the inverse precondition
- Identity interpolation and identity slice projection preserve distinct test points
- The identity homology map is distinguished from a Dehn transvection
- Reversing the noncommutative factor order changes the symbolic free word
- Constant zero radial vertices produce zero accumulated angle
- `--require-readonly` rejects the writable development tree, including under `-O`
- An output path inside the read-only packet is rejected under `-OO`; no file is created
- A requested external output succeeds

## Limits

These checks are finite consistency checks of formulas used in the proofs. They do not certify the ANR property, the non-ANR property, all homeomorphisms, arbitrary metrizable parameter spaces, or all possible extension operators. The topological statements are justified by the written proofs and the explicitly listed external theorems, not by sampling.

The source manifest records which primary sources were inspected and which proofs were not obtained. A search miss is not evidence of nonexistence of a later result. No corpus body, PDF, copied source text, or private coordination file is part of this packet.
