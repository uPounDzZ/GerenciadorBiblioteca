class ValidationException(Exception):


    def __init__(self, mensagem="Erro de validação"):
        super().__init__(mensagem)

class LivroInvalidoException(ValidationException):
    """Exceção para quando dados do livro são inválidos"""

    def __init__(self, mensagem="Dados do livro inválidos"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)



class Livro:
    def __init__(self, id, titulo, autor, isbn, ano_publicacao, editora, quantidade_disponivel, bibliotecario_id):
        self.id = id
        self.validar_titulo(titulo)
        self.titulo = titulo
        self.validar_autor(autor)
        self.autor = autor
        self.validar_isbn(isbn)
        self.isbn = isbn
        self.validar_ano_publicacao(ano_publicacao)
        self.ano_publicacao = ano_publicacao
        self.editora = editora
        self.validar_quantidade_disponivel(quantidade_disponivel)
        self.quantidade_disponivel = quantidade_disponivel
        self.bibliotecario_id = bibliotecario_id
        self.status = "DISPONIVEL"

    def validar_titulo(self, titulo):
        """Valida o título do livro"""
        if not titulo or titulo.strip() == "":
            raise LivroInvalidoException("Título não pode ser vazio")

        if len(titulo) > 100:
            raise LivroInvalidoException("Título deve ter no máximo 100 caracteres")

    def validar_autor(self, autor):
        """Valida o autor do livro"""
        if not autor or autor.strip() == "":
            raise LivroInvalidoException("Autor não pode ser vazio")

        if len(autor) > 100:
            raise LivroInvalidoException("Autor deve ter no máximo 100 caracteres")

    def validar_isbn(self, isbn):
        """Valida o ISBN do livro"""
        if not isbn or isbn.strip() == "":
            raise LivroInvalidoException("ISBN não pode ser vazio")


        isbn_limpo = isbn.replace("-", "").replace(" ", "")
        if not (len(isbn_limpo) == 10 or len(isbn_limpo) == 13) or not isbn_limpo.isdigit():
            raise LivroInvalidoException("ISBN inválido. Deve ter 10 ou 13 dígitos")

    def validar_ano_publicacao(self, ano):
        """Valida o ano de publicação"""
        try:
            ano_int = int(ano)
            import datetime
            ano_atual = datetime.datetime.now().year

            if ano_int < 1000 or ano_int > ano_atual:
                raise LivroInvalidoException(f"Ano de publicação deve estar entre 1000 e {ano_atual}")
        except ValueError:
            raise LivroInvalidoException("Ano de publicação deve ser um número válido")

    def validar_quantidade_disponivel(self, quantidade):
        """Valida a quantidade disponível"""
        try:
            qtd = int(quantidade)
            if qtd < 0:
                raise LivroInvalidoException("Quantidade disponível não pode ser negativa")
        except ValueError:
            raise LivroInvalidoException("Quantidade disponível deve ser um número válido")

    def __str__(self):
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | ISBN: {self.isbn} | " \
               f"Ano: {self.ano_publicacao} | Editora: {self.editora} | " \
               f"Qtd Disponível: {self.quantidade_disponivel} | Status: {self.status}"



from biblioteca.core.persistencia.interfaces import PersistenciaInterface
from biblioteca.core.excecoes.livro_excecoes import PersistenciaException





class LivroDAOMemoria(PersistenciaInterface):
    def __init__(self):

        self.livros = {}
        self.proximo_id = 1

    def adicionar(self, livro):
        try:
            livro.id = self.proximo_id
            self.livros[self.proximo_id] = livro
            self.proximo_id += 1
            return livro
        except Exception as e:
            raise PersistenciaException(f"Erro ao adicionar livro: {str(e)}")

    def buscar_por_id(self, id):
        try:
            return self.livros.get(id)
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por ID: {str(e)}")

    def buscar_por_isbn(self, isbn):
        try:
            for livro in self.livros.values():
                if livro.isbn == isbn:
                    return livro
            return None
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por ISBN: {str(e)}")

    def buscar_por_titulo(self, titulo):
        try:
            resultados = []
            titulo_lower = titulo.lower()
            for livro in self.livros.values():
                if titulo_lower in livro.titulo.lower():
                    resultados.append(livro)
            return resultados
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por título: {str(e)}")

    def listar_todos(self):
        try:
            return list(self.livros.values())
        except Exception as e:
            raise PersistenciaException(f"Erro ao listar livros: {str(e)}")

    def atualizar(self, livro):
        try:
            if livro.id in self.livros:
                self.livros[livro.id] = livro
                return True
            return False
        except Exception as e:
            raise PersistenciaException(f"Erro ao atualizar livro: {str(e)}")

    def remover(self, id):
        try:
            if id in self.livros:
                del self.livros[id]
                return True
            return False
        except Exception as e:
            raise PersistenciaException(f"Erro ao remover livro: {str(e)}")



