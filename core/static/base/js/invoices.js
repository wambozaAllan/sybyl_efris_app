$(document).ready(function(){
    var orderTableBody = $("#order-table-body");
    var uploadInvoiceBtn = $("#upload-invoices");

    function loadInvoices() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_invoices",
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
                $('#docs-loader').hide();

                for(a = 0; a < result.Documents.Document.length; a++){
                    let statusValue;
                    
                    if(result.Documents.Document[a].status == "0"){
                        statusValue = "Not Uploaded"
                    }
                    else {
                        statusValue = result.Documents.Document[a].status;
                    }

                    let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-invoice" value="'+result.Documents.Document[a].orderNumber+'"/></td>');
                    let rowCount = $('<td>'+ (a + 1) +'</td>');
                    let orderNumber = $('<td>'+result.Documents.Document[a].orderNumber+'</td>');
                    let documentDate = $('<td>'+result.Documents.Document[a].documentDate+'</td>');
                    let salesPersonCode = $('<td>'+result.Documents.Document[a].salesPersonCode+'</td>');
                    let documentType = $('<td>'+result.Documents.Document[a].documentType+'</td>');
                    let customerName = $('<td>'+result.Documents.Document[a].customerName+'</td>');
                    let externalDocumentNumber = '<td>'+result.Documents.Document[a].externalDocumentNumber+'</td>';
                    let uraRefNumber = '<td>'+result.Documents.Document[a].uraRefNumber+'</td>';
                    //let documentdate = '<td>'+result.Documents.Document[a].documentDate+'</td>';

                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(orderNumber);
                    tablerow.append(documentDate);
                    tablerow.append(salesPersonCode);
                    tablerow.append(documentType);
                    tablerow.append(customerName);
                    tablerow.append(externalDocumentNumber);
                    tablerow.append(uraRefNumber);

                    orderTableBody.append(tablerow)
                }
            },
            error: function(xhr, textStatus, errorMessage) {
                swal({
                            title: 'Error Occurred',
                            text: ''+errorMessage,
                            icon: 'erro',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
            },
          });
    }

    loadInvoices();

    uploadInvoiceBtn.click(function(){
        
        var checkedinvoice = $('.check-invoice');
        if(checkedinvoice.not(':checked').length == checkedinvoice.length) {
            console.log("nothing is checked");
            swal({
                text: 'Select document',
                button: {
                  text: "OK",
                  value: true,
                  visible: true,
                  className: "btn btn-primary"
                }
            })

        } 
        else {
            uploadInvoiceBtn.prop('disabled', true);

            var s = $(".check-invoice:checked")
            var documentNumber = s[0].value;

            $.ajax({
                url: "http://localhost:8000/dashboard/upload_document?documentNumber="+documentNumber,
                beforeSend: function(request) {
                    $('#e-loader').show();
                    console.log("before send");
                },
                success: function(result, status, xhr) {
                    $('#e-loader').hide()
                    uploadInvoiceBtn.prop('disabled', false);
                    console.log("success");
                    console.log(result);
                    if(result.returnStateInfo.returnMessage != "00") {
                        swal({
                            title: 'Error Occurred',
                            text: ''+result.returnStateInfo.returnMessage,
                            icon: 'success',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
                    }
                    else {

                       swal({
                            title: 'E-Invoice Successfully Generated',
                            text: 'External document number =',
                            icon: 'error',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
                    }
                    
                },
                error: function(xhr, textStatus, errorMessage) {
                    $('#e-loader').hide();
                    uploadInvoiceBtn.prop('disabled', false);
                    swal({
                            title: 'Error Occurred',
                            text: ''+errorMessage,
                            icon: 'error',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
                },
              });
        }
    });
});