# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from config import wallet as wallet_conf
from mg.forms import OfficialMTTEventForm
from pokerclub_friends.models import FriendsGroup, Alliance


class SatelliteEventFrom(OfficialMTTEventForm):
    """mg后台创建卫星赛参数校验"""

    wallet_type = forms.IntegerField(label=u"钱包类型", required=True)
    sponsor_id = forms.IntegerField(label=u'赞助人id', required=True)
    prize_guranteed = forms.FloatField(label=u'赛事保证金', required=True, min_value=100.00)

    def clean_sponsor_id(self):
        """
            判断俱乐部或者联盟是否存在
        """
        wallet_type = self.cleaned_data.get("wallet_type")
        sponsor_id = self.cleaned_data.get("sponsor_id")
        if wallet_type == wallet_conf.SATELLITE_GROUP_WALLET_TYPE:
            if not FriendsGroup.get_group_by_id(sponsor_id):
                raise ValidationError("The club does not exist")
            else:
                return sponsor_id
        elif wallet_type == wallet_conf.SATELLITE_ALLIANCE_WALLET_TYPE:
            if not Alliance.get_alliance_by_alliance_id(sponsor_id):
                raise ValidationError("The alliance does not exist")
            else:
                return sponsor_id
        else:
            raise ValidationError("The wallet type does not exist")

    def clean_wallet_type(self):
        """
            判断钱包类型
        """
        wallet_type = self.cleaned_data.get("wallet_type", None)
        if wallet_type not in [wallet_conf.SATELLITE_GROUP_WALLET_TYPE, wallet_conf.SATELLITE_ALLIANCE_WALLET_TYPE]:
            raise ValidationError("The wallet type does not exist")
        return wallet_type


class CreateGroupFlowRecordForm(forms.Form):
    """修改保证金参数校验"""

    amount = forms.IntegerField(label=u'流水金额', required=True)
    reason = forms.CharField(label=u'流水金额', required=True)
    event_name = forms.CharField(label=u'流水金额', required=True)
    source = forms.CharField(label=u'统计流水扣除和回退是否为同一笔', required=True)

    def clean_amount(self):
        amount = int(self.cleaned_data.get("amount", 0))
        if amount == 0:
            raise ValidationError("The amount does not zero")


class CheckGroupFlowRecordForm(forms.Form):
    """根据交易单号查询交易"""
    source = forms.CharField(label=u'统计流水扣除和回退是否为同一笔', required=True)
