from typing import Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.exception import PostException
from pyiikocloudapi.models import BaseResponseModel, CustomErrorModel


class AsyncNotifications(AsyncBaseAPI):
    async def send(self, order_source: str, order_id: str, additional_info: str, organization_id: str,
                   message_type: str = "delivery_attention", timeout=AsyncBaseAPI.DEFAULT_TIMEOUT):
        """

        :param order_source:
        :param order_id:
        :param additional_info:
        :param organization_id:
        :param message_type:
        :return:
        """
        data = {
            "orderSource": order_source,
            "orderId": order_id,
            "additionalInfo": additional_info,
            "messageType": message_type,
            "organizationId": organization_id,

        }

        try:

            return await self._post_request(
                url="/api/1/notifications/send",
                data=data,
                model_response_data=BaseResponseModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.send.__name__,
                                f"Не удалось отправить оповещение: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.send.__name__,
                                f"Не удалось: \n{err}")
