from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
import numpy as np
import fitz
from PIL import Image
from scipy import signal
import matplotlib.pyplot as plt
import gtp_summary as gtp
from generate_rectangle import find_object, generate_mask, parse_layout, find_largest_square_helper, generate_rectangle_res, extract_many_rectangle, choose_rect, add_all_notes_slides, write_slides

if __name__ == "__main__":


    full_obj = find_object("../slides_AXA_cropped.pdf")

    mask_dict = generate_mask("../slides_AXA_cropped.pdf", full_obj)
    
    key_openai = "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"

    prompt = gtp.generate_prompt('../transcript_audio.txt','../transcript_slides.txt', False)
    blank_space_dict = {}
    
    filename = '../slides_AXA_cropped.pdf'
    doc = fitz.open(filename) 
    for key, mask in mask_dict.items():
        res = extract_many_rectangle(mask, 3)
        blank_space_dict[key] = res
        text = gtp.generate_response(prompt[key], key_openai) 
        
        txt, rect = choose_rect(res, text, "helv", 10)

        page = doc[key] 

        add_all_notes_slides(page, txt, rect, "Helv", color = 0)
    doc.save("output21.pdf")  # save to new file