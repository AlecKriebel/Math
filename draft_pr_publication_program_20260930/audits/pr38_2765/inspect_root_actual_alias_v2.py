#!/usr/bin/env python3
"""Root's independent full byte/topology/JSON inspection of actual alias v2.

Reads evidence only; writes its own new inspection. Does not execute any
candidate builder or mathematical verifier. Scientific assessment is the
separate already-read root certificate and independent source-first reviews.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath

A = Path(__file__).resolve().parent
S = lambda b: hashlib.sha256(b).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(rows):
    result = {}
    for k, v in rows:
        require(k not in result, 'Duplicate JSON key: '+k)
        result[k] = v
    return result

def load(raw):
    return json.loads(raw, object_pairs_hook=pairs)

def read(path):
    require(path.is_file() and not path.is_symlink(), 'Nonregular file '+str(path))
    require(all(not p.is_symlink() for p in path.parents), 'Symlink ancestor')
    return path.read_bytes()

def bound(name, expected):
    raw = read(A/name)
    require(S(raw) == expected, 'Changed pinned evidence: '+name)
    return raw

def rows(root, manifest, field='files', exclusions=()):
    found = {}
    for row in manifest[field]:
        name = row['path']; pp = PurePosixPath(name)
        require(type(name) is str and name and not pp.is_absolute() and '..' not in pp.parts and pp.as_posix()==name, 'Unsafe member')
        require(name not in found, 'Duplicate member')
        size = row['bytes'] if 'bytes' in row else row['size']
        require(type(size) is int and size >= 0 and type(row['sha256']) is str and len(row['sha256'])==64, 'Untyped member')
        raw = read(root/name)
        require(len(raw)==size and S(raw)==row['sha256'], 'Full member mismatch: '+name)
        found[name] = raw
    actual = set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if any(PurePosixPath(name).parts[0]==x for x in exclusions):
            continue
        require(not path.is_symlink(), 'Symlink in exact closure')
        if path.is_file(): actual.add(name)
        else: require(path.is_dir(), 'Special file in exact closure')
    require(actual == set(found)|{manifest['_self']}, 'Wrong exact recursive closure')
    return found

def main():
    v1raw = bound('reviewed_candidate/MANIFEST.json', '054b156eb6d44903eadeffeda2012a23c68db530b514294830cc0f45c7b93912')
    v2raw = bound('reviewed_candidate_v2/MANIFEST.json', 'b48e3e17b884056143a7132fd519872ac5223a0ef15fa4bb3d5738e3f58bb52c')
    v1m, v2m = load(v1raw), load(v2raw)
    require(v1m['self_excluded']==v2m['self_excluded']==['MANIFEST.json'], 'Exact root self exclusion')
    v1m['_self']=v2m['_self']='MANIFEST.json'
    old = rows(A/'reviewed_candidate', v1m)
    new = rows(A/'reviewed_candidate_v2', v2m)
    require(len(old)==1499 and len(new)==1502, 'Exact candidate counts')
    changed = {n for n in old if old[n]!=new.get(n)}
    added = set(new)-set(old)
    require(changed=={'README.md','CURRENT_CONTEXT.md'} and added=={'review/REVIEW.md','V1_MANIFEST.json','V2_ALIAS_RECEIPT.json'}, 'Only approved delta')
    notice = read(A/'acceptance_preparation_family/alias_source_revision/ARCHIVAL_NOTICE_APPEND.txt')
    require(len(notice)==896 and all(new[n]==old[n]+notice for n in changed), 'Exact two notice appends')
    require(new['review/REVIEW.md']==old['original_archive/review/REVIEW.md'], 'Exact historic review alias')
    require(new['V1_MANIFEST.json']==v1raw, 'Exact archived v1 manifest')
    expected = read(A/'acceptance_preparation_family/alias_source_revision/EXPECTED_V2_MANIFEST.json')
    require(expected==v2raw, 'Entire deterministic v2 manifest mismatch')
    require(new['V2_ALIAS_RECEIPT.json']==read(A/'acceptance_preparation_family/alias_source_revision/EXPECTED_V2_ALIAS_RECEIPT.json'), 'Entire derived alias receipt mismatch')
    require(load(new['V2_ALIAS_RECEIPT.json'])['actual_execution_attested'] is False, 'Derived receipt cannot attest execution')
    depraw = bound('reviewed_candidate_v2/CURRENT_PROOF_DEPENDENCIES.json', '1b9d41f102cf3345777f4b77c5c5ffbf2db1084d82b6ce8b4a7fb8b5b4af2e79')
    deps = load(depraw); seen = set()
    for row in deps['files']:
        n=row['path']; require(n not in seen, 'Duplicate dependency'); seen.add(n)
        pp=PurePosixPath(n)
        require(not pp.is_absolute() and '..' not in pp.parts and pp.as_posix()==n, 'Unsafe dependency')
        size=row['bytes'] if 'bytes' in row else row['size']; raw=read(A/n)
        require(type(size) is int and len(raw)==size and S(raw)==row['sha256'], 'Whole dependency differs')
    require(len(seen)==1472, 'Exact dependency count')
    support_name='root_closed_families_actual_reproduction_support/ROOT_SUPPORT_MANIFEST.json'
    supportraw=bound(support_name,'d57da3447c0a2533dc41f461fc60625ab271577abe9ddf7b06857237193117bf')
    support=load(supportraw); support['_self']='ROOT_SUPPORT_MANIFEST.json'
    supported=rows(A/'root_closed_families_actual_reproduction_support',support)
    require(len(supported)==1269, 'Exact support count')
    badinventory=load(bound('ROOT_CURRENT_PACKET_INSPECTION.json','2990f443a4bc969215f7fa6c1b7cb8e9ca1d0e615791e1833ffec7e7a2213afa'))
    bad={r['path']:r for scope in badinventory['malformed_exceptions_exact_control_pins'] if scope['scope']=='current' for r in scope['pins']}
    require(len(bad)==12,'Exactly12 specifically pinned negative inputs')
    parsed=0; malformed=[]
    for n,raw in {**new,'MANIFEST.json':v2raw}.items():
        if not n.endswith('.json'): continue
        try: load(raw); parsed+=1
        except (ValueError,UnicodeError):
            require(n in bad and len(raw)==bad[n]['bytes'] and S(raw)==bad[n]['sha256'],'Unqualified malformed JSON: '+n)
            malformed.append(bad[n])
    require(parsed==456 and len(malformed)==12,'Exact full JSON coverage')
    closed = []
    for name,sha,exclusions,count in [
        ('whole_current_source_first_family','9f581a31a7514ff6c1ebe30301c4efbb30adaf67a1cf4b8c85d926130a769e10',('primary_text',),12),
        ('whole_current_alias_followup_family','3afb995feb3de8d62406cef0b772f0c18a6c5128543a731d8e7a29617592d37a',(),14),
        ('whole_current_alias_source_revision','3ef1b8341556d005097c9982edeaa532aa673dfd006d2b9feef1ef949d971c5d',(),4)]:
        raw=bound(name+'/FAMILY_MANIFEST.json',sha); manifest=load(raw); manifest['_self']='FAMILY_MANIFEST.json'
        members=rows(A/name,manifest,exclusions=exclusions); require(len(members)==count,'Exact independent review closure')
        closed.append({'path':name+'/FAMILY_MANIFEST.json','sha256':sha,'members':count})
    capture_raw=bound('root_v2_alias_actual_capture/CAPTURE.json','b4263832f38ca641e262919cb74aabe18d83693a7d2d41a43d1b2c7b265c7309')
    capture=load(capture_raw)
    require(capture['actual_execution'] is True and capture['completed'] is True and type(capture['exit_code']) is int and capture['exit_code']==0 and type(capture['pid']) is int and capture['pid']==40932,'Genuine actual capture')
    src=read(A/'root_v2_alias_actual_capture/prelaunch_source.py')
    require(S(src)==capture['source_sha256']=='c30a30983e3d26f36b2ca055177a0445b26870deb0085082eb6d7f44db554210','Prelaunch whole source')
    streams={}
    for label in ('stdout','stderr'):
        row=capture[label]; raw=read(A/'root_v2_alias_actual_capture'/row['path'])
        require(type(row['size']) is int and len(raw)==row['size'] and S(raw)==row['sha256'],'Complete actual stream')
        streams[label]=raw
    require(not streams['stderr'] and len(streams['stdout'])==588,'Actual clean complete streams')
    emitted=load(streams['stdout'])
    require(emitted['status']=='ACTUAL_ADMINISTRATIVE_V2_ALIAS_BUILD_COMPLETE','Actual emitted status')
    assessment=load(read(A/'whole_current_alias_followup_family/ASSESSMENT.json'))
    result={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS',
      'inspection_kind':'root independent full byte topology JSON delta and actual administrative capture inspection; no scientific rerun',
      'actual_v2_manifest_sha256':S(v2raw),'actual_v2_members':1502,'old_v1_manifest_sha256':S(v1raw),'old_v1_members':1499,
      'unchanged_original_members':1497,'changed_existing_members':sorted(changed),'added_members':sorted(added),
      'dependency_manifest_sha256':S(depraw),'dependencies':1472,'support_manifest_sha256':S(supportraw),'support_members':1269,
      'valid_JSON_including_manifest':parsed,'exact_malformed_negative_inputs':malformed,
      'root_actual_alias_capture':capture,'whole_actual_stdout_JSON':emitted,'closed_independent_reviews':closed,
      'independent_actual_v2_assessment':assessment,'root_full_current_read_completed':True,
      'scientific_reading_qualification':'All changed prose/source/capture/report read semantically; unchanged science retains earlier detailed root primary and proof reading, original actual12/108/2 reproduction, and source-first whole review. Full byte traversal is distinguished from new semantic reading.',
      'full_problem_solved':False,'partial_valid':True,'original_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,
      'mandatory_corrections_remaining':[],'final_integration_gate':'PENDING'}
    out=A/'ROOT_V2_ALIAS_INSPECTION.json'; require(not out.exists(),'Preserve prior inspection')
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS','inspection_sha256':S(out.read_bytes()),'members':1502,'dependencies':1472,'support':1269,'valid_JSON':parsed}))

if __name__=='__main__':
    main()
