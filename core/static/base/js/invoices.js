$(document).ready(function(){
    var orderTableBody = $("#order-table-body");
    var uploadInvoiceBtn = $("#upload-invoices");

    function loadCompInfo() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_company_info",
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
                console.log(result);
                console.log(result.Company.Details[0].Address)
            },
            error: function(xhr, textStatus, errorMessage) {
                console.log(xhr)
                console.log("error, "+ errorMessage);
            },
          });
    }

    function loadInvoices() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_invoices",
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
                console.log(result);
                console.log(result.Orders.Order.length)

                for(a = 0; a < result.Orders.Order.length; a++){
                    let statusValue;
                    
                    if(result.Orders.Order[a].status == "0"){
                        statusValue = "Not Uploaded"
                    }
                    else {
                        statusValue = result.Orders.Order[a].status;
                    }

                    let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-invoice" value="'+result.Orders.Order[a].orderNumber+'"/></td>');
                    let rowCount = $('<td>'+ (a + 1) +'</td>');
                    let orderNumber = $('<td>'+result.Orders.Order[a].orderNumber+'</td>');
                    let documentDate = $('<td>'+result.Orders.Order[a].documentDate+'</td>');
                    let salesPersonCode = $('<td>'+result.Orders.Order[a].salesPersonCode+'</td>');
                    let documentType = $('<td>'+result.Orders.Order[a].documentType+'</td>');
                    let status = $('<td>'+statusValue+'</td>');
                    //let documentdate = '<td>'+result.Orders.Order[a].documentDate+'</td>';
                    //let documentdate = '<td>'+result.Orders.Order[a].documentDate+'</td>';
                    //let documentdate = '<td>'+result.Orders.Order[a].documentDate+'</td>';

                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(orderNumber);
                    tablerow.append(documentDate);
                    tablerow.append(salesPersonCode);
                    tablerow.append(documentType);
                    tablerow.append(status);

                    orderTableBody.append(tablerow)
                }
            },
            error: function(xhr, textStatus, errorMessage) {
                console.log(xhr)
                console.log("error, "+ errorMessage);
            },
          });
    }

    loadCompInfo();
    loadInvoices();

    uploadInvoiceBtn.click(function(){
        var checkedinvoice = $('.check-invoice');
        if(checkedinvoice.not(':checked').length == checkedinvoice.length) {
            console.log("nothing is checked");
            btn.attr("disabled", true);
        } 
        else {
            var s = $(".check-invoice:checked")
            $.ajax({
                method: "POST",
                url: "http://localhost:9880/efristcs/ws/tcsapp/getInformation",
                data: {
                    "data": {
                        "content": "ewoJInNlbGxlckRldGFpbHMiOiB7CgkJInRpbiI6ICIyMDE5MDUwODE3MDUiLAoJCSJuaW5Ccm4iOiAiMjAxOTA1MDgxNzA1IiwKCQkibGVnYWxOYW1lIjogInpoYW5nc2FuIiwKCQkiYnVzaW5lc3NOYW1lIjogImxpc2kiLAoJCSJhZGRyZXNzIjogImJlaWppbiIsCgkJIm1vYmlsZVBob25lIjogIjE1NTAxMjM0NTY3IiwKCQkibGluZVBob25lIjogIjAxMC02Njg5NjY2IiwKCQkiZW1haWxBZGRyZXNzIjogIjEyMzQ1NkAxNjMuY29tIiwKCQkicGxhY2VPZkJ1c2luZXNzIjogImJlaWppbiIsCgkJInJlZmVyZW5jZU5vIjogIjAwMDAwMDAwMDEyIiwKCQkiYnJhbmNoSWQiOiAiMjA3MzAwOTA4ODEzNjUwMzEyIgoJfSwKCSJiYXNpY0luZm9ybWF0aW9uIjogewoJCSJpbnZvaWNlTm8iOiAiMDAwMDAwMDAwMDEiLAoJCSJhbnRpZmFrZUNvZGUiOiAiMjAxOTA1MDgxNzExIiwKCQkiZGV2aWNlTm8iOiAiMjAxOTA1MDgxMjM0IiwKCQkiaXNzdWVkRGF0ZSI6ICIyMDE5LTA1LTA4IDE3OjEzOjEyIiwKCQkib3BlcmF0b3IiOiAiYWlzaW5vIiwKCQkiY3VycmVuY3kiOiAiVUdYIiwKCQkib3JpSW52b2ljZUlkIjogIjEiLAoJCSJpbnZvaWNlVHlwZSI6ICIxIiwKCQkiaW52b2ljZUtpbmQiOiAiMSIsCgkJImRhdGFTb3VyY2UiOiAiMTAxIiwKCQkiaW52b2ljZUluZHVzdHJ5Q29kZSI6ICIxMDIiLAoJCSJpc0JhdGNoIjogIjAiCgl9LAoJImJ1eWVyRGV0YWlscyI6IHsKCQkiYnV5ZXJUaW4iOiAiMjAxOTA1MDgxNzA1IiwKCQkiYnV5ZXJOaW5Ccm4iOiAiMjAxOTA1MDgxNzA1IiwKCQkiYnV5ZXJQYXNzcG9ydE51bSI6ICIyMDE5MDUwODE3MDUiLAoJCSJidXllckxlZ2FsTmFtZSI6ICJ6aGFuZ3NhbiIsCgkJImJ1eWVyQnVzaW5lc3NOYW1lIjogImxpc2kiLAoJCSJidXllckFkZHJlc3MiOiAiYmVpamluIiwKCQkiYnV5ZXJFbWFpbCI6ICIxMjM0NTZAMTYzLmNvbSIsCgkJImJ1eWVyTW9iaWxlUGhvbmUiOiAiMTU1MDEyMzQ1NjciLAoJCSJidXllckxpbmVQaG9uZSI6ICIwMTAtNjY4OTY2NiIsCgkJImJ1eWVyUGxhY2VPZkJ1c2kiOiAiYmVpamluIiwKCQkiYnV5ZXJUeXBlIjogIjEiLAoJCSJidXllckNpdGl6ZW5zaGlwIjogIjEiLAoJCSJidXllclNlY3RvciI6ICIxIiwKCQkiYnV5ZXJSZWZlcmVuY2VObyI6ICIwMDAwMDAwMDAwMSIKCX0sCgkiYnV5ZXJFeHRlbmQiOiB7CgkJInByb3BlcnR5VHlwZSI6ICJhYmMiLAoJCSJkaXN0cmljdCI6ICJoYWlkaWFuIiwKCQkibXVuaWNpcGFsaXR5Q291bnR5IjogImhhaWRpYW4iLAoJCSJkaXZpc2lvblN1YmNvdW50eSI6ICJoYWlkaWFuMSIsCgkJInRvd24iOiAiaGFpZGlhbjEiLAoJCSJjZWxsVmlsbGFnZSI6ICJoYWlkaWFuMSIsCgkJImVmZmVjdGl2ZVJlZ2lzdHJhdGlvbkRhdGUiOiAiMjAyMC0xMC0xOSIsCgkJIm1ldGVyU3RhdHVzIjogIjEwMSIKCX0sCgkiZ29vZHNEZXRhaWxzIjogW3sKCQkiaXRlbSI6ICJhcHBsZSIsCgkJIml0ZW1Db2RlIjogIjEwMSIsCgkJInF0eSI6ICIyIiwKCQkidW5pdE9mTWVhc3VyZSI6ICJrZyIsCgkJInVuaXRQcmljZSI6ICIxNTAuMDAiLAoJCSJ0b3RhbCI6ICIxIiwKCQkidGF4UmF0ZSI6ICIwLjE4IiwKCQkidGF4IjogIjEyLjg4IiwKCQkiZGlzY291bnRUb3RhbCI6ICIxOC4wMCIsCgkJImRpc2NvdW50VGF4UmF0ZSI6ICIwLjE4IiwKCQkib3JkZXJOdW1iZXIiOiAiMSIsCgkJImRpc2NvdW50RmxhZyI6ICIxIiwKCQkiZGVlbWVkRmxhZyI6ICIxIiwKCQkiZXhjaXNlRmxhZyI6ICIyIiwKCQkiY2F0ZWdvcnlJZCI6ICIxMjM0IiwKCQkiY2F0ZWdvcnlOYW1lIjogIlRlc3QiLAoJCSJnb29kc0NhdGVnb3J5SWQiOiAiNTQ2NyIsCgkJImdvb2RzQ2F0ZWdvcnlOYW1lIjogIlRlc3QiLAoJCSJleGNpc2VSYXRlIjogIjAuMTIiLAoJCSJleGNpc2VSdWxlIjogIjEiLAoJCSJleGNpc2VUYXgiOiAiMjAuMjIiLAoJCSJwYWNrIjogIjEiLAoJCSJzdGljayI6ICIyMCIsCgkJImV4Y2lzZVVuaXQiOiAiMTAxIiwKCQkiZXhjaXNlQ3VycmVuY3kiOiAiVUdYIiwKCQkiZXhjaXNlUmF0ZU5hbWUiOiAiMTIzIgoJfV0sCgkidGF4RGV0YWlscyI6IFt7CgkJInRheENhdGVnb3J5IjogIidTdGFuZGFyZCIsCgkJIm5ldEFtb3VudCI6ICIzODEzLjU1IiwKCQkidGF4UmF0ZSI6ICIwLjE4IiwKCQkidGF4QW1vdW50IjogIjY4Ni40NSIsCgkJImdyb3NzQW1vdW50IjogIjQ1MDAuMDAiLAoJCSJleGNpc2VVbml0IjogIjEwMSIsCgkJImV4Y2lzZUN1cnJlbmN5IjogIlVHWCIsCgkJInRheFJhdGVOYW1lIjogIjEyMyIKCX1dLAoJInN1bW1hcnkiOiB7CgkJIm5ldEFtb3VudCI6ICI4Mzc5IiwKCQkidGF4QW1vdW50IjogIjg2OCIsCgkJImdyb3NzQW1vdW50IjogIjkyNDciLAoJCSJpdGVtQ291bnQiOiAiNSIsCgkJIm1vZGVDb2RlIjogIjAiLAoJCSJyZW1hcmtzIjogIlRoaXMgaXMgYW5vdGhlciByZW1hcmsgdGVzdC4iLAoJCSJxckNvZGUiOiAiYXNkZmdoamtsIgoJfSwKCSJwYXlXYXkiOiBbewoJCSJwYXltZW50TW9kZSI6ICIxMDEiLAoJCSJwYXltZW50QW1vdW50IjogIjY4Ni40NSIsCgkJIm9yZGVyTnVtYmVyIjogImEiCgl9XSwKCSJleHRlbmQiOiB7CgkJInJlYXNvbiI6ICJyZWFzb24iLAoJCSJyZWFzb25Db2RlIjogIjEwMiIKCgl9LAoJImltcG9ydFNlcnZpY2VzU2VsbGVyIjogewoJCSJpbXBvcnRCdXNpbmVzc05hbWUiOiAibGlzaSIsCgkJImltcG9ydEVtYWlsQWRkcmVzcyI6ICIxMjM0NTZAMTYzLmNvbSIsCgkJImltcG9ydENvbnRhY3ROdW1iZXIiOiAiMTU1MDEyMzQ1NjciLAoJCSJpbXBvcnRBZGRyZXMiOiAiYmVpamluIiwKCQkiaW1wb3J0SW52b2ljZURhdGUiOiAiMjAyMC0wOS0wNSIsCgkJImltcG9ydEF0dGFjaG1lbnROYW1lIjogInRlc3QiLAoJCSJpbXBvcnRBdHRhY2htZW50Q29udGVudCI6ICJNSUlERmpDQ0FmNmdBd0lCQWdJUkFLUEdBb2w5Q0VkcGtJb0ZhOGh1TTZ6ZmoxV0VCUnh0ZW9vNlBINDZ1bjRGR2o0TjZpb0lHelZyOUc0MHVoUUdkbTE2WlUrcTQ0WGpXMm9Vbkk5dz0iCgl9Cn0=",
                        "signature": "",
                        "dataDescription": {
                            "codeType": "0",
                            "encryptCode": "1",
                            "zipCode": "0"
                        }
                    },
                    "globalInfo": {
                        "appId": "",
                        "version": "1.1.20191201",
                        "dataExchangeId": "9230489223014123",
                        "interfaceCode": "T108",
                        "requestCode": "TP",
                        "requestTime": "2020-12-16 12:54:07",
                        "responseCode": "TA",
                        "userName": "1000024517",
                        "deviceMAC": "005056B65332",
                        "deviceNo": "TCSff5ba51958634436",
                        "tin": "1000024517",
                "brn": "",
                        "taxpayerID": "1000024517",
                        "longitude": "116.397128",
                        "latitude": "39.916527",
                        "extendField": {
                            "responseDateFormat": "dd/MM/yyyy",
                            "responseTimeFormat": "dd/MM/yyyy HH:mm:ss"
                        }
                    },
                    "returnStateInfo": {
                        "returnCode": "",
                        "returnMessage": ""
                    }
                },
                beforeSend: function(request) {
                    console.log("before send");
                },
                success: function(result, status, xhr) {
                    console.log("success");
                    console.log(result);
                },
                error: function(xhr, textStatus, errorMessage) {
                    console.log(xhr)
                },
              });
            // console.log(s.length);
            // console.log(s[0].value);
            // for(a = 0; a < s.length; a++){
            //     var orderNumber = s[a].value;

            // }
        }
    });
});