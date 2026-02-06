from typing import List

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.models import WebHookDeliveryOrderEventInfoModel


class AsyncWebHook(AsyncBaseAPI):
    @staticmethod
    def parse_webhook_order(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        return [WebHookDeliveryOrderEventInfoModel.model_validate(order_info) for order_info in data]

    @staticmethod
    def parse_webhook_reserve(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        raise NotImplementedError('parse_webhook_reserve is not yet implemented')
