#!/usr/bin/env python3
"""Prepare a reviewable credited correction; no Git or external mutation."""
from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent;D=A/'priority_correction_packet_v02';D.mkdir(exist_ok=False)
T='problems/30004365_gentle_derived_invariant'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  if p.parent!=D/'target' or p.name not in ['README.md','DISPOSITION.md','PUBLIC_SCOPE.json','PUBLIC_MANIFEST.json']:raise RuntimeError('Unexpected prepared overwrite '+str(p))
  p.chmod(0o644)
 p.write_bytes(b);p.chmod(0o444)
def json_write(p,o):write(p,(json.dumps(o,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
M=json.loads((A/'snapshot_manifest.json').read_text());G=json.loads((A/'ROOT_PRIORITY_ADJUDICATION.json').read_text())
if M['head']!='125d90fa3f5a4f90b813fec7a7c0f1918914d885' or M['original_submitted_status']!='claimed_solved' or G['adjudicated_operational_status']!='already_solved':raise RuntimeError('input outcome')
original={}
for e in M['files']:
 if not e['path'].startswith(T+'/'):continue
 name=e['path'][len(T)+1:];b=(A/'snapshot'/e['path']).read_bytes()
 if sha(b)!=e['sha256'] or len(b)!=e['bytes']:raise RuntimeError('original body '+name)
 original[name]=b
 write(D/'target'/name,b);write(D/'target/history/original_submission'/name,b)
if len(original)!=17:raise RuntimeError('17 originals')
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
readme='''# Gentle derived invariants: credited effectivity proof and priority correction

**30004365 / OWR-17466-004: already_solved by prior constructive mechanisms; author1/5. Corrected mathematics accepted; a new open-problem resolution is not claimed.**

[Current status](CURRENT_STATUS.json) and [priority finding](CURRENT_PRIORITY_NOTE.md) are authoritative. The exact [corrected proof](CURRENT_CORRECTED_PROOF_v02.md) computes the known complete invariant using a terminating rational PL certificate search, every boundary and puncture end, and the credited LP/APS classifier. Its header records its write-time pending-review state; the current status records its subsequent acceptance. No efficiency bound or full implementation is claimed.

QPA disclosed constructive numerical methods in2024 and released them inMay2025. Exact March2025 String Applet code already computes gcd, parity, Arf and the puncture witness. Earlier general topology algorithms also compute geometric handle pairs; a finite all-end conversion gives the theoretical gentle procedure from older credited inputs. Prior software has exhibited local defects and is not universally certified. Priority of the particular PL certificates and explicit APS range correction remains unknown; neither is promoted as a first solution. The priority note gives primary sources, dates, deductions and exact limits.

The corrected proof repairs the APS printed puncture-winding range by using all compact-core ends directly under LP. It also truncates original boundary collars as well as punctures before enumerating curves. Three initial mathematical families and a fresh corrected-proof adversary passed; ROOT reproduced46068 fresh checks, the original1328/32291 controls, and other supporting controls. The general halting and classification claims rest on written proofs, not finite samples.

The complete original17-file submission is byte-preserved in [history/original_submission](history/original_submission/README.md), including author and inherited-review manifests. Thirteen original files remain unchanged at their old paths; only README, DISPOSITION, PUBLIC_SCOPE and PUBLIC_MANIFEST are current wrappers. Original TURN_1, SOURCE_GATE, FROZEN_MANIFEST, REMOTE_SCOPE and inherited reviews are historical records, and their old status/readback/hash references refer to that submitted packet. The archived manifests resolve relative paths within history/original_submission, with the same deliberately omitted source inputs as before. [Current manifest](PUBLIC_MANIFEST.json) binds all files in this corrected public packet except itself. No copyrighted source PDFs or applet bundles are included.

Research and verification used AI tools extensively. This is unrefereed, without human peer review or formal proof verification. Under the user's current claimed_solved-only scope, this priority-corrected already_solved PR remains a draft, unmerged and unclosed, with no preprint, Zenodo upload, DOI, tracker row or release.
'''
write(D/'target/README.md',readme.encode())
proof=(A/'CURRENT_CORRECTED_PROOF_v02.md').read_bytes()
if sha(proof)!='d92a870709f5ce62440fa8a83313dd13790773f247e01cfb63c43c5ae8ea272a':raise RuntimeError('accepted proof pin')
write(D/'target/CURRENT_CORRECTED_PROOF_v02.md',proof)
note=(A/'ROOT_PRIORITY_FINDING.md').read_text()
note=note.replace('priority_effectivity_02/CANONICAL_TO_HANDLE_DERIVATION.md','review/PRIOR_TOPOLOGY_DERIVATION.md')
note=note.replace('The\nremaining work is a fresh review and verified publication of that correction,\nfollowed by descending intake of the next originally claimed_solved PR.','The current package records this outcome correction; its separate fresh review and exact branch publication must be verified before the audit is marked complete.')
write(D/'target/CURRENT_PRIORITY_NOTE.md',note.encode())
for src,dest in [('priority_effectivity_02/CANONICAL_TO_HANDLE_DERIVATION.md','PRIOR_TOPOLOGY_DERIVATION.md'),('priority_algorithm_01/DERIVATION_DIRECT_METHOD.md','PRIOR_NUMERICAL_DERIVATION.md'),('priority_adversary_03/INDEPENDENT_DERIVATION.md','PRIOR_ADVERSARIAL_DERIVATION.md'),('priority_algorithm_01/REPORT.md','PRIORITY_ALGORITHM_REPORT.md'),('priority_effectivity_02/REPORT.md','PRIORITY_EFFECTIVITY_REPORT.md'),('priority_adversary_03/REPORT.md','PRIORITY_ADVERSARIAL_REPORT.md')]:
 write(D/'target/review'/dest,(A/src).read_bytes())
status={'UTC':stamp,'problem_id':30004365,'status':'already_solved','original_submitted_status':'claimed_solved','original_submitted_head':M['head'],'turns_completed':1,'author_turns':'1/5','mathematical_acceptance':True,'corrected_proof_sha256':sha(proof),'priority_audit_accepted':True,'new_open_problem_resolution_cleared':False,'priority_qualification':G['exact_priority_qualification'],'exact_certificate_and_correction_priority':'UNKNOWN','universal_prior_software_correctness':'Not certified; concrete defects retained','current_priority_note':'CURRENT_PRIORITY_NOTE.md','historical_submission':'history/original_submission/','mathematical_percent':100,'bounded_priority_audit_percent':100,'packet_review_pending':True,'actual_branch_publication_pending':True,'workflow_percent':60,'paper':False,'preprint_ready':False,'Zenodo':False,'DOI':None,'tracker_row':False,'merge':False,'close':False,'human_peer_review':False,'formal_proof_verification':False,'AI_tools_used_extensively':True}
json_write(D/'target/CURRENT_STATUS.json',status)
scope=json.loads(original['PUBLIC_SCOPE.json']);scope.update(status='already_solved',claim='Credited certificate-based computation of the known complete gentle invariant; broad new-resolution priority defeated',original_submitted_status='claimed_solved',original_submitted_head=M['head'],historical_submission_directory='history/original_submission/',current_authority=['CURRENT_STATUS.json','CURRENT_PRIORITY_NOTE.md','CURRENT_CORRECTED_PROOF_v02.md'],current_workflow='Leave draft unmerged/unclosed under claimed-only scope after one outcome correction',paper=False,Zenodo=False,DOI=None,tracker=False,universal_prior_software_correctness_certified=False,particular_certificate_and_correction_novelty='UNKNOWN')
json_write(D/'target/PUBLIC_SCOPE.json',scope)
disposition='''# Current disposition: credited prior result, author1/5

2026-10-05. Operational outcome **already_solved**. The corrected certificate construction has passed adversarial mathematical review and ROOT reproduction. Earlier QPA and String Applet sources disclose the central numerical methods, and an exact composition of older topology/PPP/APS/LP results covers the theoretical task. A new2026 resolution is not cleared. This finding does not certify every prior software input or an unavailable thesis theorem; specific PL-certificate/correction priority remains unknown.

Read CURRENT_STATUS.json, CURRENT_PRIORITY_NOTE.md and CURRENT_CORRECTED_PROOF_v02.md for the current acceptance, proofs, primary evidence and qualifications. Original author/inherited-review artifacts and the original1/5 turn count are preserved, including all17 original files in history/original_submission. Original labels are historical. The current manifest binds this corrected packet.

Extensive AI assistance; unrefereed, without human peer review or formal proof verification. Following the user's later claimed_solved-only scope, after this correction leave the PR a draft, unmerged/unclosed, with no paper, Zenodo upload, DOI, tracker row or release. Fresh corrected-packet review and exact branch/readback verification remain pending at preparation time.
'''
write(D/'target/DISPOSITION.md',disposition.encode())
manifest={'problem_id':30004365,'UTC':stamp,'status':'already_solved','original_submitted_head':M['head'],'original_files_preserved':17,'unchanged_original_files_at_old_paths':13,'current_wrappers':['README.md','DISPOSITION.md','PUBLIC_SCOPE.json','PUBLIC_MANIFEST.json'],'historical_manifest_resolution':'history/original_submission/; original omitted references remain omitted','self_exclusion':'PUBLIC_MANIFEST.json excluded to avoid recursion','files':[]}
for p in sorted((D/'target').rglob('*')):
 if p.is_file() and p!=D/'target/PUBLIC_MANIFEST.json':manifest['files'].append({'path':str(p.relative_to(D/'target')),**pin(p)})
json_write(D/'target/PUBLIC_MANIFEST.json',manifest)
body='''## Priority-corrected outcome: already_solved, author1/5

The corrected rational PL certificate proof passes mathematical review and computes the known complete gentle derived invariant, retaining every boundary and puncture end. The audit repairs the printed APS puncture-winding range and original-boundary compact-core domain. The original submission and author1/5 history are preserved.

A deep primary-source priority audit found constructive numerical methods in QPA2024/release2025 and the exact March2025 String Applet. ROOT reproduces its gcd, parity, Arf and puncture examples. Older geometric handle algorithms plus a finite end conversion independently give the theoretical computation from credited existing results. The broad new-resolution claim is therefore withdrawn. Prior programs have concrete local defects and are not universally certified; priority of this particular certificate proof or explicit correction is unknown. No theorem is inferred from the unavailable Winspeare thesis.

The current README/status/disposition/scope/manifest and additive corrected proof/priority note make this outcome authoritative. All17 original public files are preserved in history/original_submission;13 remain unchanged at their old paths. Supporting mathematical/priority derivations and independent reports accompany the correction. Original pending-review/status/readback references are historical.

Research and verification used AI tools extensively; unrefereed, without human peer review or formal proof verification. Under the user's current claimed_solved-only process, this corrected already_solved draft remains unmerged/unclosed, without a preprint, Zenodo upload, DOI, tracker row or release.
'''
write(D/'PR_BODY.md',body.encode());write(D/'PR_TITLE.txt',b'30004365: credited gentle-invariant effectivity proof; priority correction (already_solved, 1/5)\n')
json_write(A/'PRIORITY_CORRECTION_PREPARATION.json',{'UTC':stamp,'actual_preparer_PID':os.getpid(),'source':pin(Path(__file__)),'status':'PREPARED_CREDITED_CORRECTION_NO_GIT_OR_PUBLIC_MUTATION','pr':301,'original_head':M['head'],'packet':str(D),'target_prefix':T,'prepared_files':[{'path':str(p.relative_to(D)),**pin(p)} for p in sorted(D.rglob('*')) if p.is_file()],'all17_original_bodies_preserved':True,'13_originals_unchanged_at_old_paths':True,'author_turns':'1/5','fresh_review_pending':True,'private_commit_pending':True,'public_correction_pending':True,'workflow_percent':60,'paper':False,'merge':False,'close':False,'Zenodo':False,'tracker':False})
print(json.dumps({'status':'PREPARED_CREDITED_CORRECTION_NO_GIT_OR_PUBLIC_MUTATION','target_files':len(list((D/'target').rglob('*'))),'manifest_entries':len(manifest['files']),'author_turns':'1/5','workflow_percent':60}))
