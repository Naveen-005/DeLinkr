import PyPDF2
import re
import argparse
import os

def remove_links_from_pdf(input_pdf, output_pdf):

        if not os.path.exists(input_pdf):
            print(f"Error: Input file {input_pdf} does not exist.")
            return False
        
        with open(input_pdf, 'rb') as file:

            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            for page_num in range(len(reader.pages)):

                page = reader.pages[page_num]
                page.annots = []

                if '/Annots' in page:
                    del page['/Annots']

                if page.extract_text():

                    cleaned_text = re.sub(r'https?://\S+', '', page.extract_text())
                    cleaned_text = re.sub(r'www\.\S+', '', cleaned_text)
                    
                writer.add_page(page)
            
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"PDF links removed. Saved to {output_pdf}")
            return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():

    parser = argparse.ArgumentParser(description='Remove links from a PDF file.')
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('output', help='Path to save the PDF without links')
    
    args = parser.parse_args()
    
    remove_links_from_pdf(args.input, args.output)

if __name__ == '__main__':
    main()
