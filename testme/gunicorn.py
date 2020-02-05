import gevent.monkey
gevent.monkey.patch_all()

import sys
from pkg_resources import load_entry_point


def main():
    sys.exit(
        load_entry_point('gunicorn', 'console_scripts', 'gunicorn')()
    )

if __name__ == '__main__':
    sys.exit(main())
