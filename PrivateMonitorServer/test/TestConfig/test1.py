#!/usr/bin/python
# coding: utf-8
from Config import Config

# 测试


def test_parse():
    conf = Config()
    conf.parse_from_config_ini()
    assert conf.test_config()


def test_instance():
    conf1 = Config()
    conf2 = Config()
    conf1.parse_from_config_ini()
    assert conf2.test_config()


if __name__ == "__main__":
    test_parse()
    test_instance()
