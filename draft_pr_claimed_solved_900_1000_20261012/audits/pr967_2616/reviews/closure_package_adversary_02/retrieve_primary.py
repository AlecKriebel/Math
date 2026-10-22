import pathlib,urllib.request,json,datetime,hashlib,base64,subprocess
R=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616/reviews/closure_package_adversary_02');D=R/'private/primary';D.mkdir(parents=True,exist_ok=True)
base='https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf';urls={'current':base,'archive':'https://web.archive.org/web/20261002014549id_/'+base};rows=[]
for label,url in urls.items():
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60)as response:b=response.read(2000000);hdr=dict(response.headers);status=response.status
 h=hashlib.sha256(b).hexdigest()
 if len(b)!=598093 or h!='eb095248a64ebe4a52ea2cd32b40012cefc03b18475c5432c58747febc4e5de7':raise RuntimeError('unexpected primary identity '+label)
 (D/(label+'.pdf')).write_bytes(b)
 if label=='archive' and hdr.get('Memento-Datetime',hdr.get('memento-datetime'))!='Fri, 02 Oct 2026 01:45:49 GMT':raise RuntimeError('memento mismatch')
 rows.append({'label':label,'url':url,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':status,'headers':hdr,'bytes':len(b),'sha256':h,'base32_sha1':base64.b32encode(hashlib.sha1(b).digest()).decode(),'bodies_private':True})
 subprocess.run(['pdftotext','-f','60','-l','60',str(D/(label+'.pdf')),str(D/(label+'_page60.txt'))],check=True)
 subprocess.run(['pdftoppm','-f','60','-singlefile','-scale-to','1800','-png',str(D/(label+'.pdf')),str(D/(label+'_page60'))],check=True,capture_output=True)
 text=(D/(label+'_page60.txt')).read_text();startindex=text.index('3.44.');endindex=text.index('3.45.')if '3.45.' in text else len(text);(D/(label+'_target.txt')).write_text(text[startindex:endindex])
subprocess.run(['pdfinfo','-isodates',str(D/'current.pdf')],stdout=(D/'pdfinfo.txt').open('w'),check=True)
(R/'PRIMARY_RETRIEVAL.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_only_section':'3.44, printed/PDF page60','current_archive_byte_identical':(D/'current.pdf').read_bytes()==(D/'archive.pdf').read_bytes(),'source_bodies_private':True,'retrievals':rows},indent=2)+'\n');print(json.dumps(rows,indent=2));print((D/'current_target.txt').read_text())
