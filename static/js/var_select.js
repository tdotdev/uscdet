
  



$(document).ready(function () {
    $("#varSubmit").click(function() {

        var get_params = function(search_string) {

            var parse = function(params, pairs) {
              var pair = pairs[0];
              var parts = pair.split('=');
              var key = decodeURIComponent(parts[0]);
              var value = decodeURIComponent(parts.slice(1).join('='));
          
              // Handle multiple parameters of the same name
              if (typeof params[key] === "undefined") {
                params[key] = value;
              } else {
                params[key] = [].concat(params[key], value);
              }
          
              return pairs.length == 1 ? params : parse(params, pairs.slice(1))
            }
          
            // Get rid of leading ?
            return search_string.length == 0 ? {} : parse({}, search_string.substr(1).split('&'));
          }
          
        var params = get_params(location.search);

        var plotType = params['endpoint']
        var params = params['p']

        console.log(params)

        var checked = $('.var:checkbox:checked');

        if(checked.length == 0) {
            console.log('Please select at least one variables.')
            return
        }

        if(checked.length > 9) {
            console.log('Please select less than ten variables.')
            return
        }

        var args = [];

        for(var i = 0; i < checked.length; i++)
        {
            args.push(checked[i].value)
        }

        dargs = ""

        for(var i = 0; i < params.length; i++) {
            dargs += 'p=' + params[i] + '&';
        }

        for(var i = 0; i < args.length; i++) {
            dargs += 'v=' + args[i] + '&';
        }

        dargs = dargs.slice(0, dargs.length - 1);

        var url = "http://localhost:5000/" + plotType + '?' + dargs;

        window.location = url;
    });
});