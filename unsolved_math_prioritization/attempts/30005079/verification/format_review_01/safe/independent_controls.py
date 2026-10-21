"""Private independent actual-CLI controls for the frozen PR888 tool."""
from pathlib import Path
import ast
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import struct
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PRIVATE = HERE / 'private_tmp'
FIXTURE = PRIVATE / 'fixture'
WHEELS = BASE / 'publication_tools_01/private_tmp/wheels'
EXPECTED_TOOL = 'bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910'
assert hashlib.sha256((HERE / 'portable_reviewed.py').read_bytes()).hexdigest() == EXPECTED_TOOL
spec = importlib.util.spec_from_file_location('reviewed_portable', HERE / 'portable_reviewed.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
RECEIPTS = []
RUNTIME_TMP = PRIVATE / 'runtime_tmp'
RUNTIME_TMP.mkdir(exist_ok=True)
os.environ['TMPDIR'] = str(RUNTIME_TMP)


def pin(raw):
    return {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}


def write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def repin(root, current=False):
    index = 'CURRENT_PUBLICATION_MANIFEST.json' if current else 'package_index.json'
    schema = tool.CURRENT_SCHEMA if current else tool.PACKAGE_SCHEMA
    files = []
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.relative_to(root).as_posix() != index:
            files.append({'path':p.relative_to(root).as_posix(), **pin(p.read_bytes())})
    write_json(root/index, {'schema':schema, 'problem_id':'30005079', 'files':files})
    return pin((root/index).read_bytes())['sha256']


def clone(label, current=False):
    p = PRIVATE / label
    shutil.copytree(CURRENT if current else FIXTURE, p)
    return p


def run(label, args, root=FIXTURE, optimize=False, wanted=True, reason=None):
    script = root/'portable.py' if root is not None else HERE/'portable_reviewed.py'
    assert pin(script.read_bytes())['sha256'] == EXPECTED_TOOL
    command = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimize else []) + [str(script), *map(str,args)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = sorted(str(p.relative_to(RUNTIME_TMP)) for p in RUNTIME_TMP.rglob('*'))
    clock = time.monotonic()
    proc = subprocess.run(command, capture_output=True, cwd=HERE, timeout=1200)
    after = sorted(str(p.relative_to(RUNTIME_TMP)) for p in RUNTIME_TMP.rglob('*'))
    try:
        value = json.loads(proc.stdout)
    except Exception:
        value = {'unparsed_stdout':proc.stdout.decode(errors='replace')}
    success = proc.returncode == 0 and value.get('status') == 'PASS'
    matched = success == wanted and (reason is None or reason in value.get('reason',''))
    receipt = {'label':label, 'timestamp_utc':started, 'seconds':round(time.monotonic()-clock,3),
               'actual_cli':True, 'command':command, 'returncode':proc.returncode,
               'wanted_pass':wanted, 'expected_reason_substring':reason, 'expectation_met':matched,
               'stderr':proc.stderr.decode(errors='replace'), 'output':value,
               'runtime_temp_before':before, 'runtime_temp_after':after}
    RECEIPTS.append(receipt)
    write_json(HERE/'ACTUAL_CLI_RECEIPTS.json', RECEIPTS)
    print(label, proc.returncode, matched, value.get('reason',value.get('status')), flush=True)
    assert matched, label
    return value


def verify(label, root, optimize=False, wanted=False, reason=None):
    index = pin((root/'package_index.json').read_bytes())['sha256']
    return run(label,['verify',index,'--root',root,'--verify-only'],root,optimize,wanted,reason)


def current(label, root, wanted=False, reason=None, replay=False, optimize=False):
    index = pin((root/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes())['sha256']
    args = ['current',index,'--root',root]
    args += ['--dependency-dir',WHEELS] if replay else ['--verify-only']
    return run(label,args,root,optimize,wanted,reason)


def mutation(label, mutate, reason=None, optimize=False):
    root = clone(label)
    mutate(root)
    repin(root)
    return verify(label,root,optimize,False,reason)


def change_json(root, name, change):
    value=json.loads((root/name).read_bytes())
    change(value)
    write_json(root/name,value)


def deflate_suffix(raw):
    """Produce a coherent ordinary ZIP with an unused first-stream suffix."""
    data=bytearray(raw)
    end=len(data)-22
    central=struct.unpack_from('<I',data,end+16)[0]
    first_size=struct.unpack_from('<I',data,18)[0]
    name_len,extra_len=struct.unpack_from('<HH',data,26)
    insert_at=30+name_len+extra_len+first_size
    data[insert_at:insert_at]=b'X'
    struct.pack_into('<I',data,18,first_size+1)
    cursor=central+1
    count=struct.unpack_from('<H',data,end+1+10)[0]
    for i in range(count):
        assert data[cursor:cursor+4]==b'PK\x01\x02'
        n,e,c=struct.unpack_from('<HHH',data,cursor+28)
        if i==0:
            size=struct.unpack_from('<I',data,cursor+20)[0]
            struct.pack_into('<I',data,cursor+20,size+1)
        else:
            off=struct.unpack_from('<I',data,cursor+42)[0]
            struct.pack_into('<I',data,cursor+42,off+1)
        cursor+=46+n+e+c
    struct.pack_into('<I',data,end+1+16,central+1)
    # Python's ordinary reader accepts every unchanged uncompressed member.
    import io
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert all(z.read(n)==(FIXTURE/n).read_bytes() for n in z.namelist())
    return bytes(data)


if __name__ == '__main__':
    index=pin((FIXTURE/'package_index.json').read_bytes())['sha256']
    run('normal_authenticated_replay',['verify',index,'--root',FIXTURE,'--dependency-dir',WHEELS],wanted=True)
    run('optimized_authenticated_replay',['verify',index,'--root',FIXTURE,'--dependency-dir',WHEELS],optimize=True,wanted=True)
    # Native source-only positive authenticates the entire corpus in the tool.
    corpus=HERE.parents[3]/'unsolved_math_prioritization'
    corpus_args=['--catalog',corpus/'catalog.json','--problems',corpus/'cache/problems.json','--reports',corpus/'cache/research_results.json']
    run('source_only_complete_corpus',['source-only',*corpus_args],root=None,optimize=True,wanted=True)
    wrong=PRIVATE/'wrong_reports.json'; wrong.write_bytes(b'{}\n')
    broken=corpus_args[:-1]+[wrong]
    run('source_only_third_corpus_corrupt',['source-only',*broken],root=None,wanted=False,reason='source input type/size')
    mutation('unknown_metadata_key',lambda r:change_json(r,'metadata.json',lambda x:x.update(unexpected=True)), 'publication metadata exact keys')
    mutation('wrong_title',lambda r:change_json(r,'metadata.json',lambda x:x.update(title='Incorrect title')), 'fixed identity')
    mutation('creator_extra_key',lambda r:change_json(r,'metadata.json',lambda x:x['creators'][0].update(extra='x')), 'exact sole creator')
    mutation('wrong_orcid',lambda r:change_json(r,'metadata.json',lambda x:x['creators'][0].update(orcid='0000-0000-0000-0000')), 'exact sole creator')
    mutation('deposit_third_asset',lambda r:change_json(r,'zenodo-deposit.json',lambda x:x['files'].append({'name':'extra','path':'extra'})), 'exact two deposit')
    mutation('dependency_bool_bytes',lambda r:change_json(r,'dependencies.json',lambda x:x['wheels'][0].update(bytes=True)), 'dependency contract', optimize=True)
    mutation('duplicate_json_key',lambda r:(r/'metadata.json').write_bytes(b'{"title":"a","title":"b"}'), 'duplicate JSON key')
    mutation('overflow_json_number',lambda r:(r/'metadata.json').write_bytes(b'{"x":1e400}'), 'overflow/nonfinite')
    mutation('empty_directory',lambda r:(r/'empty').mkdir(), 'unlisted directory')
    mutation('symlink_regular_file',lambda r:((r/'README.md').unlink(),(r/'README.md').symlink_to(FIXTURE/'README.md')), 'nonregular tree entry')
    mutation('corrupt_original_checker_before_launch',lambda r:(r/'source/checks/verify_construction.py').write_bytes((r/'source/checks/verify_construction.py').read_bytes()+b'\nraise RuntimeError("MUST_NOT_EXECUTE")\n'), 'pin mismatch: source/')
    malformed=clone('index_boolean_size'); obj=json.loads((malformed/'package_index.json').read_bytes()); obj['files'][0]['bytes']=True; write_json(malformed/'package_index.json',obj)
    verify('index_boolean_size',malformed,reason='typed byte count')
    malformed=clone('index_extra_row_key'); obj=json.loads((malformed/'package_index.json').read_bytes()); obj['files'][0]['extra']=None; write_json(malformed/'package_index.json',obj)
    verify('index_extra_row_key',malformed,reason='inventory row schema')
    malformed=clone('index_traversal'); obj=json.loads((malformed/'package_index.json').read_bytes()); obj['files'][0]['path']='../outside'; write_json(malformed/'package_index.json',obj)
    verify('index_traversal',malformed,reason='unsafe relative path')
    malformed=clone('directory_case_alias'); obj=json.loads((malformed/'package_index.json').read_bytes()); obj['files'].append({'path':'SOURCE/novel','bytes':0,'sha256':hashlib.sha256(b'').hexdigest()}); write_json(malformed/'package_index.json',obj)
    verify('directory_case_alias',malformed,reason='directory name alias')
    # Invalid containment must fail before a missing dependency can trigger replay.
    for label,parent in [('indexed_nested_parent',FIXTURE/'source/checks'),('indexed_case_alias',Path(str(FIXTURE/'source').replace('/source','/SOURCE')))]:
        if parent.is_dir():
            run(label,['build',index,parent/'rank-two-fano-verification.zip','--root',FIXTURE],wanted=False,reason='outside every indexed input directory')
    alias=Path('/System/Volumes/Data')/FIXTURE.relative_to('/')/'source/checks'
    if alias.is_dir():
        run('indexed_firmlink_alias',['build',index,alias/'rank-two-fano-verification.zip','--root',FIXTURE],wanted=False,reason='outside every indexed input directory')
    output_dir=PRIVATE/'output'; output_dir.mkdir()
    output=output_dir/'rank-two-fano-verification.zip'
    build=run('build_default_requires_real_replay',['build',index,output,'--root',FIXTURE,'--dependency-dir',WHEELS],wanted=True)
    before=pin(output.read_bytes())
    run('build_no_overwrite',['build',index,output,'--root',FIXTURE],wanted=False,reason='output must be fresh')
    assert pin(output.read_bytes())==before
    CURRENT=PRIVATE/'current'; CURRENT.mkdir(); shutil.copytree(FIXTURE,CURRENT/'verification')
    for name in ['portable.py','metadata.json','zenodo-deposit.json','note.tex']:
        (CURRENT/name).write_bytes((FIXTURE/name).read_bytes())
    (CURRENT/'rank-two-fano-note.pdf').write_bytes(b'%PDF-1.4\nPRIVATE FORMAT FIXTURE ONLY\n')
    (CURRENT/'rank-two-fano-verification.zip').write_bytes(output.read_bytes())
    write_json(CURRENT/'CURRENT_PUBLICATION.json',{'schema':tool.LAYOUT_SCHEMA,'problem_id':'30005079','portable_prefix':'verification','zip_path':'rank-two-fano-verification.zip','pdf_path':'rank-two-fano-note.pdf','tex_path':'note.tex'})
    repin(CURRENT,True)
    current('fresh_optimized_current_real_replay',CURRENT,wanted=True,replay=True,optimize=True)
    for label,mutate,reason in [
        ('zip_trailing_data',lambda b:b+b'x','ZIP end metadata/extent'),
        ('zip_deflate_unused_suffix',deflate_suffix,'DEFLATE exact-consumption'),
        ('zip_local_extra_length',lambda b:b[:28]+b'\x01\x00'+b[30:],'local/central metadata disagreement'),
    ]:
        root=clone(label,True); z=root/'rank-two-fano-verification.zip'; z.write_bytes(mutate(z.read_bytes())); repin(root,True); current(label,root,reason=reason,optimize=True)
    root=clone('tex_copy_disagreement',True); (root/'note.tex').write_bytes((root/'note.tex').read_bytes()+b'\nchanged\n'); repin(root,True); current('tex_copy_disagreement',root,reason='outer/portable exact copy mismatch')
    write_json(HERE/'INDEPENDENT_TEST_SUMMARY.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':80,'tool_sha256':EXPECTED_TOOL,'actual_cli_cases':len(RECEIPTS),'all_expectations_met':all(r['expectation_met'] for r in RECEIPTS),'engineering_controls_read':False,'whole_package_clearance':False})
