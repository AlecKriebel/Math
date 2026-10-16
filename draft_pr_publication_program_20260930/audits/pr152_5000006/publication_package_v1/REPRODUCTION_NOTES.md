# Reproduction and limits

The universal conclusion is the geometric argument in the manuscript.
The finite scripts do not prove the Veech lattice/cusp theorems,
hyperelliptic uniqueness, or every affine cone-germ transformation.

verify_exact.py uses exact fractions and integers for polygon edge
identifications, genus and fixed-point counts, direct-chord labels,
the parity-selected literal source definition, full corner congruences,
intrinsic and physical reversal/reflection, canonical weight signs,
marked-lattice identities, and rational linear-map scaling.
It checks n3 through32 and a bounded lattice box, with other finite
corner and linear-map controls, for 19,458 explicit checks.
Every check raises an exception on failure; Python optimization cannot
remove it. A generic positive matrix control is not claimed to verify
the geometric cone-lift lemma for all matrices.

The output verification.json pins the manuscript source and checker.
exact_reversal_counterexample.py works in Q(sqrt(5)), with y scaled by
the positive number sin(pi/5), for 15 explicit checks. It verifies strict
side-interior points A,B, the reflection and retracing equations, and the
parity-selected forward/reverse label. Its path O-A-B-A-O has side word
[1,3,1], N4, alpha=beta=pi/2, and physical label2mod3 in either direction.
The false universal label-negation rule would predict1mod3. The sine
weights of1 and2 agree, so the target theorem survives. This is an exact
control for the sign repair, not a trajectory search or proof of the
universal sine ratio.

ROOT copied the whole source layout into separate ordinary/optimized
scratch directories, ran both scripts, and compared their complete
returned JSON values: equal, with 19,458 and15 checks respectively.
It injected a false first vertex-class condition into separate scratch
copies. Both modes exited1 at the named condition and created no
success receipt. Source files in this package were not changed by those
negative controls.

The earlier independent mathematical audit additionally traced physical
billiards and checked broader exact partitions; those calculations helped
find the original label error. Their floating-point ray tracing has no
certified error bounds and is not part of the minimal reproducibility
package. A sample agreeing to floating-point precision does not certify
the all-n theorem or establish priority.

Run from an extracted scratch copy of the whole archive, preserving the
manuscript source one directory above verification/. Scripts write their
JSON outputs alongside themselves. Source changes alter the bound receipt
and require regenerating it; the manuscript is the final proof artifact.
The checks require Python3.10+ and only its standard library.

