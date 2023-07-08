$(document).ready(function () {
   
    $(".btn").click(function () {
        $.ajax({
            url: "/test",
            type: "get",
            dataType: "json",
            data: {
                button_text: $(this).text()
            },
            success: function (response) {
                var obj = JSON.parse(response)
                for (let i = 0; i < obj.length; i++) {
                    console.log(obj[i].fields.date)
                    // $("#seconds").append("div class='dates unopened'");
                    
                }
                // console.log(obj.fields.date)
                // $(".btn").text(response.seconds)
                
            }

        });
    });

});