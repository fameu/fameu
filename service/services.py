# -*- coding: utf-8 -*-
import json

from django.db import transaction

import config
import config.messages
import config.payment
import config.wallet
from config import wallet as wallet_conf
from config.lang import lang_idx, trans_lang
from config.payment import MASTER_DB_NAME
from pokerclub_friends.models import FriendsGroup
from pokerclub_master.models import MasterGroupReward, MasterWalletMsg, MasterGroupWalletLog, GroupFlowMarginRecord
from pokerclub_userinfo.models import PlayerActivityReport
from share.date_utils import get_cur_timestamp
from share.game.game_api import GameRequestApi
from share.json_extend import json_compact_encode
from share.log import logger
from share.num_trans import NumTrans
from share.utils import get_default_format_time, safe_call

alter_wallet_plugins = {}


def filter_satellite_event(event_list):
    """
    筛选卫星赛
    """
    return filter(lambda event: event.get("is_weixingsai"), event_list)


def get_wallet_params(form_data, event_data):
    """
    获取扣除保证金参数
    """
    wallet_params = {
        "sponsor_id": form_data.get("sponsor_id"),
        "amount": -float(form_data.get('prize_guranteed')),  # 扣除的保证金
        "reason": lang_idx.IDX_WALLET_INVOICE_TITLE_SATELLITE,
        "source": form_data.get('source'),
        "event_name": event_data.get("event_name"),
    }
    return wallet_params


def register_alter_wallet_plugins(name, wallet_plugins):
    alter_wallet_plugins[name] = {
        "alter_wallet_plugins": wallet_plugins
    }


def get_alter_wallet_plugins():
    return alter_wallet_plugins


def manual_alter_alliance_balance(sponsor_id, amount, reason, source, event_name):
    """
    修改联盟钱包金额
    :param sponsor_id:  联盟id
    :param amount:  修改联盟钱包金额
    :param reason:  原因
    :param source:  唯一标识统计流水扣除和回退是否为同一笔
    :param event_name:  赛事名称
    :return:
    """
    return dict(ret=0, error_msg="The alliance wallet does not exist")


def manual_alter_group_balance(sponsor_id, amount, reason, source, event_name):
    """
    修改俱乐部钱包金额
    :param sponsor_id:  俱乐部id
    :param amount:  修改俱乐部钱包金额
    :param reason:  原因
    :param source:  唯一标识统计流水扣除和回退是否为同一笔
    :param event_name:  赛事名称
    :return:
    """
    from share.utils import format_crm_group_wallet_operator

    uid = FriendsGroup.get_admin(sponsor_id)

    logger.info("satellite modify group amount. uid: %s, gid: %s, gold: %s", uid, sponsor_id, amount)

    group_money = MasterGroupReward.get_group_money(sponsor_id)

    if amount < 0 and abs(amount) > float(group_money):
        gname = FriendsGroup.objects.get(gid=sponsor_id).gname
        return False, "The club wallet balance of {} - {} is insufficient, please try again.".format(sponsor_id, gname)

    # 注册一下,避免用户没有登陆,没有在游戏那边生成记录,那边查不到记录金币修改不成功
    GameRequestApi.reg_user(dict(uid=uid))

    try:
        with transaction.atomic(MASTER_DB_NAME):

            rst, reward_info = MasterGroupReward.update_remoney(uid, sponsor_id, amount)
            if rst == 0:
                balance_after = reward_info.remoney
            else:
                return False, reward_info

            # 写钱包记录
            utime = get_cur_timestamp()
            extends = [
                (lang_idx.IDX_WALLET_DETAIL_KEY_MODIFIED_TIME, get_default_format_time(utime)),
                (lang_idx.IDX_WALLET_DETAIL_KEY_OFFICIAL_SYS, ''),
                (lang_idx.IDX_MTT_WALLET_MARGIN_NAME_EVENT, event_name),
                (lang_idx.IDX_WALLET_DETAIL_KEY_GROUP_WALLET_OPERATOR, format_crm_group_wallet_operator(uid)),
            ]
            _, record_model = MasterGroupWalletLog.insert_group_wallet_record(
                gid=sponsor_id,
                uid=uid,
                title=lang_idx.IDX_WALLET_INVOICE_TITLE_SATELLITE,
                invoice_title=lang_idx.IDX_WALLET_INVOICE_TITLE_SATELLITE,
                amount=NumTrans.multiply_100(amount),
                remain_money=balance_after,
                tag=wallet_conf.PERSONAL_WALLET_TAG_SYS_MODIFIED,
                source=wallet_conf.WALLET_RECORD_SOURCE_SYS_MODIFIED_APP,
                utime=utime,
                status=wallet_conf.TRANS_STATUS_SYS_MODIFIED,
                extends=json.dumps(extends),
            )

            # 写钱包消息
            msg_info = dict(
                type=config.messages.WALLET_MSG_TYPE_EVENT_MARGIN_REFUND,
                title=trans_lang(lang_idx.IDX_WALLET_INVOICE_TITLE_SATELLITE, config.LANG_EN_GB),
                content=trans_lang(lang_idx.IDX_WALLET_INVOICE_TITLE_SATELLITE, config.LANG_EN_GB),
                amount=NumTrans.make_eu_str(amount, divide_100=False),
                utime=get_default_format_time(utime),
                rid=record_model.id,
                gid=sponsor_id,
            )

            logger.debug("satellite_msg_info: %s", msg_info)

            MasterWalletMsg.insert_wallet_data(uid, msg=json_compact_encode(msg_info))

            # 写保证金流水记录
            trans_no = record_model.trans_no
            margin_flow_record = GroupFlowMarginRecord.insert_record(
                sponsor_id=sponsor_id,
                wallet_type=wallet_conf.SATELLITE_GROUP_WALLET_TYPE,
                amount=NumTrans.multiply_100(amount),
                trans_no=trans_no,
                reason=reason,
                source=source
            )
            if amount > 0:
                records = GroupFlowMarginRecord.query_record_by_source(source, False)
                for record in records:
                    record.is_completed = True
                    record.save()

            logger.debug("satellite_margin_flow_record: %s", margin_flow_record)

    except Exception as e:
        logger.fatal('satellite manual alter group balance error occur.{}'.format(e), exc_info=True)
        return dict(ret=-1, error_msg="satellite manual alter group balance error occur")

    safe_call(PlayerActivityReport.create_or_accumulation, uid)

    return True, source


register_alter_wallet_plugins(wallet_conf.SATELLITE_GROUP_WALLET_TYPE, manual_alter_group_balance)
register_alter_wallet_plugins(wallet_conf.SATELLITE_ALLIANCE_WALLET_TYPE, manual_alter_alliance_balance)
