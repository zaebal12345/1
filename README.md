
//@version=5
strategy('Zer0 Trader - C_TweezerTopBearish with TP LONG C_UpTrend', overlay=true, default_qty_type=strategy.fixed, default_qty_value=45000, initial_capital=500, commission_value=0.07, pyramiding=1, calc_on_every_tick=false, slippage=0)


length = 14
length1 = 25
src = close
days = 2//input(title='ТФ трендовой линии', defval='2')
tpplus2 = input.float(1, step=0.1, title='% Stop For LONG')
calcLength = 3
smoothLength = 3
long = 25
short3 = 13
signal = 13

// Moment Indicator
oscl = 0
for i = 1 to length by 1
    oscl += (src > src[i] ? 1 : src < src[i] ? -1 : 0)
    oscl

normFactor = 40 / length
oscl *= normFactor

ma = ta.ema(oscl, calcLength)
tmo = ta.ema(ma, smoothLength)
signal_tmo = ta.ema(tmo, smoothLength)
hist = tmo - signal_tmo
rsiMA =  ta.ema(tmo, length1)
rsiMA1 =  ta.sma(tmo, length1)

// True Strength Index
price = close
double_smooth(src, long, short3) =>
	fist_smooth = ta.ema(src, long)
	ta.ema(fist_smooth, short3)
pc = ta.change(price)
double_smoothed_pc = double_smooth(pc, long, short3)
double_smoothed_abs_pc = double_smooth(math.abs(pc), long, short3)
tsi_value = 100 * (double_smoothed_pc / double_smoothed_abs_pc)
tsi1 = tsi_value
signal22 = signal
signal_tsi = ta.ema(tsi1, signal22)

// Calculate Slope Angle for signal_tsi
slope_angle = math.atan(ta.change(signal_tsi)) * (180 / math.pi)
slope_label = " " + str.tostring(slope_angle, "#.##") + "°"





// === GENERAL INPUTS ===
// Интервалы
short1 = input.int(50, minval=1)
long2 = input.int(200, minval=1)

// Выбор типа скользящих средних
maTypeInput = input.string("SMA", title="Выберите тип скользящей средней", options=["SMA", "HMA"])



// Функция для расчета скользящих средних
maFunction(type, source, length) =>
    float ma = na
    if type == "SMA"
        ma := ta.sma(source, length)
    else if type == "HMA"
        ma := ta.hma(source, length)
    ma

// Расчет короткой и длинной скользящей средней
short = maFunction(maTypeInput, close, short1)
long1 = maFunction(maTypeInput, close, long2)

// Отображение графиков
plot(short, color=color.new(color.red, 0), linewidth=3)
plot(long1, color=color.new(color.green, 0), linewidth=3)
plot(ta.cross(short, long1) ? short : na, style=plot.style_cross, linewidth=4)

C_DownTrend = true
C_UpTrend = true
var trendRule1 = "SMA50"
var trendRule2 = "SMA50, SMA200"
var trendRule = input.string(trendRule1, "Detect Trend Based On", options=[trendRule1, trendRule2, "No detection"])

if trendRule == trendRule1
	priceAvg = ta.sma(close, 50)
	C_DownTrend := close < priceAvg
	C_UpTrend := close > priceAvg

if trendRule == trendRule2
	sma200 = ta.sma(close, 200)
	sma50 = ta.sma(close, 50)
	C_DownTrend := close < sma50 and sma50 < sma200
	C_UpTrend := close > sma50 and sma50 > sma200
C_Len = 14 // ta.ema depth for bodyAvg
C_ShadowPercent = 5.0 // size of shadows
C_ShadowEqualsPercent = 100.0
C_DojiBodyPercent = 5.0
C_Factor = 2.0 // shows the number of times the shadow dominates the candlestick body

