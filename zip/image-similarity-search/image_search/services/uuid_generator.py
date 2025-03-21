from typing import Annotated
from uuid import uuid4

from fastapi import Depends


class UUIDGenerator:
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid4())


UUIDGeneratorDep = Annotated[UUIDGenerator, Depends(UUIDGenerator)]
