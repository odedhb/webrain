from google.appengine.ext import ndb
import webapp2
import re

# Build a programmatic search engine, gets a string, if it doesn't fit a template, it asks for an answer or a link.
# Then parses the link to the template for matching. Use Facebook excerpt for search results.

# Match the URL and the query string. Show matches with check boxes on their sides.
# Every checked box becomes a regex group.

class Item(ndb.Model):
    url_template = ndb.StringProperty()
    query_regex = ndb.StringProperty()
    clicks = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty(auto_now_add=True)


class Search(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("q")
        all_items = Item.query().fetch()

        if not all_items:
            item = Item(url_template="https://www.facebook.com/search/str/{person}/keywords_top")
            item.query_regex = "search (?P<person>.+) on facebook"
            item.clicks = 3
            all_items = [item]

        all_items.append(Item(url_template="https://www.google.co.il/search?q={query}", query_regex="(?P<query>.+)"))
        all_items.append(Item(url_template="http://www.google.com/search?btnI&q={query}", query_regex="(?P<query>.+)"))

        matching_items = []

        for item in all_items:
            if re.match(item.query_regex, query):
                matching_items.append(item)

        html = search_box(query)
        for item in matching_items:
            matches = re.match(item.query_regex.encode('utf-8'), query.encode('utf-8'))
            group_dict = matches.groupdict()
            computed_url = item.url_template.format(**group_dict)
            html = html + "<br><a href='" + computed_url + "'>" + computed_url + "</a><br>"

        html += ADD_LINK
        self.response.write(html)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(search_box())


class Add(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("q")
        url = self.request.get("url")
        Item(url_template=url, query_regex=query).put()
        self.response.write("Added!")


def search_box(term=""):
    return """
<form action="../search">
    <input type="text"  size="80" autofocus onfocus="this.value = this.value;" name="q" value='""" + term + """'>
    <input type="submit" value="go">
</form>
        """


ADD_LINK = """
<form action="../add">
    </br></br></br></br></br><h3>Add your own result:</h3>

    Query with <a href='https://docs.python.org/2/library/re.html'>regex</a> parameter(s):</br>
    <input type="text" size="80" name="q"></br>
    e.g. "search (?P&lt;person&gt;.+) on facebook"</br></br>

    Url with matching parameter(s):</br>
    <input type="text" name="url" size="80" ></br>
    e.g. https://www.facebook.com/search/str/{person}/keywords_top</br></br>
    <input type="submit" value="add">
</form>
        """

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/add', Add),
                               ('/search', Search)]
                              , debug=True)
