import time
import random
import string

from django.test import TestCase

from .models     import FileStorage

TOTAL_FILES = 50

FILE_SIZE_SPECS = [
    dict(size=1000,    num_files=TOTAL_FILES/2 + TOTAL_FILES/16),
    dict(size=10000,   num_files=TOTAL_FILES/4),
    dict(size=100000,  num_files=TOTAL_FILES/8),
    dict(size=1000000, num_files=TOTAL_FILES/16),
]


def make_random_str(num):
    return ''.join([ random.choice(string.letters) for i in xrange(num) ])


class PerformanceTest(TestCase):
    def setUp(self):
        """
        Create a user that we will use for the test.

        """
        total = 0
        self.file_list = list()
        for spec in FILE_SIZE_SPECS:
            num_files = spec['num_files']
            size      = spec['size']
            print "@@@ Creating %d random files of size %d." % \
                (num_files, size)
            for i in xrange(num_files):
                fname = make_random_str(80)
                self.file_list.append(fname)
                body  = make_random_str(size)
                total += 1
                print "- %d/%d (%d). %s" % (i, num_files, total, fname)
                FileStorage(name=fname, blob=body).save()

    def test_010(self):
        read_chunk = 1000
        write_prob = 20   # as in: 1 in 20
        while True:
            t1 = time.time()
            total_len = 0
            total_writes = 0
            total_write_bytes = 0
            for i in xrange(read_chunk):
                fname = random.choice(self.file_list)
                fs = FileStorage.objects.get(name=fname)
                len_blob = len(fs.blob)
                total_len += len_blob
                if random.randint(1,write_prob) == write_prob:
                    find_char    = random.choice(string.letters)
                    replace_char = random.choice(string.letters)
                    fs.blob.replace(find_char, replace_char)
                    fs.save()
                    total_writes += 1
                    total_write_bytes += len_blob

            t2 = time.time()
            total_time = t2-t1
            total_len_mb = total_len/(1024*1024)
            total_write_len_mb = total_write_bytes/(1024*1024)
            print ("@@@ %d reads, reads/s: %.2f, total read chars: %.2f MB,"
                   " writes: %d, total written chars: %.2f MB,"
                   " total time: %f, average speed: %.2f MB/s" %
                   (read_chunk, read_chunk/total_time, total_len_mb,
                    total_writes, total_write_len_mb,
                    total_time, (total_len_mb / total_time)))

