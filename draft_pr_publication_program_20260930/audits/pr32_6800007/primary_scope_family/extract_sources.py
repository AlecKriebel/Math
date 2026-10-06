from pathlib import Path
import subprocess,json,datetime
ROOT=Path(__file__).resolve().parent
if __name__=="__main__":
 for n in ["falbel_veloso_v1","koshkin2009","koshkin_arxiv_current","borrelli2002"]:
  subprocess.run(["pdftotext","-layout",str(ROOT/"sources"/(n+".pdf")),str(ROOT/"sources"/(n+".txt"))],check=True)
 dest=ROOT/"tmp/forstneric_ocr";dest.mkdir(exist_ok=True)
 subprocess.run(["pdftoppm","-scale-to","2500","-png",str(ROOT/"sources/forstneric1986.pdf"),str(dest/"page")],check=True)
 texts=[]
 for page in sorted(dest.glob("page-*.png")):
  proc=subprocess.run(["tesseract",str(page),"stdout"],capture_output=True,text=True,check=True)
  texts.append(proc.stdout)
 (ROOT/"sources/forstneric1986_ocr.txt").write_text("\n\f\n".join(texts))
 (ROOT/"OCR_RECEIPT.json").write_text(json.dumps({"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pages":len(texts),"source_pdf":"forstneric1986.pdf","method":"Poppler 2500-pixel page rendering then Tesseract OCR. Relevant theorem pages visually inspected; OCR alone is not layout/mathematical verification."},indent=2)+"\n")
 print("OCR completed",len(texts),"pages")
