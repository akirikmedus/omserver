# ommdb.py

import string
import Sybase

def testdb():
    try:
        db = Sybase.connect('', '', '', '')
        c = db.cursor()
        #if len(sys.argv) > 1:
        #    c.execute('select c.text from syscomments c, sysobjects o'
        #              ' where o.name = @name and o.type = "P" and c.id = o.id'
        #              ' order by c.colid', {'@name': sys.argv[1]})
        #    print string.join([row[0] for row in c.fetchall()], '\n')
        #else:
        c.execute(
                "select site_id, name, type from sites")
        print string.join([row[0] for row in c.fetchall()], '\n')
    except (SystemExit, KeyboardInterrupt):
        raise
    #except Exception:
        #logger.error('Failed', exc_info=True)

