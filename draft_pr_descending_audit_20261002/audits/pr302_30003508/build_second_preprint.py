"""Capture a revised PDF export from the same native-editor authoring source."""
import datetime,gzip,hashlib,json,os,re,stat,subprocess,sys
from pathlib import Path
R=Path('/Users/alec/Documents/Math');A=Path(__file__).resolve().parent
F=A/'preprint_package_v02';AUTHOR=A/'preprint_package_v01/spectral_tensor_consistency.tex'
W=F/'private_build_01'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,m):
    if not ok:raise RuntimeError(m)
def pin(p):
    require(p.is_file() and not p.is_symlink(),'Regular input required')
    b=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def main():
    require(not sys.flags.optimize,'Optimization forbidden')
    native=json.loads((F/'ROOT_NATIVE_EDITOR_COMPILE_ACCEPTANCE.json').read_bytes())
    require(native['actual_tool_result_status']=='success'
            and native['compiled_authoring_source']==pin(AUTHOR),'Actual native editor compile for this source is required')
    require(AUTHOR.read_bytes()==(F/'spectral_tensor_consistency.tex').read_bytes(),'Authoring and package source differ')
    W.mkdir(exist_ok=False);(W/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    before=pin(AUTHOR);package_before=pin(F/'spectral_tensor_consistency.tex')
    archive_before=pin(F/'spectral_tensor_verification.zip')
    (W/'INPUT_TEX_AT_EXPORT.tex').write_bytes(AUTHOR.read_bytes())
    build=W/'export';build.mkdir();pages=W/'pages';pages.mkdir();captures=[]
    def run(label,argv):
        d=W/label;d.mkdir()
        request={'actual_launcher_PID':os.getpid(),'launcher_argv':sys.argv,'argv':argv,'cwd':str(R),'requested_UTC':now(),'executed_recorder_source':pin(Path(__file__).resolve()),'recorder_interpreter':pin(Path(sys.executable).resolve()),'child_binary':pin(Path(argv[0]).resolve()),'optimization':sys.flags.optimize,'manuscript':before,'retained_full_source':pin(W/'executed_source.py'),'retained_full_manuscript':pin(W/'INPUT_TEX_AT_EXPORT.tex')}
        (d/'request.json').write_text(json.dumps(request,indent=2)+'\n')
        start=now();child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (d/'started.json').write_text(json.dumps({'actual_PID':child.pid,'started_UTC':start,'outcome':'PENDING'})+'\n')
        out,err=child.communicate();result={**request,'actual_PID':child.pid,'started_UTC':start,'completed_UTC':now(),'exit_code':child.returncode}
        for stream,body in [('stdout',out),('stderr',err)]:
            p=d/(stream+'.bin.gz');p.write_bytes(gzip.compress(body,mtime=0));require(gzip.decompress(p.read_bytes())==body,'Compressed full stream roundtrip differs')
            result[stream]={'logical_bytes':len(body),'logical_sha256':sha(body),'stored':pin(p)}
        (d/'execution.json').write_text(json.dumps(result,indent=2)+'\n');captures.append(result)
        require(child.returncode==0,'Actual export/read/render failure; retain all state');return out
    run('tectonic_export',['/opt/homebrew/bin/tectonic','--only-cached','--keep-logs','--outdir',str(build),str(AUTHOR)])
    pdf=build/'spectral_tensor_consistency.pdf'
    info=run('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(pdf)])
    run('pdf_text',['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(W/'full_pdf_text.txt')])
    run('render_all_pages',['/opt/homebrew/bin/pdftoppm','-png','-r','90',str(pdf),str(pages/'page')])
    count=int(re.search(rb'^Pages:\s+(\d+)\s*$',info,re.M).group(1))
    require(count==len(list(pages.glob('*.png'))) and count>0,'Rendered page count differs')
    require(pin(AUTHOR)==before and pin(F/'spectral_tensor_consistency.tex')==package_before and pin(F/'spectral_tensor_verification.zip')==archive_before,'Export inputs changed')
    final=F/'spectral_tensor_consistency.pdf';require(not final.exists(),'Existing second candidate PDF must not be overwritten')
    final.write_bytes(pdf.read_bytes());require(final.read_bytes()==pdf.read_bytes(),'Exported PDF copy differs')
    receipt={'UTC':now(),'actual_recorder_PID':os.getpid(),'status':'PASS_ACTUAL_REVISED_EXPORT_AND_ALL_PAGE_RENDER_PENDING_VISUAL_REVIEW','source':package_before,'same_editor_authoring_source':before,'native_editor_compile_receipt':pin(F/'ROOT_NATIVE_EDITOR_COMPILE_ACCEPTANCE.json'),'PDF':pin(final),'page_count':count,'pages':[pin(pages/('page-'+str(i)+'.png')) for i in range(1,count+1)],'actual_native_processes':captures,'new_ZIP_preserved':archive_before,'visual_acceptance':False,'publication_clearance':False}
    with (F/'BUILD_RECEIPT.json').open('x') as stream:stream.write(json.dumps(receipt,indent=2)+'\n')
    with (F/'RESEARCH_LOG.md').open('a') as stream:stream.write('\n'+now()+'. Actual native editor compile and separately captured cached export succeeded for the revised source. '+str(count)+' pages are rendered; whole-page visual acceptance and portable replay are still pending. Estimates: math100%; bounded priority100%; publication workflow55%. No service or Git mutation.\n')
    print(json.dumps({'status':receipt['status'],'actual_PID':os.getpid(),'PDF':receipt['PDF'],'page_count':count},indent=2))
if __name__=='__main__':main()
