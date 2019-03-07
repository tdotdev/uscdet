
$(document).ready(function () {
    const Http = new XMLHttpRequest();
    const url = 'http://localhost:5000/index_json';
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange=(e)=>{
        var response = Http.responseText;
        var c_index = JSON.parse(response);
        c_index = [c_index];
        console.log(c_index);
        $('#tree').treeview({data: c_index});
    }

});
