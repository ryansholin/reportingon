from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives

def question_has_new_answer(sender, comment, request, *args, **kwargs):
    site = Site.objects.get_current()
    question = comment.content_object
    commenter_url = """<a href="http://%s/users/%s">%s</a>""" % (site.domain, comment.user_name, comment.user_name) if comment.user_id is not 'NULL' else ''
    question_url = """http://%s/questions/%s/%s""" % (site.domain, question.id, question.slug)
    question_link = """<a href="%s">go to question</a>""" % question_url
    
    subject = "[ReportingOn] Your question has a new answer from %s! (%s)" % (comment.user_name, str(question))
    text_message = """You asked: "%s"\n\n%s answered with: "%s"\n\nSee the question: %s""" % (str(question), comment.user_name, comment.comment, question_url)
    html_message = """<p style="color:#b9b9b9;font-size:16px">Your question</p>
                 <p style="color:#666">%s</p>
                 <br/>
                 <p style="color:#b9b9b9;font-size:16px">%s answered with:</p>
                 <p style="color:#222""><strong>%s</strong><br/><br/>%s</p>""" % (str(question), commenter_url, comment.comment, question_link)
    from_email = settings.DEFAULT_FROM_EMAIL    
    to = question.author.email

    msg = EmailMultiAlternatives(subject, text_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    msg.send()