# Independent review and portable replay

AUDIT.md is the complete, unchanged independent mathematical review. Its verdict is PASS for the five scoped partials and HOLD for a claimed solution of the original quasi-isometry problem. This is AI review, not human peer review.

The original checker, its complete output, both author-script replays, and its historical manifest are preserved byte-for-byte. The historical AUDIT_MANIFEST.json also records two locally inspected primary-source files, aim_archive.html and aim_archive.txt; those source files are deliberately not distributed here. Their absence from this repository packet is not a failed mathematical replay.

From the problem directory, run:

    PYTHONDONTWRITEBYTECODE=1 python independent_review/run_independent.py > independent_replay.json

Compare the parsed JSON with independent_review/independent_controls.json. The wrapper only points the unchanged original checker's PUB variable at the frozen packet beside this directory. It adds no mathematical control, alters no algorithm and does not create a sixth attempt. The publication manifest separately binds all distributed files.
