import pysign__anki
import pysign__articles
import pysign__common
import pysign__config
import pysign__formatting
import pysign__globals
import pysign__sentences
import pysign__variants
import pysign__videos
import pysign__wordlists

with session() as c:
  c.post(API_BASE, data = payload)
