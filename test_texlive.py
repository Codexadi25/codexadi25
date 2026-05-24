import urllib.request
import urllib.parse

def test_texlive():
    with open('Resume.tex', 'r', encoding='utf-8') as f:
        tex = f.read()

    # Fix the typo
    tex_fixed = tex.replace(r'd\input{Resume_Updated}ata', 'data')

    # Prepare POST payload for texlive.net
    # Endpoint: https://texlive.net/cgi-bin/latexcgi
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = []
    
    # filecontents[]
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(b'Content-Disposition: form-data; name="filecontents[]"; filename="document.tex"')
    body.append(b'Content-Type: application/x-tex')
    body.append(b'')
    body.append(tex_fixed.encode('utf-8'))
    
    # filename[]
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(b'Content-Disposition: form-data; name="filename[]"')
    body.append(b'')
    body.append(b'document.tex')
    
    # engine
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(b'Content-Disposition: form-data; name="engine"')
    body.append(b'')
    body.append(b'pdflatex')
    
    # return
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(b'Content-Disposition: form-data; name="return"')
    body.append(b'')
    body.append(b'pdf')
    
    body.append(f'--{boundary}--'.encode('utf-8'))
    body.append(b'')

    payload = b'\r\n'.join(body)

    url = 'https://texlive.net/cgi-bin/latexcgi'
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        print("Sending request to texlive.net...")
        with urllib.request.urlopen(req) as response:
            pdf_content = response.read()
            # If the response is HTML/text, it might be an error page instead of PDF
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' in content_type.lower():
                with open('Resume_TeXLive.pdf', 'wb') as out:
                    out.write(pdf_content)
                print('Compilation successful! Resume_TeXLive.pdf created.')
            else:
                print('Compilation failed. Response Content-Type:', content_type)
                print('Server response (first 1000 chars):')
                print(pdf_content[:1000].decode('utf-8', errors='ignore'))
    except Exception as e:
        print('Error during compilation:', e)
        if hasattr(e, 'read'):
            print('Server response:', e.read().decode('utf-8', errors='ignore')[:1000])

if __name__ == "__main__":
    test_texlive()
