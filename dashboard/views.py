from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import requests
from datetime import datetime
import base64
import dateutil.parser
import json
from decimal import *

TWO_DECIMAL_PLACES = Decimal('0.00')

def credit_notes(request):
    context = {
        'page': 'Credit Notes',
    }
    return render(request, 'dashboard/credit-notes.html', context)

def invoices(request):
    context = {
        'page': 'Invoices',
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
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_invoices(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllInvoiceHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def load_credit_notes(request):
    url = 'http://localhost:8280/services/sybyl-efris/getAllCreditNoteHeaders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)


def load_company_info(request):
    url = 'http://localhost:8280/services/sybyl-efris/getCompanyInformation'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_urainvoicenum_qrcode(request):
    ura_invoice_num = request.GET['ura_invoice_num']
    qrcode = request.GET['qrcode']
    doc_num = request.GET['doc_num']

    url = 'http://localhost:8280/services/sybyl-efris/updateUraInvoiceAndQrcode'
    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}
    req_message = (
        '<_putupdateuraoriginalinvoicenumberandqrcode>'
            '<uraOriginalInvoiceNo>'+ ura_invoice_num +'</uraOriginalInvoiceNo>'
            '<uraQrcode>'+ qrcode +'</uraQrcode>'
            '<documentNumber>'+ doc_num +'</documentNumber>'
        '</_putupdateuraoriginalinvoicenumberandqrcode>')

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def upload_invoice(request):
    documentNumber = request.GET['documentNumber']
    data = {}
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

    #####################################################################################################
    company_infor_response = requests.get('http://localhost:8280/services/sybyl-efris/getCompanyInformation', headers={'Accept':'application/json'})

    if company_infor_response.status_code == 200:
        company_data = company_infor_response.json()

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
        '"referenceNo":"' + company_data['company']['details'][0]['referenceNo'] + '",'
        '"branchId":"' + company_data['company']['details'][0]['branchId'] + '"'
        '}')

    else:
        print('error')

    #####################################################################################################
    document_header_response = requests.get('http://localhost:8280/services/sybyl-efris/getSpecificInvoiceHeader?documentNumber='+documentNumber, headers={'Accept':'application/json'})

    if document_header_response.status_code == 200:
        document_header_data = document_header_response.json()
        partdata = document_header_data['invoiceHeader']['header'][0]

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
        '"invoiceType": "1",'
        '"invoiceKind": "1",'
        '"dataSource": "101",'
        '"invoiceIndustryCode": "'+ partdata['invoiceIndustryCode'] +'",'
        '"isBatch": "0"'
        '}')

        print('basic information', basic_information)
    else: 
        print('error')

    #######################################################################################################
    document_lines_response = requests.get('http://localhost:8280/services/sybyl-efris/getSpecificInvoiceLines?documentNumber='+documentNumber, headers={'Accept':'application/json'})

    if document_lines_response.status_code == 200:
        document_lines_data = document_lines_response.json()
        counter = 0
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
            customerNumber = partdata[counter]['customerNo']
            item = partdata[counter]['item']
            tax_rate = str((Decimal(partdata[counter]['taxRate']) / 100).quantize(TWO_DECIMAL_PLACES))
            number_of_items = number_of_items + int(Decimal(partdata[counter]['qty']))

            # total amount including VAT
            total_amount_vat = (total_amount_vat + Decimal(tax) + (Decimal(partdata[counter]['total']) - Decimal(tax))).quantize(TWO_DECIMAL_PLACES)

            total_amount = (total_amount + (Decimal(partdata[counter]['total']) - Decimal(tax))).quantize(TWO_DECIMAL_PLACES)

            # discount totl
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
            else:
                unit_of_measure = partdata[counter]['unitOfMeasure']

            goodsDetailsBody = ('{'
            '"item": "'+ item +'",'
            '"itemCode": "'+ partdata[counter]['itemCode'] +'",'
            '"qty": "'+ str(int(Decimal(partdata[counter]['qty']))) +'",'
            '"unitOfMeasure": "'+ unit_of_measure +'",'
            '"unitPrice": "'+ str(Decimal(partdata[counter]['unitPrice']).quantize(TWO_DECIMAL_PLACES)) +'",'
            '"total": "'+ str(Decimal(partdata[counter]['total']).quantize(TWO_DECIMAL_PLACES)) +'",'
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
            '"goodsCategoryId": "'+ partdata[counter]['goodsCategoryId'] +'",'
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
                '"taxCategory": "'+ partdata[counter]['vatProdPostingGroup'] +'",'
                '"netAmount": "'+ str((Decimal(partdata[counter]['total']) - Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"taxRate": "'+ tax_rate +'",'
                '"taxAmount": "'+ tax +'",'
                '"grossAmount": "'+ str(Decimal(tax) + (Decimal(partdata[counter]['total']) - Decimal(tax)).quantize(TWO_DECIMAL_PLACES)) +'",'
                '"exciseUnit": "",'
                '"exciseCurrency": "",'
                '"taxRateName": "123"'
            '}')

            if counter != number_of_lines - 1:
                taxDetailsBody = taxDetailsBody + ','

            taxDetailsHeader = taxDetailsHeader + taxDetailsBody
            counter = counter + 1

        goodsDetailsHeader = goodsDetailsHeader + goodsDetailsFooter
        taxDetailsHeader = taxDetailsHeader + taxDetailsFooter

    else:
        print('error')

    buyer_infor_response = requests.get('http://localhost:8280/services/sybyl-efris/getCustomerInformation?customerNo='+customerNumber, headers={'Accept': 'application/json'})
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
                '"buyerType": "1",'
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

    print('--------------------------------------------------------------------')
    print(upload_invoice_message)
    print('--------------------------------------------------------------------')

    # encode message to base64 bytes
    message_bytes = upload_invoice_message.encode('ascii')
    # decode base64 bytes to string
    base64_message = base64.b64encode(message_bytes).decode('ascii')

    d = ('{'
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
            '"interfaceCode": "T109",'
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
    print('--------------------------------------------------------------------')
    print(d)
    print('--------------------------------------------------------------------')

    y = json.loads(d)

    finalupload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=y)

    if finalupload.status_code == 200:
        finaluploaddata = finalupload.json()
        return_message = finaluploaddata['returnStateInfo']['returnMessage']
        return_data = finaluploaddata['data']

        message = return_message

        if return_message == 'SUCCESS':
            content_base64 = finaluploaddata['data']['content']
            content_decoded = base64.b64decode(content_base64).decode('ascii')

        #     # convert to json
            content_json = json.loads(content_decoded)

        #     # get the invoice number
            invoice_number = content_json['basicInformation']['invoiceNo']
            qrcode = content_json['summary']['qrCode']
            print('invoice number = ', invoice_number)

            #update external document number
            uri = 'http://localhost:8000/dashboard/update_external_document_number?ura_invoice_num='+ invoice_number +'=&qrcode'+qrcode+'+&doc_num='+documentNumber
            upex = requests.get(uri)

            if upex.status_code == 200:
                message = 'E-invoice ('+invoice_number+') successfully generated + Ura orginal invoice number ('+ invoice_number +') and Qrcode ('+ qrcode +') updated in navision database'
            else:
                message = 'E-invoice ('+invoice_number+')  successfully generated + failed to update Ura orginal invoice number ('+ invoice_number +') and Qrcode ('+ qrcode +') updated in navision database'

        data = {
                    'data': return_data,
                    'externalDocNumber': 'hello',
                    'docNumber': ''+documentNumber,
                    'returnStateInfo': {
                        'returnCode': '00',
                        'returnMessage': ''+message
                    }
                    
                }
        return JsonResponse(data, status=200)
        
    else: 
        data = {
            'errorcode':''+str(finalupload.status_code)
        }
        return JsonResponse(data, status=400)

