# Exact verification supplement for k405

This supplement supports the research note on the unweighted vertex centroids of the **unprimed, full-line antipedals** of a Poncelet billiard family. The theorem uses a noncircular ellipse with a > b > 0, a nested nondegenerate confocal elliptical caustic with 0 < lambda < b², and even **least period N >= 4**, with distinct vertices. Simple and primitive star orbits and either orientation are included. A circle is treated separately in the written proof; the formula containing a² - b² is not evaluated at a = b. Hyperbolic caustics, endpoint caustics, two-bounce degeneracies and arbitrary repeated odd-period lists are excluded.

The source's opposite-vertex statement supports the primitive-period interpretation, but it does not formally define least period. The note retains this qualification. No copyrighted primary-source body is included here.

## Environment and commands

The actual reproduction used **CPython 3.14.6 and SymPy 1.14.0**. `author_exact.py` and the CLI/runner use only the Python standard library. The independent and exact boundary programs require SymPy. Other versions have not been tested for this supplement. To install the exact symbolic dependency into an environment of your choice:

```sh
python3 -m pip install -r requirements.txt
```

From this directory, run the complete reproduction in a fresh result directory:

```sh
python3 -B run_reproduction.py --output-dir my_results
```

The runner uses its own Python interpreter, runs all six positive and eight expected-failure cases below, and writes a `REPRODUCTION.json` journal. Each child runs from an initially empty working directory, so execution cannot depend on a local `PROOF.md` or repository layout. Each child has a 30-second deadline; a timed-out POSIX process group is terminated and reaped before failure is reported. All 14 actual recorded children exited and were reaped, with empty process groups. The supplied `results_20261007/` records are actual executions, not expected-output templates.

Individual positive runs are:

```sh
python3 -B author_exact.py --output my_results/author_normal.json
python3 -B -O author_exact.py --output my_results/author_optimized.json
python3 -B independent_exact.py --output my_results/independent_normal.json
python3 -B -O independent_exact.py --output my_results/independent_optimized.json
python3 -B exact_repeated_odd_boundary.py --output my_results/boundary_normal.json
python3 -B -O exact_repeated_odd_boundary.py --output my_results/boundary_optimized.json
```

`--output` selects a JSON file and creates its parent directory; omitting it prints JSON only. Existing output files are refused. Use a different result directory when repeating the complete runner. `--proof PATH` is optional and hashes the explicitly selected file. Without it there is **no proof-file lookup**. It does not inspect, verify or establish the correctness of that file. The included positive runs did not supply this option. Each result also records the executed verifier's SHA-256, interpreter version, optimization mode, UTC and actual process ID. The manifest hashes the whole supplement, including the shared helper.

## Actual checks and their scope

The normal and optimized runs gave identical mathematical counts:

| Program | Exact conditions per mode | Coverage |
| --- | ---: | --- |
| `author_exact.py` | 686,292 | 19,543 rational chords across five axis/focus triples, both foci and origin line systems, tangency and denominator identities, differentiated squared length, 1,036 reduced even rotation cases, and five exact axis-vertex four-periods |
| `independent_exact.py` | 12,846 | Five generic symbolic reductions; 1,004 independently generated rational endpoint chords; three exact six-bounce orbits including reflection, tangency and direct nonzero focal centroids; 662 primitive even rotation cases; repeated odd rotation exclusions |
| `exact_repeated_odd_boundary.py` | 19 | One exact least-period-three orbit, its nonzero origin antipedal centroid, and the unchanged centroid when its vertex list is traversed twice |

The author program uses focus-translated line equations and rational chord midpoint/half-angle parameters. The independently prepared program uses absolute-coordinate line equations and independently generated endpoints, and reduces symbolic numerators modulo the circle and focus relations. This portability adaptation is not a new independent mathematical review. `SOURCE_PROVENANCE.json` records the accepted source versions; mathematical calculations are retained from those versions. Changes supply portable outputs, optional proof hashing and deliberate failure switches.

These computations check the focal opposite-edge identity, supporting algebra and selected exact configurations. The written finite circle-action argument proves the half-period pairing for every admissible even least period. Reflection stationarity and unconstrained first variation establish the required sums and family perimeter constancy. Finite rotation checks are illustrations of that argument, not a simulation or proof of all billiard trajectories. No approximate numerical orbit experiment is included in this supplement. Symbolic rational-function identities are used only on the nonsingular domain established by the written proof. Neither a passing receipt nor a proof hash proves the whole theorem, validates source attribution, or establishes priority, exclusivity or independence from other work.

The boundary program gives, for a = 2 and b = 1, a primitive triangle on a confocal elliptical caustic with origin antipedal centroid ((35 - 5 sqrt(13))/24, 0). Its centrally reflected orbit has the opposite centroid. Repeating the list twice gives six entries without changing that nonzero centroid. This refutes the broader even-list-length extension; it does not refute the stated primitive-even theorem.

## Deliberate failure controls

All checks use explicit exceptions rather than Python `assert`, so optimization does not erase them. The complete runner tested these four controls both normally and with `-O`; all eight returned exit code 1, produced the specified `RuntimeError`, and wrote no success receipt:

```sh
python3 -B author_exact.py --negative-control false-guard
python3 -B independent_exact.py --negative-control corrupt-focal-identity
python3 -B independent_exact.py --negative-control singular-line
python3 -B exact_repeated_odd_boundary.py --negative-control false-guard
```

Repeat each command with `-O` after `-B` for the optimized version. The first and fourth force a false production predicate. The second adds 1 to the claimed focal pair identity before the production symbolic check. The third passes collinear input to the production antipedal solver. **Nonzero exit is the expected successful outcome of these negative controls.** Ordinary mathematical runs use none of these switches.

The supplement was prepared and reviewed using AI tools. It supports an unrefereed research note and does not claim human peer review. Its programs make no DOI, GitHub, spreadsheet, publication or external-contact changes.
