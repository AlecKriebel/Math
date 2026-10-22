# Lossless local replay custody

Archive custody contains26 completed own repair mirrors:23 historical through07 plus3 accepted final10 full mirrors.05 used superseded source;06/07 infrastructure failures are excluded, including missing RESULT status. Normal08 partials and the complete failed normal09 harness-namespace run remain loose, as do their never-run O/OO copies. Current final10 is accepted local preparation evidence only; new independent review/root clearance remain mandatory. Original live/canonical captures, review/root evidence, scientific assets and proposed integration bytes were untouched. Separately authorized external empty carriers were restored exactly. REPLAY_ARCHIVE_CUSTODY.json supplies every full archive and exact original inventory pin.

Storage exhaustion first required temporary removal of 205 redundant frozen PDF/ZIP copies and172,361 generated account-page paths across two explicit rescue phases whose bytes matched the untouched canonical originals exactly. The complete pre-unlink source/copy, byte/SHA, mode and nanosecond mtime mappings remain in `private/repair03_archival_work/TEMPORARY_*RECOVERY*`. No altered account case, source, cache, intent, result or nonmatching/incomplete binary was removed in that rescue. All missing paths are now represented in the closed archives; they are deliberately absent as loose files in the archived roots.

To avoid reinflating those paths, each archive used a **virtual original snapshot**: the retained tree plus the durable pre-unlink inventory, with each missing member supplied from separately hash-verified retained canonical bytes. The archiver verified every member, hardlink payload, path/type/mode/mtime, full member closure, gzip CRC and unchanged retained source before deleting the redundant loose tree. Original account inode sharing groups were reconstructed as archive hardlinks; PDF/ZIP members remained separate regular files. Restoring preserves exact path/type/mode/mtime/body, while operating-system inode numbers necessarily change. Canonical originals were never linked to or modified.

The first-phase source used was `private/repair03_archival_work/archive_virtual.py`, SHA256 `b314f1b9815638611793f1a5d688735a90dc7b46944a8ec1832390938e89d45f`. The later completed-mirror source is archive_virtual_completed.py SHA2564f92d59f6a9a9f512fa6db27d4f0f9e30b6cbfdffc1903c46c08bebb850a2db1; the source-checked authorized-carrier program is carrier_archiver.py SHA2566a9d563a7d3338542dd7ca5f5b528aef3060f798d83f532a59fa351d0f69b67c. Both are in private/repair03_archival_work. Its complete pre-unlink original log/inventory/source bundle is pinned in REPLAY_STORAGE_HISTORY.json. Later archives persist a per-root receipt before unlink. Earlier unsuccessful archiver sources and the ENOSPC history are retained. They did not remove source mirrors before archive verification.

## Exact restoration

First independently verify this public document and `REPLAY_ARCHIVE_CUSTODY.json` against the externally anchored final operations manifest. The following local-only utility must then be hash-checked before compilation; it imports only the standard library and cannot load the service helpers. Its source is in the private custody closure:

`private/repair03_archival_work/restore_verified.py`

SHA256: `bc7f8a954850ed45fd4a3c06343e93f7bf1e1b31adac3074c7d9f93716bb5bfc`.

Choose an archive's exact `root` from the custody JSON. Restore only to a NEW direct child of `operations/private` named `restored_replay_…`, with enough free space for its logical inventory and metadata. For example, the following restores the first probe; use a fresh destination name each time:

```sh
python3 -I -S -c '
import hashlib,json,pathlib,sys
o=pathlib.Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations")
p=o/"private/repair03_archival_work/restore_verified.py"
b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!="bc7f8a954850ed45fd4a3c06343e93f7bf1e1b31adac3074c7d9f93716bb5bfc": raise SystemExit("Restore source SHA mismatch")
r=next(r for r in json.loads((o/"REPLAY_ARCHIVE_CUSTODY.json").read_bytes())["archives"] if r["root"]==sys.argv[1])
sys.argv=[str(p),"--archive",str(o/r["archive"]["path"]),"--archive-sha256",r["archive"]["sha256"],"--inventory",str(o/r["inventory"]["path"]),"--inventory-sha256",r["inventory"]["sha256"],"--original-inventory-sha256",r["original_path_type_mode_mtime_bytes_sha256"],"--destination",str(o/"private"/sys.argv[2])]
exec(compile(b,str(p),"exec"),{"__name__":"__main__","__file__":str(p)})
' private/repair03_probe_normal_ff053f54e9ad4428a543f0e1ad71e6f1 restored_replay_probe_example_01
```

The utility checks externally supplied archive/inventory SHA pins, the canonical original inventory, every member/body and gzip CRC **before** creating the destination. It refuses unsafe paths, symlinks, special files, duplicate/forward hardlinks, an existing destination or any destination outside the assigned operations private folder. It restores exact nanosecond mtimes/modes and then verifies the complete restored inventory again. An interrupted restore leaves only its new private destination for inspection; it never overwrites archived or original evidence.

A full restore/readback of the 1,183-entry first probe passed. Its closed inventory SHA is `3105fcb2eb9bd1b65c6b0f6fe07ea3fb489f79f4a914474480ca6186bdda9545`. The durable validation receipt is `private/repair03_archival_work/RESTORE_VALIDATION.json`, SHA256 `272b97b8f8ec7573a8d8a43a6dbb15f0431e62ac63ad701d129d0d1034c79cfc`. That redundant validation copy was removed only after exact readback and receipt persistence; the verified archive remains.

Archived probes are historical evidence, not current operational clearance. Final05 passed a preceding source version; final06/final07 hit ENOSPC and are excluded from accepted all-mode evidence. Normal08 also failed ENOSPC without RESULT and remains preserved loose; its O/OO copies never ran. Root authorized the minimal harness-only safe-link correction. Normal09 failed a harness namespace control and remains preserved loose;09 O/OO never ran. Root authorized its one-line c.PRIVATE correction, with no guard relaxation. Fresh final10 ordinary/-O/-OO each passed26 full and21 nested focused groups. Each complete accepted10 mirror was verified/archived before the next mode, while all131 original copied input files plus COPY_RECEIPT/RESULT remain byte-exact as loose files for the unchanged final verifier. Full generated captures and RUN logs/receipt remain inside its archive; RETAINED_INPUTS_VERIFIED.json records exact input/report readback. The local-only private/repair03_final10_input/archive_mode.py wrapper, SHA256f0ef1f5fa2fa9576be0a7368cc5fc88736e0eb1f6981ff81228d9eb419668ffd, additionally restores only the three fixed RUN members after matching their original inventory pins. ARCHIVE_COMPLETED.json binds their exact retained bytes and the archive-completion time before the next mode. The10 archiver is private/repair03_archival_work/archive_accepted10.py, SHA256544cb345d0b68eba6fd748246855a2156f7a82104ff6d8d66dfa00e590c6ace4; its scope-only delta from the preserved09 archiver is private/repair03_final10_input/ARCHIVER_SCOPE.diff. Existing source-checked restore_verified.py and its exact restoration requirements above apply unchanged. Final10 is accepted local preparation evidence only. Publication readiness remains false pending a new independent review and root adoption/clearance.
