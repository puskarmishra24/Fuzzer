from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from datetime import datetime
from termcolor import colored
from textwrap import wrap

def create_wrapped_cell(text, width=60):
    """Helper function to wrap text in table cells"""
    if not isinstance(text, str):
        text = str(text)
    wrapped_text = "\n".join(wrap(text, width))
    return Paragraph(wrapped_text, ParagraphStyle('Normal'))

def generate_combined_report(combined_results):
    """Generates a combined PDF report for multiple URLs with enhanced formatting"""
    report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"security_scan_report_{report_time}.pdf"
    
    doc = SimpleDocTemplate(
        report_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    heading2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    vuln_style = ParagraphStyle(
        'VulnerabilityStyle',
        parent=styles['Normal'],
        spaceAfter=10,
        leftIndent=20
    )
    
    elements = []
    
    # Title and Executive Summary sections
    elements.append(Paragraph("Security Scan Combined Report", title_style))
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Executive Summary", heading2_style))
    elements.append(Spacer(1, 10))
    
    summary_data = [
        ["Scan Start Time:", combined_results['scan_start_time']],
        ["Scan End Time:", combined_results['scan_end_time']],
        ["Total Scan Duration:", f"{round(combined_results['total_scan_duration'], 2)} seconds"],
        ["Total URLs Scanned:", str(len(combined_results['urls_scanned']))],
        ["High Severity Vulnerabilities:", str(combined_results['total_vulnerabilities']['High'])],
        ["Medium Severity Vulnerabilities:", str(combined_results['total_vulnerabilities']['Medium'])],
        ["Low Severity Vulnerabilities:", str(combined_results['total_vulnerabilities']['Low'])]
    ]
    
    wrapped_summary_data = [[create_wrapped_cell(cell) for cell in row] for row in summary_data]
    summary_table = Table(wrapped_summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Detailed Scan Results", heading2_style))
    elements.append(Spacer(1, 20))
    
    for url_result in combined_results['detailed_results']:
        elements.append(Paragraph(f"Target URL: {url_result['url']}", heading2_style))
        elements.append(Spacer(1, 10))
        
        # URL Details Table
        url_details = [
            ["Scan Duration:", f"{url_result['scan_duration']} seconds"],
            ["URLs Crawled:", str(url_result['crawl_data']['num_crawls'])],
            ["Attack Performed:", str(url_result['attack_performed'])],
            ["Attack Type:", url_result['attack_type']],
            ["High Severity Findings:", str(url_result['vulnerability_counts']['High'])],
            ["Medium Severity Findings:", str(url_result['vulnerability_counts']['Medium'])],
            ["Low Severity Findings:", str(url_result['vulnerability_counts']['Low'])]
        ]
        
        wrapped_url_details = [[create_wrapped_cell(cell) for cell in row] for row in url_details]
        url_table = Table(wrapped_url_details, colWidths=[2*inch, 4*inch])
        url_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(url_table)
        elements.append(Spacer(1, 20))
        
        # Crawled URLs section - simplified to just show the list
        if 'crawled_urls' in url_result['crawl_data']:
            elements.append(Paragraph("Crawled URLs:", heading2_style))
            elements.append(Spacer(1, 10))
            
            crawled_urls_data = [["#", "URL"]]
            for idx, crawled_url in enumerate(url_result['crawl_data']['crawled_urls'], 1):
                crawled_urls_data.append([str(idx), crawled_url])
            
            wrapped_crawled_data = [[create_wrapped_cell(cell, width=40) for cell in row] for row in crawled_urls_data]
            crawled_table = Table(wrapped_crawled_data, colWidths=[0.5*inch, 5.5*inch])
            crawled_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(crawled_table)
            elements.append(Spacer(1, 20))
        
        # Vulnerabilities Details
        if url_result['vulnerabilities']:
            elements.append(Paragraph("Detected Vulnerabilities:", heading2_style))
            elements.append(Spacer(1, 10))
            
            for vuln in url_result['vulnerabilities']:
                if vuln['risk'] == 'High':
                    bg_color = colors.mistyrose
                elif vuln['risk'] == 'Medium':
                    bg_color = colors.lightgoldenrodyellow
                else:
                    bg_color = colors.lightgreen
                
                vuln_data = [
                    ["Name:", vuln['name']],
                    ["Risk Level:", vuln['risk']],
                    ["Description:", vuln['description']],
                    ["Solution:", vuln['solution']],
                    ["Affected URL:", vuln.get('affected_url', 'N/A')]
                ]
                
                wrapped_vuln_data = [[create_wrapped_cell(cell, width=50) for cell in row] for row in vuln_data]
                vuln_table = Table(wrapped_vuln_data, colWidths=[1.5*inch, 4.5*inch])
                vuln_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (1, 1), bg_color)
                ]))
                
                elements.append(vuln_table)
                elements.append(Spacer(1, 15))
        
        elements.append(PageBreak())
    
    # Build the PDF
    doc.build(elements)
    print(colored(f"\nCombined PDF report generated: {report_filename}", "green"))