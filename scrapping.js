// Simular el envío de solicitudes a la página ahrefs.com

// Encuentra los campos de texto y la imagen en la página
var textoCampo = document.querySelector(
  ".css-yv8joh.css-z0n7n9.css-yqhlb3-textAreaMaxHeight"
); // Selector de clase para el textarea
var imagenCampo = document.querySelector('input[type="file"]'); // Selector para el campo de archivo de imagen

// Establece el texto y la imagen que deseas enviar
var texto = "pizza";
var imagenURL =
  "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.foodandwine.com%2Frecipes%2Fclassic-cheese-pizza&psig=AOvVaw14b1AS7R-kTT3mtK-YoAlh&ust=1702661787330000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNDrhsq7j4MDFQAAAAAdAAAAABAD";

// Agrega el texto y la imagen a los campos
textoCampo.value = texto;

// Crea un nuevo evento de cambio para el campo de imagen
var eventoCambio = new Event("change", { bubbles: true });
imagenCampo.files = [
  new File([""], "nombre-de-archivo.jpg", { type: "image/jpeg" }),
]; // Reemplaza 'nombre-de-archivo.jpg' con el nombre real de la imagen
imagenCampo.dispatchEvent(eventoCambio);

// Envía la solicitud automáticamente
document.forms[0].submit(); // Puede ser necesario ajustar según la estructura del formulario
