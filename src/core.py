from subprocess import call

import pip

import os

import logging


class PkgUpdIns():

    def __init__(self, dir_pip=''):
        self.dir_pip = dir_pip
        self.logger = self.logger_get()

    # ------------ --------- ------------ #
    # ------------ LLVL FUNC ------------ #
    # ------------ --------- ------------ #

    def pkg_local(self, pkg_file_lst=[], dir_pkg_local=''):

        for pkg_file in pkg_file_lst:
            print('___ installing [{}] ...'.format(pkg_file))
            ret = call(
                self.dir_pip + 'pip install --upgrade --force-reinstall ' +
                os.path.join(dir_pkg_local, pkg_file), shell=True)
            if ret != 0:
                print('___ returned with code [{}].'.format(ret))

    def pkg_upd_online(self, pkg_name_lst=[]):

        for pkg_name in pkg_name_lst:
            print('___ upgrading [{}] ...'.format(pkg_name))
            ret = call(self.dir_pip + 'pip install --upgrade ' + pkg_name, shell=True)
            if ret != 0:
                print('___ returned with code [{}].'.format(ret))

    def pkg_ins_online(self, pkg_name_lst=[]):

        for pkg_name in pkg_name_lst:
            print('___ installing [{}] ...'.format(pkg_name))
            ret = call(self.dir_pip + 'pip install ' + pkg_name, shell=True)
            if ret != 0:
                print('___ returned with code [{}].'.format(ret))

    # ------------ --------- ------------ #
    # ------------ HLVL FUNC ------------ #
    # ------------ --------- ------------ #

    def logger_get(self):

        # logging.basicConfig(filename='log.log',
        #                     level=logging.DEBUG,
        #                     format='%(asctime)s %(message)s')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('log.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(name)-12s: <%(asctime)s> %(levelname)-8s %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def check_local(self, dir_pkg_local=r''):

        logger_debug = self.logger.debug

        pkg_file_lst = [
            f for f in os.listdir(dir_pkg_local)
            if (f.endswith('.whl') and
                os.path.isfile(os.path.join(dir_pkg_local, f)))
        ]

        logger_debug(
            '--- --- --- --- --- PACKAGE AT LOCAL --- --- --- --- ---')
        logger_debug(sorted(['{}'.format(i)
                             for i in pkg_file_lst]))

        self.pkg_local(pkg_file_lst, dir_pkg_local)

    def check_online(self,
                     pkg_name_inp_lst=[],
                     pkg_name_toignore_lst=[],
                     pkg_name_toprioritize_lst=[]):

        logger_debug = self.logger.debug

        pkg_name_cur_lst = []

        pkg_cur_lst = pip.get_installed_distributions()

        logger_debug(
            '--- --- --- --- --- PACKAGE CURRENTLY INSTALLED --- --- --- --- ---')
        logger_debug(sorted(['{}=={}'.format(i.key, i.version)
                             for i in pkg_cur_lst]))

        for pkg in pkg_cur_lst:
            pkg_name_cur_lst.append(pkg.project_name.lower())

        for pkg_name in pkg_name_toignore_lst:
            if pkg_name in pkg_name_cur_lst:
                del pkg_name_cur_lst[pkg_name_cur_lst.index(pkg_name)]

        for pkg_name in pkg_name_toprioritize_lst:
            if pkg_name in pkg_name_cur_lst:
                pkg_name_cur_lst.insert(0, pkg_name_cur_lst.pop(
                    pkg_name_cur_lst.index(pkg_name)))

        if pkg_name_inp_lst:
            pkg_name_toupd_lst = []
            pkg_name_toins_lst = []
            for pkg_name in pkg_name_cur_lst:
                if pkg_name in pkg_name_inp_lst:
                    pkg_name_toupd_lst.append(pkg_name)
                else:
                    pkg_name_toins_lst.append(pkg_name)

        else:
            pkg_name_toupd_lst = list(pkg_name_cur_lst)
            pkg_name_toins_lst = []

        if pkg_name_toupd_lst:
            logger_debug(
                '--- --- --- --- --- PACKAGE TO UPDATE --- --- --- --- ---')
            logger_debug(sorted(['{}'.format(i)
                                 for i in pkg_name_toupd_lst]))

            self.pkg_upd_online(pkg_name_toupd_lst)

        if pkg_name_toins_lst:
            logger_debug(
                '--- --- --- --- --- PACKAGE TO INSTALL --- --- --- --- ---')
            logger_debug(sorted(['{}'.format(i)
                                 for i in pkg_name_toins_lst]))

            self.pkg_ins_online(pkg_name_toins_lst)
