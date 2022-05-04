var fileInput = document.getElementById('myFile')
fileInput.addEventListener('change', function () {
  // Følgende funktion vil blive kaldt når en fil uploades:
  // Tilgår uploadet fil
  var RawFile = fileInput.files[0];
  // Tilgår navn
  var FileName = RawFile.name;
  console.log("Fil Modtaget")
  //Indsætter filnavn i label'et
  document.getElementById("upload_text").innerHTML = FileName;
}, false);