-- Elimina la tabla productos si ya existe (evita errores al volver a crearla)
DROP TABLE IF EXISTS productos;

-- Crea la tabla productos con sus columnas
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único autoincremental
    nombre TEXT NOT NULL UNIQUE,          -- Nombre del producto, obligatorio y único (no permite duplicados)
    descripcion TEXT NOT NULL,            -- Descripción del producto, obligatoria
    precio INTEGER NOT NULL,              -- Precio en números enteros, obligatorio
    imagen TEXT NOT NULL,                 -- Nombre del archivo de imagen, obligatorio
    es_promocion BOOLEAN DEFAULT 0,       -- Indica si el producto está en promoción (0 = no, 1 = sí)
    categoria TEXT NOT NULL               -- Categoría del producto (pollos, combos, bebidas, adicionales)
);
