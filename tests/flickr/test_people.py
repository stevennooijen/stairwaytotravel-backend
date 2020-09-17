from stairway.flickr.people import parse_flickr_people_info


def test_parse_flickr_people_info():
    """
    Expect correct creation of attribution url.
    """
    expected = {
        "username": "www.tiket2.com",
        "realname": "Tiket2.com",
        "profileurl": "https://www.flickr.com/people/tiket2/",
        "path_alias": "tiket2",
    }

    test_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<rsp stat="ok">\n<person id="61713368@N07" nsid="61713368@N07" ispro="0" can_buy_pro="0" iconserver="65535" iconfarm="66" path_alias="tiket2" has_stats="0">\n\t<username>www.tiket2.com</username>\n\t<realname>Tiket2.com</realname>\n\t<location>Yogyakarta, Indonesia</location>\n\t<timezone label="Bangkok, Hanoi, Jakarta" offset="+07:00" timezone_id="Asia/Bangkok" />\n\t<description>Hi, we are Tiket2.com. Here are our various photos taken during our travels in Asia - mostly in Indonesia, Thailand, Singapore, and Vietnam. All photos are &lt;b&gt;free for you to use&lt;/b&gt; (even for commercial projects) under the Creative Commons Attribution License &lt;b&gt;with credit given back to &lt;a href=&quot;https://www.tiket2.com&quot; rel=&quot;noreferrer nofollow&quot;&gt;www.tiket2.com&lt;/a&gt;&lt;/b&gt;.\n\nYou can find even more travel photographs licensed under Creative Commons Attribution on &lt;b&gt;&lt;a href=&quot;https://www.tiket2.com/creative-commons/&quot; rel=&quot;noreferrer nofollow&quot;&gt;our website&lt;/a&gt;&lt;/b&gt;.</description>\n\t<photosurl>https://www.flickr.com/photos/tiket2/</photosurl>\n\t<profileurl>https://www.flickr.com/people/tiket2/</profileurl>\n\t<mobileurl>https://m.flickr.com/photostream.gne?id=61692038</mobileurl>\n\t<photos>\n\t\t<firstdatetaken>2013-04-30 01:17:35</firstdatetaken>\n\t\t<firstdate>1577770969</firstdate>\n\t\t<count>96</count>\n\t</photos>\n</person>\n</rsp>\n'

    assert expected == parse_flickr_people_info(test_xml)
