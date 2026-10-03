"""Observe only assigned native queue lines and distinguish historical proposals."""
from pathlib import Path
import datetime
import hashlib
import json

F=Path(__file__).resolve().parent
q=Path('/Users/alec/Documents/Math/unsolved_math_prioritization/QUEUE.md')
b=q.read_bytes();lines=b.decode().splitlines()
rows={key:[{'line_number':i+1,'literal_line':s} for i,s in enumerate(lines)
           if s.startswith('|') and (' '+key+' / ') in s]
      for key in ('30000166','30000167')}
assert len(rows['30000166'])==1 and len(rows['30000167'])<=1
parsed={}
for key,found in rows.items():
    for row in found:
        cells=[s.strip() for s in row['literal_line'].split('|')[1:-1]]
        assert len(cells)==12
        parsed[key]={'rank':cells[0],'problem':cells[1],'title':cells[2],
                     'status':cells[7],'turns':cells[8],
                     'chat':cells[9],'findings':cells[10],'doi':cells[11]}
diff=(F/'captures'/'pr_full_diff'/'STDOUT.bin').read_text()
head_proposals=[s[1:] for s in diff.splitlines() if s.startswith('+|') and ' 30000166 / ' in s]
assert len(head_proposals)==1
result={'schema':'pr51-selected-native-boundary/v1',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'queue_path':str(q),'queue_file_identity':{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},
        'selected_literal_rows':rows,'parsed_rows':parsed,
        'duplicate_queue_row_present':bool(rows['30000167']),
        'original_head_target_queue_line_proposal':head_proposals[0],
        'original_head_proposal_qualification':'Historical unmerged branch body, not current applied status or future ROOT authorization',
        'native_source_only_boundary':{
            'four_historical_observations':['target queue row','duplicate queue row presence/absence','target selected catalog row','duplicate selected catalog row'],
            'potential_owned_queue_fields':['Status','Turns','Findings'],
            'preserved_queue_fields':['Chat','DOI','every other field and row'],
            'duplicate_absent_row_authority':'No insertion or new independent budget is authorized by this preparation',
            'current_canonical_mutations_performed':False,
            'future_canonical_mutations_approved':False},
        'accounting':{'original_proof_attempts':0,'budget':5,'new_proof_attempts':0,'audit_proof_attempts':0,
                      'separate_original_source_response_count':'Not supplied by original ledger; two events are not fabricated as responses'},
        'publication_approved':False}
(F/'SELECTED_NATIVE_BOUNDARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
