#!/usr/bin/env python

import os
import re
import sys
import shutil
from helper import *

class Package():
   def __init__(self, package, directory):
      self.package = package

      if self.validate():
         self.set_helper()
         self.clean_directory()
         self.git_clone()

         self.module = packages_path + '/' + directory
         self.version = extract(self.module, 'pkgver')
         self.description = extract(self.module, 'pkgdesc')

         if 'pre_build' in dir(self.package):
            self.package.pre_build()

   def commit(self):
         os.system(
            'git add . && ' + \
            'git commit -m "Bot: Add last update into ' + self.package.name + ' package ~ version ' + self.version + '"')

   def is_build(self):
      for f in os.listdir(repository_path):
         if not output('git status . --porcelain | sed s/^...//'):
            return True

      for f in os.listdir(repository_path):
         if f.startswith(self.package.name + '-'):
            os.remove(repository_path + '/' + f)

   def build_package(self):
      os.system(
         'sudo pacman -S $(source ./PKGBUILD && echo ${depends[@]} ${makedepends[@]}) --noconfirm && ' \
         'makepkg -Ad --skipinteg && ' \
         'mv *.pkg.tar.xz ' + repository_path);

   def clean_directory(self):
      files = os.listdir('.')
      for f in files:
         if os.path.isdir(f):
            shutil.rmtree(f)
         elif os.path.isfile(f) and f != 'package.py':
            os.remove(f)

   def git_clone(self):
      os.system(
         'git init && ' \
         'git remote add origin ' + self.package.source + ' && ' \
         'git pull origin master && ' \
         'rm -rf .git')

      if os.path.isfile('.SRCINFO'):
         os.remove('.SRCINFO')

   def set_helper(self):
      self.package.edit_file = edit_file
      self.package.replace_ending = replace_ending

   def validate(self):
      try:
          self.package.name
          self.package.source
          return True
      except AttributeError:
         return False
