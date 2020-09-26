$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#final').fadeIn(600);
                var com ,i;
                var names = ["None of These","Melanoma","Melanocytic Nevus","Basal Cell carcinoma","Actinic Keratosis","Benign Keratosis","Dermatofibroma","Vascular Lesion","Squamous cell carcinoma"]
                com = "<h3 >RESULTS</h3><br><br><ul>";
                for(i=1;i<9;i++)
                {
                    com += "<li>" + names[i] +"   " + "<b>" +  data[i+1] + "</b>"+ "%</li>";
                }
                com += "<li>" + names[0] +"   " + "<b>" +  data[1] + "</b>"+ "%</li>";
                com += "</ul>"
                $('#final').html(com);
                console.log(data);
                console.log("type of data" + typeof(data));
            },
        });
    });

});