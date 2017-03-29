from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import sys

class EmailService():
    
    
    def send_email_password(self, template, subject, to):        
        plaintext = get_template('toolshareapp/email/' + template + '.txt')
        html = get_template('toolshareapp/email/' + template + '.html')
        
        context = Context()
        
        from_email = 'from@toolshare.com'
        text_content = plaintext.render(context)
        html_content = html.render(context)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        
        try: 
            msg.send()
        except:
            print('Could not send email!!', file = sys.stderr)
            
    def send_email(self, template, subject, to, reservation):        
        plaintext = get_template('toolshareapp/email/' + template + '.txt')
        html = get_template('toolshareapp/email/' + template + '.html')
        
        context = Context({ 'reservation': reservation,
                            'tool': reservation })
        
        from_email = 'from@toolshare.com'
        text_content = plaintext.render(context)
        html_content = html.render(context)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        
        try: 
            msg.send()
        except:
            print('Could not send email!!', file = sys.stderr)
            
    
    def send_email_tool(self, template, subject, tool):        
        plaintext = get_template('toolshareapp/email/' + template + '.txt')
        html = get_template('toolshareapp/email/' + template + '.html')
        
        context = Context({ 'tool': tool})
        
        from_email = 'from@toolshare.com'
        text_content = plaintext.render(context)
        html_content = html.render(context)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [tool.owner.email])
        msg.attach_alternative(html_content, "text/html")
        
        try: 
            msg.send()
        except:
            print('Could not send email!!', file = sys.stderr)
