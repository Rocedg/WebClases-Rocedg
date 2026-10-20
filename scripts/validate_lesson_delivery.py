import sys
from pathlib import Path
import json
import os
import tempfile
import re

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
sys.path.insert(0,str(Path('tmp/lesson-review-tools').resolve()))
import pymupdf as fitz

lessons=json.loads(Path('content/lessons/lessons.json').read_text(encoding='utf8'))['lessons']
summary=[]
for lesson in lessons:
    pdf=Path(lesson['url'])
    doc=fitz.open(pdf)
    assert len(doc)==lesson['pages'] and len(doc)<=12
    log=Path('tmp/lesson-review',pdf.stem+'.log').read_text(encoding='utf8',errors='replace')
    assert not re.search(r'Overfull|undefined|LaTeX Error|Fatal error|Rerun to get',log),pdf.name
    text='\n'.join(p.get_text() for p in doc)
    assert '??' not in text
    for i,page in enumerate(doc,1):
        assert f'gina {i} de {len(doc)}' in page.get_text(),(pdf.name,i,'footer')
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    assert x0>=25 and x1<=doc[0].rect.width-25,(pdf.name,i,span['text'])
    links=[l for p in doc for l in p.get_links()]
    # PyMuPDF may expose resolved LaTeX destinations as named links.
    internal=[l for l in doc[0].get_links()
              if l['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED) and l.get('page', -1) >= 0]
    assert len(internal) in (3,4,5,6),(pdf.name,internal)
    source=Path('content/lessons/latex',pdf.stem+'.tex').read_text(encoding='utf8')
    titles=re.findall(r'\\block\{(\d)\}\{([^}]*)\}\{([^}]*)\}',source)
    aux=Path('tmp/lesson-review',pdf.stem+'.aux').read_text(encoding='utf8')
    destinations=[]
    for link,(_,title,label) in zip(internal,titles):
        match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
        assert match and link['page']+1==int(match[1])
        destinations.append(link['page']+1)
    assert any(l.get('uri','').startswith('https://openstax.org/') for l in links)
    fonts={round(s['size'],2) for p in doc for b in p.get_text('dict')['blocks']
           for line in b.get('lines',[]) for s in line['spans']}
    summary.append(dict(file=pdf.name,pages=len(doc),index_pages=destinations,font_sizes=sorted(fonts)))

with tempfile.TemporaryDirectory(prefix='rocedg-lesson-smoke-') as folder:
    os.environ['DATABASE_URL']='sqlite:///'+(Path(folder)/'test.sqlite').as_posix()
    from app import app
    from database import db
    app.config.update(TESTING=True)
    with app.app_context(): db.create_all()
    client=app.test_client()
    assert client.get('/').status_code==200
    assert client.get('/lesson/'+lessons[0]['id']).status_code==302
    response=client.post('/login',data={'username':'Guest','password':'studentpass'})
    assert response.status_code==302
    assert client.get('/topics').status_code==200
    for lesson in lessons:
        response=client.get('/lesson/'+lesson['id'])
        assert response.status_code==200
        assert b"data-pdf-viewer" in response.data
        assert ("/lesson/" + lesson["id"] + "/pdf-source").encode() in response.data
        for action,disposition in [('open','inline'),('download','attachment')]:
            response=client.get('/resource/lesson_pdf/'+lesson['id']+'/'+action)
            assert response.status_code==200 and response.mimetype=='application/pdf'
            assert disposition in response.headers['Content-Disposition']
            assert response.data==Path(lesson['url']).read_bytes()
            response.close()
        response=client.get('/'+lesson['url'])
        assert response.status_code==200 and response.data==Path(lesson['url']).read_bytes()
        response.close()
    with app.app_context():
        db.session.remove()
        db.engine.dispose()
Path('tmp/lesson-review/delivery-checks.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
print('PASS: page counts, footers, index destinations, source links, text margins; all seven viewers, inline/download and static PDF routes.')
