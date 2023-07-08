function displaydates(area) {
    // console.log(area);
    const area_date = document.getElementById(area);
    // console.log(area_date.style.height);
    if (area_date.style.height != "120px") {
        area_date.style.height = "120px";
        dates(area_date)
    } else {
        area_date.style.height = "0px";
    }
    
}

// function dates(area_date) {
//     for (let i = 0; i < 5; i++) {
//         area_date.innerHTML +=
//             ' <div class="dates unopened">' +
//             '<h5>Jun 12th 2023</h5>' +
//             '</div>';
//     }

        
// }