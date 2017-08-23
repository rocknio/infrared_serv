# !/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import logging

import tornado
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from settings import POST_RETRY_TIMES, POST_REQUEST_TIMEOUT, IS_POST_TO_MAIN_SERVER

__author__ = "Neo"


@gen.coroutine
def http_client_post(url, msg, transid):
    """
    异步发送消息到业务层,并重试，重试后仍失败，返回false
    :param url: 门户接口url
    :param msg: dict类型http body
    :param transid: 消息id
    """
    # 测试时，暂时不提交后端
    if IS_POST_TO_MAIN_SERVER == 0:
        return True, None

    header, body = {}, ""
    try:
        logging.info('[{:<20}] post msg to url[{}]: {}'.format(transid, url, msg))
        if msg is not None and msg != '':
            body = json.dumps(msg)

        client = tornado.httpclient.AsyncHTTPClient()

        retry_time = 0
        while retry_time < POST_RETRY_TIMES:
            try:
                response = yield client.fetch(url, method='POST', body=body, request_timeout=POST_REQUEST_TIMEOUT)
                logging.info('[{:<20}] time[{}] send: {}, response code: {}, response body:{}'.format(transid, retry_time+1,
                             body, response.code, response.body))

                # 对端返回200或者500，表示对端已收到，如果处理失败就不再重发
                if response.code == 200 or response.code == 500:
                    break
                else:
                    retry_time += 1
            except Exception as err_info:
                logging.error('[{:<20}] time[{}] post! send: {}, err = {}'.format(transid, retry_time+1, body, err_info))
                retry_time += 1
        else:
            return False, None

        return True, response.body

    except Exception as err:
        logging.error('[{:<20}] notify server[{} - {}] with err = {}'.format(transid, url, msg, err))
        return False, None
