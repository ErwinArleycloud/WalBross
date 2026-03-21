// ------------------ FUNCIÓN: Enviar pedido por WhatsApp ------------------
function enviarpedido(nombre, precio) {
    // 1. Número de teléfono del negocio (formato internacional)
    const telefono = "573043247458";
    
    // 2. Formatear el precio con separadores de miles (estilo colombiano)
    const precioFormateado = new Intl.NumberFormat('es-CO').format(precio);

    // 3. Crear el mensaje con nombre y precio del producto
    const mensaje = `¡Hola! Me gustaria pedir: *${nombre}* Precio: *$${precioFormateado}* ¿Me podrian confirmar el pedido?`;

    // 4. Codificar el mensaje para URL y armar el enlace de WhatsApp
    const mensajeEncoded = encodeURIComponent(mensaje);
    const url = `https://wa.me/${telefono}?text=${mensajeEncoded}`;

    // 5. Abrir WhatsApp en una nueva pestaña
    window.open(url, '_blank');
}

// ------------------ FUNCIÓN: Filtrar productos por categoría ------------------
function filtrarcategoria(categoria, boton) {
    // 1. Seleccionar todas las tarjetas de producto
    const productos = document.querySelectorAll('.tarjeta-producto');

    // 2. Mostrar u ocultar según la categoría seleccionada
    productos.forEach(prod => {
        // Si la categoría es "todos" o coincide con la tarjeta, se muestra
        if (categoria === 'todos' || prod.getAttribute('data-categoria') === categoria) {
            prod.style.display = 'block';
        } else {
            prod.style.display = 'none';
        }
    });

    // 3. Cambiar el estado visual de los botones
    // Elimina la clase "active" de todos los botones
    document.querySelectorAll('.btn-categoria').forEach(btn => btn.classList.remove('active'));
    
    // 4. Agrega la clase "active" al botón seleccionado
    boton.classList.add('active');
}
