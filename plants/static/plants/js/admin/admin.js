(function($) {
    $(document).ready(function() {
        console.log('loaded');
        $('#cultivar_set-group').addClass('clone');
        $('#commonname_set-group').addClass('clone');
        $(".field-category")
            .after($('#cultivar_set-group').clone(true).removeClass('clone').addClass('half-width'))
            .after($('#commonname_set-group').clone(true).removeClass('clone').addClass('half-width'))
        $('.clone').remove();
        $(".field-comment").before('<div style="clear:both;">&nbsp;</div>');
//        $(".field-category").after('<div class="form-row" id="chosen_category">Categories chosen:<br /><span id="chosen_cat_span"></span><div>');
        $(".vLargeTextField").css({'width':'1070px'});

        $('a').each(function(){
		    if($(this).text() == 'Add another Plant-Category Relationship') {
                $(this).text("Add another Category");
            }
		})

       // $("#id_category_to").live('change', function(){
//        this changes to #id_category_to after SelectFilter2.js gets loaded.
        var showing = new Array();
//        var selectedCategories = $.map($('#id_category option'),function(e) { return $(e).val(); } );
//        showFields(selectedCategories);
        readCategories();


        $("#id_category").live('change', function(e){
            readCategories()
        });

        $(".field-category input[type=checkbox]").click(function(){
//            alert($(this).val());
            readCategories()
        });


    $(".field-old_url a").click(function(e){
        e.preventDefault();
        window.open(this.href, 'Old Url', 'width=700,height=900')
        //alert('old url');
    });

    $(".dynamic-plantimage_set").each(function(){
//        console.log($(this).find('a').attr('href'));
        $(this).find(".field-img_url").append('<p><img src="'+$(this).find('a').attr('href')+'" height="150" /></p>');
    });

    function readCategories() {
//        el = $("#id_category");
        el = $(".field-category input[type=checkbox]");
        selectedCategories = new Array();

        $(".field-category input[type=checkbox]:checked").each(function(){
            selectedCategories.push($(this).val());
        });

//        selectedCategories = new Array();
//            if(el.val()) {
//                selectedCategories=el.val();
//                $('#chosen_cat_span').html('');
//                $('#id_category option:selected').each(function(index, value) {
//                    $('#chosen_cat_span').append($(value).text()+'<br />');
//                });
//            }

        showFields(selectedCategories);
    }

    function showFields(categories) {
        console.log(categories);
        var show = new Array();
        for(var i=0; i<categories.length; i++){
            var cat = categories[i];
            switch(cat){
                case "1": // annual
                    show.push('season','light','color','height','space');
                    break;
                case "7": // summer bulbs
                    show.push('organ','season','light','color','height','space','depth','hardiness','storage');
                    break;
                case "8": // carnivorous
                    show.push('foliage','flower','height');
                    break;
                case "9": // ferns
                    show.push('zones','habit','height','fronds');
                    break;
                case "10": // groundcover
                    show.push('hardiness','habit','site','growth_rate','size','texture','form','flower','foliage');
                    break;
                case "11": // herbs
                    show.push('hardiness','height','space','light','propagation');
                    break;
                case "12": // Spring Bulbs
                case "13": // Perennial Bulbs
                    show.push('origin','organ','season','light','color','height','space','depth','hardiness','storage','flowering_period','flower_color','usage');
                    break;
                case "14": //perennials
                    show.push('origin','season','soil','flower_color','height','exposure','propagation','hardiness','regions');
                    break;
                case "15": //native
                    show.push('zones','habit','height','exposure','fruit');
                    break;
                case "16": //ornamental grass
                    show.push('zones','light','height','soil','form','inflorescence');
                    break;
                case "17": //poison
                    show.push('family','description','origin','distribution','found','mode','poison_part','symptoms','edibility','toxic_principle','severity');
                    break;
                case "18": //roses
                    show.push('sub_type','flower_color','flower','fragrance','height');
                    break;
                case "19": //shrubs
                    show.push('zones','habit','site','width','height','texture','form','flower','foliage');
                    break;
                case "20": //trees
                    show.push('zones','habit','growth_rate','site','width','height','texture','form','flower','leaf');
                    break;
                case "21": //vines
                    show.push('zones','habit','growth_rate','exposure','climbing_method','height','texture','flower');
                    break;
                case "22": //water garden
                    show.push('height','foliage','flower');
                    break;
                case "23": //wildflowers
                    show.push('life_cycle','height','foliage','flower','season','site');
                    break;

                default:
                    break;
            }
        }

        for(s=0;s<showing.length; s++) {
               $('.module > .field-'+showing[s]).hide();
            }


        for(s=0;s<show.length; s++) {
           $('.module > .field-'+show[s]).show();
        }
        showing = show;
//        console.log(showing);
    }

    });
}(django.jQuery));



//    var box = document.getElementById("id_category");
//    for (var i = 0; i < box.options.length; i++) {
//        console.log(box.options[i])
//    }