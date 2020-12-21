from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import requests
from datetime import datetime
import base64
import dateutil.parser
import json

def items(request):
    context = {
        'page': 'Items',
    }
    return render(request, 'dashboard/items.html', context)

def invoices(request):
    context = {
        'page': 'Documents',
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
    url = 'http://localhost:8280/services/GetDocuments/getorders'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)


def load_company_info(request):
    url = 'http://localhost:8280/services/GetCompanyInformation/getcompanyinfor'
    response = requests.get(url, headers={'Accept':'application/json'})
    data = {}
    if response.status_code == 200:
        print(response.headers.get('Content-Type'))
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def update_external_document_number(request):
    external_doc_num_update = request.GET['external_doc_num_update']
    doc_num = request.GET['doc_num']

    url = 'http://localhost:8280/services/UpdateExternalDocumentNumber/updateExternalDocumentNumber'
    request_headers = {'Content-Type':'application/xml', 'Accept': 'application/json'}
    req_message = (
        '<_putupdateexternaldocumentnumber>'
            '<ExternalDocumentNumber>'+ external_doc_num_update +'</ExternalDocumentNumber>'
            '<DocumentNumber>'+ doc_num +'</DocumentNumber>'
        '</_putupdateexternaldocumentnumber>')

    response = requests.put(url, data=req_message, headers=request_headers)

    data = {}
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, status=200)
    
    else: 
        return JsonResponse(data, status=400)

