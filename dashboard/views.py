from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required

import requests
from datetime import datetime
import base64
import dateutil.parser
import json
from decimal import *
import logging

# Create a logger for this file
logger = logging.getLogger(__file__)

TWO_DECIMAL_PLACES = Decimal('0.00')

# build interface message method
def build_interface_message(base64_message, interface_code):
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

    interface_message = ('{'
        '"data": {'
        '"content": "'+ base64_message +'",'
            '"signature": "",'
            '"dataDescription": {'
                '"codeType": "0",'
                '"encryptCode": "1",'
                '"zipCode": "0"'
           ' }},'
       ' "globalInfo": {'
            '"appId": "AP04",'
            '"version": "1.1.20191201",'
            '"dataExchangeId": "9230489223014123",'
            '"interfaceCode": "'+ interface_code +'",'
            '"requestCode": "TP",'
            '"requestTime": "'+ datetime_str +'",'
            '"responseCode": "TA",'
            '"userName": "1000024517",'
            '"deviceMAC": "005056B65332",'
            '"deviceNo": "TCSff5ba51958634436",'
            '"tin": "1000024517",'
            '"brn": "",'
            '"taxpayerID": "1000024517",'
            '"longitude": "116.397128",'
            '"latitude": "39.916527",'
            '"extendField": {'
                '"responseDateFormat": "dd/MM/yyyy",'
                '"responseTimeFormat": "dd/MM/yyyy HH:mm:ss"'
            '}'
        '},'
        '"returnStateInfo": {'
            '"returnCode": "",'
            '"returnMessage": ""'
       ' }'
    '}')

    interface_message = json.loads(interface_message)

    return interface_message

def build_base64_string(message):
    # encode message to base64 bytes
    message_bytes = message.encode('ascii')
    # decode base64 bytes to string
    base64_string = base64.b64encode(message_bytes).decode('ascii')

    return base64_string

@login_required(login_url='login')
def credit_notes(request):
    context = {
        'page': 'Credit Notes',
    }
    return render(request, 'dashboard/credit-notes.html', context)

@login_required(login_url='login')
def service_credit_notes(request):
    context = {
        'page': 'Service Credit Notes',
    }
    return render(request, 'dashboard/service_credit_notes.html', context)

@login_required(login_url='login')
def service_invoices(request):
    context = {
        'page': 'Service Invoices',
    }
    return render(request, 'dashboard/service_invoices.html', context)

@login_required(login_url='login')
def invoices(request):
    context = {
        'page': 'Item Invoices',
    }
    return render(request, 'dashboard/invoices.html', context)

def login(request):
    context = {
        'page': 'Login',
    }
    return render(request, 'dashboard/login.html', context)

