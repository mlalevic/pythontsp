# -*- coding: UTF-8 -*-import web render = web.template.render('templates/') urls = (     '/', 'index',    '/coordinates', 'coordinates') import jsonimport urllibimport osbingKey = os.getenv('BINGKEY') #need to configure this in azure, if running it from command line prior to doing python code.py run SET BINGKEY=your keymaxAddresses = 10 #one address per line, limit to 10urlPrefix = 'http://dev.virtualearth.net/REST/v1/Locations?query='urlSuffix = '&maxResults=1&key=' + bingKeyclass index:     def GET(self):        return render.index()        #i = web.input(addresses = None)        #if i.addresses is None or len(i.addresses.strip()) == 0:        #            #else:        #    print urllib.unquote_plus(i.addresses)        #    return render.index(getCoordinates(i.addresses))class coordinates:    def GET(self):        print 'in'        i = web.input(addresses = None)        if i.addresses is None or len(i.addresses.strip()) == 0:            return ""            else:            print urllib.unquote_plus(i.addresses)            return getCoordinates(i.addresses)def getCoordinates(addresses):    addressQueries = [urllib.quote(address.strip()) for address in addresses.splitlines() if address.strip() <> '']    addressQueries = addressQueries[:maxAddresses]    urls = [urlPrefix + query + urlSuffix for query in addressQueries]    jsonresults = [json.loads(result) for result in [urllib.urlopen(url).read() for url in urls]]    result = [processResult(j) for j in jsonresults]    return json.dumps(result)   def processResult(data):    if data['statusCode'] <> 200:        return ("error", data.statusCode)    #do some processing    if len(data['resourceSets']) == 0:        return ('error', 'no results')    result = data['resourceSets'][0]    if result['estimatedTotal'] <= 0:        return ('error', 'no items')    result = result['resources'][0]    return ('success', result['address']['formattedAddress'], result['point']['coordinates'])def wsgiHandler():     return web.application(urls, globals(), autoreload=False).wsgifunc() if __name__ == "__main__":     app = web.application(urls, globals())     app.run()