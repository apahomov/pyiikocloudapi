from typing import List, Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.exception import TokenException, ParamSetException
from pyiikocloudapi.models import (
    CustomErrorModel,
    BaseTerminalGroupsModel,
    BaseTGIsAliveyModel,
)


class TerminalGroup(BaseAPI):
    def terminal_groups(self, organization_ids: List[str], include_disabled: bool = False,
                        timeout=BaseAPI.DEFAULT_TIMEOUT) -> Union[CustomErrorModel,
    BaseTerminalGroupsModel]:
        """

        :param organization_ids: 	Array of strings <uuid>, Organizations IDs for which information is requested.
        :param include_disabled:
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.terminal_groups.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
        }
        if include_disabled:
            data["includeDisabled"] = include_disabled
        try:

            return self._post_request(
                url="/api/1/terminal_groups",
                data=data,
                model_response_data=BaseTerminalGroupsModel,
                timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.terminal_groups.__name__,
                                 f"Не удалось получить регионы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.terminal_groups.__name__,
                            f"Не удалось получить регионы: \n{err}")

    def is_alive(self, organization_ids: List[str], terminal_group_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT) -> \
        Union[CustomErrorModel,
        BaseTGIsAliveyModel]:
        """

        :param terminal_group_ids:
        :param organization_ids: 	Array of strings <uuid>, Organizations IDs for which information is requested.
        :return:
        """
        if not bool(organization_ids):
            raise ParamSetException(self.__class__.__qualname__,
                                    self.is_alive.__name__,
                                    f"Пустой список id организаций")
        data = {
            "organizationIds": organization_ids,
            "terminalGroupIds": terminal_group_ids
        }

        try:

            return self._post_request(
                url="/api/1/terminal_groups/is_alive",
                data=data,
                model_response_data=BaseTGIsAliveyModel,
                timeout=timeout
            )
        except httpx.HTTPError as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.is_alive.__name__,
                                 f"Не удалось получить регионы: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.is_alive.__name__,
                            f"Не удалось получить регионы: \n{err}")
