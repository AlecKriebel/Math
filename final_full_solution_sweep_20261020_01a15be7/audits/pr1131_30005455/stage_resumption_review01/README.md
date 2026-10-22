# Closed operational review evidence

Decision: **HOLD**. Start with `REPORT.md` and `ACTION_REVIEW.json`. This folder contains evidence from a read-only review of the frozen known-unattempted stage-resumption v01; it is not a production execution package or authorization.

For read-only verification, run Python in isolated standard-library mode:

```sh
python3 -I -S -B /absolute/path/to/stage_resumption_review01/verify_review.py --seal-sha256 THE_EXTERNALLY_RECORDED_MANIFEST_SHA256
```

The same verifier may be run with `-O` or `-OO`. It checks the stored outcomes, copied inputs, full recursive custody inventory, file metadata, no outside hardlinks, and the allocation cap. It never imports or executes publication code, loads credentials, queries a service, or writes a file. Omit `--seal-sha256` only while initially checking evidence before sealing; that mode does not authenticate custody.

The three independent control drivers are `actual_wrapper_controls.py`, `actual_pr_reference_controls.py`, and `main_guard_controls.py`. Their completed normal, O, and OO result files are retained. The drivers deliberately refuse existing mode outputs. Do not rerun them in this closed folder, point them at production, or modify their frozen fixtures. To independently rerun, establish a newly assigned, empty review folder and an independent copy of all 282 pinned fixture inputs, then make explicit reviewed path adaptations in that new folder. All external escape interfaces must remain blocked before lifecycle modules load. The recorded private fixtures are local audit evidence and are not a claim of a portable public distribution.

`PUBLIC_MANIFEST.json` inventories the shareable reports, controls, and summaries. `MANIFEST.json` covers every recursive file, including private fixtures and all nested manifests, excluding only its own exact path. An external hash of that full manifest is the seal. Do not change this folder after sealing.
