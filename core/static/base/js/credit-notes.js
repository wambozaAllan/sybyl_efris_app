$(document).ready(function(){
    var orderTableBody = $("#credit-notes-table");
    var uploadCreditNotes = $("#upload-credit-notes");

    function loadCreditNotes() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_credit_notes",
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
                $('#docs-loader').hide();

                for(counter = 0; counter < result.creditNoteHeaders.header.length; counter++){

                    let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-credit-note" value="'+result.creditNoteHeaders.header[counter].creditNoteNo+'"/></td>');
                    let rowCount = $('<td>'+ (counter + 1) +'</td>');
                    let creditNoteNo = $('<td>'+result.creditNoteHeaders.header[counter].creditNoteNo+'</td>');
                    let documentDate = $('<td>'+result.creditNoteHeaders.header[counter].applicationTime+'</td>');
                    let operator = $('<td>'+result.creditNoteHeaders.header[counter].operator+'</td>');
                    let customerName = $('<td>'+result.creditNoteHeaders.header[counter].customerName+'</td>');
                    let externalDocumentNumber = '<td>'+result.creditNoteHeaders.header[counter].externalDocumentNo+'</td>';
                    let uraReferenceNo = '<td>'+result.creditNoteHeaders.header[counter].uraReferenceNo+'</td>';

                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(creditNoteNo);
                    tablerow.append(documentDate);
                    tablerow.append(operator);
                    tablerow.append(customerName);
                    tablerow.append(externalDocumentNumber);
                    tablerow.append(uraReferenceNo);

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