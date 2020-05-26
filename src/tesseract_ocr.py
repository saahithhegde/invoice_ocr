import cv2
from src.preprocessdata import preprocess
import pytesseract
from pytesseract import Output
from fpdf import FPDF


class ocr:

    def readimage(self,filepath):
        image=cv2.imread(filepath)
        return image

    def enhance_image(self,image):
        mypreprocess = preprocess()
        gray_image = mypreprocess.get_grayscale(image)
        thresh_image = mypreprocess.thresholding(gray_image)

        #refer preprocessdata for more functionality:
        enhanced_image=thresh_image
        return enhanced_image


    #get dictionary of pytesseract data
    def image_ocr(self,image):
        d = pytesseract.image_to_data(image, output_type=Output.DICT)
        return d

    def generate_html(self,image,filename):
        content = pytesseract.image_to_pdf_or_hocr(image, lang='eng', nice=0, extension='hocr')
        # Write content to a new file, owerwrite w or append a (b=binary)
        f = open("processeddata"+filename+".html", 'w+b')
        f.write(bytearray(content))
        f.close()
        return

    def get_pdf_with_ocr(self,image,filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('arial', '', 9.0)
        image=self.enhance_image(image)
        d=self.image_ocr(image)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            # check for confidence level > 50 and ignore empty texts
            if int(d['conf'][i]) > 50 and d["text"] != '' and d["text"] != ' ':
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                pdf.set_xy(x/4,y/4)
                pdf.cell(ln=2, h=h / 3.5, align='C', w=w / 3.5, txt=(d["text"][i]), border=0)
        pdf.output("processeddata/"+filename+".pdf", 'F')
        return filename+".pdf"

    def generate_simple_pdf(self,image,filename):
        PDF=pytesseract.image_to_pdf_or_hocr(image,lang='eng',config='',nice=0,extension='pdf')
        f = open("processeddata"+filename+"_simple.pdf", "w+b")
        f.write(bytearray(PDF))
        f.close()
        return





