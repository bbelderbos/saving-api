from enum import Enum

from tortoise.models import Model
from tortoise import fields


class User(Model):
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)  # TODO: encryption
    added = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Goal(Model):
    description = fields.CharField(max_length=255)
    amount = fields.FloatField()
    user = fields.ForeignKeyField('models.User', related_name='user',
                                  on_delete=fields.SET_NULL)
    achieved = fields.BooleanField(default=False)
    added = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.user})"


class TransactionType(Enum):
    SAVING = 1
    DONATION = 2
    WITHDRAWAL = 3
    OTHER = 4


class Transaction(Model):
    amount = fields.FloatField()
    transation_type = fields.CharEnumField(TransactionType)
    goal = fields.ForeignKeyField('models.Goal', related_name='goal',
                                  on_delete=fields.SET_NULL)
    concept = fields.CharField(max_length=255, null=True)
    added = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} ({self.transation_type})"
