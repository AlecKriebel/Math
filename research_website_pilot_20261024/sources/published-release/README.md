# Free spanning-forest degree can decrease under squaring

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X
Preprint version 1.0.0, 22 October 2026.

For the binary grandparent graph G, the expected free uniform spanning forest
root degree is exactly (24-sqrt(2))/7 > 161/50. Its simple square has expected
degree at most 3208526010913748780/10^18 < 321/100.
With b_F(X) = E[deg_FUSF(X)(o)]/2 - 1, the difference exceeds 1/200.

The original Abért Question 24 concerns arbitrary vertex-transitive graphs
and does not print the normalization formula. This package states that
convention explicitly and proves unequal expected degrees directly.
The counterexample is infinite, connected, simple, unweighted, locally finite
and vertex-transitive; G has degree 8 and nonunimodular full automorphism
group. Its square has degree 40. No negative claim about the unimodular
subclass, another nonunimodular Betti invariant, or the known Cayley case is made.

## Scientific verification

Read main.tex or the separately supplied PDF. Both actual infinite free
exhaustion derivations and the finite-flow-to-free-exhaustion transfer are
written out. Standard Kirchhoff, Thomson and Rayleigh facts are credited to
the actual corrected BLPS body. DEPENDENCIES.md and PRIORITY.md identify
precisely the inspected primary versions and the remaining coverage limits.

Python 3.10 or later, standard library only:

    python3 -I -S -B verify_currents.py
    python3 -I -S -B check_reductions.py

The outputs must exactly equal CURRENT_RESULTS.json and REDUCTION_RESULTS.json.
Optional -O before the script name leaves the guards active. The full current
checker also has an observed byte-identical optimized replay.
No external data, numerical solver, claimant program, package installation,
network request or file mutation occurs.

The current certificate is the exact 165241-byte gzip file
square_flow_certificate.json.gz, SHA256
6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f.
It decompresses to 4460799 bytes of JSON, treated solely as inert data.
The new verifier independently generates the indexed 3-regular tree,
end-oriented graph and finite square, checking all 19931 edges and all
40 root neighbors. It checks every one of 797240 actual integer current
numerators, 122800 exact divergence equations, all 40 energy numerators,
and their exact total with denominator 10^18. Four corruptions of actual
rows (changed current, wrong source, boolean current, missing entry) are rejected.

This is a complete finite certificate check, not an approximation to an
infinite wired solution. The paper's separate finite-support/exhaustion
lemma turns it into an infinite FREE-resistance upper bound.
The original sparse floating-point witness generator is unnecessary and is
not distributed or trusted. Exact feasibility suffices; optimality is not claimed.

The reduction script builds actual finite circuits from binary descendant
words and performs global rational star-mesh elimination. Four branch depths
and induced n=2,3 exhaustions agree with the written recurrences. The largest
has 127 vertices. These finite interface diagnostics support indexing; they
do not replace the all-depth recurrence and contraction arguments.

## Typesetting and archive reproduction

The manuscript uses standard LaTeX article, fontenc, lmodern, amsmath,
amssymb, amsthm, geometry, hyperref and microtype. A normal existing XeLaTeX
installation (run twice) or Tectonic can typeset main.tex.
Preparation used the built-in LaTeX editor/compiler and an already pinned
Tectonic 0.17.0 in cache-only mode with network and all writes outside the
preparation folder denied. No compiler or third-party source body is bundled.
PDF bytes/layout may vary with different engines or font versions.

This archive contains its frozen paper.pdf, identical to the separate deposit
PDF. The offline packaging builder copies that frozen input; it does not
recompile TeX:

    python3 -I -S -B build_release.py --output NEW_EMPTY_OUTPUT_DIRECTORY

It reproduces all six release files byte for byte, including the source ZIP
and five-member upload kit. The deposit manifest lists only the separate PDF
and source/verification ZIP. The builder has no provider, credentials, DOI or
publication logic. source-manifest.json hashes every other scientific member.
Archive member times and modes are fixed for deterministic packaging.

## Status, provenance and rights

The argument and rational certificate were already public in project PR1407
before this note. This version is dated 22 October 2026 and is not backdated.
The grandparent family and general electrical/forest methods are prior.
Pete–Timár's component-count noninvariance is a different result and is credited.
No exhaustive novelty, firstness or continuing-openness certificate is claimed.

AI tools were extensively involved in mathematical research, exploration,
proof development and reconstruction, computational verification, literature
and source investigation, manuscript preparation, editing and adversarial
auditing. Human author: Alec Kriebel. This is an unrefereed preprint without
formal independent human peer review, journal acceptance or proof-assistant
certification. Internal AI reviews are not human refereeing.
Original prose and certificate data: CC BY 4.0. Original code: MIT.
Third-party scholarly bodies and private operational captures are excluded.
