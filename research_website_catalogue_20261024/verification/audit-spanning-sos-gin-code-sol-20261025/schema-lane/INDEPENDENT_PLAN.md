# Independent schema lane — early reconstruction

UTC checkpoint: 2026-10-25 (exact start recorded by audit runner). Completion estimate: 30% of this narrow code/schema audit; no estimate of the mathematical research goal is made.

This lane read the entire 204-line staged helper, INPUT_PINS.json, AUTHORITY_SOURCE_BINDINGS.json, all three actual SOURCE_READY objects, both actual normalized metadata objects, all three raw API records, all three complete transport lists, and all three original root scientific clearance / root editorial authority / editorial seal / manifest objects. It has not read stage guard-control results, execution conclusions, validation receipts, or the older-suite outcome. Discovery listed filenames only. No UI, network, Git, source-program execution, or archive extraction occurred.

Independently reconstructed expectations before running own controls:

- 23181280: receipt `actual_assets`, exact uppercase SHA256/MD5 plus two true API comparison flags, two API files; metadata is the raw record itself, with no normalized alias.
- 23442760: receipt `all_actual_assets`, lowercase sha256/md5, two API files; metadata has `all_actual_file_objects` and its original `assets` alias. That metadata alias must not be confused with a receipt alias.
- 23395703: receipt `all_actual_assets`, lowercase sha256 / uppercase MD5, three API files in deposited order TeX/PDF/ZIP. Actual raw metadata lacks the version key. Config/binding/gate version values remain null; presence flags are false. Original standalone TeX is the controlling source and must survive in the derived list.
- Transport distinctions are substantive: spanning uses bytes_received/uppercase digests and relative paths, SOS bytes/lowercase digests and absolute paths, Gin status/headers/bytes/uppercase digests and absolute paths. Gin's PDF raw header oc-checksum drops one leading zero, while its canonical API/receipt/computed MD5 retains it. Raw header preservation and payload digest agreement are separate claims.
- Authentication must anchor full source objects in original file bytes and independent root/editorial authority pins. Successful calls must not mutate either caller object or its nested dictionaries/lists.
- Ordinary read/caller tampering will be tested with all pins intact. Direct `validate_sg_assets` calls will isolate exact field schemas. Any inner-schema test that deliberately blinds a digest pin will be labeled as such and is not a successful attack on the sealed helper.
- Python equality may accept integer/float or bool/integer value aliases. Investigate whether that weakens an exact caller-object type claim without confusing it with a byte-integrity bypass.

Success criterion: direct independent hashes, unmodified-helper positive calls, targeted adversarial failures, and successful-call deep input snapshots substantiate this bounded audit; exact gaps must be retained. All new artifacts will remain under this lane directory.
