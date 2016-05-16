$(function() { 
    /*
       This function parses the image encodings and calls the API.
       It's given as a callback to the ajax call to ensure it's executed with the proper data upon completion.
    */
    function parseImages(imageEncodings) {
        var encodings = JSON.parse(imageEncodings);
        getAuthors(encodings);
    }
    
    function getAuthors(PDFs) {
        $.each(PDFs, function(index, encoding) {
            $.ajax({
                url: 'http://localhost:8001/extractor/file',
                type: 'POST',
                data: encoding, 
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {alert('done'); console.log(data);}
            });
        });
    }
    /*
        Ajax call to get the images from the server, returns the base64 encoding to the proper function.
    */
    $.ajax({
        url: 'upload.php', 
        type: 'GET',
        success: parseImages
    });
});
