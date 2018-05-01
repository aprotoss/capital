# -*- coding: utf-8 -*-
'''
Produce By Captal Python API Generater 
** Do not change this file ** 
'''
'''
CLSID - CoClass
'''
CLSID_RequestOverSeaFutureRight = '{E3D827CD-3833-4B99-BB91-B510371DF6EC}'
CLSID_SKCenterLib = '{AC30BAB5-194A-4515-A8D3-6260749F8577}'
CLSID_SKOOQuoteLib = '{853EC706-F437-46E2-80E0-896901A5B490}'
CLSID_SKOSQuoteLib = '{E3CB8A7C-896F-4828-85FC-8975E56BA2C4}'
CLSID_SKOrderLib = '{54FE0E28-89B6-43A7-9F07-BE988BB40299}'
CLSID_SKQuoteLib = '{E7BCB8BB-E1F0-4F6F-A944-2679195E5807}'
CLSID_SKReplyLib = '{72D98963-03E9-42AB-B997-BB2E5CCE78DD}'


'''
CoClasse Event
'''
class SKCenterLibEvents(object):
    def OnTimer(self, nTime): 
        print('SKCenterLibEvents: OnTimer')

    def OnShowAgreement(self, bstrData): 
        print('SKCenterLibEvents: OnShowAgreement')


class SKOOQuoteLibEvents(object):
    def OnConnect(self, nCode, nSocketCode): 
        print('SKOOQuoteLibEvents: OnConnect')

    def OnProducts(self, bstrValue): 
        print('SKOOQuoteLibEvents: OnProducts')

    def OnNotifyQuote(self, sIndex): 
        print('SKOOQuoteLibEvents: OnNotifyQuote')

    def OnNotifyTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('SKOOQuoteLibEvents: OnNotifyTicks')

    def OnNotifyHistoryTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('SKOOQuoteLibEvents: OnNotifyHistoryTicks')

    def OnNotifyBest5(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5): 
        print('SKOOQuoteLibEvents: OnNotifyBest5')

    def OnNotifyBest10(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestBid6, nBestBidQty6, nBestBid7
            , nBestBidQty7, nBestBid8, nBestBidQty8, nBestBid9, nBestBidQty9
            , nBestBid10, nBestBidQty10, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5, nBestAsk6, nBestAskQty6, nBestAsk7
            , nBestAskQty7, nBestAsk8, nBestAskQty8, nBestAsk9, nBestAskQty9
            , nBestAsk10, nBestAskQty10): 
        print('SKOOQuoteLibEvents: OnNotifyBest10')


class SKOSQuoteLibEvents(object):
    def OnConnect(self, nCode, nSocketCode): 
        print('SKOSQuoteLibEvents: OnConnect')

    def OnNotifyTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('SKOSQuoteLibEvents: OnNotifyTicks')

    def OnNotifyHistoryTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('SKOSQuoteLibEvents: OnNotifyHistoryTicks')

    def OnNotifyBest5(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5): 
        print('SKOSQuoteLibEvents: OnNotifyBest5')

    def OnOverseaProducts(self, bstrValue): 
        print('SKOSQuoteLibEvents: OnOverseaProducts')

    def OnKLineData(self, bstrStockNo, bstrData): 
        print('SKOSQuoteLibEvents: OnKLineData')

    def OnNotifyServerTime(self, sHour, sMinute, sSecond): 
        print('SKOSQuoteLibEvents: OnNotifyServerTime')

    def OnNotifyQuote(self, sStockIdx): 
        print('SKOSQuoteLibEvents: OnNotifyQuote')

    def OnOverseaProductsDetail(self, bstrValue): 
        print('SKOSQuoteLibEvents: OnOverseaProductsDetail')

    def OnNotifyBest10(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestBid6, nBestBidQty6, nBestBid7
            , nBestBidQty7, nBestBid8, nBestBidQty8, nBestBid9, nBestBidQty9
            , nBestBid10, nBestBidQty10, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5, nBestAsk6, nBestAskQty6, nBestAsk7
            , nBestAskQty7, nBestAsk8, nBestAskQty8, nBestAsk9, nBestAskQty9
            , nBestAsk10, nBestAskQty10): 
        print('SKOSQuoteLibEvents: OnNotifyBest10')


class SKOrderLibEvents(object):
    def OnAccount(self, bstrLogInID, bstrAccountData): 
        print('SKOrderLibEvents: OnAccount')

    def OnAsyncOrder(self, nThreaID, nCode, bstrMessage): 
        print('SKOrderLibEvents: OnAsyncOrder')

    def OnRealBalanceReport(self, bstrData): 
        print('SKOrderLibEvents: OnRealBalanceReport')

    def OnOpenInterest(self, bstrData): 
        print('SKOrderLibEvents: OnOpenInterest')

    def OnOverseaFutureOpenInterest(self, bstrData): 
        print('SKOrderLibEvents: OnOverseaFutureOpenInterest')

    def OnStopLossReport(self, bstrData): 
        print('SKOrderLibEvents: OnStopLossReport')

    def OnOverseaFuture(self, bstrData): 
        print('SKOrderLibEvents: OnOverseaFuture')

    def OnOverseaOption(self, bstrData): 
        print('SKOrderLibEvents: OnOverseaOption')

    def OnFutureRights(self, bstrData): 
        print('SKOrderLibEvents: OnFutureRights')

    def OnOrderIPData(self, bstrOrderIPData): 
        print('SKOrderLibEvents: OnOrderIPData')

    def OnRequestProfitReport(self, bstrData): 
        print('SKOrderLibEvents: OnRequestProfitReport')

    def OnOverSeaFutureRight(self, bstrData): 
        print('SKOrderLibEvents: OnOverSeaFutureRight')

    def OnMarginPurchaseAmountLimit(self, bstrData): 
        print('SKOrderLibEvents: OnMarginPurchaseAmountLimit')

    def OnBalanceQuery(self, bstrData): 
        print('SKOrderLibEvents: OnBalanceQuery')


