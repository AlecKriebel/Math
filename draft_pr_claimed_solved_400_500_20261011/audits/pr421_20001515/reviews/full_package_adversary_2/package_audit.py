"""Independent custody and safe archive checks; writes only assigned review/private paths."""
import hashlib,json,pathlib,stat,subprocess,zipfile,os,datetime
CASE=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
PRIVATE=CASE/'private_sources/full_package_adversary_2'
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def getjson(p):return json.loads(p.read_text())
def main():
    candidate_path=CASE/'PREPRINT_PACKAGE_CANDIDATE.json'
    manifest_path=CASE/'global_candidate/packet-update-manifest.json'
    receipt_path=CASE/'ROOT_DRAFT_PACKET_UPDATE_RECEIPT.json'
    need(sha(candidate_path.read_bytes())=='0a43f04fde4e6335e7ee852357429310e013dd62d2f9a3da6b81cacb50b0cd41','original candidate drift')
    need(sha(manifest_path.read_bytes())=='91bf12afd644f5166a833386e4061f125f33c52ae8780031cffdc1af01a170e4','update mapping drift')
    need(sha(receipt_path.read_bytes())=='545197fd64e8d107ae6ab53e3388bb0ceada1ff97899006dbad669885c5fc9d7','root custody receipt drift')
    cand=getjson(candidate_path);manifest=getjson(manifest_path);remote=getjson(PRIVATE/'targeted_tree_native_gets.json')
    tree_rows=[]
    for row in remote['responses']:
        obj=json.loads(row['response']['structuredContent']['content'])
        need(obj['sha']==row['sha'] and not obj['truncated'],'tree identity/truncation')
        ordered=sorted(obj['tree'],key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode())
        body=b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in ordered)
        need(gitsha('tree',body)==row['sha'],'Git tree content SHA mismatch')
        tree_rows.append({'sha':row['sha'],'entry_count':len(ordered),'object_sha_verified':True,'truncated':False})
    need(remote['head']['sha']=='2e85a0b10c3793ed1d46726b50efac5a6306b707','wrong head')
    leaves={r['path']:r for r in remote['leaves']}
    entries=manifest['entries'];need(len(entries)==len(cand['candidate_files'])==len(leaves)==53,'wrong count')
    need(set(leaves)=={e['remote_path'] for e in entries},'extra/missing selected file')
    checks=[]
    for e in entries:
        p=CASE/e['local_path'];need(p.is_file() and not p.is_symlink(),'nonordinary candidate file')
        data=p.read_bytes();r=leaves[e['remote_path']]
        need(cand['candidate_files'][e['local_path']]==e['sha256']==sha(data),'candidate SHA drift')
        need(r['type']=='blob' and r['mode']=='100644' and r['size']==len(data),'remote mode/size mismatch')
        need(r['sha']==gitsha('blob',data),'remote Git blob disagrees with local pinned bytes')
        checks.append({**e,'bytes':len(data),'remote_git_blob_sha':r['sha'],'remote_bytes_verified_from_tree':True})
    archive_rows=[]
    inv=getjson(CASE/'publication/ARCHIVE_INVENTORY.json')
    for archive,dirname in [('aim_5_2_source.zip','source'),('aim_5_2_verification.zip','verification')]:
        archivepath=CASE/'publication'/archive
        expected=next(x for x in inv['files'] if x['path']==archive)
        need(sha(archivepath.read_bytes())==expected['sha256'],'archive hash differs')
        dest=PRIVATE/('extracted_'+dirname);dest.mkdir()
        if dirname=='source':names={'preprint.tex','README.md','LICENSE','BIBLIOGRAPHY_POINTERS.json'}
        else:names={r['path'] for r in getjson(CASE/'verification/PUBLIC_OUTPUT_WHITELIST.json')['files']}|{'PUBLIC_OUTPUT_WHITELIST.json'}
        members=[]
        with zipfile.ZipFile(archivepath) as z:
            info=z.infolist();need(len({i.filename for i in info})==len(info),'duplicate ZIP member')
            need(set(z.namelist())==names,'ZIP not exact positive inventory')
            need(z.testzip() is None,'bad ZIP CRC')
            for i in info:
                p=pathlib.PurePosixPath(i.filename)
                need(not p.is_absolute() and '..' not in p.parts and str(p)==i.filename,'unsafe ZIP path')
                need(stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG and not i.is_dir(),'nonregular ZIP member')
                need(not any(t in {'private','private_sources','private_cases','__pycache__','.secrets','.venv'} for t in p.parts),'private ZIP payload')
                need(i.date_time==(2026,10,12,0,0,0),'nondeterministic ZIP date')
                data=z.read(i);local=CASE/('publication/source' if dirname=='source' else 'verification')/i.filename
                need(data==local.read_bytes(),'ZIP bytes differ from global pinned member')
                target=dest/i.filename;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
                members.append({'path':i.filename,'bytes':len(data),'sha256':sha(data)})
        need(sorted(members,key=lambda x:x['path'])==expected['members'],'inventory records differ')
        archive_rows.append({'archive':archive,'sha256':sha(archivepath.read_bytes()),'member_count':len(names),'safe_extracted':True,'members':members})
    (PRIVATE/'tmp').mkdir()
    env={**os.environ,'TMPDIR':str(PRIVATE/'tmp')}
    runs=[]
    for optimized in (False,True):
        argv=['python3','-I','-S','-B']+(['-O'] if optimized else [])+[str(PRIVATE/'extracted_verification/verify_bundle.py')]
        r=subprocess.run(argv,cwd=PRIVATE,env=env,capture_output=True,text=True,timeout=90)
        name='driver_optimized' if optimized else 'driver_normal'
        (OUT/(name+'.json')).write_text(r.stdout);(PRIVATE/(name+'.stderr')).write_text(r.stderr)
        need(r.returncode==0 and not r.stderr,'full driver failure '+r.stderr)
        report=json.loads(r.stdout);need(report['status']=='PASS' and len(report['baseline_runs'])==6 and len(report['negative_controls']['mathematical_data'])==14,'incomplete driver result')
        runs.append({'mode':'-O' if optimized else 'normal','exit_code':r.returncode,'stderr_empty':True,'stdout_sha256':sha(r.stdout.encode()),'baseline_runs':6,'mathematical_negative_runs':14,'sha_negative_runs':3,'relocation':report['relocated_bundle']})
    result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_candidate_sha256':sha(candidate_path.read_bytes()),'update_manifest_sha256':sha(manifest_path.read_bytes()),'root_custody_receipt_sha256':sha(receipt_path.read_bytes()),'actual_head':remote['head']['sha'],'all_53_local_and_remote_pins_match':True,'targeted_nonrecursive_tree_checks':tree_rows,'selected_file_checks':checks,'archives':archive_rows,'full_driver_runs':runs}
    (OUT/'PACKAGE_AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'53_pins':'PASS','13_nonrecursive_trees':'SHA VERIFIED','safe_archives':[r['member_count'] for r in archive_rows],'driver_runs':runs},indent=2))
if __name__=='__main__':main()
