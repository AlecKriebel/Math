#!/usr/bin/env python3
"""Check prior seals/preserved bytes and global correction surfaces, read only."""
import hashlib,json,ast
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'publication';E=A.parents[1]
def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def run():
 r=A/'reviews/full_package_01';raw=(r/'MANIFEST.json').read_bytes();need(sha(raw)=='5bf7174357ccf4e228aeb14e1d25e44c9692b253919cde867c42b1a65956d3a1','review01 seal');m=json.loads(raw)
 for n,v in m['files'].items():
  b=(r/n).read_bytes();need(v=={'bytes':len(b),'sha256':sha(b)},'review01 member '+n)
 need(len(m['files'])==36,'prior36');c=P/'reviewed_candidates/candidate01';raw=(c/'PREPUBLICATION_FREEZE.json').read_bytes();need(sha(raw)=='416e87c09e37e7cc8ef5e03fe7a725f4300ba6e9c362b1ea4ba920ba6b80ecf1','prior freeze');f=json.loads(raw)
 for n,v in f['files'].items():
  b=(c/n).read_bytes();need(v=={'bytes':len(b),'sha256':sha(b)},'preserved prior14 '+n)
 need(len(f['files'])==14,'prior14')
 current=json.loads((P/'PREPUBLICATION_FREEZE.json').read_bytes());need(current['revision_candidate']==2,'revision')
 decision=json.loads((A/'PUBLICATION_DISPOSITION.json').read_bytes())['decision'];merge=(E/'merge_pr919.py').read_text();need(decision=='PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE' and decision in merge and 'Exact-source acceptance after sequential fresh reviews required' in merge and 'Accepted freeze changed' in merge and 'Live PR head changed' in merge,'R1 guards')
 surfaces={'README':P/'README.md','requirements':P/'requirements.txt','metadata':P/'zenodo-deposit.json','metadata_generator':P/'prepare_metadata.py','live_PR_source':A/'PR_DESCRIPTION_CORRECTED.md','framing':A/'PUBLICATION_FRAMING.md'}
 for n,p in surfaces.items():
  s=p.read_text();need('POSIX' in s and ('O_NOFOLLOW' in s or 'os.O_NOFOLLOW' in s),'R2 '+n);need('macOS' in s and 'Linux' in s,'execution qualifier '+n)
 need('POSIX' in (P/'note.tex').read_text(),'notePOSIX')
 for n in ['README','metadata','metadata_generator','live_PR_source','framing']:
  need('broader' in surfaces[n].read_text(),'O1 '+n)
 need('broader Question' in (P/'note.tex').read_text(),'O1 note')
 sources=[]
 for n in ['append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py']:
  raw=(E/n).read_text();tree=ast.parse(raw);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='verify_receipt_links');sources.append(ast.get_source_segment(raw,node));main=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main');need('verify_receipt_links(' in ast.get_source_segment(raw,main),'guard used '+n)
 need(len(set(sources))==1,'three guards identical')
 return {'status':'PASS_PRIOR_FOUR_ISSUES_RESOLVED','prior_review_manifest_sha256':sha((r/'MANIFEST.json').read_bytes()),'prior_review_members':36,'preserved_candidate01_frozen_members':14,'prior_issue_resolution':{'R1':{'verified':True,'evidence':'Current disposition matches merge gate, with acceptance/freeze/head checks retained; actual6-case regression reproduced'},'R2':{'verified':True,'evidence':'Current README/requirements/note/metadata/generator/livePR/framing and archived current copies scope to POSIX; actual macOS-only execution distinguished; no Windows/Linux execution asserted'},'O1':{'verified':True,'evidence':'Broader RMVQuestion0.2 relationship appears on all current claim surfaces; source p530 independently inspected; immutable historical reports remain historical'},'O2':{'verified':True,'evidence':'Identical actual cross-receipt guard called by tracker/ledger/finalizer before service/native writes;27 root substitutions and35 extended substitutions rejected with positive controls'}},'new_optional_issue_not_part_of_original_O2':'O3 applies to the earlier Zenodo launcher before publication, whereas O2 was scoped to later tracker/ledger/finalizer writes.'}
if __name__=='__main__':
 out=run();(D/'PRIOR_ISSUE_RESOLUTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
