# Singular-value basins: audited unresolved checkpoint

UnsolvedMath 30001393 / OWR-4137-010, rank 617.

**Status: unsolved, 5/5 substantive approaches.** The source's immediate basin
is a basin of an attracting fixed point. Its general region question has no
assumption of simple connectivity, boundedness of singular values, or
containment of their closure.

Read these together:

1. [Author checkpoint](submission/RESULT.md): polynomial proof, precisely
   restricted published results, route obstructions and component-capture
   criterion. The frozen author directory is preserved unchanged.
2. [Full independent audit](audit/AUDIT.md): verifies those limited conclusions
   and adds discriminating controls. This is an independent AI audit, not
   external expert peer review.
3. [Clarification addendum](ADDENDUM.md): supersedes the apparent existence
   claim about unbounded singular-value entry times and supplies the requested
   boundary and contracting-disc details.

Reproduce all checks from this directory:

    python3 verify_release.py

The release verifier checks the exact file inventory and hashes, author and
audit manifests, byte-identical output replays, 8,233 author assertions,
350 independent audit assertions, and 33 audit provenance/replay assertions.
Its recorded negative controls reject altered or missing files, unexpected
files and a modified manifest. None of these tests resolves the unrestricted
mathematical questions.

The packet contains original notes, original checks, bibliographic references
and provenance digests. Scholarly PDFs, extracted full texts, source page
images, raw corpora and private coordination records are excluded.
