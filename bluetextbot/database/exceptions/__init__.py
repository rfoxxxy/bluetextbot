from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegistrationError(Exception):
    message: str


@dataclass(frozen=True, slots=True)
class NotFoundError(Exception):
    message: str


@dataclass(frozen=True, slots=True)
class NotEnoughError(Exception):
    message: str
