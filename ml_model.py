from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
import plot
import pandas as pd

def TreeRegressor(train_x,train_y,test_x,test_y):
    ml_model = DecisionTreeRegressor(random_state=1)
    ml_model.fit(train_x, train_y)
    predictions = ml_model.predict(test_x)

    print ("Machine learning completed:")
    print ("Prediction:", predictions)
    print ("Mean absolute error:", mean_absolute_error(test_y,predictions))
    plot.line_ml_comparison(test_y,predictions)
    df = pd.DataFrame (predictions,columns = ["predictions"])
    df["id"] = df.index + 1
    return (predictions, df)