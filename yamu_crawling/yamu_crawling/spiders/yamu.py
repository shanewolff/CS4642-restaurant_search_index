import scrapy
from scrapy.selector import Selector


class YamuSpider(scrapy.Spider):
    name = 'yamu'
    start_urls = ['https://www.yamu.lk/place/restaurants']

    def parse(self, response):
        # follow links to restaurant pages
        for a in response.css('ul.media-list a.front-group-item'):
            yield response.follow(a, self.parse_restaurant)

        # follow pagination links
        a = response.css('ul.pagination li a')[-1]
        yield response.follow(a, self.parse)

    def parse_restaurant(self, response):

        url = response.url
        name = response.css('div.place-title-box h2::text').extract_first()
        excerpt = response.css('p.excerpt::text').extract_first()
        yamu_review = response.css('div.readmore-content div.bodycopy p::text').extract()
        user_reviews = response.css('div#user-reviews div#reviews-all p.comment-text::text').extract()
        user_comments = response.css('div#comments p.comment-text::text').extract()
        contact = response.css('div.info')[0].css('div.time-range a::text').extract_first()
        address = response.css('div.info')[0].css('p::text').extract()[1]
        directions = response.css('div.info')[0].css('p::text').extract()[3]
        open_html = response.css('div.info')[1].css('div.time-range span::attr(title)').extract_first()
        opening_days = Selector(text=open_html).css('strong::text').extract()
        opening_hours = Selector(text=open_html).css('body::text').extract()
        cuisine = response.css('div.info')[1].css('p')[2].css('a::text').extract()
        price_range = response.css('div.info')[1].css('p')[4].css('a::text').extract_first()
        dishes = response.css('div.info')[1].css('p')[6].css('a::text').extract()
        overall_rating = response.css('dl.dl-horizontal span::text').extract()[0]
        quality_rating = response.css('dl.dl-horizontal span::text').extract()[1]
        service_rating = response.css('dl.dl-horizontal span::text').extract()[2]
        ambience_rating = response.css('dl.dl-horizontal span::text').extract()[3]
        near_by_places_names = response.css('div.list-group li.list-group-item strong::text').extract()
        near_by_places_addresses = response.css('div.list-group li.list-group-item div::text').extract()
        near_by_places_distances = response.css('div.list-group li.list-group-item small::text').extract()
        similar_places = response.css('div.topten strong::text').extract()

        file_name = name.replace(" ", "")
        with open('crawledData/yamuDataSet2/' + file_name + '.txt', 'a+') as f:
            f.write('url: {0}\n'
                    'name: {1}\n'
                    'excerpt: {2}\n'
                    'yamu_review: {3}\n'
                    'user_reviews: {4}\n'
                    'user_comments: {5}\n'
                    'contact: {6}\n'
                    'address: {7}\n'
                    'directions: {8}\n'
                    'opening_days: {9}\n'
                    'opening_hours: {10}\n'
                    'cuisine: {11}\n'
                    'price_range: {12}\n'
                    'dishes: {13}\n'
                    'overall_rating: {14}\n'
                    'quality_rating: {15}\n'
                    'service_rating: {16}\n'
                    'ambience_rating: {17}\n'
                    'near_by_places_names: {18}\n'
                    'near_by_places_addresses: {19}\n'
                    'near_by_places_distances: {20}\n'
                    'similar_places: {21}\n'
                    .format(url,
                            name,
                            excerpt,
                            yamu_review,
                            user_reviews,
                            user_comments,
                            contact,
                            address,
                            directions,
                            opening_days,
                            opening_hours,
                            cuisine,
                            price_range,
                            dishes,
                            overall_rating,
                            quality_rating,
                            service_rating,
                            ambience_rating,
                            near_by_places_names,
                            near_by_places_addresses,
                            near_by_places_distances,
                            similar_places
                    ))

        yield {
                'url': url,
                'name': name,
                'excerpt': excerpt,
                'yamu_review': yamu_review,
                'user_reviews': user_reviews,
                'user_comments': user_comments,
                'contact': contact,
                'address': address,
                'directions': directions,
                'opening_days': opening_days,
                'opening_hours': opening_hours,
                'cuisine': cuisine,
                'price_range': price_range,
                'dishes': dishes,
                'overall_rating': overall_rating,
                'quality_rating': quality_rating,
                'service_rating': service_rating,
                'ambience_rating': ambience_rating,
                'near_by_places_names': near_by_places_names,
                'near_by_places_addresses': near_by_places_addresses,
                'near_by_places_distances': near_by_places_distances,
                'similar_places': similar_places
            }
