from bson import ObjectId, DBRef
from bson.errors import InvalidId
import typing as t

from pydantic_core import CoreSchema, core_schema
from pydantic_core.core_schema import ValidationInfo, str_schema
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic.main import _model_construction

from mongoengine import Document, ImageGridFsProxy, GridFSProxy
from mongoengine.base.metaclasses import TopLevelDocumentMetaclass

from koifish.api.core.exceptions import ValidationError

# from mongoengine.base.common import _get_documents_by_db
from koifish.models import cls_documents

__all__ = ("AllOptional", "PydanticObjectId", "DeDBRef")

T = t.TypeVar("T")


class AllOptional(_model_construction.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = t.Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class PydanticObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: t.Any, _handler: t.Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)


class DeDBRef(t.Generic[T]):
    """Dereference DBRef bson object to a schema

    Usage:
    .. code-block:: python
        from user_schema import User

        user: DeDBRef[User] = Field(json_schema_extra="user_field")"""

    def __init__(self, document_class: BaseModel):
        self.document_class = document_class

    @classmethod
    def build_validation(cls, handler, source_type):
        def validate(v: DBRef | T, validation_info: core_schema.ValidationInfo):
            document_class: BaseModel = t.get_args(source_type)[0]

            if isinstance(
                v, (dict, BaseModel, ImageGridFsProxy, GridFSProxy, ObjectId)
            ):
                return v

            if isinstance(v, Document):
                return document_class(**v.to_mongo())

            if isinstance(v, DBRef):
                for doc in cls_documents:
                    if isinstance(doc, TopLevelDocumentMetaclass):
                        if doc._get_collection_name() == v.collection:
                            try:
                                return document_class(
                                    **doc.objects.with_id(v.id).to_mongo()
                                )
                            except Exception as e:
                                print(e)
                                raise ValidationError("Could not validate DBRef object")
            return None

        return validate

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(
                cls.build_validation(handler, source_type)
            ),
            json_schema=core_schema.typed_dict_schema(
                {"attr": core_schema.typed_dict_field(core_schema.str_schema())}
            ),
        )
