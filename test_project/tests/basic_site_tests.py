#
# Run site tests against the site.
#
# The site URL is specified as the first parameter.
#
import sys
import unittest
import requests

# We rely on the site URL being passed to us as the first
# parameter on the command line.
SITE_URL = sys.argv[1]

# Need to remove the URL from the command line, since otherwise
# it will confuse unittest, which is also looking for command
# line arguments.
del sys.argv[1]

class BaseConnectionTest(unittest.TestCase):

    def test_010_get_home_page(self):
        r = requests.get(SITE_URL)
        self.assertEqual(r.status_code, 200)
    def test_020_check_home_page_content(self):
        r = requests.get(SITE_URL)
        self.assertTrue("It worked!" in r.content)


if __name__ == '__main__':
    unittest.main()



