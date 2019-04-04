
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
        //console.log(c_index);
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
                //console.log(params);
            }
        });
    }

    var plotType = null;

    $('#plotSelect .btn').on('click', function(event) {
        plotType = $(this).find('input').val();
    });

    $("#querySubmit").click(function() {
        if(params.length == 0) {
            alert('Please select a dataset.');
            return;
        }
        if(plotType == null) {
            alert('Please select a plot type');
            return;
        }

        var datasetType = params[0];
        var strippedParams = params.slice(1, params.length)
        var geographic = false;
        var timeSeries = false;
        var endpoint = "";
        var args = "";

        if(plotType == '0') {
            geographic = true;
        }
        else {
            geographic = false;
        }

        if(datasetType == 'Time Series') {
            timeSeries = true;
        }
        else {
            timeSeries = false;
        }

        if(timeSeries) {
            if(geographic) {
                endpoint = 'ts_geo';
            }
            else {
                endpoint = 'ts_plot';
            }
        }
        else {
            if(geographic) {
                endpoint = 'geo';
            }
            else {
                endpoint = 'plot';
            }
        }

        if(timeSeries) {
            strippedParams.unshift('timeseries');
        }

        args += 'endpoint=' + endpoint + '&'

        for(var i = 0; i < strippedParams.length; i++) {
            args += 'p=' + strippedParams[i].toString() + '&';
        }

        args = args.slice(0, args.length - 1);

        var url = "http://localhost:5000/" + 'var_select' + '?' + args;
        console.log(url);

        window.location = url;
    });
    
});
