class ComParisonAns(object):
    def copyenkg(self,tstr):
        if tstr[-1]==" " or tstr[-1]=="\n":
            tstr=tstr[:-1]
        return tstr
    def comparison(self,ans,out,max=10000,gle=True):
        if len(out)>max:
            return 2#oe
        if gle:
            if len(ans)!=0:
                ans=self.copyenkg(ans)
            if len(ans)!=0:
                ans=self.copyenkg(ans)
            if len(out)!=0:
                out=self.copyenkg(out)
            if len(out)!=0:
                out=self.copyenkg(out)
        if ans==out:
            return 0#正确
        acs=0
        if len(out)==0:
            return -1
        if len(out)!=len(ans):
            return -1
        for i in range(len(ans)):
            if ans[i]==out[i]:
                acs=acs+1
        if acs==0:
            return -1#全错
        return 1#错一部分
