#!/usr/bin/env python3
"""Narrow corrected-edition data proof only. Prints JSON; no project execution."""
import datetime, difflib, hashlib, json, re, stat
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
Q=P/'verification/outer-pedal-godbillon-vey-production-audit-sol-20261116'
D=Q/'corrected-continuation'
C=P/'verification/outer-pedal-godbillon-vey-production-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def need(x,label):
    if not x: raise ValueError(label)
def raw(path):
    need(path.is_absolute() and all(not x.is_symlink() for x in [path,*path.parents]),'ordinary absolute data')
    a=path.lstat(); need(stat.S_ISREG(a.st_mode),'regular data file'); b=path.read_bytes(); z=path.lstat()
    need((a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'stable input'); return b
def sha(b): return hashlib.sha256(b).hexdigest()
def bp(b): return dict(bytes=len(b),SHA256=sha(b))
def fp(p): return dict(**bp(raw(p)),mode=stat.S_IMODE(p.lstat().st_mode))
def load(p): return json.loads(raw(p))
def bound(row):
    p=Path(row['path']); p=p if p.is_absolute() else P/p
    need(bp(raw(p))=={k:row[k] for k in ('bytes','SHA256')},'bound document'); return p
def walk(root):
    files={}; dirs={'.':stat.S_IMODE(root.lstat().st_mode)}
    for p in sorted(root.rglob('*')):
        s=p.lstat(); name=p.relative_to(root).as_posix(); need(not p.is_symlink(),'no symlink')
        if stat.S_ISREG(s.st_mode): files[name]=fp(p)
        elif stat.S_ISDIR(s.st_mode): dirs[name]=stat.S_IMODE(s.st_mode)
        else: raise ValueError('special namespace')
    return files,dirs
need(sha(raw(Q/'FINAL.json'))=='de8b23a7a14f1ab5682c6abba5d2a78aba23198b16f172a6888a22d0b2e14415','original audit final')
need(sha(raw(Q/'AUDIT_MANIFEST.sha256'))=='1a27937e5334a7cf847dd342897d091042dcedea80b7aa8c177a8ce42025aa4c','original audit manifest')
old_audit_rows=raw(Q/'AUDIT_MANIFEST.sha256').decode().splitlines(); need(len(old_audit_rows)==54,'original audit payload count')
for line in old_audit_rows:
    expected,name=line.split('  ',1); need(sha(raw(Path(name)))==expected,'original audit file unchanged')
need(bp(raw(D/'CORRECTED_READY.json'))==dict(bytes=3949,SHA256='6f2ed87c2b94c57f2cc013c070fa9db2a590649c21b351763e708631bbd2edc7'),'fixed corrected READY')
need(bp(raw(D/'CORRECTED_MANIFEST.json'))==dict(bytes=9771,SHA256='76d15664837686c8468074e169f6a3a23965ae6bcc30d8e370a08347dd47684b'),'fixed corrected manifest')
manifest=load(D/'CORRECTED_MANIFEST.json'); files,dirs=walk(C)
expected={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in manifest['payload_files']}
for name in ('CORRECTED_MANIFEST.json','CORRECTED_READY.json'): expected[name]=fp(D/name)
need(files==expected and dirs=={'.':0o755,'pending-original':0o755} and len(files)==51,'whole current51/1 bytes modes topology')
oldfiles,olddirs=walk(Q/'reviewed-pending'); original,originaldirs=walk(C/'pending-original')
need(original==oldfiles and originaldirs==olddirs and len(original)==22,'entire original22 copied unchanged')
need(all(fp(C/name)==row for name,row in oldfiles.items() if name not in ('PLAN.json','release_three.py')),'all20 other old top-level files unchanged')
receipt=load(C/'BASELINE_CAPTURE_RECEIPT.json')
for row in receipt['payloads']: need(bp(raw(C/row['path']))=={k:row[k] for k in ('bytes','SHA256')},'original8 boundary payload')
oldplan=load(Q/'reviewed-pending/PLAN.json'); plan=load(D/'PLAN.json'); copy=json.loads(json.dumps(plan))
copy['stage_binding_contract']['candidate_root']=oldplan['stage_binding_contract']['candidate_root']
need(copy==oldplan,'sole PLAN description changed')
need(plan['root_stage_adoption'] is None and plan['stage_binding'] is None,'still unbound pending')
oldcode=raw(Q/'reviewed-pending/release_three.py').decode(); code=raw(D/'release_three.py').decode()
need(bp(code.encode())==dict(bytes=43501,SHA256='7a00cb068f052576c3af33671d1fbcc0b15fa3577ef23a3c5d351e91408008b9'),'current helper fixed pin')
need(bp(raw(D/'PLAN.json'))==dict(bytes=11705,SHA256='3608d183c4cd504ce7173012dea1b10594fbf35fded9471914c4dcf8ad75a8e3'),'current PLAN fixed pin')
need(re.findall(r"^PLAN_SHA = '([0-9a-f]{64})'$",code,re.M)==[sha(raw(D/'PLAN.json'))],'sole matching PLAN_SHA')
start="    candidate=relative(binding['candidate_root']);"; end="    baseline=json.loads(bound(p['baseline']));"
old_before,old_rest=oldcode.split(start,1); old_block,old_after=old_rest.split(end,1)
before,rest=code.split(start,1); block,after=rest.split(end,1)
need(before==old_before.replace(sha(raw(Q/'reviewed-pending/PLAN.json')),sha(raw(D/'PLAN.json'))) and after==old_after,'all executable text outside mapping and PLAN_SHA unchanged')
exact_block="""    candidate=relative(binding['candidate_root']); need(candidate=='public' and candidate in sd,'literal actual public candidate root')
    mapped={name:candidate+'/'+name[len('public/'):] for name in TARGETS}
    need({n for n in sf if n.startswith(candidate+'/')}==set(mapped.values()),'candidate namespace contains only the fixed22 mapped website paths')
    candidate_dirs={candidate}|{q.as_posix() for name in mapped.values() for q in Path(name).parents if q.as_posix()!='.'}
    need({n for n in sd if n==candidate or n.startswith(candidate+'/')}==candidate_dirs,'exact fixed candidate directory topology')
    buffers={}
    for name in sorted(TARGETS):
        row=sf[mapped[name]]; b=read(S/mapped[name])
        need(pin(b)=={k:row[k] for k in ('bytes','SHA256')} and row['mode']==0o644,'exact adopted candidate whole payload/mode'); buffers[name]=b
"""
need(start+block==exact_block,'only literal public mapping block')
diff=''.join(difflib.unified_diff(raw(Q/'reviewed-pending/PLAN.json').decode().splitlines(True),raw(D/'PLAN.json').decode().splitlines(True),fromfile='pending-original/PLAN.json',tofile='PLAN.json'))
diff+=''.join(difflib.unified_diff(oldcode.splitlines(True),code.splitlines(True),fromfile='pending-original/release_three.py',tofile='release_three.py'))
need(diff.encode()==raw(D/'MAPPING_CORRECTION.patch'),'entire exact mapping correction patch')
need(bp(raw(D/'ROOT_STAGE_ADOPTION.json'))==dict(bytes=4713,SHA256='8a9900e4b6abe5d9e269175be7742bc3f484af49c0cc5c90e415a3d754c1f4de'),'actual root stage adoption')
need(bp(raw(D/'ROOT_BINDING_DATA.json'))==dict(bytes=12666,SHA256='9d2bf46aa165f99d15645fa6cd5564608c304434b07fb72c06b56b903c66456b'),'actual root binding data')
adoption=load(D/'ROOT_STAGE_ADOPTION.json'); wrapper=load(D/'ROOT_BINDING_DATA.json'); binding=wrapper['stage_binding']
need(wrapper['binding_execution_authorized'] is False and adoption['production_install_Git_deploy_or_tracker_authority'] is False and adoption['independent_stage_audit_PASS'] is True,'data-only private adoption')
need(adoption['status']==plan['root_stage_adoption_required_status'] and binding['status']==plan['stage_binding_required_status'],'actual statuses compatible')
need(set(binding)==set(plan['stage_binding_contract']['required_keys']) and binding['audit_FINAL']==adoption['independent_stage_audit_FINAL'],'typed exact binding/audit pin')
bound(wrapper['root_stage_adoption']); bound(binding['audit_FINAL'])
for key in ('stage_FINAL','stage_manifest','public_payloads'): need(binding[key]==adoption[key],'same adopted stage docs'); bound(binding[key])
stage=P/plan['stage']; sf,sd=walk(stage)
need(sf=={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in binding['stage_files']} and sd==binding['stage_directories'],'actual whole53/6 stage matches typed metadata')
need(len(sf)==53 and len(sd)==7 and binding['candidate_root']=='public','actual public-root stage')
targets=set(plan['scope_paths']); mapped={name:'public/'+name.removeprefix('public/') for name in targets}
need(len(mapped)==22 and all(k==v for k,v in mapped.items()) and {n for n in sf if n.startswith('public/')}==set(mapped.values()),'exact current corrected22 mapping closure')
need({n for n in sd if n=='public' or n.startswith('public/')}=={'public'}|{p.as_posix() for n in mapped.values() for p in Path(n).parents if p.as_posix()!='.'},'corrected candidate directory topology')
need(sorted(adoption['candidate_exact_paths'])==sorted(targets) and adoption['scope']==dict(A=20,M=2,total=22,projected_counts=[747,121,122]),'adopted fixed22 scope')
need(fp(W/'.git/index')=={k:plan['website_index'][k] for k in ('bytes','SHA256','mode')} and fp(P.parent/'.git/index')==plan['Math_index'],'closing current native W/Math pins/modes')
need(sha(raw(Q/'FINAL.json'))=='de8b23a7a14f1ab5682c6abba5d2a78aba23198b16f172a6888a22d0b2e14415','closing original audit unchanged')
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_CORRECTED_STATIC_PREPARATION_ONLY',
    original_audit54payloads_plus2terminals_preserved=True,producer51files1dir_exact=True,original22_and_current8_preserved=True,
    sole_PLAN_description_and_mapping_PLAN_SHA_changes=True,exact_patch=True,all_other_executable_bytes_unchanged=True,
    actual_stage53files6dirs_and22mapping_match=True,actual_private_adoption_false_action_authority=True,
    source703_and_public727_evidence='Original audit data closure preserved; not redundantly recounted here',
    current_native_W_Math_pins_modes_unchanged=True,both_PLAN_action_bindings=None,
    helper_default_preflight_install_Git_import_compile_AST_native_render_or_network_actions=0,
    future_binding_and_runtime_review_required=True,production_authority=False),indent=2))
