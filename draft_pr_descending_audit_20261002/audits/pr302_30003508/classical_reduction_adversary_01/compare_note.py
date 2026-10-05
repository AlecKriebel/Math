import datetime, difflib, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
original=root/'inputs/TIKHONOV_EXISTENCE_REDUCTION.md'
current_path=root.parent/'priority_mechanism_adversary_01/TIKHONOV_EXISTENCE_REDUCTION.md'
before=original.read_bytes(); after=current_path.read_bytes()
final_copy=root/'inputs/TIKHONOV_EXISTENCE_REDUCTION_FINAL.md'; final_copy.write_bytes(after)
diff=''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),
                              fromfile='frozen_initial_note',tofile='current_note_20261005'))
(root/'NOTE_WORDING_DIFF.patch').write_text(diff)
result=dict(compared_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            original_copy=str(original.relative_to(root)),original_sha256=hashlib.sha256(before).hexdigest(),
            current_origin=str(current_path),current_copy=str(final_copy.relative_to(root)),
            current_sha256=hashlib.sha256(after).hexdigest(),diff_file='NOTE_WORDING_DIFF.patch',
            interpretation='Human-readable diff requires subsequent independent semantic review; no old receipt is replaced.')
(root/'CURRENT_NOTE_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2)); print(diff)
