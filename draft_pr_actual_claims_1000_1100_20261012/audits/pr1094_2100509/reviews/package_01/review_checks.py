"""Read-only candidate review; every mutation stays in this review's scratch."""
from pathlib import Path
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
PAPER = BASE / 'preprint_v1_0'
WORK = HERE / '.scratch'
COMMANDS = []

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads(path.read_text())
def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def command(args, cwd, success=True, label=''):
    p = subprocess.run(list(map(str, args)), cwd=cwd, capture_output=True)
    COMMANDS.append({'label': label, 'args': list(map(str, args)),
                     'cwd': str(cwd), 'returncode': p.returncode,
                     'expected_success': success,
                     'stdout': p.stdout.decode(errors='replace'),
                     'stderr': p.stderr.decode(errors='replace')})
    write('COMMAND_RECEIPTS_IN_PROGRESS.json', {'commands':COMMANDS,'count':len(COMMANDS)})
    need((p.returncode == 0) == success, 'unexpected command outcome: ' + label)
    return p

def pins():
    frozen = load(HERE / 'INPUT_PINS.json')
    for row in frozen['entries']:
        data = (BASE / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'changed review input: '+row['path'])
    return len(frozen['entries'])

def main():
    before = pins()
    need(not WORK.exists(), 'scratch already exists; preserve previous run')
    WORK.mkdir()
    archive_path = PAPER / 'pr1094_supportkit_v1.0.zip'
    kit = WORK / 'kit'
    kit.mkdir()
    with zipfile.ZipFile(archive_path) as z:
        need(z.testzip() is None, 'archive CRC')
        names = z.namelist()
        need(names == sorted(set(names)), 'unique sorted archive inventory')
        for info in z.infolist():
            need(not Path(info.filename).is_absolute() and '..' not in Path(info.filename).parts, 'unsafe archive member')
            need(info.date_time == (1980,1,1,0,0,0) and info.compress_type == 0
                 and info.create_system == 3 and info.external_attr == 0o100644 << 16,
                 'archive header')
            target = kit / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(info.filename))
    manifest = load(kit / 'MANIFEST.json')
    need(set(names) == {'MANIFEST.json'} | {r['path'] for r in manifest['records']}, 'manifest partition')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as out:
        for name in names:
            data = (kit / name).read_bytes()
            need(data == (PAPER / 'kit' / name).read_bytes(), 'canonical archive equality')
            info = zipfile.ZipInfo(name, (1980,1,1,0,0,0)); info.create_system=3
            info.external_attr = 0o100644 << 16; info.compress_type = 0
            out.writestr(info, data)
    need(buffer.getvalue() == archive_path.read_bytes(), 'independent CLOSED ZIP differs')
    custody = load(kit / 'CUSTODY_MAP.json')
    old = load(PAPER / 'FROZEN_INPUT_PINS.json')
    prior = {r['path']:{k:r[k] for k in ('path','bytes','sha256')} for r in old['records']}
    selected = set()
    for row in custody['copies']:
        name = row['original_path']; selected.add(name)
        data = (kit / row['copy_path']).read_bytes()
        need({'path':name,'bytes':len(data),'sha256':sha(data)} == prior[name], 'historical selected copy')
    omitted = {r['path'] for r in custody['exclusions']}
    need(not (selected & omitted) and selected | omitted == set(prior), 'exact custody partition')
    original = load(BASE / 'SUBMITTED_PINS.json')
    git_rows = []
    for row in original['files']:
        data = subprocess.check_output(['git','show',original['head_oid']+':'+row['repository_path']], cwd=BASE)
        need(data == (BASE/row['snapshot_path']).read_bytes(), 'actual Git original differs')
        need(len(data)==row['bytes'] and sha(data)==row['sha256'], 'Git pin differs')
        git_rows.append({'path':row['repository_path'],'bytes':len(data),'sha256':sha(data)})
    write('ORIGINAL_GIT_RECHECK.json', {'head':original['head_oid'],'entries':git_rows,'status':'PASS'})
    metadata = load(kit/'metadata.json')
    need(load(kit/'.zenodo.json') == metadata and load(kit/'metadata_api.json') == {'metadata':metadata}, 'three native metadata objects differ')
    need(load(PAPER/'zenodo-deposit.json') == {'metadata':metadata,'files':[
        {'path':'paper.pdf','name':'paper.pdf'},
        {'path':'pr1094_supportkit_v1.0.zip','name':'pr1094_supportkit_v1.0.zip'}]}, 'native uploader equality')
    need(load(PAPER/'DEPOSIT_BINDING.json')['metadata']==metadata, 'binding metadata')
    need((kit/'paper.pdf').read_bytes()==(PAPER/'paper.pdf').read_bytes(), 'external PDF differs')
    script = kit/'scripts'
    protected = {p.relative_to(kit).as_posix():sha(p.read_bytes()) for p in kit.rglob('*') if p.is_file()}
    py = sys.executable
    outputs = []
    for mode, extra in [('normal',[]), ('optimized',['-O'])]:
        prefix = [py,'-B'] + extra
        command(prefix+[script/'verify_kit.py'], kit, label=mode+' extracted default binding absent')
        result_path = WORK/(mode+'-checks.json')
        command(prefix+[script/'run_checks.py','--out',result_path],kit,label=mode+' fresh checks')
        outputs.append(load(result_path))
        rebuilt = WORK/(mode+'-support.zip')
        command(prefix+[script/'build_support.py','--out',rebuilt],kit,label=mode+' fresh ZIP')
        need(rebuilt.read_bytes()==archive_path.read_bytes(),'rebuilt ZIP differs')
        built = WORK/(mode+'-pdf')
        command(prefix+[script/'build_pdf.py','--out-dir',built],kit,label=mode+' real Tectonic compile')
        need((built/'paper.pdf').read_bytes()==(PAPER/'paper.pdf').read_bytes(), 'compiled PDF differs')
        command(prefix+[PAPER/'kit/scripts/verify_kit.py','--require-binding'],PAPER/'kit',label=mode+' canonical strict binding')
        command(prefix+[script/'verify_kit.py','--binding',WORK/'missing.json'],kit,False,mode+' explicitly missing binding')
        command(prefix+[script/'verify_kit.py','--require-binding'],kit,False,mode+' required missing binding')
        # Existing and aliased outputs must fail without changing protected bytes.
        hardlink = WORK/(mode+'-hardlink')
        os.link(kit/'paper.tex', hardlink)
        leaf = WORK/(mode+'-leaf-link'); leaf.symlink_to(kit/'paper.tex')
        ancestor = WORK/(mode+'-ancestor-link'); ancestor.symlink_to(kit,target_is_directory=True)
        external = WORK/(mode+'-existing'); external.write_bytes(b'KEEP')
        targets = [kit/'paper.tex', PAPER/'paper.pdf', hardlink, leaf,
                   ancestor/'absent', kit/'new-member', kit, external, WORK]
        for writer, option in [('run_checks.py','--out'), ('build_support.py','--out'), ('build_pdf.py','--out-dir')]:
            for index, target in enumerate(targets):
                command(prefix+[script/writer,option,target],kit,False,mode+' reject '+writer+' target '+str(index))
        need(external.read_bytes()==b'KEEP','external existing file changed')
        # Manifest bootstrap must be preflighted as a regular unlinked file.
        bootstrap = kit/'MANIFEST.json'; saved = bootstrap.read_bytes()
        bootstrap.unlink(); bootstrap.symlink_to(WORK/'absent-bootstrap')
        command(prefix+[script/'verify_kit.py'],kit,False,mode+' dangling manifest symlink')
        bootstrap.unlink(); bootstrap.write_bytes(saved)
        modified = load(bootstrap); modified['records'].append(modified['records'][0])
        bootstrap.write_text(json.dumps(modified))
        command(prefix+[script/'verify_kit.py'],kit,False,mode+' duplicate manifest record')
        bootstrap.write_bytes(saved)
        # Bad present binding cannot fall back to absent mode.
        default = WORK/'DEPOSIT_BINDING.json'; default.write_text('{}')
        command(prefix+[script/'verify_kit.py'],kit,False,mode+' corrupt present default binding')
        default.unlink()
    need(outputs[0] == outputs[1], 'checker JSON differs by optimization')
    write('PORTABLE_CHECKS_RESULT.json', outputs[0])
    # Exact counterexample to the advertised *lexical* symlink rejection.
    lexical = WORK/'lexical-link'; lexical.symlink_to(kit,target_is_directory=True)
    observations=[]
    for mode,extra in [('normal',[]),('optimized',['-O'])]:
        path = str(lexical)+'/../'+mode+'-lexical-output.json'
        lexical_out = WORK/(mode+'-lexical-output.json')
        p = command([py,'-B']+extra+[script/'run_checks.py','--out',path],kit,
                    label=mode+' finding: lexical symlink dot-dot accepted')
        need(lexical_out.exists(),'normalization finding not reproduced')
        observations.append({'mode':mode,'literal_argument':path,'normalized_output':str(lexical_out),
                             'returncode':p.returncode,'existing_input_modified':False})
    need(sha((kit/'paper.tex').read_bytes())==protected['paper.tex'],'finding modified protected input')
    write('LEXICAL_SYMLINK_FINDING.json', {
        'severity':'P3','observations':observations,
        'why':'abspath collapses lexical-link/.. before no_links inspects components; fresh normalized path remains outside inputs',
        'fix':'Reject lexical symlink components before abspath/resolve, or narrow all matching advertised contracts honestly.'})
    # Independent reviewer program has no candidate imports.
    own_results = []
    for mode, extra in [('normal',[]),('optimized',['-O'])]:
        p=command([py,'-B']+extra+[HERE/'independent_controls.py'], HERE,label=mode+' independent coordinate/geometry controls')
        result=json.loads(p.stdout);own_results.append(result)
        write('INDEPENDENT_'+mode.upper()+'.json',result)
    need(own_results[0]==own_results[1],'independent JSON differs by optimization')
    current = {p.relative_to(kit).as_posix():sha(p.read_bytes()) for p in kit.rglob('*') if p.is_file()}
    need(current==protected,'scratch kit protected files changed at end')
    command([py,'-B',BASE.parents[2]/'zenodo_deposit_tool/zenodo.py','check',PAPER/'zenodo-deposit.json'],BASE,
            label='real repository uploader LOCAL check')
    after = pins()
    write('COMMAND_RECEIPTS.json', {'commands':COMMANDS,'count':len(COMMANDS),
                                   'expected_rejections':sum(not r['expected_success'] for r in COMMANDS)})
    write('REPRODUCTION_RECEIPT.json', {
        'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_WITH_ONE_P3_CONTRACT_FINDING',
        'baseline_inputs_before':before,'baseline_inputs_after':after,
        'original_git_files':len(git_rows),'archive_members':len(names),'selected_prior_copies':len(selected),
        'excluded_prior_files':len(omitted),'metadata_objects_equal':True,
        'independent_closed_zip_equal':True,'compiled_pdfs_byte_equal':True,
        'portable_json_modes_equal':True,'independent_json_modes_equal':True,
        'command_count':len(COMMANDS),'expected_rejections':sum(not r['expected_success'] for r in COMMANDS),
        'candidate_mutation':False,'service_actions':False,'scratch':str(WORK)})
    print(json.dumps({'status':'PASS_WITH_ONE_P3_CONTRACT_FINDING','commands':len(COMMANDS),
                      'rejections':sum(not r['expected_success'] for r in COMMANDS),'inputs':after}))

if __name__=='__main__': main()
