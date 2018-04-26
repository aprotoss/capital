# -*- coding: utf-8 -*-
'''
 Capital Python API Generater 
'''
'''
CLSID 
'''
CLSID_RequestOverSeaFutureRight = '{E3D827CD-3833-4B99-BB91-B510371DF6EC}'
CLSID_SKCenterLib = '{AC30BAB5-194A-4515-A8D3-6260749F8577}'
CLSID_SKOOQuoteLib = '{853EC706-F437-46E2-80E0-896901A5B490}'
CLSID_SKOSQuoteLib = '{E3CB8A7C-896F-4828-85FC-8975E56BA2C4}'
CLSID_SKOrderLib = '{54FE0E28-89B6-43A7-9F07-BE988BB40299}'
CLSID_SKQuoteLib = '{E7BCB8BB-E1F0-4F6F-A944-2679195E5807}'
CLSID_SKReplyLib = '{72D98963-03E9-42AB-B997-BB2E5CCE78DD}'


'''
Event 
'''
class SKCenterLibEvents(object):
    def OnTimer(self, nTime): 
        print('Event: OnTimer')

    def OnShowAgreement(self, bstrData): 
        print('Event: OnShowAgreement')


class SKOOQuoteLibEvents(object):
    def OnConnect(self, nCode, nSocketCode): 
        print('Event: OnConnect')

    def OnProducts(self, bstrValue): 
        print('Event: OnProducts')

    def OnNotifyQuote(self, sIndex): 
        print('Event: OnNotifyQuote')

    def OnNotifyTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('Event: OnNotifyTicks')

    def OnNotifyHistoryTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('Event: OnNotifyHistoryTicks')

    def OnNotifyBest5(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5): 
        print('Event: OnNotifyBest5')

    def OnNotifyBest10(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestBid6, nBestBidQty6, nBestBid7
            , nBestBidQty7, nBestBid8, nBestBidQty8, nBestBid9, nBestBidQty9
            , nBestBid10, nBestBidQty10, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5, nBestAsk6, nBestAskQty6, nBestAsk7
            , nBestAskQty7, nBestAsk8, nBestAskQty8, nBestAsk9, nBestAskQty9
            , nBestAsk10, nBestAskQty10): 
        print('Event: OnNotifyBest10')


class SKOSQuoteLibEvents(object):
    def OnConnect(self, nCode, nSocketCode): 
        print('Event: OnConnect')

    def OnNotifyTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('Event: OnNotifyTicks')

    def OnNotifyHistoryTicks(self, sStockIdx, nPtr, nTime, nClose
            , nQty): 
        print('Event: OnNotifyHistoryTicks')

    def OnNotifyBest5(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5): 
        print('Event: OnNotifyBest5')

    def OnOverseaProducts(self, bstrValue): 
        print('Event: OnOverseaProducts')

    def OnKLineData(self, bstrStockNo, bstrData): 
        print('Event: OnKLineData')

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        print('Event: OnNotifyServerTime')

    def OnNotifyQuote(self, sStockIdx): 
        print('Event: OnNotifyQuote')

    def OnOverseaProductsDetail(self, bstrValue): 
        print('Event: OnOverseaProductsDetail')

    def OnNotifyBest10(self, sStockIdx, nBestBid1, nBestBidQty1, nBestBid2
            , nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4, nBestBidQty4
            , nBestBid5, nBestBidQty5, nBestBid6, nBestBidQty6, nBestBid7
            , nBestBidQty7, nBestBid8, nBestBidQty8, nBestBid9, nBestBidQty9
            , nBestBid10, nBestBidQty10, nBestAsk1, nBestAskQty1, nBestAsk2
            , nBestAskQty2, nBestAsk3, nBestAskQty3, nBestAsk4, nBestAskQty4
            , nBestAsk5, nBestAskQty5, nBestAsk6, nBestAskQty6, nBestAsk7
            , nBestAskQty7, nBestAsk8, nBestAskQty8, nBestAsk9, nBestAskQty9
            , nBestAsk10, nBestAskQty10): 
        print('Event: OnNotifyBest10')


class SKOrderLibEvents(object):
    def OnAccount(self, bstrLogInID, bstrAccountData): 
        print('Event: OnAccount')

    def OnAsyncOrder(self, nThreaID, nCode, bstrMessage): 
        print('Event: OnAsyncOrder')

    def OnRealBalanceReport(self, bstrData): 
        print('Event: OnRealBalanceReport')

    def OnOpenInterest(self, bstrData): 
        print('Event: OnOpenInterest')

    def OnOverseaFutureOpenInterest(self, bstrData): 
        print('Event: OnOverseaFutureOpenInterest')

    def OnStopLossReport(self, bstrData): 
        print('Event: OnStopLossReport')

    def OnOverseaFuture(self, bstrData): 
        print('Event: OnOverseaFuture')

    def OnOverseaOption(self, bstrData): 
        print('Event: OnOverseaOption')

    def OnFutureRights(self, bstrData): 
        print('Event: OnFutureRights')

    def OnOrderIPData(self, bstrOrderIPData): 
        print('Event: OnOrderIPData')

    def OnRequestProfitReport(self, bstrData): 
        print('Event: OnRequestProfitReport')

    def OnOverSeaFutureRight(self, bstrData): 
        print('Event: OnOverSeaFutureRight')

    def OnMarginPurchaseAmountLimit(self, bstrData): 
        print('Event: OnMarginPurchaseAmountLimit')

    def OnBalanceQuery(self, bstrData): 
        print('Event: OnBalanceQuery')