C_BodyHi = math.max(close, open)
C_BodyLo = math.min(close, open)
C_Body = C_BodyHi - C_BodyLo
C_BodyAvg = ta.ema(C_Body, C_Len)
C_SmallBody = C_Body < C_BodyAvg
C_LongBody = C_Body > C_BodyAvg
C_UpShadow = high - C_BodyHi
C_DnShadow = C_BodyLo - low
C_HasUpShadow = C_UpShadow > C_ShadowPercent / 100 * C_Body
C_HasDnShadow = C_DnShadow > C_ShadowPercent / 100 * C_Body
C_WhiteBody = open < close
C_BlackBody = open > close
C_Range = high-low
C_IsInsideBar = C_BodyHi[1] > C_BodyHi and C_BodyLo[1] < C_BodyLo
C_BodyMiddle = C_Body / 2 + C_BodyLo
C_ShadowEquals = C_UpShadow == C_DnShadow or (math.abs(C_UpShadow - C_DnShadow) / C_DnShadow * 100) < C_ShadowEqualsPercent and (math.abs(C_DnShadow - C_UpShadow) / C_UpShadow * 100) < C_ShadowEqualsPercent
C_IsDojiBody = C_Range > 0 and C_Body <= C_Range * C_DojiBodyPercent / 100
C_Doji = C_IsDojiBody and C_ShadowEquals

patternLabelPosLow = low - (ta.atr(30) * 0.6)
patternLabelPosHigh = high + (ta.atr(30) * 0.6)

label_color_bearish = input(color.red, "Label Color Bearish")
C_TweezerTopBearishNumberOfCandles = 2
C_TweezerTopBearish = false
if C_UpTrend[1] and (not C_IsDojiBody or (C_HasUpShadow and C_HasDnShadow)) and math.abs(high-high[1]) <= C_BodyAvg*0.05 and C_WhiteBody[1] and C_BlackBody and C_LongBody[1]
	C_TweezerTopBearish := true
		
		
direction = 0  //input(1, title = "Strategy Direction \ Long = 1 \ Short = -1 ", type=input.integer, minval=-1, maxval=1)
strategy.risk.allow_entry_in(direction == 0 ? strategy.direction.all : direction < 0 ? strategy.direction.short : strategy.direction.long)

/////////////////////// STRATEGY INPUTS ////////////////////////////////////////
title1 = false  //input(false, "-----------------Strategy Inputs-------------------")  

barsizeThreshold = input.float(0, step=.1, minval=.0, maxval=99.9, title='Размер тела')
period = input(500, title='Период Баров')
mult = input.float(0, step=.2, title='Determinate')
i_Confirmation = true  //input(true, title="Enter trade after confirmation bar")

/////////////////////// BACKTESTER /////////////////////////////////////////////
title2 = true  //input(true, "-----------------General Inputs-------------------")  

// Backtester General Inputs
i_SL = true  //input(true, title="Use Stop Loss and Take Profit")
i_SLType = 'Strategy Stop'  //input(defval="Strategy Stop", title="Type Of Stop", options=["Strategy Stop", "Swing Lo/Hi", "ATR Stop"])
i_SPL = 10  //input(defval=10, title="Swing Point Lookback")
i_PercIncrement = 3  //input(defval=3, step=.1, title="Swing Point SL Perc Increment")*0.01
i_ATR = 14  //input(14, title="ATR Length")
i_ATRMult = 1  //input(4, step=.1, title="ATR Multiple")
i_TPRRR = 1  // input(1, step=.1, title="Take Profit Risk Reward Ratio")
TS = false  //input(false, title="Trailing Stop")
tpplus = input.float(2, step=0.1, title='% Profit LONG')

// Bought and Sold Boolean Signal
bought = strategy.position_size > strategy.position_size[1] or strategy.position_size < strategy.position_size[1]

