"""Convenience runner: python run.py --full"""

import sys
sys.path.insert(0, "api")

from api.poller.__main__ import main

if __name__ == "__main__":
    main()
