#!/usr/bin/env python3
"""Authenticate audited DGA equivalence partial results; replay source-free finite checks."""
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

ACCEPTED = {'evidence/APPROACHES.json': {'bytes': 2887, 'sha256': '0062ea21d6d1f0b22e2949ee68f6ef417cbbd759b6c52ab72cce3f03451c813a'}, 'evidence/AUDIT_RUNS.public.json': {'bytes': 43979, 'sha256': '1f1cde97aa5ba9556a51f46eb28e99bcfb739698047f811094885319a61a2979'}, 'evidence/AUDIT_SUMMARY.public.json': {'bytes': 1119, 'sha256': 'c3059039ec69fd65a8e504bed6bab20170ab473b999c7b02b0c017fa221ba465'}, 'evidence/AUTHOR_RUNS.public.json': {'bytes': 26333, 'sha256': '7b5819d50793fab9817453eeb77b6de208fa37fbad2606a1bf5c93da3b6b3066'}, 'evidence/DATASET_MATCH_METADATA.json': {'bytes': 1087, 'sha256': 'c26adf25bfad462a475ac850bf6c56ff590dee9feec8e52d9a2a65b5887ad7d4'}, 'evidence/INDEPENDENT_AUDIT.public.md': {'bytes': 27411, 'sha256': 'c226f8ce6e3555d90a368902e8c5d7c1098d9d354f37bfbc7f4314e33a89c7a5'}, 'evidence/MUTATION_METADATA.json': {'bytes': 6531, 'sha256': '13add528c39fdf522fe2eac0758a43609c9509dd621b5e1de58c57c0fd1becf9'}, 'evidence/PRIOR_SOURCE_METADATA.json': {'bytes': 1577, 'sha256': '63379b4e21dc7f43ac1f00fe9dc0649ffad1d6a9eac85161f35c89253bd53ed3'}, 'evidence/PROVENANCE_ADDENDUM.md': {'bytes': 2072, 'sha256': '2c8cd637bdaa40c3b3455c3fd38de66e0c180823980d76e8d746928ba608e2d7'}, 'evidence/PUBLIC_SLICE.json': {'bytes': 4108, 'sha256': '09b6800d4839f2b2ef0aa428a1b0382526eaa2b024d148ace83d69dbe35c88a9'}, 'evidence/REPORT.md': {'bytes': 30836, 'sha256': '54bd5c5cc2b3c7f26a391f0cd82cd6e3b90a3544ee1b9c283fa22a08b04e3b98'}, 'evidence/SOURCE_COMPARISON.json': {'bytes': 389, 'sha256': '77818b237ec8f57ace3e9e16ab954434cf1534c9ac28eadb88d907b83981e0c0'}, 'evidence/SOURCE_MANIFEST.json': {'bytes': 5322, 'sha256': 'bc41721afbdb7c9666a40dc8db04b9d33b8c166d505f3004d2de3191ef09a8f8'}, 'evidence/STATUS.public.json': {'bytes': 831, 'sha256': '72bb04b32309a0c5b4a9225f1d80f382cb32a8e731a70b826d0bf796a5b605b7'}, 'evidence/check_exact.py': {'bytes': 14656, 'sha256': '74b21a37d2c09d299ddf796b49ea973b2d9d7a5eed228dd41d81f29ccb5e2893'}, 'evidence/check_independent.py': {'bytes': 8756, 'sha256': '72cf649d82d8dbb722414404304b46d1c5109c851186c0d25bb3f2a99580aa6d'}, 'expected/check_exact.py.O.json': {'bytes': 3577, 'sha256': 'aae9add439afcf88942ec485ea578dc52834d535a058bdaae161f1c9de2ae120'}, 'expected/check_exact.py.OO.json': {'bytes': 3577, 'sha256': '35df91dd8e98b9ee2ff45e7e8c18ed2d170ca58360f014e7e2498956d67229df'}, 'expected/check_exact.py.normal.json': {'bytes': 3577, 'sha256': 'f5982d201df5aa856887ac6cabb05fc54971c31e9483fbbdc98b219874781930'}, 'expected/check_independent.py.O.json': {'bytes': 952, 'sha256': '62c9afe7ace3c4a8ffdce1cf85ba0e5419c6cbdee32cae110b8a1c81a94cdfbc'}, 'expected/check_independent.py.OO.json': {'bytes': 952, 'sha256': '11d93f97ad3f2355fcaa21bd259a04f700d0f135d6faddb30f0df45046481e09'}, 'expected/check_independent.py.normal.json': {'bytes': 952, 'sha256': '67a950f43feaa4825adfa3e5bd3f866cdd6d2ae08877e4125248c44a2bb83084'}}
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
    exact_int(value['problem_id'], 3023)
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


