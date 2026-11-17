#!/usr/bin/env python3
"""Single exact bound-edition data comparator; no reviewed code or Git execution."""
import datetime, difflib, hashlib, json, re, stat
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
Q=P/'verification/outer-pedal-godbillon-vey-production-audit-sol-20261116'
D=Q/'bound-continuation'; OLD=Q/'corrected-continuation'
C=P/'verification/outer-pedal-godbillon-vey-production-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com'); M=P.parent
def need(x,label):
    if not x: raise ValueError(label)
def raw(p):
    need(p.is_absolute() and all(not x.is_symlink() for x in [p,*p.parents]),'ordinary absolute input')
    a=p.lstat(); need(stat.S_ISREG(a.st_mode),'regular file'); data=p.read_bytes(); z=p.lstat()
    need((a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable input'); return data
def sha(b): return hashlib.sha256(b).hexdigest()
def bp(b): return dict(bytes=len(b),SHA256=sha(b))
def fp(p): return dict(**bp(raw(p)),mode=stat.S_IMODE(p.lstat().st_mode))
def load(p): return json.loads(raw(p))
def bound(row):
    p=Path(row['path']); p=p if p.is_absolute() else P/p
    need(bp(raw(p))=={k:row[k] for k in ('bytes','SHA256')},'exact document pin'); return p
def walk(root):
    files={}; dirs={'.':stat.S_IMODE(root.lstat().st_mode)}
    for p in sorted(root.rglob('*')):
        s=p.lstat(); name=p.relative_to(root).as_posix(); need(not p.is_symlink(),'no namespace symlink')
        if stat.S_ISREG(s.st_mode): files[name]=fp(p)
        elif stat.S_ISDIR(s.st_mode): dirs[name]=stat.S_IMODE(s.st_mode)
        else: raise ValueError('special namespace')
    return files,dirs
def ref(root):
    head=raw(root/'.git/HEAD').strip().decode(); need(head.startswith('ref: '),'symbolic HEAD')
    branch=head[5:]; p=root/'.git'/branch
    if p.exists(): return branch,raw(p).strip().decode()
    matches=[line.split()[0] for line in raw(root/'.git/packed-refs').decode().splitlines() if line and not line.startswith(('#','^')) and line.split()[1]==branch]
    need(len(matches)==1,'one packed ref'); return branch,matches[0]
for root,name,expected in [(Q,'FINAL.json','de8b23a7a14f1ab5682c6abba5d2a78aba23198b16f172a6888a22d0b2e14415'),(OLD,'FINAL.json','54c59501681ab622da9b930a2633e75a6d363f8bf1a2c9b60b01caacd3d7026b'),(Q,'INITIAL_SEAL.json','e8e5032277de32c91835474c432a7dc3d46b4ab6092071e2caa88735af810fb1')]: need(sha(raw(root/name))==expected,'old seal unchanged')
for path,count in [(Q/'AUDIT_MANIFEST.sha256',54),(OLD/'MANIFEST.sha256',19),(Q/'INITIAL_MANIFEST.sha256',19)]:
    lines=raw(path).decode().splitlines(); need(len(lines)==count,'old manifest count')
    for line in lines:
        expected,name=line.split('  ',1); need(sha(raw(Path(name)))==expected,'all original77 files and initial bytes retained')
for table in (Q/'AUDIT_MODES.txt',OLD/'MODES.txt'):
    for line in raw(table).decode().splitlines():
        match=re.fullmatch(r'(Regular File|Directory) ([0-7]+) ([0-9]+) (.+)',line); need(match is not None,'saved mode row')
        kind,permissions,size,name=match.groups(); p=Path(name); need(stat.S_IMODE(p.lstat().st_mode)==int(permissions,8),'all original77 modes retained')
        if kind=='Regular File': need(len(raw(p))==int(size),'old regular-file extent retained')
for p in (Q/'AUDIT_MODES.txt',Q/'AUDIT_MANIFEST.sha256',Q/'FINAL.json',OLD/'MODES.txt',OLD/'MANIFEST.sha256',OLD/'FINAL.json'): need(stat.S_IMODE(p.lstat().st_mode)==420,'old metadata mode retained')
need(bp(raw(D/'BOUND_READY.json'))==dict(bytes=4972,SHA256='3dd07bbc049595753d32eeda4b94bf7e69ba341b08eee4c55422d07ef89fa6b0'),'BOUND_READY')
need(bp(raw(D/'BOUND_MANIFEST.json'))==dict(bytes=21721,SHA256='8e8db749ddd1190012badadf1398d46dc784e482f0f775652801dc4436882c47'),'BOUND_MANIFEST')
manifest=load(D/'BOUND_MANIFEST.json'); files,dirs=walk(C)
expected={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in manifest['payload_files']}
for name in ('BOUND_MANIFEST.json','BOUND_READY.json'): expected[name]=fp(D/name)
need(files==expected and len(files)==110 and dirs=={'.':493,'pending-original':493,'prebinding-corrected':493,'prebinding-corrected/pending-original':493},'complete110/3 namespace bytes/modes')
pre=C/'prebinding-corrected'; before,pre_dirs=walk(pre)
corrected_manifest=load(OLD/'CORRECTED_MANIFEST.json')
expected_pre={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in corrected_manifest['payload_files']}
for n in ('CORRECTED_MANIFEST.json','CORRECTED_READY.json'): expected_pre[n]=fp(OLD/n)
need(before==expected_pre and len(before)==51 and pre_dirs=={'.':493,'pending-original':493},'entire51 prebinding snapshot exact')
need(all(fp(C/n)==row for n,row in before.items() if n not in ('PLAN.json','release_three.py')),'all49 other prior current files unchanged')
original,original_dirs=walk(Q/'reviewed-pending')
need(walk(C/'pending-original')==(original,original_dirs) and walk(pre/'pending-original')==(original,original_dirs),'both complete original22 histories exact')
oldplan=load(pre/'PLAN.json'); plan=load(D/'PLAN.json'); data=load(D/'ROOT_BINDING_DATA.json')
need(bp(raw(D/'ROOT_BINDING_DATA.json'))==dict(bytes=12666,SHA256='9d2bf46aa165f99d15645fa6cd5564608c304434b07fb72c06b56b903c66456b'),'root data')
need(bp(raw(D/'ROOT_BINDING_GO.json'))==dict(bytes=3910,SHA256='a93efa52138cb145b4a3a5cc9d57f0dad7ed70af0ce76f7ed7b5eff06a281cc1'),'root binding-only GO')
go=load(D/'ROOT_BINDING_GO.json')
need(go['allowed_PLAN_fields']==['root_stage_adoption','stage_binding'] and go['helper_execution_import_compile_AST_runtime_authority'] is False and go['production_install_Git_deploy_Sheet_AA_authority'] is False,'binding-only scope')
need(plan['root_stage_adoption']==data['root_stage_adoption'] and plan['stage_binding']==data['stage_binding'],'entire exact two values from root data')
without=json.loads(json.dumps(plan)); without.update(root_stage_adoption=None,stage_binding=None)
need(without==oldplan,'no other PLAN value changed')
code=raw(D/'release_three.py'); oldcode=raw(pre/'release_three.py')
need(bp(code)==dict(bytes=43501,SHA256='7cf936a0c55abb1099ffee51c28be11feeb96624f84e91b301933389ea0c5653') and bp(raw(D/'PLAN.json'))==dict(bytes=24178,SHA256='21f960326e15c20c1ae41ec3eb3bb6fb98c2aa648971bd10203183924504db05'),'bound whole code/PLAN')
need(code==oldcode.replace(sha(raw(pre/'PLAN.json')).encode(),sha(raw(D/'PLAN.json')).encode()) and code.count(b'PLAN_SHA = ')==1,'sole PLAN_SHA code change')
diff=''.join(difflib.unified_diff(raw(pre/'PLAN.json').decode().splitlines(True),raw(D/'PLAN.json').decode().splitlines(True),fromfile='prebinding-corrected/PLAN.json',tofile='PLAN.json'))
diff+=''.join(difflib.unified_diff(oldcode.decode().splitlines(True),code.decode().splitlines(True),fromfile='prebinding-corrected/release_three.py',tofile='release_three.py'))
need(diff.encode()==raw(D/'STAGE_BINDING.patch'),'whole exact binding patch')
adoption=load(bound(plan['root_stage_adoption'])); binding=plan['stage_binding']; targets=set(plan['scope_paths'])
need(adoption['production_install_Git_deploy_or_tracker_authority'] is False and adoption['independent_stage_audit_PASS'] is True and adoption['independent_stage_audit_FINAL']==binding['audit_FINAL'],'private adoption and independent audit binding')
need(adoption['status']==plan['root_stage_adoption_required_status'] and binding['status']==plan['stage_binding_required_status'],'actual statuses')
bound(binding['audit_FINAL'])
for key in ('stage_FINAL','stage_manifest','public_payloads'): need(adoption[key]==binding[key],'same adopted documents'); bound(binding[key])
need(sorted(adoption['candidate_exact_paths'])==sorted(targets) and len(targets)==22 and adoption['scope']==dict(A=20,M=2,total=22,projected_counts=[747,121,122]),'canonical fixed22')
stage=P/plan['stage']; sf,sd=walk(stage)
need(sf=={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in binding['stage_files']} and sd==binding['stage_directories'] and len(sf)==53 and len(sd)==7,'whole53/6 adopted stage')
need(binding['candidate_root']=='public' and {n for n in sf if n.startswith('public/')}==targets,'actual public-prefix22 mapping')
need({n for n in sd if n=='public' or n.startswith('public/')}=={'public'}|{p.as_posix() for n in targets for p in Path(n).parents if p.as_posix()!='.'},'candidate topology')
base=load(bound(plan['baseline'])); custody=load(bound(plan['source_contract']))
public,pdirs=walk(W/'public'); need((public,pdirs)==(base['public_files'],base['public_directories_including_root']) and (len(public),len(pdirs))==(727,364),'whole current727/363 public buffers modes namespace')
source_count=0
for item in custody['namespaces']:
    need(walk(Path(item['root']))==(item['files'],item['directories']),'whole source/editorial/fact guards'); source_count+=len(item['files'])
need(source_count==703 and len(custody['namespaces'])==9,'all703/9 current source guards')
for record in custody['records']:
    prefix='public/research/'+record['slug']+'/'; page=raw(stage/(prefix+'index.html'))
    need(re.findall(rb'<main\b[^>]*>[\s\S]*?</main>',page)==[raw(bound(record['MAIN'])).rstrip(b'\n')],'whole adopted MAIN external LF only')
    need(raw(stage/(prefix+'citation.bib'))==raw(bound(record['Bib'])),'whole Bib')
    for asset in record['assets']: need(raw(stage/(prefix+asset['native_name']))==raw(bound(asset['source']))==raw(P/'papers'/record['record']/'sources/assets'/asset['native_name']),'whole original asset identity')
need(fp(W/'.git/index')=={k:plan['website_index'][k] for k in ('bytes','SHA256','mode')} and raw(W/'.git/index')==raw(Q/'W.index.baseline.bin'),'native whole index current and independent initial exact')
need(fp(M/'.git/index')==plan['Math_index'],'Math index current')
need(ref(W)==('refs/heads/master',plan['website_HEAD']) and ref(M)==('refs/heads/main',plan['Math_HEAD']),'W/Math active refs unchanged without Git')
for path,row in base['configuration_guards'].items(): need(fp(Path(path))==row,'all config guards current')
for row in plan['old_context'].values(): bound(row)
for n in ('transactions','git-transactions','ACTIVE_INSTALL.lock','ACTIVE_GIT.lock','INSTALL_AUTHORIZATION.json','GIT_AUTHORIZATION.json'): need(not (C/n).exists() and not (C/n).is_symlink(),'no runtime paths or action authority')
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_FINAL_BOUND_STATIC_ONLY',
    original77_and_sourceINITIAL_preserved=True,producer110files3dirs_exact=True,entire51prebinding_and_both22_histories_exact=True,
    only2PLANvalues_and_PLAN_SHA_changed=True,values_exact_from_root9d2b_with_a93_binding_only_GO=True,
    all_other_executable_bytes_unchanged=True,stage53files6dirs_and_exact22_match=True,
    all703source_private_and727public_buffers_modes_current=True,entire_native_index1959_and_Math91b10_unchanged=True,
    protected58665rawrecords_flags_TREE='Unchanged whole native bytes; original full parsing evidence retained',
    independent_stage_audit_and_private_false_action_adoption_bound=True,
    new_preflight_fingerprint=None,action_authority=None,runtime_paths_absent=True,
    reviewed_helper_default_preflight_install_publish_Git_import_AST_compile_native_render_network_actions=0,
    production_or_runtime_PASS=False),indent=2))
