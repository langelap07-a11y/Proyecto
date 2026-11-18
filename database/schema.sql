-- Base de datos: Rutas de recolección de basura
-- Importar desde phpMyAdmin (XAMPP) o ejecutar con: mysql -u root < schema.sql
CREATE DATABASE IF NOT EXISTS rutas_basura CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE rutas_basura;

DROP TABLE IF EXISTS parada;
DROP TABLE IF EXISTS reporte;
DROP TABLE IF EXISTS ruta;
DROP TABLE IF EXISTS barrio;

CREATE TABLE barrio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  sector VARCHAR(40) NOT NULL
);

CREATE TABLE ruta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  id_barrio INT NOT NULL,
  dia_semana VARCHAR(60) NOT NULL,
  hora_inicio TIME NOT NULL,
  vehiculo VARCHAR(40) NOT NULL,
  FOREIGN KEY (id_barrio) REFERENCES barrio(id) ON DELETE CASCADE
);

CREATE TABLE parada (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_ruta INT NOT NULL,
  orden INT NOT NULL,
  direccion VARCHAR(150) NOT NULL,
  referencia VARCHAR(150) DEFAULT '',
  FOREIGN KEY (id_ruta) REFERENCES ruta(id) ON DELETE CASCADE
);

CREATE TABLE reporte (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_barrio INT NOT NULL,
  direccion VARCHAR(150) NOT NULL,
  tipo VARCHAR(50) NOT NULL,
  descripcion VARCHAR(300) DEFAULT '',
  estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_barrio) REFERENCES barrio(id) ON DELETE CASCADE
);

-- Datos de ejemplo (cámbialos por los de tu municipio)
INSERT INTO barrio (nombre, sector) VALUES
 ('Centro', 'Urbano'), ('San Rafael', 'Urbano'), ('El Progreso', 'Urbano'), ('Vereda Centro', 'Rural');

INSERT INTO ruta (nombre, id_barrio, dia_semana, hora_inicio, vehiculo) VALUES
 ('Ruta 1 - Centro', 1, 'Lunes, Miércoles y Viernes', '06:00', 'Compactador ABC-123'),
 ('Ruta 2 - San Rafael', 2, 'Martes y Jueves', '07:00', 'Compactador DEF-456'),
 ('Ruta 3 - El Progreso', 3, 'Martes y Sábado', '06:30', 'Compactador ABC-123'),
 ('Ruta 4 - Vereda Centro', 4, 'Sábado', '08:00', 'Camión GHI-789');

INSERT INTO parada (id_ruta, orden, direccion, referencia) VALUES
 (1, 1, 'Carrera 5 con Calle 3', 'Frente a la plaza principal'),
 (1, 2, 'Calle 4 # 6-10', 'Esquina panadería'),
 (1, 3, 'Carrera 7 con Calle 5', 'Cerca al colegio'),
 (2, 1, 'Calle 10 # 12-20', 'Parque del barrio'),
 (2, 2, 'Carrera 12 # 9-15', 'Tienda de la esquina'),
 (3, 1, 'Calle 15 # 3-40', 'Salón comunal'),
 (3, 2, 'Carrera 3 # 14-22', ''),
 (4, 1, 'Entrada vereda', 'Junto a la capilla'),
 (4, 2, 'Escuela rural', '');

INSERT INTO reporte (id_barrio, direccion, tipo, descripcion, estado) VALUES
 (1, 'Calle 4 # 6-10', 'No pasó el camión', 'No pasaron el viernes', 'Pendiente'),
 (2, 'Carrera 12 # 9-15', 'Basura acumulada', 'Bolsas en la esquina desde hace dos días', 'En atención');