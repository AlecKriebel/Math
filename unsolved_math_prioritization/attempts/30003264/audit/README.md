# Independent audit of 30003264

Verdict: **PASS for the frozen statement-repair and bounded partial-investigation packet. The primary problem remains unresolved, with 5/5 approaches used.**

Read `AUDIT.md` for the mathematical, source, corpus and adversarial review. `MANDATORY_CORRECTIONS.md` identifies the already-addressed imported-domain correction and the limits on interpreting the result. `VERDICT.json` is the machine-readable disposition; `SOURCE_RECHECKS.json` records only public verification metadata.

The author freeze is unchanged. No remote write was performed.

## Replay

With Python 3.10 or newer, no third-party packages and no network:

    python3 -I -B independent_verify.py /path/to/PREBLOCH_30003264_AUTHOR_PACKET.zip

The output must equal `INDEPENDENT_VERIFICATION.json` byte for byte. Repeat with `-O` to check optimization independence. The program checks the externally pinned author archive, extracts it into a temporary directory, replays both author programs and performs independent exact finite controls and corruption tests. It does not require or include private corpus files or scholarly PDFs.

`MANIFEST.json` lists the safe audit files other than itself. The separate archive receipt anchors that manifest and the audit ZIP. Source materials and private working files are excluded.
