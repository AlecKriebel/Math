# Independent line-arrangement acceptance packet

This source-free packet accepts the specified partial mathematical work and leaves the general algorithm/lower-bound problem unresolved.

- `AUDIT.md`: mathematical, computational-model, literature, and executable audit with exact acceptance limits.
- `INPUT_PINS.json`: hashes and byte counts for every original packet file, with unchanged-input checks.
- `SOURCES_AUDIT.json`: public source hash checks and inspection limits; no source documents.
- `independent_checks.py`: independent exact graph construction, shortest distances, all-tie fixtures, metamorphic checks, and adversarial invalid paths.
- `mutation_checks.py`: eight semantic mutants, reporting original-suite survivors and detecting the two weakened guards with the supplemental tests.
- `AUDIT_VALIDATION.json`: observed execution and mutation outcomes.
- `CLARIFICATION.patch`: optional additive source/output wording refinement. No mathematical correction is necessary. The original report is not changed.
- `MANIFEST.json`: hashes and sizes of the other audit files.

## Replay

Use Python 3.12 or a compatible standard-library-only interpreter. Supply the path to the original packet's `verify.py` as the last argument; the examples below use `../original/verify.py` as a placeholder.

    python3 -I -B ../original/verify.py --require-readonly
    python3 -I -B -O ../original/verify.py --require-readonly
    python3 -I -B -OO ../original/verify.py --require-readonly
    python3 -I -B independent_checks.py ../original/verify.py
    python3 -I -B -O independent_checks.py ../original/verify.py
    python3 -I -B -OO independent_checks.py ../original/verify.py
    python3 -I -B mutation_checks.py ../original/verify.py

The first three commands require real/effective UID 1000, nonwritable original files, and a nonwritable original directory. They deliberately attempt append-open and directory-create probes. The mutation harness itself runs each mutant under all three optimization modes, writes only temporary copies in the operating system's temporary directory, and never modifies the original input. Its two expected survivors in the original suite are explicitly reported; the adversarial suite must reject both.

The independent checker's negative paths are executable fixtures in `adversarial()`. They test distinct rejection causes, not just whether an exception occurs. The first violates the incidence-sensitive edge bound. The second adds the remote line y=100 so that the same valid-edge detour fits that bound but still has disconnected intersection with y=0.

## Optional clarification

`CLARIFICATION.patch` targets exactly the report pinned in `INPUT_PINS.json`. Apply it only to a separate copy after verifying the source hash. It records the disagreement among summaries of the 1999 k-orientation bound and distinguishes input grouping from ordered expanded-output costs. Acceptance of the original mathematical proofs does not depend on applying it.

## Limits

These checks concern modest exact rational fixtures. They are not a general subquadratic algorithm, a universal complexity lower bound, a proof of present-day openness, or a formal certification of the cited literature. Neither the full 1999 paper nor the full 2020 thesis was inspected. The preserved original hop-witness correction remains necessary. No source corpus, dataset contents, or private coordination information is included.
