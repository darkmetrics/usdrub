
#########################################################
#########################################################
###### 6. COINTEGRATION AND ERRORCORRECTION MODELS ######
#########################################################
#########################################################

### PAGE 366
library("gdata")
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/COINT6.xls")

par(mfcol = c(1,1), oma = c(0,0,1,0) + 0.2, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
plot(data$y,type="s",xaxs="i",las=1,xlab="",ylab="",ylim=c(-12,2),tck=.02)
lines(data$z,lty=2)
lines(data$w,lty=3)
abline(h=0)

lm1 = summary(lm(data$y~data$z+data$w))
lm1
lm2 = summary(lm(data$z~data$y+data$w))
lm2
lm3 = summary(lm(data$w~data$y+data$z))
lm3

library("urca")
### TABLE 6.2
adf1 = ur.df(data$y,lag=0)
adf1@testreg
adf1 = ur.df(data$y,lag=4)
adf1@testreg
adf2 = ur.df(data$z,lag=0)
adf2@testreg
adf2 = ur.df(data$z,lag=4)
adf2@testreg
adf3 = ur.df(data$w,lag=0)
adf3@testreg
adf3 = ur.df(data$w,lag=4)
adf3@testreg

### TABLE 6.3
adf1 = ur.df(lm1$residuals,lag=0)
adf1@testreg
adf1 = ur.df(lm1$residuals,lag=4)
adf1@testreg
adf2 = ur.df(lm2$residuals,lag=0)
adf2@testreg
adf2 = ur.df(lm2$residuals,lag=4)
adf2@testreg
adf3 = ur.df(lm3$residuals,lag=0)
adf3@testreg
adf3 = ur.df(lm3$residuals,lag=4)
adf3@testreg

DATA = data[-1,]
for (i in 1:ncol(DATA)) {
   DATA[,i]=diff(data[,i])
}

e.w = lm3$residuals
VAR(DATA,p=1,exogen=e.w[-length(e.w)])


### PAGE 390
jo.ci = ca.jo(data,type="trace")
summary(jo.ci)
jo.ci@lambda
var.ci = vec2var(jo.ci,r=1)

plot(irf(var.ci))

ecm = jo.ci@V[,1]%*%t(data)
lines(c(ecm),col="steelblue4",lwd=2)

plot(c(ecm),type="l",xaxs="i",las=1,xlab="",ylab="",ylim=c(-1,1),tck=.02)




data = read.xls("/Users/user/Google Drive/Website/Book/Enders/QUARTERLY.xls")
data$DATE=as.yearqtr(data$DATE)
data$DATE

lm1 = summary(lm(data$r10~data$Tbill))
res.lm1 = lm1$residuals
adf1 = ur.df(res.lm1,type="drift",lag=1)
adf1@testreg

lm2 = summary(lm(data$Tbill~data$r10))
res.lm2 = lm2$residuals
adf2 = ur.df(res.lm2,type="drift",lag=1)
adf2@testreg

df = data.frame(data$r10,data$Tbill)
jo1 = ca.jo(df)
summary(jo1)


data = read.xls("/Users/user/Google Drive/Website/Book/Enders/quarterly.xls")
lm1 = summary(lm(data$IndProd~data$M1NSA))
plot(lm1$residuals,type="l")
ur.df(lm1$residuals,type="drift",lag=1)

data = read.xls("/Users/user/Google Drive/Website/Book/Enders/real.xls")
lm1 = summary(lm(log(data$RGDP)~log(data$RCons)))
lm1

### END
