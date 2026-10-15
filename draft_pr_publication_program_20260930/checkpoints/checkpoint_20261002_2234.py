"""Publish only exact owned closed work; keep foreign and active work excluded."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930';A=P/'audits'
owned=set();closures=[]
def H(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],cwd=R)
def add(p):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    owned.add(p.relative_to(R).as_posix())
def tree(p):
    for f in p.rglob('*'):
        assert not f.is_symlink()
        if f.is_file(): add(f)
def manifest(p,pin):
    b=p.read_bytes();assert H(b)==pin
    m=json.loads(b);seen=set()
    for z in m['files']:
        n=z['path'];assert n not in seen and not n.startswith('/') and not set(n.split('/'))&{'','.','..'};seen.add(n)
        f=p.parent/n;raw=f.read_bytes();assert type(z.get('bytes',z.get('size'))) is int and len(raw)==z.get('bytes',z.get('size')) and H(raw)==z['sha256'];add(f)
    add(p);closures.append(dict(path=p.relative_to(R).as_posix(),sha256=pin,members=len(seen)))
assert git('branch','--show-current').strip()==b'main'
assert git('rev-parse','HEAD').strip()==b'2e98e667acc47f2455533e09256eba921748128a'
assert not git('diff','--cached','--name-only').strip()
for rel,pin in [
 ('pr39_9500008/root_runner_revision_preparation_family/MANIFEST.json','a93237f6ecaf652942374fcb2829a534ee8edbb8d29f44c41b047a58bc15fef9'),
 ('pr39_9500008/runner_static_adversary_family/MANIFEST.json','113dc34e8396ace4069d221f1f702f922e2797195a6a14c0709bd9b5ceee536c'),
 ('pr39_9500008/final_evidence_reconciliation/FINAL_MANIFEST.json','f64775f4397c18e7e8ce7385564f56579d307db21c5c1decb7640ed5c77ef1b7'),
 ('pr40_2814/acceptance_execution_preparation_family/integration_source_revision_v2/PREPARATION_MANIFEST.json','e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba'),
 ('pr40_2814/acceptance_revised_static_adversary_family/FIRST_PARTY_MANIFEST.json','0480281a6dd9629183d1d7e2ad98b098a3b5eae8b8b423dbc4bc72eda85403cf'),
 ('pr40_2814/acceptance_revised_static_adversary_metadata_qualification_family/FIRST_PARTY_MANIFEST.json','bc05c4971ee61d50080005ce2084597098c97acc8a11f66d95d08514524cb8bb'),
 ('pr40_2814/acceptance_v2_publication_adversary_family/FIRST_PARTY_MANIFEST.json','0fe8459862fa6f651482ad967179ddd4c13b8801356c1123167ffa74c4718fa8'),
 ('pr40_2814/root_runner_preparation_family/MANIFEST.json','aa58d2e3a9f470c6ce8d2781e47c72605de8338ee6766bb390a7f57ab7f42d50'),
 ('pr41_9700035/current_preparation_family/PREPARATION_MANIFEST.json','bc6412589fa2d94c3728247735319cf980440cc976d609c138a6bbb3c0aa9e13'),
 ('pr41_9700035/reviewed_candidate/MANIFEST.json','3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'),
 ('pr41_9700035/whole_current_source_first_family/FIRST_PARTY_MANIFEST.json','233867cfb7e18b910f1ec17c9a57a386eadd1793ff3a44328260e204d8304130')]: manifest(A/rel,pin)
manifest(R/'unsolved_math_prioritization/attempts/9500008/MANIFEST.json','4be9e306fc575da130545c69b3825a5a1d437ed314dbf58eda1beb0a35fd98bf')
# Root39 has no active writer. Direct files and explicitly named root captures
# are first-party; ignoredtmp and arbitrary nested bodies are never selected.
for f in (A/'pr39_9500008').iterdir():
    if f.is_file():add(f)
    elif f.name.startswith('root_') and f.name.endswith('_actual_capture'):tree(f)
tree(A/'pr39_9500008/root_final_inspection_setup_failure')
for n in ['execute_root_acceptance_revised.py','ROOT_RESEARCH_LOG.md']:add(A/'pr40_2814'/n)
parent=A/'pr40_2814/acceptance_execution_preparation_family'
for n in ['prepare_integration_revision.py','prepare_integration_revision_v2.py','prepare_root_runner_package.py']:
    if (parent/n).exists():add(parent/n)
for n in ['prepare_revision_actual_capture','prepare_revision_v2_actual_capture','prepare_root_runner_package_actual_capture']:
    if (parent/n).exists():tree(parent/n)
for n in ['ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_CURRENT_PACKET_INSPECTION.json','ROOT_SCIENCE_CARD.json','execute_root_current_freeze.py','inspect_current_packet.py','prepare_root_current_prerequisites.py','inspect_whole_current_review.py','inspect_whole_current_review_v2.py','ROOT_WHOLE_CURRENT_REVIEW.json','ROOT_RESEARCH_LOG.md']:add(A/'pr41_9700035'/n)
tree(A/'pr41_9700035/root_current_freeze_actual_capture')
for n in ['state.json','history.jsonl']:add(R/'unsolved_math_prioritization'/n)
add(P/'inventory.json');add(P/'RESEARCH_LOG.md');add(Path(__file__).resolve())
now=dt.datetime.now(dt.timezone.utc).isoformat()
notes={
 'pr39_9500008':'Acceptance100%; full problem unresolved, discovery0%. Original-head merge2e98e667/remoteMERGED verified. Finalactual43918, preflight46331, overlay49076, prepush51008, push54977, finalize56680, mirror64208, post69773 and own post inspection82389 all genuine; full2912 canonical/real tree/native13/wholeprior29states/historyprefix verified. Exactly one present event, no new attempts; original2/5. Program29/180=16.1111%. No paper/newDOI/tracker.',
 'pr40_2814':'Acceptance95%; conservative sourcehold partial valid, discovery0%. ROOT found operational S7 ignoredcache3 Git-absence defect missed by earlier static PASS. New17+self v2e5f0 preserves earlier closures and narrows tracked10/9 plus exact absentcache3; new42+self source/wrapper adversary0fe845 is qualifiedclean, with its own failed inspector retained. No actual40 execution/futurePASS. Original0/5,new0/audit0; root complete new wrapper reading pending.',
 'pr41_9700035':'Scientific/current audit90%, full original discovery0%. Current547freezePID36236 and NEWwhole143/foreign17 closure233867 are verified. ROOT full whole result/report/source/proof reading and genuine inspection83976 PASS bind completeverdict and469dependencies. Own failed83631 administrative bytes-vs-size overrequirement preserved and corrected in separatev2, no candidate defect. Conditional tail result valid; ordinaryaxiom exterior gap unresolved. Original2/5,new0/audit0. Acceptance source preparation active excluded.'}
for folder,note in notes.items():
    with (A/folder/'ROOT_RESEARCH_LOG.md').open('a') as out:out.write('\n'+now+' — '+note+'\n')
with (P/'RESEARCH_LOG.md').open('a') as out:out.write('\n'+now+' — '+' '.join(notes.values())+' PR18/20 evidence holds preserved; PR42 source-first independent families closed, root reproduction pending and excluded. No outside human contact.\n')
records=[dict(path=n,bytes=len((R/n).read_bytes()),sha256=H((R/n).read_bytes())) for n in sorted(owned)]
out=P/'checkpoints/CHECKPOINT_20261002_2234.json'
with out.open('x') as f:json.dump(dict(utc=now,head_before=git('rev-parse','HEAD').decode().strip(),completed=29,total=180,completion_percent=29/180*100,closed_manifests=closures,exact_owned_files=records,excluded='Both unrelated tracked referee logs; active PR41 acceptance prep; PR42 work; all individual foreign source/cache/media bodies. Intentionally empty private fixture directory is retained in manifest metadata but Git cannot represent an empty directory.'),f,indent=2);f.write('\n')
add(out)
names=sorted(owned)
for i in range(0,len(names),100):git('add','-f','--',*names[i:i+100])
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n};assert staged<=owned
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    meta,name=entry.split(b'\t',1);n=name.decode()
    if n not in staged:continue
    mode,oid,stage=meta.split();assert stage==b'0' and mode in (b'100644',b'100755')
    b=(R/n).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
assert all(not n.startswith('paper_ii_') for n in staged)
print(json.dumps(dict(status='EXACT_OWNED_CHECKPOINT_STAGED',members=len(staged),bytes=sum(len((R/n).read_bytes()) for n in staged),completion_percent=29/180*100)))
