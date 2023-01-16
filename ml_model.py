from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import pandas as pd

def TreeRegressor(train_x,train_y):
    ml_model = DecisionTreeRegressor(random_state=1,max_depth=3)
    
    ml_model = ml_model.fit(train_x, train_y)

    plot_tree(ml_model)
    plt.show()
    '''
    predictions = ml_model.predict(test_x)

    print ("Machine learning completed:")
    print ("Prediction:", predictions)
    print ("Mean absolute error:", mean_absolute_error(test_y,predictions))
    plot.line_ml_comparison(test_y,predictions)
    df = pd.DataFrame (predictions,columns = ["predictions"])
    df["id"] = df.index + 1

    return (predictions, df)
    '''