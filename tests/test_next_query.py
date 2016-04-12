"""
tests for the webhose interface.

note that the webhose token is taken from the WEBHOSE_TOKEN environment variable
"""

import unittest
import os

import webhose

class NextTestCase(unittest.TestCase):
    def test_next(self):
        """
        check that if we use the 'since' parameter from one query, that we
        don't get any overlap
        """

        # run a "regular" query
        webhose.config(os.environ['WEBHOSE_TOKEN'])
        query = webhose.Query()
        query.some_terms = ('boston','red sox')
        query.language = 'english'
        query.site_type = 'news'

        response = webhose.search(query)

        # grab some stuff that we need for testing
        next_ts = response.next_ts
        last_post_crawled = response.posts[99].crawled_parsed

        # now run our second query
        response = webhose.search(query, since=response.next_ts)

        self.assertGreater(response.posts[99].crawled_parsed,
                           last_post_crawled)

if __name__ == "__main__":
    unittest.main()