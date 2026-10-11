# Review replay

Run `python verify_review.py --author /path/to/30004293`. This checks the frozen final author manifest, every recorded Git blob and all five author receipts, and replays the independent controls. Python standard library suffices. The wrapper does not claim to redownload or recheck primary PDFs. The recorded full local audit included all five PDFs; use the author's source manifest and replay_author.py with a populated sibling source/ directory to repeat those checks. Raw sources are not part of this public review bundle.
