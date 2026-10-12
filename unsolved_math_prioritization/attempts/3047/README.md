# 3047 / OPG-37222: a sharp restricted partition-sign obstruction

## Accepted result

Independently choosing signs in at most two arbitrary original unrestricted-partition factors, with all other factors positive, cannot keep every coefficient bounded in absolute value by one through degree 86. An explicit choice for factors 1 and 2 works through degree 85. This is a sharp result for the specified restricted class. The full unrestricted problem remains unresolved by this work; no novelty, priority or finite-prefix record is claimed.

The [complete authored proof](TWO_FACTOR_OBSTRUCTION.md) and [source addendum](SOURCE_ADDENDUM.md) are unchanged. Read the [full substantive independent audit](INDEPENDENT_AUDIT.md), [scope acceptance](ACCEPTANCE.md), [editorial map](EDITORIAL_MAP.json), [public source metadata](PUBLIC_SOURCE_METADATA.json) and [aggregate verification metadata](VERIFICATION_METADATA.json) alongside them.

## What the finite proof uses

The proof reduces the class to 39 pairs plus two singleton controls. Its exact recurrence was checked against every supplied frontier as a set of complete sign strings, totaling 23,683 nonempty states. All six degree-85 final states and the printed sharpness coefficients were independently checked by direct convolution. Agreement of counts or hashes alone was not the acceptance test.

The computer-assisted completeness claim was independently checked locally. This prose edition includes the recurrence, its completeness proof, the full case table, the explicit final states, the sharpness witness and the complete substantive audit. It excludes programs, the full raw 1,182,664-byte all-state certificate and detailed computational outputs. It is not an executable replay package: a reader cannot replay the recorded exhaustive calculation from these files alone without independently implementing the stated recurrence. Public aggregate verification metadata and hashes describe the checked record; they do not replace raw frontiers or independently prove completeness.

## Historical scope

The first-factor-only degree-31 result is credited to Aaron Meyerowitz's revised 2017 answer. David Newman's follow-up asks about the first two factors. Max Alekseyev's separate numerator/denominator-sign variant has a reported maximum feasible degree 121, which was not independently certified here and concerns a different class. The Andrews–Newman identities for specified sets of dilates do not license removing inactive factors from the present unrestricted product.

No result about feasibility with three or more active factors, no unrestricted construction and no separately unfinished continuation is included. At least one substantive attempt is established; the total number of attempts is unknown. There is no five-exchange exhaustion claim.

## Edition boundary and integrity

Only authored mathematics, the substantive independent audit, scope acceptance and safe public source/verification metadata are included. No copied source texts, PDFs, images, datasets, private sources, personal data, private paths or coordination records are distributed. Source retrieval/inspection history is historical metadata, not a fresh source download performed to prepare this edition.

MANIFEST.json lists every other file in this directory, with exact byte counts and SHA-256 hashes. It excludes only itself to avoid a circular self-hash; an externally retained preparation seal pins the manifest and the exact closed inventory. Hashes authenticate byte identity when checked against a trusted external value. They do not certify mathematics or supply missing executable evidence.

This is AI-assisted, unrefereed research with independent AI-assisted verification, not external human peer review. This directory is a proposed prose edition; preparation itself makes no repository changes, opens no pull request and authorizes no publication.