class SKQuoteLibEvents(object):
    def OnConnection(self, nKind, nCode): 
        print('Event: OnConnection')

    def OnNotifyQuote(self, sMarketNo, sStockIdx): 
        print('Event: OnNotifyQuote')

    def OnNotifyHistoryTicks(self, sMarketNo, sStockIdx, nPtr, nTimehms
            , nTimemillismicros, nBid, nAsk, nClose, nQty
            , nSimulate): 
        print('Event: OnNotifyHistoryTicks')

    def OnNotifyTicks(self, sMarketNo, sIndex, nPtr, nTimehms
            , nTimemillismicros, nBid, nAsk, nClose, nQty
            , nSimulate): 
        print('Event: OnNotifyTicks')

    def OnNotifyBest5(self, sMarketNo, sStockIdx, nBestBid1, nBestBidQty1
            , nBestBid2, nBestBidQty2, nBestBid3, nBestBidQty3, nBestBid4
            , nBestBidQty4, nBestBid5, nBestBidQty5, nExtendBid, nExtendBidQty
            , nBestAsk1, nBestAskQty1, nBestAsk2, nBestAskQty2, nBestAsk3
            , nBestAskQty3, nBestAsk4, nBestAskQty4, nBestAsk5, nBestAskQty5
            , nExtendAsk, nExtendAskQty, nSimulate): 
        print('Event: OnNotifyBest5')

    def OnNotifyKLineData(self, bstrStockNo, bstrData): 
        print('Event: OnNotifyKLineData')

    def OnNotifyServerTime(self, sHour, sMinute, sSecond, nTotal): 
        print('Event: OnNotifyServerTime')

    def OnNotifyMarketTot(self, sMarketNo, sPrt, nTime, nTotv
            , nTots, nTotc): 
        print('Event: OnNotifyMarketTot')

    def OnNotifyMarketBuySell(self, sMarketNo, sPrt, nTime, nBc
            , nSc, nBs, nSs): 
        print('Event: OnNotifyMarketBuySell')

    def OnNotifyMarketHighLow(self, sMarketNo, sPrt, nTime, sUp
            , sDown, sHigh, sLow, sNoChange): 
        print('Event: OnNotifyMarketHighLow')

    def OnMarketClear(self, nKind, nCode): 
        print('Event: OnMarketClear')

    def OnNotifyMACD(self, sMarketNo, sStockIdx, bstrMACD, bstrDIF
            , bstrOSC): 
        print('Event: OnNotifyMACD')

    def OnNotifyBoolTunel(self, sMarketNo, sStockIdx, bstrAVG, bstrUBT
            , bstrLBT): 
        print('Event: OnNotifyBoolTunel')

    def OnNotifyFutureTradeInfo(self, bstrStockNo, sMarketNo, sStockIdx, nBuyTotalCount
            , nSellTotalCount, nBuyTotalQty, nSellTotalQty, nBuyDealTotalCount, nSellDealTotalCount): 
        print('Event: OnNotifyFutureTradeInfo')

    def OnNotifyStrikePrices(self, bstrOptionData): 
        print('Event: OnNotifyStrikePrices')

    def OnNotifyStockList(self, sMarketNo, bstrStockData): 
        print('Event: OnNotifyStockList')


class SKReplyLibEvents(object):
    def OnConnect(self, bstrUserID, nErrorCode): 
        print('Event: OnConnect')

    def OnDisconnect(self, bstrUserID, nErrorCode): 
        print('Event: OnDisconnect')

    def OnComplete(self, bstrUserID): 
        print('Event: OnComplete')

    def OnData(self, bstrUserID, bstrData): 
        print('Event: OnData')

    def OnReportCount(self, bstrUserID, nCount): 
        print('Event: OnReportCount')

    def OnReplyMessage(self, bstrUserID, bstrMessage): 
        print('Event: OnReplyMessage')

    def OnReplyClear(self, bstrMarket): 
        print('Event: OnReplyClear')

    def OnNewData(self, bstrUserID, bstrData): 
        print('Event: OnNewData')

    def OnSolaceReplyConnection(self, bstrUserID, nErrorCode): 
        print('Event: OnSolaceReplyConnection')

    def OnSolaceReplyDisconnect(self, bstrUserID, nErrorCode): 
        print('Event: OnSolaceReplyDisconnect')

    def OnReplyClearMessage(self, bstrUserUD): 
        print('Event: OnReplyClearMessage')

    def OnSmartData(self, bstrUserID, bstrData): 
        print('Event: OnSmartData')


