# app/repositories/base_repository.py

from typing import Generic, TypeVar, Type, List, Optional
from sqlmodel import SQLModel, Session, select

# --- Tipos Genéricos ---
# Isso é o equivalente ao <T, ID> do JpaRepository
# Dizemos ao Python que vamos receber um tipo de Modelo (ex: User)
# e um tipo de Schema (ex: UserCreate)
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Repositório base genérico com operações CRUD.
    Equivalente ao JpaRepository<T, ID> do Spring Data.
    """
    def __init__(self, model: Type[ModelType]):
        """
        O construtor recebe o modelo (ex: User) 
        com o qual o repositório vai trabalhar.
        """
        self.model = model

    def get(self, session: Session, id: int) -> Optional[ModelType]:
        """Equivalente ao findById(id)"""
        # session.get() é otimizado para buscar pela Chave Primária
        return session.get(self.model, id)

    def get_all(self, session: Session) -> List[ModelType]:
        """Equivalente ao findAll()"""
        return session.exec(select(self.model)).all()

    def create(self, session: Session, obj_in: CreateSchemaType) -> ModelType:
        """Equivalente ao save(entity) para uma nova entidade"""
        # Converte o DTO (Schema) para o Modelo (Entidade)
        # model_validate é como o 'new User(userDto)'
        db_obj = self.model.model_validate(obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self, session: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Equivalente ao save(entity) para uma entidade existente"""
        
        # Pega os dados do DTO de atualização
        # exclude_unset=True garante que só atualizemos os campos
        # que foram realmente enviados (bom para 'PATCH')
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        # Atualiza o objeto do banco (db_obj) com os dados do DTO (obj_data)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, id: int) -> bool:
        """Equivalente ao deleteById(id)"""
        db_obj = session.get(self.model, id)
        if db_obj is None:
            return False # Não encontrou, falha ao deletar
        
        session.delete(db_obj)
        session.commit()
        return True # Sucesso