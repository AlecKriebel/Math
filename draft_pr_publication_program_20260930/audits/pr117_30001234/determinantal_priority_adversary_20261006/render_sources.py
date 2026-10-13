from pathlib import Path
import hashlib,json,os,subprocess,datetime
ROOT=Path(__file__).resolve().parent
OTHER=ROOT.parent/'primary_source_scope_adversary_20261006/private_sources'
items=[(ROOT/'private_sources/docampo_1011.1930v2.pdf',[1,4,21,22]),(ROOT/'private_sources/mustata_1107.2676v1.pdf',[5,8]),(ROOT/'private_sources/miller_singh_varbaro_1210.6729v2.pdf',[1,2]),(OTHER/'shibuta_takagi_0810.1278v3.pdf',[6,8]),(OTHER/'owr21_2009.pdf',[39])]
receipt={'actual_pid':os.getpid(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[],'children':[]}
for pdf,pages in items:
    data=pdf.read_bytes()
    receipt['inputs'].append({'path':str(pdf),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    for pnum in pages:
        pref=ROOT/'private_renders'/(pdf.stem+'_physical_p'+str(pnum))
        cmd=['/opt/homebrew/bin/pdftoppm','-r','175','-f',str(pnum),'-l',str(pnum),'-singlefile','-png',str(pdf),str(pref)]
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        a,b=p.communicate()
        if p.returncode:raise ValueError('Rendering failed')
        out=Path(str(pref)+'.png');data=out.read_bytes()
        receipt['children'].append({'actual_pid':p.pid,'argv':cmd,'exit_code':p.returncode,'stderr':b.decode(),'output':str(out),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'physical_page_one_based':pnum,'visual_read_not_yet_certified':True})
receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'actual_pid':os.getpid(),'rendered_count':len(receipt['children']),'result':'PASS'}))
