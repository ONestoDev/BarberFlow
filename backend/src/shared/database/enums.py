import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    BARBER = "BARBER"
    CUSTOMER = "CUSTOMER"


class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    PIX = "PIX"
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"


class FinancialTransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class FinancialOriginType(str, enum.Enum):
    APPOINTMENT = "APPOINTMENT"
    SALE = "SALE"
    EXPENSE = "EXPENSE"
    ADJUSTMENT = "ADJUSTMENT"