// Price Action Stop and Take Profit
LL = ta.lowest(i_SPL) * (1 - i_PercIncrement)
HH = ta.highest(i_SPL) * (1 + i_PercIncrement)
LL_price = ta.valuewhen(bought, LL, 0)
HH_price = ta.valuewhen(bought, HH, 0)
entry_LL_price = strategy.position_size > 0 ? LL_price : na
entry_HH_price = strategy.position_size < 0 ? HH_price : na
tp = strategy.position_avg_price + (strategy.position_avg_price - entry_LL_price) * i_TPRRR
stp = strategy.position_avg_price - (entry_HH_price - strategy.position_avg_price) * i_TPRRR
tpplus1 = tpplus * 0.01
tpplus3 = tpplus2 * 0.01
// ATR Stop
ATR = ta.atr(i_ATR) * i_ATRMult
ATRLong = ohlc4 - ATR
ATRShort = ohlc4 + ATR
ATRLongStop = ta.valuewhen(bought, ATRLong, 0)
ATRShortStop = ta.valuewhen(bought, ATRShort, 0)
LongSL_ATR_price = strategy.position_size > 0 ? ATRLongStop : na
ShortSL_ATR_price = strategy.position_size < 0 ? ATRShortStop : na
ATRtp = strategy.position_avg_price + (strategy.position_avg_price - LongSL_ATR_price) * i_TPRRR
ATRstp = strategy.position_avg_price - (ShortSL_ATR_price - strategy.position_avg_price) * i_TPRRR
ss23 = strategy.position_avg_price * (1 + tpplus1)
ss25 = strategy.position_avg_price * (1 - tpplus3)
ss24 = strategy.position_avg_price



/////////////////////// STRATEGY LOGIC /////////////////////////////////////////
pct_min_barsize_threshold = input.float(0, title='Threshold', step=0.01)
min_barsize_threshold = close * pct_min_barsize_threshold * 0.01


barsize = high - low
barbodysize = close > open ? (open - close) * -1 : open - close
barsizeavg = math.sum(barsize, period) / period
bigbar = barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold
barcolor(bigbar ? color.white : na)

// Strategy Stop
barsizemult = 1  //input(1, step=.1, title="Strategy SL/TP Mult")
float LongStop = ss23
float ShortStop = ss25
float StratTP = ss23
float StratSTP = ss25


pct_close1 =0.1// input.float(0.1, title='Candles for COTI 0.12% (in percentage)', step=0.01)
pct_high1 = 0.1//input.float(0.10, title='0.40% def (in percentage)', step=0.01)
pct_sshigh1 = 0.1//input.float(0.10, title='0.50% def (in percentage)', step=0.01)


close1 = close * pct_close1 * 0.01
high1 = close * pct_high1 * 0.01
sshigh1 = close * pct_sshigh1 * 0.01


candr = high - low
bodyr = open - close
ss1 = open > close  // ниже
ss2 = close > low  // цена закрытия должна быть ниже
ss3 = open - close > close1
ss4 = close - low > high1
ss5 = open > close and high - open < sshigh1
ss = ss1 and ss2 and ss3 and ss4 and ss5
ss6 = ss[1] ? false : true
ss11 = ss1 and ss2 and ss3 and ss4 and ss5 and ss6
sss11 = false

BUY = 2 < 1
SELL = high > 100000000000000000
SELL1 = high > 100000000000000000

// Добавьте зеркальные условия для короткой позиции
ss212 = open < close
ss222 = close < high
ss232 = close - open > close1
ss242 = high - close > high1
ss252 = open < close and open - low < sshigh1
ss_short = ss212 and ss222 and ss232 and ss242 and ss252
ss262 = ss_short[1] ? false : true
ss_short_condition = ss212 and ss222 and ss232 and ss242 and ss252 and ss262

sisa = tsi_value
sisa2 = input(-30,title="Тренд ")

if strategy.position_size > 0 or strategy.position_size < 0
    BUY := C_TweezerTopBearish and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and sisa < sisa2 and barstate.isconfirmed
    SELL := high > 100000000000000000 and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and barstate.isconfirmed
    SELL1 := C_TweezerTopBearish and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and sisa < sisa2 and barstate.isconfirmed
    SELL1

else if strategy.position_size == 0
    BUY := C_TweezerTopBearish and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and sisa < sisa2 and barstate.isconfirmed
    SELL := high > 100000000000000000 and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and barstate.isconfirmed
    SELL1 := C_TweezerTopBearish and barsize >= barsizeavg * mult and barbodysize > barsize * barsizeThreshold and barsize > min_barsize_threshold and sisa < sisa2 and barstate.isconfirmed
    SELL1

