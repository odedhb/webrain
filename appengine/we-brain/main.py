from google.appengine.ext import ndb
import webapp2
import re

# Build a programmatic search engine, gets a string, if it doesn't fit a template, it asks for an answer or a link.
# Then parses the link to the template for matching. Use Facebook excerpt for search results.


class Item(ndb.Model):
    url_template = ndb.StringProperty()
    query_regex = ndb.StringProperty()
    clicks = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty(auto_now_add=True)


class Search(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("q")

        item = Item(url_template="https://www.facebook.com/search/str/{person}/keywords_top")
        item.query_regex = "search (?P<person>.+) on facebook"
        item.clicks = 3
        all_items = [item]

        matching_items = []

        for item in all_items:
            if re.match(item.query_regex, query):
                matching_items.append(item)

        html = SEARCH_BOX
        for item in matching_items:
            matches = re.match(item.query_regex, query)
            group_dict = matches.groupdict()
            computed_url = item.url_template.format(**group_dict)
            html = html + "<br><a href='" + computed_url + "'>" + computed_url + "</a><br>"

        html += ADD_LINK
        self.response.write(html)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(SEARCH_BOX)


SEARCH_BOX = """
<form action="../search">
    <input type="text" name="q">
    <input type="submit" value="go">
</form>
        """

ADD_LINK = """
<br><a href=''>Add +</a>
        """

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/search', Search)]
                              , debug=True)
