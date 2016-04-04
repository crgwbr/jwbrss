from feedgen.feed import FeedGenerator
import requests


fg = FeedGenerator()
fg.load_extension('podcast')
fg.podcast.itunes_category('Religion & Spirituality', 'Christianity')

resp = requests.get('http://mediator.jw.org/v1/categories/E/LatestVideos?detailed=1')
data = resp.json()

fg.title( data['category']['name'] )
fg.description( data['category']['description'] )
fg.link(href='https://crgwbr.com/jwb.atom', rel='self')

for item in data['category']['media']:
    fe = fg.add_entry()

    fe.id( item['guid'] )
    fe.title( item['title'] )
    fe.description( item['description'] )
    fe.published( item['firstPublished'] )

    files = item['files']
    files.sort(key=lambda file: file['bitRate'], reverse=True)
    file = files[0]
    url = file['progressiveDownloadURL']
    mime = file['mimetype']

    fe.enclosure(url, 0, mime)
    fe.link(href=url, type=mime)

    for size in ('wsr', 'wss', 'sqr', 'sqs'):
        try:
            fe.podcast.itunes_image( item['images'][size]['lg'] )
            break
        except KeyError:
            pass

fg.rss_str(pretty=True)
fg.rss_file('podcast.xml')
