import streamlit as st
import datetime
import os
from fpdf import FPDF
from io import BytesIO

class SLATemplate(FPDF):
    def __init__(self):
        super().__init__()
        # Further increase margins to prevent overlapping
        self.set_margins(left=25, top=55, right=25)  # Increased top margin
        # Increase bottom margin significantly
        self.set_auto_page_break(auto=True, margin=40)  # Increased bottom margin
        # Set default line height
        self.set_line_height(6.5)

    def set_line_height(self, height):
        self.cell_height = height

    def header(self):
        # Add background template if exists
        if os.path.exists('background_template.jpg'):
            self.image('background_template.jpg', x=0, y=0, w=210, h=297)  # A4 size
        elif os.path.exists('background_template.png'):
            self.image('background_template.png', x=0, y=0, w=210, h=297)  # A4 size
        
        # Move header up - start at y=10
        self.set_y(10)
        
        # Logo placeholder (left side) with adjusted position
        if os.path.exists('logo.png'):
            self.image('logo.png', x=25, y=10, w=30)
        
        # Title (center) with increased spacing
        self.set_font('Calibri', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, 'SERVICE LEVEL AGREEMENT', 0, 1, 'C')
        
        # Reset text color for content
        self.set_text_color(0, 0, 0)
        
        # Reset to content start position - moved up
        self.set_y(40)  # Start content higher

    def footer(self):
        # Move footer text to the very bottom of the page
        self.set_y(-15)  # -15 is the absolute bottom position
        self.set_font('Calibri', 'I', 8)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'B.K.R Support Services W.L.L', 0, 0, 'C')
        self.set_text_color(0, 0, 0)

def format_services_list(services):
    """Format the services list for PDF"""
    return "\n".join(f"- {service.strip()}" for service in services if service.strip())

def format_payment_terms(advance, remaining):
    """Format payment terms for PDF"""
    return (
        f"- {advance}% advance payment upon signing this agreement\n"
        f"- Remaining {remaining}% upon completion of VAT registration\n"
        "- All payments are non-refundable"
    )

