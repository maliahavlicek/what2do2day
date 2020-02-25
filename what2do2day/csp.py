from functools import wraps

from flask import make_response

SETTINGS_CSP = {
   'default-src': [
       '\'self\'',
   ],
   'script-src': [
       '\'self\'',
       '\'\''
   ]
}


# Same rules for CSP, except for this will only report violations.
SETTINGS_REPORT_CSP = {}
REPORT_URI = '/report-csp-violations'


def make_csp_header(settings, report_uri=None):
   header = ''
   for directive, policies in settings.items():
       header += f'{directive} '
       header += ' '.join(
           (policy for policy in policies)
       )
       header += ';'
   if report_uri:
       header += f' report-uri {report_uri}'
   return header


def csp(func):
   @wraps(func)
   def _csp(*args, **kwargs):
       response = make_response(func(*args, **kwargs))
       if SETTINGS_REPORT_CSP:
           response.headers[
               'Content-Security-Policy-Report-Only'
           ] = make_csp_header(SETTINGS_REPORT_CSP, REPORT_URI)
       if SETTINGS_CSP:
           response.headers[
               'Content-Security-Policy'
           ] = make_csp_header(SETTINGS_CSP, REPORT_URI)
       return response
   return _csp