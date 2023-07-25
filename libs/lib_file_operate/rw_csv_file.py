import csv
import os

from libs.lib_file_operate.file_utils import file_is_empty


def read_csv_to_dict(csv_file, mode="r", encoding="utf-8"):
    """
    ����CSV�ļ����ֵ��ʽ(���Զ�ƴ�ӱ�ͷ)
    :param csv_file:
    :param mode:
    :param encoding:
    :return:
    """
    if file_is_empty:
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # �Զ������ָ���
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        row_list = [row for row in reader]
        return row_list


def read_csv_to_simple_list(csv_file, mode="r", encoding="utf-8"):
    """
    ����CSV�ļ����б��ʽ(������������)
    :param csv_file:
    :param mode:
    :param encoding:
    :return:
    """
    if file_is_empty:
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # �Զ������ָ���
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect=dialect)
        row_list = [row for row in reader]
        return row_list


def write_dict_to_csv(csv_file, dict_data=[], mode="a+", encoding="utf-8"):
    """
    д���ֵ��ʽ�����ݵ�csv�ļ���
    :param csv_file:
    :param dict_data:
    :param mode:
    :param encoding:
    :return:
    """
    # �ж��Ƿ���Ҫд���ͷ
    file_empty = file_is_empty(csv_file)

    # ��ʹ��csv.writer()д��CSV�ļ�ʱ��ͨ�����齫newline��������Ϊ''���Ա㰴��ϵͳ��Ĭ����Ϊ���л��з��Ĵ���
    with open(csv_file, mode=mode, encoding=encoding, newline='') as file_open:
        # DictWriter ֱ��д���ֵ��ʽ������
        # fieldnames=data[0].keys() ���ֵ�ļ���Ϊ��ͷ
        # quoting=csv.QUOTE_ALL  ��ÿ��Ԫ�ض���˫���Ű���
        csv_writer = csv.DictWriter(file_open, fieldnames=dict_data[0].keys(), quoting=csv.QUOTE_ALL)
        if file_empty:
            csv_writer.writeheader()
        csv_writer.writerows(dict_data)
