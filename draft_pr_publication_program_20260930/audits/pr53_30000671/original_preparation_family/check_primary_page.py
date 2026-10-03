"""Fresh official-source download, hash, selected-page rendering; no PDF publication copy."""
import datetime, hashlib, json, pathlib, subprocess, tempfile, urllib.request
F=pathlib.Path(__file__).resolve().parent
URL='https://publications.mfo.de/bitstream/handle/mfo/2988/OWR_2007_02.pdf?isAllowed=y&sequence=1'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    with urllib.request.urlopen(URL,timeout=40) as response:
        pdf=response.read(); final_url=response.geturl()
        headers={k:response.headers[k] for k in ['Content-Type','Content-Length','Last-Modified'] if k in response.headers}
    assert pdf.startswith(b'%PDF-')
    expected=json.loads((F/'original_archive/source_checksums.json').read_text())['original_report']
    assert len(pdf)==expected['bytes'] and sha(pdf)==expected['sha256']
    private=F/'private_primary_reference';private.mkdir(exist_ok=False)
    calls=[]
    with tempfile.TemporaryDirectory(prefix='pr53-source-') as td:
        p=pathlib.Path(td)/'original.pdf';p.write_bytes(pdf)
        for name,argv in [('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(p)]),('page24',['/opt/homebrew/bin/pdftoppm','-f','24','-l','24','-r','100','-singlefile','-png',str(p),str(private/'owr_2007_02_printed106')])]:
            start=datetime.datetime.now(datetime.timezone.utc).isoformat()
            proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err=proc.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
            (private/(name+'_stdout.bin')).write_bytes(out);(private/(name+'_stderr.bin')).write_bytes(err)
            calls.append({'pid':proc.pid,'argv':argv,'started_at':start,'completed_at':end,'exit_code':proc.returncode,'stdout':{'path':name+'_stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'path':name+'_stderr.bin','bytes':len(err),'sha256':sha(err)}})
            assert proc.returncode==0
            if name=='pdfinfo':assert 'Pages:           56' in out.decode()
    img=private/'owr_2007_02_printed106.png'
    record={'schema':'pr53-fresh-primary-source/v1','url':URL,'resolved_url':final_url,'headers':headers,'pdf_bytes':len(pdf),'pdf_sha256':sha(pdf),'matches_original_source_manifest':True,'full_pdf_retained':False,'selected_pdf_page':24,'printed_page':106,'selected_page_png':{'path':str(img.relative_to(F)),'bytes':img.stat().st_size,'sha256':sha(img.read_bytes())},'actual_subprocesses':calls,'no_counterexample_construction_proof_available_in_report':True,'render_is_private_reference_not_publication_content':True}
    (F/'FRESH_PRIMARY_DOWNLOAD.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['pdf_bytes','pdf_sha256','matches_original_source_manifest','selected_pdf_page','printed_page','full_pdf_retained']}))
if __name__=='__main__':main()