class DocumentGenerator:
    @staticmethod
    def create_pdf(data):
        try:
            pdf = SLATemplate()
            
            try:
                pdf.add_font('Calibri', '', 'calibri.ttf', uni=True)
                pdf.add_font('Calibri', 'B', 'calibrib.ttf', uni=True)
                pdf.add_font('Calibri', 'I', 'calibrii.ttf', uni=True)
            except Exception as e:
                print(f"Warning: Could not load Calibri fonts, falling back to Arial: {str(e)}")
                pdf.set_font('Arial', '', 10)
            
            pdf.add_page()

            # Header Information
            pdf.set_font('Calibri', 'B', 12)
            pdf.cell(0, 8, f"Ref: {data['ref_number']}", ln=True)
            pdf.cell(0, 8, f"Date: {data['current_date']}", ln=True)
            pdf.ln(5)

            # Client Details
            pdf.cell(0, 8, "TO:", ln=True)
            pdf.set_font('Calibri', '', 10)
            pdf.cell(0, 6, data['client_name'], ln=True)
            pdf.cell(0, 6, f"CR No: {data['commercial_registration_number']}", ln=True)
            pdf.cell(0, 6, f"Attn: {data['attention']}", ln=True)
            pdf.cell(0, 6, f"Email: {data['email']}", ln=True)
            pdf.ln(8)

            # Template text with placeholders
            template_text = f"""
This Service Level Agreement (hereinafter referred to as "Agreement") is made and entered into on {data['agreement_date']} by and between:

B.K.R Support Services W.L.L, a company incorporated under the laws of the Kingdom of Bahrain (hereinafter referred to as "Service Provider")

AND

{data['client_name']}, with Commercial Registration No. {data['commercial_registration_number']}, having its registered office in the Kingdom of Bahrain (hereinafter referred to as "Client").

OWNERSHIP STRUCTURE
The Client's ownership structure is as follows:
• Bahraini Ownership: {data['bahraini_ownership']}%
• GCC Nationals: {data['gcc_ownership']}%
• American Nationals: {data['american_ownership']}%
• Foreign Ownership: {data['foreign_ownership']}%

BUSINESS ACTIVITIES
The Client is engaged in the following business activities:
1. Primary Activity:
   ISIC4 Code: {data['isic_code_1']}
   Activity Name: {data['activity_name_1']}
   Description: {data['activity_desc_1']}

2. Secondary Activity:
   ISIC4 Code: {data['isic_code_2']}
   Activity Name: {data['activity_name_2']}
   Description: {data['activity_desc_2']}

SCOPE OF SERVICES
The Service Provider agrees to provide the following services to the Client:
{format_services_list(data['services'])}

FEES AND PAYMENT STRUCTURE
1. Registration and Setup Costs:
   • Company Formation: BHD {data['company_formation_cost']:.3f}
   • Desk-Space Office Rental: BHD {data['desk_space_cost']:.3f}
   • Businessman Visa: BHD {data['businessman_visa_cost']:.3f}
   • Power of Attorney: BHD {data['poa_cost']:.3f}

2. Administrative Costs:
   • Labour Authority Registration: BHD {data['labor_auth_cost']:.3f}
   • Social Insurance Registration: BHD {data['social_insurance_cost']:.3f}
   • Miscellaneous/Admin Charges: BHD {data['misc_charges']:.3f}
   • Estimation Charges (Per Head): BHD {data['estimation_charges']:.3f}
   • Free Advice/Guidance: BHD {data['free_advice_cost']:.3f}

3. VAT Services:
   • VAT Registration Fee: BHD {data['vat_registration_fee']:.3f}
   • Consultancy Fee: BHD {data['consultancy_fee']:.3f}
   Total VAT Services Fee: BHD {(data['vat_registration_fee'] + data['consultancy_fee']):.3f}

PAYMENT TERMS
{format_payment_terms(data['advance_payment'], data['remaining_payment'])}

DELIVERABLES
The Service Provider shall deliver:
1. Complete company registration documentation
2. VAT Registration Certificate
3. Ongoing support during the registration process
4. Advisory services as specified in the scope of services

TERM AND TERMINATION
This Agreement shall commence on {data['agreement_date']} and shall continue until the completion of the services outlined herein.
"""

            # Add the template text to PDF
            pdf.set_font('Calibri', '', 10)
            pdf.multi_cell(0, 6, template_text)
            
            # Signature Section
            pdf.ln(10)
            pdf.line(25, pdf.get_y(), 95, pdf.get_y())
            pdf.line(120, pdf.get_y(), 185, pdf.get_y())
            
            pdf.set_y(pdf.get_y() + 5)
            pdf.cell(95, 5, "Client Signature & Stamp", 0, 0, 'L')
            pdf.cell(0, 5, "For B.K.R Support Services W.L.L", 0, 1, 'L')
            
            pdf.set_y(pdf.get_y() + 15)
            pdf.cell(95, 5, f"Name: {data['signatory_name']}", 0, 0, 'L')
            pdf.cell(0, 5, "Name: _______________________", 0, 1, 'L')
            
            pdf.set_y(pdf.get_y() + 15)
            pdf.cell(95, 5, f"Passport Number: {data['passport_number']}", 0, 0, 'L')
            pdf.cell(0, 5, "Date: _______________________", 0, 1, 'L')
            
            return pdf
            
        except Exception as e:
            raise Exception(f"Error creating PDF: {str(e)}")

