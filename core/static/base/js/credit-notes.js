$(document).ready(function(){
    var orderTableBody = $("#credit-notes-table-body");
    var uploadCreditNotesBtn = $("#upload-credit-notes");
    var paginator = $("#paginator");
    var searchCreditNoteBtn = $('#search-credit-notes');
    var searchCreditNoteTextField = $('#credit-note-number');
    let serviceName = $('#service_name').val();

    function loadCreditNotes(page=1) {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_credit_notes?page="+page,
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                var data = result.credit_notes;
                var currentPage = parseInt(result.current_page);
                var numPages = parseInt(result.num_pages);
                var nextPage = result.next_page;
                var previousPage = result.previous_page;
                var row = (currentPage * 10) - 10 + 1;
                var y = currentPage;
                var stop = 0;

                console.log("success");
                $('#docs-loader').hide();

                orderTableBody.empty();
                paginator.empty();

                for(counter = 0; counter < data.length; counter++){
                    let qrcode = data[counter].qrcode;
                    let veriCode = data[counter].verificationCode;
                    let refNo = data[counter].uraReferenceNo;
                    let invoiceNo = data[counter].oriInvoiceNo;
                    let externalDocumentNo = data[counter].externalDocumentNo;

                    let checkBox = null;
                    let action = null;
                    let color = "";

                    let pending = (refNo != '' && invoiceNo != '' && veriCode == '' && qrcode != '' && externalDocumentNo == '');
                    let pending_customer = (refNo != '' && invoiceNo != '' && veriCode == '' && qrcode == '' && externalDocumentNo == '');
                    let uploaded = (refNo != '' && invoiceNo != '' && veriCode != '' && qrcode != '' && externalDocumentNo != '');

                    let tablerow = $('<tr></tr>');

                    if(uploaded){
                      checkBox = $('<td class="text-center"></td>');
                      tablerow.addClass("table-success");
                    }
                    else if(pending_customer){
                      checkBox = $('<td class="text-center"></td>');
                      tablerow.addClass("table-danger");
                    }
                    else if(pending){
                      checkBox = $('<td class="text-center"><input type="checkbox" class="check-credit-note" value="'+data[counter].creditNoteNo+'"/></td>');
                      tablerow.addClass("table-warning");
                    }
                    else{
                      checkBox = $('<td class="text-center"><input type="checkbox" class="check-credit-note" value="'+data[counter].creditNoteNo+'"/></td>');
                      tablerow.addClass("table-info");
                    }

                    let applicationTime = data[counter].applicationTime;
                    let [month, date, year] = new Date(applicationTime).toLocaleDateString("en-US").split("/");
                    let [hour, minute, second] = new Date(applicationTime).toLocaleTimeString("en-US").split(/:| /)
                    let dateTime = date+"-"+month+"-"+year+" "+hour+":"+minute+":"+second

                    let rowCount = $('<td>'+ row +'</td>');
                    let creditNoteNo = $('<td>'+data[counter].creditNoteNo+'</td>');
                    let documentDate = $('<td>'+dateTime+'</td>');
                    let operator = $('<td>'+data[counter].operator+'</td>');
                    let customerName = $('<td>'+data[counter].customerName+'</td>');
                    let oriInvoiceNo = '<td>'+ invoiceNo +'</td>';
                    let uraReferenceNo = '<td>'+ refNo +'</td>';


                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(creditNoteNo);
                    tablerow.append(documentDate);
                    tablerow.append(operator);
                    tablerow.append(customerName);
                    tablerow.append(oriInvoiceNo);
                    tablerow.append(uraReferenceNo);
                    
                    
                    if(uploaded){
                      action = $('<td>Uploaded</td>');
                      tablerow.append(action);
                    }
                    else if(pending_customer) {
                      action = $('<td><button type="button" title="'+data[counter].uraReferenceNo+'" class="btn btn-primary pending-btn" id="pending-client">Pending</button><input type="hidden" id="'+data[counter].uraReferenceNo+'" value="'+data[counter].creditNoteNo+'"/><span id="pending-loader" style="margin-left: 10px; width: 20px; height: 20px; display: none;" class="circle-loader"></span></td>');
                      tablerow.append(action);
                    }
                    else if(pending){
                      action = $('<td>Not Uploaded</td>');
                      tablerow.append(action);
                    }
                    else {
                      action = $('<td>Not Uploaded</td>');
                      tablerow.append(action);
                    }

                    orderTableBody.append(tablerow)

                    row += 1;
                }

                $(document).on('click', '.pending-btn', function(event){
                    var d = $(this);
                    var x = $(this).attr('title');
                    var v = $('#'+x).val();

                    d.prop('disabled', true);
                    $('#pending-loader').show();

                    $.ajax({
                        url: "http://localhost:8000/dashboard/dd?credit_note_id="+x+"&v="+v,
                        beforeSend: function(request) {
                            console.log("before send");
                        },
                        success: function(result, status, xhr) {
                          d.prop('disabled', false);
                          $('#pending-loader').hide();
                          swal({
                            title: '',
                            text: ''+result.returnStateInfo.returnMessage,
                            icon: 'success',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
                        },
                      });
                    event.stopImmediatePropagation();
                });

                if(previousPage) {
                    let x = currentPage - 1;
                    let firstPageBtn = $('<li title="'+ 1 +'" class="page-item"><span class="page-link btn">First</span></li>');
                    let previousPageBtn = $('<li title="'+ x +'" class="page-item"><span class="page-link btn">Previous</span></li>');
                    paginator.append(firstPageBtn);
                    paginator.append(previousPageBtn);
                }
                var pageBtn;
                while(y < numPages){
                    stop++;
                    if(y == currentPage){
                        pageBtn = $('<li title="'+ y +'" class="page-item"><span style="font-size:18px; text-decoration: underline" class="page-link btn"><b>'+ y +'</b></span></li>');
                    }
                    else{
                        pageBtn = $('<li title="'+ y +'" class="page-item"><span class="page-link btn">'+ y +'</span></li>');       
                    }  
                    paginator.append(pageBtn); 
                    y++;           
                    if(stop == 10){
                        break;
                    }
                }

                if(nextPage) {
                    let x = currentPage + 1;
                    console.log(x);
                    let nextPageBtn = $('<li title="'+ x +'" class="page-item"><span class="page-link btn">Next</span></li>');
                    paginator.append(nextPageBtn);
                }
                if(currentPage != numPages) {
                    let x = numPages;
                    let lastPageBtn = $('<li title="'+ x +'" class="page-item"><span class="page-link btn">Last</span></li>');
                    paginator.append(lastPageBtn);
                }

                $(document).on('click', 'li.page-item', function(event){
                    var x = parseInt($(this).attr('title'));
                    loadCreditNotes(x);
                    event.stopImmediatePropagation();
                });
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

     function searchCreditNote(doc_num) {
        $.ajax({
            url: "http://localhost:8000/dashboard/search_credit_note?doc_num="+doc_num,
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                $('#docs-loader').hide();
                if($.isEmptyObject(result.creditNoteHeader)){
                  swal({
                            title: 'Error Occurred',
                            text: 'No credit note record found',
                            icon: 'error',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
                }
                else{
                var data = result.creditNoteHeader.header[0];
                console.log("success");
                let qrcode = data.qrcode;
                    let veriCode = data.verificationCode;
                    let refNo = data.uraReferenceNo;
                    let invoiceNo = data.oriInvoiceNo;
                    let externalDocumentNo = data.externalDocumentNo;

                    let checkBox = null;
                    let action = null;
                    let color = "";

                    let pending = (refNo != '' && invoiceNo != '' && veriCode == '' && qrcode != '' && externalDocumentNo == '');
                    let pending_customer = (refNo != '' && invoiceNo != '' && veriCode == '' && qrcode == '' && externalDocumentNo == '');
                    let uploaded = (refNo != '' && invoiceNo != '' && veriCode != '' && qrcode != '' && externalDocumentNo != '');

                    let tablerow = $('<tr></tr>');

                    if(uploaded){
                      checkBox = $('<td class="text-center"></td>');
                      tablerow.addClass("table-success");
                    }
                    else if(pending_customer){
                      checkBox = $('<td class="text-center"></td>');
                      tablerow.addClass("table-danger");
                    }
                    else if(pending){
                      checkBox = $('<td class="text-center"><input type="checkbox" class="check-credit-note" value="'+data.creditNoteNo+'"/></td>');
                      tablerow.addClass("table-warning");
                    }
                    else{
                      checkBox = $('<td class="text-center"><input type="checkbox" class="check-credit-note" value="'+data.creditNoteNo+'"/></td>');
                      tablerow.addClass("table-info");
                    }

                    let applicationTime = data.applicationTime;
                    let [month, date, year] = new Date(applicationTime).toLocaleDateString("en-US").split("/");
                    let [hour, minute, second] = new Date(applicationTime).toLocaleTimeString("en-US").split(/:| /)
                    let dateTime = date+"-"+month+"-"+year+" "+hour+":"+minute+":"+second

                    let rowCount = $('<td>1</td>');
                    let creditNoteNo = $('<td>'+data.creditNoteNo+'</td>');
                    let documentDate = $('<td>'+dateTime+'</td>');
                    let operator = $('<td>'+data.operator+'</td>');
                    let customerName = $('<td>'+data.customerName+'</td>');
                    let externalDocumentNumber = '<td>'+data.externalDocumentNo+'</td>';
                    let uraReferenceNo = '<td>'+data.uraReferenceNo+'</td>';

                    tablerow.append(checkBox);
                    tablerow.append(rowCount);
                    tablerow.append(creditNoteNo);
                    tablerow.append(documentDate);
                    tablerow.append(operator);
                    tablerow.append(customerName);
                    tablerow.append(externalDocumentNumber);
                    tablerow.append(uraReferenceNo);

                    if(uploaded){
                      action = $('<td>Uploaded</td>');
                      tablerow.append(action);
                    }
                    else if(pending_customer) {
                      action = $('<td><button type="button" title="'+data.uraReferenceNo+'" class="btn btn-primary pending-btn" id="pending-client">Pending</button><input type="hidden" id="'+data.uraReferenceNo+'" value="'+data.creditNoteNo+'"></td>');
                      tablerow.append(action);
                    }
                    else if(pending){
                      action = $('<td>Not Uploaded</td>');
                      tablerow.append(action);
                    }
                    else {
                      action = $('<td>Not Uploaded</td>');
                      tablerow.append(action);
                    }

                    orderTableBody.append(tablerow)
                  }
            },
            error: function(xhr, textStatus, errorMessage) {
                swal({
                            title: 'Error Occurred',
                            text: 'No invoice record found',
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

    loadCreditNotes();

      searchCreditNoteBtn.click(function(){
      var txt = searchCreditNoteTextField.val();
      if(txt == ""){
        swal({
                            title: 'Error Occurred',
                            text: 'Enter document number',
                            icon: 'error',
                            button: {
                              text: "Ok",
                              value: true,
                              visible: true,
                              className: "btn btn-primary"
                            }
                          })
      }
      else{
        orderTableBody.empty();
        paginator.empty();
        $('#docs-loader').show();
        searchCreditNote(txt);
      }
    });

     uploadCreditNotesBtn.click(function(){
        
        var checkedinvoice = $('.check-credit-note');
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
            uploadCreditNotesBtn.prop('disabled', true);

            var s = $(".check-credit-note:checked")
            var documentNumber = s[0].value;

            $.ajax({
                url: "http://localhost:8000/dashboard/upload_credit_note?documentNumber="+documentNumber+"&service_name="+serviceName,
                beforeSend: function(request) {
                    $('#e-loader').show();
                    console.log("before send");
                },
                success: function(result, status, xhr) {
                    $('#e-loader').hide()
                    uploadCreditNotesBtn.prop('disabled', false);
                    console.log("success");
                    console.log(result);
                    if(result.returnStateInfo.returnCode != "00") {
                        swal({
                            title: 'Error Occurred',
                            text: ''+result.returnStateInfo.returnMessage,
                            icon: 'error',
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
                            title: 'Credit Note Successfully Generated',
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
                    
                },
                error: function(xhr, textStatus, errorMessage) {
                    $('#e-loader').hide();
                    uploadCreditNotesBtn.prop('disabled', false);
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