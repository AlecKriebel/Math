# Independent root reproduction for PR1119

The analytic proof establishes the universal theorem. Finite controls are attempts to falsify it and cross-check implementation, rather than a substitute for proof. Root read every mathematical family report and its complete checking code.

Four original reviewer programs were copied unchanged into ignored temporary directories and reproduced in ordinary Python mode, with assertion checks active where used. Each result equals the retained reviewer JSON data structurally. The parameter program writes its complete result file and prints only a human-readable summary; the corrected parent harness compares that file, as documented in its replay receipt.

Three programs used Python assert. Their historical originals remain unchanged. `guard_assertions.py` mechanically converts only assertions into explicit conditional raising; `GUARD_CONVERSION.json` records source and converted hashes. The retained guarded copies have zero assertion statements. Six runs (ordinary and optimized mode for each converted program) reproduce the same original expected JSON. A deliberately false converted condition exits nonzero with its expected message in both modes. Oracle controls already use explicit checking exceptions; the original independent review also verifies identical ordinary and optimized results.

These are standard-library programs. Run a checker from its own copied directory to keep generated result files together. Classical `controls.py`, classical `parameter_controls.py`, and construction `exact_controls.py` write JSON next to themselves. Retained comparison receipts list the exact hashes, result equality, execution modes, and limits. Temporary duplicate copies/results are ignored and excluded from checkpoints and publication files.