//Trading Inputs
DPR = true  //input(true, "Allow Direct Position Reverse")
reverse = input(false, ' if SHORT  then TRUE')

    
startYear = input(2021, title="Start Year")
startMonth = input(11, title="Start Month")
startDay = input(1, title="Start Day")

if (time >= timestamp(startYear, startMonth, startDay, 00, 00))
// Entries
    if reverse
        if not DPR
            strategy.entry('long', strategy.long, when=SELL and strategy.position_size == 0)
            strategy.entry('short', strategy.short, when=BUY and strategy.position_size == 0)
        else
            strategy.entry('long', strategy.long, when=SELL)
            strategy.entry('short', strategy.short, when=SELL1)
    else
        if not DPR
            strategy.entry('long', strategy.long, when=BUY and strategy.position_size == 0)
            strategy.entry('short', strategy.short, when=SELL and strategy.position_size == 0)
        else
            strategy.entry('long', strategy.long, when=BUY)
            strategy.entry('short', strategy.short, when=SELL)


SL = i_SLType == 'Swing Lo/Hi' ? entry_LL_price : i_SLType == 'ATR Stop' ? LongSL_ATR_price : LongStop
SSL = i_SLType == 'Swing Lo/Hi' ? entry_HH_price : i_SLType == 'ATR Stop' ? ShortSL_ATR_price : ShortStop
TP = i_SLType == 'Swing Lo/Hi' ? tp : i_SLType == 'ATR Stop' ? ATRtp : StratTP
STP = i_SLType == 'Swing Lo/Hi' ? stp : i_SLType == 'ATR Stop' ? ATRstp : StratSTP

//TrailingStop
dif = ta.valuewhen(strategy.position_size > 0 and strategy.position_size[1] <= 0, high, 0) - strategy.position_avg_price
trailOffset = strategy.position_avg_price - SL
var tstop = float(na)
if strategy.position_size > 0
    tstop := high - trailOffset - dif
    if tstop < tstop[1]
        tstop := tstop[1]
        tstop
else
    tstop := na
    tstop
StrailOffset = SSL - strategy.position_avg_price
var Ststop = float(na)
Sdif = strategy.position_avg_price - ta.valuewhen(strategy.position_size < 0 and strategy.position_size[1] >= 0, low, 0)
if strategy.position_size < 0
    Ststop := low + StrailOffset + Sdif
    if Ststop > Ststop[1]
        Ststop := Ststop[1]
        Ststop
else
    Ststop := na
    Ststop
reverse1 = input(true, ' % ТП')
reverse2 = input(false, ' ТП по cross Скользящим')
if reverse1==false
    if reverse2==false
        strategy.close('long', when=ta.crossunder(short, long1) and strategy.position_size > 0 and close > strategy.position_avg_price)
    else
        strategy.close('long', when=ta.crossunder(short, long1) and strategy.position_size > 0 and close > strategy.position_avg_price)
        strategy.close('long', when=ta.crossover(short, long1) and strategy.position_size > 0 and close > strategy.position_avg_price)
else 
    strategy.exit('TP & SL', 'long', stop = STP, limit=TP, when=i_SL)
if reverse==true
    strategy.exit('TP & SL', 'short', stop = TP, limit=STP, when=i_SL)
/////////////////////// PLOTS //////////////////////////////////////////////////

// Определяем значение для графика с помощью тернарного оператора
lineToPlot = (reverse1 and strategy.position_size > 0) ? TP : na

// Рисуем график в глобальной области видимости
plot(lineToPlot, title='TP', style=plot.style_linebr, color=color.new(color.green, 0))

plot(i_SL and strategy.position_size > 0 or strategy.position_size < 0 ? ss24 : na, title='AVG', style=plot.style_linebr, color=color.new(color.yellow, 0))

// Draw price action setup arrows
plotshape(BUY ? 1 : na, style=shape.triangleup, location=location.belowbar, color=color.new(color.green, 0), title='Bullish', size=size.auto)
plotshape(SELL ? 1 : na, style=shape.triangledown, location=location.abovebar, color=color.new(color.red, 0), title='Bearish', size=size.auto)

barcolor(ss11 ? color.yellow : na)


