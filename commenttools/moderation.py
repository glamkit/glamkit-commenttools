from django.contrib.comments.moderation import CommentModerator
from django.conf import settings
from django.template import Template, loader, Context
from django.contrib.sites.models import Site
from django.core.mail import send_mail


class SuperCommentModerator(CommentModerator):
    '''
    Moderator to be used with the django.contrib.comments framework.
    Partly inspired, though largely modified, from http://github.com/bartTC/django-comments-spamfighter
    '''

    # Akismet parameters -----------------------------------------

    use_akismet = False

    # If Akismet marks this message as spam, delete it instantly (False) or
    # add it to the comment the moderation queue (True). Default is True.
    akismet_moderate = True
 
    # Fields for the default django.contrib.comment.models.Comment but can be
    # overriden
    akismet_fields = {
        'comment_author': 'name',
        'comment_author_email': 'email',
        'comment_author_url': 'url',
        'comment_content': 'comment',
        }
    
    # Email notification parameters -----------------------------------------

    email_notification = False
        
    # If True, the notification email will only be sent if the comment is public.
    email_only_public_comments = True
    
    # Template used to render the email body.
    email_body_template = 'commenttools/comment_notification_email.txt'
    
    # Template used to render the email subject.
    email_subject_template_string = '[{{ site.name }}] New comment posted on "{{ content_object }}"'
    
    def _ask_akismet(self, comment, content_object, request):
        # Return True if akismet marks this comment as spam.
        from stopspam.utils import akismet_check
        akismet_data = {
                'comment_author': '' if not 'comment_author' in self.akismet_fields else getattr(comment, self.akismet_fields['comment_author']),
                'comment_author_email': '' if not 'comment_author_email' in self.akismet_fields else getattr(comment, self.akismet_fields['comment_author_email']),
                'comment_author_url': '' if not 'comment_author_url' in self.akismet_fields else getattr(comment, self.akismet_fields['comment_author_url']),
                'comment_content': '' if not 'comment_content' in self.akismet_fields else getattr(comment, self.akismet_fields['comment_content']),
            }
        
        return akismet_check(request=request, **akismet_data)
 
    def allow(self, comment, content_object, request):
        """
        Determine whether a given comment is allowed to be posted on
        a given object.
         
        Return ``True`` if the comment should be allowed, ``False
        otherwise.
        """
        if self.use_akismet:
            if not self.akismet_moderate:
                # Return False if akismet marks this comment as spam.
                if self._ask_akismet(comment, content_object, request):
                    return False
 
        return super(SuperCommentModerator, self).allow(comment, content_object, request)
 
    def moderate(self, comment, content_object, request):
        """
        Determine whether a given comment on a given object should be
        allowed to show up immediately, or should be marked non-public
        and await approval.
         
        Return ``True`` if the comment should be moderated (marked
        non-public), ``False`` otherwise.
        """
        if self.use_akismet:
            if self.akismet_moderate:
                # Return True if akismet marks this comment as spam and we want to moderate it.
                if self._ask_akismet(comment, content_object, request):
                    return True
 
        return super(SuperCommentModerator, self).moderate(comment, content_object, request)
    
    def get_notified_moderators(self, comment, content_object, request):
        '''
        Custom hook to offer control over who will receive the email notification.
        '''
        return settings.MANAGERS
    
    def email(self, comment, content_object, request):
        """
        Send email notification of a new comment to site staff when email
        notifications have been requested.
        Overriden from django.contrib.comments

        """
        if not self.email_notification or (self.email_only_public_comments and not comment.is_public):
            return
        
        recipient_list = [moderator_tuple[1] for moderator_tuple in self.get_notified_moderators(comment, content_object, request)]
        t = loader.get_template(self.email_body_template)
        c = Context({ 'comment': comment,
                      'content_object': content_object })
        body = t.render(c)
        
        t = Template(self.email_subject_template_string)
        c = Context({'site': Site.objects.get_current(),
                     'content_object': content_object})
        subject = t.render(c)

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
        
        
class AkismetCommentModerator(SuperCommentModerator):
    use_akismet = True

class EmailNotificationCommentModerator(SuperCommentModerator):
    email_notification = True