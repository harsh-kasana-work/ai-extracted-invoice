import streamlit as st
from invoice_ocr import TesseractOCR, pdf_to_images
from ai_extractor import get_ai_structured_data
import json
from PIL import Image
import io

def main():
    st.set_page_config(page_title="Invoice OCR & Extraction")
    
    st.title("📄 Invoice OCR & Data Extraction")
    st.markdown("""
    Upload an invoice PDF or image to extract structured information.
    This app will:
    1. Process your document
    2. Use AI to structure the invoice data
    """)
    
    # Create tabs for the app - fixed naming to be clearer
    upload_tab, results_tab = st.tabs(["Upload & Process", "Structured Data"])
    
    # Sidebar options
    with st.sidebar:
        st.header("Processing Options")
        dpi = st.selectbox(
            "DPI (for PDFs)", 
            ["300", "600"],
            index=0
        )
        
        st.subheader("OCR Options")
        ocr_lang = "eng"
        psm_mode = st.selectbox(
            "Page Segmentation Mode", 
            [
                "0 - Orientation and script detection only",
                "1 - Automatic page segmentation with OSD",
                "3 - Fully automatic page segmentation, but no OSD (Default)",
                "4 - Assume a single column of text of variable sizes",
                "6 - Assume a single uniform block of text",
                "11 - Sparse text. Find as much text as possible in no particular order",
            ],
            index=5
        )
        psm = int(psm_mode.split(" - ")[0])
    
    # Initialize OCR engine
    ocr_engine = TesseractOCR(lang=ocr_lang, config=f'--psm {psm}')
    
    # Upload section (Tab 1)
    with upload_tab:
        col1, col2 = st.columns(2)

        with col1:
            uploaded_file = st.file_uploader("Upload Invoice PDF", type=["pdf"])
        
        with col2:
            uploaded_img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        
        # Process PDF if uploaded
        if uploaded_file is not None:
            try:
                with st.spinner("Processing PDF..."):
                    # Convert PDF to images
                    pil_images = pdf_to_images(uploaded_file, dpi=int(dpi))
                    
                    if not pil_images:
                        st.error("Could not extract any images from the PDF.")
                        return
                    
                    # Show original images
                    st.subheader("Document Pages")
                    for page_num, img in enumerate(pil_images, 1):
                        st.image(img, caption=f"Page {page_num}", use_container_width=True)
                    
                    # Store the processed images in session state for other tabs
                    st.session_state['original_images'] = pil_images
                    st.session_state['has_processed'] = True
                    
                    process_images(pil_images, ocr_engine)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                
        # Process Image if uploaded
        elif uploaded_img is not None:
            try:
                with st.spinner("Processing Image..."):
                    # Read the image file
                    img_bytes = uploaded_img.read()
                    
                    # Convert bytes to PIL Image
                    img = Image.open(io.BytesIO(img_bytes))
                    
                    # Show image
                    st.subheader("Document Image")
                    st.image(img, caption="Uploaded Image", use_container_width=True)
                    
                    # Store as a list with one image to reuse the same processing function
                    pil_images = [img]
                    st.session_state['original_images'] = pil_images
                    st.session_state['has_processed'] = True
                    
                    process_images(pil_images, ocr_engine)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Structured Data (Tab 2)
    with results_tab:
        if 'structured_data' in st.session_state:
            st.subheader("AI-Extracted Invoice Data")
            structured_data = st.session_state['structured_data']
            
            # Display in two columns
            if 'error' in structured_data:
                st.error("AI processing error")
                st.json(structured_data)
            else:
                # Show full JSON
                with st.expander("View Raw JSON Data"):
                    st.json(structured_data)
                
                # Download JSON
                st.download_button(
                    "Download Structured Data (JSON)",
                    json.dumps(structured_data, indent=2),
                    file_name="invoice_data.json",
                    mime="application/json"
                )
        else:
            st.info("Please upload and process a document in the 'Upload & Process' tab first.")


def process_images(images, ocr_engine):
    """Process a list of PIL images with OCR and AI extraction"""
    all_text = ""
    all_blocks = []
    
    # Process each image
    for page_num, img in enumerate(images, 1):
        # Extract text blocks with bounding boxes
        text_blocks = ocr_engine.extract_text(img)
        
        # Get full text
        page_text = ocr_engine.get_full_text(img)
        all_text += page_text + "\n\n"
        
        # Removed: Displaying extracted text
        # st.subheader(f"OCR Results - Page {page_num}")
        # st.text_area(f"Extracted Text", page_text, height=150)
        
        # Store all blocks
        all_blocks.extend(text_blocks)
    
    # Store the extracted text for the next tab
    st.session_state['extracted_text'] = all_text
    st.session_state['text_blocks'] = all_blocks
    
    # Process with AI right away
    with st.spinner("Processing with AI..."):
        structured_data = get_ai_structured_data(all_text)
        st.session_state['structured_data'] = structured_data
    
    st.toast("Document processed successfully! Check the 'Structured Data' tab for results.")


if __name__ == "__main__":
    main()