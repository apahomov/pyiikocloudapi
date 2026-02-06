from pyiikocloudapi.base import BaseAPI  # noqa: F401

# Backward compatibility re-exports
from pyiikocloudapi.mixins import *  # noqa: F403
from pyiikocloudapi.mixins import (
    Address,
    Commands,
    Customers,
    Deliveries,
    DeliveryRestrictions,
    Dictionaries,
    DiscountPromotion,
    Employees,
    Menu,
    Notifications,
    Orders,
    TerminalGroup,
    WebHook,
)


# Preserve MRO order from original code
class IikoTransport(
    Orders,
    Deliveries,
    Employees,
    Address,
    DeliveryRestrictions,
    TerminalGroup,
    Menu,
    Dictionaries,
    DiscountPromotion,
    Commands,
    Notifications,
    Customers,
    WebHook,
):
    pass