import os
import pickle
from biblioteca.core.persistencia.interfaces import PersistenciaInterface
from biblioteca.core.excecoes.livro_excecoes import PersistenciaException


class LivroDAOArquivo(PersistenciaInterface):
    def __init__(self, arquivo_path):
        self.arquivo_path = arquivo_path
        self.livros = {}
        self.proximo_id = 1


        try:
            self.carregar_arquivo()
        except (FileNotFoundError, EOFError):

            self.livros = {}
            self.proximo_id = 1
        except Exception as e:
            raise PersistenciaException(f"Erro ao inicializar DAO de arquivo para livros: {str(e)}")

    def adicionar(self, livro):
        try:
            livro.id = self.proximo_id
            self.livros[self.proximo_id] = livro
            self.proximo_id += 1

            self.salvar_arquivo()
            return livro
        except Exception as e:
            raise PersistenciaException(f"Erro ao adicionar livro no arquivo: {str(e)}")

    def buscar_por_id(self, id):
        try:
            return self.livros.get(id)
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por ID no arquivo: {str(e)}")

    def buscar_por_isbn(self, isbn):
        try:
            for livro in self.livros.values():
                if livro.isbn == isbn:
                    return livro
            return None
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por ISBN no arquivo: {str(e)}")

    def buscar_por_titulo(self, titulo):
        try:
            resultados = []
            titulo_lower = titulo.lower()
            for livro in self.livros.values():
                if titulo_lower in livro.titulo.lower():
                    resultados.append(livro)
            return resultados
        except Exception as e:
            raise PersistenciaException(f"Erro ao buscar livro por título no arquivo: {str(e)}")

    def listar_todos(self):
        try:
            return list(self.livros.values())
        except Exception as e:
            raise PersistenciaException(f"Erro ao listar livros do arquivo: {str(e)}")

    def atualizar(self, livro):
        try:
            if livro.id in self.livros:
                self.livros[livro.id] = livro
                self.salvar_arquivo()
                return True
            return False
        except Exception as e:
            raise PersistenciaException(f"Erro ao atualizar livro no arquivo: {str(e)}")

    def remover(self, id):
        try:
            if id in self.livros:
                del self.livros[id]
                self.salvar_arquivo()
                return True
            return False
        except Exception as e:
            raise PersistenciaException(f"Erro ao remover livro do arquivo: {str(e)}")

    def salvar_arquivo(self):
        try:

            os.makedirs(os.path.dirname(self.arquivo_path), exist_ok=True)


            with open(self.arquivo_path, 'wb') as arquivo:
                pickle.dump((self.livros, self.proximo_id), arquivo)
        except Exception as e:
            raise PersistenciaException(f"Erro ao salvar arquivo de livros: {str(e)}")

    def carregar_arquivo(self):
        try:

            with open(self.arquivo_path, 'rb') as arquivo:
                self.livros, self.proximo_id = pickle.load(arquivo)
        except (FileNotFoundError, EOFError):

            self.livros = {}
            self.proximo_id = 1
        except Exception as e:
            raise PersistenciaException(f"Erro ao carregar arquivo de livros: {str(e)}")



import os
from biblioteca.core.persistencia.usuario_dao_memoria import UsuarioDAOMemoria
from biblioteca.core.persistencia.usuario_dao_arquivo import UsuarioDAOArquivo
from biblioteca.core.persistencia.livro_dao_memoria import LivroDAOMemoria
from biblioteca.core.persistencia.livro_dao_arquivo import LivroDAOArquivo


