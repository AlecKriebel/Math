from pathlib import Path
import hashlib,json,zipfile,zlib,subprocess,sys,shutil,datetime
R=Path(__file__).resolve().parent;C=R.parent;P=C/'publication_package_v3'
h=lambda b:hashlib.sha256(b).hexdigest()
pin=json.loads((C/'PACKAGE_REVIEW_INPUT_V3.json').read_text())
files={str(p.relative_to(P)):{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in sorted(P.rglob('*')) if p.is_file()}
if files!=pin['package_files']:raise RuntimeError('input pin mismatch')
checks=[]
with zipfile.ZipFile(P/'labelled_length_ratio_support.zip') as z:
 if z.testzip() is not None:raise RuntimeError('CRC failure')
 if z.namelist()!=pin['zip_members']:raise RuntimeError('ZIP members mismatch')
 for i in z.infolist():
  b=z.read(i.filename)
  if b!=(P/i.filename).read_bytes():raise RuntimeError('ZIP differs '+i.filename)
  checks.append({'name':i.filename,'bytes':len(b),'sha256':h(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','zip_crc':f'{i.CRC:08x}','timestamp':list(i.date_time),'mode':i.external_attr>>16,'same_as_current':True})
 checksum_lines=(P/'SHA256SUMS.txt').read_text().splitlines()
 for line in checksum_lines:
  digest,name=line.split('  ',1)
  if h((P/name).read_bytes())!=digest:raise RuntimeError('checksum '+name)
 if set(line.split('  ',1)[1] for line in checksum_lines)!=(set(files)-{'SHA256SUMS.txt','labelled_length_ratio_support.zip'}):raise RuntimeError('checksum inventory')
 metadata=json.loads((P/'metadata.json').read_text());deposit=json.loads((P/'zenodo-deposit.json').read_text())
 if metadata!=deposit['metadata']:raise RuntimeError('metadata/deposit')
 if deposit['files']!=[{'path':'labelled_length_ratio.pdf'},{'path':'labelled_length_ratio_support.zip'}]:raise RuntimeError('deposit set')
 runs=[]
 for layout in ['whole_layout','extracted_zip']:
  for mode in ['normal','optimized']:
   D=R/'scratch'/layout/mode
   if D.exists():shutil.rmtree(D)
   D.mkdir(parents=True)
   if layout=='whole_layout':
    shutil.copytree(P,D,dirs_exist_ok=True)
   else:z.extractall(D)
   for script,receipt,count in [('verify_exact.py','verification.json',19458),('exact_reversal_counterexample.py','exact_reversal_counterexample.json',19)]:
    output=D/'verification'/receipt;output.unlink()
    cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(D/'verification'/script)]
    cp=subprocess.run(cmd,cwd=D,capture_output=True,text=True)
    if cp.returncode or not output.exists():raise RuntimeError(cp.stderr)
    got=json.loads(output.read_text());gold=json.loads((P/'verification'/receipt).read_text())
    if got!=gold:raise RuntimeError('receipt differs')
    if got.get('exact_checks',got.get('check_count'))!=count:raise RuntimeError('count differs')
    runs.append({'layout':layout,'mode':mode,'script':script,'exit_code':cp.returncode,'receipt_sha256':h(output.read_bytes()),'receipt_bytes':output.stat().st_size,'count':count,'same_as_recorded':True})
 mutations=[
 ('wrong_physical_sign','verify_exact.py','verification.json','expected_reverse=(-k)%(n-2) if terminal==\'P\' else k','expected_reverse=(-k)%(n-2)'),
 ('wrong_segment_parity','verify_exact.py','verification.json',"side==terminal","side!=terminal"),
 ('wrong_cone_factor','verify_exact.py','verification.json','delta=F(n-2,n)','delta=F(n-2,2*n)'),
 ('wrong_affine_factor','verify_exact.py','verification.json','lam*lam*sum(x*x for x in av)','(lam*lam+1)*sum(x*x for x in av)'),
 ('wrong_witness','exact_reversal_counterexample.py','exact_reversal_counterexample.json','A=(scalar(0),scalar(2))','A=(scalar(0),scalar(3))')]
 negatives=[]
 for name,script,receipt,old,new in mutations:
  for mode in ['normal','optimized']:
   D=R/'scratch'/'negative_controls'/name/mode
   shutil.copytree(P,D,dirs_exist_ok=True)
   target=D/'verification'/script;src=target.read_text()
   if src.count(old)!=1:raise RuntimeError('ambiguous mutation '+name)
   target.write_text(src.replace(old,new))
   output=D/'verification'/receipt;output.unlink()
   cp=subprocess.run([sys.executable]+(['-O'] if mode=='optimized' else [])+[str(target)],cwd=D,capture_output=True,text=True)
   if cp.returncode==0 or output.exists():raise RuntimeError('negative false pass '+name)
   negatives.append({'mutation':name,'mode':mode,'exit_code':cp.returncode,'fresh_success_receipt_exists':output.exists(),'failure':cp.stderr.strip().splitlines()[-1],'mutated_source_sha256':h(target.read_bytes())})
 result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_file_pins':files,'ZIP_members':checks,'ZIP_CRC_pass':True,'checksum_inventory':'exactly 12 source/PDF files, excludes checksum itself and outer ZIP','metadata_deposit_equal':True,'deposit_files':deposit['files'],'runs':runs,'negative_controls':negatives,'status':'PASS'}
 (R/'REPRODUCTION_INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'runs':len(runs),'negative_controls':len(negatives),'status':'PASS'},indent=2))
