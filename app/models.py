from django.db import models
import uuid
from datetime import datetime

class SessionLevel(models.Model):
    """
    Table to Keeping track of sessions
    """
    session_id = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=10)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.session_id + " at Level" + str(self.level)

class BankUser(models.Model):
    """
    Table of bank users
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=30)
    registered_data = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    """
    Table of bank accounts
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    bankUser = models.OneToOneField(BankUser, on_delete = models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.balance) + " " + str(self.bankUser)

class BankTransaction(models.Model):
    """
    Table of transactions made
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    From = models.ForeignKey(BankUser, on_delete=models.CASCADE)
    To = models.CharField(max_length=30)
    Amount = models.IntegerField()

    def __str__(self):
        return str(self.Amount)

