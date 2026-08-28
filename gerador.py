def gerar_sql_script(ids):
    if not ids:
        raise ValueError("Nenhum ID válido foi encontrado no campo de texto.")

    valores_insert = ",\n".join([f"\t('{id_str}')" for id_str in ids])

    sql_template = f"""DECLARE @IdsParaProcessar TABLE (
    ID_ESOCIAL Varchar(36),
    UID UNIQUEIDENTIFIER
);

-- Inserir id's para deletar!
INSERT INTO @IdsParaProcessar (ID_ESOCIAL)
VALUES
{valores_insert};

  UPDATE P
SET P.UID = E.UID
FROM @IdsParaProcessar P
JOIN ESOCIAL_EVENTO E
    ON E.ID_ESOCIAL = P.ID_ESOCIAL;

;WITH EventosRecursivos AS
(
    -- Eventos da lista original
    SELECT E.UID
    FROM ESOCIAL_EVENTO E
    JOIN @IdsParaProcessar P
        ON P.UID = E.UID

    UNION ALL

    -- Filhos
    SELECT F.UID
    FROM ESOCIAL_EVENTO F
    JOIN EventosRecursivos R
        ON F.ID_EVENTO_ORIGEM = R.UID
)
INSERT INTO @IdsParaProcessar (UID)
SELECT DISTINCT R.UID
FROM EventosRecursivos R
WHERE NOT EXISTS (
    SELECT 1
    FROM @IdsParaProcessar P
    WHERE P.UID = R.UID
);

UPDATE P
SET P.ID_ESOCIAL = E.ID_ESOCIAL
FROM @IdsParaProcessar P
JOIN ESOCIAL_EVENTO E
    ON E.UID = P.UID
WHERE P.ID_ESOCIAL IS NULL;

DELETE FROM ESOCIAL_EVENTO_ALTERADO
WHERE ID_ESOCIAL_EVENTO IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE FROM ESOCIAL_EVENTO_ARQUIVO
WHERE ID_ESOCIAL_EVENTO IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE FROM ESOCIAL_EVENTO_TOTALIZADOR
WHERE ID_ESOCIAL_EVENTO IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE ECO
FROM ESOCIAL_LOTE_EVENTO_OCORRENCIA ECO
JOIN ESOCIAL_LOTE_EVENTO ELE
    ON ECO.ID_ESOCIAL_LOTE_EVENTO = ELE.UID
WHERE ELE.ID_ESOCIAL_EVENTO IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE FROM ESOCIAL_LOTE_EVENTO
WHERE ID_ESOCIAL_EVENTO IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE FROM ESOCIAL_EVENTO
WHERE UID IN (
    SELECT UID FROM @IdsParaProcessar
);

DELETE FROM ESOCIAL_IMPORTADOR
WHERE ID_ESOCIAL IN (
    SELECT ID_ESOCIAL FROM @IdsParaProcessar
);"""

    return sql_template

