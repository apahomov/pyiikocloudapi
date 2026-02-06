from typing import Union

import httpx

from pyiikocloudapi.async_base import AsyncBaseAPI
from pyiikocloudapi.exception import TokenException
from pyiikocloudapi.models import BaseStatusModel, CustomErrorModel


class AsyncCommands(AsyncBaseAPI):
    async def status(
        self, organization_id: str, correlation_id: str, timeout=AsyncBaseAPI.DEFAULT_TIMEOUT
    ) -> Union[
        BaseStatusModel,
        CustomErrorModel,
    ]:
        """


        :param organization_id:
        :param correlation_id:
        :param timeout:
        :return:
        """
        data = {
            "organizationId": organization_id,
            "correlationId": correlation_id,
        }

        try:
            return await self._post_request(
                url="/api/1/commands/status", data=data, model_response_data=BaseStatusModel, timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(
                self.__class__.__qualname__, self.status.__name__, f"Не удалось получить статус: \n{err}"
            )
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__, self.status.__name__, f"Не удалось получить статус: \n{err}")
