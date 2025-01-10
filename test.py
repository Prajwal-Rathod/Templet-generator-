from fpdf import FPDF
import datetime
import os

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

def get_user_input():
    """Get all required information from user"""
    print("\n=== Service Level Agreement Generator ===\n")
    
    # Client Information
    print("Client Information:")
    client_name = input("Enter Client Name: ")
    cr_number = input("Enter CR Number: ")
    attention = input("Enter Contact Person Name: ")
    email = input("Enter Email: ")
    
    # Service Details
    print("\nService Details:")
    vat_registration_fee = float(input("Enter VAT Registration Fee (BHD): "))
    consultancy_fee = float(input("Enter Consultancy Fee (BHD): "))
    
    # Reference Number Generation
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().strftime("%m")
    ref_sequence = input("Enter Reference Sequence Number (3 digits): ").zfill(3)
    ref_number = f"BKR/VAT/{current_year}/{current_month}/{ref_sequence}"
    
    # Additional Services (Optional)
    print("\nAdditional Services (Enter 'y' for Yes, 'n' for No):")
    additional_services = []
    if input("Include VAT Registration? (y/n): ").lower() == 'y':
        additional_services.append("VAT Registration with National Bureau of Revenue (NBR)")
    if input("Include VAT Compliance? (y/n): ").lower() == 'y':
        additional_services.append("VAT Compliance and Advisory Services")
    if input("Include Registration Support? (y/n): ").lower() == 'y':
        additional_services.append("Support during VAT Registration Process")
    if input("Include Documentation Support? (y/n): ").lower() == 'y':
        additional_services.append("Assistance with Documentation Requirements")
    if input("Include General Advisory? (y/n): ").lower() == 'y':
        additional_services.append("General VAT Advisory Services")
    
    # Custom Additional Services
    while input("\nAdd custom service? (y/n): ").lower() == 'y':
        service = input("Enter custom service description: ")
        additional_services.append(service)
    
    # Payment Terms
    print("\nPayment Terms:")
    advance_payment = input("Enter advance payment percentage (default 50): ") or "50"
    remaining_payment = input("Enter remaining payment percentage (default 50): ") or "50"
    
    return {
        "current_date": datetime.datetime.now().strftime("%d/%m/%Y"),
        "ref_number": ref_number,
        "client_name": client_name,
        "commercial_registration_number": cr_number,
        "attention": attention,
        "email": email,
        "vat_registration_fee": vat_registration_fee,
        "consultancy_fee": consultancy_fee,
        "authorized_person_name": attention,
        "additional_services": additional_services,
        "payment_terms": {
            "advance": advance_payment,
            "remaining": remaining_payment
        }
    }

def format_services_list(services):
    """Format the services list for PDF"""
    return "\n".join(f"- {service}" for service in services)

def format_payment_terms(terms):
    """Format payment terms for PDF"""
    return (
        f"- {terms['advance']}% advance payment upon signing this agreement\n"
        f"- Remaining {terms['remaining']}% upon completion of VAT registration\n"
        "- All payments are non-refundable"
    )

