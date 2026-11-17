"""Finite metadata seal only; never imports or replays the assembler."""
from pathlib import Path
import datetime, hashlib, json, os, stat

OWN=Path(__file__).resolve().parent

def pin(p):
    s=p.lstat()
    if not stat.S_ISREG(s.st_mode): raise ValueError('Not regular: '+str(p))
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(s.st_mode)}

def write(name,obj):
    with (OWN/name).open('x') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2); f.write('\n')

def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    terminals=['OWNED_MANIFEST.json','FINAL.json']
    assert all(not (OWN/n).exists() for n in terminals+['ACTUAL_READING_RECEIPT.json'])
    build=json.loads((OWN/'BUILD_RECEIPT.json').read_text())
    assert (OWN/'assembly.exit').read_text()=='0\n' and pin(OWN/'assembly.stderr')['bytes']==0
    for item in build['outputs']:
        assert pin(OWN/item['path'])=={k:item[k] for k in ['bytes','SHA256','mode']}
    for name in ['MAIN','EDITORIAL','citation']:
        filename={'MAIN':'MAIN.html','EDITORIAL':'EDITORIAL.json','citation':'citation.bib'}[name]
        assert pin(OWN/filename)==build[name]
    page='candidate/research/sharp-dyadic-threshold-random-cone/index.html'
    write('ACTUAL_READING_RECEIPT.json',{'UTC':now,'whole_actual_page_head_MAIN_read':{'path':page,**pin(OWN/page)},
        'whole_actual_model_read':{'path':'MODEL.json',**pin(OWN/'MODEL.json')},'Bib_read':pin(OWN/'citation.bib'),
        'whole_assembler_read_before_only_invocation':{'path':'assemble_private.py',**pin(OWN/'assemble_private.py'),'read_tool':'feab11'},
        'whole_page_read_tool':'bcbf09','whole_model_read_tool':'3d398a','whole_build_receipt_Bib_streams_read_tool':'e4ee38',
        'root_authority_whole_read_tool':'e6a5ce','full_native_record_read_tool':'725905','native_asset_API_and_rights_read_tool':'d564ac',
        'assembly_execution_history':[0],'assembly_stderr':pin(OWN/'assembly.stderr'),
        'HTML_renders':0,'HTML_saved_views':[],'browser_error_arrays':None,'native_scientific_program_invocations':0,
        'no_new_source_PDF_render_reused_original7page_reading':True,'no_live_native_PDF_mobile_download_certification':True,
        'prior_roles':'Opaque source custody followed by independent scientific scope; informed editorial draft, not a new blind family.'})
    files=[]; dirs=[]
    for base,names,leaves in os.walk(OWN,followlinks=False):
        for name in names:
            p=Path(base)/name
            assert not p.is_symlink()
            dirs.append({'path':p.relative_to(OWN).as_posix(),'mode':stat.S_IMODE(p.stat().st_mode)})
        for name in leaves:
            p=Path(base)/name
            files.append({'path':p.relative_to(OWN).as_posix(),**pin(p)})
    files.sort(key=lambda x:x['path']); dirs.sort(key=lambda x:x['path'])
    assert not any(x['path'] in terminals for x in files)
    write('OWNED_MANIFEST.json',{'UTC':now,'files':files,'directories':dirs,'root_mode':stat.S_IMODE(OWN.stat().st_mode),
        'exact_terminal_controls':terminals,'regular_files_including_terminals':len(files)+2,'child_directories':len(dirs),
        'includes_ignored_and_literal_empty_artifacts':True,'future_exclusions':[]})
    final={'UTC':now,'record':23205181,'row':177,'status':'PRIVATE_EDITORIAL_READY_FOR_FACT_REVIEW',
        'report':{'path':'REPORT.md',**pin(OWN/'REPORT.md')},'manifest':{'path':'OWNED_MANIFEST.json',**pin(OWN/'OWNED_MANIFEST.json')},
        'page':{'path':page,**pin(OWN/page)},'MAIN':{'path':'MAIN.html',**pin(OWN/'MAIN.html')},
        'head':{'path':'HEAD.html',**pin(OWN/'HEAD.html')},'model':{'path':'MODEL.json',**pin(OWN/'MODEL.json')},
        'Bib':{'path':'citation.bib',**pin(OWN/'citation.bib')},'proposed_path':'/research/sharp-dyadic-threshold-random-cone/',
        'extent':{'regular_files':len(files)+2,'child_directories':len(dirs),'exact_terminal_names':terminals},
        'root_scientific_clearance_bound':True,'full_original_claim_preserved':True,'source69_10_unchanged':True,
        'shared1170CSS_exact':True,'original_native_assets':2,'native_order':['paper.pdf','source-and-audit.zip'],
        'abstract_complete_visible_schema_DC':True,'active_canonical':None,'base':None,'AA':None,'production_URL':None,'follow_up':None,
        'private_noindex':True,'publication_authority':False,'staging_install_Git_deploy_Sheet_authority':False,
        'actual_own_data_assembly_execution_history':[0],'actual_assembly_stderr_bytes':0,
        'native_or_old_helper_or_render_invocations':0,'saved_HTML_views':[],'browser_errors':None,
        'native_PDF_mobile_download_live_certification':False,'prior_informed_scope_role_disclosed':True,
        'outside_contact_or_prepared_individual_outreach':False,'completion_percent_editorial_draft':100,'running_handles':[],'quiescent_after_seal':True}
    write('FINAL.json',final)
    print(json.dumps({'extent':final['extent'],'FINAL':pin(OWN/'FINAL.json'),'manifest':pin(OWN/'OWNED_MANIFEST.json'),'page':final['page'],'MAIN':final['MAIN']}))

if __name__=='__main__': main()
