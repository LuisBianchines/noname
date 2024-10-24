from connection import Connection

class CreatingDatabaseStructure():

    def __init__(self):
        CreatingDatabaseStructure.create_structure()        
        
    @staticmethod 
    def create_table_client():
        _qry = """CREATE TABLE public.client (
                    id varchar NOT NULL,
                    razao_social varchar NULL,
                    nome_fantasia varchar NULL,
                    identificacao varchar NULL,
                    tipo_contato int4 NULL,
                    contato varchar NULL,
                    tipo_contato2 int4 NULL,
                    contato2 varchar NULL,
                    email varchar NULL,
                    site varchar NULL,
                    endereco varchar NULL,
                    cep varchar NULL,
                    nro varchar NULL,
                    complemento varchar NULL,
                    uf varchar NULL,
                    cidade varchar NULL,
                    bairro varchar NULL,
                    dt_abertura timestamp NULL,
                    ins_estadual varchar NULL,
                    ins_municipal varchar NULL,
                    tp_regime_tributario int4 NULL,
                    ie_substituto varchar NULL,
                    ins_suframa varchar NULL,
                    cnae varchar NULL
                );
                """    
        Connection.execute(_qry)

    @staticmethod
    def create_structure():
        CreatingDatabaseStructure.create_table_client()