class DocumentGenerator:
    @staticmethod
    def create_pdf(data):
        try:
            pdf = SLATemplate()
            
            # Add Calibri fonts with error handling
            try:
                pdf.add_font('Calibri', '', 'calibri.ttf', uni=True)
                pdf.add_font('Calibri', 'B', 'calibrib.ttf', uni=True)
                pdf.add_font('Calibri', 'I', 'calibrii.ttf', uni=True)
            except Exception as e:
                print(f"Warning: Could not load Calibri fonts, falling back to Arial: {str(e)}")
                pdf.set_font('Arial', '', 10)
            
            pdf.add_page()
            
            # Reference Number and Date with increased spacing
            pdf.set_font('Calibri', 'B', 12)
            pdf.cell(0, 8, f"Ref: {data['ref_number']}", ln=True)
            pdf.cell(0, 8, f"Date: {data['current_date']}", ln=True)
            pdf.ln(5)
            
            # Client Details with adjusted spacing
            pdf.set_font('Calibri', 'B', 12)
            pdf.cell(0, 8, "TO:", ln=True)
            pdf.set_font('Calibri', '', 10)
            pdf.cell(0, 6, data['client_name'], ln=True)
            pdf.cell(0, 6, f"CR No: {data['commercial_registration_number']}", ln=True)
            pdf.cell(0, 6, f"Attn: {data['attention']}", ln=True)
            pdf.cell(0, 6, f"Email: {data['email']}", ln=True)
            pdf.ln(8)
            
            # Subject Line with proper spacing
            pdf.set_font('Calibri', 'B', 12)
            pdf.cell(0, 8, "Subject: Service Level Agreement for VAT Services", ln=True)
            pdf.ln(5)

            # Introduction with adjusted line height
            pdf.set_font('Calibri', '', 10)
            pdf.multi_cell(0, 6, 
                "Dear Sir/Madam,\n\n"
                "Thank you for choosing B.K.R Support Services W.L.L. We are pleased to present our "
                "Service Level Agreement (SLA) for VAT Services. This agreement outlines the terms and "
                "conditions under which we will provide our services."
            )
            pdf.ln(8)
            
            # Content Sections with dynamic data
            sections = [
                {
                    "title": "1. SCOPE OF SERVICES",
                    "content": (
                        "Our services include:\n" +
                        format_services_list(data['additional_services'])
                    )
                },
                {
                    "title": "2. SERVICE FEES",
                    "content": (
                        f"The fees for our services are as follows:\n\n"
                        f"VAT Registration Fee: BHD {data['vat_registration_fee']:.3f}\n"
                        f"Consultancy Fee: BHD {data['consultancy_fee']:.3f}\n"
                        f"Total Fee: BHD {(data['vat_registration_fee'] + data['consultancy_fee']):.3f}"
                    )
                },
                {
                    "title": "3. PAYMENT TERMS",
                    "content": format_payment_terms(data['payment_terms'])
                },
                {
                    "title": "4. DELIVERABLES",
                    "content": (
                        "- VAT Registration Certificate\n"
                        "- Support during the entire registration process\n"
                        "- Advisory services as outlined in the scope"
                    )
                },
                {
                    "title": "5. AGREEMENT ACCEPTANCE",
                    "content": (
                        "By signing below, both parties agree to the terms and conditions outlined in this "
                        "Service Level Agreement."
                    )
                }
            ]
            
            for section in sections:
                pdf.set_font('Calibri', 'B', 12)
                pdf.cell(0, 8, section["title"], ln=True)
                pdf.set_font('Calibri', '', 10)
                pdf.multi_cell(0, 6, section["content"])
                pdf.ln(8)
            
            # Signature Section with improved spacing
            pdf.ln(10)
            pdf.line(25, pdf.get_y(), 95, pdf.get_y())  # Client signature line
            pdf.line(120, pdf.get_y(), 185, pdf.get_y())  # Provider signature line
            
            pdf.set_y(pdf.get_y() + 5)
            pdf.set_font('Calibri', '', 10)
            pdf.cell(95, 5, "Client Signature & Stamp", 0, 0, 'L')
            pdf.cell(0, 5, "For B.K.R Support Services W.L.L", 0, 1, 'L')
            
            pdf.set_y(pdf.get_y() + 15)
            pdf.cell(95, 5, f"Name: {data['authorized_person_name']}", 0, 0, 'L')
            pdf.cell(0, 5, "Name: _______________________", 0, 1, 'L')
            
            pdf.set_y(pdf.get_y() + 15)
            pdf.cell(95, 5, "Date: _______________________", 0, 0, 'L')
            pdf.cell(0, 5, "Date: _______________________", 0, 1, 'L')
            
            return pdf
            
        except Exception as e:
            raise Exception(f"Error creating PDF: {str(e)}")

def main():
    try:
        # Get user input
        sla_data = get_user_input()
        
        # Generate and save PDF
        pdf = DocumentGenerator.create_pdf(sla_data)
        output_filename = f"SLA_{sla_data['client_name'].replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(output_filename, 'F')
        print(f"\nDocument generated successfully: {output_filename}")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
