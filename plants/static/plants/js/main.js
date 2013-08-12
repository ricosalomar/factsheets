$(document).ready(function(){

    //console.log($(".key"));
    //console.log(elExists($(".key-poison-part")));


    var poison = false;
    var poison_fields = new Array($(".key-poison-part"), $(".key-poison-delivery-mode"), $(".key-symptoms"), $(".key-toxic-principle"), $(".key-severity"));
    $.each(poison_fields, function(i, el){
        poison = poison || elExists(el)
    });
    if(poison) { $(".poison-warning").show(); }

    function elExists(el) {
        return el.length > 0;
    }

    $(".search_form").submit(function(e){
        $(".spinner").show();
        if ($("#search_input").val() == '') {
            e.preventDefault();
            $(".search_error").show();
            $(".spinner").hide();
        }
    });


    var cache = {};
    $("#search_input").autocomplete({
        source: function(request, response){
            var term = request.term;
            if ( term in cache ) {
                response( cache[ term ] );
                return;
            }

            $.getJSON( "/autocomplete/", request, function( data, status, xhr ) {
                cache[ term ] = data;
                response( data );
            });
        },
        minLength: 2,
        select: function( event, ui ) {
            console.log( ui.item ?
                "Selected: " + ui.item.value + " aka " + ui.item.url :
                "Nothing selected, input was " + this.value );
            window.location.href = ui.item.url;
        },
        'open': function(e, ui) {
            $('.ui-autocomplete').css('top', $("ul.ui-autocomplete").cssUnit('top')[0] + 4);
            $('.ui-autocomplete').css('left', $("ul.ui-autocomplete").cssUnit('left')[0] - 170);
            $('.ui-autocomplete').css('font-size', '80%');
            $('.ui-autocomplete').css('width', '294px');
        }
    }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
      return $( "<li>" )
        .append( "<a><b>" + item.sci + "</b><br><span>" + item.comm + "</span></a>" )
        .appendTo( ul );
    };


    $("#search_sort").val(GetURLParameter('s'));

    $("#search_sort").change(function(){
        $(".spinner").show();
        window.location.href = updateURLParameter(window.location.href, 's', $(this).val())
    });

    $(".nav_checkbox").not(".checked").prop('checked', false);

    $(".nav_checkbox").change(function(){
        $(".spinner").show();
    });

    if(GetURLParameter('category') || GetURLParameter('flower_color') || GetURLParameter('leaf_color') || GetURLParameter('light') || GetURLParameter('season')){
        if($(".nav_ul").is(":hidden")){
            $(".show").hide();
            $(".hide, #hide_nav, .nav_ul").show();
        }

    }

    $(".nav_toggle, #hide_nav").click(function(){
        $(".nav_ul").slideToggle(function(){
            $(".nav_toggle, #hide_nav").toggle();
        });
    });

    /* Clean up css for tiny_mce */
    $('#left_col dl dd p').last().css('margin-bottom', '0');

    function GetURLParameter(sParam){
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++)
        {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam)
            {
                return sParameterName[1];
            }
        }
        return '';
    }

    function updateURLParameter(url, param, paramVal){
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var base_array= baseURL.split('/');
    base_array.pop(); /* get rid of last '/' */
    if (IsNumeric(base_array.pop())) {
        baseURL = base_array.join('/')+'/';
    }
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

     function IsNumeric(num) {
        return (num >=0 || num < 0);
     }

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

});