from core import PkgUpdIns

_dir_pip35_ = 'C:/Python35/Scripts/'
_dir_pip27_ = 'C:/Python27/Scripts/'

# ------------ --------- ------------ #
# ------------ MAIN FUNC ------------ #
# ------------ --------- ------------ #


def main():

    pui = PkgUpdIns(_dir_pip27_)

    pui.check_local(dir_pkg_local=r'../pkg_local')

    pui.check_online(pkg_name_inp_lst=[],
                     pkg_name_toignore_lst=['numpy', 'scipy', 'pywin32', 'lxml'],
                     pkg_name_toprioritize_lst=['pip', 'wheel', 'setuptools'])

# ------------ -------- ------------ #
# ------------ EXEC SEG ------------ #
# ------------ -------- ------------ #

if __name__ == '__main__':

    main()
