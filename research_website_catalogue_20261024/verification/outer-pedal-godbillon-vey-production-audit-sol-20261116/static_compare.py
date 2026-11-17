#!/usr/bin/env python3
"""One read-only data comparison; no Git, import of project code, or mode replay."""
import datetime, difflib, hashlib, json, re, stat
from pathlib import Path

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
Q=P/'verification/outer-pedal-godbillon-vey-production-audit-sol-20261116'
A=Q/'reviewed-pending'
C=P/'verification/outer-pedal-godbillon-vey-production-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M=P.parent
def need(x,label):
    if not x: raise ValueError(label)
def raw(path):
    need(path.is_absolute() and all(not x.is_symlink() for x in [path,*path.parents]),'ordinary absolute input')
    before=path.lstat(); need(stat.S_ISREG(before.st_mode),'regular input')
    data=path.read_bytes(); after=path.lstat()
    need((before.st_dev,before.st_ino,before.st_mode,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mode,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'stable bytes/mode')
    return data
def digest(b): return hashlib.sha256(b).hexdigest()
def bp(b): return dict(bytes=len(b),SHA256=digest(b))
def filepin(path): return dict(**bp(raw(path)),mode=stat.S_IMODE(path.lstat().st_mode))
def load(path): return json.loads(raw(path))
def bound(row,base=P):
    path=Path(row['path']); path=path if path.is_absolute() else base/path
    need(bp(raw(path))=={k:row[k] for k in ('bytes','SHA256')},'bound file '+str(path))
    return path
def walk(root):
    files={}; dirs={'.':stat.S_IMODE(root.lstat().st_mode)}
    for path in sorted(root.rglob('*')):
        need(not path.is_symlink(),'no namespace symlink')
        s=path.lstat(); name=path.relative_to(root).as_posix()
        if stat.S_ISREG(s.st_mode): files[name]=filepin(path)
        elif stat.S_ISDIR(s.st_mode): dirs[name]=stat.S_IMODE(s.st_mode)
        else: raise ValueError('special entry')
    return files,dirs
def ref(root):
    name=raw(root/'.git/HEAD').strip().decode()
    need(name.startswith('ref: '),'symbolic HEAD')
    branch=name[5:]; path=root/'.git'/branch
    if path.exists(): value=raw(path).strip().decode()
    else:
        values=[line.split()[0] for line in raw(root/'.git/packed-refs').decode().splitlines() if not line.startswith(('#','^')) and line.split()[1]==branch]
        need(len(values)==1,'one packed ref'); value=values[0]
    return branch,value

need(digest(raw(Q/'INITIAL_SEAL.json'))=='e8e5032277de32c91835474c432a7dc3d46b4ab6092071e2caa88735af810fb1','own INITIAL seal')
need(digest(raw(Q/'INITIAL_MANIFEST.sha256'))=='913f14b2cf1eb3412413c32ce5194eb5ef7cabde361befbbb4c61159ac30976c','own INITIAL manifest')
initial_rows=raw(Q/'INITIAL_MANIFEST.sha256').decode().splitlines()
need(len(initial_rows)==19,'nineteen initial payloads')
for line in initial_rows:
    expected,name=line.split('  ',1); need(digest(raw(Path(name)))==expected,'unchanged initial payload')
ready=load(A/'PREPARATION_READY.json'); manifest=load(A/'PREPARATION_MANIFEST.json')
need(bp(raw(A/'PREPARATION_READY.json'))==dict(bytes=4997,SHA256='950516baef190a2d42552297b5f333d9760c33d12d73ba29bed8985715d55389'),'reviewed READY')
need(bp(raw(A/'PREPARATION_MANIFEST.json'))==dict(bytes=4130,SHA256='75c07da9634c4160dbe20b6b4be96426cfbbe6f46fbff9cafaaa35fef61673ac'),'reviewed manifest')
review_files,review_dirs=walk(A)
need(len(review_files)==22 and review_dirs=={'.':0o755},'exact copied 22-file input boundary')
for row in manifest['payload_files']:
    need(review_files[row['path']]=={k:row[k] for k in ('bytes','SHA256','mode')},'all producer payload bytes/modes')
need(set(review_files)=={r['path'] for r in manifest['payload_files']}|{'PREPARATION_MANIFEST.json','PREPARATION_READY.json'},'exact producer terminal-inclusive membership')
receipt=load(A/'BASELINE_CAPTURE_RECEIPT.json')
bound(dict(path='BASELINE_CAPTURE_RECEIPT.json',bytes=3177,SHA256='640359149dbe8b8745630bccdf4f7868e59907808339f233042412a09becd280'),A)
for row in receipt['payloads']:
    bound(row,A); bound(row,C)
plan=load(A/'PLAN.json'); code=raw(A/'release_three.py').decode()
need(bp(code.encode())==dict(bytes=43423,SHA256='32c1ad35b0df295f884eba6a13efd8db20ee7abc959d5d61269f25df33c46c45'),'whole reviewed helper pin')
need(re.findall(r"^PLAN_SHA = '([0-9a-f]{64})'$",code,re.M)==[digest(raw(A/'PLAN.json'))],'sole correct PLAN_SHA')
need(plan['root_stage_adoption'] is None and plan['stage_binding'] is None,'both actual pending fields null')
copy=load(bound(plan['copy_adoption']))
need(copy['public_install_Git_deploy_AA_authority'] is False,'copy action authority false')
expected_scope={'public/research/index.html','public/research/sitemap.xml'}
for record in copy['records']:
    prefix='public/research/'+record['proposed_slug']+'/'
    expected_scope.update([prefix+'index.html',prefix+'citation.bib'])
    expected_scope.update(prefix+n for n in record['native_assets_order'])
need(sorted(expected_scope)==plan['scope_paths'] and len(expected_scope)==22,'exact copy-derived 22 scope')
literal_line=next(line for line in code.splitlines() if line.startswith('TARGETS = '))
need(set(re.findall(r"'(public/research/[^']+)'",literal_line))==expected_scope,'same literal helper scope')
baseline=load(bound(plan['baseline'])); own_baseline=load(Q/'BASELINE.json')
public,dirs=walk(W/'public')
need((public,dirs)==(baseline['public_files'],baseline['public_directories_including_root']),'whole live filesystem 727 bytes/modes/topology')
need((len(public),len(dirs))==(727,364),'whole public extent')
need(set(raw(Q/'W.public.namespace.raw').split(b'\0')[:-1])=={str(W/'public').encode()}|{str(W/'public'/n).encode() for n in public}|{str(W/'public'/n).encode() for n in dirs if n!='.'},'independent initial NUL namespace')
for line in raw(Q/'W.public.sha256').decode().splitlines():
    expected,name=line.split('  ',1); need(digest(raw(Path(name)))==expected,'independent initial whole public hash')
for path,row in baseline['configuration_guards'].items(): need(filepin(Path(path))==row,'all configuration bytes/modes')
need(ref(W)==('refs/heads/master',plan['website_HEAD']) and ref(M)==('refs/heads/main',plan['Math_HEAD']),'actual W/Math refs unchanged without Git')
native=raw(W/'.git/index'); need(native==raw(Q/'W.index.baseline.bin'),'whole initial native index unchanged')
need(filepin(W/'.git/index')=={k:plan['website_index'][k] for k in ('bytes','SHA256','mode')},'W index bytes/mode')
need(filepin(M/'.git/index')==plan['Math_index'],'Math index bytes/mode')
need(native[:12]==bytes.fromhex('44495243000000020000e52b') and hashlib.sha1(native[:-20]).digest()==native[-20:],'independent index header/footer')
rows={}; cursor=12
for unused in range(58667):
    start=cursor; flags=int.from_bytes(native[start+60:start+62],'big')
    need(not flags&0x7000,'ordinary v2 stage-zero record')
    end=native.index(b'\0',start+62); name=native[start+62:end]
    cursor=start+8*((end+1-start+7)//8)
    need(name and name not in rows and not any(native[end+1:cursor]),'record name/padding')
    need(flags&4095==min(len(name),4095),'encoded byte length')
    rows[name]=(native[start:cursor],int.from_bytes(native[start+24:start+28],'big'),native[start+40:start+60].hex())
need(list(rows)==sorted(rows),'record byte ordering')
extension_start=cursor; extensions=[]
while cursor<len(native)-20:
    signature=native[cursor:cursor+4]; size=int.from_bytes(native[cursor+4:cursor+8],'big')
    need(cursor+8+size<=len(native)-20,'extension bounds'); extensions.append((signature.decode(),size)); cursor+=8+size
need(cursor==len(native)-20 and extensions==[('TREE',35870)],'actual sole derived TREE')
extension=native[extension_start:-20]
need(extension_start==plan['baseline_extension']['offset'] and bp(extension)=={k:plan['baseline_extension'][k] for k in ('bytes','SHA256')},'whole TREE region pin')
targets={n.encode() for n in expected_scope}; aggregates={n.encode() for n in plan['replacement_paths']}
need(set(rows)&targets==aggregates and len(targets-set(rows))==20,'native exact 20A2M')
protected=b''.join(rows[n][0] for n in rows if n not in targets)
need(len(rows)-len(aggregates)==58665 and bp(protected)=={k:baseline['protected_raw_records_excluding_two_aggregates'][k] for k in ('bytes','SHA256')},'all protected whole raw records')
stage_rows=raw(Q/'W.index.stage.raw').split(b'\0'); need(stage_rows.pop()==b'' and len(stage_rows)==58667,'own full basic stage records')
for line in stage_rows:
    header,name=line.split(b'\t',1); bits,oid,stage=header.split()
    need((int(bits,8),oid.decode(),stage)==(rows[name][1],rows[name][2],b'0'),'basic semantics independently consistent')
head_rows=raw(Q/'W.HEAD.tree.raw').split(b'\0'); need(head_rows.pop()==b'','HEAD raw NUL boundary')
head={}
for line in head_rows:
    header,name=line.split(b'\t',1); bits,kind,oid=header.split(); head[name]=(int(bits,8),oid.decode())
need({n:r[1:] for n,r in rows.items()}==head,'actual baseline index and HEAD semantics independently equal')
fs={'public/'+n for n in public}; tracked={n.decode() for n in rows if n.startswith(b'public/')}
extra=sorted(fs-tracked)
need(len(tracked)==710 and tracked<=fs and extra==plan['baseline_tracking_asymmetry']['filesystem_only_paths'] and len(extra)==17,'separate 710/727 universes with exact17 extras')
for key in ('disposition','diagnostic'): bound(plan['baseline_tracking_asymmetry'][key])
need(all((n[7:] in public)==(n in plan['replacement_paths']) for n in expected_scope),'filesystem exact20 absent2existing targets')
custody=load(bound(plan['source_contract'])); total=0
allowed_roots=set()
for record in copy['records']:
    allowed_roots.update([P/'papers'/record['record']/'sources',P/'papers'/record['record']/'reviews/editorial',(P/record['fact_FINAL']['path']).parent])
need({Path(item['root']) for item in custody['namespaces']}==allowed_roots,'only exact162163166 source/writer/fact roots; no167169170 review access')
for item in custody['namespaces']:
    files,subdirs=walk(Path(item['root'])); need((files,subdirs)==(item['files'],item['directories']),'whole opaque source/private namespace'); total+=len(files)
need(total==703 and len(custody['namespaces'])==9,'all703 guards')
for record,approved in zip(custody['records'],copy['records']):
    need(record['record']==approved['record'] and [x['native_name'] for x in record['assets']]==approved['native_assets_order'],'native original file order')
    bound(record['MAIN']); bound(record['Bib'])
    for asset in record['assets']: need(raw(bound(asset['source']))==raw(P/'papers'/record['record']/'sources/assets'/asset['native_name']),'whole native download identity')
for row in plan['old_context'].values(): bound(row)
stage=P/plan['stage']; stage_names=set(); stage_dirs={'.'}
for path in stage.rglob('*'):
    s=path.lstat(); need(not path.is_symlink(),'ordinary stage metadata')
    if stat.S_ISREG(s.st_mode): stage_names.add(path.relative_to(stage).as_posix())
    elif stat.S_ISDIR(s.st_mode): stage_dirs.add(path.relative_to(stage).as_posix())
    else: raise ValueError('special stage entry')
valid_prefixes=[prefix for prefix in sorted(stage_dirs-{'.'}) if {prefix+'/'+n for n in expected_scope}<=stage_names]
need(len(stage_names)==53 and expected_scope<=stage_names and valid_prefixes==[],'informed root candidate-root mismatch confirmed from actual path metadata')
reference=P/'verification/odd-areas-boolean-city-production-sol-20261116/release_four.py'
old=raw(reference); need(bp(old)==dict(bytes=39004,SHA256='fe45fb88493cb713d18df0b40aecd725319f02dfb13a3b96507338511e547fda'),'static reference pin only')
diff=''.join(difflib.unified_diff(old.decode().splitlines(True),code.splitlines(True),fromfile=str(reference),tofile=str(C/'release_three.py'))).encode()
need(diff==raw(A/'REFERENCE_ADAPTATION.patch'),'exact reference diff')
need(raw(W/'.git/index')==native and filepin(M/'.git/index')==plan['Math_index'],'closing native guards')
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DATA_CUSTODY_PASS_PENDING_DESIGN_HOLD',
    initial21_exact=True,reviewed_pending22_exact=True,producer_initial8_exact=True,
    reviewed_helper=bp(code.encode()),reviewed_PLAN=bp(raw(A/'PLAN.json')),
    public_files=727,public_child_directories=363,native_public=710,protected_filesystem_only=extra,
    native_entries=58667,native_mode='0644',untargeted_full_raw_records=58665,protected_raw_pin=bp(protected),
    sole_extension=extensions,extension_pin=bp(extension),foreign_staging_differences=0,
    exact_scope=sorted(expected_scope),source_namespace_count=9,source_private_guarded_files=703,
    reference_diff_exact=True,stage_metadata_files=len(stage_names),stage_metadata_child_directories=len(stage_dirs)-1,
    candidate_root_gap=dict(root_informed_before_data_check=True,direct_stage_root_contains_all22=True,non_dot_prefixes_satisfying_current_consumer=valid_prefixes),
    actual_stage_binding=None,actual_root_stage_adoption=None,implementation_or_production_PASS=False,
    helper_modes_Git_import_compile_AST_negative_tests_or_project_program_execution=0,
    output_only=True),indent=2))
