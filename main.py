import pdfrw
import sys
import subprocess
from pathlib import Path
import requests
mode = 0o777


def download_file(file_url, folder_path):
    filename = Path(folder_path + '/' + 'document.pdf')
    response = requests.get(file_url)
    filename.write_bytes(response.content)


def remove_links(new_path):
    pdf = pdfrw.PdfReader(new_path + "/document.pdf")
    new_pdf = pdfrw.PdfWriter()  # Create an empty pdf
    for page in pdf.pages:
        for annot in page.Annots or []:
            new_url = pdfrw.objects.pdfstring.PdfString("")
            annot.A.URI = new_url
        new_pdf.addpage(page)

    new_pdf.write(new_path + "/document.pdf")


def decompress_pdf(old_path, new_path):
    bash_command = 'qpdf --qdf --object-streams=disable ' + old_path + '/document.pdf ' + new_path + '/document.pdf'
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    process.communicate()


if __name__ == "__main__":
    # Script Params
    url = sys.argv[1]
    original_folder_path = sys.argv[2]
    new_folder_path = sys.argv[3]

    download_file(url, original_folder_path)

    decompress_pdf(original_folder_path, new_folder_path)

    remove_links(new_folder_path)


