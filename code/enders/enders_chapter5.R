
#################################################
#################################################
###### 5. MULTIEQUATION TIME-SERIES MODELS ######
#################################################
#################################################

### PAGE 134
library("gdata")
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/TERRORISM.xls")

### FIGURE 5.1
data$date = seq(1970,by=0.25,length.out=nrow(data))
par(mfcol = c(2,1), oma = c(0,0,1,0) + 0.2, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
plot(data$date,data$Domestic,type="l",las=1,xaxs="i",yaxs="i",xlab="",ylab="",tck=.02,main=colnames(data)[2],col="steelblue4",ylim=c(0,400))
plot(data$date,data$Domestic,type="l",las=1,xaxs="i",yaxs="i",xlab="",ylab="",tck=.02,main=colnames(data)[3],col="steelblue4",ylim=c(0,400))

ind = which(date=="1973.25")
data$pure.jump = 1
data$pure.jump[1:ind]=0
data$pulse = 0
data$pulse[ind]=1
data$grad.change = 0
data$grad.change[ind:(ind+3)]=seq(0.25,1,by=0.25)
data$prol.pulse = 0
data$prol.pulse[ind:(ind+3)]=seq(1,0.25,by=-0.25)

space=20
par(mfrow=c(2,2))
plot(data$da[1:space],data$pure[1:space],type="h",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="Pure Jump",col="steelblue4",ylim=c(0,1))
plot(data$da[1:space],data$pulse[1:space],type="h",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="Pulse",col="steelblue4",ylim=c(0,1))
plot(data$da[1:space],data$grad.change[1:space],type="h",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="Gradually Changing",col="steelblue4",ylim=c(0,1))
plot(data$da[1:space],data$prol.pulse[1:space],type="h",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="Prolonged Pulse",col="steelblue4",ylim=c(0,1))

### INTERPRETATION
library("forecast")
auto.arima(data$Transnational,xreg=data$pure.jump,ic="bic")
auto.arima(data$Transnational,xreg=data$pulse,ic="bic")
auto.arima(data$Transnational,xreg=data$grad.change,ic="bic")
auto.arima(data$Transnational,xreg=data$prol.pulse,ic="bic")

auto.arima(data$Domestic,xreg=data$pure.jump,ic="bic")
auto.arima(data$Domestic,xreg=data$pulse,ic="bic")
auto.arima(data$Domestic,xreg=data$grad.change,ic="bic")
auto.arima(data$Domestic,xreg=data$prol.pulse,ic="bic")

auto.arima(data,xreg=data$pure.jump,ic="bic")
auto.arima(data$Domestic,xreg=data$pulse,ic="bic")
auto.arima(data$Domestic,xreg=data$grad.change,ic="bic")
auto.arima(data$Domestic,xreg=data$prol.pulse,ic="bic")


### PAGE 278
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/italy.xls")
data$ENTRY = seq(1971.25,by=0.25,length.out=nrow(data))

ind1 = which(data$ENTRY=="1971.25")
ind2 = which(data$ENTRY=="1989")

par(mfrow=c(2,1))
plot(data$ENTRY,data$Attkit,type="l",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="",col="steelblue4",yaxs="i")
abline(h=0)
acf1 = acf(data$Attkit[ind1:ind2])
acf1

library("MTS")
ccor = ccm(data[,-1],level=TRUE)
ccor$ccm[3,]

plag = 3
X = embed(data$Attkit,plag+1)
summary(lm(data$Slitaly[-c(1:plag)]~X))
summary(lm(data$Slitaly[-c(1:plag)]~X[,-ncol(X)]))
summary(lm(data$Slitaly[-c(1:plag)]~X[,-c(1,ncol(X))]))
summary(lm(data$Slitaly[-c(1:plag)]~X[,3]))
summary(lm(data$Slitaly[-c(1:plag)]~X[,2]))

lm1 = summary(lm(data$Slitaly[-c(1:3)]~0+X[,-c(1,ncol(X))]))
adl.res=lm1$residuals
plot(data$ENTRY[-c(1:3)],adl.res,type="l",las=1,xaxs="i",xlab="",ylab="",tck=.02,main="",col="steelblue4",yaxs="i",ylim=c(-.3,.3))
abline(h=0,lty=2)
acf.res = acf(adl.res)
acf.res

plot(data$Slitaly,type="l")


### PAGE 310
library("vars")
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/TERRORISM.xls")
data$ENTRY = seq(1970,by=0.25,length.out=nrow(data))

library("urca")
colnames(data)
adf.dom = ur.df(data[-c(1:which(data$ENTRY=="1979.25")),2],type="drift",lag=2)
adf.tra = ur.df(data[-c(1:which(data$ENTRY=="1979.25")),3],type="drift",lag=1)
adf.dom@cval
adf.dom
adf.tra

ers.dom = ur.ers(data[-c(1:which(data$ENTRY=="1979.25")),2],model="constant",lag=2)
ers.tra = ur.ers(data[-c(1:which(data$ENTRY=="1979.25")),3],model="constant",lag=1)
ers.dom@cval
ers.dom
ers.tra

VARselect(data[-c(1:which(data$ENTRY=="1979.25")),-1],type="const") # AIC suggests 3 lags
var.terror = VAR(data[-c(1:which(data$ENTRY=="1979.25")),-1],p=3)
summary(var.terror)

fevd.terror = fevd(var.terror,n.ahead=12)
fevd.terror
plot(fevd.terror)

par(mfcol = c(2,2), oma = c(0,0,1,0) + 0.2, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
plot(irf(var.terror),col=1,las=1,xaxs="i",xlab="",ylab="")

k=ncol(data[,-1])
amat = diag(k)
diag(amat) = NA
amat[1,2] = NA
amat # the coefficient b[2,1] is set equal to zero
svar.terror = SVAR(var.terror, estmethod="direct", Amat = amat) 
svar.terror
summary(svar.terror)
plot(irf(svar.terror),col=1,las=1,xaxs="i",xlab="",ylab="")


### PAGE 325
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/Enders_Holt.xls")
data$ENTRY = seq(1974.25,by=0.25,length.out=nrow(data))
k = ncol(data[,-1])

par(mfcol = c(2,2), oma = c(0,0,1,0) + 0.2, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
for (i in 1:k) {
   plot(data$ENTRY,data[,i+1],type="l",las=1,xaxs="i",xlab="",ylab="",tck=.02,col="steelblue4",yaxs="i",main=colnames(data)[i+1])
   abline(h=0,lty=2)
}
var.enders = VAR(na.omit(data[,-1]),p=11)
summary(var.enders)

amat = diag(k)
diag(amat) = NA
amat[2,1] = NA
amat[4, ] = NA
amat
svar.enders = SVAR(var.enders, estmethod="direct", Amat = amat) 
svar.enders
plot(irf(svar.enders,boot=FALSE),col=1,las=1,xaxs="i",xlab="",ylab="")


### PAGE 331
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/Exrates.xls")
head(data)

data$loge_ca = log(data$e_uk)
data$logr_ca = data$loge_ca-log(data$p_uk)+log(data$p_us)
dloge_ca = c(diff(data$loge_ca))
dlogr_ca = c(diff(data$logr_ca))

data$date = as.yearqtr(data$DESCRIPTOR)

X1 = embed(dloge_ca,2)
X2 = embed(data$loge_ca,2)
summary(lm(X1[,1]~X2[-1,2]+X1[,-1]))

df1 = ur.df(dloge_ca,type="drift")
df1@testreg

df = data.frame(r_uk=logr_ca,e_uk=loge_ca)
VAR.PPP = VAR(df,p=3)
summary(VAR.PPP)
fevd(VAR.PPP)

k = ncol(df)
amat = diag(k)
diag(amat) = NA
amat[2,1] = NA
amat
SVAR.PPP = SVAR(VAR.PPP, estmethod = "scoring", Amat = amat, Bmat = NULL,
                max.iter = 100, maxls = 1000, conv.crit = 1.0e-8)
fevd(SVAR.PPP)

plot(irf(SVAR.PPP,boot=FALSE),col=1,las=1,xaxs="i",xlab="",ylab="")

BQ.PPP = BQ(VAR.PPP)
fevd(BQ.PPP)
plot(irf(BQ.PPP,boot=FALSE),col=1,las=1,xaxs="i",xlab="",ylab="")



### PAGE 340
data = read.xls("/Users/user/Google Drive/Website/Book/Enders/QUARTERLY.xls")
dinfl = diff(log(data$CPI))
dlip = diff(log(data$IndProd))
Y = cbind(dlip,dinfl)
VAR.PPP = VAR(Y,p=3)
summary(VAR.PPP)
fevd(VAR.PPP)

SBQ.PPP = BQ(VAR.PPP)
IRF.PPP = irf(SBQ.PPP,boot=TRUE,cumulative=T,n.ahead=25,ortho=T,las=1)

par(mfcol = c(2,1), oma = c(0,0,1,0) + 1, mar = c(0,1,0,0) + 1, mgp = c(0, 0.2, 0))
plot(IRF.PPP$irf$dinfl[,1]/0.01,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4",ylim=c(-1,6),yaxs="i")
lines(IRF.PPP$Lower$dinfl[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$Upper$dinfl[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$irf$dinfl[,2]/0.005,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue1")
lines(IRF.PPP$Lower$dinfl[,2]/0.005,col="steelblue1",lty=2)
lines(IRF.PPP$Upper$dinfl[,2]/0.005,col="steelblue1",lty=2)
abline(h=0)

plot(IRF.PPP$irf$dlip[,1]/0.01,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4",ylim=c(-6,6),yaxs="i")
lines(IRF.PPP$Lower$dlip[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$Upper$dlip[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$irf$dlip[,2]/0.005,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue1")
lines(IRF.PPP$Lower$dlip[,2]/0.005,col="steelblue1",lty=2)
lines(IRF.PPP$Upper$dlip[,2]/0.005,col="steelblue1",lty=2)
abline(h=0)


k = ncol(Y)
amat = diag(k)
diag(amat) = NA
amat[1,2] = NA
amat # inflation is not influencing GDP
SVAR.PPP = SVAR(VAR.PPP, estmethod = "direct", Amat = amat, Bmat = NULL,
                max.iter = 100, maxls = 1000, conv.crit = 1.0e-8)
IRF.PPP = irf(SVAR.PPP,boot=TRUE,cumulative=T,n.ahead=25,ortho=T,las=1)
plot(IRF.PPP$irf$dinfl[,1]/0.01,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4",ylim=c(-4,8),yaxs="i")
lines(IRF.PPP$Lower$dinfl[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$Upper$dinfl[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$irf$dinfl[,2]/0.005,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue1")
lines(IRF.PPP$Lower$dinfl[,2]/0.005,col="steelblue1",lty=2)
lines(IRF.PPP$Upper$dinfl[,2]/0.005,col="steelblue1",lty=2)
abline(h=0)

plot(IRF.PPP$irf$dlip[,1]/0.01,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue4",ylim=c(0,4),yaxs="i")
lines(IRF.PPP$Lower$dlip[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$Upper$dlip[,1]/0.01,col="steelblue4",lty=2)
lines(IRF.PPP$irf$dlip[,2]/0.005,type="l",las=1,xaxs="i",xlab="",ylab="",tck=0.02,col="steelblue1")
lines(IRF.PPP$Lower$dlip[,2]/0.005,col="steelblue1",lty=2)
lines(IRF.PPP$Upper$dlip[,2]/0.005,col="steelblue1",lty=2)
abline(h=0)

### END
