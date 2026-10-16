"""Continue the journaled review after transient ENOSPC; do not repeat builds."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
import review_checks as r

def main():
    h, b, p, w = r.HERE, r.BASE, r.PAPER, r.WORK
    r.COMMANDS[:] = r.load(h/'COMMAND_RECEIPTS_IN_PROGRESS.json')['commands']
    r.need(len(r.COMMANDS)==44 and r.COMMANDS[-1]['label']=='optimized required missing binding',
           'continuation expects the exact journaled interruption')
    before = r.pins()
    kit=w/'kit';script=kit/'scripts';py=sys.executable;prefix=[py,'-B','-O']
    protected={q.relative_to(kit).as_posix():r.sha(q.read_bytes()) for q in kit.rglob('*') if q.is_file()}
    ancestor=w/'optimized-ancestor-link'
    if not ancestor.is_symlink():ancestor.symlink_to(kit,target_is_directory=True)
    external=w/'optimized-existing'
    if not external.exists():external.write_bytes(b'KEEP')
    targets=[kit/'paper.tex',p/'paper.pdf',w/'optimized-hardlink',w/'optimized-leaf-link',
             ancestor/'absent',kit/'new-member',kit,external,w]
    for writer,option in [('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')]:
        for i,target in enumerate(targets):
            r.command(prefix+[script/writer,option,target],kit,False,'optimized reject '+writer+' target '+str(i))
    r.need(external.read_bytes()==b'KEEP','existing external file changed')
    bootstrap=kit/'MANIFEST.json';saved=bootstrap.read_bytes()
    bootstrap.unlink();bootstrap.symlink_to(w/'absent-bootstrap')
    r.command(prefix+[script/'verify_kit.py'],kit,False,'optimized dangling manifest symlink')
    bootstrap.unlink();bootstrap.write_bytes(saved)
    modified=r.load(bootstrap);modified['records'].append(modified['records'][0])
    bootstrap.write_text(json.dumps(modified))
    r.command(prefix+[script/'verify_kit.py'],kit,False,'optimized duplicate manifest record')
    bootstrap.write_bytes(saved)
    default=w/'DEPOSIT_BINDING.json';default.write_text('{}')
    r.command(prefix+[script/'verify_kit.py'],kit,False,'optimized corrupt present default binding')
    default.unlink()
    outputs=[r.load(w/(mode+'-checks.json')) for mode in ['normal','optimized']]
    r.need(outputs[0]==outputs[1],'portable checker JSON mode difference')
    r.write('PORTABLE_CHECKS_RESULT.json',outputs[0])
    # Both modes reproduce the narrow lexical contract mismatch.
    lexical=w/'lexical-link';lexical.symlink_to(kit,target_is_directory=True)
    finding=[]
    for mode,extra in [('normal',[]),('optimized',['-O'])]:
        literal=str(lexical)+'/../'+mode+'-lexical-output.json'
        got=r.command([py,'-B']+extra+[script/'run_checks.py','--out',literal],kit,
                      label=mode+' finding: lexical symlink dot-dot accepted')
        normalized=w/(mode+'-lexical-output.json')
        r.need(normalized.exists(),'lexical mismatch not reproduced')
        finding.append({'mode':mode,'literal_argument':literal,'normalized_output':str(normalized),
                        'returncode':got.returncode,'existing_input_modified':False})
    r.write('LEXICAL_SYMLINK_FINDING.json',{
        'severity':'P3','observations':finding,
        'why':'abspath removes lexical-link/.. before no_links inspects components; fresh normalized target remains outside inputs',
        'fix':'Reject all lexical symlink components before normalization, or honestly narrow all matching advertised contracts.'})
    own=[]
    for mode,extra in [('normal',[]),('optimized',['-O'])]:
        got=r.command([py,'-B']+extra+[h/'independent_controls.py'],h,
                      label=mode+' independent coordinate and geometry controls')
        value=json.loads(got.stdout);own.append(value);r.write('INDEPENDENT_'+mode.upper()+'.json',value)
    r.need(own[0]==own[1],'independent mode JSON difference')
    current={q.relative_to(kit).as_posix():r.sha(q.read_bytes()) for q in kit.rglob('*') if q.is_file()}
    r.need(protected==current,'scratch protected files changed')
    r.command([py,'-B',b.parents[2]/'zenodo_deposit_tool/zenodo.py','check',p/'zenodo-deposit.json'],b,
              label='real repository uploader LOCAL check')
    # Independently recheck final current archive, custody, and the native objects.
    zpath=p/'pr1094_supportkit_v1.0.zip';buffer=io.BytesIO()
    with zipfile.ZipFile(zpath) as z,zipfile.ZipFile(buffer,'w',compression=0) as out:
        names=z.namelist();r.need(z.testzip() is None and names==sorted(set(names)),'archive inventory/CRC')
        for name in names:
            info=z.getinfo(name);data=z.read(name)
            r.need(data==(kit/name).read_bytes(),'archive payload differs')
            r.need(info.date_time==(1980,1,1,0,0,0) and info.create_system==3
                   and info.external_attr==0o100644<<16 and info.compress_type==0,'archive header')
            new=zipfile.ZipInfo(name,(1980,1,1,0,0,0));new.create_system=3;new.external_attr=0o100644<<16
            out.writestr(new,data)
    r.need(buffer.getvalue()==zpath.read_bytes(),'independent CLOSED archive bytes differ')
    custody=r.load(kit/'CUSTODY_MAP.json');prior=r.load(p/'FROZEN_INPUT_PINS.json')['records']
    originals={row['path']:{k:row[k] for k in ['path','bytes','sha256']} for row in prior}
    for row in custody['copies']:
        data=(kit/row['copy_path']).read_bytes();name=row['original_path']
        r.need({'path':name,'bytes':len(data),'sha256':r.sha(data)}==originals[name],'exact historical copy differs')
    selected={row['original_path'] for row in custody['copies']};omitted={row['path'] for row in custody['exclusions']}
    r.need(not selected&omitted and selected|omitted==set(originals),'custody partition')
    metadata=r.load(kit/'metadata.json')
    r.need(metadata==r.load(kit/'.zenodo.json')==r.load(p/'DEPOSIT_BINDING.json')['metadata']
           ==r.load(p/'zenodo-deposit.json')['metadata'],'native metadata identity')
    r.need(r.load(kit/'metadata_api.json')=={'metadata':metadata},'API metadata wrapper')
    cleanup=r.load(h/'OWN_COMPILE_ARCHIVE_CLEANUP.json')['entries']
    canonical_pdf=r.sha((p/'paper.pdf').read_bytes());canonical_zip=r.sha(zpath.read_bytes())
    for mode in ['normal','optimized']:
        r.need(next(row['sha256'] for row in cleanup if row['path']==mode+'-pdf/paper.pdf')==canonical_pdf,'completed compile hash')
        r.need(next(row['sha256'] for row in cleanup if row['path']==mode+'-support.zip')==canonical_zip,'completed archive hash')
    after=r.pins()
    r.write('COMMAND_RECEIPTS.json',{'commands':r.COMMANDS,'count':len(r.COMMANDS),
                                   'expected_rejections':sum(not x['expected_success'] for x in r.COMMANDS)})
    r.write('REPRODUCTION_RECEIPT.json',{
        'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_WITH_ONE_P3_CONTRACT_FINDING',
        'continuation':'44-command live journal retained across ENOSPC; completed builds not repeated',
        'baseline_inputs_before':before,'baseline_inputs_after':after,'original_git_files':8,
        'archive_members':len(names),'selected_prior_copies':len(selected),'excluded_prior_files':len(omitted),
        'metadata_objects_equal':True,'independent_closed_zip_equal':True,'compiled_pdfs_byte_equal':True,
        'portable_json_modes_equal':True,'independent_json_modes_equal':True,
        'command_count':len(r.COMMANDS),'expected_rejections':sum(not x['expected_success'] for x in r.COMMANDS),
        'candidate_mutation':False,'service_actions':False,'scratch':str(w)})
    print(json.dumps({'status':'PASS_WITH_ONE_P3_CONTRACT_FINDING','commands':len(r.COMMANDS),'inputs':after}))

if __name__=='__main__':main()
