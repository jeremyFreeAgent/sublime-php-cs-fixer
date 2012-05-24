import sublime
import sublime_plugin
import subprocess
import threading
import os

from subprocess import Popen
from subprocess import PIPE

settings = sublime.load_settings('PHP-CS-Fixer.sublime-settings')

class Setting:
    @staticmethod
    def load():
        Setting.show_debug = bool(settings.get('show_debug', False))
        Setting.path = settings.get('path', '')
        Setting.php_path = settings.get('php_path', '')
        Setting.additional_args = settings.get('additional_args', {})
        Setting.activated = bool(settings.get('activated'))

Setting.load()

[settings.add_on_change(setting, Setting.load) for setting in [
    'show_debug',
    'path',
    'php_path',
    'additional_args',
    'activated']]

def show_debug(message):
    if Setting.show_debug == True:
        print "[PHP CS Fixer] " + message

class ShellCommand():
    def shell_out(self, cmd):
        data = None
        show_debug(' '.join(cmd))

        if sublime.platform() == "windows":
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        if proc.stdout:
            data = proc.communicate()[0]

        return data

class PhpCsFixerFixThisFileCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
      self.view = view

    def run(self, path):
        show_debug('Start - Fix this file')
        if Setting.activated != True:
            return

        if Setting.php_path != "":
            args = [Setting.php_path]
        else:
            args = ['php']

        if Setting.path == "":
            return

        args.append(Setting.path)

        args.append("fix")

        for key, value in Setting.additional_args.items():
            arg = key
            if value != "":
                arg += "=" + value
            args.append(arg)

        args.append(self.view.file_name())

        self.fix_the_code(args)
        show_debug('End - Fix this file')

    def shell_out(self, cmd):
        data = None
        show_debug(' '.join(cmd))

        if sublime.platform() == "windows":
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        else:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        if proc.stdout:
            data = proc.communicate()[0]

        return data

    def fix_the_code(self, args):
        result = self.shell_out(args)
        sublime.set_timeout(lambda: self.view.run_command('revert'), 100)
        show_debug(result)