class SKQuoteLibEvents(object):
    def OnConnection(self, nKind, nCode): 
        print('SKQuoteLibEvents: OnConnection')

    def OnNotifyQuote(self, sMarketNo, sStockIdx): 
        print('SKQuoteLibEvents: OnNotifyQuote')

    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, nTimehms
            , nTimemillismicros, nBid, nAsk, nClose, nQty
            , nSimulate): 
        print('SKQuoteLibEvents: OnNotifyHistoryTicks')

    def OnNotifyTicks(self, sMarketNo, sIndex, nPtr, nTimehms
            , nTimemillismicros, nBid, nAsk, nClose, nQty
            , nSimulate): 
        print('SKQuoteLibEvents: OnNotifyTicks')

    def OnNotifyBest5(self, sMarketNo, sStockIdx, nBestBid1, nBestBidQty1
            , nBestBid2, nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4
            , nBestBidQty4, nBestBid5, nBestBidQty5, nExtendBid, nExtendBidQty
            , nBestAsk1, nBestAskQty1, nBestAsk2, nBestAskQty2, nBestAsk3
            , nBestAskQty3, nBestAsk4, nBestAskQty4, nBestAsk5, nBestAskQty5
            , nExtendAsk, nExtendAskQty, nSimulate): 
        print('SKQuoteLibEvents: OnNotifyBest5')

    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        print('SKQuoteLibEvents: OnNotifyKLineData')

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        print('SKQuoteLibEvents: OnNotifyServerTime')

    def OnNotifyMarketTot(self, sMarketNo, sPrt, nTime, nTotv
            , nTots, nTotc): 
        print('SKQuoteLibEvents: OnNotifyMarketTot')

    def OnNotifyMarketBuySell(self, sMarketNo, sPrt, nTime, nBc
            , nSc, nBs, nSs): 
        print('SKQuoteLibEvents: OnNotifyMarketBuySell')

    def OnNotifyMarketHighLow(self, sMarketNo, sPrt, nTime, sUp
            , sDown, sHigh, sLow, sNoChange): 
        print('SKQuoteLibEvents: OnNotifyMarketHighLow')

    def OnMarketClear(self, nKind, nCode): 
        print('SKQuoteLibEvents: OnMarketClear')

    def OnNotifyMACD(self, sMarketNo, sStockIdx, bstrMACD, bstrDIF
            , bstrOSC): 
        print('SKQuoteLibEvents: OnNotifyMACD')

    def OnNotifyBoolTunel(self, sMarketNo, sStockIdx, bstrAVG, bstrUBT
            , bstrLBT): 
        print('SKQuoteLibEvents: OnNotifyBoolTunel')

    def OnNotifyFutureTradeInfo(self, bstrStockNo, sMarketNo, sStockIdx, nBuyTotalCount
            , nSellTotalCount, nBuyTotalQty, nSellTotalQty, nBuyDealTotalCount, nSellDealTotalCount): 
        print('SKQuoteLibEvents: OnNotifyFutureTradeInfo')

    def OnNotifyStrikePrices(self, bstrOptionData): 
        print('SKQuoteLibEvents: OnNotifyStrikePrices')

    def OnNotifyStockList(self, sMarketNo, bstrStockData): 
        print('SKQuoteLibEvents: OnNotifyStockList')


class SKReplyLibEvents(object):
    def OnConnect(self, bstrUserID, nErrorCode): 
        print('SKReplyLibEvents: OnConnect')

    def OnDisconnect(self, bstrUserID, nErrorCode): 
        print('SKReplyLibEvents: OnDisconnect')

    def OnComplete(self, bstrUserID): 
        print('SKReplyLibEvents: OnComplete')

    def OnData(self, bstrUserID, bstrData): 
        print('SKReplyLibEvents: OnData')

    def OnReportCount(self, bstrUserID, nCount): 
        print('SKReplyLibEvents: OnReportCount')

    def OnReplyMessage(self, bstrUserID, bstrMessage): 
        print('SKReplyLibEvents: OnReplyMessage')

    def OnReplyClear(self, bstrMarket): 
        print('SKReplyLibEvents: OnReplyClear')

    def OnNewData(self, bstrUserID, bstrData): 
        print('SKReplyLibEvents: OnNewData')

    def OnSolaceReplyConnection(self, bstrUserID, nErrorCode): 
        print('SKReplyLibEvents: OnSolaceReplyConnection')

    def OnSolaceReplyDisconnect(self, bstrUserID, nErrorCode): 
        print('SKReplyLibEvents: OnSolaceReplyDisconnect')

    def OnReplyClearMessage(self, bstrUserUD): 
        print('SKReplyLibEvents: OnReplyClearMessage')

    def OnSmartData(self, bstrUserID, bstrData): 
        print('SKReplyLibEvents: OnSmartData')


