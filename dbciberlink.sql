CREATE DATABASE ciberlink_db;
USE ciberlink_db;

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    marca_equipo VARCHAR(100),
    numero_serie VARCHAR(50),
    sistema_operativo VARCHAR(50),
    disco_duro VARCHAR(50),
    memoria_ram VARCHAR(50),
    accesorios TEXT,
    estado_equipo TEXT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);