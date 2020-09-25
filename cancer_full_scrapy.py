import scrapy

class cancer(scrapy.Spider):
      name = "cancer" #spider name
      start_urls = ['http://db.idrblab.net/ttd/data/target/details/t14597/']


      def parse(self,response):
            page = response.url.split('/')[-1] #cancer target id
            filename = "cancer-%s.txt" %page
            ext=[]   #储存xpath提取出的原始数据
            ext.append(response.xpath('//tbody//tr[position()]//text()').extract())

            one=str(ext[0])   #将这一整段都转为字符串方便后面写入和操作

            one=one.replace("\\n","")  #整理一下 增加可读性
            one=one.replace("    ","")
            one=one.replace("      ","")
            one=one.replace("        ","")

            with open (filename, "w") as f: #写入 
                  f.write(one)


            '''
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
            '''
#Disease展开的3项
#//tbody//tr[@class="child-T14597-disease"]//text()

#大部分的非展开文字
#//div[starts-with(@class,"target")]/text()'

#全部的左侧标题
#//th[starts-with(@class,"")]
