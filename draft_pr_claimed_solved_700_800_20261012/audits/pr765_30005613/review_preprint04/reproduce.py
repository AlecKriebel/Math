"""Review04 physical controls. Run only in a disposable review copy; writes receipts/tmp."""
from pathlib import Path
import ast, contextlib, datetime, hashlib, importlib.util, io, json, math, os
import shutil, stat, struct, subprocess, sys, tempfile, zipfile, zlib

R=Path(__file__).resolve().parent
A=R.parent
P=A/'preprint'
T=R/'tmp'
S=T/'source'
NAMES=['paper.tex','output/pdf/paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','zenodo-upload-kit.zip']
SEVEN=NAMES+['PACKAGE_INVENTORY.json']
PDF=P/'output/pdf/paper.pdf'
BUNDLED='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'

def need(c,m):
    if not c: raise RuntimeError(m)

def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,obj):(R/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def snap(root):
    out={}
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat(); v={'mode':st.st_mode,'dev':st.st_dev,'inode':st.st_ino,'nlink':st.st_nlink}
        if stat.S_ISREG(st.st_mode):v.update(ident(p.read_bytes()))
        elif stat.S_ISLNK(st.st_mode):v['target']=os.readlink(p)
        out[str(p.relative_to(root))]=v
    return out
def call(argv,env=None):
    e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1'
    if env:e.update(env)
    p=subprocess.run(list(map(str,argv)),cwd='/',env=e,text=True,capture_output=True,timeout=300)
    return {'argv':list(map(str,argv)),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def loadmodule(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def preservation():
    source=(P/'source-and-verification.zip').read_bytes()
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        need(z.testzip() is None,'source CRC')
        names=z.namelist();need(len(names)==len(set(names))==120,'source names')
        need(names==sorted(names),'sort')
        raw={n:z.read(n) for n in names}
    rows=json.loads(raw['MANIFEST.json'])['files'];need(len(rows)==119,'manifest rows')
    need(set(raw)=={x['path'] for x in rows}|{'MANIFEST.json'},'exact inventory')
    for row in rows:need(ident(raw[row['path']])=={k:row[k] for k in ['bytes','sha256']},'manifest identity')
    originals=[]
    for row in json.loads(raw['audit/SNAPSHOT.json'])['files']:
        prefix='unsolved_math_prioritization/attempts/30005613/';name=row['path'][len(prefix):]
        b=raw['historical_candidate/'+name]
        need(b==(A/'original'/row['path']).read_bytes(),'actual immutable original')
        need(ident(b)=={k:row[k] for k in ['bytes','sha256']},'snapshot original')
        originals.append({'path':name,**ident(b)})
    need(len(originals)==39,'original count')
    archives=[]
    hv=json.loads(raw['historical_candidate/VERDICT.json'])
    for row in hv['archives']:
        prefix='historical_candidate/'+row['extracted_directory']+'/'
        expected={n[len(prefix):]:b for n,b in raw.items() if n.startswith(prefix)}
        with zipfile.ZipFile(io.BytesIO(raw['historical_candidate/'+row['path']])) as z:
            need(z.testzip() is None,'historical CRC')
            need(len(z.namelist())==len(set(z.namelist()))==row['members'],'historical exact names')
            need(set(z.namelist())==set(expected),'historical extracted set')
            for name in z.namelist():need(z.read(name)==expected[name],'historical extracted bytes')
        archives.append({'path':row['path'],'members':len(expected),'identity':ident(raw['historical_candidate/'+row['path']])})
    scripts=[];textfiles=[]
    for name,b in raw.items():
        if name.endswith('.py'):
            ast.parse(b.decode(),feature_version=(3,11));scripts.append({'path':name,**ident(b)})
        if not name.endswith('.zip'):
            v=b.decode('utf-8');textfiles.append({'path':name,'lines':len(v.splitlines()),**ident(b)})
    kit=zipfile.ZipFile(P/'zenodo-upload-kit.zip');need(kit.testzip() is None,'kit CRC')
    need(set(kit.namelist())=={'paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','README.md'},'kit names')
    need(kit.read('paper.pdf')==PDF.read_bytes(),'kit PDF');need(kit.read('source-and-verification.zip')==source,'kit source')
    md=json.loads((P/'zenodo-metadata.json').read_bytes())
    need(json.loads(kit.read('zenodo-metadata.json'))==md,'kit metadata')
    need(json.loads((P/'zenodo-deposit.json').read_bytes())['metadata']==md['metadata'],'deposit metadata')
    need(json.loads(kit.read('zenodo-deposit.json'))=={'metadata':md['metadata'],'files':[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}]},'kit deposit two flat files')
    save('PRESERVATION_RECEIPT.json',{'source_files':120,'manifest_rows':119,'originals':originals,'historical_archives':archives,'scripts_311_grammar_only':scripts,'all_text_file_inventory':textfiles,'kit_two_deposit_files':True,'third_party_bodies_included':False,'scope':'Exact preservation and content inventory; syntax is not Python3.11 runtime execution or theorem certification.'})

def streams():
    rows=[]
    for archive in ['source-and-verification.zip','zenodo-upload-kit.zip']:
        data=(P/archive).read_bytes()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            need(z.namelist()==sorted(z.namelist()),'ZIP sorting')
            for info in z.infolist():
                need(info.compress_type==8 and info.date_time==(2026,10,15,0,0,0) and info.external_attr>>16==0o100644,'ZIP settings')
                h=struct.unpack_from('<4s5H3I2H',data,info.header_offset)
                start=info.header_offset+30+h[-2]+h[-1];physical=data[start:start+info.compress_size];raw=z.read(info)
                def compressed(level):
                    c=zlib.compressobj(level,zlib.DEFLATED,-15);return c.compress(raw)+c.flush()
                need(physical==compressed(9),'raw stream not level9')
                rows.append({'archive':archive,'member':info.filename,'raw_level9':True,'differs_default':physical!=compressed(-1)})
    need(len(rows)==125,'stream count');save('COMPRESSION_RECEIPT.json',{'runtime':sys.version,'zlib':zlib.ZLIB_RUNTIME_VERSION,'streams':rows,'scope':'Raw streams in this zlib runtime, no cross-runtime byte guarantee.'})

def replays_builds():
    before=snap(S);rows=[]
    for label,python,flags,env in [('normal',sys.executable,[],{}),('outerO',sys.executable,['-O'],{}),('env2',sys.executable,[],{'PYTHONOPTIMIZE':'2'}),('bundled',BUNDLED,[],{})]:
        r=call([python,*flags,'-B',S/'verify_bundle.py','--pdf',PDF],env);need(r['exit']==0,'replay '+label+str(r));j=json.loads(r['stdout']);need(j['status']=='PASS' and j['inventory_files']==120,'replay status')
        need(snap(S)==before,'replay source mutation');rows.append({'mode':label,**r})
    save('REPLAY_RECEIPT.json',{'replays':rows,'source_unchanged':True,'bundled_version':call([BUNDLED,'--version']),'system_version':sys.version})
    rows=[]
    for label,python,flags in [('normal',sys.executable,[]),('outerO',sys.executable,['-O']),('bundled',BUNDLED,[])]:
        out=T/('rebuild_'+label)
        r=call([python,*flags,'-B',S/'build_package.py','--output-dir',out,'--pdf',PDF]);need(r['exit']==0,'rebuild '+label+str(r))
        identities={}
        for n in NAMES:
            b=(out/n).read_bytes();need(b==(P/n).read_bytes(),'six output byte mismatch '+n);identities[n]=ident(b)
        need({str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()}==set(SEVEN),'seven exact outputs')
        need(snap(S)==before,'build mutated source');rows.append({'mode':label,**r,'six':identities,'exact_seven_outputs':True})
        shutil.rmtree(out)
    save('REBUILD_RECEIPT.json',{'builds':rows,'source_and_pdf_unchanged':True,'receipt_timestamp_excluded':True})

def attacks():
    rows=[]
    def case(label,setup,verifier=False):
        with tempfile.TemporaryDirectory(prefix='attack_',dir=T) as td:
            base=Path(td);s=base/'closed';shutil.copytree(S,s);out=base/'out';out.mkdir();pdf=base/'input.pdf';shutil.copy2(PDF,pdf)
            setup(base,s,out,pdf)
            before=snap(base)
            argv=[sys.executable,'-O','-B',s/('verify_bundle.py' if verifier else 'build_package.py')]
            if not verifier:argv+=['--output-dir',out]
            argv+=['--pdf',pdf]
            r=call(argv,{'PYTHONOPTIMIZE':'2'});need(r['exit']!=0,'attack accepted '+label+str(r));need(snap(base)==before,'attack wrote before rejecting '+label)
            rows.append({'case':label,'exit':r['exit'],'last_error':r['stderr'].splitlines()[-1] if r['stderr'] else '', 'all_fixture_types_inodes_bytes_links_unchanged':True})
    for n in SEVEN:
        for kind in ['directory','fifo','symlink_source','dangling','hardlink_source','hardlink_foreign','hardlink_pdf','pdf_ordinary_overlap']:
            def setup(base,s,out,pdf,n=n,kind=kind):
                p=out/n;p.parent.mkdir(parents=True,exist_ok=True)
                if kind=='directory':p.mkdir()
                elif kind=='fifo':os.mkfifo(p)
                elif kind=='symlink_source':p.symlink_to(s/'paper.tex')
                elif kind=='dangling':p.symlink_to(base/'missing')
                elif kind=='hardlink_source':os.link(s/'paper.tex',p)
                elif kind=='hardlink_foreign':
                    q=base/'valuable';q.write_bytes(b'valuable');os.link(q,p)
                elif kind=='hardlink_pdf':os.link(pdf,p)
                else:
                    p.write_bytes(pdf.read_bytes());pdf.unlink();pdf.symlink_to(p)
            case(n+':'+kind,setup)
    for kind in ['source_ancestor_link','ancestor_directory_link','ancestor_dangling','ancestor_fifo','ancestor_file']:
        def setup(base,s,out,pdf,kind=kind):
            p=out/'output'
            if kind=='source_ancestor_link':p.symlink_to(s,target_is_directory=True)
            elif kind=='ancestor_directory_link':
                q=base/'foreign';q.mkdir();p.symlink_to(q,target_is_directory=True)
            elif kind=='ancestor_dangling':p.symlink_to(base/'absent',target_is_directory=True)
            elif kind=='ancestor_fifo':os.mkfifo(p)
            else:p.write_bytes(b'valuable parent')
        case(kind,setup)
    for kind in ['hidden_file','empty_hidden_dir','fifo_input','symlink_input','changed_tex','missing_review','extra_review','original_rehash','review_pin_rehash','unsafe_dot','unsafe_backslash','duplicate_manifest','manifest_self']:
        def setup(base,s,out,pdf,kind=kind):
            if kind=='hidden_file':(s/'.extra').write_bytes(b'x')
            elif kind=='empty_hidden_dir':(s/'.empty').mkdir()
            elif kind=='fifo_input':os.mkfifo(s/'fifo')
            elif kind=='symlink_input':(s/'link').symlink_to(s/'paper.tex')
            elif kind=='changed_tex':(s/'paper.tex').write_bytes(b'changed')
            elif kind=='missing_review':(s/'audit/review_geometry_family/REPORT.md').unlink()
            elif kind=='extra_review':(s/'audit/review_geometry_family/.added').write_bytes(b'x')
            else:
                p=s/'MANIFEST.json';m=json.loads(p.read_bytes())
                if kind in ['original_rehash','review_pin_rehash']:
                    name='historical_candidate/author/PROOF.md' if kind=='original_rehash' else 'audit/review_geometry_family/MANIFEST.json'
                    q=s/name;q.write_bytes(q.read_bytes()+b'\n')
                    for row in m['files']:
                        if row['path']==name:row.update(ident(q.read_bytes()))
                elif kind=='unsafe_dot':m['files'][0]['path']='audit/./bad'
                elif kind=='unsafe_backslash':m['files'][0]['path']='audit\\bad'
                elif kind=='duplicate_manifest':m['files'].append(m['files'][0])
                else:m['files'].append({'path':'MANIFEST.json',**ident(p.read_bytes())})
                p.write_text(json.dumps(m))
        case(kind,setup,True)
    # Materially distinct same-inode output/output alias and cancelled lexical symlink.
    def alias(base,s,out,pdf):
        p=out/'paper.tex';p.write_bytes(b'valuable');os.link(p,out/'PACKAGE_INVENTORY.json')
    case('two_outputs_share_inode',alias)
    # Invalid bound PDF is rejected without writes.
    case('wrong_pdf_bytes',lambda base,s,out,pdf:pdf.write_bytes(b'%PDF-wrong'))
    save('PHYSICAL_ATTACKS.json',{'rejections':len(rows),'rows':rows,'scope':'Physical ordinary static fixtures; no hostile concurrency, race or security certification.'})

def atomic():
    out=T/'atomic';out.mkdir();fds=[];old={};source=snap(S);pdf=PDF.read_bytes()
    for n in SEVEN:
        p=out/n;p.parent.mkdir(parents=True,exist_ok=True);b=('review04 old '+n).encode();p.write_bytes(b);fds.append((n,p.open('rb')));old[n]={'inode':p.stat().st_ino,'bytes':b}
    r=call([sys.executable,'-B',S/'build_package.py','--output-dir',out,'--pdf',PDF]);need(r['exit']==0,'atomic build')
    rows=[]
    for n,f in fds:
        p=out/n;need(f.read()==old[n]['bytes'],'old FD changed');f.close();need(p.stat().st_ino!=old[n]['inode'],'inode reused');need(p.stat().st_nlink==1 and stat.S_ISREG(p.stat().st_mode),'not ordinary output');rows.append({'path':n,'old_fd_preserved':True,'fresh_regular_single_link_inode':True})
    need({str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()}==set(SEVEN),'atomic unexpected files');need(snap(S)==source and PDF.read_bytes()==pdf,'atomic input mutation');shutil.rmtree(out)
    save('ATOMIC_REPLACEMENT_RECEIPT.json',{'run':r,'seven_outputs':rows,'no_leftover_temps':True,'inputs_preserved':True})

def comparator():
    sys.path.insert(0,str(S));m=loadmodule('bundle04',S/'verify_bundle.py');rows=[]
    tests=[('exact',{'x':[1,True,'a',0.0]},{'x':[1,True,'a',0.0]},True),('rounding',1.0,1.0+5e-13,True),('large',1.,1.+2e-12,False),('tiny_zero',0.,1e-310,False),('nan',float('nan'),float('nan'),False),('posinf',float('inf'),float('inf'),False),('neginf',float('-inf'),float('-inf'),False),('intfloat',1,1.,False),('boolint',True,1,False),('tuplelist',(1,),[1],False),('count',4187,4186,False),('keys',{'a':1},{'b':1},False),('length',[1],[1,2],False),('string','1','01',False),('nested',{'a':[1]},{'a':[True]},False),('negative',-1.,-1.-5e-13,True)]
    for label,a,b,expected in tests:
        try:m.compare_diagnostics(a,b);accepted=True
        except ValueError:accepted=False
        need(accepted==expected,'comparator '+label);rows.append({'case':label,'expected_accept':expected,'accepted':accepted})
    save('COMPARATOR_RECEIPT.json',{'cases':rows,'relative_float_tolerance':1e-12,'absolute':0,'all_nonfloat_types_shapes_values_strict':True})

if __name__=='__main__':
    need(S.is_dir(),'Extract source into owned tmp/source first')
    preservation();streams();replays_builds();attacks();atomic();comparator()
    print(json.dumps({'status':'PASS','physical_rejections':json.loads((R/'PHYSICAL_ATTACKS.json').read_text())['rejections'],'review_work_not_formal_PDE_certificate':True}))
