import typing as t
import numpy
from koifish.schemas import DeDBRef
from koifish.schemas.base import BaseSchema, BaseSchemaId


class StartRedis(BaseSchema):
    name: t.Optional[str] = None


class DataRedis(BaseSchema):
    averaged_A: t.Optional[list] = []
    averaged_B: t.Optional[list] = []
    averaged_C: t.Optional[list] = []

    averaged_X: t.Optional[list] = []
    averaged_Y: t.Optional[list] = []
    fish_name: t.Optional[list] = []

    heatmap_data: t.Optional[list] = []
    xedges: t.Optional[list] = []
    yedges: t.Optional[list] = []

    image: t.Optional[str] = ""
    image_scatter: t.Optional[str] = ""
