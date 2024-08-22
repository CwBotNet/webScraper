import scrapy



class NoberoSpider(scrapy.Spider):
    name = "nobero"
    allowed_domains = ["nobero.com"]
    start_url=["https://nobero.com/pages/men"] 
    
    # Method to start requests
    def start_requests(self):
         # Start URLs where the spider will begin its scraping
        urls = [    
                  "https://nobero.com/collections/men-oversized-t-shirts",
                  "https://nobero.com/collections/pick-printed-t-shirts",
                  "https://nobero.com/collections/best-selling-co-ord-sets",
                  "https://nobero.com/collections/fashion-joggers-men",
                  "https://nobero.com/collections/mens-shorts-collection",
                  "https://nobero.com/collections/plus-size-t-shirts"
                  ]
            
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
      # Method to parse the response from each request   
    def parse(self, response):
        # Extract category name from URL
        page = response.url.split("/")[-1]
        # Select product cards on the page
        cards = response.css(".product_link")
        
        # Iterate over each product card
        for card in cards:
            # Extract image URL from the card
            image_link = card.css("#image-container img")
            
            # Extract product details from the card
            product_name= card.css("#product-info")
            product_price = card.css("#product_price")
            product_priceDrop = card.css(".price-drop")
            url_link= card.css("a.product_link::attr(href)")
            
            # Yield the extracted data as a dictionary
            yield {
                "category" :page,
                "url": url_link.get().replace("/products", "https://nobero.com/products"),
                "image_link": image_link.attrib["src"].replace("//nobero.com/cdn","https://nobero.com/cdn"),
                "name":product_name.css("h3::text").get().strip(),
                "price":{
                    "regular": product_price.css("#price__regular>span>spanclass::text").get().strip("₹"),
                    "sale": product_price.css("#product__sale>span>spanclass::text").get().strip("₹"),
                    "discount": product_price.css("#discount>span::text").get().strip()
                },
                "price-drop": product_priceDrop.css("p::text").get().strip()
            }                
             
