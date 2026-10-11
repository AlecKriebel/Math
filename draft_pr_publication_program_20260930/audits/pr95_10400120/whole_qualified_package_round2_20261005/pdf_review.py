from review_tools import *
pdf=Q/'publicfiles/pr95_note.pdf'
folder=A/'pdf85';folder.mkdir()
for label,argv in [('pdfinfo',['/opt/homebrew/bin/pdfinfo',pdf]),('pdftext',['/opt/homebrew/bin/pdftotext','-layout',pdf,folder/'manuscript.txt']),('pdfrender',['/opt/homebrew/bin/pdftoppm','-r','85','-png',pdf,folder/'page'])]:
    if run(label,argv,A,[pdf])['exit_code']:raise RuntimeError('PDF read failed')
dump(A/'PDF_FILES.json',{'source_sha256':sha(pdf),'dpi':85,'page_renders':[{'file':str(p.relative_to(A)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(folder.glob('page-*.png'))]})
