from pathlib import Path
import hashlib, json, datetime, io, zipfile, tempfile, subprocess, os

A = Path(__file__).resolve().parents[1]
P = A / 'NEWpreprint_v1_0'
R = A / 'repairs/package01'
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def check(p, x):
    b = p.read_bytes()
    if len(b) != x['bytes'] or sha(b) != x['sha256']:
        raise RuntimeError(str(p))
    return b

outputs = load(R/'OUTPUT_PINS.json')['records']
for x in outputs: check(R/x['path'], x)
changes = load(R/'CHANGE_INVENTORY.json')['authorized_existing_changes']
changed = {x['path']: x for x in changes}
baseline = load(R/'BASELINE_INPUT_PINS.json')['records']
for x in baseline:
    if x['path'] in changed:
        c = changed[x['path']]
        check(A/c['before_bytes_path_relative_to_audit'], x)
        if c['after'] is None:
            if (A/x['path']).exists(): raise RuntimeError('Deleted CFF active')
        else: check(A/x['path'], c['after'])
    else: check(A/x['path'], x)
current = load(R/'CURRENT_OUTPUT_PINS.json')['records']
for x in current: check(P/x['path'], x)
frozen = load(P/'FROZEN_INPUTS.json')['records']
for x in frozen: check(Path(x['path']) if Path(x['path']).is_absolute() else A/x['path'], x)
historical = load(R/'PREPARATION_92_PIN_RESOLUTION.json')['records']
for x in historical:
    before = x.get('before_bytes_path_relative_to_audit')
    check(A/before if before else P/x['path'], x)
copies = load(P/'INPUT_COPY_MAP.json')['copies']
for x in copies:
    b = check(P/x['package_copy'], x)
    source = A/x.get('source_snapshot', x['original_path'])
    if source.read_bytes() != b: raise RuntimeError('Historical source copy differs')
metadata = load(P/'metadata.json')
if metadata != load(P/'metadata_wrapped.json')['metadata'] or metadata != load(P/'deposit.json')['metadata']:
    raise RuntimeError('Metadata differs')
for n in ['metadata.json','metadata_wrapped.json','deposit.json','paper.tex','paper.pdf']:
    x = next(x for x in baseline if x['path']=='NEWpreprint_v1_0/'+n)
    check(P/n, x)
manifest = load(P/'PACKAGE_MANIFEST.json')
names = sorted([x['path'] for x in manifest['members']]+['PACKAGE_MANIFEST.json'])
for x in manifest['members']: check(P/x['path'], x)
archive = P/'PR1071_preprint_v1_0_support.zip'
with zipfile.ZipFile(archive) as z:
    if z.namelist()!=names or z.testzip() is not None: raise RuntimeError('ZIP structure')
    for n in names:
        i=z.getinfo(n)
        if z.read(n)!=(P/n).read_bytes() or i.date_time!=(2026,10,14,0,0,0) or i.external_attr!=(0o100644<<16) or i.compress_type!=zipfile.ZIP_STORED:
            raise RuntimeError('ZIP payload/header')
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
    for n in names:
        i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED
        z.writestr(i,(P/n).read_bytes())
if buf.getvalue()!=archive.read_bytes(): raise RuntimeError('Independent CLOSED ZIP differs')
commands=[]
with tempfile.TemporaryDirectory(prefix='root-repair01-',dir=Path(__file__).parent) as td:
    td=Path(td).resolve(); clean=td/'clean'
    with zipfile.ZipFile(archive) as z: z.extractall(clean)
    protected={n:sha((clean/n).read_bytes()) for n in names}
    def run(flags,args,success=True):
        argv=['python3','-B',*flags,*args]
        p=subprocess.run(argv,cwd=clean,capture_output=True)
        if (p.returncode==0)!=success: raise RuntimeError(str(argv)+p.stderr.decode(errors='replace'))
        commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':success,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
    for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
        run(flags,['scripts/verify_package.py'])
        run(flags,['scripts/check.py','--out',str(td/('checks-'+mode))])
        rebuilt=td/('rebuilt-'+mode+'.zip')
        run(flags,['scripts/build_archive.py','--out',str(rebuilt)])
        if rebuilt.read_bytes()!=archive.read_bytes(): raise RuntimeError('Supplied rebuild differs')
        run(flags,['scripts/verify_package.py','--require-bindings','--bindings',str(P/'UPLOAD_BINDINGS.json'),'--archive',str(rebuilt)])
        run(flags,['scripts/verify_package.py','--require-bindings'],False)
        alias=td/('alias-'+mode);os.link(clean/'paper.tex',alias)
        run(flags,['scripts/build_archive.py','--out',str(alias)],False)
        alias.unlink()
        run(flags,['scripts/build_archive.py','--out',str(clean/'custody'/'new.zip')],False)
        mp=clean/'PACKAGE_MANIFEST.json'; old=mp.read_bytes(); mp.unlink(); target=td/('manifest-'+mode);target.write_bytes(old);mp.symlink_to(target)
        run(flags,['scripts/verify_package.py'],False);mp.unlink();mp.write_bytes(old)
        if {n:sha((clean/n).read_bytes()) for n in names}!=protected:raise RuntimeError('Protected clean bytes changed')
    # The historical deposit.json is a metadata-only API wrapper. A separate
    # native uploader manifest preserves that immutable reviewed object.
    native = A/'publication/zenodo-deposit.json'
    if load(native)['metadata'] != metadata: raise RuntimeError('Native metadata differs')
    run([], [str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(native)])
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ADOPT_BOUNDED_PACKAGE_REPAIR01_PENDING_NEW_COMPLETE_WHOLE02','full_repair_report_and_complete_352_line_diff_read':True,'terminal_outputs_rehashed':len(outputs),'immediate_baseline_resolved':len(baseline),'authorized_changes':len(changes),'unchanged_protected':len(baseline)-len(changes),'current_candidate_records_rehashed':len(current),'original_preparation_inputs_rehashed':len(frozen),'historical_92_output_records_resolved':len(historical),'source_equal_copies_rehashed':len(copies),'archive_members_rehashed':len(names),'independent_closed_archive_byte_identical':True,'actual_commands':commands,'paper_source_pdf_and_native_metadata_unchanged':True,'no_current_compile_or_render_by_root_in_bounded_repair':True,'whole_reviews_completed':1,'minimum_whole_reviews':2,'publication_ready':False,'issues_resolved':False,'published':False,'ordered_hold_pr':1032}
(A/'ROOT_REPAIR_REVIEW_01.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['actual_commands']}))
