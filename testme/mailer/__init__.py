"""
After run queue_html_text_email, they will be stored in the local maildir folder,
in order to send out to target user, we need to run qp process explicitly:
    qp --config qp.ini
"""
import premailer

from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from pyramid.threadlocal import get_current_request

from zope import component

logger = __import__('logging').getLogger(__name__)


def queue_html_text_email(template,
                          subject,
                          recipients,
                          template_args={},
                          attachments=None,
                          request=None):
    """
    Send html/text email to a queue.
    https://docs.pylonsproject.org/projects/pyramid-mailer/en/latest/#html-email
    """
    request = request or get_current_request()

    html_body = render(template + ".pt", template_args, request=request)
    text_body = render(template + ".mak", template_args, request=request)

    html_body = premailer.transform(html_body)

    mailer = get_mailer(request)

    sender = mailer.default_sender

    logger.info("Sending email from %s to %s.", sender, ','.join(recipients))

    message = Message(subject=subject,
                      sender=sender,
                      recipients=recipients,
                      body=text_body,
                      html=html_body,
                      attachments=attachments)
    mailer.send_to_queue(message)
