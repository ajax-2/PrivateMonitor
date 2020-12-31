# coding: utf-8

from src.info.ServerInfo import ServerInfo

si = ServerInfo()


def test_frequency():
    si.init()
    print si.get_monitor_frequency()


if __name__ == "__main__":
    si.set_server_info("http://192.168.1.63:9200", "demo")
    test_frequency()
