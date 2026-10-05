"""Prepare an authoritative scope correction, preserving frozen historical proofs."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
A=Path(__file__).resolve().parent;S=A/'snapshot/problems/30000590_group_ring_cohomology';D=A/'tmp/scope_repaired_packet'
shutil.copytree(S,D,dirs_exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
correction='''# Current finite-graph scope correction

This is the authoritative current reading of the incidental graph-of-groups statement in historical TURN_2.md, section4. It supersedes its phrase “general graph” and the earlier review's claim that no mathematical wording repair was needed. All historical author/reviewer bytes remain available unchanged. The original question is still unresolved by this packet, five substantive author turns completed.

**Correct statement:** the fundamental group of a **finite graph** of groups, all of whose vertex and edge groups admit finite-length resolutions of the trivial integral module by finitely generated projectives, admits such a resolution too. A uniform finite-orbit projective tree-resolution hypothesis is an equivalent sufficient formulation. No claim for an arbitrary infinite underlying graph is intended.

Proof: the Bass–Serre tree's augmented cellular sequence has a direct sum of induced vertex modules in degree0 and induced edge modules in degree1. For a finite graph these sums are finite. Replace the stabilizer modules by their induced finite projective resolutions and lift the edge incidence map. Its mapping cone is a finite-length resolution by finitely generated projectives resolving the trivial group module. Freeness of the group ring over each stabilizer ring preserves exactness and projectivity. There are finitely many finite resolution lengths, so the total length is bounded.

The finiteness hypothesis cannot be removed: a graph with one trivial vertex group and countably many trivial loop edge groups has fundamental group the free group on countably many generators. Its abelianization is the free abelian group of countably infinite rank, so the group is not finitely generated and is not FP1, hence not finite-length FP. Every stabilizer in that example is nevertheless finite-length FP. This is a counterexample to the historical broad explanatory sentence, not to the original group-ring cohomology question, since the resulting group fails its hypothesis.

The single ascending HNN and finite free-product theorems in TURN_2 already use finite orbit sets and remain supported, with their explicit good-base assumptions. Even for a finite nonascending graph, typeFP alone does not make every intermediate right regular cohomology kernel finitely generated. Neither this correction nor the source's known positive classes closes the arbitrary augmentation-resolution kernel, integral Tor or multicolumn extension gaps.

The coefficient and FP conventions remain total integral RIGHT ZG-module finite generation, with a finite-length trivial LEFT ZG-projective augmentation resolution. Keep both existing additive source locators: Sharifi Theorem4.3.12 on printed/PDF97; Davis FP definition on printed229/physical233. Computational replay verifies historical arithmetic identities; it is not a proof of a universal graph statement or of novelty. AI tools were used extensively; this is unrefereed and is not external human peer review. No sixth author search, paper, DOI or release is created.
'''
(D/'CURRENT_SCOPE_CORRECTION.md').write_text(correction)
cm={'utc':t,'target_id':30000590,'original_frozen_head':'90794508688ec07f598e0871bbd1eb38aaf466ce','current_authoritative_scope':'finite underlying graph in historical TURN2 section4; main scoped results unchanged','original_status':'unsolved','turns':'5/5','historical_files_preserved':True,'files':[{'path':'CURRENT_SCOPE_CORRECTION.md','bytes':len((D/'CURRENT_SCOPE_CORRECTION.md').read_bytes()),'sha256':sha((D/'CURRENT_SCOPE_CORRECTION.md').read_bytes())}]}
(D/'CURRENT_SCOPE_MANIFEST.json').write_text(json.dumps(cm,indent=2)+'\n')
status=(D/'PUBLICATION_STATUS.md').read_text()
status=status.replace('A complete independent AI-assisted source/proof audit passed all five turns. It requested only a bibliographic page correction, supplied additively.', 'The historical AI-assisted review passed the five scoped turns and supplied a bibliographic locator correction. The descending audit additionally found that the incidental graph-of-groups generalization needs a finite underlying graph; the authoritative CURRENT_SCOPE_CORRECTION.md supplies the corrected theorem, proof and infinite-graph counterexample.')
status=status.replace('Start with [RESULT.md](RESULT.md), then the five proofs and [the full review](review/ADVERSARIAL_REVIEW.md).','Start with [the authoritative scope correction](CURRENT_SCOPE_CORRECTION.md), then [RESULT.md](RESULT.md), the five historical proofs and [the historical review](review/ADVERSARIAL_REVIEW.md). Read the broad historical TURN_2 section4 claim only with its finite-graph qualification.')
status=status.replace('this additive wrapper gives the current disposition.','this current wrapper supplies the corrected scoped interpretation; exact-head acceptance review remains pending.')
(D/'PUBLICATION_STATUS.md').write_text(status)
code=(D/'verify_publication.py').read_text()
addition=f"\n# Current scope correction is additional to the immutable historical packet.\nassert hashlib.sha256((d/'CURRENT_SCOPE_MANIFEST.json').read_bytes()).hexdigest()=={sha((D/'CURRENT_SCOPE_MANIFEST.json').read_bytes())!r}\nfor f in json.loads((d/'CURRENT_SCOPE_MANIFEST.json').read_bytes())['files']:\n b=(d/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']\n"
code=code.replace("cmd=[sys.executable,str(d/'verify_packet.py')]",addition+"\ncmd=[sys.executable,str(d/'verify_packet.py')]")
code=code.replace('original unsolved 5/5','current finite-graph qualification bound; original unsolved 5/5')
(D/'verify_publication.py').write_text(code)
pm=json.loads((D/'PUBLICATION_MANIFEST.json').read_text());pm['current_scope_correction']='CURRENT_SCOPE_CORRECTION.md';pm['historical_author_and_review_bindings_preserved']=True
for e in pm['files']:
 b=(D/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
for name in ['CURRENT_SCOPE_CORRECTION.md','CURRENT_SCOPE_MANIFEST.json']:
 b=(D/name).read_bytes();pm['files'].append({'path':name,'bytes':len(b),'sha256':sha(b)})
pm['files'].sort(key=lambda e:e['path']);(D/'PUBLICATION_MANIFEST.json').write_text(json.dumps(pm,indent=2)+'\n')
changed=[str(f.relative_to(S)) for f in S.rglob('*') if f.is_file() and f.read_bytes()!=(D/f.relative_to(S)).read_bytes()]
assert set(changed)=={'PUBLICATION_STATUS.md','PUBLICATION_MANIFEST.json','verify_publication.py'},changed
proc=subprocess.run([sys.executable,'-B',str((D/'verify_publication.py').absolute())],capture_output=True,cwd=D)
(A/'root_scope_repaired_publication.stdout').write_bytes(proc.stdout);(A/'root_scope_repaired_publication.stderr').write_bytes(proc.stderr);assert proc.returncode==0 and not proc.stderr,proc.stderr.decode()
receipt={'utc':t,'original_head':cm['original_frozen_head'],'private_packet':str(D.absolute()),'original_files_preserved_except_current_wrappers':changed,'new_files':['CURRENT_SCOPE_CORRECTION.md','CURRENT_SCOPE_MANIFEST.json'],'all_historical_author_and_review_bytes_unchanged':True,'current_all_target_files':len([x for x in D.rglob('*') if x.is_file() and '__pycache__' not in x.parts]),'current_publication_complete_replay_exit':0,'complete_stdout_sha256':sha(proc.stdout),'math_repair':'finite graph required; independent infinite bouquet counterexample supplied','status':'unsolved','turns':'5/5','workflow_percent':75,'publication_branch_head_pending':True,'fresh_whole_package_gate_pending':True}
(A/'scope_repair_preparation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
