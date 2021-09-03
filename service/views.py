# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from mg.satellite.forms import SatelliteEventFrom
from mg.satellite.services import get_alter_wallet_plugins, filter_satellite_event, get_wallet_params
from mg.views.mtt_events import SatelliteMttEvent, MttEventList
from pokerclub_friends.models import FriendsGroup
from share.innerapi.utils import inner_request_required
from share.log import logger
from share.log import logger_mg as logger
from share.mtt_helper import MTTHelper
from share.utils import jsonify


# Create your views here.
class SatelliteListView(View):
    template_name = 'mg/content/club_mtt/mtt_events.html'

    def get(self, request):
        render_params_dict = dict(
            event_list=self.get_satellite_list(),
        )

        logger.info('satellite_msg -> render_params_dict: %s', render_params_dict)

        return render(request, self.template_name, render_params_dict)

    def get_satellite_list(self):
        """
        获取satellite列表
        :return:
        """
        event_list = MTTHelper.get_mtt_list()

        logger.info('satellite_msg -> from game satellite_list: %s', event_list)

        event_list = map(MttEventList().warp_mtt_info, event_list)

        logger.info('satellite_msg -> warp_mtt_info_satellite_list: %s', event_list)

        # 筛选卫星赛
        statllite_list = filter_satellite_event(event_list)

        logger.info('satellite_msg -> result_list: %s', statllite_list)

        return statllite_list


class SatelliteCreateView(View):
    template_name = 'mg/content/club_mtt/club_mtt_add.html'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request):
        """
        创建satellite赛事
        :return:
        {
            "code": 0为正常, -1为异常
        }
        """
        event_data = json.loads(request.POST.get('event_data'))

        form = SatelliteEventFrom(event_data)

        if not form.is_valid():
            return jsonify(code=-1, error_msg=form.errors)

        form.data['source'] = str(uuid.uuid4())

        logger.info('satellite_msg -> create_satellite form_data: %s', form.data)

        # 游戏端参数校验
        ret, result, event_data = SatelliteMttEvent.do_satellite_mtt_info(form.data)

        logger.error("satellite_msg -> create_satellite, ret:%s, result:%s, event_data:%s", ret, result, event_data)

        if ret != 0:
            return jsonify(ret=ret, error_msg=result)

        wallet_params = get_wallet_params(form.data, event_data)

        logger.info('satellite_msg -> create_satellite wallet_params: %s', wallet_params)

        # 扣除保证金
        try:
            wallet_plugins = get_alter_wallet_plugins()

            flag, info = wallet_plugins[form.data.pop("wallet_type")]["alter_wallet_plugins"](**wallet_params)

        except Exception as error:
            logger.fatal('satellite_msg -> create_satellite: Failed to save transaction.{}'.format(error),
                         exc_info=True)
            return jsonify(code=-1, error_msg="Failed to save transaction")

        if not flag:
            return jsonify(code=-1, error_msg=info)

        # 调用游戏创建赛事
        try:
            ret, result = MTTHelper.create_satellite_mtt(event_data)
        except Exception as error:
            logger.fatal('satellite_msg -> create_satellite: Failed to create satellite.{}'.format(error),
                         exc_info=True)
            logger.fatal('satellite_msg -> create_satellite: Records of successful deduction. source: %s',
                         form.data['source'])

            return jsonify(code=-1, error_msg="Failed to create satellite")

        return jsonify(code=ret, error_msg=result)


@method_decorator(inner_request_required, name='post')
class QueryGroupView(View):

    def post(self, request):
        """
        根据club_id或alliance_id查询俱乐部列表
        """
        params_data = request.POST

        gid = params_data.get("club_id", None)
        alliance_id = params_data.get("alliance_id", None)

        if not gid and not alliance_id:
            return jsonify(code=-1, error_msg="Param missing")

        if gid:
            try:
                group = FriendsGroup.objects.get(gid=gid)
            except FriendsGroup.DoesNotExist as error:
                logger.error('satellite_msg -> gid does not exist, data: gid', gid)
                return jsonify(gid_list=[])

            if not group.alliance_id:
                return jsonify(gid_list=[(gid, group.gname)])
            else:
                return jsonify(gid_list=[(gid_dict['gid'], gid_dict['gname']) for gid_dict in
                                         FriendsGroup.objects.filter(alliance_id=group.alliance_id).values('gid', 'gname')])

        if alliance_id:
            gid_queryset = FriendsGroup.objects.filter(alliance_id=alliance_id).values('gid', 'gname')
            gid_list = [(gid_dict['gid'], gid_dict['gname']) for gid_dict in gid_queryset] if gid_queryset else []
            return jsonify(gid_list=gid_list)
