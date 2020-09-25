import scrapy

class cancer(scrapy.Spider):
      name = "cancer" #spider name
      start_urls = ['http://db.idrblab.net/ttd/data/target/details/t14597/']

      def parse(self,response):
            page = response.url.split('/')[-1] #cancer target id
            filename = "cancer-%s.txt" %page

            ex=[] #用于储存所有提取的文字
            ex.append(response.xpath('//div[starts-with(@class,"target")]/text()').extract())

            text = str(ex[0]).split("', '")#提取以逗号分隔的 每一个小项

            for i in range(len(text)):
                  text[i]=text[i].replace("\n","")
                  print(text[i])
            #write in file 
            with open (filename, "w") as f:
                  for i in range(len(text)):
                        f.write(text[i])
            self.log("保存文件: %s" %filename)
