"""Render one ignored source page and retain a hash receipt, never a source copy."""
import datetime,hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent
name,page=sys.argv[1],int(sys.argv[2])
pdf=R/'sources/raw'/f'{name}.pdf'
tmp=R/'private'; tmp.mkdir(exist_ok=True)
prefix=tmp/f'{name}_{page}'
subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','90','-png',str(pdf),str(prefix)],check=True,capture_output=True)
p=prefix.with_suffix('.png'); data=p.read_bytes()
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'id':name,'pdf_page':page,
         'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'png_bytes':len(data),
         'png_sha256':hashlib.sha256(data).hexdigest(),'image_path':str(p),'rendered':True,
         'actual_view_status':'PENDING_VIEW_TOOL'}
j=R/'SOURCE_VISUAL_RECEIPTS.json'; rows=json.loads(j.read_text()) if j.exists() else []
rows.append(receipt); j.write_text(json.dumps(rows,indent=2)+'\n')
print(p)
