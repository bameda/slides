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


from merengue.block.blocks import Block, ContentBlock
from merengue.registry import params

from django.contrib.sites.models import Site

from plugins.twitter.utils import get_latest_tweets


class LatestTweetsBlock(Block):
    name = 'latesttweets'
    default_place = 'rightsidebar'

    config_params = [
        params.Single(
            name='username',
            label='Twitter username',
            default='username',
        ),
        params.PositiveInteger(
            name='limit',
            label='Number of tweets to show',
            default=3,
        ),
    ]


    def render(self, request, place, context):
        username = self.get_config()['username'].get_value()
        limit = self.get_config()['limit'].get_value()

        tweets_list = get_latest_tweets(username, limit)

        return self.render_block(request,
                                template_name='twitter/block_latesttweets.html',
                                block_title='Latest tweets',
                                context={'tweets_list': tweets_list})



class TweetThisBlock(ContentBlock):
    name = 'tweetthis'
    default_place = 'aftercontenttitle'

    config_params = [
        params.Single(
            name='username',
            label='Via param (twitter username)',
            default='username',
        ),
        params.Single(
            name='counttype',
            label='Twitter count type',
            choices=[('vertical','vertical'),
                     ('horizontal','horizontal'),
                     ('none', 'none')]),
    ]


    def render(self, request, place, content, context, *args, **kwargs):
        viauser = self.get_config()['username'].get_value()
        contenturl = 'http://%s%s' % (Site.objects.get_current().domain, content.public_link())
        contenttitle = content.name
        counttype = self.get_config()['counttype'].get_value()

        return self.render_block(request,
                                template_name='twitter/block_tweetthis.html',
                                block_title='Tweet this',
                                context={'viauser': viauser,
                                        'contenturl': contenturl,
                                        'contenttitle': contenttitle,
                                        'counttype': counttype,})
