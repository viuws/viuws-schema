from enum import Enum
from typing import Literal, Optional, Union

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class Address(str, Enum):
    WEBPAGE = "webpage"
    CONTENT_SCRIPT = "contentScript"
    SERVICE_WORKER = "serviceWorker"
    NATIVE_HOST = "nativeHost"


class Header(SchemaBaseModel):
    id: int
    source: Address
    target: Address
    source_webpage: Optional[int] = Field(default=None, alias="sourceWebpage")
    target_webpage: Optional[int] = Field(default=None, alias="targetWebpage")


class PayloadType(str, Enum):
    PING_REQUEST = "pingRequest"
    PING_RESPONSE = "pingResponse"


class PayloadBase(SchemaBaseModel):
    type: PayloadType


class RequestPayloadBase(SchemaBaseModel):
    pass


class ResponsePayloadBase(SchemaBaseModel):
    request_id: int = Field(alias="requestId")


class PingRequestPayload(RequestPayloadBase):
    type: Literal[PayloadType.PING_REQUEST] = PayloadType.PING_REQUEST


class PingResponsePayload(ResponsePayloadBase):
    type: Literal[PayloadType.PING_RESPONSE] = PayloadType.PING_RESPONSE
    ok: bool
    error: Optional[str] = None


class Message(RootSchemaBaseModelV01):
    header: Header
    payload: Union[PingRequestPayload, PingResponsePayload] = Field(
        discriminator="type"
    )
