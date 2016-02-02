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
    fe.id( item['naturalKey'] )
    fe.title( item['title'] )
    fe.description( item['description'] )

    files = item['files']
    files.sort(key=lambda file: file['bitRate'], reverse=True)
    file = files[0]
    fe.enclosure(file['progressiveDownloadURL'], 0, file['mimetype'])

fg.rss_str(pretty=True)
fg.rss_file('podcast.xml')
