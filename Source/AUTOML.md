## AUTOML

###Methods from Paper

| Model                                                | Advatage                                                     | Disvantage                                       | Data sets                                    | Paper                                                        |
| ---------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| FE using RL                                          | reduce error rate / small computational budget               | missing value imputation / no model selection    | 48 datasets from OpemML and UCIrvine         | Feature Engineering for Predictive Modeling using Reinforcement Learning |
| APRL                                                 | reduce error / better than auto-sklearn                      | small subsets of FE(10), model(4/3) , HPO(1)     | 56 binary classfication datasets from OpenML | Automating Predictive Modeling Process using Reinforcement Learning |
| DAUB                                                 | low cost / robust / fast                                     | only model selection / need better bound, split. | HIGGS/PARITY                                 | Selecting Near-Optimal Learners via Incremental Data Allocation |
| Cognito                                              | explore various feature construction in a hierarchical and non-exhaustive manner while progressively maximizing the accuracy of the model | only FE in supervised Learning                   | UCI ML  LIBSVM                               | Cognito: Automated Feature Engineering for Supervised Learning |
| Meta Learning for time series combination            | ranking based combination of methods over simple model selection approaches | only model selection                             | NN3 / NN5                                    | Meta-learning for time series forecasting and forecast combination |
| Meta Learning Approach to Select times series models | use of meta learning in time series forecasting              | only model selection                             | M3-Competition                               | Meta-learning approaches to selecting time series models     |



###AutoML System

| Name         | Method                                                       | Feature - Transformation | Model Selection | Hpyerparameter Optimization             | Classification or Regression |
| ------------ | ------------------------------------------------------------ | ------------------------ | --------------- | --------------------------------------- | ---------------------------- |
| Auto-WEKA    | 2 ensemble methods, 10 meta-methods, 28 base learners, and hyperparameter settings for each learner. |                          | ✅               | ✅                                       | Classification               |
| Hyperopt     | define a search space that encompasses many standard components (e.g. SVM, RF, KNN, PCA, TFIDF) and common patterns of composing them together |                          |                 | ✅                                       |                              |
| Auto-Sklearn | 15 classifiers, 14 feature preprocessing methods, and 4 data preprocessing methods, giving rise to a structured hypothesis space with 110 hyperparameters | ✅                        | ✅               | ✅                                       | Classification/ Regression   |
| TPOT         | genetic programming-based                                    | ✅                        | ✅               |                                         | Classification               |
| STATLOG      | Meta Learning                                                | 16 meta feature          | Decision Tree   | 20 ML-algorithms / 22 benchmark problem | Classification               |
| NOEMON       | Meta Learning                                                | base learner pair(X,Y)   | ✅               |                                         |                              |
| MAML         | Meta Learning: NN 找初始值                                   |                          |                 |                                         |                              |