import urllib.request

def test_compile():
    with open('Resume.tex', 'r', encoding='utf-8') as f:
        tex = f.read()

    # Fix the typo
    tex_fixed = tex.replace(r'd\input{Resume_Updated}ata', 'data')

    # Create multipart/form-data payload
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = []
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(b'Content-Disposition: form-data; name="file"; filename="resume.tex"')
    body.append(b'Content-Type: application/x-tex')
    body.append(b'')
    body.append(tex_fixed.encode('utf-8'))
    body.append(f'--{boundary}--'.encode('utf-8'))
    body.append(b'')

    payload = b'\r\n'.join(body)

    url = 'https://latexonline.cc/compile'
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        print("Sending request to LaTeXOnline...")
        with urllib.request.urlopen(req) as response:
            pdf_content = response.read()
            with open('Resume.pdf', 'wb') as out:
                out.write(pdf_content)
        print('Compilation successful! Resume.pdf created.')
    except Exception as e:
        print('Error during compilation:', e)
        if hasattr(e, 'read'):
            print('Server response (first 500 chars):', e.read()[:500].decode('utf-8', errors='ignore'))

if __name__ == "__main__":
    test_compile()
