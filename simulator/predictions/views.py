from django.shortcuts import render, redirect
from .forms import PredictionForm
from .models import Predictions


def predictions(request):
    import yfinance as yf

    if request.method == "POST":
        #should check if the stock already exists SHOULD NOT ADD THE SAME STOCK TWICE
        pred_ticker = Predictions.objects.all().values('ticker')
        for pred in pred_ticker:
            if pred['ticker'] == request.POST:
                return redirect('predictions')

        form = PredictionForm(request.POST or None)

        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            return redirect('predictions')
    else:
        ticker = Predictions.objects.all()
        output = []
        for ticker_item in ticker:
            tick = yf.Ticker(str(ticker_item))
            api = tick.info

            # if api.get("currentPrice") is None:
            #     api = "Error"
            # else:
            output.append(api)

        return render(request, 'predictions.html', {'output': output})

 # if request.method == "POST":
 #        get_ticker = request.POST['ticker']
 #
 #        ticker = yf.Ticker(get_ticker)
 #        api = ticker.info
 #
 #        if api.get("currentPrice") is None:
 #            api = "Error"

