class TrinketError(Exception):
    """Базовое исключение для всех ошибок, связанных с Trinket."""

    pass


class LoginError(TrinketError):
    """Исключение, вызываемое при ошибке входа в систему."""

    pass


class NavigationError(TrinketError):
    """Исключение, вызываемое при ошибке навигации."""

    pass


class TrinketCreationError(TrinketError):
    """Исключение, вызываемое при ошибке создания Trinket."""

    pass


class TrinketVerificationError(TrinketError):
    """Исключение, вызываемое при ошибке проверки созданного Trinket."""

    pass


class TrinketUpdateError(TrinketError):
    """Исключение, вызываемое при ошибке обновления Trinket."""

    pass
