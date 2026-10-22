# Verification scope

The following records describe historical finite checks on 10 October 2026. Edition preparation verifies identities and prose preservation, not a fresh run of the mathematical programs.

## Author checks

Normal Python used all eleven starts: 10, 25, 50, 100, 187, 200, 252, 317, 400, 512, 800. Each tail used 24 shells. Python -O and -OO used the quick three-start subset 10, 25, 50. The two optimized outputs agree exactly; their shared fields agree with the corresponding normal-run fields. These are not three identical full runs.

Literal running-LCM enumeration and odd-part enumeration agreed on 16 shells below 2^16, including 283 smooth occurrences. The repeated shell [16,32) has seven terms and numerator 65; the deduplicated numerator 19 and a missing normalization factor 1/2 were rejected. Sample actual-tail and profile enclosures had widths below 10^-14. Decisions used exact rational intervals and outward-rounded fixed-point logarithms; floats were display-only.

## Independent audit checks

The independent implementation used cumulative smooth counts between prime-power events and a different -log(1-z) logarithm series, importing and running no candidate code. Its small checks agreed on 104 shells and 991 occurrences across nine prime sets. It reconstructed all eleven normal sample starts with 28 tail shells. Optimized -O and -OO runs used three starts, 10, 100, 317, while retaining all nine small-support cases and the full 32-shell gap-constant check. Optimized outputs agree with each other and with corresponding normal fields, not with the entire eleven-sample normal output.

Independent actual-tail and profile enclosures had widths below 10^-18 and overlapped the candidate enclosures. The oscillation constant was enclosed to width below 10^-25 and certified strictly between 0.0127214469683 and 0.0127214469684. Changed-manifest, same-size altered-proof and truncated-proof controls were rejected. The candidate packet was unchanged.

## What is and is not reproduced here

The full mathematical proof and complete independent audit, including finite-check methodology and remainder arguments, are present. Programs, raw output files, full exact enclosure records and numerical certificates are omitted. A reader can inspect and reconstruct the arguments but cannot execute the original finite computations from this prose-only edition alone. Historical PASS metadata does not imply fresh execution or formal certification. Finite examples corroborate formulas and constants; the infinite asymptotic, interval and finite-family obstruction follow from the written proofs. Irrationality and cofinal residue escape remain unresolved.

Source hashes, byte counts and retrieval history authenticate identified historical bytes; source documents are not redistributed. The independent audit's Cook comparison uses retained bytes after live retrieval failed. No new scholarly-source retrieval or inspection was performed during edition preparation.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance is limited to the stated partial analytic result. No external human peer review, journal acceptance, formal proof-assistant certification, exhaustive priority search, or novelty certification is claimed.