def validate_runs(value, count):
    keys(value,['schema','problem_id','role','fresh_source_bindings','fresh_corpus_bindings','runs'])
    exact_int(value['schema'],1);exact_int(value['problem_id'],3023)
    need(value['fresh_source_bindings']==value['fresh_corpus_bindings']=='NOT_RUN','historical scope')
    need(type(value['runs']) is list and len(value['runs'])==count,'historical output count')
    seen=set()
    for row in value['runs']:
        keys(row,['label','exit_code','stdout','stderr','stdout_sha256','stderr_sha256'])
        need(type(row['label']) is str and row['label'] not in seen,'unique run label');seen.add(row['label'])
        exact_int(row['exit_code']);need(type(row['stdout']) is type(row['stderr']) is str,'complete stream strings')
        for kind in ['stdout','stderr']:
            digest(row[kind+'_sha256']);need(sha(row[kind].encode())==row[kind+'_sha256'],'complete stream binding')
            if row[kind]:parse(row[kind])
    return {x['label']:x for x in value['runs']}


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name,row in ACCEPTED.items():
        need(same(row,dict(bytes=len(snapshot[name]),sha256=sha(snapshot[name]))),'accepted evidence bytes changed')
    record=parsed['evidence/PUBLIC_SLICE.json']
    need(record['retained_authored_mathematics_unchanged'] is True and record['source_documents_or_private_material_included'] is False,'public scope')
    for name,row in record['unchanged_public_members'].items():
        need(name in ACCEPTED and same(row,dict(bytes=len(snapshot[name]),sha256=sha(snapshot[name]))),'unchanged public binding')
    for row in record['public_derivatives']:
        need(row['path'] in ACCEPTED and same(row,dict(path=row['path'],bytes=len(snapshot[row['path']]),sha256=sha(snapshot[row['path']]))),'derivative binding')
    audit=validate_runs(parsed['evidence/AUDIT_RUNS.public.json'],41)
    author=validate_runs(parsed['evidence/AUTHOR_RUNS.public.json'],5)
    for label in ['normal','optimized','double_optimized']:
        need(same(audit[label],author[label]),'native audit/author complete output equality')
    summary=parsed['evidence/AUDIT_SUMMARY.public.json']
    need(summary['semantic_mutations']==11 and summary['semantic_mutation_runs']==33 and summary['all_semantic_mutations_rejected'] is True,'historical mutation scope')
    need(summary['full_source_coverage']=='NOT_RUN','Bokut absence scope')
    status=parsed['evidence/STATUS.public.json']
    need(status['status']=='exhausted' and type(status['turns']) is int and status['turns']==5 and status['full_resolution'] is False,'target scope')
    prior=parsed['evidence/PRIOR_SOURCE_METADATA.json']
    need(prior['substantive_same_target_attempts'] is True and prior['verified_inherited_corpus_match'] is False and prior['novelty_claim'] is False,'prior overlap scope')
    import ast
    for name in ['check_exact.py','check_independent.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot['evidence/'+name]))),'optimized-away assertion')
    return snapshot,parsed


def expected_stdout(name,snapshot,mode):
    return snapshot['expected/'+name+'.'+['normal','O','OO'][mode]+'.json']


def check_output(raw,expected):
    need(type(raw) is type(expected) is bytes and raw==expected,'complete exact output mismatch')


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
    label=['normal','optimized','double_optimized'][mode]
    audit={x['label']:x for x in parsed['evidence/AUDIT_RUNS.public.json']['runs']}
    records=[]
    with tempfile.TemporaryDirectory(prefix='dga-publication-output-') as directory:
        temp=Path(directory)
        env=dict(PATH=os.defpath,HOME=str(temp),TMPDIR=str(temp),LC_ALL='C')
        def call(name,script,extra,expected_exit,stdout,stderr=b''):
            proc=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*extra],cwd=Path.cwd(),env=env,capture_output=True,timeout=120)
            need(proc.returncode==expected_exit,'exact exit code')
            check_output(proc.stdout,stdout);check_output(proc.stderr,stderr)
            if stdout:parse(stdout)
            if stderr:parse(stderr)
            records.append(dict(label=name,exit_code=proc.returncode,stdout=proc.stdout.decode(),stderr=proc.stderr.decode(),stdout_sha256=sha(proc.stdout),stderr_sha256=sha(proc.stderr)))
            return parse(stdout) if stdout else None
        native=root/'evidence/check_exact.py'
        value=call('native',native,['--probe-readonly'],0,expected_stdout('check_exact.py',snapshot,mode))
        need(value['source_verification']['status']=='NOT_RUN' and all(x['status']=='DENIED' for x in value['readonly_probes']) and len(value['readonly_probes'])==2,'native source-free readonly scope')
        ind=call('independent',root/'evidence/check_independent.py',[str(native)],0,expected_stdout('check_independent.py',snapshot,mode))
        need(ind['checks']['word_normalization_comparisons']==6825 and ind['checks']['massey_defining_system_samples']==810,'independent exact counts')
        for old,extra,exitcode in [('missing_sources_required',['--require-sources'],2),('corrupt_source',[],1)]:
            expected=parse(audit[old]['stdout']);expected['optimization']=mode
            if old=='corrupt_source':
                corrupt=temp/'corrupt-source';corrupt.mkdir()
                (corrupt/'manolescu_rozenblyum.pdf').write_bytes(b'CONTROL: deliberately invalid public-source byte sequence\n')
                extra=['--sources',str(corrupt)]
            raw=(json.dumps(expected,indent=2,sort_keys=True)+'\n').encode()
            call(old,native,extra,exitcode,raw)
        mutations=parsed['evidence/MUTATION_METADATA.json']
        need(len(mutations)==11,'semantic mutation count')
        mutated=temp/'mutated';mutated.mkdir()
        (mutated/'SOURCE_MANIFEST.json').write_bytes(snapshot['evidence/SOURCE_MANIFEST.json'])
        original=snapshot['evidence/check_exact.py'].decode()
        for change in mutations:
            need(original.count(change['before'])==1,'unique mutation anchor')
            raw=original.replace(change['before'],change['after']).encode()
            need(sha(raw)==change['mutated_code_sha256'],'historical exact mutation')
            script=mutated/'check_exact.py';script.write_bytes(raw)
            historic=audit[change['name']+'_'+label]
            call(change['name'],script,[],1,historic['stdout'].encode(),historic['stderr'].encode())
    need(len(records)==15,'exact replay count')
    return dict(positive_checkers=2,semantic_mutations_rejected=11,source_controls=2,complete_outputs_byte_identical=True,records=records,readonly_probes_denied=6,fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',source_free=True,mathematical_scope='audited partial results; general graded-commutative decision questions unresolved')


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin);result=replay(root,snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=3023,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='exhausted',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
