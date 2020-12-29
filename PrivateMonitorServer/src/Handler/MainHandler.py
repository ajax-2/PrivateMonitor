# coding: utf-8

from flask import render_template
from src.Implement.MainImplement import MainImplement


class MainHandler(object):

    @staticmethod
    def main():
        clusters, error = MainImplement.main()
        return render_template("index.html", clusters=clusters, error=error)


