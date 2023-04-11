#!/usr/bin/env python
# encoding: utf-8
import copy

from libs.lib_rule_dict.base_key_replace import replace_list_has_key_str
from libs.lib_rule_dict.base_rule_parser import base_rule_render_list
from libs.lib_rule_dict.util_dict import dict_content_base_rule_render, cartesian_product_merging, frozen_tuple_list
from libs.util_file import get_dir_path_file_name, read_file_to_frequency_dict, file_encoding, get_key_list_with_frequency
from setting import *


# 合并folders目录字典列表和files目录字典列表
def product_folders_and_files(folder_list, files_list):
    def format_paths(path_list):
        """
        格式化目录和文件的路径，使其符合要求
        """
        formatted_paths = []
        for path in path_list:
            path = path.strip("/")
            if not path.startswith('/'):
                path = '/' + path
            if path.endswith('/'):
                path = path.rstrip('/')
            formatted_paths.append(path)
        formatted_paths = list(set(formatted_paths))
        return formatted_paths

    # 记录开始替换的时间
    start_time = time.time()

    # 格式化目录
    folder_list = format_paths(folder_list)
    # 格式化file
    files_list = format_paths(files_list)

    group_folder_files_list = cartesian_product_merging(folder_list, files_list)
    group_folder_files_list = frozen_tuple_list(group_folder_files_list, link_symbol="")
    end_time = time.time()
    run_time = end_time - start_time
    return group_folder_files_list, run_time


# 合并urls列表和paths列表
def product_urls_and_paths(urls, paths):
    def format_urls(url_list):
        """
        格式化目录和文件的路径，使其符合要求
        """
        formatted_paths = []
        for url in url_list:
            if url.endswith('/'):
                url = url.rstrip('/')
            formatted_paths.append(url)
        formatted_paths = list(set(formatted_paths))
        return formatted_paths

    # 格式化目录
    urls = format_urls(urls)
    paths = format_urls(paths)

    url_add_path_list = cartesian_product_merging(urls, paths)
    url_add_path_list = frozen_tuple_list(url_add_path_list, link_symbol="")
    return url_add_path_list


# 按频率 读取直接路径 -> 全路径 字典下的所有文件,并进行 解析
def read_dirs_frequency_rule_list(dict_dir=None,
                                  dict_suffix=".lst",
                                  frequency_symbol="<-->",
                                  annotation_symbol="#",
                                  frequency_min=0):
    """
    # 1 读取 所有基本替换变量字典 到频率字典
    # 2 按频率筛选 并加入到 基本变量替换字典
    # 3 对 基本变量替换字典 进行规则解析
    """
    # 存储所有规则
    rule_list = []
    # 获取文件名
    base_var_file_list = get_dir_path_file_name(dict_dir, ext=dict_suffix)
    # 生成文件名对应基础变量
    # 并 同时读文件组装 {基本变量名: [基本变量文件内容列表]}
    for dict_file in base_var_file_list:
        # 读文件到列表
        base_var_file_path = os.path.join(dict_dir, dict_file)
        # 获取频率字典 # 筛选频率字典
        frequency_dict = read_file_to_frequency_dict(base_var_file_path,
                                                     encoding=file_encoding(base_var_file_path),
                                                     frequency_symbol=frequency_symbol,
                                                     annotation_symbol=annotation_symbol)
        frequency_list = get_key_list_with_frequency(frequency_dict,frequency_min)

        rule_list.extend(frequency_list)

    # 对 列表 中的规则进行 进行 动态解析
    rule_list, render_count, run_time = base_rule_render_list(rule_list)
    return rule_list


