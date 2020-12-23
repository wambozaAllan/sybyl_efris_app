$(document).ready(function(){
    var orderTableBody = $("#credit-notes-table");
    var uploadInvoiceBtn = $("#upload-invoices");

    function loadCreditNotes() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_credit_notes",
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
                $('#docs-loader').hide();

                for(a = 0; a < result.Documents.Document.length; a++){

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

    loadCreditNotes();
});