import pathlib, subprocess, datetime, hashlib, json
assert __debug__
r=pathlib.Path(__file__).resolve().parent
pages={'K3':[259,260],'W20':[23,24,25],'BIP':[9,10,14],'T12':[2],'BHW':[2]}
rows=[]
for label,chosen in pages.items():
 for n in chosen:
  dest=r/'tmp'/'pdfs'/f'{label}_page_{n}'
  cmd=['/opt/homebrew/bin/pdftoppm','-f',str(n),'-l',str(n),'-r','110','-singlefile','-png',str(r/'tmp'/'pdfs'/f'{label}.pdf'),str(dest)]
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err=p.communicate()
  finish=datetime.datetime.now(datetime.timezone.utc).isoformat()
  assert p.returncode==0,(label,n,err)
  body=dest.with_suffix('.png').read_bytes()
  rows.append({'label':label,'pdf_one_based_page':n,'argv':cmd,'pid':p.pid,'started_utc':start,'finished_utc':finish,'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'png_bytes':len(body),'png_sha256':hashlib.sha256(body).hexdigest()})
(r/'PRIMARY_RENDER_RECEIPTS.json').write_text(json.dumps({'schema':'pr48-smooth-geometry-fresh-primary-page-renders/v1','rows':rows,'foreign_pngs_transient_only':True},indent=2)+'\n')
print(json.dumps({'rendered_pages':len(rows),'all_exit_codes_zero':True}))