class DAOFactory:
    _tipo_persistencia = None
    _usuario_dao = None
    _livro_dao = None

    @classmethod
    def configurar(cls, tipo_persistencia="MEMORIA"):
        if tipo_persistencia not in ["MEMORIA", "ARQUIVO"]:
            tipo_persistencia = "MEMORIA"
        cls._tipo_persistencia = tipo_persistencia
        cls._usuario_dao = None
        cls._livro_dao = None

    @classmethod
    def get_tipo_persistencia(cls):
        if cls._tipo_persistencia is None:
            cls.configurar()
        return cls._tipo_persistencia

    @classmethod
    def get_usuario_dao(cls):
        if cls._usuario_dao is None:
            if cls.get_tipo_persistencia() == "MEMORIA":
                cls._usuario_dao = UsuarioDAOMemoria()
            else:

                diretorio = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados')
                if not os.path.exists(diretorio):
                    os.makedirs(diretorio)

                arquivo_path = os.path.join(diretorio, 'usuarios.bin')
                cls._usuario_dao = UsuarioDAOArquivo(arquivo_path)

        return cls._usuario_dao

    @classmethod
    def get_livro_dao(cls):
        if cls._livro_dao is None:
            if cls.get_tipo_persistencia() == "MEMORIA":
                cls._livro_dao = LivroDAOMemoria()
            else:

                diretorio = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados')
                if not os.path.exists(diretorio):
                    os.makedirs(diretorio)

                arquivo_path = os.path.join(diretorio, 'livros.bin')
                cls._livro_dao = LivroDAOArquivo(arquivo_path)

        return cls._livro_dao


from biblioteca.core.entidades.livro import Livro
from biblioteca.core.persistencia.dao_factory import DAOFactory
from biblioteca.core.excecoes.validacao_excecoes import ValidationException, LivroInvalidoException, PersistenciaException


class LivroService:
    def __init__(self):
        self.livro_dao = DAOFactory.get_livro_dao()
        self.usuario_dao = DAOFactory.get_usuario_dao()

    def adicionar_livro(self, titulo, autor, isbn, ano_publicacao, editora, quantidade_disponivel, bibliotecario_id):
        try:

            bibliotecario = self.usuario_dao.buscar_por_id(bibliotecario_id)
            if not bibliotecario:
                raise ValidationException("Bibliotecário não encontrado")

            if bibliotecario.tipo != "BIBLIOTECARIO":
                raise ValidationException("Apenas bibliotecários podem cadastrar livros")


            if self.livro_dao.buscar_por_isbn(isbn):
                raise ValidationException("Já existe um livro com este ISBN")


            livro = Livro(0, titulo, autor, isbn, ano_publicacao, editora, quantidade_disponivel, bibliotecario_id)
            return self.livro_dao.adicionar(livro)
        except (ValidationException, PersistenciaException) as e:

            raise e
        except Exception as e:

            raise ValidationException(f"Erro ao adicionar livro: {str(e)}")

    def atualizar_livro(self, id, titulo, autor, isbn, ano_publicacao, editora, quantidade_disponivel, bibliotecario_id):
        try:

            livro_existente = self.livro_dao.buscar_por_id(id)
            if not livro_existente:
                raise ValidationException("Livro não encontrado")


            bibliotecario = self.usuario_dao.buscar_por_id(bibliotecario_id)
            if not bibliotecario:
                raise ValidationException("Bibliotecário não encontrado")

            if bibliotecario.tipo != "BIBLIOTECARIO":
                raise ValidationException("Apenas bibliotecários podem atualizar livros")


            if isbn != livro_existente.isbn:
                livro_com_isbn = self.livro_dao.buscar_por_isbn(isbn)
                if livro_com_isbn and livro_com_isbn.id != id:
                    raise ValidationException("Já existe outro livro com este ISBN")


            livro_atualizado = Livro(id, titulo, autor, isbn, ano_publicacao, editora, quantidade_disponivel, bibliotecario_id)
            livro_atualizado.status = livro_existente.status

            return self.livro_dao.atualizar(livro_atualizado)
        except (ValidationException, PersistenciaException) as e:
            raise e
        except Exception as e:
            raise ValidationException(f"Erro ao atualizar livro: {str(e)}")

    def remover_livro(self, id, bibliotecario_id):
        try:

            livro = self.livro_dao.buscar_por_id(id)
            if not livro:
                raise ValidationException("Livro não encontrado")


            bibliotecario = self.usuario_dao.buscar_por_id(bibliotecario_id)
            if not bibliotecario:
                raise ValidationException("Bibliotecário não encontrado")

            if bibliotecario.tipo != "BIBLIOTECARIO":
                raise ValidationException("Apenas bibliotecários podem remover livros")

            return self.livro_dao.remover(id)
        except ValidationException as e:
            raise e
        except Exception as e:
            raise ValidationException(f"Erro ao remover livro: {str(e)}")

    def buscar_livro_por_id(self, id):
        try:
            return self.livro_dao.buscar_por_id(id)
        except Exception as e:
            raise ValidationException(f"Erro ao buscar livro: {str(e)}")

    def buscar_livros_por_titulo(self, titulo):
        try:
            return self.livro_dao.buscar_por_titulo(titulo)
        except Exception as e:
            raise ValidationException(f"Erro ao buscar livros por título: {str(e)}")

    def listar_todos_livros(self):
        try:
            return self.livro_dao.listar_todos()
        except Exception as e:
            raise ValidationException(f"Erro ao listar livros: {str(e)}")

    def marcar_como_indisponivel(self, id):
        try:
            livro = self.livro_dao.buscar_por_id(id)
            if not livro:
                raise ValidationException("Livro não encontrado")

            livro.status = "INDISPONIVEL"
            return self.livro_dao.atualizar(livro)
        except ValidationException as e:
            raise e
        except Exception as e:
            raise ValidationException(f"Erro ao marcar livro como indisponível: {str(e)}")

    def marcar_como_disponivel(self, id):
        try:
            livro = self.livro_dao.buscar_por_id(id)
            if not livro:
                raise ValidationException("Livro não encontrado")

            livro.status = "DISPONIVEL"
            return self.livro_dao.atualizar(livro)
        except ValidationException as e:
            raise e
        except Exception as e:
            raise ValidationException(f"Erro ao marcar livro como disponível: {str(e)}")



