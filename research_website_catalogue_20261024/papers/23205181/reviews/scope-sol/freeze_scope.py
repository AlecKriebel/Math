"""One data-only finite seal; no scientific program or project helper runs."""
from pathlib import Path
import datetime, hashlib, json, os, stat

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
CACHE = Path('/Users/alec/Documents/Math/openai_wreath_planar_consequences/sources/family197')
RECEIPT = CACHE.parents[1] / 'target_a/source_receipt.json'

def pin(p):
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError('Not regular: ' + str(p))
    b = p.read_bytes()
    return {'bytes':len(b), 'SHA256':hashlib.sha256(b).hexdigest(), 'mode':stat.S_IMODE(s.st_mode)}

def census(root):
    files, dirs = [], []
    for base, names, leaves in os.walk(root, followlinks=False):
        for name in names:
            p = Path(base)/name
            if p.is_symlink():
                raise ValueError('Symlink: ' + str(p))
            dirs.append({'path':p.relative_to(root).as_posix(), 'mode':stat.S_IMODE(p.stat().st_mode)})
        for name in leaves:
            p = Path(base)/name
            files.append({'path':p.relative_to(root).as_posix(), **pin(p)})
    return sorted(files,key=lambda x:x['path']), sorted(dirs,key=lambda x:x['path'])

def write(name, obj):
    with (OWN/name).open('x') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')

