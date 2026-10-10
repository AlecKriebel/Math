from pathlib import Path
import json,hashlib,shutil,subprocess,sys,tempfile,zipfile,stat

def run(packet,manifest,archive,optimized):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(packet/'verify_packet.py'),str(packet),str(manifest),str(archive)]
    cp=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    out=(cp.stdout or cp.stderr).strip()
    try: record=json.loads(out)
    except Exception: record={'raw_output':out[:1000]}
    if 'error' in record:
        record['error']=record['error'].replace(str(packet),'PACKET').replace(str(manifest),'MANIFEST').replace(str(archive),'ARCHIVE')
    return {'exit_code':cp.returncode,'output':record}

def execute(packet,manifest,archive,label):
    results={'label':label,'positive':[],'negative':[],'adversarial':[]}
    for optimized in (False,True):
        r=run(packet,manifest,archive,optimized); results['positive'].append({'optimized':optimized,'location':'original',**r})
        if r['exit_code']!=0: raise ValueError('Positive baseline failed')
        with tempfile.TemporaryDirectory(prefix='four-manifold relocation ') as td:
            td=Path(td); p=td/'packet with spaces'; shutil.copytree(packet,p); m=td/'external manifest.json'; shutil.copy2(manifest,m); z=td/'archive renamed.zip'; shutil.copy2(archive,z)
            r=run(p,m,z,optimized); results['positive'].append({'optimized':optimized,'location':'relocated_with_spaces',**r})
            if r['exit_code']!=0: raise ValueError('Relocation positive failed')
        cases=['changed_status','extra_file','missing_file','symlink','duplicate_manifest_key','zip_byte_corruption', 'empty_directory','root_symlink','manifest_symlink','archive_symlink','manifest_path_traversal','manifest_duplicate_entry','zip_duplicate_entry','zip_path_traversal','zip_symlink','zip_extra_entry','zip_directory_entry','zip_payload_mismatch','false_full_solution_rebound','wrong_part_b_rebound','wrong_turns_rebound']
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='four-manifold negative ') as td:
                td=Path(td); p=td/'packet'; shutil.copytree(packet,p); m=td/'manifest.json'; shutil.copy2(manifest,m); z=td/'archive.zip'; shutil.copy2(archive,z); md=json.loads(m.read_text())
                if case=='changed_status': (p/'status.json').write_bytes((p/'status.json').read_bytes()+b' ')
                elif case=='extra_file': (p/'extra.txt').write_text('x')
                elif case=='missing_file': (p/'README.md').unlink()
                elif case=='symlink': (p/'REPORT.md').unlink(); (p/'REPORT.md').symlink_to('PROOF.md')
                elif case=='duplicate_manifest_key': m.write_text(m.read_text().replace('"problem_id": 2894','"problem_id": 2894, "problem_id": 2894',1))
                elif case=='zip_byte_corruption': z.write_bytes(z.read_bytes()+b'changed')
                elif case=='empty_directory': (p/'empty').mkdir()
                elif case in ('root_symlink','manifest_symlink','archive_symlink'):
                    if case=='root_symlink': target=td/'link'; target.symlink_to(p,target_is_directory=True); p=target
                    elif case=='manifest_symlink': target=td/'link'; target.symlink_to(m); m=target
                    else: target=td/'link'; target.symlink_to(z); z=target
                elif case=='manifest_path_traversal': md['files'][0]['path']='../README.md'; m.write_text(json.dumps(md))
                elif case=='manifest_duplicate_entry': md['files'].append(md['files'][0]); m.write_text(json.dumps(md))
                elif case.startswith('zip_'):
                    with zipfile.ZipFile(z,'w') as out:
                        for f in sorted(p.iterdir()):
                            if case=='zip_symlink' and f.name=='REPORT.md':
                                info=zipfile.ZipInfo(f.name); info.create_system=3; info.external_attr=(stat.S_IFLNK|0o777)<<16; out.writestr(info,'PROOF.md')
                            else: out.writestr(f.name,f.read_bytes()+(b'altered' if case=='zip_payload_mismatch' and f.name=='REPORT.md' else b''))
                        if case=='zip_duplicate_entry': out.writestr('README.md',(p/'README.md').read_bytes())
                        elif case=='zip_path_traversal': out.writestr('../escape.txt','x')
                        elif case=='zip_extra_entry': out.writestr('extra.txt','x')
                        elif case=='zip_directory_entry': out.writestr('empty/','')
                    md['zip']['bytes']=z.stat().st_size; md['zip']['sha256']=hashlib.sha256(z.read_bytes()).hexdigest(); m.write_text(json.dumps(md))
                elif case.endswith('_rebound'):
                    s=json.loads((p/'status.json').read_text())
                    if case=='false_full_solution_rebound': s['full_problem_solved']=True
                    elif case=='wrong_part_b_rebound': s['part_b']='solved'
                    elif case=='wrong_turns_rebound': s['turns_used']=2
                    (p/'status.json').write_text(json.dumps(s))
                    for item in md['files']:
                        if item['path']=='status.json': item['bytes']=(p/'status.json').stat().st_size; item['sha256']=hashlib.sha256((p/'status.json').read_bytes()).hexdigest()
                    m.write_text(json.dumps(md))
                r=run(p,m,z,optimized); record={'optimized':optimized,'case':case,'rejected':r['exit_code']!=0,**r}
                (results['negative'] if case in cases[:6] else results['adversarial']).append(record)
                if r['exit_code']==0: raise ValueError('Negative unexpectedly accepted: '+case)
    return results

if __name__=='__main__':
    if len(sys.argv)!=6: raise SystemExit('Usage: replay_integrity.py PACKET MANIFEST ZIP LABEL OUTPUT_JSON')
    result=execute(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4])
    Path(sys.argv[5]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'label':sys.argv[4],'positive':len(result['positive']),'negative':len(result['negative']),'adversarial':len(result['adversarial']),'all_expected':True}))
