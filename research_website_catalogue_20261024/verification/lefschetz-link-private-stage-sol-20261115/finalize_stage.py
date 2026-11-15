"""Prepare exact private overlay contracts after actual normal/-O executions.

Never installs, deploys, mutates originals, runs science or launches subprocesses.
"""
from pathlib import Path
import datetime
import json
from stage_common import A,read,obj,sha,need,names,frozen_inputs,records,CSS
from render_stage import validate_buffers,additions


def write(name,value):
    need(not (A/name).exists(),'refuse overwriting final private artifact')
    (A/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    g,source,website,by=frozen_inputs();rows=records(by)
    ledger=obj(A/'EXECUTION_LEDGER.json');need(ledger['actual_tool_exits_recorded'] is True,'actual execution receipts required')
    expected=[('BUILD_NORMAL',0),('BUILD_OPTIMIZED',1),('CONTROLS_NORMAL',0),('CONTROLS_OPTIMIZED',1)]
    need([r['name'] for r in ledger['runs']]==[x[0] for x in expected],'four actual bounded rendering/control runs')
    for r,(name,opt) in zip(ledger['runs'],expected):
        need(r['exit_code']==0 and read(A/r['stderr'])==b'','whole actual stderr/exit')
        body=read(A/r['stdout']);need(sha(body)==r['stdout_SHA256'],'whole execution stdout pin')
        report=json.loads(body);need(report['optimization_level']==opt,'actual distinct interpreter optimization')
        if name.startswith('BUILD'):need(report['actual_all_eleven_buffers_written'] is True,'actual rendering/write, not checker-only')
        else:need(report['fault_count']==9 and all(q['rejected'] is True for q in report['new_memory_only_faults']),'nine actual rejected editorial losses')
    paired={};files=[]
    for path in names(A/'candidate-a/public')[0]:
        relative=path.relative_to(A/'candidate-a/public').as_posix();left=read(path);right=read(A/'candidate-b/public'/relative)
        need(left==right,'all actual normal/-O output bytes identical')
        paired[relative]=left;files.append({'path':relative,'bytes':len(left),'SHA256':sha(left)})
    need([r['path'] for r in files]==[p.relative_to(A/'candidate-b/public').as_posix() for p in names(A/'candidate-b/public')[0]],'whole paired candidate namespaces')
    result=validate_buffers(paired,by,website,rows,g['build_date']);entries,nodes=additions(rows,g['build_date'])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('OVERLAY_MANIFEST.json',{'UTC':now,'files':files,'all_actual_normal_optimized_buffers_identical':True})
    write('STAGE_CONTRACT.json',{'UTC':now,'records':['23570763','23331295'],'baseline_counts':[605,90,91],
          'virtual_counts':[614,92,93],'overlay_paths':[r['path'] for r in files],
          'source_native_asset_order':[['periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'],
                                       ['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf']],
          'only_main_change':'add id="main" to the exact initial main tag','nonhiding_supplemental_css':CSS,
          'index_additions':entries,'sitemap_additions':nodes,'127_mixed_ZIP_encoding_license_omitted':True,
          '128_broad_CCBY_all_three_assets':True,'native_verified_published_count_not_index_count':87,
          'publication_or_canonical_AA_authority':False})
    write('INSTALLATION_PLAN.json',{'UTC':now,'reviewable_private_outputs_only':True,'website_baseline_commit':g['prior_installation_commit'],
          'exact_future_public_relative_paths':[r['path'] for r in files],'existing_aggregate_overlays':['research/index.html','research/sitemap.xml'],
          'new_leaf_files':9,'future_expected_counts':[614,92,93],'actual_all603_unrelated_public_files_protected':True,
          'source_owner_root_paperconfigs_site_core_Sheet_Git_deploy_redirect_contact_changes':[],
          'separate_root_installation_code_audit_and_authority_required':True,'production_installation_authorized':False})
    write('READY.json',{'UTC':now,'status':'PRIVATE_PAIR_RENDERED_READY_FOR_SEPARATE_ROOT_CODE_AND_COPY_ADOPTION',
          'informed_writer_not_new_independent_science':True,**result,'source_scientific_replay':False,
          'root_stage_code_adopted':False,'production_install_authorized':False,'installed':False,'deployed':False,
          'live_verified':False,'browser_verified':False,'native_Sheet_publication_verified':False,
          'canonical_url':None,'AA':None,'follow_up':None})
    print(json.dumps({'status':'PRIVATE_READY',**result,'production_install_authorized':False},indent=2))


if __name__=='__main__':main()
