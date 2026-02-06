from pyiikocloudapi.base import BaseAPI  # noqa: F401
from pyiikocloudapi.mixins import (
    WebHook,
    Commands,
    Dictionaries,
    DiscountPromotion,
    Menu,
    TerminalGroup,
    Address,
    DeliveryRestrictions,
    Orders,
    Deliveries,
    Notifications,
    Employees,
    Customers,
)

# Backward compatibility re-exports
from pyiikocloudapi.mixins import *  # noqa: F401, F403


# Preserve MRO order from original code
class IikoTransport(Orders, Deliveries, Employees, Address, DeliveryRestrictions,
                     TerminalGroup, Menu, Dictionaries, DiscountPromotion, Commands,
                     Notifications, Customers, WebHook):
    pass
