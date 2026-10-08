# External-ray rotation: accepted scoped partial audit

Problem 5300074. Start with RESULT.md and ACCEPTANCE.md. The original question remains unresolved: disconnected neutral-boundary continuity and initially accessible indifferent-point compatibility are still gaps. The stopping budget is exhausted at 5/5.

The current RESULT.md is the accepted reviewed proof; INDEPENDENT_AUDIT.md preserves the complete independent audit with an archival-execution preamble. RESULT.md.patch contains contextual authored corrections; removed material is superseded, the full original report is omitted, and historical patch application is NOT_RUN. Public PDF titles, URLs, hashes, sizes and inspection history are metadata only. No source PDF/text, corpus/dataset content or private coordination is included.

For verification, first authenticate BOOTSTRAP.py against a hash obtained externally, such as the reviewed draft-PR body. Use Python 3 as actual UID=EUID=1000, with all delivered files 0444 and this directory 0555:

    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

Add --controls before the packet path to run the integrity/schema/comparator/hostile controls. The authenticated bootstrap fixes the verifier, controls, and whole-delivery manifest; changing a manifest does not replace the external anchor. Read CHECKS.md for exact testing scope and excluded stages.

Manuscript status: unrefereed authored partial-results audit, without a journal acceptance or originality claim.