def main():
    st.set_page_config(page_title="SLA Generator", layout="wide")
    st.title("Service Level Agreement Generator")

    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None

    with st.form("sla_form"):
        st.subheader("Basic Information")
        client_name = st.text_input("Client Name")
        cr_number = st.text_input("CR Number")
        attention = st.text_input("Contact Person Name")
        email = st.text_input("Email")
        agreement_date = st.date_input("Date of Agreement")

        st.subheader("Ownership Details")
        bahraini_ownership = st.number_input("Bahraini Ownership (%)", min_value=0, max_value=100)
        gcc_ownership = st.number_input("GCC Nationals Ownership (%)", min_value=0, max_value=100)
        american_ownership = st.number_input("American Nationals Ownership (%)", min_value=0, max_value=100)
        foreign_ownership = st.number_input("Foreign Ownership (%)", min_value=0, max_value=100)

        st.subheader("Business Activities")
        col1, col2 = st.columns(2)
        with col1:
            isic_code_1 = st.text_input("Business Activity ISIC4 Code (1st)")
            activity_name_1 = st.text_input("Business Activity Name (1st)")
            activity_desc_1 = st.text_area("Business Activity Description (1st)")
        
        with col2:
            isic_code_2 = st.text_input("Business Activity ISIC4 Code (2nd)")
            activity_name_2 = st.text_input("Business Activity Name (2nd)")
            activity_desc_2 = st.text_area("Business Activity Description (2nd)")

        st.subheader("Costs")
        col1, col2 = st.columns(2)
        with col1:
            company_formation_cost = st.number_input("Company Formation Cost", min_value=0.0)
            desk_space_cost = st.number_input("Desk-Space Office Rental Cost", min_value=0.0)
            businessman_visa_cost = st.number_input("Businessman Visa Cost", min_value=0.0)
            misc_charges = st.number_input("Miscellaneous/Admin Charges", min_value=0.0)
            poa_cost = st.number_input("Power of Attorney Cost", min_value=0.0)

        with col2:
            estimation_charges = st.number_input("Estimation Charges (Per Head)", min_value=0.0)
            labor_auth_cost = st.number_input("Labour Authority Registration Cost", min_value=0.0)
            social_insurance_cost = st.number_input("Social Insurance Registration Cost", min_value=0.0)
            free_advice_cost = st.number_input("Free Advice/Guidance Cost", min_value=0.0)

        st.subheader("Signatory Information")
        signatory_name = st.text_input("Signatory Name")
        passport_number = st.text_input("Passport Number")

        st.subheader("Service Details")
        vat_registration_fee = st.number_input("VAT Registration Fee (BHD)", min_value=0.0)
        consultancy_fee = st.number_input("Consultancy Fee (BHD)", min_value=0.0)
        ref_sequence = st.text_input("Reference Sequence Number", max_chars=3)
        services = st.text_area("Services (Comma-separated)").split(",")
        
        advance_payment = st.slider("Advance Payment (%)", 0, 100, 50)
        remaining_payment = st.slider("Remaining Payment (%)", 0, 100, 50)

        submitted = st.form_submit_button("Generate SLA")

        if submitted:
            data = {
                "current_date": datetime.datetime.now().strftime("%d/%m/%Y"),
                "agreement_date": agreement_date.strftime("%d/%m/%Y"),
                "ref_number": f"BKR/VAT/{datetime.datetime.now().year}/{datetime.datetime.now().strftime('%m')}/{ref_sequence.zfill(3)}",
                "client_name": client_name,
                "commercial_registration_number": cr_number,
                "attention": attention,
                "email": email,
                "bahraini_ownership": bahraini_ownership,
                "gcc_ownership": gcc_ownership,
                "american_ownership": american_ownership,
                "foreign_ownership": foreign_ownership,
                "isic_code_1": isic_code_1,
                "activity_name_1": activity_name_1,
                "activity_desc_1": activity_desc_1,
                "isic_code_2": isic_code_2,
                "activity_name_2": activity_name_2,
                "activity_desc_2": activity_desc_2,
                "company_formation_cost": company_formation_cost,
                "desk_space_cost": desk_space_cost,
                "businessman_visa_cost": businessman_visa_cost,
                "misc_charges": misc_charges,
                "poa_cost": poa_cost,
                "estimation_charges": estimation_charges,
                "labor_auth_cost": labor_auth_cost,
                "social_insurance_cost": social_insurance_cost,
                "free_advice_cost": free_advice_cost,
                "signatory_name": signatory_name,
                "passport_number": passport_number,
                "vat_registration_fee": vat_registration_fee,
                "consultancy_fee": consultancy_fee,
                "services": services,
                "advance_payment": advance_payment,
                "remaining_payment": remaining_payment,
            }

            pdf = DocumentGenerator.create_pdf(data)
            st.session_state.pdf_data = pdf.output(dest='S').encode('latin1')

    # Download button outside the form
    if st.session_state.pdf_data is not None:
        st.download_button(
            "Download SLA PDF",
            data=st.session_state.pdf_data,
            file_name="SLA.pdf",
            mime="application/pdf"
        )


if __name__ == "__main__":
    main()
