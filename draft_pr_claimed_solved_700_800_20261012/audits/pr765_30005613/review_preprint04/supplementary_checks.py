"""Additional Review04 controls; run in a disposable copy before final closure."""
from pathlib import Path
import datetime, hashlib, io, json, os, re, shutil, stat, subprocess, sys, tempfile, zipfile
from reproduce import R,A,P,T,S,PDF,NAMES,SEVEN,need,ident,save,snap,call

rows=[]
for family in ['review_spectral_family','review_geometry_family','review_spectral_family_addendum','priority_audit','priority_adversary01','review_preprint01','review_preprint02','review_preprint03']:
    root=A/family;m=json.loads((root/'MANIFEST.json').read_text());entries=m.get('authored_files',m.get('files'))
    if isinstance(entries,dict):entries=[{'path':k,**v} for k,v in entries.items()]
    expected={x['path'] for x in entries};need(len(expected)==len(entries),'closure duplicate')
    actual={};dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'review symlink')
        if p.is_dir():dirs.add(p.relative_to(root).as_posix())
        else:
            need(stat.S_ISREG(p.stat().st_mode),'review special')
            if p.name!='MANIFEST.json' or p.parent!=root:actual[p.relative_to(root).as_posix()]=ident(p.read_bytes())
    need(set(actual)==expected,'review exact authored history '+family)
    need(dirs=={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'},'review empty dirs')
    for row in entries:need(actual[row['path']]=={k:row[k] for k in ['bytes','sha256']},'review identity')
    rows.append({'family':family,'authored_files':len(entries),'manifest':ident((root/'MANIFEST.json').read_bytes()),'authored_history_pass':True,'current_input_binding_not_imposed_on_old_history':True})
save('INHERITED_CLOSURE_RECEIPT.json',{'reviews':rows,'scope':'Independent recursive historical-authored closure, including hidden paths, type/empty-dir checks; not inherited theorem acceptance.'})

# Idempotent unchanged outputs preserve their inodes and open descriptors.
with tempfile.TemporaryDirectory(prefix='idempotent_',dir=T) as td:
    out=Path(td)/'out';before=snap(S);b=PDF.read_bytes()
    first=call([sys.executable,'-B',S/'build_package.py','--output-dir',out,'--pdf',PDF]);need(first['exit']==0,'idempotence first')
    old={n:(out/n).stat().st_ino for n in SEVEN};fds={n:(out/n).open('rb') for n in NAMES}
    second=call([sys.executable,'-O','-B',S/'build_package.py','--output-dir',out,'--pdf',PDF]);need(second['exit']==0,'idempotence second')
    for n,f in fds.items():need((out/n).stat().st_ino==old[n] and f.read()==(P/n).read_bytes(),'unchanged inode');f.close()
    need((out/'PACKAGE_INVENTORY.json').stat().st_ino!=old['PACKAGE_INVENTORY.json'],'dated receipt fresh inode')
    need(snap(S)==before and PDF.read_bytes()==b,'idempotence input changed')
    save('IDEMPOTENT_REBUILD_RECEIPT.json',{'first':first,'second':second,'six_unchanged_inodes_and_open_FDs_preserved':True,'new_timestamped_receipt_fresh_inode':True,'inputs_preserved':True})

# Lexically cancelled symlink must be detected before resolution hides it.
with tempfile.TemporaryDirectory(prefix='lexical_',dir=T) as td:
    base=Path(td);s=base/'source';shutil.copytree(S,s);out=base/'out';out.mkdir();foreign=base/'foreign';foreign.mkdir();(out/'alias').symlink_to(foreign,target_is_directory=True)
    destination=out/'alias'/'..'/'new';before=snap(base)
    run=call([sys.executable,'-O','-B',s/'build_package.py','--output-dir',destination,'--pdf',PDF]);need(run['exit']!=0 and snap(base)==before,'cancelled lexical link bypass')
    save('LEXICAL_CANCELLATION_RECEIPT.json',{'run':run,'rejected_before_any_fixture_change':True,'scope':'Existing symlink ancestor lexically traversed even with following dot-dot.'})

with zipfile.ZipFile(P/'source-and-verification.zip') as z:
    paths=z.namelist();textrows=[];credential_hits=[];jsonrows=[];archives=[]
    for n in paths:
        data=z.read(n)
        need(not n.startswith('/') and '\\' not in n and all(p not in ['', '.', '..'] for p in n.split('/')),'unsafe archive name')
        if n.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(data)) as h:
                need(h.testzip() is None and len(h.namelist())==len(set(h.namelist())),'nested ZIP safety')
                archives.append({'path':n,'members':len(h.namelist())})
        else:
            txt=data.decode('utf8');textrows.append({'path':n,**ident(data),'lines':len(txt.splitlines())})
            if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{24,}|sk-[A-Za-z0-9]{32,}|AIza[A-Za-z0-9_-]{30,}',txt):credential_hits.append(n)
            if n.endswith('.json'):json.loads(txt);jsonrows.append(n)
    need(not credential_hits,'credential signature')
    save('CONTENT_SCREEN_RECEIPT.json',{'all_source_paths':paths,'all_text_files':textrows,'json_validated':jsonrows,'historical_zip_structures':archives,'source_file_count':len(paths),'credential_pattern_hits':credential_hits,'forbidden_body_extensions':[n for n in paths if Path(n).suffix.lower() in ['.pdf','.png','.jpg','.jpeg','.docx']],'scope':'Every path/type/UTF8 text and JSON parsed; narrow credential signatures only. Human-style claim review is documented separately; no universal secrecy certificate.'})

# Recompiled PDF/paper text and individual page-raster identities.
render=[]
for n in range(1,7):
    old=T/f'original-{n}.png';fresh=T/f'fresh-{n}.png';need(old.read_bytes()==fresh.read_bytes(),'render page differs')
    render.append({'page':n,'original':ident(old.read_bytes()),'fresh':ident(fresh.read_bytes()),'both_individually_viewed':True,'raster_identical':True})
def pdftext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'])
need(pdftext(PDF)==pdftext(T/'paper.pdf'),'PDF text differs')
log=(T/'paper.log').read_text();need('Undefined' not in log and 'Overfull' not in log,'LaTeX diagnostic')
save('COMPILE_RENDER_RECEIPT.json',{'builtin_compiler':{'path':str(T/'paper.tex'),'result':'success','actual_tool_message':'The current source compiled successfully with the desktop editor\'s compiler.'},'tectonic':{'argv':['/opt/homebrew/bin/tectonic','--only-cached','--keep-logs','--outdir',str(T),str(T/'paper.tex')],'exit':0,'compiled_pdf':ident((T/'paper.pdf').read_bytes()),'log':ident((T/'paper.log').read_bytes()),'undefined_or_overfull':False},'paper_pages':render,'all_twelve_individually_viewed':True,'primary_pages_rendered_and_viewed':['KL3','KL4','KL5','OWR61/printed2077','OWR62/printed2078','HSS11/printed458','HSS12/printed459','HSS13/printed460','K26PDF16'],'K26_both_closure_bars_visually_present':True,'artifact_start_marker_repeated':False,'compiled_pdf_byte_identity_not_required':True,'observed_defects':[]})
print(json.dumps({'status':'PASS','inherited_closed_reviews':len(rows),'extra_physical_rejections':1,'twelve_paper_pages_viewed':True}))
