from tortoise import fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = "users"

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32)
    hash_password = fields.CharField(max_length=128)