def upload_document(request):
    ddd = request.GET['documentNumber']
    data = {}
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")

    company_infor_response = requests.get('http://localhost:8280/services/GetCompanyInformation/getcompanyinfor', headers={'Accept':'application/json'})

    if company_infor_response.status_code == 200:
        company_data = company_infor_response.json()

        seller_details = ('"sellerDetails": {'
        '"tin":"' + company_data['Company']['Details'][0]['VatRegistrationNumber'] + '",'
        '"ninBrn":"' + company_data['Company']['Details'][0]['MinBRN'] + '",'
        '"legalName":"' + company_data['Company']['Details'][0]['LegalName'] + '",'
        '"businessName":"' + company_data['Company']['Details'][0]['BusinessName'] + '",'
        '"address":"' + company_data['Company']['Details'][0]['Address'] + '",'
        '"mobilePhone":"' + company_data['Company']['Details'][0]['MobileNumber'] + '",'
        '"linePhone":"' + company_data['Company']['Details'][0]['PhoneNumber'] + '",'
        '"emailAddress":"' + company_data['Company']['Details'][0]['Email'] + '",'
        '"placeOfBusiness":"' + company_data['Company']['Details'][0]['PlaceOfBusiness'] + '",'
        '"referenceNo":"' + company_data['Company']['Details'][0]['ReferenceNumber'] + '",'
        '"branchId":"' + company_data['Company']['Details'][0]['BranchId'] + '"'
        '}')

    else:
        print('error')

    document_header_response = requests.get('http://localhost:8280/services/GetDocuments/getSpecificDocument?OrderNumber='+ddd, headers={'Accept':'application/json'})

    if document_header_response.status_code == 200:
        document_header_data = document_header_response.json()
        partdata = document_header_data['Documents']['Document'][0]

        document_date = dateutil.parser.parse(partdata['documentDate']) 
        currency = "UGX" if not partdata['currencyCode'] else document_header_data['Documents']['Document'][0]['documentDate']
        issue_date = document_date.strftime('%Y-%m-%d %H:%M:%S')
        basic_information = ('"basicInformation": {'
        '"invoiceNo": "'+ partdata['externalDocumentNumber'] +'",'
        '"antifakeCode": "",'
        '"deviceNo": "TCSff5ba51958634436",'
        '"issuedDate": "'+ issue_date +'",'
        '"operator": "'+ partdata['salesPersonCode'] +'",'
        '"currency": "'+ currency +'",'
        '"oriInvoiceId": "'+ partdata['externalDocumentNumber'] +'",'
        '"invoiceType": "1",'
        '"invoiceKind": "1",'
        '"dataSource": "101",'
        '"invoiceIndustryCode": "",'
        '"isBatch": "0"'
        '}')

        print('basic information', basic_information)
    else: 
        print('error')

    document_lines_response = requests.get('http://localhost:8280/services/GetOrderLines/getDocumentLines?DocumentNumber='+ddd, headers={'Accept':'application/json'})

    if document_lines_response.status_code == 200:
        document_lines_data = document_lines_response.json()
        counter = 0
        partdata =  document_lines_data['DocumentLines']['goodsDetails']
        number_of_lines = len(partdata)
        
        goodsDetailsHeader = '"goodsDetails": ['
        goodsDetailsFooter = ']'

        taxDetailsHeader = '"taxDetails": ['
        taxDetailsFooter = ']'
    
        while counter < number_of_lines:
            tax = str(float(partdata[counter]['AmountIncludingVat']) - float(partdata[counter]['Amount']))
            total = str(float(partdata[counter]['Amount']) * float(partdata[counter]['Quantity']))
            customerNumber = partdata[counter]['CustomerNumber']

            goodsDetailsBody = ('{'
            '"item": "'+ partdata[counter]['Description'] +'",'
            '"itemCode": "'+ partdata[counter]['Number'] +'",'
            '"qty": "'+ str(float(partdata[counter]['Quantity'])) +'",'
            '"unitOfMeasure": "'+ partdata[counter]['UnitOfMeasure'] +'",'
            '"unitPrice": "'+ partdata[counter]['UnitPrice'] +'",'
            '"total": "'+ partdata[counter]['Amount'] +'",'
            '"taxRate": "'+ partdata[counter]['VatPercentage'] +'",'
            '"tax": "'+ tax +'",'
            '"discountTotal": "'+ partdata[counter]['LineDiscountAmount'] +'",'
            '"discountTaxRate": "'+ partdata[counter]['LineDiscountPercentage'] +'",'
            '"orderNumber": "'+ partdata[counter]['DocumentNumber'] +'",'
            '"discountFlag": "2",'
            '"deemedFlag": "2",'
            '"exciseFlag": "'+ partdata[counter]['ExciseFlag'] +'",'
            '"categoryId": "",'
            '"categoryName": "",'
            '"goodsCategoryId": "'+ partdata[counter]['GoodsCategoryId'] +'",'
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
                '"taxCategory": "'+ partdata[counter]['VatProdPostingGroup'] +'",'
                '"netAmount": "'+ partdata[counter]['Amount'] +'",'
                '"taxRate": "'+ partdata[counter]['VatPercentage'] +'",'
                '"taxAmount": "'+ tax +'",'
                '"grossAmount": "'+ str(float(partdata[counter]['AmountIncludingVat'])) +'",'
                '"exciseUnit": "",'
                '"exciseCurrency": "",'
                '"taxRateName": ""'
            '}')

            if counter != number_of_lines - 1:
                taxDetailsBody = taxDetailsBody + ','

            taxDetailsHeader = taxDetailsHeader + taxDetailsBody
            counter = counter + 1

        goodsDetailsHeader = goodsDetailsHeader + goodsDetailsFooter
        taxDetailsHeader = taxDetailsHeader + taxDetailsFooter

        print('goods details', goodsDetailsHeader)
        print('tax details', taxDetailsHeader)

    else:
        print('error')

    buyer_infor_response = requests.get('http://localhost:8280/services/GetCustomerInformation/getCustomerInformation?CustomerNumber='+customerNumber, headers={'Accept': 'application/json'})
    if buyer_infor_response.status_code == 200:
        buyer_infor_data = buyer_infor_response.json()
        if(bool(buyer_infor_data['Customer'])):
            partdata = buyer_infor_data['Customer']['Details'][0]
            buyer_details = ('"buyerDetails": {'
                '"buyerTin": "'+ partdata['VatRegistrationNumber'] +'",'
                '"buyerNinBrn": "'+ partdata['MinBrn'] +'",'
                '"buyerPassportNum": "'+ partdata['PassportNumber'] +'",'
                '"buyerLegalName": "'+ partdata['Name'] +'",'
                '"buyerBusinessName": "'+ partdata['Name'] +'",'
                '"buyerAddress": "'+ partdata['Address'] +'",'
                '"buyerEmail": "'+ partdata['Email'] +'",'
                '"buyerMobilePhone": "'+ partdata['MobileNumber'] +'",'
                '"buyerLinePhone": "'+ partdata['PhoneNumber'] +'",'
                '"buyerPlaceOfBusi": "'+ partdata['PlaceOfBusiness'] +'",'
                '"buyerType": "1",'
                '"buyerCitizenship": "'+ partdata['BuyerCitizenship'] +'",'
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
    '"netAmount": "8379",'
    '"taxAmount": "868",'
    '"grossAmount": "9247",'
    '"itemCount": "5",'
    '"modeCode": "0",'
    '"remarks": "",'
    '"qrCode": ""'
    '},'
    '"payWay": [{'
    '"paymentMode": "",'
    '"paymentAmount": "",'
    '"orderNumber": ""'
    '}],'
    '"extend": {'
    '"reason": "",'
    '"reasonCode": ""},'
    '"importServicesSeller": {}'
    '}')

    message_bytes = upload_invoice_message.encode('ascii')
    base64_message = base64.b64encode(message_bytes).decode('ascii')

    testbase64message = ('ewoJInNlbGxlckRldGFpbHMiOiB7CgkidGluIjogIjEwMDAwMjQ1MTciLAoJIm5pbkJybiI6ICIvUjEwMDAwMDAxOTMzNzMiLAoJImxlZ2FsTmFtZSI6ICJTWUJZTCBMSU1JVEVEIiwKCSJidXNpbmVzc05hbWUiOiAibGlzaSIsCgkiYWRkcmVzcyI6ICJQbG90IDFBIEthZnUgUm9hZCIsCgkibW9iaWxlUGhvbmUiOiAiMDc3Mjc2NTc2NSIsCgkibGluZVBob25lIjogIisyNTYgNDEgNDMwNTQwMCIsCgkiZW1haWxBZGRyZXNzIjogImFsYmVydEBzeWJ5bC5jb20iLAoJInBsYWNlT2ZCdXNpbmVzcyI6ICJQbG90IDFBIEthZnUgUm9hZCIsCgkicmVmZXJlbmNlTm8iOiAiIiwKCSJicmFuY2hJZCI6ICIiCgl9LAoJImJhc2ljSW5mb3JtYXRpb24iOiB7CgkiaW52b2ljZU5vIjogIiIsCgkiYW50aWZha2VDb2RlIjogIiIsCgkiZGV2aWNlTm8iOiAiVENTZmY1YmE1MTk1ODYzNDQzNiIsCgkiaXNzdWVkRGF0ZSI6ICIyMDIwLTEyLTIwIDE3OjEzOjEyIiwKCSJvcGVyYXRvciI6ICJBbGxhbiIsCgkiY3VycmVuY3kiOiAiVUdYIiwKCSJvcmlJbnZvaWNlSWQiOiAiIiwKCSJpbnZvaWNlVHlwZSI6ICIxIiwJCgkiaW52b2ljZUtpbmQiOiAiMSIsCgkiZGF0YVNvdXJjZSI6ICIxMDEiLAoJImludm9pY2VJbmR1c3RyeUNvZGUiOiAiMTAyIiwKCSJpc0JhdGNoIjogIjAiCgl9LAoJImJ1eWVyRGV0YWlscyI6IHsKCSJidXllclRpbiI6ICIxMDAwMjcyNDc4IiwKCSJidXllck5pbkJybiI6ICIiLAoJImJ1eWVyUGFzc3BvcnROdW0iOiAiIiwKCSJidXllckxlZ2FsTmFtZSI6ICJBbWVyaWNhbiBFbWJhc3N5IEthbXBhbGEiLAoJImJ1eWVyQnVzaW5lc3NOYW1lIjogIkFtZXJpY2FuIEVtYmFzc3kgS2FtcGFsYSIsCgkiYnV5ZXJBZGRyZXNzIjogIkdTTyA2My82NyBTcHJpbmcgUm9hZCBCdWdvbG9iaSIsCgkiYnV5ZXJFbWFpbCI6ICIxMjM0NTZAMTYzLmNvbSIsCgkiYnV5ZXJNb2JpbGVQaG9uZSI6ICIxNTUwMTIzNDU2NyIsCgkiYnV5ZXJMaW5lUGhvbmUiOiAiMDQxNCAzNDUgMTIzIiwKCSJidXllclBsYWNlT2ZCdXNpIjogImJlaWppbiIsCgkiYnV5ZXJUeXBlIjogIjEiLAoJImJ1eWVyQ2l0aXplbnNoaXAiOiAiMSIsCgkiYnV5ZXJTZWN0b3IiOiAiMSIsCgkiYnV5ZXJSZWZlcmVuY2VObyI6ICIwMDAwMDAwMDAwMSIKCX0sCgkiYnV5ZXJFeHRlbmQiOiB7CgkicHJvcGVydHlUeXBlIjogIiIsCgkiZGlzdHJpY3QiOiAiIiwKCSJtdW5pY2lwYWxpdHlDb3VudHkiOiAiIiwKCSJkaXZpc2lvblN1YmNvdW50eSI6ICIiLAoJInRvd24iOiAiIiwKCSJjZWxsVmlsbGFnZSI6ICIiLAoJImVmZmVjdGl2ZVJlZ2lzdHJhdGlvbkRhdGUiOiAiIiwKCSJtZXRlclN0YXR1cyI6ICIiCgl9LAoJImdvb2RzRGV0YWlscyI6IFt7CgkiaXRlbSI6ICJTdXBlciBTZXJ2ZXJzIiwKCSJpdGVtQ29kZSI6ICIzMzIyREQiLAoJInF0eSI6ICIxIiwKCSJ1bml0T2ZNZWFzdXJlIjogIkJveCIsCgkidW5pdFByaWNlIjogIjEwMDAwMDAuMDAiLAoJInRvdGFsIjogIjEwMDAwMDAuMDAiLAoJInRheFJhdGUiOiAiMC4xOCIsCgkidGF4IjogIjEyLjg4IiwKCSJkaXNjb3VudFRvdGFsIjogIjE4LjAwIiwKCSJkaXNjb3VudFRheFJhdGUiOiAiMC4xOCIsCgkib3JkZXJOdW1iZXIiOiAiMCIsCgkiZGlzY291bnRGbGFnIjogIjEiLAoJImRlZW1lZEZsYWciOiAiMiIsCgkiZXhjaXNlRmxhZyI6ICIyIiwKCSJjYXRlZ29yeUlkIjogIiIsCgkiY2F0ZWdvcnlOYW1lIjogIiIsCgkiZ29vZHNDYXRlZ29yeUlkIjogIjQzMjExNTAxIiwKCSJnb29kc0NhdGVnb3J5TmFtZSI6ICIiLAoJImV4Y2lzZVJhdGUiOiAiIiwKCSJleGNpc2VSdWxlIjogIiIsCgkiZXhjaXNlVGF4IjogIiIsCgkicGFjayI6ICIiLAoJInN0aWNrIjogIiIsCgkiZXhjaXNlVW5pdCI6ICIiLAoJImV4Y2lzZUN1cnJlbmN5IjogIiIsCgkiZXhjaXNlUmF0ZU5hbWUiOiAiIgoJfV0sCiJ0YXhEZXRhaWxzIjogW3sKInRheENhdGVnb3J5IjogIlN0YW5kYXJkIiwKIm5ldEFtb3VudCI6ICI4MjAwMDAiLAoidGF4UmF0ZSI6ICIwLjE4IiwKInRheEFtb3VudCI6ICIxODAwMDAiLAoiZ3Jvc3NBbW91bnQiOiAiMTAwMDAwMCIsCiJleGNpc2VVbml0IjogIiIsCiJleGNpc2VDdXJyZW5jeSI6ICJVR1giLAoidGF4UmF0ZU5hbWUiOiAiMTIzIgp9XSwKInN1bW1hcnkiOiB7CiJuZXRBbW91bnQiOiAiODIwMDAwIiwKInRheEFtb3VudCI6ICIxODAwMDAiLAoiZ3Jvc3NBbW91bnQiOiAiMTAwMDAwMCIsCiJpdGVtQ291bnQiOiAiMSIsCiJtb2RlQ29kZSI6ICIwIiwKInJlbWFya3MiOiAiVGhpcyBpcyBhbm90aGVyIHJlbWFyayB0ZXN0LiIsCiJxckNvZGUiOiAiYXNkZmdoamtsIgp9LAoicGF5V2F5IjogW3sKInBheW1lbnRNb2RlIjogIjEwMSIsCiJwYXltZW50QW1vdW50IjogIjEwMDAwMDAiLAoib3JkZXJOdW1iZXIiOiAiYSIKfV0sCiJleHRlbmQiOiB7CiJyZWFzb24iOiAiIiwKInJlYXNvbkNvZGUiOiAiIgoKfSwKImltcG9ydFNlcnZpY2VzU2VsbGVyIjoge30KfQ==')

    d = ('{'
        '"data": {'
        '"content": "'+testbase64message+'",'
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

    y = json.loads(d)

    finalupload = requests.post('http://192.168.0.232:9880/efristcs/ws/tcsapp/getInformation', json=y)

    if finalupload.status_code == 200:
        print('upload done')
        data = finalupload.json()
        return_message = data['returnStateInfo']['returnMessage']

        # if return_message == 'SUCCESS':
        #     content_base64 = data['data']['content']
        #     content_decoded = base64.b64decode(content).decode('ascii')

        #     # convert to json
        #     content_json = json.loads(content_decoded)

        #     # get the invoice number
        #     invoice_number = content_json['basicInformation']['invoiceNo']
        #     print('invoice number = ', invoice_number)

        #     #update external document number
        #     uri = 'http://localhost:8000/dashboard/update_external_document_number?external_doc_num_update='+ invoice_number +'+&doc_num='+ddd
        #     upex = requests.get('uri')
        #     if upex.status_code == 200:
        #         data = {
        #             'externalDocNumber': ''+invoice_number,
        #             'docNumber': ''+dd,
        #             'message': 'external doc number updated in database'
        #         }
        #         return JsonResponse(data, status=200)
        #     else:
        #         data = {
        #             'externalDocNumber': ''+invoice_number,
        #             'docNumber': ''+dd,
        #             'message': 'failed to update external document number in database'
        #         }
        else:
            return JsonResponse({'error', 'failed to upload invoice'}, status=400)
        
    else: 
        data = {
            'errorcode':''+str(finalupload.status_code)
        }
        return JsonResponse(data, status=400)