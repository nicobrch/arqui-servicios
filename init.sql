CREATE TABLE usuario (
    rut INT PRIMARY KEY,
    name CHAR(50),
    type CHAR(10),
    rol CHAR(20),
    password VARCHAR,
    created_at DATE DEFAULT CURRENT_DATE,
    updated_at DATE DEFAULT CURRENT_DATE
);

INSERT INTO usuario (rut, name, type, rol, password)
VALUES
    (111, 'User1', 'Type1', 'Role1', 'password1'),
    (222, 'User2', 'Type2', 'Role2', 'password2'),
    (333, 'User3', 'Type3', 'Role3', 'password3'),
    (444, 'User4', 'Type4', 'Role4', 'password4'),
    (555, 'User5', 'Type5', 'Role5', 'password5');
