#encoding: utf-8

import urllib2

'''
    HTTP proxy only
'''
class ProxyHandler:
    """
        '~' indicates no proxy!
    """
    ROUND_ROBIN = 'round-robin'
    RANDOM = 'random'
    def __init__(self, proxy_list, policy=ROUND_ROBIN):
        self.proxy_list = proxy_list
        self.policy = policy
        self.next_proxy_i = -1

    def _proxy(self):
        '''
            '' indicates no proxy
        '''
        if self.policy == ProxyHandler.ROUND_ROBIN:
            self.next_proxy_i = (self.next_proxy_i + 1) % len(
                                self.proxy_list)
        else:
            pass
        return {'http': self.proxy_list[self.next_proxy_i]} if (
                self.proxy_list[self.next_proxy_i] != '~') else None


    def get_opener(self, opener=None):
        proxy = self._proxy()
        print "proxy: ", proxy
        if opener == None:
            return urllib2.build_opener() if proxy == None else (
                urllib2.build_opener(urllib2.ProxyHandler(proxy)))
        elif proxy != None:
            opener.add_handler(urllib2.ProxyHandler(proxy))
        return opener


if __name__ == '__main__':
    f = open('proxy_ok.txt', 'r')
    proxy = []
    for line in f.readlines():
        proxy += [line.strip(),]
    p = ProxyHandler(proxy)
    for i in xrange(200):
        p.get_opener()
