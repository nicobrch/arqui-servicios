CREATE TABLE usuario (
    id serial PRIMARY KEY,
    usuario char(20) NOT NULL,
    nombre char(20) NOT NULL,
    cargo char(20),
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
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (bloque_id) REFERENCES bloque(id)
);

CREATE TABLE comentarios (
    id serial PRIMARY KEY,
    usuario_id int NOT NULL,
    asignacion_id int NOT NULL,
    texto char(100) NOT NULL,
    created_at date DEFAULT current_date NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (asignacion_id) REFERENCES asignacion(id)
);

