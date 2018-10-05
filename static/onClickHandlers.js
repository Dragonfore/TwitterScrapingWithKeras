const plot = (data,svg) => {
    var pos = 0;
    for (var data_point of data){
        var my_dat;
        if(data_point.innerHTML){
            my_dat += data_point.innerHTML;
            if (pos <= 2){
                data_point.innerHTML = "1547";
            }
            else{
                data_point.innerHTML = "Changed!";
            }
            pos += 1;
        }
    } 
    alert(my_dat)
}