def main():
    terminals = ['MANIFEST.json','FINAL.json']
    if any((OWN/n).exists() for n in terminals+['FINAL_CUSTODY.json','POST_INITIAL_READING_RECEIPT.json']):
        raise FileExistsError('Do not overwrite a seal')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    initial = json.loads((OWN/'INITIAL_MANIFEST.json').read_text())
    for r in initial['payload_files']:
        if pin(OWN/r['path']) != {k:r[k] for k in ('bytes','SHA256','mode')}:
            raise ValueError('INITIAL payload changed: '+r['path'])
    assert pin(OWN/'INITIAL_MANIFEST.json')['SHA256']=='db2eb8815e486ca47649b1c07dd940052e118182385d31b90c6456a97ff5a6f1'
    assert pin(OWN/'INITIAL_SEAL.json')['SHA256']=='abb949246480289a1f7f77c5d2de31871c71a15f14209ebf5db3e910ef1e1806'
    assert stat.S_IMODE((OWN/'pixels').stat().st_mode)==493
    expected=json.loads((OWN/'INITIAL_SOURCE_GUARDS.json').read_text())
    source_files,source_dirs=census(SOURCE)
    assert source_files==expected['files'] and source_dirs==expected['directories']
    assert len(source_files)==69 and len(source_dirs)==10
    receipt_pin=pin(RECEIPT)
    assert receipt_pin['bytes']==5272 and receipt_pin['SHA256']=='d3f71c2398704a01208f88dedb267a6e6d9093ac85d23e6ebf9a61e81078701d'
    r=json.loads(RECEIPT.read_text())
    assert r['commit']=='adc7f1241b42e322a6451854ab7e4b4c146bf78a'
    primaries=[]
    for item in r['sources']:
        p=CACHE/Path(item['path']).name
        actual=pin(p)
        assert actual['bytes']==item['bytes'] and actual['SHA256']==item['sha256']
        primaries.append({'path':str(p),**actual,'git_blob_SHA1_from_receipt':item['git_blob_sha1'],'reading':'whole actual TeX body personally read after INITIAL'})
    tree=SOURCE/'published-source/container-001/tree'
    code=[{'path':str(tree/'verification'/n),**pin(tree/'verification'/n),'whole_actual_body_personally_read_before_any_native_run':True} for n in ['verify.py','verify_parameter.py','verify_plane32.py','verify_embedding.py','reproduce.py']]
    write('POST_INITIAL_READING_RECEIPT.json',{
        'UTC':now,'primary_commit':r['commit'],'raw_cache_receipt':{'path':str(RECEIPT),**receipt_pin},
        'cached_primary_bodies':primaries,'fresh_remote_equivalence_claim':False,'new_GETs':0,
        'native_code_read':code,'native_routes_executed':['verification/verify_plane32.py (once; no flags)'],
        'archived_parameter_audit_after_initial_and_direct_primary_proofs':{'path':str(tree/'notes/EXTENSION_PARAMETER_AUDIT.md'),**pin(tree/'notes/EXTENSION_PARAMETER_AUDIT.md')},
        'current_peer_root_findings_read':False,'exact_exposure_qualifications':'REPORT.md and NATIVE_READING_AND_SAFETY.md',
        'figures_of_cached_primary_not_inspected':True,'historical_HNN_ring_citations_not_fetched':True,
        'full_native_Description_and_LICENSES_LICENSE_CODE_read_postinitial':True})
    run=json.loads((OWN/'PLANE32_RUN.json').read_text())
    assert run['exit']==0 and pin(OWN/'plane32.stderr')['bytes']==0
    assert (OWN/'plane32.exit').read_text()=='0\n' and (OWN/'launcher.exit').read_text()=='0\n'
    write('FINAL_CUSTODY.json',{'UTC':now,'source_root':str(SOURCE),'files':source_files,'directories':source_dirs,
        'entire_source_69_10_bytes_modes_topology_exact':True,'entire_initial_23_1_preserved':True,
        'INITIAL_manifest':pin(OWN/'INITIAL_MANIFEST.json'),'INITIAL_seal':pin(OWN/'INITIAL_SEAL.json'),
        'all_new_writes_owned_only':True,'native_run_count':1,'native_run_exit_history':[0],
        'reading_tool_exit_history':[0,0],'no_current_peer_root_findings_opened':True,'running_handles':[]})
    files,dirs=census(OWN)
    assert not any(x['path'] in terminals for x in files)
    manifest={'UTC':now,'schema':'finite-full-original-scope-v1','payload_files':files,'directories':dirs,
        'root_mode':stat.S_IMODE(OWN.stat().st_mode),'exact_terminal_controls':terminals,
        'regular_files_including_exact_terminals':len(files)+2,'child_directories':len(dirs),
        'entire_namespace_including_ignored_empty_and_rasters':True,'future_exclusions':[]}
    write('MANIFEST.json',manifest)
    final={'UTC':now,'record':23205181,'row':177,'family':'independent scientific scope',
        'status':'PASS_FULL_ORIGINAL_MATHEMATICAL_SCOPE','substantive_gap':None,'follow_up':None,'AA':None,
        'report':{'path':'REPORT.md',**pin(OWN/'REPORT.md')},
        'source_first_hand_proof':{'path':'HAND_PROOF.md',**pin(OWN/'HAND_PROOF.md')},
        'post_primary_proof':{'path':'POST_PRIMARY_PROOF.md',**pin(OWN/'POST_PRIMARY_PROOF.md')},
        'manifest':{'path':'MANIFEST.json',**pin(OWN/'MANIFEST.json')},
        'extent':{'regular_files':len(files)+2,'child_directories':len(dirs),'terminal_names':terminals},
        'initial_23_1_unchanged':True,'source_69_10_unchanged':True,
        'initial_seal_SHA256':'abb949246480289a1f7f77c5d2de31871c71a15f14209ebf5db3e910ef1e1806',
        'actual_native_run_count':1,'actual_native_exit_history':[0],'actual_native_stderr_bytes':0,
        'native_scope':'Finite field/projective incidence/Fano/inverse pairing; no matching, group presentation, asphericity or target multiplication certified by code.',
        'full_claim_reviewed':True,'prior_opaque_source_role_and_native_audit_assertions_disclosed':True,
        'archived_parameter_audit_only_after_own_initial_and_direct_primary_review':True,
        'current_peer_root_findings_opened_before_final':False,'outside_contact_or_outreach':False,
        'formal_verification_human_refereeing_universal_priority_or_publication_authority':False,
        'tool_wrapper_parse_and_truncated_read_qualifications_preserved':'POST_INITIAL_RESUME.json and REPORT.md',
        'completion_percent_review':100,'running_handles':[],'quiescent_after_seal':True}
    write('FINAL.json',final)
    print(json.dumps({'extent':final['extent'],'FINAL':pin(OWN/'FINAL.json'),'MANIFEST':pin(OWN/'MANIFEST.json'),'REPORT':pin(OWN/'REPORT.md')}))

if __name__=='__main__':
    main()
