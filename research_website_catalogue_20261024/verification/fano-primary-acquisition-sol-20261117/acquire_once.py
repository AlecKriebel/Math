"""One opaque cache acquisition plus Poppler metadata/text extraction; no research execution."""
import datetime,hashlib,json,os,re,stat,subprocess,time
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');OWN=P/'verification/fano-primary-acquisition-sol-20261117';PAYLOAD=P/'papers/23411227/reviews/root-continuation-20261117/primary'
ROOTS={'native_source':P/'papers/23411227/sources','root_INITIAL':P/'papers/23411227/reviews/root-initial-20261117'}
EXPECTED={'native_source':(196,21),'root_INITIAL':(18,1)}
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink(),str(p)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  z=os.fstat(fd);assert (a.st_dev,a.st_ino)==(z.st_dev,z.st_ino)
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
  q=os.fstat(fd);assert (z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)==(q.st_dev,q.st_ino,q.st_mode,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
  assert len(b)==q.st_size;return b
 finally:os.close(fd)
def pin(p):
 b=raw(p);z=p.stat();return dict(bytes=len(b),SHA256=sha(b),mode=format(stat.S_IMODE(z.st_mode),'04o'))
def census(root):
 files={};dirs={};pending=[root]
 while pending:
  here=pending.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
  entries=sorted(here.iterdir());rel=here.relative_to(root).as_posix();d=dict(mode=format(stat.S_IMODE(a.st_mode),'04o'),empty=not entries,mtime_ns=a.st_mtime_ns,ctime_ns=a.st_ctime_ns)
  if rel=='.':rootpin=d
  else:dirs[rel]=d
  for p in entries:
   z=p.lstat();assert not p.is_symlink()
   if stat.S_ISDIR(z.st_mode):pending.append(p)
   else:files[p.relative_to(root).as_posix()]=dict(**pin(p),hidden=any(x.startswith('.') for x in p.relative_to(root).parts),empty=z.st_size==0,mtime_ns=z.st_mtime_ns,ctime_ns=z.st_ctime_ns)
  z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
 return dict(root=str(root),root_metadata=rootpin,files=files,directories=dirs)
def save(n,d):
 with (OWN/n).open('x') as f:json.dump(d,f,indent=2);f.write('\n')
assert PAYLOAD.is_dir() and not PAYLOAD.is_symlink() and not list(PAYLOAD.iterdir())
ignore=raw(P/'.gitignore');boundary='/papers/23411227/reviews/root-continuation-20261117/primary/'
assert len(ignore)==5846 and sha(ignore)=='256b1359b16a7f339a93be38430e696ee93a48db784c984d08bb8d736059c1e6' and boundary in ignore.decode().splitlines()
before={n:census(p) for n,p in ROOTS.items()}
for n,(nf,nd) in EXPECTED.items():assert (len(before[n]['files']),len(before[n]['directories']))==(nf,nd)
assert before['root_INITIAL']['files']['INITIAL_SEAL.json']['SHA256']=='7d2c5575923b6b56ef4c4c77150a2d52a4e7ba82b71d85f2d68b13a704ce72f2'
assert before['root_INITIAL']['files']['INITIAL_MANIFEST.json']['SHA256']=='ab3298ed377b33150f9b9fa8f4d2b5900298459bdff82c30c4d172cf7f528ea0'
assert before['root_INITIAL']['root_metadata']['mode']=='0555' and all(v['mode']=='0444' for v in before['root_INITIAL']['files'].values()) and set(v['mode'] for v in before['root_INITIAL']['directories'].values())=={'0555'}
save('GUARDS_BEFORE.json',before)
inputs=json.loads(raw(OWN/'INPUT_IDENTITIES.json'));metadata=Path(inputs['metadata_path']);assert sha(raw(metadata))==inputs['metadata_SHA256']
names={'OWR':'OWR-2022-17','MW':'MW-arxiv-2401.13999v2','LL':'LL-arxiv-2103.06439v6','WZ':'WZ-toric-pinned','HL':'HL-arxiv-2009.01010v1','HLYTD':'HLYTD-g-soliton-pinned','BLXZ':'BLXZ-arxiv-2103.15278v2'}
locators={'OWR':[r'\b888\b',r'\b889\b',r'Harold\s+Blum'], 'MW':[r'3\.1\.',r'Theorem\s+3\.1\b',r'Theorem\s+3\.2\b'],'LL':[r'6\.\s',r'6\s+Examples'],'WZ':[r'Theorem\s+1\.1\b'],'HL':[r'Definition\s+4\.1\b',r'Theorem\s+5\.3\b',r'Theorem\s+1\.5\b',r'Remark\s+2\.45\b'],'HLYTD':[r'Corollary\s+31\b',r'Proposition\s+32\b'],'BLXZ':[r'Definition\s+2\.2\b',r'Theorem\s+1\.2\b',r'Theorem\s+1\.3\b']}
records=[];commands=[]
def run(argv,out,err):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with out.open('xb') as stdout,err.open('xb') as stderr:r=subprocess.run(argv,stdout=stdout,stderr=stderr,check=False)
 row=dict(argv=argv,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,exit_code=r.returncode,stdout=dict(path=str(out),**pin(out)),stderr=dict(path=str(err),**pin(err)),one_invocation_no_retry=True)
 commands.append(row);return row
for item in inputs['primaries']:
 label=item['label'];cache=Path(item['cache_path']);body=raw(cache);cachepin=pin(cache)
 assert (len(body),sha(body))==(item['declared_bytes'],item['declared_SHA256']),(label,'Cache identity mismatch')
 assert body.startswith(b'%PDF-'),label
 stem=names[label];pdf=PAYLOAD/(stem+'.pdf');text=PAYLOAD/(stem+'.text.txt')
 with pdf.open('xb') as f:f.write(body)
 assert raw(pdf)==body and pin(cache)==cachepin
 info=run(['/opt/homebrew/bin/pdfinfo',str(pdf)],PAYLOAD/(stem+'.pdfinfo.stdout.txt'),PAYLOAD/(stem+'.pdfinfo.stderr.txt'))
 extraction=run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(text)],PAYLOAD/(stem+'.pdftotext.stdout.txt'),PAYLOAD/(stem+'.pdftotext.stderr.txt'))
 rec=dict(**item,acquisition='Exact pinned pre-existing cache copied; no direct HTTP/curl used for this payload',source_cache_actual=cachepin,payload_pdf=dict(path=str(pdf),**pin(pdf)),cache_and_payload_whole_bytes_equal=True,pdfinfo=info,pdftotext=extraction,complete=False)
 if info['exit_code']==0 and extraction['exit_code']==0 and text.is_file():
  content=raw(text);decoded=content.decode('utf-8');infotext=raw(Path(info['stdout']['path'])).decode('utf-8',errors='replace');page=re.search(r'^Pages:\s*(\d+)\s*$',infotext,re.M)
  rec['pdf_pages']=int(page.group(1)) if page else 'PDFINFO_PAGES_UNAVAILABLE'
  rec['payload_text']=dict(path=str(text),**pin(text));rec['observed_arxiv_stamps']=list(dict.fromkeys(re.findall(r'arXiv\s*:\s*\d{4}\.\d{4,5}v\d+(?:\s*\[[^\]]+\])?(?:\s+\d{1,2}\s+[A-Za-z]+\s+\d{4})?',decoded)))[:4]
  rec['locator_occurrences']=[dict(pattern=pattern,matches=[dict(character_offset=m.start(),text_line=decoded.count('\n',0,m.start())+1,PDF_page=decoded.count('\f',0,m.start())+1) for m in list(re.finditer(pattern,decoded,re.I))[:20]]) for pattern in locators[label]]
  expected={'MW':'2401.13999v2','LL':'2103.06439v6','HL':'2009.01010v1','BLXZ':'2103.15278v2'}
  if label in expected:rec['requested_version_stamp_found']=bool(re.search(r'arXiv\s*:\s*'+re.escape(expected[label]),decoded))
  if label=='OWR':rec['requested_DOI_text_found']='10.4171/OWR/2022/17' in decoded
  if label in ['WZ','HLYTD']:rec['edition_limit']='Unversioned pinned author PDF; no publisher/VOR or current-HTTP-byte identity claim'
  rec['text_alphanumeric_characters']=sum(c.isalnum() for c in decoded)
  rec['complete']=rec['text_alphanumeric_characters']>100 and (rec.get('requested_version_stamp_found',True)) and rec.get('requested_DOI_text_found',True)
 records.append(rec)
