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

                for(counter = 0; counter < result.invoiceHeaders.header.length; counter++){

                    let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-invoice" value="'+result.invoiceHeaders.header[counter].antifakeCode+'"/></td>');
                    let rowCount = $('<td>'+ (counter + 1) +'</td>');
                    let antifakeCode = $('<td>'+result.invoiceHeaders.header[counter].antifakeCode+'</td>');
                    let documentDate = $('<td>'+result.invoiceHeaders.header[counter].documentDate+'</td>');
                    let operator = $('<td>'+result.invoiceHeaders.header[counter].operator+'</td>');
                    let invoiceType = $('<td>'+result.invoiceHeaders.header[counter].invoiceType+'</td>');
                    let customerName = $('<td>'+result.invoiceHeaders.header[counter].customerName+'</td>');
                    let externalDocumentNumber = '<td>'+result.invoiceHeaders.header[counter].invoiceNo+'</td>';
                    let oriInvoiceId = '<td>'+result.invoiceHeaders.header[counter].oriInvoiceId+'</td>';
                    //let documentdate = '<td>'+result.invoiceHeaders.header[a].documentDate+'</td>';

                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(antifakeCode);
                    tablerow.append(documentDate);
                    tablerow.append(operator);
                    tablerow.append(invoiceType);
                    tablerow.append(customerName);
                    tablerow.append(externalDocumentNumber);
                    tablerow.append(oriInvoiceId);

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