
#####################################
#####################################
###### 3. MODELLING VOLATILITY ######
#####################################
#####################################

### PAGE 134
library("gdata")
library("rugarch")
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/RGDP.xls")
data$DATE=as.Date(as.character(data$DATE))

par(mfcol = c(1,1), oma = c(0,0,1,0) + 0.2, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
plot(data$DATE,data$RGDP,type="l",xaxs="i",las=1,xlab="",ylab="",col="steelblue4",tck=0.02)
t = 1:nrow(data)
lm1 = lm(data$RGDP~t+I(t^2)+I(t^3))
summary(lm1)
lines(data$DATE,lm1$fitted.values,col="steelblue4",lty=2)


### PAGE 194
dlgdp = diff(log(data$RGDP))
X = embed(dlgdp,2)
lm2 = lm(X[,1]~X[,-1])
summary(lm2)

par(mfrow=c(3,1))
plot(lm1$residuals,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
abline(h=0,lty=2)
acf1 = acf(lm1$residuals,lag=12,xlab="",ylab="",las=1,tck=.02)
pacf1 = pacf(lm1$residuals,lag=12,xlab="",ylab="",las=1,tck=.02)

par(mfrow=c(3,1))
plot(dlgdp,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
abline(h=0,lty=2)
acf1 = acf(dlgdp,lag=12,xlab="",ylab="",las=1,tck=.02)
pacf1 = pacf(dlgdp,lag=12,xlab="",ylab="",las=1,tck=.02)

### PAGE 205
nburn = 50
n = 100 + nburn
rep = 10000
t.val = NULL
for (i in 1:rep) {
   y = cumsum(rnorm(n,0,1))
   y = y[-c(1:nburn)]
   dy = diff(y)
   lm1 = summary(lm(dy~y[-length(y)]),xaxs="i")
   plot(y,type="l")
   t.val[i] = lm1$coefficients[2,3]
   if (i%%500==0) {
      print(paste0(round(i/rep*100,2),"%"))
   }
}
### FIGURE 4.6
par(mfrow=c(1,1))
plot(density(t.val),las=1,xaxs="i",type="l",xlab="",ylab="",main="",col="steelblue4")

### PAGE 210
library("urca")
df.gdp = ur.df(log(data$RGDP),lag=1,type="trend")
df.gdp@testreg


### PAGE 219
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/LAGLENGTH.XLS")
data$time
adf1 = ur.df(data$Y,type="trend",lag=4)
adf1@testreg


data = read.xls("/Users/user/Google Drive/Website/Book/Enders/BREAK.XLS")
par(mfrow=c(2,1))
plot(data$Y1,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
plot(data$Y2,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
acf.y1 = acf(data$Y1)
acf.y1
df1 = ur.df(data$Y1,type="none",lag=0)
df1@testreg
df2 = ur.df(data$Y1,type="drift",lag=0)
df2@testreg
df3 = ur.df(data$Y1,type="trend",lag=0)
df3@testreg

### PERRON PROCEDURE
par(mfrow=c(1,1))
plot(data$Y1,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")

ind = which(max(abs(diff(data$Y1)))==abs(diff(data$Y1)))
DATA = data.frame(Y=data$Y1,Ylag=c(NA,embed(data$Y1,2)[,-1]))
colnames(DATA)=c("Y","Ylag")
tau = ind+1
tau
DATA$Dl=1
DATA$Dl[1:tau]=0
DATA$Dp=0
DATA$Dp[tau]=1
DATA$t = 1:nrow(DATA)

lm1 = lm(Y~Ylag+t+Dp+Dl,DATA)
summary(lm1)

par(mfrow=c(1,1))
plot(DATA$Y[-1],type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02)
lines(lm1$fitted.values,col="steelblue4",lty=1)


###PAGE 242
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/ERSTEST.XLS")
data$ylag = c(0,embed(data$y,2)[,-1])

alpha = 1-13.5/200
alpha
ytilde = data$y-alpha*data$ylag

plot(data$y_tilde,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02)
lines(ytilde,col="steelblue4",lty=2)

n = length(ytilde)
t = 1:n
z1t = c(1,rep(1-alpha,n-1))
z2t = alpha+(1-alpha)*t
z2t

lm2 = summary(lm(ytilde~0+z1t+z2t))
lm2

yd = c(data$y-lm2$coefficients[,1]%*%t(cbind(1,t)))
plot(data$yd,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02)
lines(yd,col="steelblue4",lty=2)
Yd = embed(yd,2)
ers.df = ur.df(yd,lag=0,type="none")
ers.df@testreg     

ers.test = ur.ers(data$y,lag=0,type="DF-GLS",model="trend")
ers.test@testreg

df1 = ur.df(data$y,type="trend",lag=0)
df1@testreg


### PAGE 251
### BEVEREGE NELSON DECOMPOSITION
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/REAL.XLS")
data$DATE=as.Date(as.character(data$DATE))
data$LGDP = log(data$RGDP)
data$LGDP[1]
DLGDP = diff(data$LGDP)
Y = embed(DLGDP,2)
lm1 = summary(lm(Y[,1]~Y[,-1]))

SC=PC=0
s = 100 # 100 forecasts
for (j in 2:length(DLGDP)) {
   fore = NULL
   for (i in 1:(s)) {
      fore = c(fore,lm1$coefficients[2,1]^(i)*DLGDP[j])
   }
   SC[j]=sum(fore)
   PC[j]=data$LGDP[j]+SC[j]
}
### FIGURE 4.11: PANEL A
plot(data$DATE[-c(1:51)],SC[-c(1:50)],type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
abline(h=0,lty=2)

### PAGE 253
library("mFilter")
plot(data$RGDP,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
hp.RGDP = hpfilter(log(data$RGDP),freq=1600,type="lambda")
hp.RCons = hpfilter(log(data$RCons),freq=1600,type="lambda")
hp.RInv = hpfilter(log(data$Rinv),freq=1600,type="lambda")

### FIGURE 4.11: PANEL B
plot(data$DATE[-c(1:50)],hp.RGDP$cycle[-c(1:50)],type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4")
abline(h=0,lty=2)

### PAGE 254
plot(data$DATE,data$RGDP/1000,type="l",las=1,xaxs="i",yaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4",ylim=c(0,14))
lines(data$DATE,exp(hp.RGDP$trend)/1000,col="steelblue4",lty=2)
lines(data$DATE,data$RCons/1000,col="steelblue2")
lines(data$DATE,exp(hp.RCons$trend)/1000,col="steelblue2",lty=2)
lines(data$DATE,data$Rinv/1000,col="steelblue1")
lines(data$DATE,exp(hp.RInv$trend)/1000,col="steelblue1",lty=2)

### END
