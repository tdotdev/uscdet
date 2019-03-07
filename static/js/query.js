
$(document).ready(function () {
    const Http = new XMLHttpRequest();
    const url = 'http://localhost:5000/index_json';
    var params = [];

    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange=(e)=>{
        var response = Http.responseText;
        var c_index = JSON.parse(response);
        c_index = [c_index];
        console.log(c_index);
        $('#tree').treeview({
            data: c_index,
            onNodeSelected: function(event, node) {
                params = [];
                node = $('#tree').treeview('getParent', node);
                while(node.text != 'Datasets') {
                    params.push(node.text);
                    node = $('#tree').treeview('getParent', node);
                }
                params = params.reverse();
                console.log(params);
            }
        });
    }

    
    $("#data-select").submit(function(){
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
               window.location.href = "localhost:5000/geo";
            }
        })
    });
});
