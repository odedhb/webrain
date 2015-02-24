from google.appengine.ext import ndb
import webapp2
import re


class Item(ndb.Model):
    url_template = ndb.StringProperty()
    # url_computed = ndb.ComputedProperty()
    query_template = ndb.StringProperty()
    # excerpt = ndb.StringProperty()
    image = ndb.StringProperty()
    # clicks = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty(auto_now_add=True)


class Search(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("q")

        item = Item(url_template="https://www.facebook.com/search/str/mike/keywords_top")
        item.query_template = "flights from (?P<source>.+) to (?P<destination>.+)"
        item.image = "https://cdn2.vox-cdn.com/uploads/chorus_asset/file/3397376/tbf_014_gates_education_thumb_raw.0.jpg"
        item.clicks = 3
        all_items = [item]

        matching_items = []

        for item in all_items:
            if re.match(item.query_template, query):
                matching_items.append(item)

        html = SEARCH_BOX
        for item in matching_items:
            html = html + "<br><a href='" + item.url_template + "'>" + item.query_template + "</a><br>"

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