after={n:census(p) for n,p in ROOTS.items()};save('GUARDS_AFTER.json',after);assert before==after
closing_ignore=raw(P/'.gitignore');assert boundary in closing_ignore.decode().splitlines()
private=census(PAYLOAD);complete=all(x['complete'] for x in records) and len(records)==7
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='COMPLETE_PINNED_PRIMARY_ACQUISITION' if complete else 'INCOMPLETE_PRIMARY_ACQUISITION',complete=complete,requested_primaries=7,authenticated_cache_copies=len(records),direct_curl_invocations=0,direct_payload_HTTP_body_downloads=0,browser_URL_verification_separate=True,whole_native_source196files21dirs_and_ROOTINITIAL18files1dir_unchanged=True,original_INITIAL_modes_and_seals_exact=True,private_payload=str(PAYLOAD),exact_actual_ignore_boundary=boundary,ignore_file_initial=dict(bytes=len(ignore),SHA256=sha(ignore)),ignore_file_closing=dict(bytes=len(closing_ignore),SHA256=sha(closing_ignore)),records=records,commands=commands,private_payload_whole_census=private,no_mathematical_verdict_or_current_peer_report_read=True,no_source_code_import_AST_compile_execution=True,no_Git_W_Sheet_global_mutation=True,completion_percent=100 if complete else round(100*sum(x['complete'] for x in records)/7,2),programme_goal_active_incomplete=True)
save('SOURCE_EDITION_MAP.json',result)
print(json.dumps(dict(status=result['status'],complete=complete,PDFs=len(records),PDFs_and_text_complete=sum(x['complete'] for x in records),Poppler_invocations=len(commands),Poppler_exits=[x['exit_code'] for x in commands],protected_whole_guards_equal=True,private_payload_files=len(private['files']),no_fresh_HTTP_download_claim=True,completion_percent=result['completion_percent'])))
