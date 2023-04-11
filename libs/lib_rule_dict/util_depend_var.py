#!/usr/bin/env python
# encoding: utf-8


# 从URL中获取域名相关的单词
import copy

from libs.lib_log_print.logger_printer import output
from libs.lib_rule_dict.util_dict import dict_content_base_rule_render
from libs.lib_url_analysis.url_tools import get_domain_words, get_path_words_urlsplit


# 获取 基于 HTTP 请求的 因变量
def set_dependent_var_dict(target_url,
                           base_dependent_dict,
                           ignore_ip_format=None,
                           symbol_replace_dict=None,
                           not_allowed_symbol=None):
    """
    获取 基于 HTTP 请求的 因变量
    %%DOMAIN%%  域名相关--较多
    "%%PATH%%"  路径相关--极少
    """
    dependent_var_dict = copy.copy(base_dependent_dict)

    # 基于URL获取因变量
    if target_url:
        domain_words = get_domain_words(target_url,
                                        ignore_ip_format=ignore_ip_format,
                                        symbol_replace_dict=symbol_replace_dict,
                                        not_allowed_symbol=not_allowed_symbol)
        dependent_var_dict["%%DOMAIN%%"] = domain_words

        path_words = get_path_words_urlsplit(target_url,
                                             symbol_replace_dict=symbol_replace_dict,
                                             not_allowed_symbol=not_allowed_symbol)
        dependent_var_dict["%%PATH%%"] = path_words
    else:
        output(f"[-] 注意: 未输入目标URL参数,无法获取因变量", level="error")
        dependent_var_dict["%%DOMAIN%%"] = None
        dependent_var_dict["%%PATH%%"] = None

    # 对 内容列表 中的规则进行 进行 动态解析
    dependent_var_dict = dict_content_base_rule_render(dependent_var_dict)

    return dependent_var_dict