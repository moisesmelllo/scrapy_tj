import scrapy
from interface import interface
import subprocess


class TjspspiderSpider(scrapy.Spider):
    name = "tjspfinal"
    allowed_domains = ["esaj.tjsp.jus.br"]

    def start_requests(self):
        start_urls = [interface()]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response, **kwargs):
        processos = response.xpath("//div[@class='row unj-ai-c home__lista-de-processos']")

        for processo in processos:
            parte_processo = processo.xpath(".//label[@class='unj-label tipoDeParticipacao']/text()").get()
            if parte_processo is None:
                parte_processo = processo.xpath(".//label[@class='unj-label tipoDeParticipacao']/text()")
            link_processo = processo.xpath(".//a[@class='linkProcesso']//@href").get()
            link_processo_url = 'https://esaj.tjsp.jus.br' + link_processo
            yield response.follow(link_processo_url, callback=self.parse_processo_page,
                                  meta={'parte_processo': parte_processo})

        next_page = response.xpath("//a[@title='Próxima página']//@href").get()

        if next_page is not None:
            next_page_url = 'https://esaj.tjsp.jus.br' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_processo_page(self, response, **kwargs):
        parte_processo = response.meta.get('parte_processo', None)

        yield {
            'numero_do_processo': response.xpath(".//span[@id='numeroProcesso']/text()").get(),
            'valor_do_processo': response.xpath(".//div[@id='valorAcaoProcesso']/text()").get(),
            'parte_no_processo': parte_processo
        }


subprocess.run(['scrapy', 'crawl', 'tjspfinal', '-o', 'dados.csv'])
