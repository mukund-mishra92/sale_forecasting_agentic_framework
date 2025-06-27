def recommend_model(analysis: dict) -> str:
    trend = analysis["trend_strength"]
    seasonality = analysis["seasonality_strength"]

    if trend > 0.6 and seasonality > 0.6:
        return "🔮 Use Prophet or SARIMA (both trend & seasonality present)."
    elif trend > 0.6:
        return "📈 Use linear regression or Prophet (strong trend, weak seasonality)."
    elif seasonality > 0.6:
        return "🔁 Use seasonal models like SARIMA (strong seasonality)."
    else:
        return "🤷 Use simple models like ARIMA or exponential smoothing (weak pattern)."
