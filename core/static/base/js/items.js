$(document).ready(function(){
    function loadItems() {
        $.ajax({
            url: "http://localhost:8000/dashboard/load_items",
            headers: {
                "Accept":"application/json"
            },
            beforeSend: function(request) {
                console.log("before send");
            },
            success: function(result, status, xhr) {
                console.log("success");
            },
            error: function(xhr, textStatus, errorMessage) {
                console.log(xhr)
                console.log("error, "+ errorMessage);
            },
          });
    }
    loadItems();
});