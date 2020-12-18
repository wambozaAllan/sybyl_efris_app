$(document).ready(function () {
    let uploadInvoiceBtn = $("#upload-invoices");
    let checkInvoice = $('.check-invoice');
    let checkAllInvoices = $("#check-all-invoices");

    let uploadItemsBtn = $("#upload-items");
    let checkItems = $('.check-item');
    let checkAllItems = $("#check-all-items");



    function checkBoxes(btn, checkAll, itemCheck){
        checkAll.click(function () {
            itemCheck.not(this).prop('checked', this.checked);
            if(itemCheck.not(':checked').length == itemCheck.length) {
                console.log("nothing is checked");
                btn.attr("disabled", true);
            } 
            else {
                btn.attr("disabled", false);
            }
        });
    
        itemCheck.click(function () {
            checkAll.prop('checked', false);
            if(itemCheck.not(':checked').length == itemCheck.length) {
                console.log("nothing is checked");
                btn.attr("disabled", true);
            } 
            else {
                btn.attr("disabled", false);
            }
        });
    }

    checkBoxes(uploadInvoiceBtn, checkAllInvoices, checkInvoice);
    checkBoxes(uploadItemsBtn, checkAllItems, checkItems);
})