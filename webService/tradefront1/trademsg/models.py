# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



OT_CHOICES = (
    ("SL","SL"),
    ("Limit","Limit"),

)
class TradeMessage(models.Model):
    date_time = models.DateTimeField(db_column='Date_time')  # Field name made lowercase.
    script = models.CharField(max_length=150)
    close_price = models.FloatField()
    trade_pos = models.CharField(max_length=50)
    entry_price = models.FloatField()
    sl = models.FloatField(db_column='SL')  # Field name made lowercase.
    i_target_price = models.FloatField(db_column='I_target_price')  # Field name made lowercase.
    i_target_exit = models.FloatField(db_column='I_target_exit')  # Field name made lowercase.
    i_target_pl = models.FloatField(db_column='I_target_PL')  # Field name made lowercase.
    ii_target_price = models.FloatField(db_column='II_target_price')  # Field name made lowercase.
    ii_target_exit = models.FloatField(db_column='II_target_exit')  # Field name made lowercase.
    ii_target_pl = models.FloatField(db_column='II_target_PL')  # Field name made lowercase.
    trailing_exit = models.FloatField()
    trailing_float = models.FloatField()
    share_float = models.FloatField()

    class Meta:
        managed = True
        db_table = 'trade_message'


class APIINFO(models.Model):
    no = models.IntegerField()
    api_key = models.CharField(max_length=250,default="l5x8ay13aegnq946")
    api_token = models.CharField(max_length=250)
    dattime = models.DateTimeField()
    order_type = models.CharField(max_length=50,choices=OT_CHOICES,default="SL")
    script_exposure = models.IntegerField(default=1)
    cushion_price = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'trade_apiinfo'


class TradeMessageHFloat(models.Model):
    date_time = models.DateTimeField(db_column='Date_time')  # Field name made lowercase.
    script = models.CharField(max_length=150)
    close_price = models.FloatField()
    trade_pos = models.CharField(max_length=50)
    entry_price = models.FloatField()
    sl = models.FloatField(db_column='SL')  # Field name made lowercase.
    i_target_price = models.FloatField(db_column='I_target_price')  # Field name made lowercase.
    i_target_exit = models.FloatField(db_column='I_target_exit')  # Field name made lowercase.
    i_target_pl = models.FloatField(db_column='I_target_PL')  # Field name made lowercase.
    ii_target_price = models.FloatField(db_column='II_target_price')  # Field name made lowercase.
    ii_target_exit = models.FloatField(db_column='II_target_exit')  # Field name made lowercase.
    ii_target_pl = models.FloatField(db_column='II_target_PL')  # Field name made lowercase.
    trailing_exit = models.FloatField()
    trailing_float = models.FloatField()
    share_float = models.FloatField()

    class Meta:
        managed = True
        db_table = 'trade_messageHFloat'
