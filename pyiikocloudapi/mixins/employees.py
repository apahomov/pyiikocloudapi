from typing import List, Optional, Union

import httpx

from pyiikocloudapi.base import BaseAPI
from pyiikocloudapi.decorators import experimental
from pyiikocloudapi.exception import PostException
from pyiikocloudapi.models import (
    CouriersModel,
    BaseEInfoModel,
    ErrorModel,
    EmployeeModel,
    EmployeeTerminalModel,
    CustomErrorModel,
)


class Employees(BaseAPI):

    def couriers(self, organization_ids: List[str], timeout=BaseAPI.DEFAULT_TIMEOUT):

        #     https://api-ru.iiko.services/api/1/employees/couriers
        data = {
            "organizationIds": organization_ids,
        }

        try:

            return self._post_request(
                url="/api/1/employees/couriers",
                data=data,
                model_response_data=CouriersModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось получить курьеров: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.couriers.__name__,
                                f"Не удалось: \n{err}")

    @experimental
    def employees_couriers_locations_by_time_offset(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_by_role(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_active_location_by_terminal(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    @experimental
    def employees_couriers_active_location(self, timeout=BaseAPI.DEFAULT_TIMEOUT):
        pass

    def employees_info(self, organization_id: str, id: str, timeout=BaseAPI.DEFAULT_TIMEOUT):
        data = {
            "organizationId": organization_id,
            "id": id
        }

        try:

            return self._post_request(
                url="/api/1/employees/info",
                data=data,
                model_response_data=BaseEInfoModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_info.__name__,
                                f"Не удалось получить информацию о сотруднике: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_info.__name__,
                                f"Не удалось: \n{err}")

    def employees_shift_clockin(self, organization_id: str, terminal_group_id: str, employee_id: str,
                                role_id: Optional[str] = None, timeout=BaseAPI.DEFAULT_TIMEOUT):
        """
        Open personal session.
        This method is a command. Use api/1/commands/status method to get the progress status.
        Restriction group: Employees: shifts.

        :param organization_id: Can be obtained by /api/1/organizations
        :param terminal_group_id: Can be obtained by /api/1/terminal_groups
        :param employee_id: Employee ID.
        :param role_id: Must be null if the restaurant doesn't use roles, otherwise not-null role must be specified.
        :param timeout:
        :return:
        """
        data = {
            "organizationId": organization_id,
            'terminalGroupId': terminal_group_id,
            'employeeId': employee_id,
        }
        if role_id is not None: data["roleId"] = role_id
        try:

            return self._post_request(
                url="/api/1/employees/shift/clockin",
                data=data,
                model_response_data=ErrorModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_clockin.__name__,
                                f"Не удалось открыть персональную сессию: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_clockin.__name__,
                                f"Не удалось: \n{err}")

    def employees_shift_clockout(self, organization_id: str, terminal_group_id: str, employee_id: str,
                                 timeout=BaseAPI.DEFAULT_TIMEOUT):
        """
        Close personal session.
        This method is a command. Use api/1/commands/status method to get the progress status.
        Restriction group: Employees: shifts.

        :param organization_id: Can be obtained by /api/1/organizations
        :param terminal_group_id: Can be obtained by /api/1/terminal_groups
        :param employee_id: Employee ID.
        :param timeout:
        :return: ErrorModel || CustomErrorModel
        """
        data = {
            "organizationId": organization_id,
            'terminalGroupId': terminal_group_id,
            'employeeId': employee_id,
        }
        try:

            return self._post_request(
                url="/api/1/employees/shift/clockout",
                data=data,
                model_response_data=ErrorModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_clockout.__name__,
                                f"Не удалось закрыть персональную сессию: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_clockout.__name__,
                                f"Не удалось: \n{err}")

    def employees_shift_is_open(self, organization_id: str, terminal_group_id: str, employee_id: str,
                                timeout=BaseAPI.DEFAULT_TIMEOUT):
        """
        Check if personal session is open.

        :param organization_id: Can be obtained by /api/1/organizations
        :param terminal_group_id: Can be obtained by /api/1/terminal_groups
        :param employee_id: Employee ID.
        :param timeout: EmployeeModel or CustomErrorModel
        :return:
        """
        data = {
            "organizationId": organization_id,
            'terminalGroupId': terminal_group_id,
            'employeeId': employee_id,
        }
        try:

            return self._post_request(
                url="/api/1/employees/shift/is_open",
                data=data,
                model_response_data=EmployeeModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_is_open.__name__,
                                f"Не удалось проверить, открыта ли персональная сессия: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_is_open.__name__,
                                f"Не удалось: \n{err}")

    def employees_shift_by_courier(self, employee_id: str, timeout=BaseAPI.DEFAULT_TIMEOUT):
        """
        Get terminal groups where employee session is opened.

        :param employee_id:
        :param timeout:
        :return: EmployeeTerminalModel or CustomErrorModel
        """
        data = {
            'employeeId': employee_id,
        }
        try:

            return self._post_request(
                url="/api/1/employees/shift/by_courier",
                data=data,
                model_response_data=EmployeeTerminalModel,
                timeout=timeout
            )

        except httpx.HTTPError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_by_courier.__name__,
                                f"Не удалось получить список групп терминалов, в которых открыт сеанс сотрудника: \n{err}")
        except TypeError as err:
            raise PostException(self.__class__.__qualname__,
                                self.employees_shift_by_courier.__name__,
                                f"Не удалось: \n{err}")
