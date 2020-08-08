import scrapy


class CharactersSpider(scrapy.Spider):
    name = 'characters'

    allowed_domains = ['disney.fandom.com']
    start_urls = ['https://disney.fandom.com/wiki/Category:Disney_characters']

    def parse(self, response):
        skip_this = [
            'Category:', 'User blog:', 'Disney Prince', 'Disney Princess'
        ]

        for char in response.css('li.category-page__member'):
            name = char.css('a.category-page__member-link::text').get()
            url = char.css('a.category-page__member-link')

            if any(el in name for el in skip_this):
                continue

            yield from response.follow_all(url, self.parse_character)

        next_page = response.css('a.category-page__pagination-next')
        yield from response.follow_all(next_page, self.parse)

    def parse_character(self, response):
        yield {
            'name':
            response.css('h1.page-header__title::text').get(),
            'image':
            response.css('a.image-thumbnail > img::attr(src)').get(),
            'films':
            response.css(
                'div[data-source=films] div.pi-data-value > i > a::text').
            getall(),
        }