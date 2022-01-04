from sys import exit
import logging
from logging import basicConfig

if __name__ == "__main__":
  from poetry.console.application import main

  level = getattr(logging, loglevel.upper(), None)
  if not isinstance(level, int):
      raise ValueError(f"Bad log level: {level}")

  basicConfig("../logs/pysign.log", encoding="utf-8", level=level)

  exit(main())
