import unittest

import os
import sys
import time
import sqlite3
import os.path as op
from shutil import rmtree
from functools import partial
from kivy.clock import Clock

main_path = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(main_path)
from main import KrySA


class Test(unittest.TestCase):
    def pause(*args):
        time.sleep(0.000001)

    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        # open open_project dialog
        app.root.open_project()
        test_project = op.join(op.dirname(self.folder), 'test_Project')
        app.root.opendlg.run([op.join(test_project, 'Test.krysa')])

        self.assertTrue(app.project_exists)
        self.assertEqual(app.project_dir, test_project)
        self.assertEqual(app.project_name, 'Test')
        data = op.join(test_project, 'data')
        results = op.join(test_project, 'results')

        # set testing data
        newdata_values = [[0, u'', 0.0],
                          [0, u'', 0.0],
                          [0, u'end', 0.0],
                          [0, u'', 1.1],
                          [1, u'', 0.0]]
        newdata2_values = [[1, u'text', 1.1]]

        # get data from krysa table
        krysa_ndv = []
        for d in app.root.tables[0][1].rv.data:
            if 'c' in d.keys():
                if d['type'] == int:
                    krysa_ndv.append(int(d['text']))
                elif d['type'] == float:
                    krysa_ndv.append(float(d['text']))
                else:
                    krysa_ndv.append(d['text'])
        krysa_ndv = [krysa_ndv[x:x+3] for x in xrange(0, len(krysa_ndv), 3)]

        krysa_ndv2 = []
        for d in app.root.tables[1][1].rv.data:
            if 'c' in d.keys():
                if d['type'] == int:
                    krysa_ndv2.append(int(d['text']))
                elif d['type'] == float:
                    krysa_ndv2.append(float(d['text']))
                else:
                    krysa_ndv2.append(d['text'])
        krysa_ndv2 = [krysa_ndv2[x:x+3] for x in xrange(0, len(krysa_ndv2), 3)]

        # test data
        self.assertTrue(op.exists(op.join(data, 'data.sqlite')))
        conn = sqlite3.connect(op.join(data, 'data.sqlite'))
        c = conn.cursor()
        c.execute('SELECT * FROM NewData')
        values = [item for sublist in c.fetchall() for item in sublist]
        values = [values[x:x+3] for x in xrange(0, len(values), 3)]
        conn.close()
        print 'NewData:'
        for i, v in enumerate(values):
            # values == sql values
            self.assertEqual(v, newdata_values[i])
            # values == KrySA values
            self.assertEqual(krysa_ndv[i], newdata_values[i])
            print v

        conn = sqlite3.connect(op.join(data, 'data.sqlite'))
        c = conn.cursor()
        c.execute('SELECT * FROM NewData2')
        values = [item for sublist in c.fetchall() for item in sublist]
        values = [values[x:x+3] for x in xrange(0, len(values), 3)]
        conn.close()
        print '\nNewData2:'
        for i, v in enumerate(values):
            self.assertEqual(v, newdata2_values[i])
            self.assertEqual(krysa_ndv2[i], newdata2_values[i])
            print v

        app.stop()

    def test_file_openproject(self):
        self.path = op.dirname(op.abspath(__file__))
        if not op.exists(op.join(self.path, 'test_folder')):
            os.mkdir(op.join(self.path, 'test_folder'))
        else:
            rmtree(op.join(self.path, 'test_folder'))
            os.mkdir(op.join(self.path, 'test_folder'))
        self.folder = op.join(self.path, 'test_folder')

        app = KrySA()
        p = partial(self.run_test, app)
        Clock.schedule_once(p, .000001)
        app.run()
        rmtree(self.folder)

if __name__ == '__main__':
    unittest.main()
