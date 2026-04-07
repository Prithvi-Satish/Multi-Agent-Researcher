import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_docx(docx_path):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    try:
        with zipfile.ZipFile(docx_path) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        texts = []
        for elem in tree.iter():
            if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                texts.append('\n')
            elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t' and elem.text:
                texts.append(elem.text)
            elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br':
                texts.append('\n')
        
        # clean up multiple newlines
        content = ''.join(texts)
        import re
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()
    except Exception as e:
        return str(e)

with open('multiagent_pro.txt', 'w', encoding='utf-8') as f:
    f.write(extract_text_from_docx('multiagent pro.docx'))
