import scrapy

#funcition:根据start_url 完整爬取单页text 并进行轻微整理 写入成txt
#todo：1爬取prostate cancer全部的target id
#         2增加存储到mysql

class cancer(scrapy.Spider):
      name = "cancer" #spider name
      start_urls = ['http://db.idrblab.net/ttd/search/ttd/target-drug?field_moa=&field_therapeutic_class=&name=&name_1=&name_2=&search_api_fulltext=&search_api_fulltext_1=&search_api_fulltext_2=prostate%20cancer&page=0']
      #初始URL
      word = '?field_moa=&field_therapeutic_class=&name=&name_1=&name_2=&search_api_fulltext=&search_api_fulltext_1=&search_api_fulltext_2=prostate%20cancer&page='
      #用来replace url 得到page= 的值
      page_end = 0 #控制爬取数量 自动获取最大页码

      # def parse(self,response):  #获取每一页的URL
      #       #获取最后一页的index
            
      #       end =  response.xpath('//*[@id="fixed-width-page"]/div/main/div[2]/nav[1]/ul/li[12]/a//@href').extract()[0] #last的标签
      #       end = int(end.replace(self.word,''))  #提取出page=
      #       self.page_end = end #将控制页数的值传给成员
      #       #url前缀
      #       prefix = 'http://db.idrblab.net/ttd/search/ttd/target-drug?field_moa=&field_therapeutic_class=&name=&name_1=&name_2=&search_api_fulltext=&search_api_fulltext_1=&search_api_fulltext_2=prostate%20cancer&page='
            
      #       for num in range(self.page_end+1):  #页码从0开始一直到page_end
      #             url=prefix+str(num)
      #             yield scrapy.Request(url=url,callback=self.parse_url) #拼接并传递
            
            
            
      ''' #缺陷方案：根据选页栏爬取会缺第10页
            for con in response.xpath('//*[@id="fixed-width-page"]/div/main/div[2]/nav[1]/ul/li/a'):  #下一页的标签
                  if con.xpath('@href').extract_first():  #如果下一页存在
                        url='http://db.idrblab.net/ttd/search/ttd/target-drug'+str(con.xpath('@href').extract_first()) #拼接url
                  yield scrapy.Request(url,callback=self.parse_url) #传递下一页
            #print(checked)

      '''      
      
      def parse(self,response):  #获取当前页target_info的url
            now = response.url.replace(self.word,'')
            now = int(now.replace('http://db.idrblab.net/ttd/search/ttd/target-drug',''))+1
            print("当前是第%d页*********************************************************"%now)
            for web in response.xpath('//*[@id="fixed-width-page"]/div/main/div[2]/table/tbody/tr[1]/th[1]/span/a'):  #爬到一个url的list
                  if web.xpath('@href').extract_first():#如果还有当前这条url
                        url='http://db.idrblab.net'+str(web.xpath('@href').extract_first()) #拼接
                        print("正在爬：=====================",web.xpath('@href').extract_first())
                        yield scrapy.Request(url, callback=self.parse_page) #传递
            

      
      def parse_page(self,response): #获取当前target的text数据
            page = response.url.split('/')[-1] #cancer target id
            filename = "prostate_cancer-%s.txt" %page


            for item in response.xpath('//tbody//tr'):
                  label=item.xpath('//tbody//th//text()').extract()
                  text=item.xpath('//tbody//td//text()').extract()
            print("当前爬取页：=====================",page)
            text = [i for i in text if i !='' and len(i) >=2]
            with open(filename, "w") as f:
                 for i in range(len(text)):
                        text[i]=text[i].strip()
                        text[i]=text[i].replace('\n','')
                        text[i]=text[i].replace('\t','')
                        text[i]=text[i].replace('],    [','')
                        text[i]=text[i].replace('],  [','')
                        text[i]=text[i].replace('[+]','')
                        text[i]=text[i].replace('      ','')
                        f.write(text[i].strip()+'\n')
            print("已完成爬取页：=====================",page)
            

      ''' VERSION 1  提取完整但并未分开

            ext=[]   #储存xpath提取出的原始数据
            ext.append(response.xpath('//tbody//tr//text()').extract())

            one=str(ext[0])   #将这一整段都转为字符串方便后面写入和操作

            one=one.replace("\\n","")  #整理一下 增加可读性
            one=one.replace("    ","")
            one=one.replace("      ","")
            one=one.replace("        ","")

            with open (filename, "w") as f: #写入 
                  f.write(one)
      '''

      '''  VERSION 0.5 提取不完整

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
