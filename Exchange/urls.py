from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.shortcuts import redirect

def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Exchange.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Authentication
    url(r'^login/$',
        anonymous_required(login),
        {
            'template_name': 'auth/login.html',
            'authentication_form': AuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('incidents.api_url')),
    url(r'^manage/', include('incidents.admin_url')),
    url(r'^a-ppl-e/', include('a_ppl_e.urls')),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)