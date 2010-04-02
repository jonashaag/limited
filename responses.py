from django.http import HttpResponse
from django.utils.translation import ugettext as _

class HttpNotAcceptable(HttpResponse):
    """ A HTTP 406 error response """
    status_code = 406
    def __init__(self, message, *args, **kwargs):
        message = """
            <html>
                <body>
                    <h2>%s</h2>
                    <p>%s</p>
                </body>
            </html>
        """ % (_('No way to get in!'), _(message))
        HttpResponse.__init__(self, message, *args, **kwargs)

class SuccessfullyCommentedResponse(HttpResponse):
    """ Redirection page displayed after a comment was successfully posted """
    def __init__(self, redirect_to, *args, **kwargs):
        HttpResponse.__init__(self, """
            <html>
                <head>
                    <meta http-equiv="refresh" content="0; URL=%(url)s
                </head>
                <body>
                    <h2>%(headline)s</h2>
                    <p>%(expl_1)s</p>
                    <p>(%(expl_2)s <a href='%(url)s'>%(expl_3)s</a>)</p>
                </body>
            </html>
        """ % {
            'url' : redirect_to,
            'headline' : _('Comment saved successfully!'),
            'expl_1' : _("You're comment has been saved successfully. You're being redirected..."),
            'expl_2' : _("In case you're not being redirected, please click"),
            'expl_3' : _('here.')
        })
