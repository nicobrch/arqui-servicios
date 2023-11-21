CREATE TABLE usuario (
    id serial PRIMARY KEY,
    usuario char(20) UNIQUE NOT NULL,
    nombre char(20) NOT NULL,
    cargo char(20) NOT NULL,
    tipo char(10) NOT NULL,
    password char(72) NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    updated_at date DEFAULT current_date NOT NULL
);

CREATE TABLE bloque (
    id serial PRIMARY KEY,
    hora_inicio int NOT NULL,
    hora_fin int NOT NULL,
    dia char(10) NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    updated_at date DEFAULT current_date NOT NULL
);

CREATE TABLE asignacion (
    id serial PRIMARY KEY,
    usuario_id int NOT NULL,
    bloque_id int NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    updated_at date DEFAULT current_date NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ,
    FOREIGN KEY (bloque_id) REFERENCES bloque(id) ON DELETE CASCADE
);

CREATE TABLE comentarios (
    id serial PRIMARY KEY,
    usuario_id int NOT NULL,
    asignacion_id int NOT NULL,
    texto char(100) NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (asignacion_id) REFERENCES asignacion(id) ON DELETE CASCADE
);

INSERT INTO usuario (usuario, nombre, cargo, tipo, password)
VALUES
('jonas', 'jonas', 'tecnico', 'admin', '123'),
('nico', 'nico', 'admin', 'admin', '456'),
('diego', 'diego', 'medico', 'personal', '789');

INSERT INTO bloque (hora_inicio, hora_fin, dia)
VALUES
(9, 12, 'lunes'),
(14, 17, 'martes'),
(10, 13, 'miercoles');

INSERT INTO asignacion (usuario_id, bloque_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO comentarios (usuario_id, asignacion_id, texto)
VALUES
(1, 1, 'hola'),
(2, 2, 'hola2'),
(3, 3, 'hola3');
