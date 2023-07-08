function displaydates(area) {
    // console.log(area);
    const area_date = document.getElementById(area);
    // console.log(area_date.style.height);
    if (area_date.style.height != "120px") {
        area_date.style.height = "120px";
        area_date.innerHTML = "";
        // dates(area_date)
    } else {
        area_date.style.height = "0px";
        area_date.innerHTML = "";
    }
    
}


$(document).ready(function () {
    $(".areas").click(function (event) {

        var text = $(this).text();
        text = text.trim();

        $.ajax({
            url: "/reportlist",
            type: "GET",
            datatype: "json",
            data: {
                btn_txt: $(this).text()
            },
            success: function (response) {
                // console.log(response)
                var obj = JSON.parse(response)
                for (let i = 0; i < obj.length; i++) {
                    // console.log(obj[i].fields.date);
                    // console.log(obj[i].fields.viewed);
                    text = text.replace(",", "");
                    text = text.split(" ")
                    text = text.join("_")
                    // console.log(text);

                    var unopened = obj[i].fields.viewed ? "" : "unopened";

                    var out = "<div class=" + "'" + unopened + " dates'>"
                    // console.log(out)
                    var link = "<a href='/reporttable/" + text + "_" + obj[i].fields.date + "' >"

                    var eng_date = new Date(obj[i].fields.date)
                    var eng_date = eng_date.toLocaleString('default', { month: 'short', day:'2-digit', year:'numeric'});

                    // console.log(month)
                    // console.log(moment(eng_date).format('MMMM D Y'));


                    // console.log(data.btn_txt);
                    $("." + text.toString()).append(
                       link + out + "<h5>" +  eng_date + "</h5>" + "</div>" + "</a>"
                    );
                    // $("#seconds").append("<li>" +  obj[i].fields.date + "</li>")

                }
                // alert("Hello World!");
            }
        });

    });
});

//  function dates(area_date) {
//     {% for report in reports %}
//         var date = '{{ report }}'
//         var dt = new Date(date)
//         dt = dt.toLocaleDateString("en-EN", {
//             day: "numeric",
//             month: "long",
//             year: "numeric"
//         })

//          area_date.innerHTML +=
//                 ' <div class="dates unopened">' +
//                 '<h5>'+ dt +'</h5>' +
//                 '</div>';
//     {% endfor %}
// }

// function dates(area_date) {
//     for (let i = 0; i < 5; i++) {
//         area_date.innerHTML +=
//             ' <div class="dates unopened">' +
//             '<h5>Jun 12th 2023</h5>' +
//             '</div>';
//     }

        
// }