def load_items(request):
    url = 'http://localhost:8280/services/GetItems/getitems'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_invoices(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllInvoiceHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        # pagination logic
        paginator = Paginator(data['invoiceHeaders']['header'], 10)
        page = request.GET.get('page')

        invoices_page = paginator.page(page)

        pagination_data = {
            'invoices': invoices_page.object_list,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'next_page': invoices_page.has_next(),
            'previous_page': invoices_page.has_previous(),
        }

        return JsonResponse(pagination_data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_service_invoices(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllServiceInvoiceHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        # pagination logic
        paginator = Paginator(data['invoiceHeaders']['header'], 10)
        page = request.GET.get('page')

        invoices_page = paginator.page(page)

        pagination_data = {
            'invoices': invoices_page.object_list,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'next_page': invoices_page.has_next(),
            'previous_page': invoices_page.has_previous(),
        }

        return JsonResponse(pagination_data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_invoices(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllInvoiceHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        # pagination logic
        paginator = Paginator(data['invoiceHeaders']['header'], 10)
        page = request.GET.get('page')

        invoices_page = paginator.page(page)

        pagination_data = {
            'invoices': invoices_page.object_list,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'next_page': invoices_page.has_next(),
            'previous_page': invoices_page.has_previous(),
        }

        return JsonResponse(pagination_data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_credit_notes(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllCreditNoteHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        # pagination logic
        paginator = Paginator(data['creditNoteHeaders']['header'], 10)
        page = request.GET.get('page')

        credit_notes_page = paginator.page(page)

        pagination_data = {
            'credit_notes': credit_notes_page.object_list,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'next_page': credit_notes_page.has_next(),
            'previous_page': credit_notes_page.has_previous(),
        }

        return JsonResponse(pagination_data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_service_credit_notes(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllServiceCreditNoteHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        # pagination logic
        paginator = Paginator(data['creditNoteHeaders']['header'], 10)
        page = request.GET.get('page')

        credit_notes_page = paginator.page(page)

        pagination_data = {
            'credit_notes': credit_notes_page.object_list,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'next_page': credit_notes_page.has_next(),
            'previous_page': credit_notes_page.has_previous(),
        }

        return JsonResponse(pagination_data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_company_info(request):
    url = 'http://localhost:8280/services/sybyl-efris/getCompanyInformation'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_credit_note_id(request):
    credit_note_id = request.GET['credit_note_id']
    doc_num = request.GET['doc_num']
    service_name = request.GET['service_name']
    url = ''

    if service_name == 'item credit notes':
        url = 'http://localhost:8280/services/sybyl-efris/updateCreditNoteID'
        req_message = (
        '<_putupdatecreditnoteid>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ credit_note_id +'</uraRefNo>'
            '<qrcode></qrcode>'
        '</_putupdatecreditnoteid>')
    else:
        url = 'http://localhost:8280/services/sybyl-efris/updateServiceCreditNoteId'
        req_message = (
        '<_putupdateservicecreditnoteidquery>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ credit_note_id +'</uraRefNo>'
            '<qrcode></qrcode>'
        '</_putupdateservicecreditnoteidquery>')

    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_urainvoicenum_qrcode(request):
    ura_invoice_num = request.GET['ura_invoice_num']
    qrcode = request.GET['qrcode']
    doc_num = request.GET['doc_num']
    ura_ref_no = request.GET['ura_ref_no']
    verification_code = request.GET['verification_code']
    service_name = request.GET['service_name']
    url = ''
    req_message = ''

    if service_name == 'item invoices':
        url = 'http://localhost:8280/services/sybyl-efris/updateUraInvoiceAndQrcode'
        req_message = (
        '<_putupdateuraoriginalinvoicenumberandqrcode>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ ura_ref_no +'</uraRefNo>'
            '<verificationCode>'+ verification_code +'</verificationCode>'
        '</_putupdateuraoriginalinvoicenumberandqrcode>')
    else:
        url = 'http://localhost:8280/services/sybyl-efris/updateServiceInvoiceHeader'
        req_message = (
        '<_putupdateserviceinvoiceheaderquery>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ ura_ref_no +'</uraRefNo>'
            '<verificationCode>'+ verification_code +'</verificationCode>'
        '</_putupdateserviceinvoiceheaderquery>')

    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_credit_note_three(request):
    ura_invoice_num = request.GET['ura_invoice_num']
    qrcode = request.GET['qrcode']
    doc_num = request.GET['doc_num']
    verification_code = request.GET['verification_code']

    url = 'http://localhost:8280/services/sybyl-efris/updateCreditNoteThree'
    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}
    req_message = (
        '<_putupdatecreditnotethree>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<verificationCode>'+ verification_code +'</verificationCode>'
        '</_putupdatecreditnotethree>')

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_credit_note_header(request):
    ura_invoice_num = request.GET['ura_invoice_num']
    qrcode = request.GET['qrcode']
    doc_num = request.GET['doc_num']
    ura_ref_no = request.GET['ura_ref_no']
    verification_code = request.GET['verification_code']
    service_name = request.GET['service_name']
    url = ''
    req_message = ''

    if service_name == 'item credit notes':
        url = 'http://localhost:8280/services/sybyl-efris/updateCreditNoteHeader'
        req_message = (
        '<_putupdatecreditnoteheader>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ ura_ref_no +'</uraRefNo>'
            '<verificationCode>'+ verification_code +'</verificationCode>'
        '</_putupdatecreditnoteheader>')
    else:
        url = 'http://localhost:8280/services/sybyl-efris/updateServiceCreditNoteHeader'
        req_message = (
        '<_putupdateservicecreditnoteheaderquery>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
            '<uraRefNo>'+ ura_ref_no +'</uraRefNo>'
            '<verificationCode>'+ verification_code +'</verificationCode>'
        '</_putupdateservicecreditnoteheaderquery>')


    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def upload_invoice(request):
    documentNumber = request.GET['documentNumber']
    service_name = request.GET['service_name']
    specific_invoice_header_url = ''
    specific_invoice_lines_url = ''
    customer_number = ''
    goodsDetailsBody = '{}'
    goodsDetailsHeader = '"goodsDetails": []'
    goodsDetailsFooter = '],'
    taxDetailsHeader = '"taxDetails": []'
    total = Decimal(0.00)
    tax_amount = Decimal(0.00)
    total_amount = Decimal(0.00)
    total_amount_vat = Decimal(0.00)
    number_of_items = 0

    if service_name == 'item invoices':
        specific_invoice_header_url = 'http://localhost:8280/services/sybyl-efris/getSpecificInvoiceHeader?documentNumber='+documentNumber
        specific_invoice_lines_url = 'http://localhost:8280/services/sybyl-efris/getSpecificInvoiceLines?documentNumber='+documentNumber
    else:
        specific_invoice_header_url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceInvoiceHeader?documentNumber='+documentNumber
        specific_invoice_lines_url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceInvoiceLines?documentNumber='+documentNumber

    data = {}

    #####################################################################################################
    company_infor_response = requests.get('http://localhost:8280/services/sybyl-efris/getCompanyInformation', headers={'Accept':'application/json'})
    company_data = ''
    if company_infor_response.status_code == 200:
        company_data = company_infor_response.json()

    else:
        logger.error("Error fetching company information")

    #####################################################################################################
    document_header_response = requests.get(specific_invoice_header_url, headers={'Accept':'application/json'})

    if document_header_response.status_code == 200:
        document_header_data = document_header_response.json()
        partdata = document_header_data['invoiceHeader']['header'][0]

        customer_number = partdata['customerNumber']
        ref_no = partdata['antifakeCode']

        seller_details = ('"sellerDetails": {'
        '"tin":"' + company_data['company']['details'][0]['tin'] + '",'
        '"ninBrn":"' + company_data['company']['details'][0]['ninBrn'] + '",'
        '"legalName":"' + company_data['company']['details'][0]['legalName'] + '",'
        '"businessName":"' + company_data['company']['details'][0]['businessName'] + '",'
        '"address":"' + company_data['company']['details'][0]['address'] + '",'
        '"mobilePhone":"' + company_data['company']['details'][0]['mobilePhone'] + '",'
        '"linePhone":"' + company_data['company']['details'][0]['linePhone'] + '",'
        '"emailAddress":"' + company_data['company']['details'][0]['emailAddress'] + '",'
        '"placeOfBusiness":"' + company_data['company']['details'][0]['placeOfBusiness'] + '",'
        '"referenceNo":"'+ ref_no +'",'
        '"branchId":"' + company_data['company']['details'][0]['branchId'] + '"'
        '}')

        document_date = dateutil.parser.parse(partdata['documentDate']) 
        currency = "UGX" if not partdata['currency'] else partdata['currency']
        issue_date = document_date.strftime('%Y-%m-%d %H:%M:%S')

        basic_information = ('"basicInformation": {'
        '"invoiceNo": "'+ partdata['invoiceNo'] +'",'
        '"antifakeCode": "'+ partdata['antifakeCode'] +'",'
        '"deviceNo": "TCSff5ba51958634436",'
        '"issuedDate": "'+ issue_date +'",'
        '"operator": "'+ partdata['operator'] +'",'
        '"currency": "'+ currency +'",'
        '"oriInvoiceId": "'+ partdata['invoiceNo'] +'",'
        '"invoiceType": "'+ partdata['invoiceType'] +'",'
        '"invoiceKind": "'+ partdata['invoiceKind'] +'",'
        '"dataSource": "101",'
        '"invoiceIndustryCode": "'+ partdata['invoiceIndustryCode'] +'",'
        '"isBatch": "0"'
        '}')

    else: 
        logger.error("Failed to fetch invoice details.")

    #######################################################################################################
    document_lines_response = requests.get(specific_invoice_lines_url, headers={'Accept':'application/json'})

    if document_lines_response.status_code == 200:
        counter = 0
        document_lines_data = document_lines_response.json()
        partdata =  document_lines_data['invoiceLines']['line']
        number_of_lines = len(partdata)
        number_of_items = 0   
        total_amount_vat = Decimal(0.0)
        total_amount = Decimal(0.0)   
        total_net = Decimal(0.0)      

        goodsDetailsHeader = '"goodsDetails": ['
        goodsDetailsFooter = ']'

        taxDetailsHeader = '"taxDetails": ['
        taxDetailsFooter = ']'
    
        while counter < number_of_lines:
            tax = str((Decimal(partdata[counter]['amountIncludingVat']) - Decimal(partdata[counter]['total'])).quantize(TWO_DECIMAL_PLACES))
            total = str((Decimal(partdata[counter]['total']) * Decimal(partdata[counter]['qty'])).quantize(TWO_DECIMAL_PLACES))
            item = (partdata[counter]['item']).replace('"', '\\"')
            tax_rate = str((Decimal(partdata[counter]['taxRate']) / 100).quantize(TWO_DECIMAL_PLACES))
            number_of_items = number_of_items + int(Decimal(partdata[counter]['qty']))
            tax_category = partdata[counter]['vatProdPostingGroup']

            if tax_category == 'VAT18-P' or tax_category == 'VAT18-E':
                tax_category = 'STANDARD'
            elif tax_category == '':
                tax_category = 'ZERO RATE'
            elif tax_category == 'ZERO RATED':
                tax_category = 'ZERO RATE'


            # total amount including VAT
            total_amount_vat = (total_amount_vat + (Decimal(partdata[counter]['amountIncludingVat']))).quantize(TWO_DECIMAL_PLACES)

            total_amount = (total_amount + (Decimal(partdata[counter]['total']))).quantize(TWO_DECIMAL_PLACES)

            # discount total
            discount_total = ''
            discount_flag = partdata[counter]['discountFlag']

            if discount_flag == '0' or discount_flag == '2':
                discount_total = ''
            else:
                discount_total = '-'+partdata[counter]['discountTaxRate']
            #########################################################################

            unit_of_measure = partdata[counter]['unitOfMeasure']

            if unit_of_measure == 'UNIT':
                unit_of_measure = 'UN'
            elif unit_of_measure == 'PIECES':
                unit_of_measure = 'PP'
            else:
                unit_of_measure = partdata[counter]['unitOfMeasure']

            if partdata[counter]['deemedFlag'] == '1':
                item_name = item+' (Deemed)'
            else:
                item_name = item

            goodsDetailsBody = ('{'
                                    '"item": "'+ item_name +'",'
                                    '"itemCode": "'+ partdata[counter]['itemCode'] +'",'
                                    '"qty": "'+ str(int(Decimal(partdata[counter]['qty']))) +'",'
                                    '"unitOfMeasure": "'+ unit_of_measure +'",'
                                    '"unitPrice": "'+ str((Decimal(partdata[counter]['unitPrice']) + Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
                                    '"total": "'+ str((Decimal(partdata[counter]['unitPrice']) + (Decimal(tax) * int(Decimal(partdata[counter]['qty'])))).quantize(TWO_DECIMAL_PLACES)) +'",'
                                    '"taxRate": "'+ tax_rate +'",'
                                    '"tax": "'+ tax +'",'
                                    '"discountTotal": "'+ discount_total +'",'
                                    '"discountTaxRate": "'+ str(Decimal(partdata[counter]['discountTaxRate']).quantize(TWO_DECIMAL_PLACES)) +'",'
                                    '"orderNumber": "'+ str(counter) +'",'
                                    '"discountFlag": "'+ partdata[counter]['discountFlag']+ '",'
                                    '"deemedFlag": "'+ partdata[counter]['deemedFlag'] +'",'
                                    '"exciseFlag": "'+ partdata[counter]['exciseFlag'] +'",'
                                    '"categoryId": "",'
                                    '"categoryName": "",'
                                    '"goodsCategoryId": "'+ str(partdata[counter]['goodsCategoryId']) +'",'
                                    '"goodsCategoryName": "",'
                                    '"exciseRate": "",'
                                    '"exciseRule": "",'
                                    '"exciseTax": "",'
                                    '"pack": "",'
                                    '"stick": "",'
                                    '"exciseUnit": "",'
                                    '"exciseCurrency": "",'
                                    '"exciseRateName": ""'
            '}')

            if counter != number_of_lines - 1:
                goodsDetailsBody = goodsDetailsBody + ','

            goodsDetailsHeader = goodsDetailsHeader + goodsDetailsBody

            taxDetailsBody = ('{'
                '"taxCategory": "'+ tax_category +'",'
                '"netAmount": "'+ str((Decimal(partdata[counter]['amountIncludingVat']) - Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"taxRate": "'+ tax_rate +'",'
                '"taxAmount": "'+ tax +'",'
                '"grossAmount": "'+ str(Decimal(partdata[counter]['amountIncludingVat']).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"exciseUnit": "",'
                '"exciseCurrency": "",'
                '"taxRateName": "'+str(Decimal(partdata[counter]['taxRate']).quantize(TWO_DECIMAL_PLACES))+'%"'
            '}')

            if counter != number_of_lines - 1:
                taxDetailsBody = taxDetailsBody + ','

            taxDetailsHeader = taxDetailsHeader + taxDetailsBody
            counter = counter + 1

        goodsDetailsHeader = goodsDetailsHeader + goodsDetailsFooter
        taxDetailsHeader = taxDetailsHeader + taxDetailsFooter

    else:
        logger.error("Failed to fetch invoice lines.")

    buyer_infor_response = requests.get('http://localhost:8280/services/sybyl-efris/getCustomerInformation?customerNo='+customer_number, headers={'Accept': 'application/json'})

    if buyer_infor_response.status_code == 200:
        buyer_infor_data = buyer_infor_response.json()
        if(bool(buyer_infor_data['customer'])):
            partdata = buyer_infor_data['customer']['details'][0]
            buyer_details = ('"buyerDetails": {'
                '"buyerTin": "'+ partdata['buyerTin'] +'",'
                '"buyerNinBrn": "'+ partdata['buyerNinBrn'] +'",'
                '"buyerPassportNum": "'+ partdata['buyerPassportNum'] +'",'
                '"buyerLegalName": "'+ partdata['name'] +'",'
                '"buyerBusinessName": "'+ partdata['buyerBusinessName'] +'",'
                '"buyerAddress": "'+ partdata['buyerAddress'] +'",'
                '"buyerEmail": "'+ partdata['buyerEmail'] +'",'
                '"buyerMobilePhone": "'+ partdata['buyerMobilePhone'] +'",'
                '"buyerLinePhone": "'+ partdata['buyerLinePhone'] +'",'
                '"buyerPlaceOfBusi": "'+ partdata['buyerPlaceOfBusi'] +'",'
                '"buyerType": "'+ partdata['buyerType']+'",'
                '"buyerCitizenship": "'+ partdata['buyerCitizenship'] +'",'
                '"buyerSector": "",'
                '"buyerReferenceNo": ""'
                '}')
        else:
            buyer_details = '''"buyerDetails": {
                "buyerTin": "",
                "buyerNinBrn": "",
                "buyerPassportNum": "",
                "buyerLegalName": "",
                "buyerBusinessName": "",
                "buyerAddress": "",
                "buyerEmail": "",
                "buyerMobilePhone": "",
                "buyerLinePhone": "",
                "buyerPlaceOfBusi": "",
                "buyerType": "1",
                "buyerCitizenship": "",
                "buyerSector": "",
                "buyerReferenceNo": ""
                }'''

    buyer_extend_infor = '''"buyerExtend": {
	"propertyType": "",
	"district": "",
	"municipalityCounty": "",
	"divisionSubcounty": "",
	"town": "",
	"cellVillage": "",
	"effectiveRegistrationDate": "",
	"meterStatus": ""
	}'''

    if goodsDetailsHeader != '"goodsDetails": [],':
        upload_invoice_message =  ('{'+seller_details+','+ basic_information+','+buyer_details+','+ buyer_extend_infor+','
                +goodsDetailsHeader+','+ taxDetailsHeader+','+
                '"summary": {'
                '"netAmount": "'+ str(total_amount) +'",'
                '"taxAmount": "'+ str(total_amount_vat - total_amount) +'",'
                '"grossAmount": "'+ str(total_amount_vat) +'",'
                '"itemCount": "'+ str(number_of_items) +'",'
                '"modeCode": "0",'
                '"remarks": "",'
                '"qrCode": ""'
                '},'
                '"payWay": [],'
                '"extend": {'
                '"reason": "",'
                '"reasonCode": ""},'
                '"importServicesSeller": {}'
                '}')
    else:
        upload_invoice_message =  ('{'+seller_details+','+ basic_information+','+buyer_details+','+ buyer_extend_infor+','
                +goodsDetailsHeader+','+ taxDetailsHeader+','+
                '"summary": {'
                '"netAmount": "",'
                '"taxAmount": "",'
                '"grossAmount": "",'
                '"itemCount": "",'
                '"modeCode": "0",'
                '"remarks": "",'
                '"qrCode": ""'
                '},'
                '"payWay": [],'
                '"extend": {'
                '"reason": "",'
                '"reasonCode": ""},'
                '"importServicesSeller": {}'
                '}')

    logger.info('invoice message = '+upload_invoice_message)

    interface_code = 'T109'
    base64_message = build_base64_string(upload_invoice_message)
    interface_message = build_interface_message(base64_message, interface_code)

    finalupload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_message)

    if finalupload.status_code == 200:
        finaluploaddata = finalupload.json()
        return_message = finaluploaddata['returnStateInfo']['returnMessage']
        return_code = finaluploaddata['returnStateInfo']['returnCode']
        return_data = finaluploaddata['data']

        message = return_message

        if return_message == 'SUCCESS':
            content_base64 = finaluploaddata['data']['content']
            content_decoded = base64.b64decode(content_base64).decode('ascii')

            # convert to json
            content_json = json.loads(content_decoded)

            # get the invoice number
            invoice_number = content_json['basicInformation']['invoiceNo']
            qrcode = content_json['summary']['qrCode']
            ura_ref_no = content_json['basicInformation']['invoiceId']
            verification_code = content_json['basicInformation']['antifakeCode']

            uri = ''
            #update external document number
            if service_name == 'item invoices':
                uri = 'http://localhost/dashboard/update_urainvoicenum_qrcode?ura_invoice_num='+ invoice_number +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+ura_ref_no+'&verification_code='+verification_code+'&service_name=item invoices'
            else:
                uri = 'http://localhost/dashboard/update_urainvoicenum_qrcode?ura_invoice_num='+ invoice_number +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+ura_ref_no+'&verification_code='+verification_code+'&service_name=service invoices'
            upex = requests.get(uri)

            if upex.status_code == 200:
                message = 'E-invoice ('+invoice_number+') successfully generated + Ura orginal invoice number ('+ invoice_number +'), Qrcode ('+ qrcode +') , URA reference No ('+ ura_ref_no +') and verification code ('+ verification_code +') updated in navision database'
            else:
                message = 'E-invoice ('+invoice_number+')  successfully generated + failed to update Ura orginal invoice number ('+ invoice_number +'), Qrcode ('+ qrcode +'), URA reference No ('+ ura_ref_no +') and verification code ('+ verification_code +') in navision database'

        data = {
                    'data': return_data,
                    'externalDocNumber': '',
                    'docNumber': ''+documentNumber,
                    'returnStateInfo': {
                        'returnCode': ''+str(return_code),
                        'returnMessage': ''+message
                    }
                    
                }
        return JsonResponse(data, status=200)
        
    else: 
        data = {
            'errorcode':''+str(finalupload.status_code)
        }
        return JsonResponse(data, status=400)

def upload_credit_note(request):
    documentNumber = request.GET['documentNumber']
    service_name = request.GET['service_name']
    specific_credit_note_header_url = ''
    specific_credit_note_lines_url = ''
    total_amount = Decimal(0.00)
    total_amount_vat = Decimal(0.00)
    number_of_items = 0
    goodsDetailsBody = '{}'
    goodsDetailsHeader = '"goodsDetails": [],'
    goodsDetailsFooter = '],'
    taxDetailsHeader = '"taxDetails": [],'

    if service_name == 'item credit notes':
        specific_credit_note_header_url = 'http://localhost:8280/services/sybyl-efris/getSpecificCreditNoteHeader?creditNoteNo='+documentNumber
        specific_credit_note_lines_url = 'http://localhost:8280/services/sybyl-efris/getSpecificCreditNoteLines?creditNoteNo='+documentNumber
    else:
        specific_credit_note_header_url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceCreditNoteHeader?creditNoteNo='+documentNumber
        specific_credit_note_lines_url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceCreditNoteLines?creditNoteNo='+documentNumber

    data = {}
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

    document_header_response = requests.get(specific_credit_note_header_url, headers={'Accept':'application/json'})

    if document_header_response.status_code == 200:
        document_header_data = document_header_response.json()
        partdata = document_header_data['creditNoteHeader']['header'][0]

        orginal_invoice_num = partdata['oriInvoiceNo']
        document_date = dateutil.parser.parse(partdata['applicationTime']) 
        currency = "UGX" if not partdata['currency'] else partdata['currency']
        application_time = document_date.strftime('%Y-%m-%d %H:%M:%S')
        orginal_invoice_id = ''
        seller_ref_num = partdata['creditNoteNo']

        if partdata['uraReferenceNo'] == '':
            orginal_invoice_id = '618344974134880543'
        else:
            orginal_invoice_id = partdata['uraReferenceNo']


        top = (
                '"oriInvoiceId": "'+ orginal_invoice_id +'",'
                '"oriInvoiceNo": "'+ orginal_invoice_num +'",'
                '"reasonCode": "'+ partdata['reasonCode'] +'",'
                '"reason": "'+ partdata['reason'] +'",'
                '"applicationTime": "'+ application_time +'",'
                '"invoiceApplyCategoryCode": "101",'
                '"currency": "'+ currency +'",'
                '"contactName": "",'
                '"contactMobileNum": "",'
                '"contactEmail": "",'
                '"source": "101",'
                '"remarks": "",'
                '"sellersReferenceNo": "'+ seller_ref_num +'",')
    else: 
        logger.error("Failed to fetch credit note header.")

    document_lines_response = requests.get(specific_credit_note_lines_url, headers={'Accept':'application/json'})

    if document_lines_response.status_code == 200:
        document_lines_data = document_lines_response.json()
        counter = 0
        partdata =  document_lines_data['creditNoteLines']['line']
        number_of_lines = len(partdata)
        number_of_items = 0   
        total_amount_vat = Decimal(0.0)
        total_amount = Decimal(0.0)   
        total_net = Decimal(0.0)      

        goodsDetailsHeader = '"goodsDetails": ['
        goodsDetailsFooter = '],'

        taxDetailsHeader = '"taxDetails": ['
        taxDetailsFooter = '],'
    
        while counter < number_of_lines:
            tax = str((Decimal(partdata[counter]['amountIncludingVat']) - Decimal(partdata[counter]['total'])).quantize(TWO_DECIMAL_PLACES))
            total = str((Decimal(partdata[counter]['total']) * Decimal(partdata[counter]['qty'])).quantize(TWO_DECIMAL_PLACES))
            customerNumber = partdata[counter]['customerNo']
            item = (partdata[counter]['item']).replace('"', '\\"')
            tax_rate = str((Decimal(partdata[counter]['taxRate']) / 100).quantize(TWO_DECIMAL_PLACES))
            number_of_items = number_of_items + int(Decimal(partdata[counter]['qty']))

            tax_category = partdata[counter]['taxCategory']

            if tax_category == 'VAT18-P' or tax_category == 'VAT18-E':
                tax_category = 'STANDARD'
            elif tax_category == '':
                tax_category = 'ZERO RATE'
            elif tax_category == 'ZERO RATED':
                tax_category = 'ZERO RATE'

            if tax_rate == '0.00':
                tax_rate = '0';

           # total amount including VAT
            total_amount_vat = (total_amount_vat + (Decimal(partdata[counter]['amountIncludingVat']))).quantize(TWO_DECIMAL_PLACES)

            total_amount = (total_amount + (Decimal(partdata[counter]['total']))).quantize(TWO_DECIMAL_PLACES)

            # discount totl
            discount_total = ''
            discount_flag = partdata[counter]['discountFlag']

            if discount_flag == '0' or discount_flag == '2':
                discount_total = ''
            else:
                a = Decimal(partdata[counter]['discountTaxRate']).quantize(TWO_DECIMAL_PLACES)
                if a == 0.00:
                    discount_total = str(a)
                else:
                    discount_total = '-'+str(a)

            #########################################################################

            unit_of_measure = partdata[counter]['unitOfMeasure']
            if unit_of_measure == 'UNIT':
                unit_of_measure = 'UN'
            elif unit_of_measure == 'PIECES':
                unit_of_measure = 'PP'
            else:
                unit_of_measure = partdata[counter]['unitOfMeasure']

            if partdata[counter]['deemedFlag'] == '1':
                item_name = item+' (Deemed)'
            else:
                item_name = item

            goodsDetailsBody = ('{'
            '"item": "'+ item_name +'",'
            '"itemCode": "'+ partdata[counter]['itemCode'] +'",'
            '"qty": "-'+ str(int(Decimal(partdata[counter]['qty']))) +'",'
            '"unitOfMeasure": "'+ unit_of_measure +'",'
            '"unitPrice": "'+ str((Decimal(partdata[counter]['unitPrice']) + Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
            '"total": "-'+ str((Decimal(partdata[counter]['unitPrice']) + (Decimal(tax) * int(Decimal(partdata[counter]['qty'])))).quantize(TWO_DECIMAL_PLACES)) +'",'
            '"taxRate": "'+ tax_rate +'",'
            '"tax": "-'+ tax +'",'
            '"discountTotal": "'+ discount_total +'",'
            '"discountTaxRate": "'+ str(Decimal(partdata[counter]['discountTaxRate']).quantize(TWO_DECIMAL_PLACES)) +'",'
            '"orderNumber": "'+ str(counter) +'",'
            '"discountFlag": "'+ partdata[counter]['discountFlag']+ '",'
            '"deemedFlag": "'+ partdata[counter]['deemedFlag'] +'",'
            '"exciseFlag": "'+ partdata[counter]['exciseFlag'] +'",'
            '"categoryId": "",'
            '"categoryName": "",'
            '"goodsCategoryId": "'+ str(partdata[counter]['goodsCategoryId']) +'",'
            '"goodsCategoryName": "",'
            '"exciseRate": "",'
            '"exciseRule": "",'
            '"exciseTax": "",'
            '"pack": "",'
            '"stick": "",'
            '"exciseUnit": "",'
            '"exciseCurrency": "",'
            '"exciseRateName": ""'
            '}')

            if counter != number_of_lines - 1:
                goodsDetailsBody = goodsDetailsBody + ','

            goodsDetailsHeader = goodsDetailsHeader + goodsDetailsBody

            taxDetailsBody = ('{'
                '"taxCategory": "'+ tax_category +'",'
                '"netAmount": "-'+ str((Decimal(partdata[counter]['amountIncludingVat']) - Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"taxRate": "'+ tax_rate +'",'
                '"taxAmount": "-'+ tax +'",'
                '"grossAmount": "-'+ str(Decimal(partdata[counter]['amountIncludingVat']).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"exciseUnit": "",'
                '"exciseCurrency": "",'
                '"taxRateName": "'+str(Decimal(partdata[counter]['taxRate']).quantize(TWO_DECIMAL_PLACES))+'%"'
            '}')

            if counter != number_of_lines - 1:
                taxDetailsBody = taxDetailsBody + ','

            taxDetailsHeader = taxDetailsHeader + taxDetailsBody
            counter = counter + 1

        goodsDetailsHeader = goodsDetailsHeader + goodsDetailsFooter
        taxDetailsHeader = taxDetailsHeader + taxDetailsFooter

    else:
        logger.error("Failed to fetch credit note lines.")
    
    bottom = ('"summary": {'
    '"netAmount": "-'+ str(total_amount) +'",'
    '"taxAmount": "-'+ str(total_amount_vat - total_amount) +'",'
    '"grossAmount": "-'+ str(total_amount_vat) +'",'
    '"itemCount": "'+ str(number_of_items) +'",'
    '"modeCode": "0",'
    '"qrCode": ""'
    '},'
    '"payWay": []')

    credit_note_message = ('{'
    ''+top+''
    ''+ goodsDetailsHeader +''
    ''+ taxDetailsHeader +''
    ''+bottom+''
    '}')

    logger.info('credit note message = '+credit_note_message)

    interface_code = 'T110'
    base64_message = build_base64_string(credit_note_message)
    interface_message = build_interface_message(base64_message, interface_code)

    finalupload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_message)

    if finalupload.status_code == 200:
        finaluploaddata = finalupload.json()
        return_message = finaluploaddata['returnStateInfo']['returnMessage']
        return_data = finaluploaddata['data']
        return_code = finaluploaddata['returnStateInfo']['returnCode']

        message = return_message

        if return_message == 'SUCCESS':
            content_base64 = finaluploaddata['data']['content']
            content_decoded = base64.b64decode(content_base64).decode('ascii')

            # convert to json
            content_json = json.loads(content_decoded)
            reference_num = content_json['referenceNo']

            # build interface T111 message
            interface_t111_message = ('{'
                    '"referenceNo": "'+ reference_num +'",'
                    '"oriInvoiceNo": "'+ orginal_invoice_num +'",'
                    '"invoiceNo": "",'
                    '"combineKeywords": "",'
                    '"approveStatus": "",'
                    '"queryType": "1",'
                    '"invoiceApplyCategoryCode": "",'
                    '"startDate": "",'
                    '"endDate": "",'
                    '"pageNo": "1",'
                    '"pageSize": "10"'
                '}')

            # encode message to base64 bytes
            message_bytes = interface_t111_message.encode('ascii')
            # decode base64 bytes to string
            base64_message = base64.b64encode(message_bytes).decode('ascii')

            interface_code = 'T111'
            base64_message = build_base64_string(interface_t111_message)
            interface_message = build_interface_message(base64_message, interface_code)

            t111_upload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_message)

            if t111_upload.status_code == 200:
                t111_data = t111_upload.json()
                return_message = t111_data['returnStateInfo']['returnMessage']
                return_data = t111_data['data']

                if return_message == 'SUCCESS':
                    content_base64 = t111_data['data']['content']
                    content_decoded = base64.b64decode(content_base64).decode('ascii')

                    # convert to json
                    content_json = json.loads(content_decoded)
                    credit_note_id = content_json['records'][0]['id']

                    # build interface T112 message
                    interface_t112_message = ('{'
                            '"id": "'+ credit_note_id +'"'
                        '}')

                    interface_code = 'T112'
                    base64_message = build_base64_string(interface_t112_message)
                    interface_message = build_interface_message(base64_message, interface_code)

                    t112_upload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_message)

                    if t112_upload.status_code == 200:
                        t112_data = t112_upload.json()
                        return_message = t112_data['returnStateInfo']['returnMessage']
                        return_data = t112_data['data']

                        if return_message == 'SUCCESS':
                            content_base64 = t112_data['data']['content']
                            content_decoded = base64.b64decode(content_base64).decode('ascii')

                            # convert to json
                            content_json = json.loads(content_decoded)
                            
                            if content_json.get('refundInvoiceNo') == None:
                                message = 'Credit note generated awaiting client approval'
                                uri = ''

                                if service_name == 'item credit notes':
                                    uri = 'http://localhost/dashboard/update_credit_note_id?credit_note_id='+credit_note_id+'&doc_num='+documentNumber+'&service_name=item credit notes'
                                else:
                                    uri = 'http://localhost/dashboard/update_credit_note_id?credit_note_id='+credit_note_id+'&doc_num='+documentNumber+'&service_name=service credit notes'
                                
                                upex = requests.get(uri)

                                if upex.status_code == 200:
                                    message = 'Credit note generated awaiting client approval'
                                else:
                                    message = 'Credit note generated awaiting client approval + failed to update credit note id'
    
                            else:
                                refund_invoice_num = content_json['refundInvoiceNo']

                                # build interface T108 message
                                interface_t108_message = ('{'
                                        '"invoiceNo": "'+ refund_invoice_num +'"'
                                    '}')

                                interface_code = 'T108'
                                base64_message = build_base64_string(interface_t108_message)
                                interface_message = build_interface_message(base64_message, interface_code)

                                t108_upload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_message)

                                if t108_upload.status_code == 200:
                                    t108_data = t108_upload.json()
                                    return_message = t108_data['returnStateInfo']['returnMessage']
                                    return_data = t108_data['data']

                                    if return_message == 'SUCCESS':
                                        content_base64 = t108_data['data']['content']
                                        content_decoded = base64.b64decode(content_base64).decode('ascii')

                                        # convert to json
                                        content_json = json.loads(content_decoded)

                                        # get fields
                                        verification_code = content_json['basicInformation']['antifakeCode']
                                        qrcode = content_json['summary']['qrCode']
                                        
                                        uri = ''

                                        if service_name == 'item credit notes':
                                            #update credit note header
                                            uri = 'http://localhost/dashboard/update_credit_note_header?ura_invoice_num='+ refund_invoice_num +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+credit_note_id+'&verification_code='+verification_code+'&service_name=item credit notes'
                                        else:
                                            #update credit note header
                                            uri = 'http://localhost/dashboard/update_credit_note_header?ura_invoice_num='+ refund_invoice_num +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+credit_note_id+'&verification_code='+verification_code+'&service_name=service credit notes'
                                        
                                        upex = requests.get(uri)

                                        if upex.status_code == 200:
                                            message = 'Credit note ('+refund_invoice_num+') successfully generated + credit note no('+ refund_invoice_num +'), Qrcode('+ qrcode +'), Credit Note ID ('+ credit_note_id +') and verification code ('+ verification_code +') updated in navision database'
                                        else:
                                            message = 'Credit note ('+refund_invoice_num+')  successfully generated + failed to update credit note no('+ refund_invoice_num +'), Qrcode('+ qrcode +'), Credit Note ID ('+ credit_note_id +') and verification code('+ verification_code +') in navision database'

        else:
            return_code = finaluploaddata['returnStateInfo']['returnCode']

        data = {
                    'data': return_data,
                    'docNumber': ''+documentNumber,
                    'returnStateInfo': {
                        'returnCode': ''+return_code,
                        'returnMessage': ''+message
                    }
                    
                }
    return JsonResponse(data, status=200)

def search_invoice(request):
    doc_num = request.GET.get('doc_num')
    url = 'http://localhost:8280/services/sybyl-efris/getSpecificInvoiceHeader?documentNumber='+doc_num

    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def search_service_invoice(request):
    doc_num = request.GET.get('doc_num')
    url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceInvoiceHeader?documentNumber='+doc_num

    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def search_credit_note(request):
    doc_num = request.GET.get('doc_num')
    url = 'http://localhost:8280/services/sybyl-efris/getSpecificCreditNoteHeader?creditNoteNo='+doc_num

    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def search_service_credit_note(request):
    doc_num = request.GET.get('doc_num')
    url = 'http://localhost:8280/services/sybyl-efris/getSpecificServiceCreditNoteHeader?creditNoteNo='+doc_num

    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        data = response.json()

        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def dd(request):
    documentNumber = request.GET['v']
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    credit_note_id = request.GET['credit_note_id']
    message = 'Credit note pending client approval'
    # build interface T112 message
    interface_t112_message = ('{'
            '"id": "'+ credit_note_id +'"'
        '}')

    # encode message to base64 bytes
    message_bytes = interface_t112_message.encode('ascii')
    # decode base64 bytes to string
    base64_message = base64.b64encode(message_bytes).decode('ascii')

    # complete T112 message
    complete_t112_message = ('{'
    '"data": {'
    '"content": "'+base64_message+'",'
        '"signature": "",'
        '"dataDescription": {'
            '"codeType": "0",'
            '"encryptCode": "1",'
            '"zipCode": "0"'
       ' }},'
    ' "globalInfo": {'
        '"appId": "",'
        '"version": "1.1.20191201",'
        '"dataExchangeId": "9230489223014123",'
        '"interfaceCode": "T112",'
        '"requestCode": "TP",'
        '"requestTime": "'+datetime_str+'",'
        '"responseCode": "TA",'
        '"userName": "1000024517",'
        '"deviceMAC": "005056B65332",'
        '"deviceNo": "TCSff5ba51958634436",'
        '"tin": "1000024517",'
        '"brn": "",'
        '"taxpayerID": "1000024517",'
        '"longitude": "116.397128",'
        '"latitude": "39.916527",'
        '"extendField": {'
            '"responseDateFormat": "dd/MM/yyyy",'
            '"responseTimeFormat": "dd/MM/yyyy HH:mm:ss"'
        '}'
    '},'
    '"returnStateInfo": {'
        '"returnCode": "",'
        '"returnMessage": ""'
    ' }'
    '}')

    # convert message to json
    interface_t112_json = json.loads(complete_t112_message)

    t112_upload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_t112_json)

    if t112_upload.status_code == 200:
        t112_data = t112_upload.json()
        return_message = t112_data['returnStateInfo']['returnMessage']
        return_data = t112_data['data']

        if return_message == 'SUCCESS':
            content_base64 = t112_data['data']['content']
            content_decoded = base64.b64decode(content_base64).decode('ascii')

            # convert to json
            content_json = json.loads(content_decoded)

            if content_json.get('refundInvoiceNo') == None:
                message = 'Credit note generated awaiting client approval'
                uri = 'http://localhost/dashboard/update_credit_note_id?credit_note_id='+credit_note_id+'&doc_num='+documentNumber
                upex = requests.get(uri)

                if upex.status_code == 200:
                    message = 'Credit note generated awaiting client approval'
                else:
                    message = 'Credit note generated awaiting client approval + failed to update credit note id'

            else:
                refund_invoice_num = content_json['refundInvoiceNo']

                # build interface T108 message
                interface_t108_message = ('{'
                        '"invoiceNo": "'+ refund_invoice_num +'"'
                    '}')

                # encode message to base64 bytes
                message_bytes = interface_t108_message.encode('ascii')
                # decode base64 bytes to string
                base64_message = base64.b64encode(message_bytes).decode('ascii')

                # complete T108 message
                complete_t108_message = ('{'
                        '"data": {'
                        '"content": "'+base64_message+'",'
                            '"signature": "",'
                            '"dataDescription": {'
                                '"codeType": "0",'
                                '"encryptCode": "1",'
                                '"zipCode": "0"'
                           ' }},'
                       ' "globalInfo": {'
                            '"appId": "",'
                            '"version": "1.1.20191201",'
                            '"dataExchangeId": "9230489223014123",'
                            '"interfaceCode": "T108",'
                            '"requestCode": "TP",'
                            '"requestTime": "'+datetime_str+'",'
                            '"responseCode": "TA",'
                            '"userName": "1000024517",'
                            '"deviceMAC": "005056B65332",'
                            '"deviceNo": "TCSff5ba51958634436",'
                            '"tin": "1000024517",'
                            '"brn": "",'
                            '"taxpayerID": "1000024517",'
                            '"longitude": "116.397128",'
                            '"latitude": "39.916527",'
                            '"extendField": {'
                                '"responseDateFormat": "dd/MM/yyyy",'
                                '"responseTimeFormat": "dd/MM/yyyy HH:mm:ss"'
                            '}'
                        '},'
                        '"returnStateInfo": {'
                            '"returnCode": "",'
                            '"returnMessage": ""'
                       ' }'
                    '}')

                # convert message to json
                interface_t108_json = json.loads(complete_t108_message)

                t108_upload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=interface_t108_json)

                if t108_upload.status_code == 200:
                    t108_data = t108_upload.json()
                    return_message = t108_data['returnStateInfo']['returnMessage']
                    return_data = t108_data['data']

                    if return_message == 'SUCCESS':
                        content_base64 = t108_data['data']['content']
                        content_decoded = base64.b64decode(content_base64).decode('ascii')

                        # convert to json
                        content_json = json.loads(content_decoded)

                        # get fields
                        verification_code = content_json['basicInformation']['antifakeCode']
                        qrcode = content_json['summary']['qrCode']

                        uri = ''

                        if service_name == 'item credit notes':
                            #update credit note header
                            uri = 'http://localhost/dashboard/update_credit_note_header?ura_invoice_num='+ refund_invoice_num +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+credit_note_id+'&verification_code='+verification_code+'&service_name=item credit notes'
                        else:
                            #update credit note header
                            uri = 'http://localhost/dashboard/update_credit_note_header?ura_invoice_num='+ refund_invoice_num +'&qrcode='+qrcode+'&doc_num='+documentNumber+'&ura_ref_no='+credit_note_id+'&verification_code='+verification_code+'&service_name=service credit notes'
                        
                        upex = requests.get(uri)

                        if upex.status_code == 200:
                            message = 'Credit note - credit note no('+ refund_invoice_num +'), Qrcode('+ qrcode +'), Credit Note ID ('+ credit_note_id +') and verification code ('+ verification_code +') successfully updated in navision database'
                        else:
                            message = 'Failed to update credit note no('+ refund_invoice_num +'), Qrcode('+ qrcode +'), Credit Note ID ('+ credit_note_id +') and verification code('+ verification_code +') in navision database'

    data = {
                    'data': return_data,
                    'externalDocNumber': '',
                    'docNumber': '',
                    'returnStateInfo': {
                        'returnCode': '',
                        'returnMessage': ''+message
                    }
                    
                }
    return JsonResponse(data, status=200)