"""One authorized factual publication update of the already merged PR body."""
from pathlib import Path
import json
from root_submission_gate import A, Capture, current_clearance, load, pin, utc

D = A / 'publication'
assert not (D / 'FINAL_PR_BODY_UPDATE.json').exists()
current_clearance()
status = load(A / 'CURRENT_PUBLICATION_STATUS.json')
assert status['status'] == 'MERGED_PUBLISHED_AND_TRACKER_VERIFIED'
assert status['workflow_completion_percent'] == 100
capture = Capture('published_pr_body')
fields = 'state,headRefOid,mergeCommit,body,url'
before = json.loads(capture.run('prior_body', ['gh', 'pr', 'view', '344', '--json', fields]).stdout)
assert before['state'] == 'MERGED' and before['headRefOid'] == status['accepted_head']
assert before['mergeCommit']['oid'] == status['actual_merge']
original = (A / 'accepted_pr_body.txt').read_text()
assert before['body'] == original
body = (original + '\nPublication completed on 4 October 2026: [A counterexample to Takao\'s self-duality question]('
        + status['doi_url'] + '), DOI **' + status['doi'] + '**, version 1.0. The public PDF and verification ZIP were downloaded in full and match the reviewed files; all 11 supplied metadata fields match, with no normalization. The DOI resolves. One row was appended through the Google Workspace CLI and read back exactly at '
        + status['tracker_updated_range'] + '. PR344 publication workflow: **100%**. Earlier pending and adverse review records remain dated history; the final third NEW full preprint review is clean.\n')
path = D / 'final_pr_body.txt'
assert not path.exists()
path.write_text(body)
capture.run('actual_body_edit', ['gh', 'pr', 'edit', '344', '--body-file', path])
after = json.loads(capture.run('actual_body_readback', ['gh', 'pr', 'view', '344', '--json', fields]).stdout)
assert after['body'] == body and after['state'] == 'MERGED'
assert after['headRefOid'] == status['accepted_head'] and after['mergeCommit']['oid'] == status['actual_merge']
record = dict(utc=utc(), status='PASS_MERGED_PR_PUBLICATION_BODY_EXACT_READBACK',
              pr=344, actual_merge=status['actual_merge'], doi=status['doi'],
              final_body=pin(path), native_capture_directory=str(capture.directory),
              comment_or_person_message_sent=False)
(D / 'FINAL_PR_BODY_UPDATE.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
