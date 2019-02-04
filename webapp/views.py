"""
Django views for www.canonical.com.
"""
from django_template_finder_view import TemplateFinder
from canonicalwebteam.get_feeds import get_json_feed_content
from feedparser import parse


class CanonicalTemplateFinder(TemplateFinder):
    """
    Local customisations of the shared django_template_finder_view.
    """

    def get_context_data(self, **kwargs):
        """
        Get context data fromt the database for the given page.
        """

        # Get any existing context
        context = super(CanonicalTemplateFinder, self).get_context_data(
            **kwargs
        )

        # Add common URL query params to context
        context["product"] = self.request.GET.get("product")
        context["utm_source"] = self.request.GET.get("utm_source")
        context["utm_campaign"] = self.request.GET.get("utm_campaign")
        context["utm_medium"] = self.request.GET.get("utm_medium")

        # Add level_* context variables
        clean_path = self.request.path.strip("/")
        for index, path in enumerate(clean_path.split("/")):
            context["level_" + str(index + 1)] = path

        return context
