$(document).ready(function () {
   
    $(".btn").click(function () {
        $.ajax({
            url: "test/",
            type: "get",
            data: {
                button_text: $(this).text()
            },
            success: function (response) {
                $(".btn").text(response.seconds)
            }

        });
    });

});