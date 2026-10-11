from pathlib import Path
import datetime, hashlib, json
p=Path(__file__).resolve().parent
def pin(f):
 b=f.read_bytes();return {'path':str(f),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
v={
 'frozen_at_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'family':'mechanism-first independent priority audit',
 'original_claimed_solved_fraction':{'numerator':1,'denominator':5},
 'first_model_freeze':pin(p/'FIRST_SOURCE_ONLY.json'),
 'candidate':pin(p/'private/CANDIDATE_pinned.md'),
 'input_pdfs':[pin(f) for f in sorted((p/'private').glob('*.pdf'))],
 'forbidden_conclusion_inputs_read_before_freeze':[],
 'priority_verdict':'PRIORITY_UNESTABLISHED; no historical explicit complete resolution established in inspected primary corpus',
 'already_solved_supported':False,
 'novel_application_certified':False,
 'validity_verdict':'NOT_ASSIGNED: no fresh central proof search or independent central proof certification in this family',
 'strongest_verified_findings':[
  'Original 2004/2005 primary sources explicitly pose symmetric W4 LOCC dense-codeability as unknown under separate unitary senders and LOCC receivers.',
  'Pradhan–Agrawal–Pati 0705.1917v1 section 4.2.3 already published W4 Bell preprocessing and classical forwarding followed by Bell decoding, recovering exactly 2 bits in a one-copy, one-sender/two-receiver model.',
  'Winter quant-ph/9807019v3 Theorem 9 supplies a general independent-input cq-MAC coding theorem; Huang–Zhang–Hou quant-ph/9911120v5 supplies pure-output MAC achievability and an explicit generalized dense-coding application with one global output receiver. These establish prior ingredients, not an explicit W4 LOCC strict >2-bit application.',
  'Das et al. 1412.6247v1 and Muhuri et al. 2211.13057v2 explicitly define their two-receiver quantities as upper bounds. Values above the classical threshold do not certify achievable W4 rates.',
  'Wang–Yan 2011 and Shukla et al. 1204.4573v1 show 3-bit W4 encodings for one sender holding two qubits and one receiver performing a four-qubit joint measurement.',
  'Hayashi–Wang 2109.12518v1 and final PRX Quantum 3 030346 Theorem 2 address one encoder system fully sent to Bob plus a nonencoding helper, with multiplicity-free direct-part hypothesis; no explicit W4 two-independent-sender split-routing strict >2-bit application was found in the inspected setting/results.',
  'Situ et al. 1106.3956v2 W protocol uses two three-party W resources and joint unlocking requiring receiver quantum communication, extra shared entanglement, or direct interaction.',
 ],
 'remaining_gaps':[
  'Finite search and partial citation coverage cannot certify global novelty or universal historical absence.',
  'No complete retained binary of final Hayashi–Wang publisher PDF: direct curl returned 403 and APS harvest timed out; final setting and Theorem 2 were checked through publisher PDF web extraction, with complete arXiv v1 retained.',
  'Primary full texts for Zhao et al. 2012 and Yuan et al. 2011 DSQC near matches were not obtained in this family; they remain access gaps rather than conclusive exclusions.',
  'Not all downstream citations, theses, non-English literature, or unindexed publications were enumerated.',
 ],
 'decision_rule':'A source must give an actual achievable strict >2-bit rate for symmetric W4 with independent local-unitary messages and receiver-only LOCC after A1→B1 and A2→B2, or a complete historically published equivalent application. A deduction performed now from a generic old theorem is not enough to label the original target already solved.',
}
(p/'FIRST_PRIORITY_VERDICT.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
(p/'FIRST_PRIORITY_VERDICT.md').write_text('# First independent priority verdict\n\nFrozen UTC: '+v['frozen_at_UTC']+'\n\n'+v['priority_verdict']+'.\n\nAn explicit complete historical resolution is not established by the inspected corpus. The application is not certified novel. The Bell-first mechanism and general MAC theorem are prior art and must be attributed. The strict >2-bit asymptotic W4 application under the frozen original allocation is the exact priority gap. Author SOURCES, prior reviews, sibling reports, and ROOT mathematical/priority conclusions remain unread.\n\nNo central validity verdict is assigned. Original claimed_solved 1/5 is preserved.\n\n'+ '\n'.join('- '+s for s in v['remaining_gaps'])+'\n')
print(json.dumps({'frozen_at_UTC':v['frozen_at_UTC'],'verdict':v['priority_verdict'],'json_pin':pin(p/'FIRST_PRIORITY_VERDICT.json'),'md_pin':pin(p/'FIRST_PRIORITY_VERDICT.md')},indent=2))
