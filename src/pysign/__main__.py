from sys import exit
import logging
from logging import basicConfig

if __name__ == "__main__":
  from poetry.console.application import main

  level = (logging, loglevel.upper(), None) |*> getattr
  if not (level, int) |*> isinstance:
      raise f"Bad log level: {level}" |> ValueError

  basicConfig(?, encoding="utf-8", level=level) <| "../logs/pysign.log"

  main() |> exit

