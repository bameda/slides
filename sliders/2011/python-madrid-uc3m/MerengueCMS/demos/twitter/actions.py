# Copyright (c) 2011 by FOSS - Entel IT
#
# This file is part of Merengue.
#
# Merengue is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Merengue is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Merengue.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.utils.http import urlquote

from merengue.action.actions import ContentAction
from merengue.registry import params

class TweetThisLink(ContentAction):
    name = 'tweetthislink'
    verbose_name = 'Share in Twitter'
    help_text = 'Tweet This share widget'

    config_params = [
        params.Single(
            name='viauser',
            label='Via param (twitter username)',
            default='username',
        ),
    ]

    def get_response(self, request, content):
        via = self.get_config()['viauser'].get_value()
        url = 'http://%s%s' % (Site.objects.get_current().domain, content.public_link())

        return HttpResponseRedirect('http://twitter.com/intent/tweet?original_referer=%s&related=%s&text=%s&url=%s&via=%s' % (urlquote(Site.objects.get_current().domain), urlquote(via), urlquote(content.name), urlquote(url), urlquote(via)))
