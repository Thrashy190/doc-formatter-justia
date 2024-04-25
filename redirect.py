f = open("code.txt", "r")
urls = f.read().split()

for url in urls:
    print(f"RewriteRule ^/?(amp/)?{url} - [G]")