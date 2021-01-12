$(document).ready(function(){
    var orderTableBody = $("#order-table-body");
    var uploadInvoiceBtn = $("#upload-invoices");
    var paginator = $("#paginator");
    var searchInvoiceBtn = $('#search-invoices');
    var searchInvoiceTextField = $('#document-number');

    function loadInvoices(page=1) {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_invoices?page="+page,
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                var data = result.invoices
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

                    let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-invoice" value="'+data[counter].antifakeCode+'"/></td>');
                    let rowCount = $('<td>'+ row +'</td>');
                    let antifakeCode = $('<td>'+data[counter].antifakeCode+'</td>');
                    let documentDate = $('<td>'+data[counter].documentDate+'</td>');
                    let operator = $('<td>'+data[counter].operator+'</td>');
                    let invoiceType = $('<td>'+data[counter].invoiceType+'</td>');
                    let customerName = $('<td>'+data[counter].customerName+'</td>');
                    let externalDocumentNumber = '<td>'+data[counter].invoiceNo+'</td>';
                    let oriInvoiceId = '<td>'+data[counter].oriInvoiceId+'</td>';
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

                    row += 1;
                  }

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

                $(document).on('click', 'li', function(event){
                    var x = parseInt($(this).attr('title'));
                    loadInvoices(x);
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

    function searchInvoice(doc_num) {
        $.ajax({
            url: "http://localhost:8000/dashboard/search_invoice?doc_num="+doc_num,
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                $('#docs-loader').hide();
                if($.isEmptyObject(result.invoiceHeader)){
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
                }
                else{
                var data = result.invoiceHeader.header[0];
                console.log("success");
                let tablerow = $('<tr></tr>').addClass("table-info");
                    let checkBox = $('<td class="text-center"><input type="checkbox" class="check-invoice" value="'+data.antifakeCode+'"/></td>');
                    let rowCount = $('<td>1</td>');
                    let antifakeCode = $('<td>'+data.antifakeCode+'</td>');
                    let documentDate = $('<td>'+data.documentDate+'</td>');
                    let operator = $('<td>'+data.operator+'</td>');
                    let invoiceType = $('<td>'+data.invoiceType+'</td>');
                    let customerName = $('<td>'+data.customerName+'</td>');
                    let externalDocumentNumber = '<td>'+data.invoiceNo+'</td>';
                    let oriInvoiceId = '<td>'+data.oriInvoiceId+'</td>';
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
                url: "http://localhost:8000/dashboard/upload_invoice?documentNumber="+documentNumber,
                beforeSend: function(request) {
                    $('#e-loader').show();
                    console.log("before send");
                },
                success: function(result, status, xhr) {
                    $('#e-loader').hide()
                    uploadInvoiceBtn.prop('disabled', false);
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
                            title: 'E-Invoice Successfully Generated',
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

    searchInvoiceBtn.click(function(){
      var txt = searchInvoiceTextField.val();
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
        searchInvoice(txt);
      }
    });
});