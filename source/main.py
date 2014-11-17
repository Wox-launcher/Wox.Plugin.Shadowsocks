#encoding=utf8
import json
import re,os
from wox import Wox,WoxAPI

class Shadowsocks(Wox):

    def get_pac_path(self):
        with open(os.path.join(os.path.dirname(__file__),"config.json"), "r") as content_file:
            config = json.loads(content_file.read())
            return config["pacPath"]

    def add_new_domain(self,domain):
        if not domain:
            WoxAPI.show_msg("Warning","You can't add empty domain")
            return

        r = re.compile(r"domains = {([\s\S]*)};")
        with open(self.get_pac_path(),"r+") as pac:
            pactxt = pac.read()
            existing_domains = r.search(pactxt).group(1)
            domains = json.loads("{" + existing_domains + "}")
            domains[domain] = 1
            newpactxt = r.sub(r"domains = " + json.dumps(domains,indent = 4) +";",pactxt)
            pac.seek(0)
            pac.write(newpactxt)
            pac.truncate()
            WoxAPI.show_msg("Success","{} is now in PAC file".format(domain))

    def query(self,query):
        res = []
        res.append({
            "Title": "add {} to Shadowsocks PAC list".format(query),
            "IcoPath":"kitty.png",
            "JsonRPCAction":{"method": "add_new_domain", "parameters": [query]}
            })
        return res

if __name__ == "__main__":
    Shadowsocks()
