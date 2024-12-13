from playsound import playsound
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from num2words import num2words
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from ConnectDatabase.connect_database import *
from Queries.quaries import *
import random

class MyPDF:
    
    def generate_pdf(self,username,uid,city, pincode, country, district, address,order_date,da=0):
        file_name = f"{username}_invoice.pdf"
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        elements = []
        foid=0
        qurey_runner(GET_ORDER_ID_BY_UID_QRY,(uid,))
        oid=cursor.fetchone()[0]
        qurey=f"""SELECT ROW_NUMBER() OVER (PARTITION BY oi.order_id ORDER BY oi.product_id) AS "Si.No", p.name as "product name", p.price AS "price per unit", oi.quantity || ' ' || oi.base_quantity AS quantity, (oi.price * oi.quantity) AS "net amount", o.tax_rate || '%' as "tax rate", o.tax_type, ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2) AS tax_amount, (oi.price * oi.quantity) + ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2) AS "total amount", SUM(ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2)) OVER (PARTITION BY oi.order_id) AS "total tax amount", SUM((oi.price * oi.quantity) + ROUND(((oi.price * oi.quantity) * o.tax_rate) / 100, 2)) OVER (PARTITION BY oi.order_id) AS "order total amount", o.total FROM  orderitems oi JOIN  products p ON oi.product_id = p.product_id  JOIN orders o ON oi.order_id = o.order_id WHERE  oi.order_id = {oid};"""
        cursor.execute(qurey)
        db_cnn.commit()
        result=cursor.fetchall()
        
        table_s = [
        ['Si.No', 'Description','Unit Price','Qty', 'Net Amount', 'Tax Rate', 'Tax Type', 'Tax Amount', 'Total Amount'],
        ]

        for i in range(0,len(result)):
            table_s.append([result[i][0],result[i][1],int(result[i][2]),result[i][3],int(result[i][4]),result[i][5],result[i][6],float(result[i][7]),float(result[i][8])])
      
        amount = result[0][11]+300    
        amount_in_words = num2words(int(amount), lang='en') + ' only'
    
        lr=len(result)
        if da>0:
            table_e=[ 
            [f'{len(result)+1}','Shipping charges','-','-','-','-','-','-','300'],
            [f'{len(result)+2}','Discount','-','-','-','-','-','-',f'-{da}'],
            ['TOTAL:', '', '', '', '','', '', f"{float(result[0][9])}",f"{amount}"],    
            [f'Amount in Words:\n{amount_in_words}'],
            ['for saller name:\n\n\n\nAuthorized Signatory']]
        else:
            lr-=1
            table_e=[ 
            [f'{len(result)+1}','Shipping charges','-','-','-','-','-','-','300'],
            ['TOTAL:', '', '', '', '','', '', f"{float(result[0][9])}",f"{amount}"],    
            [f'Amount in Words:\n{amount_in_words}'],
            ['for saller name:\n\n\n\nAuthorized Signatory']]

        table_s.extend(table_e)

        col_widths1 = [0.5*inch,2.0*inch, 0.7*inch, 0.7*inch, 0.9*inch,0.7*inch, 0.7*inch, 0.9*inch,1.0*inch]

        # Create the table with specified column widths
        table1 = Table(table_s, colWidths=col_widths1)
        # Add style to the table
        def table_data(length):
            for i in range(0,length):
                return ('TEXTCOLOR',(i,i+1),(),colors.black)
        style1 = TableStyle([
            
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            #main data creation
            ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
            ('TEXTCOLOR',(0,1),(-1,-1),colors.black),
            ('ALIGN',(0,1),(-1,-1),'CENTER'),
            ('VALIGN',(0,1),(-1,-1),'MIDDLE'),

            #spanning for the total (LEFT PART) 
            ('SPAN', (0, lr+3), (6, lr+3)),
            ('FONTNAME', (0, lr+3), (6, lr+3),'Helvetica-Bold'),
            ('ALIGN', (0, lr+3), (6, lr+3),'LEFT'),
            ('TOPPADDING', (0, lr+3), (6, lr+3),5),
            ('BOTTOMPADDING', (0, lr+3), (6, lr+3),5),

            #spanning for the total (rightpart)
            ('FONTNAME', (7, lr+3), (8, lr+3),'Helvetica-Bold'),
            ('BACKGROUND', (7, lr+3), (8, lr+3),colors.lightgrey),
            
            #amouont in words
            ('FONTNAME', (0, lr+4), (-1, lr+4),'Helvetica-Bold'),
            ('FONTSIZE', (0, lr+4), (-1, lr+4),12),
            ('ALIGN', (0, lr+4), (-1, lr+4),'LEFT'),
            ('SPAN', (0, lr+4), (-1, lr+4)),

            #for siganture and seller
            ('FONTNAME', (0, lr+5), (-1, lr+5),'Helvetica-Bold'),
            ('SPAN', (0, lr+5), (-1, lr+5)),
            ('TOPPADDING', (0, lr+5), (-1, lr+5),5),
            ('BOTTOMPADDING', (0, lr+5), (-1, lr+5),5),
            ('ALIGN', (0, lr+5), (-1, lr+5),'RIGHT')

            ])
        table1.setStyle(style1)
        # Adding the table to elements
        elements.append(Spacer(1, 4.5*inch))
        elements.append(table1)

        #table 2
        def add_header(canvas, doc):
            width, height = letter

            # Insert an image
            image_path = "Grocery Store Scaled\BillGeneration\Screenshot 2024-11-04 123236.png"  # Replace with your image path
            image_x = 5  # X position
            image_y = height - 55  # Y position
            image_width = 190  # Width of the image
            image_height = 50  # Height of the image

            # Draw the image
            canvas.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)

            # Right side text
            canvas.setFont("Helvetica-Bold", 15)
            canvas.drawString(330, height - 27, "Tax Invoice/Bill of Supply/Cash Memo")
            canvas.setFont("Helvetica", 13)
            canvas.drawString(470, height - 42, "(Original for Recipient)")

            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(15, height - 100, "Sold By:")

            canvas.setFont("Helvetica", 11)
            canvas.drawString(15, height - 115, "Amazon fresh store")
            canvas.drawString(15, height - 130, "152-157, Sankalp Iconic Tower")
            canvas.drawString(15, height - 145, "Ahmedabad, 380001")
            canvas.drawString(15, height - 160, "India")

            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(15, height - 210, "PAN No:")
            canvas.setFont("Helvetica", 11)
            canvas.drawString(60, height - 210, " 1238934923")
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(15, height - 225, "GST Registration No:")
            canvas.setFont("Helvetica", 11)
            canvas.drawString(125, height - 225, " GSTIN3845937397")

            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(515, height - 100, "Billing Address:")

            text_width = pdfmetrics.stringWidth(username, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.setFont("Helvetica", 11)
            canvas.drawString(x_position, height - 115, username)#115

            x_position = 0
            text_width = pdfmetrics.stringWidth(address, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 130, address)

            x_position = 0
            text_width = pdfmetrics.stringWidth(city + ", " + district + ", " + pincode, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 145, city + ", " + district + ", " + pincode)

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 160, country)

            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(502, height - 250, "Shipping Address:")

            text_width = pdfmetrics.stringWidth(username, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.setFont("Helvetica", 11)
            canvas.drawString(x_position, height - 265, username)

            x_position = 0
            text_width = pdfmetrics.stringWidth(address, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 280, address)

            x_position = 0
            text_width = pdfmetrics.stringWidth(city + ", " + district + ", " + pincode, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 295, city + ", " + district + ", " + pincode)

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 13
            canvas.drawString(x_position, height - 310, country)

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 115
            canvas.drawString(x_position, height - 330, f"Place of Supply : {district}")

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 115
            canvas.drawString(x_position, height - 345, f"Place of Delivery : {district}")

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 115
            canvas.drawString(x_position, height - 360, f"Invoice number : {random.randint(10,10000)}")

            x_position = 0
            text_width = pdfmetrics.stringWidth(country, 'Helvetica', 11)
            x_position = width - text_width - 115
            canvas.drawString(x_position, height - 375, f"Invoice date : {order_date}")


            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(15, height - 360, "Order No:")
            canvas.setFont("Helvetica", 11)
            canvas.drawString(65, height - 360, f" {random.randint(10,10000)}")

            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(15, height - 375, "Order Date:")
            canvas.setFont("Helvetica", 11)
            canvas.drawString(75, height - 375, f" {order_date}")

            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(310, height - 730,
                                     "*ASSPL-Amazon Seller Services Pvt. Ltd., ARIPL-Amazon Retail India Pvt. Ltd. (only where Amazon Retail India Pvt. Ltd. fulfillment center is co-located)")
            canvas.drawCentredString(310, height - 745,
                                     "Customers desirous of availing input GST credit are requested to create a Business account and purchase on Amazon.in/business from Business eligible offers")
            canvas.drawCentredString(310, height - 760,
                                     "Please note that this invoice is not a demand for payment")

        # Build the PDF
        doc.build(elements, onFirstPage=add_header)