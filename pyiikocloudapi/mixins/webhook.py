from typing import List

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.models import WebHookDeliveryOrderEventInfoModel


class WebHook(BaseAPI):
    @staticmethod
    def parse_webhook_order(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        return [WebHookDeliveryOrderEventInfoModel.model_validate(order_info) for order_info in data]

    @staticmethod
    def parse_webhook_reserve(data: List[dict]) -> List[WebHookDeliveryOrderEventInfoModel]:
        raise NotImplementedError('parse_webhook_reserve is not yet implemented')
