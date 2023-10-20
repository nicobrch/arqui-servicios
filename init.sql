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

-- HASH
INSERT INTO usuario (rut, name, type, rol, password)
VALUES
    (123, 'user1', 'Type1', 'Role1', '$2b$10$A1D.G0z39JEBk9Btl.jykuFro0BEK2pDhoLekpJQuCFoU7ZJzUyAe'),
    (234, 'user2', 'Type2', 'Role2', '$2b$10$vO9OQVFXeS6WlYPG7Wn.2Ol7X.ZZ1o9Z2Lj19QdOhrw.24lAe4kF6'),
    (345, 'user3', 'Type3', 'Role3', '$2b$10$5CXO1rxENwjZzLGRDBqsquBIXjs0M0NEsNSgDZs71QynJ.XFIti7i'),
    (456, 'user4', 'Type4', 'Role4', '$2b$10$DMr6OhrXcXYx8oM.Yx7AL.a1UGs.Zs1hPz9UCQGy.7tPsBZeeFurK'),
    (567, 'user5', 'Type5', 'Role5', '$2b$10$ZlU2Nht.S90BC3CH1W8EQeGpiB95fFvRr7vA5wW.p4vj.Hd86UZJm');