# 获取基本变量替换字典
def gen_base_var_dict_frequency(base_var_dir,
                                dict_suffix,
                                base_replace_dict,
                                frequency_symbol,
                                annotation_symbol,
                                frequency_min):
    """
    # 1 读取 所有基本替换变量字典 到频率字典
    # 2 按频率筛选 并加入到 基本变量替换字典
    # 3 对 基本变量替换字典 进行规则解析
    """
    base_var_replace_dict = copy.copy(base_replace_dict)
    # 获取文件名
    base_var_file_list = get_dir_path_file_name(base_var_dir, ext=dict_suffix)

    # 生成文件名对应基础变量
    # 并 同时读文件组装 {基本变量名: [基本变量文件内容列表]}
    for base_var_file_name in base_var_file_list:
        base_file_pure_name = base_var_file_name.rsplit(dict_suffix, 1)[0]
        base_var_name = f'%{base_file_pure_name}%'

        # 读文件到列表
        base_var_file_path = os.path.join(base_var_dir, base_var_file_name)
        # 获取频率字典 # 筛选频率字典
        frequency_dict = read_file_to_frequency_dict(base_var_file_path,
                                                     encoding=file_encoding(base_var_file_path),
                                                     frequency_symbol=frequency_symbol,
                                                     annotation_symbol=annotation_symbol)
        frequency_list = get_key_list_with_frequency(frequency_dict,frequency_min)
        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_replace_dict[base_var_name] = frequency_list

    # 对 内容列表 中的规则进行 进行 动态解析
    base_var_replace_dict = dict_content_base_rule_render(base_var_replace_dict)

    return base_var_replace_dict


def gen_base_scan_path_list():
    base_paths = []
    # 获取基本变量替换字典
    base_var_replace_dict = gen_base_var_dict_frequency(base_var_dir=GB_BASE_VAR_DIR,
                                                        dict_suffix=GB_DICT_FILE_EXT,
                                                        base_replace_dict=GB_BASE_VAR_REPLACE_DICT,
                                                        frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                        annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                        frequency_min=1
                                                        )

    # 2、读取直接追加字典
    if GB_ADD_DIRECT_DICT:
        # module = '读取直接追加路径'
        direct_path_list = read_dirs_frequency_rule_list(dict_dir=GB_DIRECT_PATH_DIR,
                                                         dict_suffix=GB_DICT_FILE_EXT,
                                                         frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                         annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                         frequency_min=FREQUENCY_MIN)
        # 4、对每个元素进行规则替换
        direct_path_list, replace_count, run_time = replace_list_has_key_str(direct_path_list, base_var_replace_dict)
        base_paths.extend(direct_path_list)

    # 3、读取笛卡尔积路径 字典
    if GB_ADD_GROUP_DICT:
        # 按频率 读取笛卡尔积路径 -> 目录 字典下的所有文件,并进行解析
        # module = '读取笛卡尔积路径 -> 目录'
        group_folder_list = read_dirs_frequency_rule_list(dict_dir=GB_GROUP_FOLDER_DIR,
                                                          dict_suffix=GB_DICT_FILE_EXT,
                                                          frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                          annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                          frequency_min=FREQUENCY_MIN)
        # 对每个元素进行规则替换
        group_folder_list, replace_count, run_time = replace_list_has_key_str(group_folder_list, base_var_replace_dict)

        # 按频率 读取笛卡尔积路径 -> 文件 字典下的所有文件,并进行解析
        # module = '读取笛卡尔积路径 -> 文件'
        group_files_list = read_dirs_frequency_rule_list(dict_dir=GB_GROUP_FILES_DIR,
                                                         dict_suffix=GB_DICT_FILE_EXT,
                                                         frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                         annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                         frequency_min=FREQUENCY_MIN)
        # 4、对每个元素进行规则替换
        group_files_list, replace_count, run_time = replace_list_has_key_str(group_files_list, base_var_replace_dict)

        # 组合 group_folder_list group_files_list
        group_dict_list, run_time = product_folders_and_files(group_folder_list, group_files_list)
        base_paths.extend(group_dict_list)
    return base_paths


if __name__ == '__main__':
    gen_base_scan_path_list()