from biblioteca.core.excecoes.validacao_excecoes import (ValidationException, LivroInvalidoException, PersistenciaException)


class TelaLivro:
    def __init__(self, livro_service, usuario_service):
        self.livro_service = livro_service
        self.usuario_service = usuario_service
        self.bibliotecario_atual_id = None

    def definir_bibliotecario(self, bibliotecario_id):
        self.bibliotecario_atual_id = bibliotecario_id

    def exibir_menu(self):
        print("\n=== GERENCIAMENTO DE LIVROS ===")
        print("1. Adicionar novo livro")
        print("2. Atualizar livro")
        print("3. Remover livro")
        print("4. Buscar livro por ID")
        print("5. Buscar livros por título")
        print("6. Listar todos os livros")
        print("7. Marcar livro como indisponível")
        print("8. Marcar livro como disponível")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ")
        return opcao

    def adicionar_livro(self):
        if not self.verificar_bibliotecario():
            return

        print("\n=== ADICIONAR NOVO LIVRO ===")
        titulo = input("Título: ")
        autor = input("Autor: ")
        isbn = input("ISBN (10 ou 13 dígitos): ")
        ano_publicacao = input("Ano de publicação: ")
        editora = input("Editora: ")
        quantidade_disponivel = input("Quantidade disponível: ")

        try:
            livro = self.livro_service.adicionar_livro(
                titulo, autor, isbn, ano_publicacao, editora,
                quantidade_disponivel, self.bibliotecario_atual_id
            )
            print(f"\nLivro adicionado com sucesso! ID: {livro.id}")
        except (LivroInvalidoException, ValidationException, PersistenciaException) as e:
            self.tratar_excecao(e)

    def atualizar_livro(self):
        if not self.verificar_bibliotecario():
            return

        print("\n=== ATUALIZAR LIVRO ===")
        try:
            id = int(input("ID do livro: "))
            livro = self.livro_service.buscar_livro_por_id(id)

            if not livro:
                print("Livro não encontrado!")
                return

            print(f"Livro atual: {livro}")
            print("\nDigite os novos dados (ou deixe em branco para manter os valores atuais):")

            titulo = input(f"Título [{livro.titulo}]: ") or livro.titulo
            autor = input(f"Autor [{livro.autor}]: ") or livro.autor
            isbn = input(f"ISBN [{livro.isbn}]: ") or livro.isbn
            ano_publicacao = input(f"Ano de publicação [{livro.ano_publicacao}]: ") or livro.ano_publicacao
            editora = input(f"Editora [{livro.editora}]: ") or livro.editora
            quantidade_disponivel = input(f"Quantidade disponível [{livro.quantidade_disponivel}]: ") or livro.quantidade_disponivel

            self.livro_service.atualizar_livro(
                id, titulo, autor, isbn, ano_publicacao, editora,
                quantidade_disponivel, self.bibliotecario_atual_id
            )
            print("\nLivro atualizado com sucesso!")
        except ValueError:
            print("\nErro: ID deve ser um número inteiro")
        except (LivroInvalidoException, ValidationException, PersistenciaException) as e:
            self.tratar_excecao(e)

    def remover_livro(self):
        if not self.verificar_bibliotecario():
            return

        print("\n=== REMOVER LIVRO ===")
        try:
            id = int(input("ID do livro: "))

            livro = self.livro_service.buscar_livro_por_id(id)
            if not livro:
                print("Livro não encontrado!")
                return

            confirmacao = input(f"Tem certeza que deseja remover o livro '{livro.titulo}'? (s/n): ")
            if confirmacao.lower() == 's':
                self.livro_service.remover_livro(id, self.bibliotecario_atual_id)
                print("\nLivro removido com sucesso!")
            else:
                print("\nOperação cancelada.")
        except ValueError:
            print("\nErro: ID deve ser um número inteiro")
        except ValidationException as e:
            self.tratar_excecao(e)

    def buscar_livro_por_id(self):
        print("\n=== BUSCAR LIVRO POR ID ===")
        try:
            id = int(input("ID do livro: "))
            livro = self.livro_service.buscar_livro_por_id(id)

            if livro:
                print("\nLivro encontrado:")
                print(livro)
            else:
                print("Livro não encontrado!")
        except ValueError:
            print("\nErro: ID deve ser um número inteiro")
        except ValidationException as e:
            self.tratar_excecao(e)

    def buscar_livros_por_titulo(self):
        print("\n=== BUSCAR LIVROS POR TÍTULO ===")
        titulo = input("Digite parte do título: ")

        try:
            livros = self.livro_service.buscar_livros_por_titulo(titulo)

            if livros:
                print(f"\nForam encontrados {len(livros)} livros:")
                for livro in livros:
                    print(livro)
            else:
                print("Nenhum livro encontrado com esse título!")
        except ValidationException as e:
            self.tratar_excecao(e)

    def listar_livros(self):
        print("\n=== LISTA DE LIVROS ===")
        try:
            livros = self.livro_service.listar_todos_livros()

            if not livros:
                print("Nenhum livro cadastrado.")
                return

            for livro in livros:
                print(livro)
        except ValidationException as e:
            self.tratar_excecao(e)

    def marcar_como_indisponivel(self):
        if not self.verificar_bibliotecario():
            return

        print("\n=== MARCAR LIVRO COMO INDISPONÍVEL ===")
        try:
            id = int(input("ID do livro: "))
            self.livro_service.marcar_como_indisponivel(id)
            print("\nLivro marcado como indisponível com sucesso!")
        except ValueError:
            print("\nErro: ID deve ser um número inteiro")
        except ValidationException as e:
            self.tratar_excecao(e)

    def marcar_como_disponivel(self):
        if not self.verificar_bibliotecario():
            return

        print("\n=== MARCAR LIVRO COMO DISPONÍVEL ===")
        try:
            id = int(input("ID do livro: "))
            self.livro_service.marcar_como_disponivel(id)
            print("\nLivro marcado como disponível com sucesso!")
        except ValueError:
            print("\nErro: ID deve ser um número inteiro")
        except ValidationException as e:
            self.tratar_excecao(e)

    def verificar_bibliotecario(self):
        if not self.bibliotecario_atual_id:
            print("\nAtenção: É necessário estar logado como bibliotecário para realizar esta operação.")
            return False


        usuario = self.usuario_service.buscar_usuario_por_id(self.bibliotecario_atual_id)
        if not usuario or usuario.tipo != "BIBLIOTECARIO":
            print("\nApenas bibliotecários podem realizar esta operação.")
            return False

        return True

    def tratar_excecao(self, e):
        if isinstance(e, LivroInvalidoException):
            print(f"\nErro de validação do livro: {e}")
        elif isinstance(e, PersistenciaException):
            print(f"\nErro de persistência: {e}")
        elif isinstance(e, ValidationException):
            print(f"\nErro de validação: {e}")
        else:
            print(f"\nErro: {e}")



def buscar_usuario_por_id(self, id):
    """Novo método para buscar usuário por ID"""
    try:
        return self.usuario_dao.buscar_por_id(id)
    except Exception as e:
        raise ValidationException(f"Erro ao buscar usuário: {str(e)}")



class BibliotecaFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BibliotecaFacade, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if not self._inicializado:
            from biblioteca.servicos.usuario_service import UsuarioService
            from biblioteca.servicos.livro_service import LivroService

            self.usuario_service = UsuarioService()
            self.livro_service = LivroService()
            self._inicializado = True
            self.usuario_logado = None


    def adicionar_usuario(self, login, senha, nome, email, tipo="REGULAR"):
        return self.usuario_service.adicionar_usuario(login, senha, nome, email, tipo)

    def bloquear_usuario(self, id):
        return self.usuario_service.bloquear_usuario(id)

    def desbloquear_usuario(self, id):
        return self.usuario_service.desbloquear_usuario(id)

    def listar_todos_usuarios(self):
        return self.usuario_service.listar_todos