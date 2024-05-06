document.getElementById('pdfInput').addEventListener('change', function(e) {
    var file = e.target.files[0];
    var reader = new FileReader();
  
    reader.onload = function() {
      var pdfData = new Uint8Array(this.result);
      PDFJS.getDocument(pdfData).promise.then(function(pdf) {
        for (var i = 0; i < pdf.numPages; i++) {
          pdf.getPage(i + 1).then(function(page) {
            var canvas = document.createElement('canvas');
            var viewport = page.getViewport({ scale: 1 });
            var scale = 0.5; // Crop the page in half
  
            canvas.width = viewport.width * scale;
            canvas.height = viewport.height;
  
            var context = canvas.getContext('2d');
            var renderContext = {
              canvasContext: context,
              viewport: page.getViewport({ scale: scale })
            };
  
            page.render(renderContext).promise.then(function() {
              var img = document.createElement('img');
              img.src = canvas.toDataURL();
              img.classList.add('page');
              document.getElementById('output').appendChild(img);
            });
          });
        }
      });
    };
  
    reader.readAsArrayBuffer(file);
  });
  