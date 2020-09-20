from typing import Dict

import pytest
from stairway.apis.flickr.people import parse_flickr_people_info


@pytest.mark.parametrize(
    "xml,expected",
    [
        (
            '<?xml version="1.0" encoding="utf-8" ?>\n<rsp stat="ok">\n<person id="61713368@N07" nsid="61713368@N07" ispro="0" can_buy_pro="0" iconserver="65535" iconfarm="66" path_alias="tiket2" has_stats="0">\n\t<username>www.tiket2.com</username>\n\t<realname>Tiket2.com</realname>\n\t<location>Yogyakarta, Indonesia</location>\n\t<timezone label="Bangkok, Hanoi, Jakarta" offset="+07:00" timezone_id="Asia/Bangkok" />\n\t<description>Hi, we are Tiket2.com. Here are our various photos taken during our travels in Asia - mostly in Indonesia, Thailand, Singapore, and Vietnam. All photos are &lt;b&gt;free for you to use&lt;/b&gt; (even for commercial projects) under the Creative Commons Attribution License &lt;b&gt;with credit given back to &lt;a href=&quot;https://www.tiket2.com&quot; rel=&quot;noreferrer nofollow&quot;&gt;www.tiket2.com&lt;/a&gt;&lt;/b&gt;.\n\nYou can find even more travel photographs licensed under Creative Commons Attribution on &lt;b&gt;&lt;a href=&quot;https://www.tiket2.com/creative-commons/&quot; rel=&quot;noreferrer nofollow&quot;&gt;our website&lt;/a&gt;&lt;/b&gt;.</description>\n\t<photosurl>https://www.flickr.com/photos/tiket2/</photosurl>\n\t<profileurl>https://www.flickr.com/people/tiket2/</profileurl>\n\t<mobileurl>https://m.flickr.com/photostream.gne?id=61692038</mobileurl>\n\t<photos>\n\t\t<firstdatetaken>2013-04-30 01:17:35</firstdatetaken>\n\t\t<firstdate>1577770969</firstdate>\n\t\t<count>96</count>\n\t</photos>\n</person>\n</rsp>\n',
            {
                "nsid": "61713368@N07",
                "username": "www.tiket2.com",
                "realname": "Tiket2.com",
                "profileurl": "https://www.flickr.com/people/tiket2/",
                "location": "Yogyakarta, Indonesia",
                "path_alias": "tiket2",
            },
        ),
        (
            '<?xml version="1.0" encoding="utf-8" ?>\n<rsp stat="ok">\n<person id="105105658@N03" nsid="105105658@N03" ispro="1" can_buy_pro="0" iconserver="65535" iconfarm="66" path_alias="" has_stats="1" pro_badge="standard" expire="0">\n\t<username>Rob Oo</username>\n\t<location>NL</location>\n\t<timezone label="Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna" offset="+01:00" timezone_id="Europe/Amsterdam" />\n\t<description>Thanks for stopping by! Your visit, faves and comments are appreciated.\nA camera helps me to be a different observer: I try to photograph how I see, less what I see. I am looking for depth in images. My main focus areas are landscapes and architecture. Look up!\nI believe in sharing using a &lt;a href=&quot;https://creativecommons.org/licenses/by/4.0/&quot; rel=&quot;noreferrer nofollow&quot;&gt;Creative Commons license&lt;/a&gt;. \nIf you would like to use my images under other license conditions, then &lt;a href=&quot;mailto:flickr@roboosterling.nl&quot; rel=&quot;noreferrer nofollow&quot;&gt;email me&lt;/a&gt; FIRST - commercial rates will be applicable. Any revenue will be donated to Creative Commons. \nBe inspired!</description>\n\t<photosurl>https://www.flickr.com/photos/105105658@N03/</photosurl>\n\t<profileurl>https://www.flickr.com/people/105105658@N03/</profileurl>\n\t<mobileurl>https://m.flickr.com/photostream.gne?id=105082604</mobileurl>\n\t<photos>\n\t\t<firstdatetaken>1993-11-01 00:00:00</firstdatetaken>\n\t\t<firstdate>1382695614</firstdate>\n\t\t<count>3874</count>\n\t</photos>\n</person>\n</rsp>\n',
            {
                "nsid": "105105658@N03",
                "username": "Rob Oo",
                "profileurl": "https://www.flickr.com/people/105105658@N03/",
                "location": "NL",
                "path_alias": "",
            },
        ),
    ],
)
def test_parse_flickr_people_info(xml: str, expected: Dict) -> None:
    """
    Expect to retrieve Dict with the available people info in the xml.
    """
    assert expected == parse_flickr_people_info(xml)
