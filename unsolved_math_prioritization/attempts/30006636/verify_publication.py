#!/usr/bin/env python3
"""Authenticate frozen trisection TQFT partial results; replay source-free finite checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

ACCEPTED = {'AUTHOR_RELEASE_VALIDATION.public.json': {'bytes': 26239, 'sha256': '62961b79541eb83e7315187f3baecada34f860466ba9285d13a9ea93ac67e5dc'}, 'evidence/AUDIT.md': {'bytes': 15675, 'sha256': 'b52c67fbf041215ed55e3be582e616fa7c20e0c285f11d1d22ea0e4c3fd56b27'}, 'evidence/CONNECTED_Y_CORRECTION.json': {'bytes': 366, 'sha256': '7911d62000055bfde4d2b8cae813509ad229cca486e5e5ea4a0284ed67e36891'}, 'evidence/FIRST_STAGE_AUDIT_MANIFEST.public.json': {'bytes': 2347, 'sha256': '3cdb4fff333854c68dd31c8b941e8c9249c1ce755cb4e4cdb4fec4764a5877a4'}, 'evidence/FIVE_APPROACH_CORRECTION.patch': {'bytes': 1385, 'sha256': '37afc1e7d43775932fd2c8abb4f6ffbaca4f6929c56aa9e278b71c2a9fc2b6c0'}, 'evidence/FIVE_APPROACH_REPORT.md': {'bytes': 16612, 'sha256': 'e3c128de7015148827e998dbc5ac779e4167963dfa0fa1f95650f521244eb79c'}, 'evidence/FOLLOWUP_AUDIT.md': {'bytes': 16726, 'sha256': 'a609b8715aab86b4bc00a41ce30eee0a4fb780cb362a7df36ae4b9f42faf1e29'}, 'evidence/FOLLOWUP_AUDIT_MANIFEST.public.json': {'bytes': 2743, 'sha256': 'ecd4aaa837aeeb48af652d55d27feed4d624a0f16364ed8c613f5b586420d166'}, 'evidence/HARDENING_MANIFEST.public.json': {'bytes': 2527, 'sha256': '5667d9d7c8bd35fbbcb2be5a98ec6c646126de9dfac67b72d2417ca6edab7948'}, 'evidence/HARDENING_RECEIPT.public.json': {'bytes': 36619, 'sha256': '9356b6e6d65ff60efd8f202c531abd98e7a46dcab6ad6ad780d2f497df4f2a55'}, 'evidence/HARDENING_REPORT.md': {'bytes': 5434, 'sha256': '8b740979e6d16d7ae10e61d80dc467cb0e764791ae81417d8e783134e9a63fc8'}, 'evidence/HISTORICAL_check_followup.py.txt': {'bytes': 6811, 'sha256': '9ec96fcbd9ed5a0d0ce5190addab102266d5eeb65a59bc7a9998a40690a8499f'}, 'evidence/HISTORICAL_check_normalization.py.txt': {'bytes': 4502, 'sha256': 'b4a7d72999c4fc0a63a1deee037c15c9f9125378792865aaec616aecac4fc595'}, 'evidence/INDEPENDENT_FOLLOWUP_RESULTS.json': {'bytes': 850, 'sha256': '7c5dc113a61c5af720540a6c3b6b920cf45a5d5f7b31226de024194488ab606c'}, 'evidence/INDEPENDENT_NORMALIZATION_RESULTS.json': {'bytes': 733, 'sha256': '050d9ab1e3fe12cce96e2682a33eb96cea46ae245984a3498a4786cf227a627b'}, 'evidence/PROOF.md': {'bytes': 14820, 'sha256': 'ea1692e3304a67d1051192bfaba974a8aaead3821bd2f38b7826cbfc00d29cf3'}, 'evidence/PUBLIC_SLICE.json': {'bytes': 2822, 'sha256': '21b8e28ee0df95af500dbee425d3d529830070e9cd2a22b7ffb12332265015b1'}, 'evidence/SOURCES.json': {'bytes': 2752, 'sha256': 'e028d6535c8ec75737fd87569817294d353506210b7584be978bf0d50dbb155e'}, 'evidence/check_extensions.py': {'bytes': 9221, 'sha256': '28761575a4b603fd59acd26894c0ce8417f54b5fe1e777236b875c3e6f20bc5e'}, 'evidence/check_followup.py': {'bytes': 10172, 'sha256': 'fda065bb4d900798ec416a6ea9e3337328dcd4c80b9c5eb918d6377c4137a075'}, 'evidence/check_followup.py.patch': {'bytes': 8657, 'sha256': '569be340ba1da8e3ab8d11e8debb6cea4dadb535582072bca1f81a3fff3eb411'}, 'evidence/check_normalization.py': {'bytes': 7739, 'sha256': '224f3300a713b0c7ced2ab60651702d788f7713badf6bccf659665109496eee1'}, 'evidence/check_normalization.py.patch': {'bytes': 7599, 'sha256': 'dc5fa3d1a19a0c61707d431f1c26c7c3cf72f04f738a0946d854e595295d1ac0'}, 'evidence/check_obstruction.py': {'bytes': 8842, 'sha256': '5176dbc947e6a9a56e9df007f7054011d4178392eab98159b80be5de0329a1c5'}, 'expected/check_extensions.py.O.json': {'bytes': 648, 'sha256': 'b8dd0f89aa32fbe600973b9565f8f6234112bb960a8a5c8ea8f9d36d6d9fded7'}, 'expected/check_extensions.py.OO.json': {'bytes': 649, 'sha256': 'b5a6aa084f6b08e69d04098a2ba906463fa28a77043461e24b2e7eaaf835ebb6'}, 'expected/check_extensions.py.normal.json': {'bytes': 652, 'sha256': 'ed258262fbefc89bbdb03731a73a162cead257219746f72d7f40690d854d7430'}, 'expected/check_obstruction.py.O.json': {'bytes': 1200, 'sha256': 'c0b7e72894d0e59c77d588b3f38fbfcd191a3f653ed43938d6bc46bf6e613a3d'}, 'expected/check_obstruction.py.OO.json': {'bytes': 1201, 'sha256': '43da33a00f69349e0d10a29fb4b02b88f0e899a0c09bb1bd34d863f3f02d5e93'}, 'expected/check_obstruction.py.normal.json': {'bytes': 1204, 'sha256': '2a80cea257d2031c053cd9e3c529751535db891ecb52c6b3d8bfe7bea0f2adb7'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'evidence', 'expected'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 30006636)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence bytes changed')
    slice_record=parsed['evidence/PUBLIC_SLICE.json']
    keys(slice_record,['schema','problem_id','role','retained_authored_mathematics_unchanged','unmodified_original_members','contextualized_correction','public_metadata_derivatives','source_documents_or_private_material_included'])
    exact_int(slice_record['schema'],1);exact_int(slice_record['problem_id'],30006636)
    need(slice_record['retained_authored_mathematics_unchanged'] is True and slice_record['source_documents_or_private_material_included'] is False,'public slice scope')
    exact_int(slice_record['unmodified_original_members'],17)
    for row in slice_record['public_metadata_derivatives']:
        keys(row,['path','original','published','arithmetic_outputs_and_accepted_findings_unchanged'])
        need(row['path'] in ACCEPTED and row['arithmetic_outputs_and_accepted_findings_unchanged'] is True,'public metadata derivative')
        data=snapshot[row['path']]
        need(same(row['published'],dict(bytes=len(data),sha256=sha(data))),'public derivative byte binding')
        need(same(parsed[row['path']]['public_derivative']['original'],row['original']),'historical provenance binding')
    contextual=snapshot['evidence/FIVE_APPROACH_CORRECTION.patch']
    preamble=b"Historical correction record: the removed mapping-torus statement is REJECTED\nat its former disconnected-Y scope. It is not an accepted claim. Connectedness\nof Y is mandatory in the replacement and in the current accepted report.\nThe full rejected report is intentionally not distributed. The original exact\nunified correction diff follows unchanged below.\n\n"
    need(contextual.startswith(preamble),'required rejected-scope correction context')
    exact_diff=contextual[len(preamble):]
    correction=slice_record['contextualized_correction']
    need(same(correction,dict(path='evidence/FIVE_APPROACH_CORRECTION.patch',original_diff=dict(bytes=len(exact_diff),sha256=sha(exact_diff)),published=dict(bytes=len(contextual),sha256=sha(contextual)),preamble_bytes=len(preamble))),'contextualized correction exact provenance')
    # The corrected report and contextualized patch are independently pinned.
    # No full rejected report is distributed or reconstructed for public replay.
    added=[line[1:] for line in exact_diff.decode().splitlines() if line.startswith('+') and not line.startswith('+++')]
    need(len(added)==1 and added[0] in snapshot['evidence/FIVE_APPROACH_REPORT.md'].decode().splitlines(),'correction replacement in accepted report')
    need(added[0].startswith('Let Y be a connected closed oriented 3-manifold'),'connectedness mandatory')
    import difflib, ast
    corrections=[('HISTORICAL_check_normalization.py.txt','check_normalization.py','check_normalization.py.patch'),
                 ('HISTORICAL_check_followup.py.txt','check_followup.py','check_followup.py.patch')]
    for old,new,patch in corrections:
        raw=snapshot['evidence/'+patch].decode();lines=raw.splitlines(True)
        need(lines[0].startswith('--- ') and lines[1].startswith('+++ '),'patch headers')
        generated=''.join(difflib.unified_diff(snapshot['evidence/'+old].decode().splitlines(True),snapshot['evidence/'+new].decode().splitlines(True),fromfile=lines[0][4:].rstrip('\n'),tofile=lines[1][4:].rstrip('\n')))
        need(generated==raw,'exact patch reconstruction')
    for name in SPECS:
        tree=ast.parse(snapshot['evidence/'+name]);need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'optimized-away assertion')
    # Historical records are provenance, not fresh source checks or a replacement inventory.
    need(same({k:parsed['AUTHOR_RELEASE_VALIDATION.public.json'][k] for k in ['positive_modes','semantic_mutations_rejected','output_path_or_overwrite_rejections','explicit_external_output_modes']},dict(positive_modes=12,semantic_mutations_rejected=81,output_path_or_overwrite_rejections=36,explicit_external_output_modes=12)),'historical arithmetic control counts')
    return snapshot,parsed


SPECS = {
 'check_obstruction.py':['omit-red-factor','wrong-stabilizer','unbalanced-as-product','round-dimension','euler-sign','nonzero-seam'],
 'check_extensions.py':['drop-closed-color','wrong-product-trace','abelianize-dihedral','allow-negative-multiplicity','accept-noncube','forget-connectedness'],
 'check_normalization.py':['double-raw-product','omit-stabilizer-crossing','omit-heegaard-constraint','wrong-euler-coefficient','wrong-stabilization-genus','wrong-rescaling-power','nonzero-seam'],
 'check_followup.py':['drop-free-closed-color','ignore-conflicting-colors','drop-new-closed-component','wrong-euler-weight','wrong-gram-power','commutative-dihedral-product','wrong-fourier-sign','uniform-component-normalization']
}
BASELINES={'check_normalization.py':'INDEPENDENT_NORMALIZATION_RESULTS.json','check_followup.py':'INDEPENDENT_FOLLOWUP_RESULTS.json'}

def expected_stdout(name,snapshot,mode):
    if name in BASELINES:return snapshot['evidence/'+BASELINES[name]]
    return snapshot['expected/'+name+'.'+['normal','O','OO'][mode]+'.json']


def expected_external(name,snapshot,mode):
    raw=expected_stdout(name,snapshot,mode)
    if name in BASELINES:return raw
    value=parse(raw)
    # The two authored checkers intentionally emit this one different field to
    # describe their explicit-output interface. All other bytes are predetermined.
    need(value['writes']=='stdout only','expected stdout write declaration')
    value['writes']='explicit external destination'
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()


def check_output(raw,expected):
    need(raw==expected,'complete exact output mismatch')


def readonly(root):
    need(os.getuid()==os.geteuid()==1000,'real/effective UID 1000 required')
    for path in [root,*[root/n for n in DIRS],*[root/n for n in FILES],Path.cwd()]:
        need(not os.access(path,os.W_OK),'all input files/directories and cwd must be readonly')
    for path in [root/'NEW_FILE',root/'verify_publication.py',root/'evidence/NEW_FILE',Path.cwd()/'NEW_FILE']:
        try:
            with path.open('ab') as stream:stream.write(b'forbidden')
        except PermissionError:pass
        else:raise ValueError('actual readonly probe succeeded')


def replay(root,snapshot,parsed):
    readonly(root)
    mode=sys.flags.optimize;flags=[] if mode==0 else ['-'+('O'*mode)]
    records=[];historical=[]
    with tempfile.TemporaryDirectory(prefix='tqft-publication-output-') as directory:
        temp=Path(directory)
        env=dict(PATH=os.defpath,HOME=str(temp),TMPDIR=str(temp),LC_ALL='C')
        def call(script,extra=(),cwd=None):
            return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*extra],cwd=cwd or Path.cwd(),env=env,capture_output=True,timeout=180)
        for name,mutations in SPECS.items():
            script=root/'evidence'/name
            expected=expected_stdout(name,snapshot,mode)
            proc=call(script,['--require-readonly'])
            need(proc.returncode==0 and proc.stderr==b'','native positive execution')
            check_output(proc.stdout,expected)
            records.append(dict(checker=name,kind='positive',exit_code=0,stdout_sha256=sha(proc.stdout)))
            for mutant in mutations:
                proc=call(script,['--require-readonly','--mutant',mutant])
                diagnostic=proc.stderr.decode().strip().splitlines()[-1] if proc.stderr else ''
                need(proc.returncode!=0 and proc.stdout==b'' and diagnostic.startswith('RuntimeError:'),'semantic guard rejection')
                historical_record=[x for x in parsed['AUTHOR_RELEASE_VALIDATION.public.json']['runs'] if x['checker']==name and x['mode']==['normal','O','OO'][mode] and x['control']==mutant]
                need(len(historical_record)==1 and diagnostic==historical_record[0]['diagnostic'],'exact semantic diagnostic')
                records.append(dict(checker=name,kind='semantic-mutation',mutant=mutant,exit_nonzero=True,diagnostic=diagnostic))
            destination=temp/(name+'.json')
            proc=call(script,['--require-readonly','--output',str(destination)])
            need(proc.returncode==0 and proc.stdout==b'' and proc.stderr==b'','explicit external output execution')
            external=expected_external(name,snapshot,mode);check_output(ordinary(destination),external)
            records.append(dict(checker=name,kind='explicit-external-output',exit_code=0,output_sha256=sha(external)))
            for label,target in [('existing',str(destination)),('relative','forbidden.json'),('inside-input',str(root/'evidence/forbidden.json'))]:
                proc=call(script,['--require-readonly','--output',target])
                need(proc.returncode!=0 and proc.stdout==b'' and b'RuntimeError:' in proc.stderr,'output safeguard rejection')
                records.append(dict(checker=name,kind='reject-output-'+label,exit_nonzero=True))
            check_output(ordinary(destination),external)
        # Reproduce the preserved old scripts' limitations in disposable copies.
        changes={'check_normalization.py':('r1 * c1 + r3 * c3','r1 * c1'),'check_followup.py':('a, b, c = n*n*q**4, n*q**2, n','a, b, c = n*n*q**3, n*q**2, n')}
        for name in BASELINES:
            baseline=expected_stdout(name,snapshot,mode)
            for kind in ['positive','readonly','semantic-mutation']:
                location=temp/(name+'-'+kind);location.mkdir();script=location/name
                raw=snapshot['evidence/HISTORICAL_'+name+'.txt']
                if kind=='semantic-mutation':
                    old,new=changes[name];need(raw.count(old.encode())==1,'unique historical mutation');raw=raw.replace(old.encode(),new.encode())
                script.write_bytes(raw)
                if kind=='readonly':script.chmod(0o444);location.chmod(0o555)
                try:
                    proc=call(script,cwd=location)
                    if name=='check_followup.py' and mode:
                        need(proc.returncode!=0 and proc.stdout==b'' and b'requires enabled assertions' in proc.stderr,'historical explicit optimization refusal')
                        disposition='optimized mode explicitly unsupported; no arithmetic validation'
                    elif kind=='readonly':
                        need(proc.returncode!=0 and proc.stdout==b'' and b'PermissionError:' in proc.stderr,'historical implicit-write failure')
                        disposition='implicit adjacent write fails on readonly input'
                    elif kind=='positive':
                        need(proc.returncode==0 and proc.stderr==b'','historical positive execution');check_output(proc.stdout,baseline)
                        disposition='normal arithmetic validated' if mode==0 else 'payload produced with assertions disabled; not validation'
                    elif mode==0:
                        need(proc.returncode!=0 and proc.stdout==b'' and b'AssertionError' in proc.stderr,'historical normal assertion rejection')
                        disposition='normal assertion catches corrupted computation'
                    else:
                        records_old=parsed['evidence/HARDENING_RECEIPT.public.json']['historical_runs']
                        target=[x for x in records_old if x['script']==name and x['mode']==['normal','O','OO'][mode] and x['kind']==kind]
                        need(len(target)==1,'historical false-pass record missing')
                        expected=(json.dumps(target[0]['incorrect_payload'],indent=2)+'\n').encode()
                        need(proc.returncode==0 and proc.stderr==b'','historical false pass execution');check_output(proc.stdout,expected)
                        need(parse(proc.stdout)['c2_stabilizer']['averaged_evaluation']==32,'historical corruption witness')
                        disposition='false PASS reproduced: incorrect stabilization evaluation 32'
                    historical.append(dict(checker=name,kind=kind,interpretation=disposition))
                finally:location.chmod(0o755)
    need(len(records)==47 and len(historical)==6,'exact native control count')
    return dict(positive_modes=4,semantic_mutations_rejected=27,explicit_external_outputs=4,output_safeguard_rejections=12,historical_controls=6,complete_positive_outputs_byte_identical=True,semantic_diagnostics_exact=True,negative_traceback_bytes_compared=False,records=records,historical=historical,readonly_probes_denied=4,fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',source_free=True,mathematical_scope='partial; general normalization-flexible/source extension unresolved')


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin);result=replay(root,snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=30006636,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='exhausted',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
