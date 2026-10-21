#!/usr/bin/env python3
"""Independent package corruption controls; writes only this review folder."""
import copy, hashlib, importlib.util, json, pathlib, shutil, stat, sys, tempfile, zipfile, subprocess
O=pathlib.Path(__file__).resolve().parent
C=O/'clean'
P=O.parent.parent/'preprint_v1_0'
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    records=[]
    spec=importlib.util.spec_from_file_location('v',C/'verify_support.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    with tempfile.TemporaryDirectory(dir=O,prefix='faults-') as name:
        R=pathlib.Path(name);v.ROOT=R
        members=json.loads((C/'SUPPORT_ALLOWLIST.json').read_text())['members']
        for fn in members:
            target=R/fn;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/fn,target)
        for fn in ['pr1052_support_v1_0.zip','pr1052_support_v1_0.zip.sha256','zenodo-deposit.json']:shutil.copyfile(P/fn,R/fn)
        baseline={fn:(R/fn).read_bytes() for fn in members+['pr1052_support_v1_0.zip','pr1052_support_v1_0.zip.sha256','zenodo-deposit.json']}
        def reset():
            for fn,b in baseline.items():
                p=R/fn
                if p.is_symlink():p.unlink()
                p.write_bytes(b)
        def mutatejson(fn,change):
            p=R/fn;d=json.loads(p.read_text());change(d);p.write_text(json.dumps(d))
        def rehashmanifest():
            mutatejson('SUPPORT_MANIFEST.json',lambda d:d.update(entries=[{'path':e['path'],'bytes':len((R/e['path']).read_bytes()),'sha256':sha((R/e['path']).read_bytes())} for e in d['entries']]))
        def wrapped():v.verify_payload();v.verify_archive(R/'pr1052_support_v1_0.zip',members);v.verify_upload_if_present()
        def record(label,edit,verify,accept=False):
            reset();edit()
            try:verify()
            except (ValueError,KeyError,TypeError,FileNotFoundError,zipfile.BadZipFile) as e:
                need(not accept,'valid control rejected '+label+': '+str(e));records.append({'case':label,'outcome':'rejected','reason':str(e)})
            else:
                need(accept,'fault falsely accepted '+label);records.append({'case':label,'outcome':'accepted'})
        record('actual wrapped baseline',lambda:None,wrapped,True)
        record('descriptor absent clean semantics',lambda:(R/'zenodo-deposit.json').unlink(),lambda:(v.verify_payload(),v.verify_upload_if_present()),True)
        record('modified paper bytes',lambda:(R/'paper.pdf').write_bytes(b'changed'),v.verify_payload)
        record('missing payload file',lambda:(R/'README.md').unlink(),v.verify_payload)
        record('symlink payload file',lambda:((R/'README.md').unlink(),(R/'README.md').symlink_to(R/'LICENSE.txt')),v.verify_payload)
        record('duplicate allowlist',lambda:mutatejson('SUPPORT_ALLOWLIST.json',lambda d:d['members'].append(d['members'][0])),v.verify_payload)
        record('traversal allowlist',lambda:mutatejson('SUPPORT_ALLOWLIST.json',lambda d:d['members'].__setitem__(0,'../x')),v.verify_payload)
        record('manifest missing entry',lambda:mutatejson('SUPPORT_MANIFEST.json',lambda d:d['entries'].pop()),v.verify_payload)
        record('copy map altered digest with rehashed manifest',lambda:(mutatejson('support/COPY_MAP.json',lambda d:d['copies'][0].update(sha256='0'*64)),rehashmanifest()),v.verify_payload)
        for name,change in [('descriptor wrong PDF digest',lambda d:d['files'][0].update(sha256='0'*64)),('descriptor wrong ZIP length',lambda d:d['files'][1].update(bytes=-1)),('descriptor boolean byte count',lambda d:d['files'][0].update(bytes=True)),('descriptor extra file',lambda d:d['files'].append(d['files'][0])),('descriptor extra field',lambda d:d.update(extra=1)),('descriptor wrong metadata',lambda d:d['metadata'].update(title='Wrong'))]:
            record(name,lambda change=change:mutatejson('zenodo-deposit.json',change),v.verify_upload_if_present)
        for label,field,value in [('all surfaces undated notes','notes','This metadata is prepared locally; no deposit or publication occurred.'),('all surfaces wrong date notes','notes','Prepared locally on 2026-10-15 before deposit or publication.'),('all surfaces wrong publication type','publication_type','article')]:
            def edit(field=field,value=value):
                mutatejson('.zenodo.json',lambda d:d.update({field:value}))
                mutatejson('metadata.json',lambda d:d['metadata'].update({field:value}))
                mutatejson('zenodo-deposit.json',lambda d:d['metadata'].update({field:value}))
                rehashmanifest()
            record(label,edit,v.verify_payload)
        for label,field,value in [('ready false required','publication_ready',True),('issues false required','all_issues_resolved',True),('stage exact required','stage','ACCEPTED'),('snapshot date exact required','preparation_snapshot_date','2026-10-13')]:
            record(label,lambda field=field,value=value:(mutatejson('metadata.json',lambda d:d.update({field:value})),rehashmanifest()),v.verify_payload)
        # Closed archive constructor does not import the shipped builder.
        def closed(path,kind=None):
            names=sorted(members)
            if kind=='order':names=list(reversed(names))
            if kind=='duplicate':names.append(names[-1])
            with zipfile.ZipFile(path,'w') as z:
                for index,fn in enumerate(names):
                    zi=zipfile.ZipInfo(fn,(2026,10,14,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_STORED
                    data=baseline[fn]
                    if index==0:
                        if kind=='mode':zi.external_attr=(stat.S_IFREG|0o600)<<16
                        if kind=='symlink':zi.external_attr=(stat.S_IFLNK|0o644)<<16
                        if kind=='time':zi.date_time=(2026,10,13,0,0,0)
                        if kind=='compress':zi.compress_type=zipfile.ZIP_DEFLATED
                        if kind=='bytes':data+=b'changed'
                    z.writestr(zi,data)
            pathlib.Path(str(path)+'.sha256').write_text(sha(path.read_bytes())+'  '+path.name+'\n')
        reset();closed(R/'closed.zip');need((R/'closed.zip').read_bytes()==baseline['pr1052_support_v1_0.zip'],'closed exact build');records.append({'case':'independent closed ZIP equal','outcome':'accepted'})
        for kind in ['order','duplicate','mode','symlink','time','compress','bytes']:
            record('archive '+kind,lambda kind=kind:closed(R/'fault.zip',kind),lambda:v.verify_archive(R/'fault.zip',members))
        record('wrong archive sidecar',lambda:(R/'pr1052_support_v1_0.zip.sha256').write_text('0'*64+'  pr1052_support_v1_0.zip\n'),lambda:v.verify_archive(R/'pr1052_support_v1_0.zip',members))
        for path in ['../x','/x','a/./b','a//b','C:/x','a\\b','x\x00y']:
            record('safe path '+repr(path),lambda:None,lambda path=path:v.safe(path))
        # Even a hash-consistent matching metadata fault must prevent archive creation.
        reset()
        mutatejson('.zenodo.json',lambda d:d.update(notes='undated'))
        mutatejson('metadata.json',lambda d:d['metadata'].update(notes='undated'));rehashmanifest()
        cmd=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])+[str(R/'build_support.py'),'--output','bad.zip']
        q=subprocess.run(cmd,cwd=R,capture_output=True)
        need(q.returncode!=0 and not (R/'bad.zip').exists(),'builder bypassed strict metadata')
        records.append({'case':'hash-consistent undated metadata build','outcome':'rejected','reason':q.stderr.decode().splitlines()[-1]})
    return {'all_passed':True,'accepted':sum(r['outcome']=='accepted' for r in records),'rejected':sum(r['outcome']=='rejected' for r in records),'controls':records,'external_descriptor_scope':'Actual descriptor regular. Optional descriptor symlink handling remains disclosed non-security behavior, unchanged.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
